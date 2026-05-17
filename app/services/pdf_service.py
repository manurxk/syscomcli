# app/services/pdf_service.py

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.platypus import Image as RLImage
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from io import BytesIO
from datetime import datetime


class FichaMedicaPDFService:
    """
    Servicio para generar PDFs de fichas médicas
    Utiliza ReportLab para crear documentos profesionales
    """
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        # Paleta de colores moderna y profesional
        self.colores = {
            'primario': colors.HexColor('#2563eb'),  # Azul moderno
            'primario_oscuro': colors.HexColor('#1e40af'),  # Azul oscuro
            'secundario': colors.HexColor('#0891b2'),  # Cyan
            'accento': colors.HexColor('#7c3aed'),  # Púrpura
            'exito': colors.HexColor('#10b981'),  # Verde
            'advertencia': colors.HexColor('#f59e0b'),  # Amarillo
            'peligro': colors.HexColor('#ef4444'),  # Rojo
            'gris_oscuro': colors.HexColor('#1f2937'),
            'gris_medio': colors.HexColor('#6b7280'),
            'gris_claro': colors.HexColor('#f3f4f6'),
            'gris_borde': colors.HexColor('#e5e7eb'),
            'fondo_claro': colors.HexColor('#f9fafb'),
            'fondo_azul': colors.HexColor('#eff6ff'),
            'fondo_verde': colors.HexColor('#ecfdf5'),
            'fondo_amarillo': colors.HexColor('#fffbeb'),
        }
        self._configurar_estilos()
    
    def _configurar_estilos(self):
        """Configura estilos personalizados para el PDF con diseño moderno"""
        # Estilo para títulos principales
        self.styles.add(ParagraphStyle(
            name='TituloFicha',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.colores['primario_oscuro'],
            spaceAfter=16,
            spaceBefore=0,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold',
            leading=28
        ))
        
        # Estilo para subtítulos (secciones principales)
        self.styles.add(ParagraphStyle(
            name='Subtitulo',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=self.colores['primario'],
            spaceAfter=14,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            leading=20,
            borderWidth=0,
            borderPadding=0,
            borderColor=self.colores['gris_borde'],
            backColor=self.colores['fondo_azul']
        ))
        
        # Estilo para secciones secundarias
        self.styles.add(ParagraphStyle(
            name='Seccion',
            parent=self.styles['Heading3'],
            fontSize=13,
            textColor=self.colores['gris_oscuro'],
            spaceAfter=10,
            spaceBefore=14,
            fontName='Helvetica-Bold',
            leading=16
        ))
        
        # Estilo para texto normal mejorado
        self.styles.add(ParagraphStyle(
            name='TextoNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=7,
            fontName='Helvetica',
            textColor=self.colores['gris_oscuro'],
            leading=12
        ))
        
        # Estilo para datos importantes
        self.styles.add(ParagraphStyle(
            name='DatoImportante',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=self.colores['primario'],
            fontName='Helvetica-Bold',
            leading=12
        ))
        
        # Estilo para texto en bloques (anamnesis)
        self.styles.add(ParagraphStyle(
            name='TextoBloque',
            parent=self.styles['Normal'],
            fontSize=9.5,
            spaceAfter=10,
            fontName='Helvetica',
            alignment=TA_JUSTIFY,
            textColor=self.colores['gris_oscuro'],
            leading=13,
            leftIndent=6,
            rightIndent=6
        ))
        
        # Estilo para etiquetas de campos
        self.styles.add(ParagraphStyle(
            name='Etiqueta',
            parent=self.styles['Normal'],
            fontSize=9.5,
            textColor=self.colores['gris_medio'],
            fontName='Helvetica-Bold',
            leading=11
        ))
    
    def generar_ficha_completa(self, ficha_data):
        """
        Genera un PDF completo de la ficha médica
        
        Args:
            ficha_data (dict): Diccionario con toda la información de la ficha médica
            
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        buffer = BytesIO()
        
        # Crear documento PDF con márgenes mejorados
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=40,
            leftMargin=40,
            topMargin=60,
            bottomMargin=50,
            title="Ficha Médica",
            author="Sistema Clínico"
        )
        
        # Lista de elementos del documento
        elementos = []
        
        # Agregar encabezado
        elementos.extend(self._crear_encabezado(ficha_data.get('paciente', {})))
        
        # Agregar información del paciente
        elementos.extend(self._crear_info_paciente(ficha_data.get('paciente', {})))
        
        # Agregar estadísticas
        elementos.extend(self._crear_estadisticas(ficha_data.get('estadisticas', {})))
        
        # Agregar anamnesis si existe
        if ficha_data.get('anamnesis'):
            elementos.extend(self._crear_anamnesis(ficha_data.get('anamnesis', {})))
        
        # Agregar timeline de eventos
        if ficha_data.get('timeline'):
            elementos.extend(self._crear_timeline(ficha_data.get('timeline', [])))
        
        # Agregar tratamientos activos
        if ficha_data.get('tratamientos_activos'):
            elementos.extend(self._crear_tratamientos(ficha_data.get('tratamientos_activos', [])))
        
        # Agregar diagnósticos
        if ficha_data.get('diagnosticos'):
            elementos.extend(self._crear_diagnosticos(ficha_data.get('diagnosticos', [])))
        
        # Agregar consultas recientes
        if ficha_data.get('consultas_recientes'):
            elementos.extend(self._crear_consultas(ficha_data.get('consultas_recientes', [])))
        
        # Agregar procedimientos
        if ficha_data.get('procedimientos'):
            elementos.extend(self._crear_procedimientos(ficha_data.get('procedimientos', [])))
        
        # Agregar próximas citas
        if ficha_data.get('proximas_citas'):
            elementos.extend(self._crear_citas(ficha_data.get('proximas_citas', [])))
        
        # Agregar pie de página
        elementos.extend(self._crear_pie_pagina())
        
        # Construir PDF
        doc.build(elementos)
        
        # Posicionar el buffer al inicio
        buffer.seek(0)
        return buffer
    
    def generar_ficha_basica(self, ficha_data):
        """
        Genera un PDF básico con información resumida
        
        Args:
            ficha_data (dict): Diccionario con la información de la ficha médica
            
        Returns:
            BytesIO: Buffer con el PDF generado
        """
        buffer = BytesIO()
        
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50
        )
        
        elementos = []
        
        # Agregar encabezado
        elementos.extend(self._crear_encabezado(ficha_data.get('paciente', {})))
        
        # Agregar información del paciente
        elementos.extend(self._crear_info_paciente(ficha_data.get('paciente', {})))
        
        # Agregar estadísticas
        elementos.extend(self._crear_estadisticas(ficha_data.get('estadisticas', {})))
        
        # Incluir resumen de anamnesis en ficha básica
        if ficha_data.get('anamnesis'):
            elementos.extend(self._crear_anamnesis_resumen(ficha_data.get('anamnesis', {})))
        
        # Solo tratamientos activos
        if ficha_data.get('tratamientos_activos'):
            elementos.extend(self._crear_tratamientos(ficha_data.get('tratamientos_activos', [])))
        
        # Agregar pie de página
        elementos.extend(self._crear_pie_pagina())
        
        doc.build(elementos)
        buffer.seek(0)
        return buffer
    
    def _crear_encabezado(self, paciente):
        """Crea el encabezado del documento con diseño mejorado"""
        elementos = []
        
        # Barra superior decorativa
        barra_superior = Table(
            [['']],
            colWidths=[7*inch],
            rowHeights=[0.15*inch]
        )
        barra_superior.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['primario']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(barra_superior)
        elementos.append(Spacer(1, 0.25 * inch))
        
        # Título principal con mejor diseño
        titulo = Paragraph(
            "FICHA MÉDICA DEL PACIENTE",
            self.styles['TituloFicha']
        )
        elementos.append(titulo)
        elementos.append(Spacer(1, 0.15 * inch))
        
        # Fecha de generación con diseño mejorado
        fecha_actual = datetime.now().strftime("%d/%m/%Y a las %H:%M")
        fecha_texto = Paragraph(
            f"<font color='{self.colores['gris_medio']}'><i>Documento generado el {fecha_actual}</i></font>",
            ParagraphStyle(
                'FechaGen',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=self.colores['gris_medio'],
                alignment=TA_CENTER,
                spaceAfter=0
            )
        )
        elementos.append(fecha_texto)
        elementos.append(Spacer(1, 0.35 * inch))
        
        # Línea separadora decorativa
        linea_separadora = Table(
            [['']],
            colWidths=[7*inch],
            rowHeights=[1]
        )
        linea_separadora.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['gris_borde']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(linea_separadora)
        elementos.append(Spacer(1, 0.25 * inch))
        
        return elementos
    
    def _crear_info_paciente(self, paciente):
        """Crea la sección de información del paciente con diseño mejorado"""
        elementos = []
        
        # Título de sección con fondo
        titulo_seccion = Table(
            [[Paragraph("DATOS DEL PACIENTE", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        # Crear tabla con información del paciente
        datos = [
            ['Historia Clínica:', paciente.get('historia_clinica', 'N/A')],
            ['Nombre Completo:', paciente.get('nombre_completo', 'N/A')],
            ['Cédula:', paciente.get('cedula', 'N/A')],
            ['Fecha de Nacimiento:', paciente.get('fecha_nacimiento', 'N/A')],
            ['Edad:', f"{paciente.get('edad', 'N/A')} años"],
            ['Género:', paciente.get('genero', 'N/A')],
            ['Teléfono:', paciente.get('telefono', 'N/A')],
            ['Correo:', paciente.get('correo', 'N/A')],
            ['Domicilio:', paciente.get('domicilio', 'N/A')],
            ['Ciudad:', paciente.get('ciudad', 'N/A')]
        ]
        
        tabla = Table(datos, colWidths=[2.2*inch, 4.8*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_claro']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colores['primario']),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.35 * inch))
        
        return elementos
    
    def _crear_tratamientos(self, tratamientos):
        """Crea la sección de tratamientos activos"""
        elementos = []
        
        if not tratamientos:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("TRATAMIENTOS ACTIVOS", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_verde']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        for i, t in enumerate(tratamientos, 1):
            elementos.append(Paragraph(f"<b>Tratamiento {i}:</b> {t.get('descripcion', 'Sin descripción')}", 
                                     self.styles['Seccion']))
            
            datos_trat = [
                ['Estado:', t.get('estado', 'N/A')],
                ['Tipo:', t.get('tipo_tratamiento', 'N/A')],
                ['Fecha Inicio:', t.get('fecha_inicio', 'N/A')],
                ['Fecha Fin:', t.get('fecha_fin', 'N/A') if t.get('fecha_fin') else 'Sin definir'],
                ['Duración:', f"{t.get('dias_tratamiento', 0)} días"],
                ['Sesiones:', f"{t.get('numero_sesiones', 'N/A')} - {t.get('frecuencia_sesiones', 'N/A')}"],
                ['Diagnóstico:', t.get('diagnostico', 'N/A')],
            ]
            
            if t.get('objetivos'):
                datos_trat.append(['Objetivos:', t.get('objetivos')])
            
            tabla_trat = Table(datos_trat, colWidths=[1.5*inch, 4.5*inch])
            tabla_trat.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_verde']),
                ('TEXTCOLOR', (0, 0), (0, -1), self.colores['exito']),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ]))
            
            elementos.append(tabla_trat)
            elementos.append(Spacer(1, 0.2 * inch))
        
        return elementos
    
    def _crear_diagnosticos(self, diagnosticos):
        """Crea la sección de diagnósticos"""
        elementos = []
        
        if not diagnosticos:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("DIAGNÓSTICOS REGISTRADOS", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        datos = [['Fecha', 'Diagnóstico', 'CIE-10', 'Tipo', 'Gravedad', 'Profesional']]
        
        for d in diagnosticos[:15]:  # Limitar a 15 diagnósticos
            # Color según gravedad
            gravedad = d.get('gravedad', 'N/A')
            
            datos.append([
                d.get('fecha', 'N/A'),
                d.get('diagnostico', 'N/A')[:30] + '...' if len(d.get('diagnostico', '')) > 30 else d.get('diagnostico', 'N/A'),
                d.get('codigo_cie10', 'N/A'),
                d.get('tipo', 'N/A'),
                gravedad,
                d.get('profesional', 'N/A')[:20] + '...' if len(d.get('profesional', '')) > 20 else d.get('profesional', 'N/A')
            ])
        
        tabla = Table(datos, colWidths=[0.9*inch, 1.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch])
        
        # Estilo base mejorado
        estilo_tabla = [
            ('BACKGROUND', (0, 0), (-1, 0), self.colores['primario']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]
        
        # Agregar colores según gravedad
        for i, d in enumerate(diagnosticos[:15], 1):
            if d.get('gravedad') == 'GRAVE':
                estilo_tabla.append(('TEXTCOLOR', (4, i), (4, i), self.colores['peligro']))
                estilo_tabla.append(('FONTNAME', (4, i), (4, i), 'Helvetica-Bold'))
            elif d.get('gravedad') == 'MODERADA':
                estilo_tabla.append(('TEXTCOLOR', (4, i), (4, i), self.colores['advertencia']))
        
        tabla.setStyle(TableStyle(estilo_tabla))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.3 * inch))
        
        return elementos
    
    def _crear_consultas(self, consultas):
        """Crea la sección de consultas recientes"""
        elementos = []
        
        if not consultas:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("CONSULTAS RECIENTES", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        for i, c in enumerate(consultas[:10], 1):  # Limitar a 10 consultas
            elementos.append(Paragraph(
                f"<b>Consulta {i} - {c.get('fecha', 'N/A')}</b>", 
                self.styles['Seccion']
            ))
            
            datos_consulta = [
                ['Motivo:', c.get('motivo', 'N/A')],
                ['Estado:', c.get('estado', 'N/A')],
                ['Profesional:', c.get('profesional', 'N/A')],
                ['Matrícula:', c.get('matricula', 'N/A')],
                ['Diagnósticos:', str(c.get('total_diagnosticos', 0))],
                ['Procedimientos:', str(c.get('total_procedimientos', 0))],
            ]
            
            if c.get('descripcion'):
                datos_consulta.append(['Descripción:', c.get('descripcion')[:150] + '...' if len(c.get('descripcion', '')) > 150 else c.get('descripcion')])
            
            tabla_consulta = Table(datos_consulta, colWidths=[1.5*inch, 4.5*inch])
            tabla_consulta.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_azul']),
                ('TEXTCOLOR', (0, 0), (0, -1), self.colores['primario']),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ]))
            
            elementos.append(tabla_consulta)
            elementos.append(Spacer(1, 0.15 * inch))
        
        return elementos
    
    def _crear_procedimientos(self, procedimientos):
        """Crea la sección de procedimientos"""
        elementos = []
        
        if not procedimientos:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("PROCEDIMIENTOS REALIZADOS", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        datos = [['Fecha', 'Tipo de Procedimiento', 'Duración', 'Resultado', 'Profesional']]
        
        for p in procedimientos[:15]:  # Limitar a 15 procedimientos
            datos.append([
                p.get('fecha', 'N/A'),
                p.get('tipo_procedimiento', 'N/A')[:25] + '...' if len(p.get('tipo_procedimiento', '')) > 25 else p.get('tipo_procedimiento', 'N/A'),
                p.get('duracion', 'N/A'),
                p.get('resultado', 'N/A')[:20] + '...' if len(p.get('resultado', '')) > 20 else p.get('resultado', 'N/A'),
                p.get('profesional', 'N/A')[:20] + '...' if len(p.get('profesional', '')) > 20 else p.get('profesional', 'N/A')
            ])
        
        tabla = Table(datos, colWidths=[1.1*inch, 1.8*inch, 0.9*inch, 1.2*inch, 1.3*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colores['primario']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.3 * inch))
        
        return elementos
    
    def _crear_citas(self, citas):
        """Crea la sección de próximas citas"""
        elementos = []
        
        if not citas:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("PRÓXIMAS CITAS PROGRAMADAS", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_amarillo']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        for i, c in enumerate(citas, 1):
            elementos.append(Paragraph(
                f"<b>Cita {i} - {c.get('fecha', 'N/A')} a las {c.get('hora_inicio', 'N/A')}</b>",
                self.styles['Seccion']
            ))
            
            datos_cita = [
                ['Especialidad:', c.get('especialidad', 'N/A')],
                ['Especialista:', c.get('especialista', 'N/A')],
                ['Tipo:', c.get('tipo', 'N/A')],
                ['Horario:', f"{c.get('hora_inicio', 'N/A')} - {c.get('hora_fin', 'N/A')}"],
                ['Estado:', c.get('estado', 'N/A')],
                ['Días faltantes:', f"{c.get('dias_hasta_cita', 0)} días"],
            ]
            
            if c.get('motivo'):
                datos_cita.append(['Motivo:', c.get('motivo')])
            
            tabla_cita = Table(datos_cita, colWidths=[1.5*inch, 4.5*inch])
            
            # Color según días faltantes
            bg_color = self.colores['fondo_verde']  # Verde por defecto
            text_color = self.colores['exito']
            
            dias = c.get('dias_hasta_cita', 999)
            if dias <= 3:
                bg_color = colors.HexColor('#fee2e2')  # Rojo claro
                text_color = self.colores['peligro']
            elif dias <= 7:
                bg_color = self.colores['fondo_amarillo']  # Amarillo
                text_color = self.colores['advertencia']
            
            tabla_cita.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), bg_color),
                ('TEXTCOLOR', (0, 0), (0, -1), text_color),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                ('TOPPADDING', (0, 0), (-1, -1), 10),
                ('LEFTPADDING', (0, 0), (-1, -1), 10),
                ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ]))
            
            elementos.append(tabla_cita)
            elementos.append(Spacer(1, 0.15 * inch))
        
        return elementos
    
    def _crear_pie_pagina(self):
        """Crea el pie de página del documento con diseño mejorado"""
        elementos = []
        
        elementos.append(Spacer(1, 0.4 * inch))
        
        # Línea separadora
        linea_separadora = Table(
            [['']],
            colWidths=[7*inch],
            rowHeights=[1]
        )
        linea_separadora.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['gris_borde']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elementos.append(linea_separadora)
        elementos.append(Spacer(1, 0.2 * inch))
        
        # Texto del pie de página
        elementos.append(Paragraph(
            f"<font color='{self.colores['gris_medio']}'><i>Este documento es confidencial y contiene información médica sensible.<br/>"
            "Su uso está restringido a profesionales autorizados.</i></font>",
            ParagraphStyle(
                'PiePagina',
                parent=self.styles['Normal'],
                fontSize=8,
                textColor=self.colores['gris_medio'],
                alignment=TA_CENTER,
                leading=10
            )
        ))
        
        return elementos

    
    def _crear_estadisticas(self, estadisticas):
        """Crea la sección de estadísticas con diseño mejorado"""
        elementos = []
        
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("RESUMEN ESTADÍSTICO", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        datos = [
            ['Métrica', 'Valor'],
            ['Total de Consultas', str(estadisticas.get('total_consultas', 0))],
            ['Tratamientos Activos', str(estadisticas.get('tratamientos_activos', 0))],
            ['Total de Diagnósticos', str(estadisticas.get('total_diagnosticos', 0))],
            ['Diagnósticos Graves', str(estadisticas.get('diagnosticos_graves', 0))],
            ['Tiene Anamnesis', 'Sí' if estadisticas.get('tiene_anamnesis') else 'No'],
            ['Próxima Cita', estadisticas.get('proxima_cita', 'Sin citas programadas')]
        ]
        
        tabla = Table(datos, colWidths=[3.5*inch, 3.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colores['primario']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 1), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.35 * inch))
        
        return elementos
    
    def _crear_anamnesis(self, anamnesis):
        """Crea la sección completa de anamnesis"""
        elementos = []
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("ANAMNESIS PSICOLÓGICA", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        # Información básica
        datos_basicos = [
            ['Fecha de Elaboración:', anamnesis.get('fecha_elaboracion', 'N/A')],
            ['Última Modificación:', anamnesis.get('fecha_ultima_modificacion', 'N/A')],
            ['Versión:', str(anamnesis.get('version', 1))],
            ['Elaborada por:', anamnesis.get('elaborado_por', 'N/A')],
        ]
        
        if anamnesis.get('informante'):
            datos_basicos.append(['Informante:', anamnesis.get('informante')])
        if anamnesis.get('relacion_informante'):
            datos_basicos.append(['Relación:', anamnesis.get('relacion_informante')])
        
        tabla_basica = Table(datos_basicos, colWidths=[2*inch, 4*inch])
        tabla_basica.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_amarillo']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colores['advertencia']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
        ]))
        
        elementos.append(tabla_basica)
        elementos.append(Spacer(1, 0.2 * inch))
        
        # Motivo de Consulta
        if anamnesis.get('motivo_consulta'):
            elementos.append(Paragraph("Motivo de Consulta", self.styles['Seccion']))
            elementos.append(Paragraph(anamnesis.get('motivo_consulta'), self.styles['TextoBloque']))
            elementos.append(Spacer(1, 0.15 * inch))
        
        # Antecedentes
        antecedentes = anamnesis.get('antecedentes', {})
        if any(antecedentes.values()):
            elementos.append(Paragraph("Antecedentes", self.styles['Seccion']))
            
            if antecedentes.get('patologicos_personales'):
                elementos.append(Paragraph("<b>Personales:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(antecedentes.get('patologicos_personales'), self.styles['TextoBloque']))
            
            if antecedentes.get('patologicos_familiares'):
                elementos.append(Paragraph("<b>Familiares:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(antecedentes.get('patologicos_familiares'), self.styles['TextoBloque']))
            
            if antecedentes.get('historia_familiar'):
                elementos.append(Paragraph("<b>Historia Familiar:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(antecedentes.get('historia_familiar'), self.styles['TextoBloque']))
            
            elementos.append(Spacer(1, 0.15 * inch))
        
        # Historias
        historias = anamnesis.get('historias', {})
        if any(historias.values()):
            elementos.append(PageBreak())
            elementos.append(Paragraph("Historia Clínica", self.styles['Seccion']))
            
            if historias.get('problema_actual'):
                elementos.append(Paragraph("<b>Problema Actual:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(historias.get('problema_actual'), self.styles['TextoBloque']))
            
            if historias.get('desarrollo'):
                elementos.append(Paragraph("<b>Desarrollo:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(historias.get('desarrollo'), self.styles['TextoBloque']))
            
            if historias.get('academica'):
                elementos.append(Paragraph("<b>Historia Académica:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(historias.get('academica'), self.styles['TextoBloque']))
            
            if historias.get('laboral'):
                elementos.append(Paragraph("<b>Historia Laboral:</b>", self.styles['TextoNormal']))
                elementos.append(Paragraph(historias.get('laboral'), self.styles['TextoBloque']))
            
            elementos.append(Spacer(1, 0.15 * inch))
        
        # Medicación
        medicacion = anamnesis.get('medicacion', {})
        if any(medicacion.values()):
            elementos.append(Paragraph("Medicación y Sustancias", self.styles['Seccion']))
            
            if medicacion.get('actual'):
                elementos.append(Paragraph("<b>Actual:</b> " + medicacion.get('actual'), self.styles['TextoBloque']))
            
            if medicacion.get('psiquiatrica_previa'):
                elementos.append(Paragraph("<b>Psiquiátrica Previa:</b> " + medicacion.get('psiquiatrica_previa'), self.styles['TextoBloque']))
            
            if medicacion.get('consumo_sustancias'):
                elementos.append(Paragraph("<b>Consumo de Sustancias:</b> " + medicacion.get('consumo_sustancias'), self.styles['TextoBloque']))
            
            elementos.append(Spacer(1, 0.15 * inch))
        
        # Áreas de Funcionamiento
        areas = anamnesis.get('areas_funcionamiento', {})
        if any(areas.values()):
            elementos.append(PageBreak())
            elementos.append(Paragraph("Áreas de Funcionamiento", self.styles['Seccion']))
            
            datos_areas = []
            if areas.get('relaciones_interpersonales'):
                datos_areas.append(['Relaciones Interpersonales:', areas.get('relaciones_interpersonales')])
            if areas.get('actividad_fisica'):
                datos_areas.append(['Actividad Física:', areas.get('actividad_fisica')])
            if areas.get('patron_sueno'):
                datos_areas.append(['Patrón de Sueño:', areas.get('patron_sueno')])
            if areas.get('patron_alimentacion'):
                datos_areas.append(['Patrón de Alimentación:', areas.get('patron_alimentacion')])
            if areas.get('actividad_emocional'):
                datos_areas.append(['Actividad Emocional:', areas.get('actividad_emocional')])
            if areas.get('actividad_sexual'):
                datos_areas.append(['Actividad Sexual:', areas.get('actividad_sexual')])
            
            if datos_areas:
                tabla_areas = Table(datos_areas, colWidths=[2*inch, 4*inch])
                tabla_areas.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_verde']),
                    ('TEXTCOLOR', (0, 0), (0, -1), self.colores['exito']),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9.5),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('TOPPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
                    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
                ]))
                elementos.append(tabla_areas)
                elementos.append(Spacer(1, 0.15 * inch))
        
        # Impresión Diagnóstica y Plan
        if anamnesis.get('impresion_diagnostica'):
            elementos.append(Paragraph("Impresión Diagnóstica", self.styles['Seccion']))
            elementos.append(Paragraph(anamnesis.get('impresion_diagnostica'), self.styles['TextoBloque']))
            elementos.append(Spacer(1, 0.15 * inch))
        
        if anamnesis.get('plan_trabajo'):
            elementos.append(Paragraph("Plan de Trabajo", self.styles['Seccion']))
            elementos.append(Paragraph(anamnesis.get('plan_trabajo'), self.styles['TextoBloque']))
            elementos.append(Spacer(1, 0.15 * inch))
        
        # Evaluaciones y Terapias Requeridas
        evaluaciones = anamnesis.get('evaluaciones', {})
        terapias = anamnesis.get('terapias', {})
        
        if any(evaluaciones.values()) or any(terapias.values()):
            elementos.append(Paragraph("Intervenciones Requeridas", self.styles['Seccion']))
            
            datos_intervenciones = []
            
            # Evaluaciones
            if evaluaciones.get('neuropsicologica'):
                datos_intervenciones.append(['✓', 'Evaluación Neuropsicológica'])
            if evaluaciones.get('psicologica'):
                datos_intervenciones.append(['✓', 'Evaluación Psicológica'])
            if evaluaciones.get('psicopedagogica'):
                datos_intervenciones.append(['✓', 'Evaluación Psicopedagógica'])
            if evaluaciones.get('fonoaudiologica'):
                datos_intervenciones.append(['✓', 'Evaluación Fonoaudiológica'])
            if evaluaciones.get('psicomotora'):
                datos_intervenciones.append(['✓', 'Evaluación Psicomotora'])
            
            # Terapias
            if terapias.get('individual'):
                datos_intervenciones.append(['✓', 'Terapia Individual'])
            if terapias.get('familiar'):
                datos_intervenciones.append(['✓', 'Terapia Familiar'])
            if terapias.get('grupal'):
                datos_intervenciones.append(['✓', 'Terapia Grupal'])
            if terapias.get('ocupacional'):
                datos_intervenciones.append(['✓', 'Terapia Ocupacional'])
            if terapias.get('otra'):
                datos_intervenciones.append(['✓', f"Otra: {terapias.get('otra')}"])
            
            if datos_intervenciones:
                tabla_intervenciones = Table(datos_intervenciones, colWidths=[0.5*inch, 5.5*inch])
                tabla_intervenciones.setStyle(TableStyle([
                    ('TEXTCOLOR', (0, 0), (0, -1), self.colores['exito']),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (1, 0), (1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('TOPPADDING', (0, 0), (-1, -1), 8),
                    ('LEFTPADDING', (0, 0), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 0), (-1, -1), 10),
                    ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
                    ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ]))
                elementos.append(tabla_intervenciones)
                elementos.append(Spacer(1, 0.15 * inch))
        
        # Observaciones e Indicaciones
        if anamnesis.get('observaciones'):
            elementos.append(Paragraph("Observaciones", self.styles['Seccion']))
            elementos.append(Paragraph(anamnesis.get('observaciones'), self.styles['TextoBloque']))
            elementos.append(Spacer(1, 0.15 * inch))
        
        if anamnesis.get('indicaciones'):
            elementos.append(Paragraph("Indicaciones", self.styles['Seccion']))
            elementos.append(Paragraph(anamnesis.get('indicaciones'), self.styles['TextoBloque']))
        
        return elementos
    
    def _crear_anamnesis_resumen(self, anamnesis):
        """Crea un resumen condensado de la anamnesis para la ficha básica"""
        elementos = []
        
        elementos.append(Paragraph("ANAMNESIS (Resumen)", self.styles['Subtitulo']))
        
        datos = [
            ['Fecha:', anamnesis.get('fecha_elaboracion', 'N/A')],
            ['Versión:', str(anamnesis.get('version', 1))],
        ]
        
        if anamnesis.get('motivo_consulta'):
            motivo_corto = anamnesis.get('motivo_consulta')[:200] + '...' if len(anamnesis.get('motivo_consulta', '')) > 200 else anamnesis.get('motivo_consulta')
            datos.append(['Motivo:', motivo_corto])
        
        if anamnesis.get('impresion_diagnostica'):
            impresion_corta = anamnesis.get('impresion_diagnostica')[:200] + '...' if len(anamnesis.get('impresion_diagnostica', '')) > 200 else anamnesis.get('impresion_diagnostica')
            datos.append(['Impresión Diagnóstica:', impresion_corta])
        
        tabla = Table(datos, colWidths=[1.5*inch, 4.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), self.colores['fondo_amarillo']),
            ('TEXTCOLOR', (0, 0), (0, -1), self.colores['advertencia']),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TOPPADDING', (0, 0), (-1, -1), 10),
            ('LEFTPADDING', (0, 0), (-1, -1), 10),
            ('RIGHTPADDING', (0, 0), (-1, -1), 10),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ROWBACKGROUNDS', (0, 0), (-1, -1), [colors.white, self.colores['fondo_claro']]),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.2 * inch))
        
        return elementos
    
    def _crear_timeline(self, timeline):
        """Crea la sección de timeline de eventos"""
        elementos = []
        
        if not timeline:
            return elementos
        
        elementos.append(PageBreak())
        # Título con fondo
        titulo_seccion = Table(
            [[Paragraph("LÍNEA DE TIEMPO MÉDICA", self.styles['Subtitulo'])]],
            colWidths=[7*inch],
            rowHeights=[0.5*inch]
        )
        titulo_seccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colores['fondo_azul']),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
        ]))
        elementos.append(titulo_seccion)
        elementos.append(Spacer(1, 0.2 * inch))
        
        datos = [['Fecha', 'Tipo', 'Descripción', 'Profesional']]
        
        for evento in timeline[:20]:  # Limitar a 20 eventos
            datos.append([
                evento.get('fecha', 'N/A'),
                evento.get('tipo_evento', 'N/A'),
                evento.get('descripcion', 'N/A')[:50] + '...' if len(evento.get('descripcion', '')) > 50 else evento.get('descripcion', 'N/A'),
                evento.get('profesional', 'N/A')
            ])
        
        tabla = Table(datos, colWidths=[1.2*inch, 1.3*inch, 2.3*inch, 1.5*inch])
        tabla.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), self.colores['primario']),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, self.colores['gris_borde']),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, self.colores['fondo_claro']]),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        
        elementos.append(tabla)
        elementos.append(Spacer(1, 0.3 * inch))
        
        return elementos