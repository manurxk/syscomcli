from flask import Blueprint, render_template

timbradomod = Blueprint('timbrado', __name__, template_folder='templates')

@timbradomod.route('/timbrado-index')
def timbradoIndex():
    return render_template('timbrado-index.html')

@timbradomod.route('/timbrado-agregar')
def timbradoAgregar():
    """Página para agregar nuevo timbrado (formulario completo sin modales)"""
    return render_template('timbrado-agregar.html')

