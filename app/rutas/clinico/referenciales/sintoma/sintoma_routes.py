from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

sintomamod = Blueprint('sintoma', __name__, template_folder='templates')


@sintomamod.route('/sintoma-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def sintomaIndex():
    return render_template('sintoma-index.html')
