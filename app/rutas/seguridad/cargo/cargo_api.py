from flask import Blueprint, request, jsonify, current_app as app
from app.dao.seguridad.cargo.CargoDao import CargoDao  # Asegúrate que esta ruta es correcta

cargoapi = Blueprint('cargoapi', __name__)

# Trae todos los cargos
@cargoapi.route('/cargos', methods=['GET'])
def getCargos():
    cargodao = CargoDao()
    try:
        cargos = cargodao.getCargos()
        return jsonify({
            'success': True,
            'data': cargos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los cargos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un cargo por ID
@cargoapi.route('/cargos/<int:cargo_id>', methods=['GET'])
def getCargo(cargo_id):
    cargodao = CargoDao()
    try:
        cargo = cargodao.getCargoById(cargo_id)
        if cargo:
            return jsonify({
                'success': True,
                'data': cargo,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo cargo
@cargoapi.route('/cargos', methods=['POST'])
def addCargo():
    data = request.get_json()
    cargodao = CargoDao()

    # Validar que el JSON no esté vacío y tenga la propiedad necesaria
    if not data or 'car_des' not in data or not data['car_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo car_des es obligatorio y no puede estar vacío.'
        }), 400

    try:
        car_des = data['car_des'].strip()
        cargo_id = cargodao.guardarCargo(car_des)
        if cargo_id:
            return jsonify({
                'success': True,
                'data': {'car_id': cargo_id, 'car_des': car_des},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el cargo. Consulte con el administrador.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un cargo
@cargoapi.route('/cargos/<int:cargo_id>', methods=['PUT'])
def updateCargo(cargo_id):
    data = request.get_json()
    cargodao = CargoDao()

    if not data or 'car_des' not in data or not data['car_des'].strip():
        return jsonify({
            'success': False,
            'error': 'El campo car_des es obligatorio y no puede estar vacío.'
        }), 400

    car_des = data['car_des'].strip()

    try:
        if cargodao.updateCargo(cargo_id, car_des):
            return jsonify({
                'success': True,
                'data': {'car_id': cargo_id, 'car_des': car_des},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un cargo
@cargoapi.route('/cargos/<int:cargo_id>', methods=['DELETE'])
def deleteCargo(cargo_id):
    cargodao = CargoDao()
    try:
        if cargodao.deleteCargo(cargo_id):
            return jsonify({
                'success': True,
                'mensaje': f'Cargo con ID {cargo_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el cargo con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar cargo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
