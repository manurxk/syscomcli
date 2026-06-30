from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

entidademisoramod = Blueprint('entidad_emisora', __name__, template_folder='templates')


@entidademisoramod.route('/entidad-emisora-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def entidadEmisoraIndex():
    return render_template('entidad-emisora-index.html')
