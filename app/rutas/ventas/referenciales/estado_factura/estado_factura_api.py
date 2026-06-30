from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.estado_factura.EstadoFacturaDao import EstadoFacturaDao
from app.auth.utils.decorators import role_required

estadofacturaapi = Blueprint('estadofacturaapi', __name__)


@estadofacturaapi.route('/estados-factura', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEstadosFactura():
    try:
        return jsonify({'success': True, 'data': EstadoFacturaDao().getEstadosFactura(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estados de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@estadofacturaapi.route('/estados-factura/<int:id_estado_factura>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getEstadoFactura(id_estado_factura):
    try:
        registro = EstadoFacturaDao().getEstadoFacturaById(id_estado_factura)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@estadofacturaapi.route('/estados-factura', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEstadoFactura():
    data = request.get_json() or {}
    dao = EstadoFacturaDao()

    descripcion = (data.get('des_estado_factura') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.estadoFacturaExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe un estado de factura "{descripcion}".'}), 400

    try:
        nuevo_id = dao.guardarEstadoFactura(
            descripcion=descripcion,
            codigo=data.get('cod_estado_factura'),
            permite_modificacion=bool(data.get('permite_modificacion', True)),
            permite_anulacion=bool(data.get('permite_anulacion', True)),
            color=data.get('color_estado', 'secondary'),
            estado=bool(data.get('est_estado_factura', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_estado_factura': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@estadofacturaapi.route('/estados-factura/<int:id_estado_factura>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEstadoFactura(id_estado_factura):
    data = request.get_json() or {}
    dao = EstadoFacturaDao()

    if not dao.getEstadoFacturaById(id_estado_factura):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_estado_factura') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.estadoFacturaExiste(descripcion, excluir_id=id_estado_factura):
        return jsonify({'success': False, 'error': f'Ya existe un estado de factura "{descripcion}".'}), 400

    try:
        dao.updateEstadoFactura(
            id_estado_factura=id_estado_factura,
            descripcion=descripcion,
            codigo=data.get('cod_estado_factura'),
            permite_modificacion=bool(data.get('permite_modificacion', True)),
            permite_anulacion=bool(data.get('permite_anulacion', True)),
            color=data.get('color_estado', 'secondary'),
            estado=bool(data.get('est_estado_factura', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_estado_factura': id_estado_factura}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@estadofacturaapi.route('/estados-factura/<int:id_estado_factura>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarEstadoFactura(id_estado_factura):
    dao = EstadoFacturaDao()
    if not dao.getEstadoFacturaById(id_estado_factura):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarEstadoFactura(id_estado_factura, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_estado_factura} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar estado de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
