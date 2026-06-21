from flask import Blueprint, render_template

feriadomod = Blueprint('feriados', __name__, template_folder='templates')

@feriadomod.route('/feriado-index')
def feriadoIndex():
    return render_template('feriado-index.html')
