from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

agendamod = Blueprint('agenda', __name__, template_folder='templates')

@agendamod.route('/agenda-index')
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def agendaIndex():
    return render_template('agenda_medica-index.html')