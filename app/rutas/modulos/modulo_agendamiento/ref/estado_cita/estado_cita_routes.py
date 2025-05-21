from flask import Blueprint, render_template

estdmod = Blueprint('estado_cita', __name__, template_folder='templates')

@estdmod.route('/estado_cita-index')
def estado_citaIndex():
    return render_template('estado_cita-index.html')
