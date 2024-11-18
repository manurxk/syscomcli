from flask import Blueprint, render_template

consumod = Blueprint('consulta', __name__, template_folder='templates')

@consumod.route('/consulta-index')
def consultaIndex():
    return render_template('consulta-index.html')