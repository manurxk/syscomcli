from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

marcatarjetamod = Blueprint('marca_tarjeta', __name__, template_folder='templates')


@marcatarjetamod.route('/marca-tarjeta-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def marcaTarjetaIndex():
    return render_template('marca-tarjeta-index.html')
