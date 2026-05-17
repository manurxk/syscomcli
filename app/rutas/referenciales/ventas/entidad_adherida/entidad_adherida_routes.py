from flask import Blueprint, render_template

entidad_adherida_mod = Blueprint('entidad_adherida', __name__, template_folder='templates')

@entidad_adherida_mod.route('/entidad-adherida-index')
def entidadAdheridaIndex():
    return render_template('entidad-adherida-index.html')


















