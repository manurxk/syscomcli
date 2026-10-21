from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

facturamod = Blueprint('factura', __name__, template_folder='templates')


@facturamod.route('/factura-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
@permiso_requerido("VENTAS", "LEER")
def facturaIndex():
    """Página principal de factura (listado y acciones)."""
    return render_template('factura-index.html')


@facturamod.route('/factura-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
@permiso_requerido("VENTAS", "CREAR")
def facturaAgregar():
    """Página del formulario para registrar factura."""
    return render_template('factura-agregar.html')
