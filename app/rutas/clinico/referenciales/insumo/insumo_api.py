from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.referenciales.insumo.InsumoDao import InsumoDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_caracteres, msg_existe, msg_obligatorio

insumoapi = Blueprint('insumoapi', __name__)


@insumoapi.route('/insumos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getInsumos():
    """GET: lista los registros de insumo."""
    try:
        data = InsumoDao().getInsumos()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
def getInsumo(insumo_id):
    """GET: registro de insumo por su id; 404 si no existe."""
    try:
        registro = InsumoDao().getInsumoById(insumo_id)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addInsumo():
    """POST: valida los datos y crea un registro de insumo; devuelve el id nuevo (201)."""
    data = request.get_json() or {}
    dao = InsumoDao()

    descripcion = (data.get('des_insumo') or '').strip().upper()
    unidad_medida = (data.get('insumo_unidad_medida') or 'UNIDAD').strip().upper()
    stock_actual = data.get('stock_actual', 0)
    stock_minimo = data.get('stock_minimo', 0)
    precio_unitario = data.get('insumo_precio_unitario')
    estado = bool(data.get('est_insumo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.insumoExiste(descripcion):
        return jsonify({'success': False, 'error': msg_existe('un insumo', descripcion)}), 400
    if stock_actual is not None and float(stock_actual) < 0:
        return jsonify({'success': False, 'error': 'El stock actual no puede ser negativo.'}), 400
    if stock_minimo is not None and float(stock_minimo) < 0:
        return jsonify({'success': False, 'error': 'El stock mínimo no puede ser negativo.'}), 400
    if precio_unitario is not None and float(precio_unitario) < 0:
        return jsonify({'success': False, 'error': 'El precio unitario no puede ser negativo.'}), 400

    try:
        nuevo_id = dao.guardarInsumo(
            descripcion, unidad_medida, stock_actual, stock_minimo, precio_unitario,
            estado, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_insumo': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateInsumo(insumo_id):
    """PUT: valida y actualiza el registro de insumo; 404 si no existe."""
    data = request.get_json() or {}
    dao = InsumoDao()

    if not dao.getInsumoById(insumo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    descripcion = (data.get('des_insumo') or '').strip().upper()
    unidad_medida = (data.get('insumo_unidad_medida') or 'UNIDAD').strip().upper()
    stock_actual = data.get('stock_actual', 0)
    stock_minimo = data.get('stock_minimo', 0)
    precio_unitario = data.get('insumo_precio_unitario')
    estado = bool(data.get('est_insumo', True))

    if not descripcion:
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción')}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': msg_caracteres('Descripción', 'letras, números, espacios y puntos')}), 400
    if dao.insumoExiste(descripcion, excluir_id=insumo_id):
        return jsonify({'success': False, 'error': msg_existe('un insumo', descripcion)}), 400
    if stock_actual is not None and float(stock_actual) < 0:
        return jsonify({'success': False, 'error': 'El stock actual no puede ser negativo.'}), 400
    if stock_minimo is not None and float(stock_minimo) < 0:
        return jsonify({'success': False, 'error': 'El stock mínimo no puede ser negativo.'}), 400
    if precio_unitario is not None and float(precio_unitario) < 0:
        return jsonify({'success': False, 'error': 'El precio unitario no puede ser negativo.'}), 400

    try:
        dao.updateInsumo(
            insumo_id, descripcion, unidad_medida, stock_actual, stock_minimo, precio_unitario,
            estado, usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_insumo': insumo_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@insumoapi.route('/insumos/<int:insumo_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarInsumo(insumo_id):
    """DELETE: baja lógica del registro de insumo; 404 si no existe."""
    dao = InsumoDao()

    if not dao.getInsumoById(insumo_id):
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404

    try:
        dao.desactivarInsumo(insumo_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Insumo {insumo_id} desactivado correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar insumo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
