from flask import Blueprint, render_template

moneda_mod = Blueprint('moneda', __name__, template_folder='templates')

@moneda_mod.route('/moneda-index')
def monedaIndex():
    return render_template('moneda-index.html')


















