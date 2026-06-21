from flask import Blueprint, render_template

nota_debito_mod = Blueprint('nota_debito', __name__, template_folder='templates')

@nota_debito_mod.route('/nota-debito-index')
def notaDebitoIndex():
    """Página principal de gestión de notas de débito"""
    return render_template('registrar-nota-debito-index.html')

@nota_debito_mod.route('/nota-debito-agregar')
def notaDebitoAgregar():
    """Página para agregar nueva nota de débito"""
    return render_template('registrar-nota-debito-agregar.html')


















