from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.movimientos.orden.OrdenDao import OrdenDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.auth.utils.decorators import role_required

ordenapi = Blueprint('ordenapi', __name__)

ROLES_ORDEN = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@ordenapi.route('/consultas/<int:id_consulta>/ordenes', methods=['GET'])
@role_required(*ROLES_ORDEN)
def getOrdenes(id_consulta):
    try:
        data = OrdenDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener órdenes de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/consultas/<int:id_consulta>/ordenes', methods=['POST'])
@role_required(*ROLES_ORDEN)
def addOrden(id_consulta):
    data = request.get_json() or {}
    if not data.get('orden_fecha'):
        return jsonify({'success': False, 'error': 'La fecha de la orden es obligatoria.'}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La orden debe tener al menos un ítem de estudio o análisis.'}), 400
    for d in detalles:
        if d.get('tipo_orden') not in ('ESTUDIO', 'ANALISIS'):
            return jsonify({'success': False, 'error': 'Cada ítem debe indicar tipo ESTUDIO o ANALISIS.'}), 400
        if d['tipo_orden'] == 'ESTUDIO' and not d.get('id_tipo_estudio'):
            return jsonify({'success': False, 'error': 'Seleccione el tipo de estudio en cada ítem.'}), 400
        if d['tipo_orden'] == 'ANALISIS' and not d.get('id_tipo_analisis'):
            return jsonify({'success': False, 'error': 'Seleccione el tipo de análisis en cada ítem.'}), 400

    consulta = ConsultaDao().getConsultaParaEditar(id_consulta)
    if not consulta:
        return jsonify({'success': False, 'error': 'La consulta no existe.'}), 404

    try:
        nuevo_id = OrdenDao().guardar(
            id_consulta, consulta['id_paciente'], consulta['id_especialista'],
            data, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_orden': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar orden de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/ordenes/<int:id_orden>', methods=['DELETE'])
@role_required(*ROLES_ORDEN)
def deleteOrden(id_orden):
    try:
        if OrdenDao().desactivar(id_orden, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar orden de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
