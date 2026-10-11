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

    def generar_pdf_manual(self, html_renderizado):
        buffer = BytesIO()

        if WEASYPRINT_AVAILABLE:
            HTML(string=html_renderizado, base_url=app.config.get('SERVER_NAME', '')).write_pdf(buffer)
        else:
            pisa_status = pisa.CreatePDF(html_renderizado, dest=buffer, encoding='utf-8')
            if pisa_status.err:
                raise Exception(f"Error al generar PDF con xhtml2pdf: {pisa_status.err}")

        return buffer.getvalue()
