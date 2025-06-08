from flask import Blueprint, render_template, session, redirect, url_for

usumod = Blueprint('usuario', __name__, template_folder='templates')

def rol_requerido(roles_permitidos):
    def decorator(f):
        def wrapper(*args, **kwargs):
            rol = session.get('rol')
            if rol not in roles_permitidos:
                return "No tienes permiso para acceder a esta página", 403
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__  # para evitar problemas con flask
        return wrapper
    return decorator

@usumod.route('/usuario-index')
@rol_requerido(['admin', 'recepcion', 'consultorio', 'ventas'])
def usuarioIndex():
    rol = session.get('rol')
    # Aquí podrías devolver distintas plantillas o datos según rol
    if rol == 'admin':
        return render_template('admin/index.html')
    elif rol == 'recepcion':
        return render_template('agendamiento_vista-index.html')
    elif rol == 'consultorio':
        return render_template('consultorio_vista-index.html')
    elif rol == 'ventas':
        return render_template('ventas_vista-index.html')
    else:
        return "Rol no reconocido", 403
