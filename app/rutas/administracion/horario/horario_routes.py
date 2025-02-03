# agenda_routes.py
from flask import Blueprint, render_template
from app.dao.agenda.horario.HorarioDao import HorarioDao

# Asegúrate de que 'agenda' sea el nombre del Blueprint y que coincida con la ruta
hormod = Blueprint('horario', __name__, template_folder='templates')

@hormod.route('/horario-index')  # Ruta de la agenda
def horarioIndex():
    horariodao = HorarioDao()
    return render_template('horario-index.html')

