from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

pedidomod = Blueprint('pedido', __name__, template_folder='templates')


@pedidomod.route('/pedido-index')
@role_required("ADMINISTRADOR", "VENTAS")
@permiso_requerido("VENTAS", "LEER")
def pedidoIndex():
    """Página principal de pedido (listado y acciones)."""
    return render_template('pedido-index.html')


@pedidomod.route('/pedido-agregar')
@role_required("ADMINISTRADOR", "VENTAS")
@permiso_requerido("VENTAS", "CREAR")
def pedidoAgregar():
    """Página del formulario para registrar pedido."""
    return render_template('pedido-agregar.html')
