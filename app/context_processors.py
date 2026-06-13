from flask_wtf.csrf import generate_csrf
from datetime import datetime
from app.config.version import get_version, get_version_full, RELEASE_DATE
from app.services.ui_settings_service import UISettingsService
from app.dao.referenciales.ventas.empresa.EmpresaDao import EmpresaDao
from app.utils.sidebar_builder import build_sidebar

def init_context_processors(app):
    """Initialize context processors for templates."""
    
    @app.context_processor
    def inject_global_data():
        """Make global variables available in all templates."""
        # Obtener configuración de la clínica para branding global
        try:
            empresadao = EmpresaDao()
            config_clinica = empresadao.getEmpresaPrincipal()
        except:
            config_clinica = None

        return dict(
            csrf_token=generate_csrf,
            app_version=get_version(),
            app_version_full=get_version_full(),
            app_release_date=RELEASE_DATE,
            current_year=datetime.now().year,
            ui=UISettingsService.obtener_preferencias(),
            clinica=config_clinica,
            sidebar_items=build_sidebar()
        )
