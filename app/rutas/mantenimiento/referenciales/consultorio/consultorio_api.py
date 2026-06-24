from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.consultorio.ConsultorioDao import ConsultorioDao
from app.auth.utils.decorators import role_required

consultorioapi = Blueprint('consultorioapi', __name__)


@consultorioapi.route('/consultorios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getConsultorios():
    try:
        data = ConsultorioDao().getConsultorios()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultorios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultorioapi.route('/consultorios/<int:consultorio_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getConsultorio(consultorio_id):
    try:
        consultorio = ConsultorioDao().getConsultorioById(consultorio_id)
        if not consultorio:
            return jsonify({'success': False, 'error': 'No se encontró el consultorio con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': consultorio, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultorio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultorioapi.route('/consultorios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addConsultorio():
    data = request.get_json() or {}
    consultoriodao = ConsultorioDao()

    id_sede = data.get('id_sede') or None
    descripcion = (data.get('des_consultorio') or '').strip().upper()
    estado = bool(data.get('est_consultorio', True))

    if not id_sede:
        return jsonify({'success': False, 'error': 'La sede es obligatoria.'}), 400
    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if consultoriodao.descripcionExiste(id_sede, descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un consultorio "{descripcion}" en esa sede.'}), 400

    try:
        consultorio_id = consultoriodao.guardarConsultorio(
            id_sede, descripcion, estado=estado, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_consultorio': consultorio_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar consultorio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultorioapi.route('/consultorios/<int:consultorio_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateConsultorio(consultorio_id):
    data = request.get_json() or {}
    consultoriodao = ConsultorioDao()

    actual = consultoriodao.getConsultorioById(consultorio_id)
    if not actual:
        return jsonify({'success': False, 'error': 'No se encontró el consultorio con el ID proporcionado.'}), 404

    id_sede = data.get('id_sede') or None
    descripcion = (data.get('des_consultorio') or '').strip().upper()
    estado = bool(data.get('est_consultorio', True))

    if not id_sede:
        return jsonify({'success': False, 'error': 'La sede es obligatoria.'}), 400
    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if consultoriodao.descripcionExiste(id_sede, descripcion, excluir_id=consultorio_id):
        return jsonify({'success': False, 'error': f'Ya existe un consultorio "{descripcion}" en esa sede.'}), 400

    try:
        consultoriodao.updateConsultorio(
            consultorio_id, id_sede, descripcion, estado=estado, usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_consultorio': consultorio_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar consultorio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@consultorioapi.route('/consultorios/<int:consultorio_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarConsultorio(consultorio_id):
    consultoriodao = ConsultorioDao()

    if not consultoriodao.getConsultorioById(consultorio_id):
        return jsonify({'success': False, 'error': 'No se encontró el consultorio con el ID proporcionado.'}), 404

    try:
        consultoriodao.desactivarConsultorio(consultorio_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Consultorio {consultorio_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar consultorio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
