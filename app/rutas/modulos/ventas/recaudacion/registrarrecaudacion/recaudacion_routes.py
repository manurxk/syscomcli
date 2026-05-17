from flask import Blueprint, render_template

recaudacion_mod = Blueprint('recaudacion', __name__, template_folder='templates')

@recaudacion_mod.route('/recaudacion-index')
def recaudacionIndex():
    """Página principal de gestión de recaudaciones"""
    return render_template('registrar-recaudacion-index.html')

@recaudacion_mod.route('/recaudacion-agregar')
def recaudacionAgregar():
    """Página para agregar nueva recaudación"""
    return render_template('registrar-recaudacion-agregar.html')


















