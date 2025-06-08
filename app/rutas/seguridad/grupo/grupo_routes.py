from flask import Blueprint, render_template

grumod = Blueprint('grupo', __name__, template_folder='templates')

@grumod.route('/grupo-index')
def grupoIndex():
    return render_template('grupo-index.html')