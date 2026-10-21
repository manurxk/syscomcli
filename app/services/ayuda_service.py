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

    def manual_seguridad_docx(self, secciones, scripts, fecha):
        """Manual de seguridad en Word, con el formato estándar (manual_word_service)."""
        # Import local: si falta python-docx, falla solo esta descarga y no el arranque de la app
        from app.services import manual_word_service
        return manual_word_service.manual_seguridad(
            raiz=os.path.abspath(os.path.join(app.root_path, '..')),
            dir_secciones=os.path.join(app.root_path, 'rutas', 'ayuda', 'templates'),
            secciones=secciones,
            scripts=scripts,
            logo=os.path.join(app.root_path, 'static', 'img', 'sys_logo.png'),
            fecha=fecha)

    def manual_seguridad_pdf(self, secciones, scripts, fecha):
        """PDF exportado del mismo Word con LibreOffice: el PDF y el Word quedan iguales."""
        from app.services import manual_word_service
        return manual_word_service.docx_a_pdf(self.manual_seguridad_docx(secciones, scripts, fecha))

    def manual_guia_docx(self, secciones_html, perfil, fecha):
        """Guía de uso (manual de usuario) en Word, con el formato estándar (manual_word_service)."""
        from app.services import manual_word_service
        return manual_word_service.manual_guia(
            secciones_html=secciones_html,
            perfil=perfil,
            logo=os.path.join(app.root_path, 'static', 'img', 'sys_logo.png'),
            fecha=fecha)

    def manual_guia_pdf(self, secciones_html, perfil, fecha):
        """PDF exportado del mismo Word con LibreOffice: el PDF y el Word quedan iguales."""
        from app.services import manual_word_service
        return manual_word_service.docx_a_pdf(self.manual_guia_docx(secciones_html, perfil, fecha))
