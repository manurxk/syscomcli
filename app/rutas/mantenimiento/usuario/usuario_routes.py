from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

usuariomod = Blueprint('usuario', __name__, template_folder='templates')

@usuariomod.route('/usuario-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def usuarioIndex():
    return render_template('usuario-index.html')

@usuariomod.route('/usuario-agregar')
@usuariomod.route('/usuario-editar/<int:id_usuario>')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def usuarioAgregar(id_usuario=None):
    """Página para agregar o editar usuario (formulario completo sin modales)"""
    return render_template('usuario-agregar.html', id_usuario=id_usuario)
