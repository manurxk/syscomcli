from flask import Blueprint, render_template, request

recetamod = Blueprint('registrarreceta', __name__, template_folder='templates')

@recetamod.route('/receta-index')
def recetaIndex():
    return render_template('registrarreceta-index.html')

@recetamod.route('/receta-agregar')
def recetaAgregar():
    id_receta = request.args.get('id', type=int)
    embedded = request.args.get('embedded', '0') == '1'
    id_paciente = request.args.get('id_paciente', type=int)
    id_consulta = request.args.get('id_consulta', type=int)

    return render_template(
        'registrarreceta-agregar.html',
        id_receta=id_receta,
        embedded=embedded,
        id_paciente=id_paciente,
        id_consulta=id_consulta
    )
