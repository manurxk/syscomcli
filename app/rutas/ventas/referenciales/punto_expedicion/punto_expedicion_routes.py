from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

puntoexpedicionmod = Blueprint('punto_expedicion', __name__, template_folder='templates')


@puntoexpedicionmod.route('/punto-expedicion-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def puntoExpedicionIndex():
    return render_template('punto-expedicion-index.html')
