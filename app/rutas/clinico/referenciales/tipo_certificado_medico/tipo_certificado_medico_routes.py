from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipo_certificado_medicomod = Blueprint('tipo_certificado_medico', __name__, template_folder='templates')


@tipo_certificado_medicomod.route('/tipo-certificado-medico-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoCertificadoMedicoIndex():
    return render_template('tipo_certificado_medico-index.html')
