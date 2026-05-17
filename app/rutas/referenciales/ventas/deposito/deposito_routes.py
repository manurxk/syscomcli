from flask import Blueprint, render_template

deposito_mod = Blueprint('deposito', __name__, template_folder='templates')

@deposito_mod.route('/deposito-index')
def depositoIndex():
    return render_template('deposito-index.html')


















