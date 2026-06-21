from flask import Blueprint, render_template, request
from app.utils.especialista_helper import obtener_id_especialista_usuario

derivacionmod = Blueprint('derivacion', __name__, template_folder='templates')

@derivacionmod.route('/derivacion-index')
def derivacionIndex():
    """Vista principal de gestión de derivaciones"""
    embedded = request.args.get('embedded', '0') == '1'
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    id_especialista = obtener_id_especialista_usuario()
    
    return render_template(
        'derivacion-index.html',
        embedded=embedded,
        id_consulta=id_consulta,
        id_paciente=id_paciente,
        id_especialista_actual=id_especialista
    )

@derivacionmod.route('/derivacion-agregar')
def derivacionAgregar():
    """Vista para agregar/editar derivaciones"""
    embedded = request.args.get('embedded', '0') == '1'
    id_derivacion = request.args.get('id', type=int)
    id_consulta = request.args.get('id_consulta', type=int)
    id_paciente = request.args.get('id_paciente', type=int)
    id_especialista = obtener_id_especialista_usuario()
    
    return render_template(
        'derivacion-agregar.html',
        embedded=embedded,
        id_derivacion=id_derivacion,
        id_consulta=id_consulta,
        id_paciente=id_paciente,
        id_especialista_actual=id_especialista
    )











