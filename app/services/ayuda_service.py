import base64
import os
from io import BytesIO

from flask import current_app as app

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint no disponible ({type(e).__name__}: {e}). Usando xhtml2pdf como alternativa.")
    from xhtml2pdf import pisa


class AyudaService:
    """
    Servicio del manual de ayuda: convierte el mismo HTML que se muestra en la
    vista previa a PDF, mismo patrón que ReporteService / FacturaPDFService.
    """

    def logo_base64(self):
        """Logo de SYSCLIN embebido (mismo criterio que factura/ficha): así sale igual en la vista previa y en el PDF."""
        ruta = os.path.join(app.root_path, 'static', 'img', 'sys_logo.png')
        try:
            with open(ruta, 'rb') as f:
                return base64.b64encode(f.read()).decode('ascii')
        except OSError:
            return None

    def generar_pdf_manual(self, html_renderizado):
        buffer = BytesIO()

        if WEASYPRINT_AVAILABLE:
            HTML(string=html_renderizado, base_url=app.config.get('SERVER_NAME', '')).write_pdf(buffer)
        else:
            pisa_status = pisa.CreatePDF(html_renderizado, dest=buffer, encoding='utf-8')
            if pisa_status.err:
                raise Exception(f"Error al generar PDF con xhtml2pdf: {pisa_status.err}")

        return buffer.getvalue()

    def manual_tecnico_docx(self, partes, anexos, scripts, fecha, datos):
        """Manual técnico (seguridad o infraestructura) en Word, con el formato estándar (manual_word_service)."""
        # Import local: si falta python-docx, falla solo esta descarga y no el arranque de la app
        from app.services import manual_word_service
        return manual_word_service.manual_tecnico(
            raiz=os.path.abspath(os.path.join(app.root_path, '..')),
            partes=partes,
            anexos=anexos,
            scripts=scripts,
            logo=os.path.join(app.root_path, 'static', 'img', 'sys_logo.png'),
            fecha=fecha,
            datos=datos)

    def manual_tecnico_pdf(self, partes, anexos, scripts, fecha, datos):
        """PDF exportado del mismo Word con LibreOffice: el PDF y el Word quedan iguales."""
        from app.services import manual_word_service
        return manual_word_service.docx_a_pdf(self.manual_tecnico_docx(partes, anexos, scripts, fecha, datos))

    def manual_sistema_docx(self, partes, scripts, fecha):
        """Manual del sistema (guías de uso + seguridad) en Word, con el formato estándar (manual_word_service)."""
        from app.services import manual_word_service
        return manual_word_service.manual_sistema(
            partes=partes,
            raiz=os.path.abspath(os.path.join(app.root_path, '..')),
            scripts=scripts,
            logo=os.path.join(app.root_path, 'static', 'img', 'sys_logo.png'),
            fecha=fecha)

    def manual_sistema_pdf(self, partes, scripts, fecha):
        """PDF exportado del mismo Word con LibreOffice: el PDF y el Word quedan iguales."""
        from app.services import manual_word_service
        return manual_word_service.docx_a_pdf(self.manual_sistema_docx(partes, scripts, fecha))
