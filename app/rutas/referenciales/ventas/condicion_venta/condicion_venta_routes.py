from flask import Blueprint, render_template

condicion_venta_mod = Blueprint('condicion_venta', __name__, template_folder='templates')

@condicion_venta_mod.route('/condicion-venta-index')
def condicionVentaIndex():
    return render_template('condicion-venta-index.html')


















