from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.clinico.movimientos.consulta.AnamnesisDao import AnamnesisDao, CAMPOS_ANAMNESIS, CAMPOS_BOOLEANOS_ANAMNESIS
from app.auth.utils.decorators import role_required

anamnesisapi = Blueprint('anamnesisapi', __name__)

ROLES_ANAMNESIS = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@anamnesisapi.route('/anamnesis/paciente/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_ANAMNESIS)
def getAnamnesisActual(id_paciente):
    try:
        data = AnamnesisDao().getAnamnesisActual(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener anamnesis actual: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/paciente/<int:id_paciente>/historial', methods=['GET'])
@role_required(*ROLES_ANAMNESIS)
def getHistorialAnamnesis(id_paciente):
    try:
        data = AnamnesisDao().getHistorialAnamnesis(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de anamnesis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>', methods=['GET'])
@role_required(*ROLES_ANAMNESIS)
def getAnamnesis(id_anamnesis):
    try:
        data = AnamnesisDao().getAnamnesisById(id_anamnesis)
        if not data:
            return jsonify({'success': False, 'error': 'No se encontró la versión de anamnesis indicada.'}), 404
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener anamnesis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/paciente/<int:id_paciente>', methods=['POST'])
@role_required(*ROLES_ANAMNESIS)
def addVersionAnamnesis(id_paciente):
    """Crea una nueva versión de la anamnesis del paciente (insert-only, ver AnamnesisDao)."""
    data = request.get_json() or {}

    if not (data.get('motivo_consulta') or '').strip():
        return jsonify({'success': False, 'error': 'El campo "motivo_consulta" es obligatorio.'}), 400

    try:
        datos = {campo: data.get(campo) for campo in CAMPOS_ANAMNESIS}
        for campo in CAMPOS_BOOLEANOS_ANAMNESIS:
            datos[campo] = bool(data.get(campo, False))
        id_anamnesis = AnamnesisDao().guardarNuevaVersion(id_paciente, datos, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_anamnesis': id_anamnesis}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
