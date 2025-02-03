from flask import Blueprint, render_template

pacmod = Blueprint('paciente', __name__, template_folder='templates')

@pacmod.route('/paciente-index')
def pacienteIndex():
    return render_template('paciente-index.html')