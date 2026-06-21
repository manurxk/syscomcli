from flask import Blueprint, render_template

tipo_certificado_medico_mod = Blueprint('tipo_certificado_medico', __name__, template_folder='templates')

@tipo_certificado_medico_mod.route('/tipo-certificado-medico-index')
def tipoCertificadoMedicoIndex():
    return render_template('certificado-medico-index.html')


















