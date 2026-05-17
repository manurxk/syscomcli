from flask import Blueprint, render_template

fichamedmod = Blueprint('fichamedica', __name__, template_folder='templates')

@fichamedmod.route('/ficha-medica-index')
def fichaMedicaIndex():
    return render_template('ficha-index.html')