from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.cita.CitaDao import CitaDao

cita_api = Blueprint('cita_api', __name__)

# Trae todas las citas
@cita_api.route('/citas', methods=['GET'])
def getCitas():
    citadao = CitaDao()

    try:
        citas = citadao.getCitas()

        return jsonify({
            'success': True,
            'data': citas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las citas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae una cita por ID
@cita_api.route('/citas/<int:cita_id>', methods=['GET'])
def getCita(cita_id):
    citadao = CitaDao()

    try:
        cita = citadao.getCitaById(cita_id)

        if cita:
            return jsonify({
                'success': True,
                'data': cita,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva cita
@cita_api.route('/citas', methods=['POST'])
def addCita():
    data = request.get_json()
    citadao = CitaDao()

    campos_requeridos = ['id_persona','id_especialidad','id_dia','id_turno','hora_inicio', 'hora_fin','id_sala_atencion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        id_persona = data['id_persona']
        id_especialidad = data['id_especialidad']
        id_dia = data['id_dia']
        id_turno = data['id_turno']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']
        id_sala_atencion = data['id_sala_atencion']

        cita_id = citadao.guardarCita(id_persona,id_especialidad,id_dia,id_turno,hora_inicio, hora_fin,id_sala_atencion)
        if cita_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_cita': cita_id, 'id_persona': id_persona, 'id_especialidad': id_especialidad, 
                        'id_dia': id_dia, 'id_turno': id_turno, 'hora_inicio': hora_inicio, 
                        'hora_fin': hora_fin,'id_sala_atencion': id_sala_atencion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la cita. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una cita
@cita_api.route('/citas/<int:cita_id>', methods=['PUT'])
def updateCita(cita_id):
    data = request.get_json()
    citadao = CitaDao()

    campos_requeridos = ['id_persona','id_especialidad','id_dia','id_turno','hora_inicio', 'hora_fin','id_sala_atencion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

        id_persona = data['id_persona']
        id_especialidad = data['id_especialidad']
        id_dia = data['id_dia']
        id_turno = data['id_turno']
        hora_inicio = data['hora_inicio']
        hora_fin = data['hora_fin']
        id_sala_atencion = data['id_sala_atencion']
    try:
        if citadao.updateCita(cita_id, id_persona, id_especialidad, id_dia, id_turno, hora_inicio, hora_fin, id_sala_atencion):
            return jsonify({
                'success': True,
                'data': {'id_cita': cita_id, 'id_persona': id_persona, 'id_especialidad': id_especialidad, 
                        'id_dia': id_dia, 'id_turno': id_turno, 'hora_inicio': hora_inicio, 
                        'hora_fin': hora_fin,'id_sala_atencion': id_sala_atencion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una cita
@cita_api.route('/citas/<int:cita_id>', methods=['DELETE'])
def deleteCita(cita_id):
    citadao = CitaDao()

    try:
        if citadao.deleteCita(cita_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cita con ID {cita_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar cita: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500