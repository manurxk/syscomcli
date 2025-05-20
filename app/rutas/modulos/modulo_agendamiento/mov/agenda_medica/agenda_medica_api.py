from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.agenda_medica.Agenda_medicaDao import Agenda_medicaDao

agenda_medica_api = Blueprint('agenda_medica_api', __name__)

# Trae todas las agendas médicas
@agenda_medica_api.route('/agenda_medicas', methods=['GET'])
def getAgenda_medicas():
    agendamedicadao = Agenda_medicaDao()

    try:
        agenda_medicas = agendamedicadao.getAgenda_medicas()

        return jsonify({
            'success': True,
            'data': agenda_medicas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las agendas médicas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae una agenda médica por ID
@agenda_medica_api.route('/agenda_medicas/<int:agenda_medica_id>', methods=['GET'])
def getAgenda_medica(agenda_medica_id):
    agendamedicadao = Agenda_medicaDao()

    try:
        agenda_medica = agendamedicadao.getAgenda_medicaById(agenda_medica_id)

        if agenda_medica:
            return jsonify({
                'success': True,
                'data': agenda_medica,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda médica con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener agenda médica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva agenda médica
@agenda_medica_api.route('/agenda_medicas', methods=['POST'])
def addAgenda_medica():
    data = request.get_json()
    agendamedicadao = Agenda_medicaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['id_medico','id_especialidad','id_dia','id_turno','id_sala_atencion','id_estado_laboral']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        #print("hola")
        id_medico = data['id_medico']
        id_especialidad = data['id_especialidad']
        id_dia = data['id_dia']
        id_turno = data['id_turno']
        id_sala_atencion = data['id_sala_atencion']
        id_estado_laboral = data['id_estado_laboral']

        agenda_medica_id = agendamedicadao.guardarAgenda_medica(id_medico, id_especialidad, id_dia, id_turno, id_sala_atencion, id_estado_laboral)
        if agenda_medica_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_agenda_medica': agenda_medica_id, 'id_medico': id_medico, 'id_especialidad': id_especialidad, 'id_dia': id_dia, 'id_turno': id_turno, 'id_sala_atencion': id_sala_atencion, 'id_estado_laboral': id_estado_laboral},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la agenda médica. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar agenda médica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una agenda médica
@agenda_medica_api.route('/agenda_medicas/<int:agenda_medica_id>', methods=['PUT'])
def updateAgenda_medica(agenda_medica_id):
    data = request.get_json()
    agendamedicadao = Agenda_medicaDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['id_medico','id_especialidad','id_dia','id_turno','id_sala_atencion','id_estado_laboral']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

        id_medico = data['id_medico']
        id_especialidad = data['id_especialidad']
        id_dia = data['id_dia']
        id_turno = data['id_turno']
        id_sala_atencion = data['id_sala_atencion']
        id_estado_laboral = data['id_estado_laboral']
    try:
        if agendamedicadao.updateAgenda_medica(agenda_medica_id, id_medico, id_especialidad, id_dia, id_turno, id_sala_atencion, id_estado_laboral):
            return jsonify({
                'success': True,
                'data': {'id_agenda_medica': agenda_medica_id, 'id_medico': id_medico, 'id_especialidad': id_especialidad, 'id_dia': id_dia, 'id_turno': id_turno, 'id_sala_atencion': id_sala_atencion, 'id_estado_laboral': id_estado_laboral},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda médica con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar agenda médica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una agenda médica
@agenda_medica_api.route('/agenda_medicas/<int:agenda_medica_id>', methods=['DELETE'])
def deleteAgenda_medica(agenda_medica_id):
    agendamedicadao = Agenda_medicaDao()

    try:
        # Usar el retorno de eliminarAgenda_medica para determinar el éxito
        if agendamedicadao.deleteAgenda_medica(agenda_medica_id):
            return jsonify({
                'success': True,
                'mensaje': f'Agenda médica con ID {agenda_medica_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda médica con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar agenda médica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
