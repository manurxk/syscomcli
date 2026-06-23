from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.sede.SedeDao import SedeDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.auth.utils.decorators import role_required

sedeapi = Blueprint('sedeapi', __name__)


@sedeapi.route('/sedes', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSedes():
    try:
        data = SedeDao().getSedes()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener sedes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sedeapi.route('/sedes/<int:sede_id>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getSede(sede_id):
    try:
        sede = SedeDao().getSedeById(sede_id)
        if not sede:
            return jsonify({'success': False, 'error': 'No se encontró la sede con el ID proporcionado.'}), 404
        return jsonify({'success': True, 'data': sede, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener sede: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sedeapi.route('/sedes', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addSede():
    data = request.get_json() or {}
    sededao = SedeDao()

    descripcion = (data.get('des_sede') or '').strip().upper()
    codigo_sede = (data.get('codigo_sede') or '').strip().upper() or None
    cod_establecimiento_sifen = (data.get('cod_establecimiento_sifen') or '').strip() or None
    id_ciudad = data.get('id_ciudad') or None
    direccion = (data.get('direccion') or '').strip() or None
    codigo_postal = (data.get('codigo_postal') or '').strip() or None
    telefono = (data.get('telefono') or '').strip() or None
    email = (data.get('email') or '').strip() or None
    horario_atencion = (data.get('horario_atencion') or '').strip() or None
    estado = bool(data.get('est_sede', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not sededao.validarCodigoEstablecimiento(cod_establecimiento_sifen):
        return jsonify({'success': False, 'error': 'El código de establecimiento SIFEN debe tener 3 dígitos numéricos.'}), 400

    empresa = EmpresaDao().getEmpresaPrincipal()
    if not empresa:
        return jsonify({'success': False, 'error': 'No hay una empresa configurada. Configure los datos de la empresa antes de crear sedes.'}), 400
    if sededao.codigoEstablecimientoExiste(cod_establecimiento_sifen, empresa['id_empresa']):
        return jsonify({'success': False, 'error': f'Ya existe una sede con el código de establecimiento "{cod_establecimiento_sifen}".'}), 400

    try:
        sede_id = sededao.guardarSede(
            descripcion, codigo_sede=codigo_sede, cod_establecimiento_sifen=cod_establecimiento_sifen,
            id_ciudad=id_ciudad, direccion=direccion, codigo_postal=codigo_postal, telefono=telefono,
            email=email, horario_atencion=horario_atencion, estado=estado,
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_sede': sede_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar sede: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sedeapi.route('/sedes/<int:sede_id>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateSede(sede_id):
    data = request.get_json() or {}
    sededao = SedeDao()

    actual = sededao.getSedeById(sede_id)
    if not actual:
        return jsonify({'success': False, 'error': 'No se encontró la sede con el ID proporcionado.'}), 404

    descripcion = (data.get('des_sede') or '').strip().upper()
    codigo_sede = (data.get('codigo_sede') or '').strip().upper() or None
    cod_establecimiento_sifen = (data.get('cod_establecimiento_sifen') or '').strip() or None
    id_ciudad = data.get('id_ciudad') or None
    direccion = (data.get('direccion') or '').strip() or None
    codigo_postal = (data.get('codigo_postal') or '').strip() or None
    telefono = (data.get('telefono') or '').strip() or None
    email = (data.get('email') or '').strip() or None
    horario_atencion = (data.get('horario_atencion') or '').strip() or None
    estado = bool(data.get('est_sede', True))

    if not descripcion:
        return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400
    if not sededao.validarCodigoEstablecimiento(cod_establecimiento_sifen):
        return jsonify({'success': False, 'error': 'El código de establecimiento SIFEN debe tener 3 dígitos numéricos.'}), 400
    if sededao.codigoEstablecimientoExiste(cod_establecimiento_sifen, actual['id_empresa'], excluir_id=sede_id):
        return jsonify({'success': False, 'error': f'Ya existe una sede con el código de establecimiento "{cod_establecimiento_sifen}".'}), 400

    try:
        sededao.updateSede(
            sede_id, descripcion, codigo_sede=codigo_sede, cod_establecimiento_sifen=cod_establecimiento_sifen,
            id_ciudad=id_ciudad, direccion=direccion, codigo_postal=codigo_postal, telefono=telefono,
            email=email, horario_atencion=horario_atencion, estado=estado,
            usuario_modificacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_sede': sede_id}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar sede: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@sedeapi.route('/sedes/<int:sede_id>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def desactivarSede(sede_id):
    sededao = SedeDao()

    if not sededao.getSedeById(sede_id):
        return jsonify({'success': False, 'error': 'No se encontró la sede con el ID proporcionado.'}), 404

    try:
        sededao.desactivarSede(sede_id, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Sede {sede_id} desactivada correctamente.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar sede: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
