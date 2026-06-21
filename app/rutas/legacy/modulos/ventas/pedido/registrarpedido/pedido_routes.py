from flask import Blueprint, render_template

pedidomod = Blueprint('pedido', __name__, template_folder='templates')

@pedidomod.route('/pedido-index')
def pedidoIndex():
    """Página principal de gestión de pedidos"""
    return render_template('registrar-pedido-index.html')


















