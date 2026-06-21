from flask import Blueprint, render_template

establecimientomod = Blueprint('establecimiento', __name__, template_folder='templates')

@establecimientomod.route('/establecimiento-index')
def establecimientoIndex():
    return render_template('establecimiento-index.html')

@establecimientomod.route('/establecimiento-agregar')
def establecimientoAgregar():
    """Página para agregar nuevo establecimiento (formulario completo sin modales)"""
    return render_template('establecimiento-agregar.html')

