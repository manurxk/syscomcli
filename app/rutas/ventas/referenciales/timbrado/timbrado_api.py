from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.timbrado.TimbradoDao import TimbradoDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_existe, msg_obligatorio

timbradoapi = Blueprint('timbradoapi', __name__)

ROLES_ADM = ("ADMINISTRADOR", "SUPERADMIN")
ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@timbradoapi.route('/timbrados', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbrados():
    """GET: lista los registros de timbrado."""
    try:
        return jsonify({'success': True, 'data': TimbradoDao().getTimbrados(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/vigentes', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbradosVigentes():
    """GET: lista los registros de timbrado."""
    try:
        return jsonify({'success': True, 'data': TimbradoDao().getTimbradosVigentes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados vigentes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@timbradoapi.route('/timbrados/<int:id_timbrado>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getTimbrado(id_timbrado):
    """GET: devuelve timbrado por su id; 404 si no existe."""
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
    """POST: valida los datos y registra timbrado; devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    dao = TimbradoDao()

    numero = (data.get('numero_timbrado') or '').strip()
    codigo_estab = (data.get('codigo_establecimiento') or '001').strip().zfill(3)
    fecha_inicio = data.get('fecha_inicio')
    fecha_vencimiento = data.get('fecha_vencimiento')

    if not numero:
        return jsonify({'success': False, 'error': msg_obligatorio('Número de timbrado')}), 400
    if not dao.validarNumeroTimbrado(numero):
        return jsonify({'success': False, 'error': 'El número de timbrado debe tener 8 dígitos numéricos.'}), 400
    if not dao.validarCodigoEstablecimiento(codigo_estab):
        return jsonify({'success': False, 'error': 'El código de establecimiento debe tener 3 dígitos numéricos.'}), 400
    if not fecha_inicio or not fecha_vencimiento:
        return jsonify({'success': False, 'error': msg_obligatorio('Fechas de inicio y vencimiento')}), 400
    if fecha_vencimiento < fecha_inicio:
        return jsonify({'success': False, 'error': 'La fecha de vencimiento debe ser mayor o igual a la de inicio.'}), 400
    if dao.timbradoExiste(numero):
        return jsonify({'success': False, 'error': msg_existe('un timbrado con número', numero)}), 400

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
    """PUT: valida y actualiza timbrado; 404 si no existe."""
    data = request.get_json() or {}
    dao = TimbradoDao()

    if not dao.getTimbradoById(id_timbrado):
        return jsonify({'success': False, 'error': 'No se encontró el timbrado.'}), 404

    numero = (data.get('numero_timbrado') or '').strip()
    codigo_estab = (data.get('codigo_establecimiento') or '001').strip().zfill(3)
    fecha_inicio = data.get('fecha_inicio')
    fecha_vencimiento = data.get('fecha_vencimiento')

    if not numero:
        return jsonify({'success': False, 'error': msg_obligatorio('Número de timbrado')}), 400
    if not dao.validarNumeroTimbrado(numero):
        return jsonify({'success': False, 'error': 'El número de timbrado debe tener 8 dígitos numéricos.'}), 400
    if not dao.validarCodigoEstablecimiento(codigo_estab):
        return jsonify({'success': False, 'error': 'El código de establecimiento debe tener 3 dígitos numéricos.'}), 400
    if not fecha_inicio or not fecha_vencimiento:
        return jsonify({'success': False, 'error': msg_obligatorio('Fechas')}), 400
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
    """DELETE: da de baja (lógica) timbrado; 404 si no existe."""
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
