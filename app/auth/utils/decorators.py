"""Helpers de autorización por rol."""

from functools import wraps
from flask import session, redirect, url_for, abort, flash, request, jsonify


def role_required(*roles):
    """Exige que el usuario tenga alguno de los roles indicados.

    Uso:
        @role_required("ADMINISTRADOR", "RECEPCION")
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            # Detectar si es una petición AJAX/API
            # Verificar múltiples condiciones para asegurar detección correcta
            is_api_path = request.path.startswith('/api/')
            is_ajax_header = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
            is_json_content = request.is_json or request.headers.get('Content-Type', '').startswith('application/json')
            accepts_json = 'application/json' in request.headers.get('Accept', '')
            
            is_ajax = is_api_path or is_ajax_header or is_json_content or accepts_json
            
            roles_usuario = {(r or "").strip().upper() for r in session.get("roles", [])}
            if not roles_usuario:
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'error': 'Debes iniciar sesión primero',
                        'code': 'UNAUTHORIZED'
                    }), 401
                flash("Debes iniciar sesión primero", "warning")
                return redirect(url_for("login.login"))

            allowed = {r.strip().upper() for r in roles}
            if allowed and not (roles_usuario & allowed):
                if is_ajax:
                    return jsonify({
                        'success': False,
                        'error': f'Acceso denegado. Se requiere uno de los siguientes roles: {", ".join(roles)}',
                        'code': 'FORBIDDEN',
                        'required_roles': list(roles),
                        'current_roles': list(roles_usuario)
                    }), 403
                return abort(403)

            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator



