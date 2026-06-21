from flask import Blueprint, render_template

libro_ventas_mod = Blueprint('libro_ventas', __name__, template_folder='templates')

@libro_ventas_mod.route('/libro-ventas-index')
def libroVentasIndex():
    """Página principal del libro de ventas"""
    return render_template('registrar-libro-ventas-index.html')


















