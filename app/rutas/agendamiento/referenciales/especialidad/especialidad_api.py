from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.especialidad.EspecialidadDao import EspecialidadDao
from app.auth.utils.decorators import role_required

especialidadapi = Blueprint('especialidadapi', __name__)


@especialidadapi.route('/especialidades', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEspecialidades():
    try:
        data = EspecialidadDao().getEspecialidades()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialidades: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@especialidadapi.route('/especialidades/<int:especialidad_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEspecialidad(especialidad_id):
    try:
        especialidad = EspecialidadDao().getEspecialidadById(especialidad_id)
        if not especialidad:
            return jsonify({'success': False, 'error': 'No se encontró la especialidad con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': especialidad, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@especialidadapi.route('/especialidades', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEspecialidad():
    data = request.get_json() or {}
    especialidaddao = EspecialidadDao()

    descripcion = (data.get('des_especialidad') or '').strip().upper()
    estado = bool(data.get('est_especialidad', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not especialidaddao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números y espacios.'}), 400
    if especialidaddao.especialidadExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una especialidad "{descripcion}".'}), 400

    try:
        especialidad_id = especialidaddao.guardarEspecialidad(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_especialidad': especialidad_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@especialidadapi.route('/especialidades/<int:especialidad_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEspecialidad(especialidad_id):
    data = request.get_json() or {}
    especialidaddao = EspecialidadDao()

    if not especialidaddao.getEspecialidadById(especialidad_id):
        return jsonify({'success': False, 'error': 'No se encontró la especialidad con el ID proporcionado.'}), 404

    descripcion = (data.get('des_especialidad') or '').strip().upper()
    estado = bool(data.get('est_especialidad', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not especialidaddao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números y espacios.'}), 400
    if especialidaddao.especialidadExiste(descripcion, excluir_id=especialidad_id):
        return jsonify({'success': False, 'error': f'Ya existe una especialidad "{descripcion}".'}), 400

    try:
        especialidaddao.updateEspecialidad(especialidad_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_especialidad': especialidad_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@especialidadapi.route('/especialidades/<int:especialidad_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarEspecialidad(especialidad_id):
    especialidaddao = EspecialidadDao()

    if not especialidaddao.getEspecialidadById(especialidad_id):
        return jsonify({'success': False, 'error': 'No se encontró la especialidad con el ID proporcionado.'}), 404

    try:
        especialidaddao.desactivarEspecialidad(especialidad_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Especialidad {especialidad_id} desactivada correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
