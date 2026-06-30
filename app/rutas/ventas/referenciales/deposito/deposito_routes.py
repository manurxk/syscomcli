from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

depositomod = Blueprint('deposito', __name__, template_folder='templates')


@depositomod.route('/deposito-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def depositoIndex():
    return render_template('deposito-index.html')
