from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.cargo.CargoDao import CargoDao
from app.auth.utils.decorators import role_required

cargoapi = Blueprint('cargoapi', __name__)


@cargoapi.route('/cargos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getCargos():
    try:
        data = CargoDao().getCargos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cargos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cargoapi.route('/cargos/<int:cargo_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getCargo(cargo_id):
    try:
        cargo = CargoDao().getCargoById(cargo_id)
        if not cargo:
            return jsonify({'success': False, 'error': 'No se encontró el cargo con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': cargo, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cargo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cargoapi.route('/cargos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addCargo():
    data = request.get_json() or {}
    cargodao = CargoDao()

    descripcion = (data.get('des_cargo') or '').strip().upper()
    estado = bool(data.get('est_cargo', True))
    es_clinico = bool(data.get('es_clinico', False))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not cargodao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números y espacios.'}), 400
    if cargodao.esCargoReservado(descripcion):
        return jsonify({'success': False, 'error': f'El cargo "{descripcion}" está reservado por el sistema.'}), 400
    if cargodao.cargoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un cargo "{descripcion}".'}), 400

    try:
        cargo_id = cargodao.guardarCargo(descripcion, estado, es_clinico=es_clinico, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cargo': cargo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar cargo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cargoapi.route('/cargos/<int:cargo_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateCargo(cargo_id):
    data = request.get_json() or {}
    cargodao = CargoDao()

    if not cargodao.getCargoById(cargo_id):
        return jsonify({'success': False, 'error': 'No se encontró el cargo con el ID proporcionado.'}), 404

    descripcion = (data.get('des_cargo') or '').strip().upper()
    estado = bool(data.get('est_cargo', True))
    es_clinico = bool(data.get('es_clinico', False))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not cargodao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números y espacios.'}), 400
    if cargodao.esCargoReservado(descripcion):
        return jsonify({'success': False, 'error': f'El cargo "{descripcion}" está reservado por el sistema.'}), 400
    if cargodao.cargoExiste(descripcion, excluir_id=cargo_id):
        return jsonify({'success': False, 'error': f'Ya existe un cargo "{descripcion}".'}), 400

    try:
        cargodao.updateCargo(cargo_id, descripcion, estado, es_clinico=es_clinico, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_cargo': cargo_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar cargo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cargoapi.route('/cargos/<int:cargo_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarCargo(cargo_id):
    cargodao = CargoDao()

    if not cargodao.getCargoById(cargo_id):
        return jsonify({'success': False, 'error': 'No se encontró el cargo con el ID proporcionado.'}), 404

    try:
        cargodao.desactivarCargo(cargo_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Cargo {cargo_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar cargo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
