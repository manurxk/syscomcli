from flask import Blueprint, render_template, request

certificadomedicomod = Blueprint('registrarcertificadomedico', __name__, template_folder='templates')

@certificadomedicomod.route('/certificado-medico-index')
def certificadoMedicoIndex():
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarcertificadomedico-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )

@certificadomedicomod.route('/certificado-medico-agregar')
def certificadoMedicoAgregar():
    embedded = request.args.get('embedded', '0') == '1'
    id_certificado = request.args.get('id', type=int)
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarcertificadomedico-agregar.html',
        embedded=embedded,
        id_certificado=id_certificado,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )
