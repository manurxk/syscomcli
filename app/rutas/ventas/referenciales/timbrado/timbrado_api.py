from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.timbrado.TimbradoDao import TimbradoDao
from app.auth.utils.decorators import role_required

timbradoapi = Blueprint('timbradoapi', __name__)

ROLES_ADM = ("ADMINISTRADOR", "SUPERADMIN")
ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@timbradoapi.route('/timbrados', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbrados():
    try:
        return jsonify({'success': True, 'data': TimbradoDao().getTimbrados(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/vigentes', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbradosVigentes():
    try:
        return jsonify({'success': True, 'data': TimbradoDao().getTimbradosVigentes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados vigentes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/<int:id_timbrado>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbrado(id_timbrado):
    try:
        reg = TimbradoDao().getTimbradoById(id_timbrado)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró el timbrado.'}), 404
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados', methods=['POST'])
@role_required(*ROLES_ADM)
def addTimbrado():
    data = request.get_json() or {}
    dao = TimbradoDao()

    numero = (data.get('numero_timbrado') or '').strip()
    codigo_estab = (data.get('codigo_establecimiento') or '001').strip().zfill(3)
    fecha_inicio = data.get('fecha_inicio')
    fecha_vencimiento = data.get('fecha_vencimiento')

    if not numero:
        return jsonify({'success': False, 'error': 'El número de timbrado es obligatorio.'}), 400
    if not fecha_inicio or not fecha_vencimiento:
        return jsonify({'success': False, 'error': 'Las fechas de inicio y vencimiento son obligatorias.'}), 400
    if fecha_vencimiento < fecha_inicio:
        return jsonify({'success': False, 'error': 'La fecha de vencimiento debe ser mayor o igual a la de inicio.'}), 400
    if dao.timbradoExiste(numero):
        return jsonify({'success': False, 'error': f'Ya existe un timbrado con número "{numero}".'}), 400

    try:
        nuevo_id = dao.guardar(
            numero_timbrado=numero,
            codigo_establecimiento=codigo_estab,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            observaciones=data.get('observaciones'),
            est_timbrado=bool(data.get('est_timbrado', True)),
            usuario_creacion=session.get('id_usuario'),
        )
        return jsonify({'success': True, 'data': {'id_timbrado': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar timbrado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/<int:id_timbrado>', methods=['PUT'])
@role_required(*ROLES_ADM)
def updateTimbrado(id_timbrado):
    data = request.get_json() or {}
    dao = TimbradoDao()

    if not dao.getTimbradoById(id_timbrado):
        return jsonify({'success': False, 'error': 'No se encontró el timbrado.'}), 404

    numero = (data.get('numero_timbrado') or '').strip()
    codigo_estab = (data.get('codigo_establecimiento') or '001').strip().zfill(3)
    fecha_inicio = data.get('fecha_inicio')
    fecha_vencimiento = data.get('fecha_vencimiento')

    if not numero:
        return jsonify({'success': False, 'error': 'El número de timbrado es obligatorio.'}), 400
    if not fecha_inicio or not fecha_vencimiento:
        return jsonify({'success': False, 'error': 'Las fechas son obligatorias.'}), 400
    if fecha_vencimiento < fecha_inicio:
        return jsonify({'success': False, 'error': 'La fecha de vencimiento debe ser mayor o igual a la de inicio.'}), 400
    if dao.timbradoExiste(numero, excluir_id=id_timbrado):
        return jsonify({'success': False, 'error': f'Ya existe otro timbrado con número "{numero}".'}), 400

    try:
        dao.update(
            id_timbrado=id_timbrado,
            numero_timbrado=numero,
            codigo_establecimiento=codigo_estab,
            fecha_inicio=fecha_inicio,
            fecha_vencimiento=fecha_vencimiento,
            observaciones=data.get('observaciones'),
            est_timbrado=bool(data.get('est_timbrado', True)),
            usuario_modificacion=session.get('id_usuario'),
        )
        return jsonify({'success': True, 'data': {'id_timbrado': id_timbrado}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar timbrado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/<int:id_timbrado>', methods=['DELETE'])
@role_required(*ROLES_ADM)
def deleteTimbrado(id_timbrado):
    dao = TimbradoDao()
    if not dao.getTimbradoById(id_timbrado):
        return jsonify({'success': False, 'error': 'No se encontró el timbrado.'}), 404
    if dao.tieneFacturas(id_timbrado):
        return jsonify({'success': False, 'error': 'No se puede eliminar: tiene facturas asociadas.'}), 409
    try:
        dao.desactivar(id_timbrado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Timbrado {id_timbrado} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar timbrado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
