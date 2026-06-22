"""
Módulo centralizado de Autenticación y Seguridad
================================================

Este módulo centraliza todas las funcionalidades relacionadas con autenticación,
autorización y seguridad del sistema.

Estructura:
- routes: Rutas y blueprints de autenticación
- dao: Data Access Objects para seguridad
- services: Lógica de negocio de autenticación
- middleware: Middleware de autenticación
- tasks: Tareas programadas de seguridad
- utils: Utilidades (validadores, decoradores)
"""

# ============================================================================
# ROUTES - Rutas y Blueprints
# ============================================================================
from app.auth.routes.login import logmod as login_blueprint
from app.auth.routes.auth_api import authapi as auth_api_blueprint
from app.auth.routes.admin_api import adminauthapi as admin_auth_api_blueprint

# ============================================================================
# DAO - Data Access Objects
# ============================================================================
from app.dao.auth.auth_dao import AuthDao
from app.dao.auth.user_dao import UsuarioDao

# ============================================================================
# SERVICES - Lógica de Negocio
# ============================================================================
from app.auth.services.auth_service import AuthService

# ============================================================================
# MIDDLEWARE - Middleware de Autenticación
# ============================================================================
from app.auth.middleware.auth_middleware import verificar_sesion_mejorada

# ============================================================================
# TASKS - Tareas Programadas
# ============================================================================
from app.auth.tasks.auth_tasks import limpiar_sesiones_expiradas, limpiar_tokens_expirados

# ============================================================================
# UTILS - Utilidades
# ============================================================================
from app.auth.utils.decorators import role_required
from app.auth.utils.password_validator import validar_politica_password

# ============================================================================
# EXPORTS - Lo que se puede importar desde app.auth
# ============================================================================
__all__ = [
    # Blueprints
    'login_blueprint',
    'auth_api_blueprint',
    'admin_auth_api_blueprint',
    # DAOs
    'AuthDao',
    'UsuarioDao',
    # Services
    'AuthService',
    # Middleware
    'verificar_sesion_mejorada',
    # Tasks
    'limpiar_sesiones_expiradas',
    'limpiar_tokens_expirados',
    # Utils
    'role_required',
    'validar_politica_password',
]


