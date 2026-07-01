from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

facturamod = Blueprint('factura', __name__, template_folder='templates')


@facturamod.route('/factura-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def facturaIndex():
    return render_template('factura-index.html')


@facturamod.route('/factura-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def facturaAgregar():
    return render_template('factura-agregar.html')
