from flask import Blueprint, render_template

pacientemod = Blueprint('paciente', __name__, template_folder='templates')

@pacientemod.route('/paciente-index')
def pacienteIndex():
    return render_template('paciente-index.html')

@pacientemod.route('/paciente-agregar')
def pacienteAgregar():
    """Página para agregar nuevo paciente (formulario completo sin modales)"""
    return render_template('paciente-agregar.html')

@pacientemod.route('/mis-pacientes')
def misPacientes():
    """Vista de Mis Pacientes para especialistas - Solo muestra pacientes asignados"""
    return render_template('paciente-mis-pacientes.html')