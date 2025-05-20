from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.genero.GeneroDao import GeneroDao

genapi = Blueprint('genapi', __name__)

# Trae todas las ciudades
@genapi.route('/generos', methods=['GET'])
def getGeneros():
    gendao = GeneroDao()

    try:
        generos = gendao.getGeneros()

        return jsonify({
            'success': True,
            'data': generos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los géneros: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@genapi.route('/generos/<int:genero_id>', methods=['GET'])
def getGenero(genero_id):
    gendao = GeneroDao()

    try:
        genero = gendao.getGeneroById(genero_id)

        if genero:
            return jsonify({
                'success': True,
                'data': genero,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el género con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener género: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva ciudad
@genapi.route('/generos', methods=['POST'])
def addGenero():
    data = request.get_json()
    gendao = GeneroDao()

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
        genero_id = gendao.guardarGenero(descripcion)
        if genero_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': genero_id, 'descripcion': descripcion},
                'error': None
            }), 201
        else:
            return jsonify({ 'success': False, 'error': 'No se pudo guardar el género. Consulte con el administrador.' }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar género: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@genapi.route('/generos/<int:genero_id>', methods=['PUT'])
def updateGenero(genero_id):
    data = request.get_json()
    gendao = GeneroDao()

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
        if gendao.updateGenero(genero_id, descripcion.upper()):
            return jsonify({
                'success': True,
                'data': {'id': genero_id, 'descripcion': descripcion},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el género con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar género: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@genapi.route('/generos/<int:genero_id>', methods=['DELETE'])
def deleteGenero(genero_id):
    gendao = GeneroDao()

    try:
        # Usar el retorno de eliminarCiudad para determinar el éxito
        if gendao.deleteGenero(genero_id):
            return jsonify({
                'success': True,
                'mensaje': f'género con ID {genero_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el género con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar género: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500