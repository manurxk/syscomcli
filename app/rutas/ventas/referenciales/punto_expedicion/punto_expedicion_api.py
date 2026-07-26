from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.punto_expedicion.PuntoExpedicionDao import PuntoExpedicionDao
from app.auth.utils.decorators import role_required

puntoexpedicionapi = Blueprint('puntoexpedicionapi', __name__)

ROLES_ADM = ("ADMINISTRADOR", "SUPERADMIN")
ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@puntoexpedicionapi.route('/puntos-expedicion', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getPuntosExpedicion():
    id_timbrado = request.args.get('id_timbrado', type=int)
    try:
        return jsonify({'success': True, 'data': PuntoExpedicionDao().getPuntosExpedicion(id_timbrado), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener puntos de expedición: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@puntoexpedicionapi.route('/puntos-expedicion/vigentes', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getPuntosVigentes():
    try:
        return jsonify({'success': True, 'data': PuntoExpedicionDao().getPuntosVigentes(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener puntos vigentes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@puntoexpedicionapi.route('/puntos-expedicion/<int:id_punto_expedicion>', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getPuntoExpedicion(id_punto_expedicion):
    try:
        reg = PuntoExpedicionDao().getPuntoExpedicionById(id_punto_expedicion)
        if not reg:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': reg, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener punto de expedición: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@puntoexpedicionapi.route('/puntos-expedicion', methods=['POST'])
@role_required(*ROLES_ADM)
def addPuntoExpedicion():
    data = request.get_json() or {}
    dao = PuntoExpedicionDao()

    id_timbrado = data.get('id_timbrado')
    codigo = (data.get('codigo_punto_expedicion') or '').strip()
    nombre = (data.get('nombre_punto_expedicion') or '').strip()

    if not id_timbrado:
        return jsonify({'success': False, 'error': 'El timbrado es obligatorio.'}), 400
    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio (3 dígitos).'}), 400
    if not dao.validarCodigo(codigo.zfill(3)):
        return jsonify({'success': False, 'error': 'El código debe tener 3 dígitos numéricos.'}), 400
    if not nombre:
        return jsonify({'success': False, 'error': 'El nombre del punto es obligatorio.'}), 400
    if dao.codigoExiste(id_timbrado, codigo.zfill(3)):
        return jsonify({'success': False, 'error': f'Ya existe el código "{codigo}" para este timbrado.'}), 400

    try:
        nuevo_id = dao.guardar(
            id_timbrado=id_timbrado,
            codigo_punto_expedicion=codigo,
            nombre_punto_expedicion=nombre,
            est_punto_expedicion=bool(data.get('est_punto_expedicion', True)),
            usuario_creacion=session.get('id_usuario'),
        )
        return jsonify({'success': True, 'data': {'id_punto_expedicion': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar punto de expedición: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@puntoexpedicionapi.route('/puntos-expedicion/<int:id_punto_expedicion>', methods=['PUT'])
@role_required(*ROLES_ADM)
def updatePuntoExpedicion(id_punto_expedicion):
    data = request.get_json() or {}
    dao = PuntoExpedicionDao()

    reg = dao.getPuntoExpedicionById(id_punto_expedicion)
    if not reg:
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    codigo = (data.get('codigo_punto_expedicion') or '').strip()
    nombre = (data.get('nombre_punto_expedicion') or '').strip()

    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    if not dao.validarCodigo(codigo.zfill(3)):
        return jsonify({'success': False, 'error': 'El código debe tener 3 dígitos numéricos.'}), 400
    if not nombre:
        return jsonify({'success': False, 'error': 'El nombre es obligatorio.'}), 400
    if dao.codigoExiste(reg['id_timbrado'], codigo.zfill(3), excluir_id=id_punto_expedicion):
        return jsonify({'success': False, 'error': f'Ya existe el código "{codigo}" para este timbrado.'}), 400

    try:
        dao.update(
            id_punto_expedicion=id_punto_expedicion,
            codigo_punto_expedicion=codigo,
            nombre_punto_expedicion=nombre,
            est_punto_expedicion=bool(data.get('est_punto_expedicion', True)),
            usuario_modificacion=session.get('id_usuario'),
        )
        return jsonify({'success': True, 'data': {'id_punto_expedicion': id_punto_expedicion}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar punto de expedición: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@puntoexpedicionapi.route('/puntos-expedicion/<int:id_punto_expedicion>', methods=['DELETE'])
@role_required(*ROLES_ADM)
def deletePuntoExpedicion(id_punto_expedicion):
    dao = PuntoExpedicionDao()
    if not dao.getPuntoExpedicionById(id_punto_expedicion):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    if dao.tieneFacturas(id_punto_expedicion):
        return jsonify({'success': False, 'error': 'No se puede eliminar: tiene facturas asociadas.'}), 409
    try:
        dao.desactivar(id_punto_expedicion, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Punto {id_punto_expedicion} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar punto de expedición: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
