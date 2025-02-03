from flask import Blueprint, render_template

especimod = Blueprint('especialista', __name__, template_folder='templates')

@especimod.route('/especialista-index')
def especialistaIndex():
    return render_template('especialista_index.html')
