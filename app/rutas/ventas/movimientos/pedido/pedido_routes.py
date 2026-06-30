from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

pedidomod = Blueprint('pedido', __name__, template_folder='templates')


@pedidomod.route('/pedido-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def pedidoIndex():
    return render_template('pedido-index.html')


@pedidomod.route('/pedido-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def pedidoAgregar():
    return render_template('pedido-agregar.html')
