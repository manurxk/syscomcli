import os
from io import BytesIO
from xhtml2pdf import pisa
from flask import render_template, current_app as app
from datetime import datetime

class ContratoPDFService:
    """
    Servicio para generar contratos en PDF a partir de plantillas HTML
    usando xhtml2pdf.
    """

    def generar_contrato_pdf(self, datos_contrato, template_name='contrato_template.html'):
        """
        Genera un PDF del contrato.
        
        Args:
            datos_contrato (dict): Diccionario con datos del presupuesto, paciente, citas, etc.
            template_name (str): Ruta al template HTML dentro de la carpeta templates de Flask.
            
        Returns:
            BytesIO: Buffer con el binario del PDF generado.
        """
        try:
            # Añadir fecha de generación
            datos_contrato['fecha_impresion'] = datetime.now().strftime('%d/%m/%Y %H:%M')
            
            # Obtener el HTML renderizado usando Flask
            html_content = render_template(template_name, **datos_contrato)
            
            # Crear un buffer en memoria
            result_file = BytesIO()
            
            # Convertir HTML a PDF
            # pisa.CreatePDF requiere la codificación correcta
            pisa_status = pisa.CreatePDF(
                src=html_content,    # String con HTML
                dest=result_file,     # Archivo de salida o buffer
                encoding='utf-8'
            )
            
            if pisa_status.err:
                app.logger.error(f"Error generando PDF de contrato: {pisa_status.err}")
                return None
                
            # Retornar el archivo virtual al principio para lectura
            result_file.seek(0)
            return result_file
            
        except Exception as e:
            app.logger.error(f"Error interno generando contrato PDF: {str(e)}", exc_info=True)
            return None
