from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipoimpuestomod = Blueprint('tipo_impuesto', __name__, template_folder='templates')


@tipoimpuestomod.route('/tipo-impuesto-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoImpuestoIndex():
    return render_template('tipo-impuesto-index.html')
