from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.turno.TurnoDao import TurnoDao

turapi = Blueprint('turapi', __name__)

# Obtener todos los turnos
@turapi.route('/turnos', methods=['GET'])
def getTurnos():
    turdao = TurnoDao()

    try:
        turnos = turdao.getTurno()

        return jsonify({
            'success': True,
            'data': turnos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los turnos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtener un turno por ID
@turapi.route('/turnos/<int:id_turno>', methods=['GET'])
def getTurno(id_turno):
    turdao = TurnoDao()

    try:
        turno = turdao.getTurnoById(id_turno)

        if turno:
            return jsonify({
                'success': True,
                'data': turno,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agregar un nuevo turno
@turapi.route('/turnos', methods=['POST'])
def addTurno():
    data = request.get_json()
    turdao = TurnoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        id_turno = turdao.guardarTurno(descripcion)
        if id_turno is not None:
            return jsonify({
                'success': True,
                'data': {'id_turno': id_turno, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el turno. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un turno por ID
@turapi.route('/turnos/<int:id_turno>', methods=['PUT'])
def updateTurno(id_turno):
    data = request.get_json()
    turdao = TurnoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    descripcion = data['descripcion']
    try:
        if turdao.updateTurno(id_turno, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id_turno': id_turno, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un turno por ID
@turapi.route('/turnos/<int:id_turno>', methods=['DELETE'])
def deleteTurno(id_turno):
    turdao = TurnoDao()

    try:
        if turdao.deleteTurno(id_turno):
            return jsonify({
                'success': True,
                'mensaje': f'Turno con ID {id_turno} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el turno con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar turno: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500