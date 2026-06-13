from flask import Blueprint, render_template, request

diagnosticomod = Blueprint('registrar_diagnostico', __name__, template_folder='templates')

@diagnosticomod.route('/index')
def diagnosticoIndex():
    return render_template('registrar-diagnostico-index.html')

@diagnosticomod.route('/agregar')
@diagnosticomod.route('/agregar/<int:id_consulta>')
def diagnosticoAgregar(id_consulta=None):
    if not id_consulta:
        id_consulta = request.args.get('id_consulta', type=int)
    embedded = request.args.get('embedded', '0') == '1'
    id_paciente = request.args.get('id_paciente', type=int)
    return render_template(
        'registrar-diagnostico-agregar.html', 
        id_consulta=id_consulta,
        embedded=embedded,
        id_paciente=id_paciente
    )