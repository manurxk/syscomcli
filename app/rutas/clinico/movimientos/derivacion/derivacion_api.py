from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.movimientos.derivacion.DerivacionDao import DerivacionDao
from app.auth.utils.decorators import role_required

derivacionapi = Blueprint('derivacionapi', __name__)

ROLES_DERIVACION = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@derivacionapi.route('/consultas/<int:id_consulta>/derivaciones', methods=['GET'])
@role_required(*ROLES_DERIVACION)
def getDerivaciones(id_consulta):
    try:
        data = DerivacionDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener derivaciones de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/consultas/<int:id_consulta>/derivaciones', methods=['POST'])
@role_required(*ROLES_DERIVACION)
def addDerivacion(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_especialidad_destino'):
        return jsonify({'success': False, 'error': 'La especialidad de destino es obligatoria.'}), 400
    if not (data.get('motivo_derivacion') or '').strip():
        return jsonify({'success': False, 'error': 'El motivo de derivación es obligatorio.'}), 400

    try:
        nuevo_id = DerivacionDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_derivacion': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar derivación de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>', methods=['DELETE'])
@role_required(*ROLES_DERIVACION)
def deleteDerivacion(id_derivacion):
    try:
        if DerivacionDao().desactivar(id_derivacion, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Derivación eliminada correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró la derivación con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
