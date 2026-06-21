from flask import Blueprint, render_template

estado_factura_mod = Blueprint('estado_factura', __name__, template_folder='templates')

@estado_factura_mod.route('/estado-factura-index')
def estadoFacturaIndex():
    return render_template('estado-factura-index.html')


















