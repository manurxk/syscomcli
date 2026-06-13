from flask import Blueprint, render_template

empresamod = Blueprint('empresa', __name__, template_folder='templates')

@empresamod.route('/empresa-index')
def empresaIndex():
    return render_template('empresa-index.html')

@empresamod.route('/empresa-agregar')
def empresaAgregar():
    """Página para agregar nueva empresa (formulario completo sin modales)"""
    return render_template('empresa-agregar.html')

