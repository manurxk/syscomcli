"""Formato estándar de los manuales de SYSCLIN en Word (IEEE Std 1063-2001 / ISO/IEC 26514:2008).

Define una sola vez portada, control del documento, historial, índice, estilos (Times New Roman 12 justificado
con interlineado 1,5; títulos 14 en negrita numerados 1., 1.1, 1.1.1; Nota; Advertencia; tablas; código),
encabezado y pie. El manual se arma en Word y el PDF se exporta desde ese mismo Word con LibreOffice, así
el PDF y el Word son siempre iguales.

Solo depende de python-docx (sin Flask), para que los scripts de docs/scripts también puedan usarlo.
"""
import os
import re
import shutil
import subprocess
import tempfile
from html.parser import HTMLParser
from io import BytesIO

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

LETRA = 'Times New Roman'
LETRA_CODIGO = 'Consolas'
NEGRO = RGBColor(0, 0, 0)
GRIS_TABLA = 'D9D9D9'
VERSION = '1.0'
ANCHO_UTIL_CM = 21 - 2.5 - 2  # A4 menos márgenes izquierdo y derecho

# Conversión a PDF: script UNO que corre con el Python del sistema (python3-uno), no con el de la app
SCRIPT_UNO = os.path.join(os.path.dirname(__file__), 'uno_docx_a_pdf.py')
PYTHON_UNO = '/usr/bin/python3'


# ---------------------------------------------------------------- utilidades XML

# Orden de hijos que exige el esquema de Word (si no se respeta, Word dice que el archivo está dañado)
DESPUES_PBDR = ('w:shd', 'w:tabs', 'w:suppressAutoHyphens', 'w:kinsoku', 'w:wordWrap', 'w:overflowPunct',
                'w:topLinePunct', 'w:autoSpaceDE', 'w:autoSpaceDN', 'w:bidi', 'w:adjustRightInd', 'w:snapToGrid',
                'w:spacing', 'w:ind', 'w:contextualSpacing', 'w:mirrorIndents', 'w:suppressOverlap', 'w:jc',
                'w:textDirection', 'w:textAlignment', 'w:textboxTightWrap', 'w:outlineLvl', 'w:divId',
                'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange')
DESPUES_NUMPR = ('w:suppressLineNumbers', 'w:pBdr') + DESPUES_PBDR
DESPUES_SHD_CELDA = ('w:noWrap', 'w:tcMar', 'w:textDirection', 'w:tcFitText', 'w:vAlign', 'w:hideMark')


def insertar(padre, hijo, sucesores):
    """Inserta hijo antes del primer sucesor presente (o al final)."""
    for etiqueta in sucesores:
        siguiente = padre.find(qn(etiqueta))
        if siguiente is not None:
            siguiente.addprevious(hijo)
            return
    padre.append(hijo)


def _ppr(estilo_o_parrafo):
    elemento = getattr(estilo_o_parrafo, 'element', None)
    if elemento is None:
        elemento = estilo_o_parrafo._p
    return elemento.get_or_add_pPr()


def letra(run_o_estilo, nombre=LETRA):
    """Fija la letra en todas las variantes (latina, asiática, compleja) para que Word no la cambie."""
    rpr = run_o_estilo.element.get_or_add_rPr()
    fuentes = rpr.find(qn('w:rFonts'))
    if fuentes is None:
        fuentes = OxmlElement('w:rFonts')
        rpr.insert(0, fuentes)
    for atributo in ('w:ascii', 'w:hAnsi', 'w:cs', 'w:eastAsia'):
        fuentes.set(qn(atributo), nombre)


def borde_parrafo(estilo_o_parrafo, grosor_octavos, lados=('top', 'left', 'bottom', 'right'), espacio=4):
    ppr = _ppr(estilo_o_parrafo)
    bordes = OxmlElement('w:pBdr')
    for lado in lados:
        b = OxmlElement(f'w:{lado}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), str(grosor_octavos))
        b.set(qn('w:space'), str(espacio))
        b.set(qn('w:color'), '000000')
        bordes.append(b)
    insertar(ppr, bordes, DESPUES_PBDR)


def sombreado(elemento_pr, color, sucesores=DESPUES_PBDR[1:]):
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), color)
    insertar(elemento_pr, shd, sucesores)


def campo(parrafo, instruccion, texto_previo=''):
    """Inserta un campo de Word (PAGE, TOC, SEQ...). Word/LibreOffice lo calcula al actualizar."""
    for tipo in ('begin', None, 'separate'):
        run = parrafo.add_run()
        if tipo is None:
            instr = OxmlElement('w:instrText')
            instr.set(qn('xml:space'), 'preserve')
            instr.text = f' {instruccion} '
            run._r.append(instr)
        else:
            marca = OxmlElement('w:fldChar')
            marca.set(qn('w:fldCharType'), tipo)
            run._r.append(marca)
    parrafo.add_run(texto_previo)
    run = parrafo.add_run()
    fin = OxmlElement('w:fldChar')
    fin.set(qn('w:fldCharType'), 'end')
    run._r.append(fin)


def tab_derecha(parrafo, posicion_cm, relleno=None):
    ppr = parrafo._p.get_or_add_pPr()
    tabs = OxmlElement('w:tabs')
    tab = OxmlElement('w:tab')
    tab.set(qn('w:val'), 'right')
    tab.set(qn('w:pos'), str(int(Cm(posicion_cm).twips)))
    if relleno:
        tab.set(qn('w:leader'), relleno)
    tabs.append(tab)
    insertar(ppr, tabs, DESPUES_PBDR[2:])


# ---------------------------------------------------------------- estilos

def _numeracion_titulos(doc):
    """Lista multinivel 1. / 1.1 / 1.1.1 enlazada a Título 1-3: se numeran solos los capítulos."""
    numbering = doc.part.numbering_part.element
    abstract = OxmlElement('w:abstractNum')
    abstract.set(qn('w:abstractNumId'), '90')
    for nivel, formato in enumerate(('%1.', '%1.%2', '%1.%2.%3')):
        lvl = OxmlElement('w:lvl')
        lvl.set(qn('w:ilvl'), str(nivel))
        for etiqueta, valor in (('w:start', '1'), ('w:numFmt', 'decimal'),
                                ('w:pStyle', f'Heading{nivel + 1}'), ('w:lvlText', formato),
                                ('w:lvlJc', 'left')):
            e = OxmlElement(etiqueta)
            e.set(qn('w:val'), valor)
            lvl.append(e)
        ppr = OxmlElement('w:pPr')
        ind = OxmlElement('w:ind')
        sangria = int(Cm(0.9 + 0.3 * nivel).twips)
        ind.set(qn('w:left'), str(sangria))
        ind.set(qn('w:hanging'), str(sangria))
        ppr.append(ind)
        lvl.append(ppr)
        abstract.append(lvl)
    # abstractNum debe ir antes de los w:num
    primer_num = numbering.find(qn('w:num'))
    if primer_num is not None:
        primer_num.addprevious(abstract)
    else:
        numbering.append(abstract)
    num = OxmlElement('w:num')
    num.set(qn('w:numId'), '90')
    ref = OxmlElement('w:abstractNumId')
    ref.set(qn('w:val'), '90')
    num.append(ref)
    numbering.append(num)
    for nivel in range(3):
        ppr = doc.styles[f'Heading {nivel + 1}'].element.get_or_add_pPr()
        numpr = OxmlElement('w:numPr')
        ilvl = OxmlElement('w:ilvl')
        ilvl.set(qn('w:val'), str(nivel))
        numid = OxmlElement('w:numId')
        numid.set(qn('w:val'), '90')
        numpr.append(ilvl)
        numpr.append(numid)
        insertar(ppr, numpr, DESPUES_NUMPR)


def _estilos_anexo(doc):
    """Títulos del anexo: mismo formato que Título 1/2 pero sin número (el anexo se rotula A, A.1...)."""
    for nombre, base, nivel in (('Título de anexo', 'Heading 1', 0), ('Título de anexo 2', 'Heading 2', 1)):
        e = doc.styles.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        e.base_style = doc.styles[base]
        ppr = e.element.get_or_add_pPr()
        numpr = OxmlElement('w:numPr')
        numid = OxmlElement('w:numId')
        numid.set(qn('w:val'), '0')
        numpr.append(numid)
        insertar(ppr, numpr, DESPUES_NUMPR)
        nivel_esquema = OxmlElement('w:outlineLvl')
        nivel_esquema.set(qn('w:val'), str(nivel))
        insertar(ppr, nivel_esquema, ('w:divId', 'w:cnfStyle', 'w:rPr', 'w:sectPr', 'w:pPrChange'))


def _estilos_densos(doc):
    """Manual de usuario: letra 11, interlineado simple y espacios cortos, para que entren dos pantallas por hoja.
    Cada capítulo (módulo) sigue empezando en hoja nueva."""
    estilos = doc.styles
    normal = estilos['Normal']
    normal.font.size = Pt(11)
    normal.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    normal.paragraph_format.space_after = Pt(3)
    for nivel in (1, 2, 3):
        t = estilos[f'Heading {nivel}']
        t.font.size = Pt(14 if nivel == 1 else 12)
        t.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
        t.paragraph_format.space_before = Pt(14 if nivel == 1 else 10)
        t.paragraph_format.space_after = Pt(4)
    for nombre in ('List Number', 'List Bullet'):
        estilos[nombre].font.size = Pt(11)
        estilos[nombre].paragraph_format.space_after = Pt(1)
    estilos['Caption'].font.size = Pt(9)
    estilos['Caption'].paragraph_format.space_after = Pt(4)
    for nombre in ('Nota', 'Advertencia'):
        estilos[nombre].paragraph_format.space_before = Pt(3)
        estilos[nombre].paragraph_format.space_after = Pt(5)


def _estilos(doc):
    estilos = doc.styles

    normal = estilos['Normal']
    normal.font.name = LETRA
    normal.font.size = Pt(12)
    normal.font.color.rgb = NEGRO
    letra(normal)
    pf = normal.paragraph_format
    pf.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)

    for nivel in (1, 2, 3):
        t = estilos[f'Heading {nivel}']
        t.font.name = LETRA
        t.font.size = Pt(14)
        t.font.bold = True
        t.font.italic = False
        t.font.color.rgb = NEGRO
        letra(t)
        t.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        t.paragraph_format.space_before = Pt(18 if nivel == 1 else 12)
        t.paragraph_format.space_after = Pt(6)
        t.paragraph_format.keep_with_next = True
        t.paragraph_format.line_spacing_rule = WD_LINE_SPACING.ONE_POINT_FIVE
    # Cada capítulo empieza en hoja nueva
    estilos['Heading 1'].paragraph_format.page_break_before = True
    _numeracion_titulos(doc)
    _estilos_anexo(doc)

    # Títulos sin número (control del documento, índice): no aparecen en el índice
    sin_num = estilos.add_style('Título sin número', WD_STYLE_TYPE.PARAGRAPH)
    sin_num.base_style = normal
    sin_num.font.size = Pt(14)
    sin_num.font.bold = True
    sin_num.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    sin_num.paragraph_format.space_before = Pt(12)
    sin_num.paragraph_format.keep_with_next = True

    portada = estilos.add_style('Portada', WD_STYLE_TYPE.PARAGRAPH)
    portada.base_style = normal
    portada.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    portada.paragraph_format.space_after = Pt(0)

    titulo_portada = estilos.add_style('Portada título', WD_STYLE_TYPE.PARAGRAPH)
    titulo_portada.base_style = portada
    titulo_portada.font.size = Pt(14)
    titulo_portada.font.bold = True

    for nombre, grosor in (('Nota', 6), ('Advertencia', 12)):
        e = estilos.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        e.base_style = normal
        e.paragraph_format.left_indent = Cm(0.2)
        e.paragraph_format.right_indent = Cm(0.2)
        e.paragraph_format.space_before = Pt(6)
        e.paragraph_format.space_after = Pt(10)
        borde_parrafo(e, grosor)

    pie_fig = estilos['Caption']
    pie_fig.font.name = LETRA
    pie_fig.font.size = Pt(12)
    pie_fig.font.italic = True
    pie_fig.font.bold = False
    pie_fig.font.color.rgb = NEGRO
    letra(pie_fig)
    pie_fig.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pie_fig.paragraph_format.space_after = Pt(12)

    figura = estilos.add_style('Figura', WD_STYLE_TYPE.PARAGRAPH)
    figura.base_style = normal
    figura.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    figura.paragraph_format.keep_with_next = True
    figura.paragraph_format.space_before = Pt(6)
    figura.paragraph_format.space_after = Pt(0)
    figura.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    tabla = estilos.add_style('Texto de tabla', WD_STYLE_TYPE.PARAGRAPH)
    tabla.base_style = normal
    tabla.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    tabla.paragraph_format.space_after = Pt(0)
    tabla.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE

    codigo = estilos.add_style('Código', WD_STYLE_TYPE.PARAGRAPH)
    codigo.base_style = normal
    codigo.font.name = LETRA_CODIGO
    codigo.font.size = Pt(9)
    letra(codigo, LETRA_CODIGO)
    codigo.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    codigo.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    codigo.paragraph_format.space_after = Pt(0)
    sombreado(codigo.element.get_or_add_pPr(), 'F2F2F2')

    for nombre in ('List Number', 'List Bullet'):
        lista = estilos[nombre]
        lista.font.name = LETRA
        lista.font.size = Pt(12)
        letra(lista)
        lista.paragraph_format.space_after = Pt(3)

    nombres = [s.name for s in estilos]
    for nivel in (1, 2, 3):
        nombre = f'TOC {nivel}'
        toc = estilos[nombre] if nombre in nombres else estilos.add_style(nombre, WD_STYLE_TYPE.PARAGRAPH)
        toc.base_style = normal
        toc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        toc.paragraph_format.left_indent = Cm(0.6 * (nivel - 1))
        toc.paragraph_format.space_after = Pt(2)

    # Marca interna del párrafo que aloja un índice (ver cerrar_indices)
    fin_indice = estilos.add_style('Fin de índice', WD_STYLE_TYPE.PARAGRAPH)
    fin_indice.base_style = normal

    for e in (estilos['Footer'], estilos['Header']):
        e.font.name = LETRA
        e.font.size = Pt(12)
        letra(e)


def nuevo_documento():
    """Documento A4 con los márgenes y estilos del estándar."""
    doc = Document()
    seccion = doc.sections[0]
    seccion.page_width = Cm(21)
    seccion.page_height = Cm(29.7)
    seccion.top_margin = Cm(2.5)
    seccion.bottom_margin = Cm(2)
    seccion.left_margin = Cm(2.5)
    seccion.right_margin = Cm(2)
    seccion.header_distance = Cm(1.25)
    seccion.footer_distance = Cm(1)
    _estilos(doc)
    return doc


# ---------------------------------------------------------------- piezas del documento

def encabezado_y_pie(seccion, titulo, version=VERSION):
    seccion.different_first_page_header_footer = True

    encabezado = seccion.header.paragraphs[0]
    encabezado.style = 'Header'
    encabezado.alignment = WD_ALIGN_PARAGRAPH.LEFT
    tab_derecha(encabezado, ANCHO_UTIL_CM)
    encabezado.add_run(f'SYSCLIN — {titulo}')
    encabezado.add_run(f'\tVersión {version}')
    borde_parrafo(encabezado, 4, lados=('bottom',), espacio=1)

    # Pie: solo el número de página, en el margen derecho
    pie = seccion.footer.paragraphs[0]
    pie.style = 'Footer'
    pie.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    campo(pie, 'PAGE', '1')


def portada(doc, logo, titulo, subtitulo, lineas_finales):
    for _ in range(4):
        doc.add_paragraph('', style='Portada')
    if logo and os.path.isfile(logo):
        doc.add_paragraph('', style='Portada').add_run().add_picture(logo, width=Cm(3))
    doc.add_paragraph('', style='Portada')
    p = doc.add_paragraph('SYSCLIN', style='Portada')
    p.runs[0].bold = True
    for _ in range(3):
        doc.add_paragraph('', style='Portada')
    doc.add_paragraph(titulo.upper(), style='Portada título')
    doc.add_paragraph(subtitulo, style='Portada')
    for _ in range(8):
        doc.add_paragraph('', style='Portada')
    for linea in lineas_finales:
        doc.add_paragraph(linea, style='Portada')
    doc.add_paragraph('', style='Portada').add_run().add_break(WD_BREAK.PAGE)


def tabla(doc, encabezados, filas, anchos_cm):
    """Tabla con fila de títulos gris que se repite en cada hoja. Una celda (texto,) va en negrita."""
    t = doc.add_table(rows=1, cols=len(encabezados))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = False
    for i, texto in enumerate(encabezados):
        celda = t.rows[0].cells[i]
        celda.width = Cm(anchos_cm[i])
        p = celda.paragraphs[0]
        p.style = 'Texto de tabla'
        p.add_run(texto).bold = True
        sombreado(celda._tc.get_or_add_tcPr(), GRIS_TABLA, DESPUES_SHD_CELDA)
    t.rows[0]._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
    for fila in filas:
        celdas = t.add_row().cells
        for i, texto in enumerate(fila):
            celdas[i].width = Cm(anchos_cm[i])
            p = celdas[i].paragraphs[0]
            p.style = 'Texto de tabla'
            if isinstance(texto, tuple):
                p.add_run(texto[0]).bold = True
            else:
                p.add_run(texto)
    doc.add_paragraph('')
    return t


def control(doc, datos, fecha, version=VERSION):
    """Control del documento (datos, firmas) e historial de revisiones, en hoja propia."""
    doc.add_paragraph('CONTROL DEL DOCUMENTO', style='Título sin número')
    tabla(doc, ['Campo', 'Valor'], [[(nombre,), valor] for nombre, valor in datos], [5, 11.5])
    tabla(doc, ['', 'Nombre', 'Firma', 'Fecha'], [
        [('Elaborado por',), '', '', ''],
        [('Revisado por',), '', '', ''],
        [('Aprobado por',), '', '', ''],
    ], [4, 6, 3.5, 3])
    doc.add_paragraph('HISTORIAL DE REVISIONES', style='Título sin número')
    tabla(doc, ['Versión', 'Fecha', 'Descripción del cambio'], [[version, fecha, 'Emisión inicial']], [2.5, 3, 11])
    doc.add_paragraph('').add_run().add_break(WD_BREAK.PAGE)


def indice(doc, con_figuras=False, niveles='1-2'):
    doc.add_paragraph('ÍNDICE', style='Título sin número')
    campo(doc.add_paragraph('', style='Fin de índice'), f'TOC \\o "{niveles}" \\h \\z \\u',
          'Haga clic derecho y elija «Actualizar campos» para generar el índice.')
    if con_figuras:
        doc.add_paragraph('ÍNDICE DE FIGURAS', style='Título sin número')
        campo(doc.add_paragraph('', style='Fin de índice'), 'TOC \\h \\z \\c "Figura"',
              'Haga clic derecho y elija «Actualizar campos» para generar el índice de figuras.')


def cerrar_indices(doc):
    """Al actualizar un índice, Word deja vacío el párrafo que lo aloja; si el índice llena la hoja, ese párrafo
    cae solo en una hoja en blanco antes del capítulo 1. Si al índice le sigue un capítulo, el cierre del campo
    pasa al inicio del título del capítulo y no queda ningún párrafo entre los dos. Se llama al terminar."""
    marca = doc.styles['Fin de índice']
    for p in doc.paragraphs:
        if p.style.name != 'Fin de índice':
            continue
        p.style = doc.styles['Normal']
        siguiente = p._p.getnext()
        ppr_sig = siguiente.find(qn('w:pPr')) if siguiente is not None and siguiente.tag == qn('w:p') else None
        estilo_sig = ppr_sig.find(qn('w:pStyle')) if ppr_sig is not None else None
        if estilo_sig is None or estilo_sig.get(qn('w:val')) != 'Heading1':
            continue
        ppr_sig.addnext(p._p.findall(qn('w:r'))[-1])
    # El estilo era solo una marca interna: no queda en la lista de estilos del documento
    doc.styles.element.remove(marca.element)


def nota(doc, estilo, texto):
    p = doc.add_paragraph('', style=estilo)
    p.add_run(f'{estilo}: ').bold = True
    p.add_run(texto)


def guardar(doc, titulo):
    """Bytes del .docx final."""
    cerrar_indices(doc)
    # La plantilla base de python-docx trae <w:zoom> sin el porcentaje que exige el esquema
    zoom = doc.settings.element.find(qn('w:zoom'))
    if zoom is not None and zoom.get(qn('w:percent')) is None:
        zoom.set(qn('w:percent'), '100')
    doc.core_properties.title = titulo
    doc.core_properties.author = 'SYSCLIN'
    buffer = BytesIO()
    doc.save(buffer)
    return buffer.getvalue()


# ---------------------------------------------------------------- HTML de la ayuda -> Word

class _Nodo:
    def __init__(self, etiqueta, atributos=None, padre=None):
        self.etiqueta = etiqueta
        self.atributos = dict(atributos or [])
        self.padre = padre
        self.hijos = []

    @property
    def clases(self):
        return (self.atributos.get('class') or '').split()


class _LectorHtml(HTMLParser):
    VACIAS = {'br', 'img', 'hr'}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.raiz = _Nodo('raiz')
        self.actual = self.raiz

    def handle_starttag(self, etiqueta, atributos):
        nodo = _Nodo(etiqueta, atributos, self.actual)
        self.actual.hijos.append(nodo)
        if etiqueta not in self.VACIAS:
            self.actual = nodo

    def handle_endtag(self, etiqueta):
        nodo = self.actual
        while nodo is not None and nodo.etiqueta != etiqueta:
            nodo = nodo.padre
        if nodo is not None and nodo.padre is not None:
            self.actual = nodo.padre

    def handle_data(self, texto):
        self.actual.hijos.append(texto)


def _texto_plano(nodo):
    if isinstance(nodo, str):
        return nodo
    return ''.join(_texto_plano(h) for h in nodo.hijos)


def _colapsar(texto):
    """Junta espacios y saltos de línea como lo hace el navegador, conservando un espacio en los bordes."""
    if not texto:
        return ''
    if not texto.strip():
        return ' '
    centro = ' '.join(texto.split())
    return (' ' if texto[0].isspace() else '') + centro + (' ' if texto[-1].isspace() else '')


def _runs(parrafo, nodo, negrita=False, cursiva=False, es_codigo=False):
    """Vuelca el contenido en línea (strong, em, code, a, span, br) como runs del párrafo."""
    for hijo in nodo.hijos:
        if isinstance(hijo, str):
            texto = _colapsar(hijo)
            if not parrafo.text:
                texto = texto.lstrip()
            if not texto:
                continue
            run = parrafo.add_run(texto)
            run.bold = negrita or None
            run.italic = cursiva or None
            if es_codigo:
                run.font.name = LETRA_CODIGO
                run.font.size = Pt(11)
                letra(run, LETRA_CODIGO)
        elif hijo.etiqueta == 'br':
            parrafo.add_run().add_break()
        elif hijo.etiqueta in ('strong', 'b') or 'btn-ref' in hijo.clases:
            _runs(parrafo, hijo, True, cursiva, es_codigo)
        elif hijo.etiqueta in ('em', 'i'):
            _runs(parrafo, hijo, negrita, True, es_codigo)
        elif hijo.etiqueta == 'code':
            _runs(parrafo, hijo, negrita, cursiva, True)
        else:  # a, span y cualquier otra etiqueta en línea
            _runs(parrafo, hijo, negrita, cursiva, es_codigo)


def _nueva_numeracion(doc):
    """Cada lista numerada del HTML empieza en 1 (python-docx, por defecto, sigue la numeración anterior)."""
    numbering = doc.part.numbering_part.element
    num_id_estilo = doc.styles['List Number'].element.pPr.numPr.numId.val
    abstract_id = None
    for num in numbering.findall(qn('w:num')):
        if num.get(qn('w:numId')) == str(num_id_estilo):
            abstract_id = num.find(qn('w:abstractNumId')).get(qn('w:val'))
    nuevo_id = max(int(n.get(qn('w:numId'))) for n in numbering.findall(qn('w:num'))) + 1
    num = OxmlElement('w:num')
    num.set(qn('w:numId'), str(nuevo_id))
    ref = OxmlElement('w:abstractNumId')
    ref.set(qn('w:val'), abstract_id)
    num.append(ref)
    override = OxmlElement('w:lvlOverride')
    override.set(qn('w:ilvl'), '0')
    inicio = OxmlElement('w:startOverride')
    inicio.set(qn('w:val'), '1')
    override.append(inicio)
    num.append(override)
    numbering.append(num)
    return nuevo_id


def _aplicar_numeracion(parrafo, num_id):
    numpr = OxmlElement('w:numPr')
    ilvl = OxmlElement('w:ilvl')
    ilvl.set(qn('w:val'), '0')
    numid = OxmlElement('w:numId')
    numid.set(qn('w:val'), str(num_id))
    numpr.append(ilvl)
    numpr.append(numid)
    insertar(parrafo._p.get_or_add_pPr(), numpr, DESPUES_NUMPR)


def _descendientes(nodo, etiqueta):
    for h in nodo.hijos:
        if isinstance(h, _Nodo):
            if h.etiqueta == etiqueta:
                yield h
            else:
                yield from _descendientes(h, etiqueta)


def _tabla_html(doc, nodo):
    filas = list(_descendientes(nodo, 'tr'))
    if not filas:
        return
    celdas_por_fila = [[c for c in f.hijos if isinstance(c, _Nodo) and c.etiqueta in ('th', 'td')] for f in filas]
    columnas = max(len(c) for c in celdas_por_fila)
    # Ancho de cada columna según el largo de su texto (mínimo 2,5 cm)
    largos = [0] * columnas
    for celdas in celdas_por_fila:
        for i, c in enumerate(celdas):
            largos[i] = max(largos[i], min(len(_colapsar(_texto_plano(c))), 120))
    total = sum(max(largo, 12) for largo in largos)
    anchos = [max(2.5, ANCHO_UTIL_CM * max(largo, 12) / total) for largo in largos]
    escala = ANCHO_UTIL_CM / sum(anchos)
    anchos = [a * escala for a in anchos]

    t = doc.add_table(rows=0, cols=columnas)
    t.style = 'Table Grid'
    t.autofit = False
    for n_fila, celdas in enumerate(celdas_por_fila):
        fila = t.add_row()
        fila._tr.get_or_add_trPr().append(OxmlElement('w:cantSplit'))  # una fila no se corta entre dos hojas
        if n_fila == 0 and all(c.etiqueta == 'th' for c in celdas):
            fila._tr.get_or_add_trPr().append(OxmlElement('w:tblHeader'))
        for i in range(columnas):
            celda = fila.cells[i]
            celda.width = Cm(anchos[i])
            p = celda.paragraphs[0]
            p.style = 'Texto de tabla'
            # El encabezado va con la primera fila (y el título anterior con ambos): sin tablas «colgadas». Una tabla
            # chica se mantiene entera en una hoja.
            if n_fila == 0 or (len(celdas_por_fila) <= 9 and n_fila < len(celdas_por_fila) - 1):
                p.paragraph_format.keep_with_next = True
            if i < len(celdas):
                origen = celdas[i]
                _runs(p, origen, negrita=origen.etiqueta == 'th')
                if origen.etiqueta == 'th':
                    sombreado(celda._tc.get_or_add_tcPr(), GRIS_TABLA, DESPUES_SHD_CELDA)


def _codigo(doc, texto):
    for linea in texto.strip('\n').split('\n'):
        doc.add_paragraph(linea.rstrip() or ' ', style='Código')


def _lista(doc, nodo):
    numerada = nodo.etiqueta == 'ol'
    num_id = _nueva_numeracion(doc) if numerada else None
    for li in nodo.hijos:
        if not isinstance(li, _Nodo) or li.etiqueta != 'li':
            continue
        p = doc.add_paragraph('', style='List Number' if numerada else 'List Bullet')
        if num_id:
            _aplicar_numeracion(p, num_id)
        en_linea = _Nodo('li')
        for h in li.hijos:
            if isinstance(h, _Nodo) and h.etiqueta in ('ul', 'ol', 'pre', 'table'):
                _bloques(doc, [h])
            else:
                en_linea.hijos.append(h)
        _runs(p, en_linea)


def _recortar_base(img, margen=14):
    """Quita el fondo liso que queda debajo del contenido de una captura (formularios cortos, listados con pocas
    filas): la imagen ocupa menos alto en la hoja. Deja un margen y un alto mínimo de un tercio del original."""
    gris = img.convert('L')
    ancho, alto = gris.size
    minimo = alto // 3
    y = alto - 1
    while y > minimo:
        menor, mayor = gris.crop((0, y, ancho, y + 1)).getextrema()
        if mayor - menor > 40:  # el fondo de las pantallas tiene degradados suaves: no cuentan como contenido
            break
        y -= 1
    return img.crop((0, 0, ancho, min(alto, y + margen)))


def _imagen_liviana(ruta, ancho_max=1300, recortar=False):
    """Las capturas están a doble resolución (2232 px): a 12-15 cm basta con 1500 px (unos 280 ppp a 12 cm) y el Word y el
    PDF pesan mucho menos. Devuelve la ruta tal cual si ya es chica o no se puede reducir.
    recortar=True además quita el fondo liso de abajo (manual de usuario)."""
    try:
        from PIL import Image
        with Image.open(ruta) as img:
            if img.width <= ancho_max and not recortar:
                return ruta
            img = img.convert('RGB')
            if img.width > ancho_max:
                img = img.resize((ancho_max, round(img.height * ancho_max / img.width)), Image.LANCZOS)
            if recortar:
                img = _recortar_base(img)
            salida = BytesIO()
            img.save(salida, 'JPEG', quality=80, optimize=True)
            salida.seek(0)
            return salida
    except Exception:
        return ruta


def _ruta_figura(nodo):
    """Ruta en disco de la imagen de un <figure>, o '' si no existe."""
    img = next(_descendientes(nodo, 'img'), None)
    ruta = (img.atributos.get('src') or '').removeprefix('file://') if img else ''
    return ruta if os.path.isfile(ruta) else ''


def _pie_figura(doc, pie, nodo):
    """Escribe en el párrafo `pie` la leyenda «Figura N.M. texto» (N = capítulo, M = figura del capítulo). Se calculan al
    generar y M va en un campo SEQ con reinicio explícito (\\r): así el índice de figuras y LibreOffice dan lo mismo
    que Word."""
    capitulo = sum(1 for p in doc.paragraphs if p.style.name == 'Heading 1')
    anterior_cap, anterior_n = getattr(doc, '_ultima_figura', (None, 0))
    numero = anterior_n + 1 if anterior_cap == capitulo else 1
    doc._ultima_figura = (capitulo, numero)
    pie.add_run(f'Figura {capitulo}.').bold = True
    campo(pie, f'SEQ Figura \\r {numero} \\* ARABIC', str(numero))
    pie.add_run('. ').bold = True
    leyenda = next(_descendientes(nodo, 'figcaption'), None)
    pie.add_run(_colapsar(_texto_plano(leyenda)).strip() if leyenda else '')


def _figura_html(doc, nodo, ancho_cm=None):
    """<figure class="captura"><img><figcaption>: captura centrada con pie «Figura N.M.» (N = capítulo, M = figura
    del capítulo), como en docs/scripts/generar_plantilla_manual.py. Sin imagen en disco no pone nada."""
    ruta = _ruta_figura(nodo)
    if not ruta:
        return
    imagen = _imagen_liviana(ruta, recortar=getattr(doc, 'recortar_figuras', False))
    ancho = ancho_cm or getattr(doc, 'ancho_figura_cm', 15)
    alto_max = getattr(doc, 'alto_apilada_cm', None) if ancho_cm else None
    if alto_max:  # captura alta (un formulario largo): se achica para que la pantalla entre en una hoja
        try:
            from PIL import Image
            if hasattr(imagen, 'seek'):
                imagen.seek(0)
            with Image.open(imagen) as im:
                ancho = min(ancho, alto_max * im.width / im.height)
            if hasattr(imagen, 'seek'):
                imagen.seek(0)
        except Exception:
            pass
    doc.add_paragraph('', style='Figura').add_run().add_picture(imagen, width=Cm(ancho))
    _pie_figura(doc, doc.add_paragraph('', style='Caption'), nodo)


def _pantallas_juntas(parrafos):
    """Cada pantalla del manual (un título de nivel 2 y lo que sigue hasta el próximo) se mantiene en una sola hoja si
    cabe: todos sus párrafos menos el último van «con el siguiente». Si no cabe, sigue de largo, como siempre. Así
    una pantalla corta comparte hoja con la anterior, una larga empieza en hoja nueva y no quedan títulos solos al pie
    ni notas sueltas en la hoja siguiente."""
    bloque = []
    for p in list(parrafos) + [None]:
        if p is None or p.style.name == 'Heading 2':
            for q in bloque[:-1]:
                q.paragraph_format.keep_with_next = True
            bloque = []
        if p is not None:
            bloque.append(p)


def _par_figuras_html(doc, nodo, lado_a_lado=False):
    """<div class="par"> con varias <figure>: las capturas van lado a lado en una tabla sin bordes, cada una con su
    pie, si el documento lo pide (ancho_par_cm); si no, una debajo de otra y más grandes. <div class="par-mini"> (avisos
    de error, capturas chicas) siempre va lado a lado. Con menos de dos imágenes se ponen como figuras comunes."""
    figuras = [f for f in _descendientes(nodo, 'figure') if _ruta_figura(f)]
    ancho = getattr(doc, 'ancho_par_cm', None) or (8.0 if lado_a_lado else 0)
    if not figuras or not ancho or (len(figuras) < 2 and not lado_a_lado):
        # Una debajo de otra; si son dos de una misma pantalla, algo más chicas para que la pantalla entre en una hoja
        for f in figuras:
            _figura_html(doc, f, getattr(doc, 'ancho_apilada_cm', None) if len(figuras) > 1 else None)
        return
    t = doc.add_table(rows=1, cols=len(figuras))
    t.autofit = False
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for celda, f in zip(t.rows[0].cells, figuras):
        celda.width = Cm(ancho + 0.3)
        celda.paragraphs[0].style = 'Figura'
        celda.paragraphs[0].add_run().add_picture(_imagen_liviana(_ruta_figura(f)), width=Cm(ancho))
        _pie_figura(doc, celda.add_paragraph('', style='Caption'), f)


def _es_nota(nodo):
    return isinstance(nodo, _Nodo) and nodo.etiqueta == 'p' and ('importante' in nodo.clases or 'peligro' in nodo.clases)


def _bloques(doc, hijos):
    hijos = [h for h in hijos if not (isinstance(h, str) and not h.strip())]
    for n, nodo in enumerate(hijos):
        if isinstance(nodo, str):
            envoltorio = _Nodo('p')
            envoltorio.hijos.append(nodo)
            _runs(doc.add_paragraph(''), envoltorio)
            continue
        e = nodo.etiqueta
        if e == 'h3':  # la guía de uso trae el título del capítulo dentro de cada sección
            doc.add_heading(_colapsar(_texto_plano(nodo)).strip(), level=1)
        elif e == 'figure':
            _figura_html(doc, nodo)
        elif 'par' in nodo.clases:  # capturas lado a lado (o apiladas, según el documento)
            _par_figuras_html(doc, nodo)
        elif 'par-mini' in nodo.clases:  # capturas chicas: siempre lado a lado
            _par_figuras_html(doc, nodo, lado_a_lado=True)
        elif 'aqui' in nodo.clases:  # rótulo «Pantalla actual» de la vista previa: no va en el documento
            continue
        elif e == 'h4':
            doc.add_paragraph(_colapsar(_texto_plano(nodo)).strip(), style='Heading 2')
        elif e == 'h5':
            doc.add_paragraph(_colapsar(_texto_plano(nodo)).strip(), style='Heading 3')
        elif e == 'p':
            if _es_nota(nodo):
                estilo = 'Nota' if 'importante' in nodo.clases else 'Advertencia'
                p = doc.add_paragraph('', style=estilo)
                p.add_run(f'{estilo}: ').bold = True
            else:
                p = doc.add_paragraph('')
            siguiente_nodo = hijos[n + 1] if n + 1 < len(hijos) else None
            if isinstance(siguiente_nodo, _Nodo) and siguiente_nodo.etiqueta == 'table':
                p.paragraph_format.keep_with_next = True  # el texto que presenta una tabla no queda solo al pie
            _runs(p, nodo)
        elif e in ('ul', 'ol'):
            _lista(doc, nodo)
        elif e in ('table', 'pre'):
            if e == 'table':
                _tabla_html(doc, nodo)
            else:
                _codigo(doc, _texto_plano(nodo))
            # Espacio después de la tabla o el código, salvo que siga una nota (ya trae su propio margen)
            siguiente = hijos[n + 1] if n + 1 < len(hijos) else None
            if not _es_nota(siguiente):
                doc.add_paragraph('')
        else:
            _bloques(doc, nodo.hijos)


def html_a_docx(doc, ruta_html):
    """Vuelca una sección de la ayuda (h4, h5, p, p.importante, p.peligro, ul, ol, table, pre) al documento."""
    with open(ruta_html, encoding='utf-8') as f:
        html_texto_a_docx(doc, f.read())


def html_texto_a_docx(doc, html):
    """Igual que html_a_docx, con el HTML ya en memoria (secciones renderizadas con Jinja)."""
    lector = _LectorHtml()
    lector.feed(html)
    _bloques(doc, lector.raiz.hijos)


def anexo_scripts(doc, raiz, scripts, fecha):
    """Anexo A: contenido vigente de cada script, leído del repositorio al generar."""
    doc.add_paragraph('Anexo A. Scripts y archivos de configuración', style='Título de anexo')
    doc.add_paragraph(f'Contenido vigente de cada archivo al {fecha}, tomado directamente del sistema. Las rutas '
                      'son relativas a la carpeta raíz del proyecto (syscomcli). Las contraseñas no aparecen: '
                      'viven en el .env, que no forma parte de este anexo.')
    tabla(doc, ['Archivo', 'Para qué sirve'], [[ruta, desc] for ruta, desc in scripts], [7.5, 9])
    for n, (ruta, descripcion) in enumerate(scripts, start=1):
        doc.add_paragraph(f'A.{n} {ruta}', style='Título de anexo 2')
        doc.add_paragraph(f'{descripcion}.')
        try:
            with open(os.path.join(raiz, ruta), encoding='utf-8') as f:
                contenido = f.read()
        except OSError:
            doc.add_paragraph('El archivo no se encontró al generar el manual.')
            continue
        _codigo(doc, contenido.rstrip('\n'))


# ---------------------------------------------------------------- manuales

def manual_tecnico(raiz, partes, anexos, scripts, logo, fecha, datos):
    """Manual técnico (seguridad o infraestructura, .docx en bytes) con el contenido de las secciones de la ayuda.
    partes = [{'titulo' (o None, sin carátula), 'introduccion', 'capitulos': [{'titulo', 'html'}]}];
    anexos = [{'letra', 'titulo', 'html'}] (sin subtítulos h4: el anexo no lleva numeración);
    datos = titulo, subtitulo, destinatario, revision, confidencialidad y referencias (ayuda_routes.MANUALES_TECNICOS).
    El anexo de scripts solo sale si se pasan scripts."""
    titulo = datos['titulo']
    doc = nuevo_documento()
    compacto = datos.get('compacto', False)
    denso = datos.get('denso', False)
    if compacto:  # igual que el Manual del sistema: para no pasar de 100 hojas
        doc.styles['Normal'].paragraph_format.line_spacing = 1.15
        doc.styles['Normal'].paragraph_format.space_after = Pt(4)
        doc.ancho_figura_cm = 12
    if denso:  # manual de usuario: dos pantallas por hoja, capturas lado a lado
        _estilos_densos(doc)
        doc.ancho_figura_cm = datos.get('ancho_figura_cm', 11.5)
        doc.ancho_par_cm = datos.get('ancho_par_cm')  # None: las capturas van una debajo de otra, más grandes
        doc.recortar_figuras = True
        doc.ancho_apilada_cm = datos.get('ancho_apilada_cm', 10.0)  # dos capturas de una pantalla, una debajo de otra
        doc.alto_apilada_cm = datos.get('alto_apilada_cm', 8.6)     # y sin pasar de este alto
    encabezado_y_pie(doc.sections[0], titulo)
    portada(doc, logo, titulo, datos['subtitulo'],
            ('Sistema SYSCLIN de gestión clínica', f'Versión {VERSION}', fecha, 'Documento confidencial'))
    control(doc, [
        ('Documento', titulo),
        ('Sistema', 'Sysclin, gestión clínica (agendamiento, consultorio, ventas)'),
        ('Destinatario', datos['destinatario']),
        ('Versión', VERSION),
        ('Fecha de generación', fecha),
        ('Revisión', datos['revision']),
        ('Confidencialidad', datos['confidencialidad']),
        ('Referencias', datos['referencias']),
    ], fecha)
    indice(doc, con_figuras=not denso and any('<figure' in c['html'] for p in partes for c in p['capitulos']),
           niveles='1-1' if denso else '1-2')  # denso: el índice lista solo los capítulos
    for parte in partes:
        if parte['titulo']:
            caratula_parte(doc, parte['titulo'], parte['introduccion'], [c['titulo'] for c in parte['capitulos']])
        antes = len(doc.paragraphs)
        for capitulo in parte['capitulos']:
            doc.add_heading(capitulo['titulo'], level=1)
            antes_capitulo = len(doc.paragraphs)
            html_texto_a_docx(doc, capitulo['html'])
            if denso and capitulo['id'].startswith('modulo-'):
                _pantallas_juntas(doc.paragraphs[antes_capitulo:])
        if (compacto and not denso) or datos.get('capitulos_seguidos'):
            # Capítulos seguidos: solo el primero del documento empieza hoja nueva (los demás siguen al anterior)
            titulos = [p for p in doc.paragraphs[antes:] if p.style.name == 'Heading 1']
            for i, t in enumerate(titulos):
                t.paragraph_format.page_break_before = (i == 0 and parte is partes[0])
    for n_anexo, anexo in enumerate(anexos):
        titulo_anexo = doc.add_paragraph(f"Anexo {anexo['letra']}. {anexo['titulo']}", style='Título de anexo')
        if datos.get('capitulos_seguidos'):  # solo el primer anexo empieza hoja nueva
            titulo_anexo.paragraph_format.page_break_before = (n_anexo == 0)
        html_texto_a_docx(doc, anexo['html'])
    if scripts:
        anexo_scripts(doc, raiz, scripts, fecha)
    return guardar(doc, titulo)


def manual_sistema(partes, raiz, scripts, logo, fecha):
    """Manual del sistema (.docx en bytes): guías de uso y seguridad en un solo documento, dividido en partes.
    partes = [{'titulo', 'introduccion', 'capitulos': [(titulo o None, html)]}]; si el capítulo trae título se
    lo pone aquí (seguridad), si no, el html ya trae su h3 (guía de uso). Los capítulos se numeran seguidos."""
    titulo = 'Manual del sistema'
    doc = nuevo_documento()
    # Documento largo (unas 100 hojas): interlineado 1,15 en vez de 1,5 del estándar de los manuales individuales
    doc.styles['Normal'].paragraph_format.line_spacing = 1.15
    doc.styles['Normal'].paragraph_format.space_after = Pt(4)
    doc.ancho_figura_cm = 12  # capturas más angostas que en las guías individuales (15 cm)
    encabezado_y_pie(doc.sections[0], titulo)
    portada(doc, logo, titulo, 'Guía de uso, administración, seguridad y operación',
            ('Sistema SYSCLIN de gestión clínica', f'Versión {VERSION}', fecha, 'Documento confidencial'))
    control(doc, [
        ('Documento', titulo),
        ('Sistema', 'Sysclin, gestión clínica (agendamiento, consultorio, ventas)'),
        ('Destinatario', 'Administrador y Superadministrador del sistema'),
        ('Contenido', '; '.join(p['titulo'] for p in partes)),
        ('Versión', VERSION),
        ('Fecha de generación', fecha),
        ('Confidencialidad', 'Incluye la parte de seguridad y operación, que describe la infraestructura: no se '
                             'entrega a usuarios finales. Para ellos están las guías de uso por rol'),
        ('Referencia', 'IEEE Std 1063-2001, Software User Documentation; ISO/IEC 26514:2008'),
    ], fecha)
    indice(doc, con_figuras=True, niveles='1-1')  # solo partes y capítulos: con subtítulos ocupa 9 hojas
    primeros = []  # primer capítulo de cada parte: es el único que empieza en hoja nueva, tras la carátula
    for parte in partes:
        nombres = [t or re.search(r'<h3[^>]*>(.*?)</h3>', h, re.S).group(1).strip()
                   for t, h in parte['capitulos']]
        caratula_parte(doc, parte['titulo'], parte['introduccion'], nombres)
        antes = len(doc.paragraphs)
        for titulo_capitulo, html in parte['capitulos']:
            if titulo_capitulo:
                doc.add_heading(titulo_capitulo, level=1)
            html_texto_a_docx(doc, html)
        primeros.append(next(p._p for p in doc.paragraphs[antes:] if p.style.name == 'Heading 1'))
    # Con 37 capítulos, uno por hoja deja la mitad en blanco: siguen uno tras otro dentro de cada parte
    for p in doc.paragraphs:
        if p.style.name == 'Heading 1':
            p.paragraph_format.page_break_before = p._p in primeros
    anexo_scripts(doc, raiz, scripts, fecha)
    return guardar(doc, titulo)


def caratula_parte(doc, titulo, introduccion, capitulos):
    """Carátula de una parte: hoja propia con el título grande, una línea de introducción y los capítulos que
    contiene. El título usa el estilo de anexo (sin número, entra en el índice)."""
    p = doc.add_paragraph('', style='Título de anexo')
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(150)
    p.paragraph_format.space_after = Pt(18)
    r = p.add_run(titulo)
    r.font.size = Pt(26)
    if introduccion:
        intro = doc.add_paragraph(introduccion)
        intro.alignment = WD_ALIGN_PARAGRAPH.CENTER
        intro.paragraph_format.space_after = Pt(24)
    doc.add_paragraph('Contenido de esta parte', style='Título sin número').alignment = WD_ALIGN_PARAGRAPH.CENTER
    for nombre in capitulos:
        item = doc.add_paragraph(nombre)
        item.alignment = WD_ALIGN_PARAGRAPH.CENTER
        item.paragraph_format.space_after = Pt(2)
        item.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE


def docx_a_pdf(docx_bytes, timeout=110):
    """Exporta el .docx a PDF con LibreOffice (actualiza antes índice y números de página)."""
    if not shutil.which('soffice') or not os.path.isfile(PYTHON_UNO):
        raise RuntimeError('LibreOffice no está instalado en el contenedor (ver dock/Dockerfile).')
    with tempfile.TemporaryDirectory(prefix='sysclin_manual_') as carpeta:
        entrada = os.path.join(carpeta, 'manual.docx')
        salida = os.path.join(carpeta, 'manual.pdf')
        with open(entrada, 'wb') as f:
            f.write(docx_bytes)
        # Perfil de LibreOffice propio de esta conversión: permite descargas simultáneas
        perfil = os.path.join(carpeta, 'perfil')
        resultado = subprocess.run([PYTHON_UNO, SCRIPT_UNO, entrada, salida, perfil],
                                   capture_output=True, text=True, timeout=timeout)
        if resultado.returncode != 0 or not os.path.isfile(salida):
            raise RuntimeError(f'No se pudo convertir el manual a PDF: {resultado.stderr.strip()[-500:]}')
        with open(salida, 'rb') as f:
            return f.read()
