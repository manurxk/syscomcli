from flask import Blueprint, render_template

bp_ventas_vista = Blueprint(
    'ventas_vista',
    __name__,
    template_folder='templates'
)

@bp_ventas_vista.route('/ventas')
def ventas_index():
    return render_template('ventas_vista-index.html')
