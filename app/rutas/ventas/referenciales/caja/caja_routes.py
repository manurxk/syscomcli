from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

cajamod = Blueprint('caja', __name__, template_folder='templates')


@cajamod.route('/caja-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def cajaIndex():
    return render_template('caja-index.html')
