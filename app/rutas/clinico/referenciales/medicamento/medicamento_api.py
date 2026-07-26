from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.medicamento.MedicamentoDao import MedicamentoDao
from app.auth.utils.decorators import role_required

medicamentoapi = Blueprint('medicamentoapi', __name__)


@medicamentoapi.route('/medicamentos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getMedicamentos():
    try:
        data = MedicamentoDao().getMedicamentos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener medicamentos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@medicamentoapi.route('/medicamentos/<int:medicamento_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getMedicamento(medicamento_id):
    try:
        registro = MedicamentoDao().getMedicamentoById(medicamento_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener medicamento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@medicamentoapi.route('/medicamentos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addMedicamento():
    data = request.get_json() or {}
    dao = MedicamentoDao()

    descripcion = (data.get('des_medicamento') or '').strip().upper()
    estado = bool(data.get('est_medicamento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.medicamentoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarMedicamento(descripcion, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_medicamento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar medicamento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@medicamentoapi.route('/medicamentos/<int:medicamento_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateMedicamento(medicamento_id):
    data = request.get_json() or {}
    dao = MedicamentoDao()

    if not dao.getMedicamentoById(medicamento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_medicamento') or '').strip().upper()
    estado = bool(data.get('est_medicamento', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.medicamentoExiste(descripcion, excluir_id=medicamento_id):
        return jsonify({'success': False, 'error': f'Ya existe un registro "{descripcion}".'}), 400

    try:
        dao.updateMedicamento(medicamento_id, descripcion, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_medicamento': medicamento_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar medicamento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@medicamentoapi.route('/medicamentos/<int:medicamento_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarMedicamento(medicamento_id):
    dao = MedicamentoDao()

    if not dao.getMedicamentoById(medicamento_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarMedicamento(medicamento_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {medicamento_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar medicamento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
