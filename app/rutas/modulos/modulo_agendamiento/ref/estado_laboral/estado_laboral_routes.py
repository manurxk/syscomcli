from flask import Blueprint, render_template

estado_laboralmod = Blueprint('estado_laboral', __name__, template_folder='templates')

@estado_laboralmod.route('/estado_laboral-index')
def estado_laboralIndex():
    return render_template('estado_laboral-index.html')
