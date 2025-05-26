from flask import Blueprint, render_template
from flask import Blueprint, render_template

avisos_routes = Blueprint('avisos_routes', __name__)

@avisos_routes.route('/avisos')
def pagina_avisos():
    return render_template('aviso-index.html')
