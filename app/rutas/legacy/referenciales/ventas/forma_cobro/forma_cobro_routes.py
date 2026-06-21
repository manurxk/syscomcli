from flask import Blueprint, render_template

forma_cobro_mod = Blueprint('forma_cobro', __name__, template_folder='templates')

@forma_cobro_mod.route('/forma-cobro-index')
def formaCobroIndex():
    return render_template('forma-cobro-index.html')


















