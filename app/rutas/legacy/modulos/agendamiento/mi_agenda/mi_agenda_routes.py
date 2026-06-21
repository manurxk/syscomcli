from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

miagendamod = Blueprint('miagenda', __name__, template_folder='templates')


@miagendamod.route('/mi-agenda')
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def miAgendaIndex():
    """Página Mi Agenda — citas del día del especialista logueado."""
    return render_template('mi-agenda.html')
