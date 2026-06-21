from flask import Blueprint, render_template

arqueo_caja_mod = Blueprint('arqueo_caja', __name__, template_folder='templates')

@arqueo_caja_mod.route('/arqueo-caja-index')
def arqueoCajaIndex():
    """Página principal de gestión de arqueos de caja"""
    return render_template('registrar-arqueo-caja-index.html')

@arqueo_caja_mod.route('/arqueo-caja-agregar')
def arqueoCajaAgregar():
    """Página para agregar nuevo arqueo de caja"""
    return render_template('registrar-arqueo-caja-agregar.html')


















