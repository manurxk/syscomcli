from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

condicionventamod = Blueprint('condicion_venta', __name__, template_folder='templates')


@condicionventamod.route('/condicion-venta-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def condicionVentaIndex():
    """Página principal de condición de venta (listado y acciones)."""
    return render_template('condicion-venta-index.html')
