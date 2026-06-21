from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.hora.HoraDao import HoraDao

horapi = Blueprint('horapi', __name__)

# Trae todas las ciudades
@horapi.route('/horas', methods=['GET'])
def getHoras():
    hordao = HoraDao()

    try:
        horas = hordao.getHoras()

        return jsonify({
            'success': True,
            'data': horas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los días: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horapi.route('/horas/<int:hora_id>', methods=['GET'])
def getHora(hora_id):
    hordao = HoraDao()

    try:
        hora = hordao.getHoraById(hora_id)

        if hora:
            return jsonify({
                'success': True,
                'data': hora,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el hora con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener horas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ciudad
@horapi.route('/horas', methods=['POST'])
def addHora():
    data = request.get_json()
    hordao = HoraDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        hora_id = hordao.guardarHora(descripcion)
        if hora_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': hora_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el día. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar día: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horapi.route('/horas/<int:hora_id>', methods=['PUT'])
def updateHora(hora_id):
    data = request.get_json()
    hordao = HoraDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if hordao.updateHora(hora_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id':hora_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró al hora con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar hora: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@horapi.route('/horas/<int:hora_id>', methods=['DELETE'])
def deleteHora(hora_id):
    hordao = HoraDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if hordao.deleteHora(hora_id):
            return jsonify({
                'success': True,
                'mensaje': f'dia con ID {hora_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró al hora con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar hora: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500