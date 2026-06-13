from flask import Blueprint, render_template, request

procedimientomod = Blueprint('registrarprocedimiento', __name__, template_folder='templates')

@procedimientomod.route('/procedimiento-index')
def procedimientoIndex():
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarprocedimiento-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )

@procedimientomod.route('/procedimiento-agregar')
def procedimientoAgregar():
    embedded = request.args.get('embedded', '0') == '1'
    id_procedimiento = request.args.get('id', type=int)
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarprocedimiento-agregar.html',
        embedded=embedded,
        id_procedimiento=id_procedimiento,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )