from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

citamod = Blueprint('cita', __name__, template_folder='templates')


@citamod.route('/citas-index')
@role_required("ADMINISTRADOR", "RECEPCION")
def citaIndex():
    """Página principal de citas (calendario y listado)."""
    return render_template('cita-index.html')


@citamod.route('/citas-agregar')
@role_required("ADMINISTRADOR", "RECEPCION")
def citaAgregar():
    """Página del formulario para agendar una cita."""
    return render_template('cita-agregar.html')
