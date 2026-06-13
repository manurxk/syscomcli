from flask import Blueprint, render_template, request

tratamientomod = Blueprint('registrartratamiento', __name__, template_folder='templates')

@tratamientomod.route('/tratamiento-index')
def tratamientoIndex():
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrartratamiento-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )

@tratamientomod.route('/tratamiento-agregar')
def tratamientoAgregar():
    embedded = request.args.get('embedded', '0') == '1'
    id_tratamiento = request.args.get('id', type=int)
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrartratamiento-agregar.html',
        embedded=embedded,
        id_tratamiento=id_tratamiento,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )