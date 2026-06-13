import os
from flask import Blueprint, render_template

TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

fichamedmod = Blueprint('fichamedica', __name__, template_folder=TEMPLATES_DIR)

# ✅ SIN el prefijo 'ficha-medica' porque ya está en url_prefix
@fichamedmod.route('/index')
def fichaMedicaIndex():
    return render_template('ficha-index.html')

@fichamedmod.route('/ver/<int:id_paciente>')
def fichaMedicaVer(id_paciente):
    return render_template('ficha-ver.html', id_paciente=id_paciente)