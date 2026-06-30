from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.diagnostico.DiagnosticoDao import DiagnosticoDao
from app.auth.utils.decorators import role_required

diagnosticoapi = Blueprint('diagnosticoapi', __name__)


@diagnosticoapi.route('/diagnosticos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getDiagnosticos():
    try:
        data = DiagnosticoDao().getDiagnosticos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener diagnósticos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@diagnosticoapi.route('/diagnosticos/<int:diagnostico_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getDiagnostico(diagnostico_id):
    try:
        registro = DiagnosticoDao().getDiagnosticoById(diagnostico_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener diagnóstico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@diagnosticoapi.route('/diagnosticos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addDiagnostico():
    data = request.get_json() or {}
    dao = DiagnosticoDao()

    descripcion = (data.get('des_diagnostico') or '').strip().upper()
    cod_cie10 = (data.get('cod_cie10') or '').strip().upper() or None
    estado = bool(data.get('est_diagnostico', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.diagnosticoExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un diagnóstico "{descripcion}".'}), 400
    if cod_cie10:
        if not dao.validarCodigoCie10(cod_cie10):
            return jsonify({'success': False, 'error': 'El código CIE-10 no tiene un formato válido (ej. F32 o F32.1).'}), 400
        if dao.codigoCie10Existe(cod_cie10):
            return jsonify({'success': False, 'error': f'Ya existe un diagnóstico con el código CIE-10 "{cod_cie10}".'}), 400

    try:
        nuevo_id = dao.guardarDiagnostico(descripcion, cod_cie10, estado, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_diagnostico': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar diagnóstico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@diagnosticoapi.route('/diagnosticos/<int:diagnostico_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateDiagnostico(diagnostico_id):
    data = request.get_json() or {}
    dao = DiagnosticoDao()

    if not dao.getDiagnosticoById(diagnostico_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_diagnostico') or '').strip().upper()
    cod_cie10 = (data.get('cod_cie10') or '').strip().upper() or None
    estado = bool(data.get('est_diagnostico', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción solo puede contener letras, números, espacios y puntos.'}), 400
    if dao.diagnosticoExiste(descripcion, excluir_id=diagnostico_id):
        return jsonify({'success': False, 'error': f'Ya existe un diagnóstico "{descripcion}".'}), 400
    if cod_cie10:
        if not dao.validarCodigoCie10(cod_cie10):
            return jsonify({'success': False, 'error': 'El código CIE-10 no tiene un formato válido (ej. F32 o F32.1).'}), 400
        if dao.codigoCie10Existe(cod_cie10, excluir_id=diagnostico_id):
            return jsonify({'success': False, 'error': f'Ya existe un diagnóstico con el código CIE-10 "{cod_cie10}".'}), 400

    try:
        dao.updateDiagnostico(diagnostico_id, descripcion, cod_cie10, estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_diagnostico': diagnostico_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar diagnóstico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@diagnosticoapi.route('/diagnosticos/<int:diagnostico_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarDiagnostico(diagnostico_id):
    dao = DiagnosticoDao()

    if not dao.getDiagnosticoById(diagnostico_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarDiagnostico(diagnostico_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Diagnóstico {diagnostico_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar diagnóstico: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
