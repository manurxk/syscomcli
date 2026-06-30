from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

estadofacturamod = Blueprint('estado_factura', __name__, template_folder='templates')


@estadofacturamod.route('/estado-factura-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def estadoFacturaIndex():
    return render_template('estado-factura-index.html')
