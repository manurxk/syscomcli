from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

monedamod = Blueprint('moneda', __name__, template_folder='templates')


@monedamod.route('/moneda-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def monedaIndex():
    return render_template('moneda-index.html')
