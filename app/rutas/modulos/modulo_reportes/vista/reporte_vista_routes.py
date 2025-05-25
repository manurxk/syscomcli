from flask import Blueprint, render_template

bp_reporte_vista = Blueprint(
    'reporte_vista',
    __name__,
    template_folder='templates'
)

@bp_reporte_vista.route('/reporte')
def reporte_index():
    return render_template('reporte_vista-index.html')
