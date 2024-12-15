from flask import Blueprint, render_template

medimod = Blueprint('medico', __name__, template_folder='templates')

@medimod.route('/medico-index')
def medicoIndex():
    return render_template('medico_index.html')