from flask import Blueprint, render_template, request

consultamod = Blueprint('registrarconsulta', __name__, template_folder='templates')

@consultamod.route('/consulta-index')
def consultaIndex():
    return render_template('registrarconsulta-index.html')

@consultamod.route('/consulta-agregar')
def consultaAgregar():
    id_consulta = request.args.get('id', type=int)
    id_cita = request.args.get('id_cita', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    id_profesional = request.args.get('id_profesional', type=int)
    return render_template(
        'registrarconsulta-agregar.html',
        id_consulta=id_consulta,
        id_cita=id_cita,
        id_paciente=id_paciente,
        id_profesional=id_profesional
    )