from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.ventas.referenciales.forma_cobro.FormaCobroDao import FormaCobroDao
from app.auth.utils.decorators import role_required

formacobroapi = Blueprint('formacobroapi', __name__)


@formacobroapi.route('/formas-cobro', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getFormasCobro():
    try:
        return jsonify({'success': True, 'data': FormaCobroDao().getFormasCobro(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener formas de cobro: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@formacobroapi.route('/formas-cobro/<int:id_forma_cobro>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def getFormaCobro(id_forma_cobro):
    try:
        registro = FormaCobroDao().getFormaCobroById(id_forma_cobro)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener forma de cobro: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@formacobroapi.route('/formas-cobro', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addFormaCobro():
    data = request.get_json() or {}
    dao = FormaCobroDao()

    descripcion = (data.get('des_forma_cobro') or '').strip().upper()
    codigo = (data.get('cod_forma_cobro') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.formaCobroExiste(descripcion):
        return jsonify({'success': False, 'error': f'Ya existe una forma de cobro "{descripcion}".'}), 400
    if dao.codigoExiste(codigo):
        return jsonify({'success': False, 'error': f'Ya existe una forma de cobro con código "{codigo}".'}), 400

    try:
        nuevo_id = dao.guardarFormaCobro(
            descripcion=descripcion,
            codigo=codigo,
            requiere_entidad=bool(data.get('requiere_entidad', False)),
            permite_cuotas=bool(data.get('permite_cuotas', False)),
            estado=bool(data.get('est_forma_cobro', True)),
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_forma_cobro': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar forma de cobro: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@formacobroapi.route('/formas-cobro/<int:id_forma_cobro>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateFormaCobro(id_forma_cobro):
    data = request.get_json() or {}
    dao = FormaCobroDao()

    if not dao.getFormaCobroById(id_forma_cobro):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404

    descripcion = (data.get('des_forma_cobro') or '').strip().upper()
    codigo = (data.get('cod_forma_cobro') or '').strip().upper()

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not codigo:
        return jsonify({'success': False, 'error': 'El código es obligatorio.'}), 400
    if not dao.validarDescripcion(descripcion):
        return jsonify({'success': False, 'error': 'La descripción contiene caracteres inválidos.'}), 400
    if dao.formaCobroExiste(descripcion, excluir_id=id_forma_cobro):
        return jsonify({'success': False, 'error': f'Ya existe una forma de cobro "{descripcion}".'}), 400
    if dao.codigoExiste(codigo, excluir_id=id_forma_cobro):
        return jsonify({'success': False, 'error': f'Ya existe una forma de cobro con código "{codigo}".'}), 400

    try:
        dao.updateFormaCobro(
            id_forma_cobro=id_forma_cobro,
            descripcion=descripcion,
            codigo=codigo,
            requiere_entidad=bool(data.get('requiere_entidad', False)),
            permite_cuotas=bool(data.get('permite_cuotas', False)),
            estado=bool(data.get('est_forma_cobro', True)),
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_forma_cobro': id_forma_cobro}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar forma de cobro: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@formacobroapi.route('/formas-cobro/<int:id_forma_cobro>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarFormaCobro(id_forma_cobro):
    dao = FormaCobroDao()
    if not dao.getFormaCobroById(id_forma_cobro):
        return jsonify({'success': False, 'error': 'No se encontró el registro.'}), 404
    try:
        dao.desactivarFormaCobro(id_forma_cobro, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Registro {id_forma_cobro} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar forma de cobro: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
