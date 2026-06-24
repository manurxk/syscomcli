from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

consultoriomod = Blueprint('consultorio', __name__, template_folder='templates')


@consultoriomod.route('/consultorio-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def consultorioIndex():
    return render_template('consultorio-index.html')
