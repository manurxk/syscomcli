from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

funcionariomod = Blueprint('funcionario', __name__, template_folder='templates')

@funcionariomod.route('/funcionario-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def funcionarioIndex():
    return render_template('funcionario-index.html')

@funcionariomod.route('/funcionario-agregar')
@funcionariomod.route('/funcionario-editar/<int:id_funcionario>')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def funcionarioAgregar(id_funcionario=None):
    """Página para agregar o editar funcionario (formulario completo sin modales)"""
    return render_template('funcionario-agregar.html', id_funcionario=id_funcionario)