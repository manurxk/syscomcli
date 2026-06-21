from flask import Blueprint, render_template, request

anamnesismod = Blueprint('anamnesis', __name__, template_folder='templates')

@anamnesismod.route('/anamnesis-index')
def anamnesisIndex():
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'anamnesis-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )

@anamnesismod.route('/anamnesis-agregar')
def anamnesisAgregar():
    id_anamnesis = request.args.get('id', type=int)
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'anamnesis-agregar.html', 
        id_anamnesis=id_anamnesis,
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente
    )