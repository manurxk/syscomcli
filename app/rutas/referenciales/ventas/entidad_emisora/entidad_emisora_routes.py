from flask import Blueprint, render_template

entidad_emisora_mod = Blueprint('entidad_emisora', __name__, template_folder='templates')

@entidad_emisora_mod.route('/entidad-emisora-index')
def entidadEmisoraIndex():
    return render_template('entidad-emisora-index.html')


















