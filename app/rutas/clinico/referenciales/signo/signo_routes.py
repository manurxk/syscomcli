from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

signomod = Blueprint('signo', __name__, template_folder='templates')


@signomod.route('/signo-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def signoIndex():
    return render_template('signo-index.html')
