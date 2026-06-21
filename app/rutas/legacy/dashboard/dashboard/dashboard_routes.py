"""
Rutas del Dashboard principal
app/modulos/dashboard/dashboard_routes.py
"""
from flask import Blueprint, render_template, session, redirect, url_for

dashboardmod = Blueprint('dashboardmod', __name__, template_folder='templates')


def es_admin():
    """Verifica si el usuario es administrador"""
    return session.get('id_grupo') == 1


def es_recepcion():
    """Verifica si el usuario es recepcionista"""
    return session.get('id_grupo') == 2


def es_especialista():
    """Verifica si el usuario es especialista"""
    return session.get('id_grupo') == 3


def es_ventas():
    """Verifica si el usuario es del grupo Ventas"""
    return session.get('id_grupo') == 4


def obtener_nombre_usuario():
    """Obtiene el nombre del usuario de la sesión"""
    return session.get('nombre_persona', 'Usuario')


@dashboardmod.route('/')
@dashboardmod.route('/inicio')
def inicio():
    """
    Página de inicio - Dashboard dinámico según el rol del usuario
    """
    # Verificar si el usuario está logueado
    # CORREGIDO: Usar 'id_usuario' en lugar de 'id'
    if 'id_usuario' not in session:
        return redirect(url_for('login.login'))
    
    # Preparar datos del usuario para el template
    data_usuario = {
        "esAdmin": es_admin(),
        "esRecepcion": es_recepcion(),
        "esEspecialista": es_especialista(),
        "esVentas": es_ventas(),
        "grupoId": session.get('id_grupo', 0),
        "nombre": obtener_nombre_usuario()
    }
    
    return render_template('dashboard.html', data_usuario=data_usuario)


@dashboardmod.route('/referenciales')
def referenciales():
    """
    Página índice de módulos referenciales
    Solo para administradores
    """
    if not es_admin():
        return redirect(url_for('dashboardmod.inicio'))

    return render_template('referenciales-index.html')