from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

miagendamod = Blueprint('mi_agenda', __name__, template_folder='templates')


@miagendamod.route('/mi-agenda')
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def miAgendaIndex():
    """Citas de hoy del especialista logueado, con acceso directo a 'Iniciar consulta'."""
    return render_template('mi-agenda.html')
