from flask import Blueprint, render_template

facturamod = Blueprint('factura', __name__, template_folder='templates')

@facturamod.route('/factura-index')
def facturaIndex():
    """Página principal de gestión de facturas"""
    return render_template('registrar-factura-index.html')

@facturamod.route('/factura-agregar')
def facturaAgregar():
    """Página para agregar nueva factura (formulario completo sin modales)"""
    return render_template('registrar-factura-agregar.html')

