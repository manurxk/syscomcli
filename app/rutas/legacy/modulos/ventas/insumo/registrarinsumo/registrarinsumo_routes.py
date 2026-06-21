from flask import Blueprint, render_template

insumomod = Blueprint('registrarinsumo', __name__, template_folder='templates')


@insumomod.route('/insumo-index')
def insumoIndex():
    """Página principal de gestión de insumos"""
    return render_template('registrarinsumo-index.html')


















