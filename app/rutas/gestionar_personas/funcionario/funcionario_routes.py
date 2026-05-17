from flask import Blueprint, render_template
from app.utils.decorators import admin_only

funcionariomod = Blueprint('funcionario', __name__, template_folder='templates')

@funcionariomod.route('/funcionario-index')
@admin_only  # Permite acceso a Administrador y Superadministrador
def funcionarioIndex():
    return render_template('funcionario-index.html')

@funcionariomod.route('/funcionario-agregar')
@funcionariomod.route('/funcionario-editar/<int:id_funcionario>')
@admin_only  # Permite acceso a Administrador y Superadministrador
def funcionarioAgregar(id_funcionario=None):
    """Página para agregar o editar funcionario (formulario completo sin modales)"""
    return render_template('funcionario-agregar.html', id_funcionario=id_funcionario)