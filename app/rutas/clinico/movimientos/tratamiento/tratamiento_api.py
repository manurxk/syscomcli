from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.movimientos.tratamiento.TratamientoDao import TratamientoDao
from app.auth.utils.decorators import role_required

tratamientoapi = Blueprint('tratamientoapi', __name__)

ROLES_TRATAMIENTO = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@tratamientoapi.route('/consultas/<int:id_consulta>/tratamientos', methods=['GET'])
@role_required(*ROLES_TRATAMIENTO)
def getTratamientos(id_consulta):
    try:
        data = TratamientoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tratamientos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/consultas/<int:id_consulta>/tratamientos', methods=['POST'])
@role_required(*ROLES_TRATAMIENTO)
def addTratamiento(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_tipo_tratamiento'):
        return jsonify({'success': False, 'error': 'El tipo de tratamiento es obligatorio.'}), 400
    if not (data.get('des_tratamiento') or '').strip():
        return jsonify({'success': False, 'error': 'La descripción del tratamiento es obligatoria.'}), 400
    if not data.get('tratamiento_fecha_inicio'):
        return jsonify({'success': False, 'error': 'La fecha de inicio es obligatoria.'}), 400

    try:
        nuevo_id = TratamientoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tratamiento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tratamiento de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>', methods=['DELETE'])
@role_required(*ROLES_TRATAMIENTO)
def deleteTratamiento(id_tratamiento):
    try:
        if TratamientoDao().desactivar(id_tratamiento, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tratamiento de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
