from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.condicion_venta.CondicionVentaDao import CondicionVentaDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_caracteres, msg_existe, msg_obligatorio

condicionventaapi = Blueprint('condicionventaapi', __name__)


@condicionventaapi.route('/condiciones-venta', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getCondicionesVenta():
    """GET: lista los registros de condición de venta."""
    try:
        return jsonify({'success': True, 'data': CondicionVentaDao().getCondicionesVenta(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener condiciones de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@condicionventaapi.route('/condiciones-venta/<int:id_condicion_venta>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getCondicionVenta(id_condicion_venta):
    """GET: devuelve condición de venta por su id; 404 si no existe."""
    try:
        registro = CondicionVentaDao().getCondicionVentaById(id_condicion_venta)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@condicionventaapi.route('/condiciones-venta', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addCondicionVenta():
    """POST: valida los datos y registra condición de venta; devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    dao = CondicionVentaDao()

    descripcion = (data.get('des_condicion_venta') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.condicionVentaExiste(descripcion):
        return jsonify({'success': False, 'error': msg_existe('una condición de venta', descripcion)}), 400

    try:
        nuevo_id = dao.guardarCondicionVenta(
            descripcion=descripcion,
            codigo=data.get('cod_condicion_venta'),
            dias_credito=int(data.get('dias_credito', 0)),
            permite_cuotas=bool(data.get('permite_cuotas', False)),
            numero_cuotas_max=int(data.get('numero_cuotas_max', 1)),
            estado=bool(data.get('est_condicion_venta', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_condicion_venta': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@condicionventaapi.route('/condiciones-venta/<int:id_condicion_venta>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateCondicionVenta(id_condicion_venta):
    """PUT: valida y actualiza condición de venta; 404 si no existe."""
    data = request.get_json() or {}
    dao = CondicionVentaDao()

    if not dao.getCondicionVentaById(id_condicion_venta):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_condicion_venta') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.condicionVentaExiste(descripcion, excluir_id=id_condicion_venta):
        return jsonify({'success': False, 'error': msg_existe('una condición de venta', descripcion)}), 400

    try:
        dao.updateCondicionVenta(
            id_condicion_venta=id_condicion_venta,
            descripcion=descripcion,
            codigo=data.get('cod_condicion_venta'),
            dias_credito=int(data.get('dias_credito', 0)),
            permite_cuotas=bool(data.get('permite_cuotas', False)),
            numero_cuotas_max=int(data.get('numero_cuotas_max', 1)),
            estado=bool(data.get('est_condicion_venta', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_condicion_venta': id_condicion_venta}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@condicionventaapi.route('/condiciones-venta/<int:id_condicion_venta>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarCondicionVenta(id_condicion_venta):
    """DELETE: da de baja (lógica) condición de venta; 404 si no existe."""
    dao = CondicionVentaDao()
    if not dao.getCondicionVentaById(id_condicion_venta):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarCondicionVenta(id_condicion_venta, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_condicion_venta} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar condición de venta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
