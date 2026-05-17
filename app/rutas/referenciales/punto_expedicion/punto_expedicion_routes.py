from flask import Blueprint, render_template

puntoexpedicionmod = Blueprint('puntoexpedicion', __name__, template_folder='templates')

@puntoexpedicionmod.route('/punto-expedicion-index')
def puntoExpedicionIndex():
    return render_template('punto-expedicion-index.html')

@puntoexpedicionmod.route('/punto-expedicion-agregar')
def puntoExpedicionAgregar():
    """Página para agregar nuevo punto de expedición (formulario completo sin modales)"""
    return render_template('punto-expedicion-agregar.html')

