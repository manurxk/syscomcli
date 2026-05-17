from flask import Blueprint, render_template

caja_mod = Blueprint('caja', __name__, template_folder='templates')

@caja_mod.route('/caja-index')
def cajaIndex():
    return render_template('caja-index.html')


















