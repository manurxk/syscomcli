from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

citamod = Blueprint('cita', __name__, template_folder='templates')

@citamod.route('/cita-index')
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def citaIndex():
    return render_template('cita-index.html')

# Nueva ruta para el calendario
@citamod.route('/calendario')
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def calendario():
    return render_template('calendario-index.html')

# Nueva ruta para registrar nueva cita
@citamod.route('/cita-agregar')
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def citaAgregar():
    """Página para agregar nueva cita (formulario completo sin modales)"""
    return render_template('cita-agregar.html')