from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

timbradomod = Blueprint('timbrado', __name__, template_folder='templates')


@timbradomod.route('/timbrado-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def timbradoIndex():
    return render_template('timbrado-index.html')
