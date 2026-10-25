from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.dao.auth.user_dao import UsuarioDao
from app.auth.utils.decorators import role_required

empresaapi = Blueprint('empresaapi', __name__)

TIPOS_CONTRIBUYENTE = ("PERSONA_FISICA", "PERSONA_JURIDICA", "EAS")


def _extraer_datos(data):
    """Toma del JSON los datos de la empresa, los normaliza y devuelve (datos, errores de validación)."""
    errores = []

    ruc_nit = (data.get('ruc_nit') or '').strip()
    digito_verificador = (data.get('digito_verificador') or '').strip()
    razon_social = (data.get('razon_social') or '').strip()
    nombre_comercial = (data.get('nombre_comercial') or '').strip() or None
    tipo_contribuyente = (data.get('tipo_contribuyente') or 'PERSONA_JURIDICA').strip().upper()
    id_ciudad = data.get('id_ciudad') or None
    direccion = (data.get('direccion') or '').strip()
    numero_casa = (data.get('numero_casa') or '').strip() or None
    codigo_postal = (data.get('codigo_postal') or '').strip() or None
    telefono = (data.get('telefono') or '').strip()
    celular = (data.get('celular') or '').strip()
    email = (data.get('email') or '').strip()
    sitio_web = (data.get('sitio_web') or '').strip() or None
    actividad_economica_principal = (data.get('actividad_economica_principal') or '').strip() or None
    horario_atencion = (data.get('horario_atencion') or '').strip() or None

    empresadao = EmpresaDao()

    if not ruc_nit:
        errores.append('El RUC/NIT no puede estar vacío.')
    elif not empresadao.validarRuc(ruc_nit):
        errores.append('El RUC/NIT solo puede contener dígitos y debe tener entre 6 y 20 caracteres.')

    if not digito_verificador or len(digito_verificador) != 1:
        errores.append('El dígito verificador es obligatorio y debe ser un solo carácter.')

    if not razon_social:
        errores.append('La razón social no puede estar vacía.')

    if tipo_contribuyente not in TIPOS_CONTRIBUYENTE:
        errores.append('El tipo de contribuyente no es válido.')

    if not direccion:
        errores.append('La dirección no puede estar vacía.')

    if not telefono:
        errores.append('El teléfono no puede estar vacío.')

    if not celular:
        errores.append('El celular no puede estar vacío.')

    if not email:
        errores.append('El email no puede estar vacío.')
    elif not empresadao.validarEmail(email):
        errores.append('El email no tiene un formato válido.')

    horario_atencion_tramos, errores_horario = empresadao.validarTramos(data.get('horario_atencion_tramos'))
    errores.extend(errores_horario)

    datos = dict(
        ruc_nit=ruc_nit, digito_verificador=digito_verificador, razon_social=razon_social,
        nombre_comercial=nombre_comercial, tipo_contribuyente=tipo_contribuyente, id_ciudad=id_ciudad,
        direccion=direccion, numero_casa=numero_casa, codigo_postal=codigo_postal, telefono=telefono,
        celular=celular, email=email, sitio_web=sitio_web,
        actividad_economica_principal=actividad_economica_principal, horario_atencion=horario_atencion,
        horario_atencion_tramos=horario_atencion_tramos,
    )
    return datos, errores


@empresaapi.route('/empresa', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEmpresa():
    """GET: datos de la empresa (registro único)."""
    try:
        data = EmpresaDao().getEmpresaPrincipal()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener empresa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@empresaapi.route('/empresa', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEmpresa():
    """POST: crea el registro de la empresa."""
    data = request.get_json() or {}
    empresadao = EmpresaDao()

    if empresadao.getEmpresaPrincipal() is not None:
        return jsonify({'success': False, 'error': 'Ya existe una empresa configurada.'}), 400

    datos, errores = _extraer_datos(data)
    if errores:
        return jsonify({'success': False, 'error': ' '.join(errores)}), 400
    if empresadao.rucExiste(datos['ruc_nit']):
        return jsonify({'success': False, 'error': f"Ya existe una empresa con el RUC/NIT \"{datos['ruc_nit']}\"."}), 400

    try:
        id_empresa = empresadao.guardarEmpresa(**datos, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_empresa': id_empresa}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar empresa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@empresaapi.route('/empresa/topes', methods=['PATCH'])
@role_required("SUPERADMIN")
def updateTopes():
    """PATCH: el Superadministrador fija cuántos funcionarios y usuarios pueden estar activos a la vez."""
    data = request.get_json() or {}
    try:
        max_func, max_usu = int(data.get('max_funcionarios_activos')), int(data.get('max_usuarios_activos'))
    except (TypeError, ValueError):
        return jsonify({'success': False, 'error': 'Indique el máximo de funcionarios y de usuarios como números enteros.'}), 400
    if max_func < 1 or max_usu < 1:
        return jsonify({'success': False, 'error': 'Los máximos deben ser al menos 1.'}), 400
    if max_usu > max_func:
        return jsonify({'success': False, 'error': 'El máximo de usuarios no puede superar al de funcionarios: cada usuario es un funcionario distinto.'}), 400

    usuariodao = UsuarioDao()
    if max_func < usuariodao.contar_funcionarios_activos() or max_usu < usuariodao.contar_usuarios_activos_con_funcionario():
        return jsonify({'success': False, 'error': 'Los máximos no pueden ser menores que los funcionarios y usuarios activos hoy. Desactive primero a quien corresponda.'}), 400
    actual = EmpresaDao().getEmpresaPrincipal()
    if not actual:
        return jsonify({'success': False, 'error': 'Todavía no hay una empresa configurada.'}), 404
    try:
        EmpresaDao().actualizarTopes(actual['id_empresa'], max_func, max_usu, session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'max_funcionarios_activos': max_func, 'max_usuarios_activos': max_usu}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar topes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@empresaapi.route('/empresa/<int:id_empresa>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEmpresa(id_empresa):
    """PUT: valida y actualiza los datos de la empresa; 404 si no existe."""
    data = request.get_json() or {}
    empresadao = EmpresaDao()

    actual = empresadao.getEmpresaPrincipal()
    if not actual or actual['id_empresa'] != id_empresa:
        return jsonify({'success': False, 'error': 'No se encontró la empresa con el ID proporcionado.'}), 404

    datos, errores = _extraer_datos(data)
    if errores:
        return jsonify({'success': False, 'error': ' '.join(errores)}), 400
    # Sin el campo en el pedido se conserva el horario guardado (solo se borra si llega vacío a propósito)
    if 'horario_atencion_tramos' not in data:
        datos['horario_atencion_tramos'] = actual.get('horario_atencion_tramos')
    if empresadao.rucExiste(datos['ruc_nit'], excluir_id=id_empresa):
        return jsonify({'success': False, 'error': f"Ya existe una empresa con el RUC/NIT \"{datos['ruc_nit']}\"."}), 400

    try:
        empresadao.updateEmpresa(id_empresa, **datos, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_empresa': id_empresa}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar empresa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
