from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipocomprobantemod = Blueprint('tipo_comprobante', __name__, template_folder='templates')


@tipocomprobantemod.route('/tipo-comprobante-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoComprobanteIndex():
    return render_template('tipo-comprobante-index.html')
