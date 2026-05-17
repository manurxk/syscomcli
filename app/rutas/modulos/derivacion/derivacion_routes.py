"""
Rutas de vistas para derivaciones
"""
from flask import Blueprint, render_template

derivacionmod = Blueprint('derivacion', __name__, template_folder='templates')

@derivacionmod.route('/derivacion-index')
def derivacionIndex():
    """Vista principal de gestión de derivaciones"""
    return render_template('derivacion-index.html')











