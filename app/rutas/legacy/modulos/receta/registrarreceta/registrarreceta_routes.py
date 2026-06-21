from flask import Blueprint, render_template

recetamod = Blueprint('registrarreceta', __name__, template_folder='templates')

@recetamod.route('/receta-index')
def recetaIndex():
    return render_template('registrarreceta-index.html')


















