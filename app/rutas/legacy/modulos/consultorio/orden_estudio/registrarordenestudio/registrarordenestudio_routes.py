from flask import Blueprint, render_template, request

ordenestudiomod = Blueprint('registrarordenestudio', __name__, template_folder='templates')

@ordenestudiomod.route('/orden-estudio-index')
def ordenEstudioIndex():
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarordenestudio-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )

@ordenestudiomod.route('/orden-estudio-agregar')
def ordenEstudioAgregar():
    embedded = request.args.get('embedded', '0') == '1'
    id_orden_estudio = request.args.get('id', type=int)
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrarordenestudio-agregar.html',
        embedded=embedded,
        id_orden_estudio=id_orden_estudio,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )
