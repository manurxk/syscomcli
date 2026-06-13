from flask import redirect, request, session, url_for, jsonify

def init_middleware(app):
    """Initialize common middleware for the application."""
    
    @app.before_request
    def require_login():
        """
        Authentication middleware (FASE 2)
        Uses improved session verification if available.
        """
        # Improved session verification
        try:
            from app.auth.middleware.auth_middleware import verificar_sesion_mejorada
            resultado = verificar_sesion_mejorada()
            if resultado:
                return resultado
        except Exception as e:
            app.logger.warning(f"Error in improved middleware, using traditional method: {str(e)}")
            
            # Public endpoints
            public_endpoints = {
                "login.login", 
                "login.logout", 
                "static",
                "informacion.privacidad",
                "informacion.soporte",
                "informacion.contacto",
                "auth.login",
                "auth.solicitar_recuperacion",
                "auth.confirmar_recuperacion"
            }

            if request.endpoint in public_endpoints or request.endpoint is None:
                return None

            # Allow static files even if endpoint is None
            if request.path.startswith("/static"):
                return None

            if "usu_nick" not in session:
                if request.path.startswith('/api/'):
                    return jsonify({
                        'success': False,
                        'error': 'No autenticado'
                    }), 401
                else:
                    return redirect(url_for("login.login"))
