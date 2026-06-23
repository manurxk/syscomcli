from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

cargomod = Blueprint('cargo', __name__, template_folder='templates')


@cargomod.route('/cargo-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def cargoIndex():
    return render_template('cargo-index.html')
