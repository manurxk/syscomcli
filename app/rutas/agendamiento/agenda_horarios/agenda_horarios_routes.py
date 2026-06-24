from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

agendahorariosmod = Blueprint('agenda_horarios', __name__, template_folder='templates')


@agendahorariosmod.route('/agenda-horarios-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def agendaHorariosIndex():
    return render_template('agenda_horarios-index.html')
