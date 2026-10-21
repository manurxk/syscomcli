from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

usuariomod = Blueprint('usuario', __name__, template_folder='templates')

@usuariomod.route('/usuario-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def usuarioIndex():
    """Página principal de usuarios."""
    return render_template('usuario-index.html')

@usuariomod.route('/usuario-detalle/<int:id_usuario>')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def usuarioDetalle(id_usuario):
    """Ventana de detalle: datos de identidad/bloqueo + historial de
    accesos, MFA, dispositivos confiables y recuperaciones de contraseña."""
    return render_template('usuario-detalle.html', id_usuario=id_usuario)

@usuariomod.route('/usuario-agregar')
@usuariomod.route('/usuario-editar/<int:id_usuario>')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def usuarioAgregar(id_usuario=None):
    """Página para agregar o editar usuario (formulario completo sin modales)"""
    return render_template('usuario-agregar.html', id_usuario=id_usuario)
