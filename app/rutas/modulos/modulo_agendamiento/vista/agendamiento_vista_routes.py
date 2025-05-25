from flask import Blueprint, render_template

bp_agendamiento_vista = Blueprint(
    'agendamiento_vista',  # nombre del blueprint
    __name__,
    template_folder='templates'  # relativa a la carpeta donde está este archivo
)

@bp_agendamiento_vista.route('/agendamiento')
def agendamiento_index():
    return render_template('agendamiento_vista-index.html')
