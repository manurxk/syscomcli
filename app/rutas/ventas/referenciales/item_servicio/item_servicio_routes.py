from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

itemserviciomod = Blueprint('item_servicio', __name__, template_folder='templates')


@itemserviciomod.route('/item-servicio-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def itemServicioIndex():
    return render_template('item-servicio-index.html')
