from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

pacientemod = Blueprint('paciente', __name__, template_folder='templates')

@pacientemod.route('/paciente-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def pacienteIndex():
    return render_template('paciente-index.html')

@pacientemod.route('/paciente-agregar')
@pacientemod.route('/paciente-editar/<int:id_paciente>')
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def pacienteAgregar(id_paciente=None):
    """Página para agregar o editar paciente (formulario completo)"""
    return render_template('paciente-agregar.html', id_paciente=id_paciente)
