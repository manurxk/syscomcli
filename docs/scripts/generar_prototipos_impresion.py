"""
Genera los prototipos de impresión de la consulta (orden de estudios/análisis, receta y
certificado) en docs/prototipos/, en HTML y PDF, para revisarlos antes de pasar a las
plantillas reales.

Usa la misma hoja de estilos que la ficha clínica (la lee de FICHA.html), el paciente,
el especialista y la empresa reales de la base; los ítems son de los catálogos de
psicología (migración 111).

También genera los de Ventas: nota de crédito y nota de débito (KuDE, con la plantilla
FE.html real vía FacturaPDFService), nota de remisión, presupuesto y presupuesto de plan
de tratamiento (PEI). La NC sale de la base; la ND, la remisión y los presupuestos usan
datos de ejemplo sobre una factura real (no hay PEI cargados todavía).

Uso (dentro del contenedor de la app):
    docker exec -w /app syscomcli_app python docs/scripts/generar_prototipos_impresion.py [id_orden] [id_nota_credito]
"""
import os
import re
import sys
from datetime import date, timedelta

sys.path.insert(0, '/app')

from weasyprint import HTML

from app import app
from app.services.ficha_html_pdf_service import FichaHtmlPdfService
from app.services import factura_pdf_service
from app.services.factura_pdf_service import FacturaPDFService
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao, numero_a_letras
from app.dao.ventas.movimientos.nota_credito.NotaCreditoDao import NotaCreditoDao

SALIDA = '/app/docs/prototipos'
PLANTILLA_FICHA = '/app/app/rutas/clinico/movimientos/ficha/templates/FICHA.html'
MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'septiembre', 'octubre', 'noviembre', 'diciembre']

svc = FichaHtmlPdfService()
fv = svc._fv


def fecha_larga(d):
    return f"{d.day} de {MESES[d.month - 1]} de {d.year}"


def fecha_corta(d):
    return d.strftime('%d/%m/%Y')


def gs(valor):
    """Monto en guaraníes con separador de miles (150.000)."""
    return f"{int(valor):,}".replace(',', '.')


def hoja_de_estilos():
    """CSS de FICHA.html con el pie de página parametrizado (@@PIE@@) + estilos propios."""
    plantilla = open(PLANTILLA_FICHA, encoding='utf-8').read()
    css = re.search(r'<style type="text/css">(.*?)</style>', plantilla, re.S).group(1)
    css = re.sub(r'content: "Ficha médica[^;]*;',
                 'content: "@@PIE@@ · Página " counter(page) " de " counter(pages);', css)
    return css + """
    .doc-num { text-align: center; font-size: 10pt; margin-top: 6px; }
    .cuerpo-cert { font-size: 10pt; line-height: 1.9; text-align: justify; margin: 14px 4px; }
    .rp { font-size: 16pt; font-weight: bold; font-style: italic; margin: 6px 0 2px 2px; }
    .indic { font-size: 7.5pt; color: #333333; font-style: italic; }
    .lugar-fecha { text-align: right; margin-top: 10px; font-size: 9pt; }
    .num { text-align: right; }
    .firmas { margin-top: 40px; }
    .firmas td { width: 50%; padding: 0 25px; text-align: center; vertical-align: top; font-size: 8pt; }
    .firmas .linea { border-top: 1px solid #000000; padding-top: 3px; }
    .totales td { border: 1px solid #040303; padding: 3px 5px; }
    """


def main(id_orden, id_nota_credito):
    fd = FichaDao()
    cons = fd.execute_query_one(
        """SELECT c.id_consulta, c.id_paciente, c.id_especialista, c.consulta_fecha
           FROM ordenes o JOIN consultas c USING (id_consulta) WHERE o.id_orden = %s""", (id_orden,))
    if not cons:
        raise SystemExit(f'No existe la orden {id_orden}')
    pac = fd.getFichaCompleta(cons['id_paciente'])['paciente']
    gen = fd.getDatosGenerador(cons['id_especialista']) or {}
    dx = fd.execute_query(
        """SELECT d.cod_cie10, d.des_diagnostico FROM registro_diagnosticos r
           JOIN diagnosticos d USING (id_diagnostico) WHERE r.id_consulta = %s""", (cons['id_consulta'],))
    if not dx:
        dx = [{'cod_cie10': 'F90.0', 'des_diagnostico': 'TRASTORNO DE ACTIVIDAD Y ATENCION'}]
    emp = EmpresaDao().getEmpresaPrincipal() or {}
    ruc = f"{emp.get('ruc_nit', '')}-{emp.get('digito_verificador', '')}" if emp.get('ruc_nit') else ''
    fecha = cons['consulta_fecha'].date()

    css = hoja_de_estilos()
    logo = svc._resolver_logo_base64('/app')
    logo_html = f'<img src="data:image/png;base64,{logo}" alt="Logo">' if logo else ''

    def encabezado(titulo, numero, subtitulo, fecha_doc=None):
        return f"""
  <table class="encabezado" style="border: 1px solid #040303;">
    <tr style="background-color: #dcdcdc;">
      <td colspan="2" style="text-align: center; font-size: 7pt; padding: 3px; border-bottom: 1px solid #040303;">{subtitulo}</td>
    </tr>
    <tr>
      <td style="width: 60%; padding: 10px 12px; line-height: 1.5;">
        {logo_html}
        <div style="font-size: 10pt; font-weight: bold;">{fv(emp.get('nombre_comercial') or emp.get('razon_social'), 'SYSCLIN')}</div>
        <div>{fv(emp.get('direccion'), '')}</div>
        <div>Teléfono: {fv(emp.get('telefono') or emp.get('celular'), '')}</div>
        <div>RUC: {fv(ruc, '')}</div>
      </td>
      <td style="width: 40%; padding: 10px 12px; border-left: 1px solid #040303; line-height: 1.6;">
        <div class="titulo-doc">{titulo}</div>
        <div class="doc-num">Nº <b>{numero}</b></div>
        <div style="text-align: center; margin-top: 10px;">Fecha: {fecha_corta(fecha_doc or fecha)}</div>
      </td>
    </tr>
  </table>"""

    def bloque_paciente(pac=pac):
        tutor = ''
        if pac.get('es_menor'):
            responsable = pac.get('madre_nombre') or pac.get('padre_nombre')
            tutor = (f'<tr><td colspan="4"><span class="lbl">Responsable (paciente menor de edad)</span>'
                     f'{fv(responsable)}</td></tr>')
        nacimiento = (pac.get('fecha_nacimiento') or '') + (
            f" · {pac['edad']} años" if pac.get('edad') is not None else '')
        return f"""
  <div class="seccion">Paciente</div>
  <table class="tabla-datos">
    <tr>
      <td style="width: 50%;"><span class="lbl">Nombre completo</span><b>{fv(pac.get('nombre_completo'))}</b></td>
      <td style="width: 17%;"><span class="lbl">Cédula</span>{fv(pac.get('cedula'))}</td>
      <td style="width: 20%;"><span class="lbl">Fecha de nacimiento · edad</span>{fv(nacimiento)}</td>
      <td style="width: 13%;"><span class="lbl">Historia clínica</span>{fv(pac.get('historia_clinica'))}</td>
    </tr>
    {tutor}
  </table>"""

    def firma():
        return f"""
  <div class="firma no-cortar"><div class="linea">
    <b>{fv(gen.get('nombre_completo'))}</b><br>
    Matrícula Nº {fv(gen.get('matricula'))}<br>
    {fv(gen.get('especialidades'))}
  </div></div>"""

    def confidencial(texto):
        return f'<div class="confidencial">{texto}</div>'

    def documento(pie, cuerpo):
        return (f'<!DOCTYPE html>\n<html><head><meta charset="UTF-8" /><title>{pie}</title>\n'
                f'<style type="text/css">{css.replace("@@PIE@@", pie)}</style></head>\n<body>{cuerpo}</body></html>')

    # ---------------- Orden de estudios y análisis ----------------
    dx_html = ''.join(f"<div>{fv(d['cod_cie10'])} — {fv(d['des_diagnostico'])}</div>" for d in dx)
    items = [('ESTUDIO', 'EVALUACIÓN NEUROPSICOLÓGICA'), ('ESTUDIO', 'ELECTROENCEFALOGRAMA'),
             ('ANÁLISIS', 'PERFIL TIROIDEO TSH Y T4 LIBRE'), ('ANÁLISIS', 'HEMOGRAMA COMPLETO')]
    filas = ''.join(
        f'<tr><td style="text-align: center; width: 6%;">{i}</td><td style="width: 18%;">{tipo}</td><td>{des}</td></tr>'
        for i, (tipo, des) in enumerate(items, 1))
    orden = documento(
        'Orden de estudios y análisis ORD-2026-0005',
        encabezado('ORDEN DE ESTUDIOS<br>Y ANÁLISIS', 'ORD-2026-0005', 'Orden médica · Documento confidencial')
        + bloque_paciente() + f"""
  <div class="seccion">Diagnóstico presuntivo (CIE-10)</div>
  <table class="tabla-datos"><tr><td>{dx_html}</td></tr></table>
  <div class="seccion">Estudios y análisis solicitados</div>
  <table class="detalle"><tr><th>Nº</th><th>Tipo</th><th>Descripción</th></tr>{filas}</table>
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Indicaciones</span>Electroencefalograma con privación parcial de sueño. Análisis en ayunas de 8 horas.</td></tr>
    <tr><td><span class="lbl">Observaciones</span>Control antes de iniciar tratamiento farmacológico. Traer los resultados a la próxima consulta.</td></tr>
  </table>""" + firma() + confidencial(
            'Documento con datos de salud del paciente: uso exclusivo para la realización de los estudios '
            'indicados. Prohibida su reproducción o divulgación sin autorización.'))

    # ---------------- Receta ----------------
    medicamentos = [
        ('METILFENIDATO 10 MG', '1 comprimido', 'Cada 24 horas, por la mañana', '30 días', '30',
         'Tomar con el desayuno. No administrar después de las 14:00.'),
        ('MELATONINA 3 MG', '1 comprimido', 'Cada 24 horas, 30 min antes de dormir', '30 días', '30', ''),
    ]
    filas_rx = ''
    for med, dosis, frecuencia, duracion, cantidad, indicacion in medicamentos:
        filas_rx += (f'<tr><td><b>{med}</b></td><td>{dosis}</td><td>{frecuencia}</td>'
                     f'<td style="text-align: center;">{duracion}</td><td style="text-align: center;">{cantidad}</td></tr>')
        if indicacion:
            filas_rx += f'<tr><td colspan="5" class="indic">Indicación: {indicacion}</td></tr>'
    validez = 30
    receta = documento(
        'Receta REC-2026-0005',
        encabezado('RECETA', 'REC-2026-0005', 'Receta médica · Documento confidencial') + bloque_paciente() + f"""
  <div class="rp">Rp/</div>
  <table class="detalle"><tr><th>Medicamento</th><th>Dosis</th><th>Frecuencia</th><th>Duración</th><th>Cantidad</th></tr>{filas_rx}</table>
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Indicaciones generales</span>Mantener horarios regulares de sueño. Control en 30 días.</td></tr>
    <tr><td><span class="lbl">Validez</span>{validez} días (hasta el {fecha_corta(fecha + timedelta(days=validez))})</td></tr>
  </table>""" + firma() + confidencial('Receta personal e intransferible. Documento con datos de salud del paciente.'))

    # ---------------- Certificado ----------------
    texto = (f"Por la presente certifico que <b>{fv(pac.get('nombre_completo'))}</b>, con cédula de identidad "
             f"Nº <b>{fv(pac.get('cedula'))}</b>, asistió a consulta de <b>{fv(gen.get('especialidades'))}</b> "
             f"el día <b>{fecha_larga(fecha)}</b>, en el horario de 08:00 a 08:45.")
    certificado = documento(
        'Certificado CER-2026-0001',
        encabezado('CERTIFICADO<br>DE ASISTENCIA', 'CER-2026-0001', 'Certificado · Documento confidencial') + f"""
  <div class="cuerpo-cert">{texto}</div>
  <table class="tabla-datos">
    <tr><td><span class="lbl">Motivo</span>Evaluación y seguimiento psicológico.</td></tr>
    <tr><td><span class="lbl">Recomendaciones</span>Se sugiere justificar la inasistencia escolar de la fecha indicada.</td></tr>
  </table>
  <div class="cuerpo-cert">Se extiende el presente a solicitud del interesado, para ser presentado ante quien corresponda.</div>
  <div class="lugar-fecha">{fecha_larga(fecha)}</div>""" + firma() + confidencial(
            'El diagnóstico solo se incluye si el especialista lo carga en el certificado (dato sensible de salud).'))

    # ================= VENTAS =================
    nc = NotaCreditoDao().getNotaCreditoById(id_nota_credito)
    if not nc:
        raise SystemExit(f'No existe la nota de crédito {id_nota_credito}')
    fact_dao = FacturaDao()
    fact = fact_dao.getFacturaById(nc['id_factura'])
    det_fact = fact_dao.getFacturaDetalle(nc['id_factura'])
    iva_fact = float(det_fact[0]['impuesto_porcentaje']) if det_fact else 10
    pac_fact = fd.getFichaCompleta(fact['id_paciente'])['paciente']
    hoy = date(2026, 10, 13)

    def kude(titulo, nombre, numero, fecha_iso, motivo, items):
        """KuDE con FE.html real (FacturaPDFService); se captura el HTML en vez de escribir el PDF
        y se cambian los rótulos de 'Factura' por el del documento. Ítems: (descripción, cantidad, total)."""
        capturado = {}

        class _Captura:
            def __init__(self, string, base_url=None):
                capturado['html'] = string

            def write_pdf(self, destino):
                pass

        datos = {
            'factura_numero': numero, 'fecha_factura': fecha_iso,
            'numero_timbrado': fact.get('numero_timbrado'), 'fecha_inicio_vigencia': '',
            'paciente_nombre': fact.get('paciente_nombre'), 'paciente_cedula': fact.get('paciente_cedula'),
            'paciente_direccion': pac_fact.get('direccion', ''), 'paciente_telefono': fact.get('paciente_telefono'),
            'paciente_email': fact.get('paciente_correo') or '', 'condicion_venta': '',
            'moneda': fact.get('cod_moneda', 'PYG'), 'tipo_operacion': motivo,
            'factura_total_letras': numero_a_letras(sum(t for _, _, t in items)),
        }
        detalle = [{'item_codigo': f'{i:03d}', 'item_descripcion': des, 'unidad_medida': 'UNI',
                    'item_cantidad': cant, 'item_total': total, 'item_descuento': 0,
                    'impuesto_porcentaje': iva_fact}
                   for i, (des, cant, total) in enumerate(items, 1)]
        empresa = {'ruc': ruc, 'direccion': emp.get('direccion', ''), 'ciudad': emp.get('des_ciudad') or '',
                   'telefono': emp.get('telefono', '') or emp.get('celular', ''), 'email': emp.get('email', ''),
                   'actividad_economica': emp.get('actividad_economica_principal', '')}
        original = factura_pdf_service.HTML
        factura_pdf_service.HTML = _Captura
        try:
            FacturaPDFService().generar_factura_pdf(datos, detalle, empresa)
        finally:
            factura_pdf_service.HTML = original
        html = capturado['html']
        html = html.replace('KuDE de Factura Electrónica', f'KuDE de {nombre} Electrónica')
        html = html.replace('FACTURA ELECTRÓNICA', f'{titulo} ELECTRÓNICA')
        html = html.replace('esta Factura Electrónica', f'esta {nombre} Electrónica')
        html = re.sub(r'(?<!Tipo de )Documento asociado: ', f"Documento asociado: Factura {fact['factura_numero']}", html)
        html = html.replace('Tipo de Documento asociado: ', 'Tipo de Documento asociado: Electrónico')
        html = html.replace('Tipo de Operación: ', 'Motivo de emisión: ')
        return html

    # ---------------- Nota de crédito (de la base) ----------------
    d, hm = nc['fecha_nota_credito_fmt'].split(' ')
    fecha_nc = f"{d[6:10]}-{d[3:5]}-{d[0:2]}T{hm}:00"
    items_nc = [(x['item_descripcion'].upper(), int(x['item_cantidad']), float(x['monto_total']))
                for x in NotaCreditoDao().getNotaCreditoDetalle(id_nota_credito)]
    nota_credito = kude('NOTA DE CRÉDITO', 'Nota de Crédito', nc['nota_credito_numero'], fecha_nc,
                        nc['motivo_nota_credito'], items_nc)

    # ---------------- Nota de débito (ejemplo sobre la misma factura, venta a crédito) ----------------
    nota_debito = kude('NOTA DE DÉBITO', 'Nota de Débito', 'ND-2026-10-0001', f'{hoy.isoformat()}T10:30:00',
                       'Recargo por mora en el pago de la cuota', [('RECARGO POR MORA - CUOTA 1/1', 1, 15000)])

    # ---------------- Nota de remisión (ejemplo, ligada a la factura real) ----------------
    items_rem = [('INFORME DE EVALUACIÓN PSICOPEDAGÓGICA (IMPRESO, ORIGINAL)', '1', 'Sobre cerrado'),
                 ('CUADERNILLO DE EJERCICIOS DE ATENCIÓN Y MEMORIA', '1', ''),
                 ('PLANILLAS DE REGISTRO DE CONDUCTA PARA EL HOGAR', '1 juego', '10 hojas')]
    filas_rem = ''.join(
        f'<tr><td style="text-align: center; width: 6%;">{i}</td><td>{des}</td>'
        f'<td style="text-align: center; width: 12%;">{cant}</td><td style="width: 22%;">{obs}</td></tr>'
        for i, (des, cant, obs) in enumerate(items_rem, 1))
    remision = documento(
        'Nota de remisión REM-2026-10-0001',
        encabezado('NOTA DE<br>REMISIÓN', 'REM-2026-10-0001', 'Nota de remisión · Documento sin valor fiscal', hoy)
        + bloque_paciente(pac_fact) + f"""
  <div class="seccion">Datos de la entrega</div>
  <table class="tabla-datos">
    <tr>
      <td style="width: 25%;"><span class="lbl">Documento asociado</span>Factura {fact['factura_numero']}</td>
      <td style="width: 25%;"><span class="lbl">Fecha de remisión</span>{fecha_corta(hoy)}</td>
      <td style="width: 25%;"><span class="lbl">Fecha de entrega</span>{fecha_corta(hoy)}</td>
      <td style="width: 25%;"><span class="lbl">Estado</span>ENTREGADA</td>
    </tr>
  </table>
  <div class="seccion">Ítems entregados</div>
  <table class="detalle"><tr><th>Nº</th><th>Descripción</th><th>Cantidad</th><th>Observaciones</th></tr>{filas_rem}</table>
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Observaciones</span>Retira el paciente en recepción. El informe se entrega en sobre cerrado.</td></tr>
  </table>
  <table class="firmas no-cortar"><tr>
    <td><div class="linea"><b>Entregado por</b><br>Firma y aclaración del funcionario</div></td>
    <td><div class="linea"><b>Recibido conforme</b><br>Firma, aclaración y C.I.</div></td>
  </tr></table>""" + confidencial(
            'La nota de remisión acredita la entrega de material o documentos al paciente. No lleva montos: '
            'lo cobrado figura en la factura asociada.'))

    # ---------------- Presupuesto (formato actual del sistema) ----------------
    validez = 30

    def tabla_presupuesto(lineas, descuento, etiqueta_dto='Descuento'):
        filas = ''
        subtotal = 0
        for i, (des, cant, precio) in enumerate(lineas, 1):
            subtotal += cant * precio
            filas += (f'<tr><td style="text-align: center; width: 6%;">{i}</td><td>{des}</td>'
                      f'<td style="text-align: center; width: 10%;">{cant}</td>'
                      f'<td class="num" style="width: 16%;">{gs(precio)}</td>'
                      f'<td class="num" style="width: 16%;">{gs(cant * precio)}</td></tr>')
        total = subtotal - descuento
        return f"""
  <table class="detalle"><tr><th>Nº</th><th>Servicio</th><th>Cant.</th><th>Precio unit. (Gs.)</th><th>Subtotal (Gs.)</th></tr>{filas}</table>
  <table class="totales" style="width: 40%; margin-left: auto; margin-top: 4px;">
    <tr><td>Subtotal</td><td class="num">{gs(subtotal)}</td></tr>
    <tr><td>{etiqueta_dto}</td><td class="num">- {gs(descuento)}</td></tr>
    <tr style="font-weight: bold; background: #dcdcdc;"><td>TOTAL Gs.</td><td class="num">{gs(total)}</td></tr>
  </table>
  <div style="font-size: 7.5pt; margin-top: 4px;">Son guaraníes: {numero_a_letras(total)}. Precios con IVA incluido.</div>""", total

    det_pres, _ = tabla_presupuesto([('EVALUACION PSICOPEDAGOGICA', 1, 200000),
                                     ('CONSULTA PSICOLOGICA', 4, 150000)], 50000)
    presupuesto = documento(
        'Presupuesto PRES-2026-10-0001',
        encabezado('PRESUPUESTO', 'PRES-2026-10-0001', 'Presupuesto · Documento sin valor fiscal', hoy)
        + bloque_paciente() + f"""
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr>
      <td style="width: 40%;"><span class="lbl">Profesional</span>{fv(gen.get('nombre_completo'))}</td>
      <td style="width: 20%;"><span class="lbl">Moneda</span>Guaraníes (PYG)</td>
      <td style="width: 20%;"><span class="lbl">Válido hasta</span>{fecha_corta(hoy + timedelta(days=validez))}</td>
      <td style="width: 20%;"><span class="lbl">Estado</span>PENDIENTE</td>
    </tr>
  </table>
  <div class="seccion">Detalle</div>{det_pres}
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Observaciones</span>Las sesiones se agendan según disponibilidad. El presupuesto aprobado puede convertirse en pedido.</td></tr>
  </table>
  <table class="firmas no-cortar"><tr>
    <td><div class="linea"><b>{fv(gen.get('nombre_completo'))}</b><br>Profesional</div></td>
    <td><div class="linea"><b>Aceptación del paciente o responsable</b><br>Firma, aclaración y C.I.</div></td>
  </tr></table>""" + confidencial(
            f'Presupuesto válido por {validez} días. No constituye comprobante de venta.'))

    # ---------------- Presupuesto de plan de tratamiento (PEI, propuesta) ----------------
    etapas = [('ETAPA 1 · EVALUACION INICIAL — EVALUACION PSICOPEDAGOGICA', 1, 200000),
              ('ETAPA 2 · INTERVENCION — SESION DE TERAPIA INDIVIDUAL (SEMANAL)', 12, 150000),
              ('ETAPA 2 · INTERVENCION — ENTRENAMIENTO EN ESTRATEGIAS DE LECTURA (QUINCENAL)', 6, 150000),
              ('ETAPA 3 · CIERRE — REEVALUACION E INFORME FINAL', 1, 200000)]
    subtotal_plan = sum(c * p for _, c, p in etapas)
    det_plan, total_plan = tabla_presupuesto(etapas, round(subtotal_plan * 0.10),
                                             'Descuento por plan completo (10%)')
    cuota = total_plan / 4
    presupuesto_plan = documento(
        'Presupuesto de plan de tratamiento PRES-2026-10-0002',
        encabezado('PRESUPUESTO DE<br>PLAN DE TRATAMIENTO', 'PRES-2026-10-0002',
                   'Presupuesto de tratamiento · Documento confidencial', hoy)
        + bloque_paciente() + f"""
  <div class="seccion">Plan de tratamiento (PEI versión 1 · ACTIVO)</div>
  <table class="tabla-datos">
    <tr><td colspan="2"><span class="lbl">Diagnóstico de referencia (CIE-10)</span>{dx_html}</td></tr>
    <tr><td colspan="2"><span class="lbl">Objetivos</span>Mejorar la fluidez y la comprensión lectora; incorporar estrategias compensatorias para el ámbito laboral y académico; reducir la ansiedad asociada a la lectura.</td></tr>
    <tr>
      <td style="width: 50%;"><span class="lbl">Áreas de intervención</span>Lectoescritura · Cognitiva (memoria de trabajo, procesamiento fonológico) · Emocional</td>
      <td style="width: 50%;"><span class="lbl">Estrategias</span>Intervención psicopedagógica en lectura, entrenamiento en estrategias de comprensión, herramientas de apoyo (lectura asistida), acompañamiento emocional.</td>
    </tr>
    <tr>
      <td><span class="lbl">Duración estimada</span>4 meses (16 semanas)</td>
      <td><span class="lbl">Cronograma de seguimiento</span>Revisión del plan cada 4 semanas; reevaluación al finalizar la etapa 2.</td>
    </tr>
  </table>
  <div class="seccion">Servicios presupuestados por etapa</div>{det_plan}
  <div class="seccion" style="margin-top: 8px;">Formas de pago</div>
  <table class="tabla-datos">
    <tr>
      <td style="width: 33%;"><span class="lbl">Contado (plan completo)</span>Gs. {gs(total_plan)}</td>
      <td style="width: 34%;"><span class="lbl">Crédito · 4 cuotas mensuales</span>Gs. {gs(cuota)} c/u</td>
      <td style="width: 33%;"><span class="lbl">Por sesión (sin descuento)</span>Según precio vigente de cada servicio</td>
    </tr>
  </table>
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Condiciones</span>La cantidad de sesiones es estimada: si el plan cambia se emite una nueva versión del PEI y un nuevo presupuesto. Las sesiones no realizadas sin aviso con 24 h de anticipación se consideran realizadas. Válido por {validez} días (hasta el {fecha_corta(hoy + timedelta(days=validez))}).</td></tr>
  </table>
  <table class="firmas no-cortar"><tr>
    <td><div class="linea"><b>{fv(gen.get('nombre_completo'))}</b><br>Matrícula Nº {fv(gen.get('matricula'))}</div></td>
    <td><div class="linea"><b>Conformidad del paciente o responsable</b><br>Firma, aclaración y C.I.</div></td>
  </tr></table>""" + confidencial(
            'Documento con datos de salud del paciente. Prototipo: hoy el presupuesto no está ligado al PEI; '
            'requiere agregar id_pei a la tabla presupuestos.'))

    for nombre, html in [('orden_estudios_ejemplo', orden), ('receta_ejemplo', receta),
                         ('certificado_asistencia_ejemplo', certificado),
                         ('nota_credito_ejemplo', nota_credito), ('nota_debito_ejemplo', nota_debito),
                         ('nota_remision_ejemplo', remision), ('presupuesto_ejemplo', presupuesto),
                         ('presupuesto_plan_tratamiento_ejemplo', presupuesto_plan)]:
        with open(f'{SALIDA}/{nombre}.html', 'w', encoding='utf-8') as f:
            f.write(html)
        HTML(string=html, base_url='/app').write_pdf(f'{SALIDA}/{nombre}.pdf')
        print('generado', nombre, os.path.getsize(f'{SALIDA}/{nombre}.pdf'), 'bytes')


if __name__ == '__main__':
    with app.app_context():
        main(int(sys.argv[1]) if len(sys.argv) > 1 else 6,
             int(sys.argv[2]) if len(sys.argv) > 2 else 3)
