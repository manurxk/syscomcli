from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

entidadadheridamod = Blueprint('entidad_adherida', __name__, template_folder='templates')


@entidadadheridamod.route('/entidad-adherida-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def entidadAdheridaIndex():
    return render_template('entidad-adherida-index.html')
