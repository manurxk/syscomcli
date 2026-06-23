from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

referencialesmod = Blueprint('referenciales', __name__, template_folder='templates')


@referencialesmod.route('/referenciales-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def referencialesIndex():
    return render_template('referenciales-index.html')
