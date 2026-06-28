from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipo_procedimientomod = Blueprint('tipo_procedimiento', __name__, template_folder='templates')


@tipo_procedimientomod.route('/tipo-procedimiento-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoProcedimientoIndex():
    return render_template('tipo_procedimiento-index.html')
