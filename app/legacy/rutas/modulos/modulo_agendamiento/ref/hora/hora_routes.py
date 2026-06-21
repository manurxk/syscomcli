from flask import Blueprint,render_template

hormod = Blueprint('hora', __name__, template_folder='templates')

@hormod.route('/hora-index')
def horaIndex():
    return render_template('hora-index.html')