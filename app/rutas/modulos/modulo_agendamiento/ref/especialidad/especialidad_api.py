from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.especialidad.EspecialidadDao import EspecialidadDao

espapi = Blueprint('espapi', __name__)

# Trae todas las especialidades
@espapi.route('/especialidades', methods=['GET'])
def getEspecialidades():
    espdao = EspecialidadDao()

    try:
        especialidades = espdao.getEspecialidades()

        return jsonify({
            'success': True,
            'data': especialidades,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las especialidades: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@espapi.route('/especialidades/<int:especialidad_id>', methods=['GET'])
def getEspecialidad(especialidad_id):
    espdao = EspecialidadDao()

    try:
        especialidad = espdao.getEspecialidadById(especialidad_id)

        if especialidad:
            return jsonify({
                'success': True,
                'data': especialidad,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la especialidad con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener especialidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva especialidad
@espapi.route('/especialidades', methods=['POST'])
def addEspecialidad():
    data = request.get_json()
    espdao = EspecialidadDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400

    try:
        descripcion = data['descripcion'].upper()
        especialidad_id = espdao.guardarEspecialidad(descripcion)
        if especialidad_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': especialidad_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar la especialidad. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar especialidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@espapi.route('/especialidades/<int:especialidad_id>', methods=['PUT'])
def updateEspecialidad(especialidad_id):
    data = request.get_json()
    espdao = EspecialidadDao()

    campos_requeridos = ['descripcion']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                            'success': False,
                            'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
                            }), 400
    descripcion = data['descripcion']
    try:
        if espdao.updateEspecialidad(especialidad_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': especialidad_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la especialidad con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar especialidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@espapi.route('/especialidades/<int:especialidad_id>', methods=['DELETE'])
def deleteEspecialidad(especialidad_id):
    espdao = EspecialidadDao()

    try:
        if espdao.deleteEspecialidad(especialidad_id):
            return jsonify({
                'success': True,
                'mensaje': f'Especialidad con ID {especialidad_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la especialidad con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar especialidad: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500