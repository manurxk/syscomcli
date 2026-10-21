"""Helpers de autorización por rol."""

from functools import wraps
from flask import session, redirect, url_for, abort, flash, request, jsonify

from app.auth.utils.permisos import tiene_permiso_accion


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


def permiso_requerido(modulo, accion):
    """Exige además del rol el permiso `accion` (LEER/CREAR/EDITAR/ELIMINAR) sobre `modulo` en la matriz «Permisos».

    Uso (debajo de @role_required):
        @permiso_requerido("VENTAS", "CREAR")
    """

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(*args, **kwargs):
            if not tiene_permiso_accion(modulo, accion):
                es_ajax = (request.path.startswith('/api/')
                           or request.headers.get('X-Requested-With') == 'XMLHttpRequest'
                           or request.is_json
                           or 'application/json' in request.headers.get('Accept', ''))
                if es_ajax:
                    return jsonify({
                        'success': False,
                        'error': f'No tenés permiso de {accion.lower()} en {modulo.title()}.',
                        'code': 'FORBIDDEN'
                    }), 403
                return abort(403)
            return view_func(*args, **kwargs)

        return wrapped_view

    return decorator
