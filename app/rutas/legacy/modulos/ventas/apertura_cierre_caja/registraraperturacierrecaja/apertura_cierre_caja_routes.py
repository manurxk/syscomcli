from flask import Blueprint, render_template

apertura_cierre_caja_mod = Blueprint('apertura_cierre_caja', __name__, template_folder='templates')

@apertura_cierre_caja_mod.route('/apertura-cierre-index')
def aperturaCierreIndex():
    """Página principal de gestión de aperturas y cierres de caja"""
    return render_template('registrar-apertura-cierre-index.html')

@apertura_cierre_caja_mod.route('/apertura-cierre-agregar')
def aperturaCierreAgregar():
    """Página para agregar nueva apertura o cierre de caja"""
    return render_template('registrar-apertura-cierre-agregar.html')


















