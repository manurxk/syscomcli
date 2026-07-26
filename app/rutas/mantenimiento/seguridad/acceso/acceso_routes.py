from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

accesomod = Blueprint('acceso', __name__, template_folder='templates')


@accesomod.route('/acceso-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def accesoIndex():
    return render_template('acceso-index.html')
