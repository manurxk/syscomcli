from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

especialidadmod = Blueprint('especialidad', __name__, template_folder='templates')


@especialidadmod.route('/especialidad-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def especialidadIndex():
    return render_template('especialidad-index.html')
