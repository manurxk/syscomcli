from flask import Blueprint, render_template

bp_consultorio_vista = Blueprint(
    'consultorio_vista',
    __name__,
    template_folder='templates'
)

@bp_consultorio_vista.route('/consultorio')
def consultorio_index():
    return render_template('consultorio_vista-index.html')
