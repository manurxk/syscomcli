from flask import Blueprint, render_template

# Definir el Blueprint para las salas de atención
salmod = Blueprint('sala_atencion', __name__, template_folder='templates')

# Ruta para la vista principal de las salas de atención
@salmod.route('/sala_atencion-index')
def sala_atencionIndex():
    return render_template('sala_atencion-index.html')
