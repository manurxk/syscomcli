from flask import Blueprint, render_template

nota_credito_mod = Blueprint('nota_credito', __name__, template_folder='templates')

@nota_credito_mod.route('/nota-credito-index')
def notaCreditoIndex():
    """Página principal de gestión de notas de crédito"""
    return render_template('registrar-nota-credito-index.html')

@nota_credito_mod.route('/nota-credito-agregar')
def notaCreditoAgregar():
    """Página para agregar nueva nota de crédito"""
    return render_template('registrar-nota-credito-agregar.html')


















