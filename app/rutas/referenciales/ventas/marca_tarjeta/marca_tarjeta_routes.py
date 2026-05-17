from flask import Blueprint, render_template

marca_tarjeta_mod = Blueprint('marca_tarjeta', __name__, template_folder='templates')

@marca_tarjeta_mod.route('/marca-tarjeta-index')
def marcaTarjetaIndex():
    return render_template('marca-tarjeta-index.html')


















