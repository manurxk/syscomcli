# agenda_routes.py
from flask import Blueprint, render_template
from app.dao.referenciales.agenda.AgendaDao import AgendaDao

# Asegúrate de que 'agenda' sea el nombre del Blueprint y que coincida con la ruta
agemod = Blueprint('agenda', __name__, template_folder='templates')

@agemod.route('/agenda-index')  # Ruta de la agenda
def agendaIndex():
    agendadao = AgendaDao()
    return render_template('agendamed-index.html', lista_agendas=agendadao.getAgendas())

