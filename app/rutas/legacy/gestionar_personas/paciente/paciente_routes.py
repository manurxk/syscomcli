from flask import Blueprint, render_template

pacientemod = Blueprint('paciente', __name__, template_folder='templates')

@pacientemod.route('/paciente-index')
def pacienteIndex():
    return render_template('paciente-index.html')

@pacientemod.route('/paciente-agregar')
@pacientemod.route('/paciente-editar/<int:id_paciente>')
def pacienteAgregar(id_paciente=None):
    """Página para agregar o editar paciente (formulario completo)"""
    return render_template('paciente-agregar.html', id_paciente=id_paciente)

@pacientemod.route('/mis-pacientes')
def misPacientes():
    """Vista de Mis Pacientes para especialistas - Solo muestra pacientes asignados"""
    return render_template('paciente-mis-pacientes.html')