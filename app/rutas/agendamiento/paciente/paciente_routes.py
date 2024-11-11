from flask import Blueprint, render_template

paciemod = Blueprint('paciente', __name__, template_folder='templates')

@paciemod.route('/paciente-index')
def pacienteIndex():
    return render_template('paciente_index.html')