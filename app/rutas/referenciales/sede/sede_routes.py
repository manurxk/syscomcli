from flask import Blueprint, render_template

sedemod = Blueprint('sede', __name__, template_folder='templates')

@sedemod.route('/sede-index')
def sedeIndex():
    return render_template('sede-index.html')

@sedemod.route('/sede-agregar')
def sedeAgregar():
    """Página para agregar nueva sede (formulario completo sin modales)"""
    return render_template('sede-agregar.html')

