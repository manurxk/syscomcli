"""
Manejo centralizado de errores HTTP.
"""

from flask import Blueprint, render_template, redirect, url_for

error_bp = Blueprint("errors", __name__)


@error_bp.app_errorhandler(404)
def page_not_found(error):  # noqa: D401, ARG001
    """Página 404 - No encontrada."""
    return render_template("errors/404.html"), 404


@error_bp.app_errorhandler(500)
def internal_error(error):  # noqa: D401, ARG001
    """Página 500 - Error interno."""
    return render_template("errors/500.html"), 500


@error_bp.app_errorhandler(403)
def forbidden(error):  # noqa: D401, ARG001
    """Página 403 - Acceso prohibido."""
    return render_template("errors/403.html"), 403


@error_bp.app_errorhandler(401)
def unauthorized(error):  # noqa: D401, ARG001
    """Página 401 - No autorizado (redirige a login)."""
    return redirect(url_for("login.login"))


@error_bp.app_errorhandler(400)
def bad_request(error):  # noqa: D401, ARG001
    """Página 400 - Solicitud incorrecta."""
    return render_template("errors/400.html"), 400








