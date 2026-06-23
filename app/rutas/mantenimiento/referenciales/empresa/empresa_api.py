from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.auth.utils.decorators import role_required

empresaapi = Blueprint('empresaapi', __name__)

TIPOS_CONTRIBUYENTE = ("PERSONA_FISICA", "PERSONA_JURIDICA", "EAS")


def _extraer_datos(data):
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

    datos = dict(
        ruc_nit=ruc_nit, digito_verificador=digito_verificador, razon_social=razon_social,
        nombre_comercial=nombre_comercial, tipo_contribuyente=tipo_contribuyente, id_ciudad=id_ciudad,
        direccion=direccion, numero_casa=numero_casa, codigo_postal=codigo_postal, telefono=telefono,
        celular=celular, email=email, sitio_web=sitio_web,
        actividad_economica_principal=actividad_economica_principal, horario_atencion=horario_atencion,
    )
    return datos, errores


@empresaapi.route('/empresa', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getEmpresa():
    try:
        data = EmpresaDao().getEmpresaPrincipal()
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener empresa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@empresaapi.route('/empresa', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addEmpresa():
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


@empresaapi.route('/empresa/<int:id_empresa>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateEmpresa(id_empresa):
    data = request.get_json() or {}
    empresadao = EmpresaDao()

    actual = empresadao.getEmpresaPrincipal()
    if not actual or actual['id_empresa'] != id_empresa:
        return jsonify({'success': False, 'error': 'No se encontró la empresa con el ID proporcionado.'}), 404

    datos, errores = _extraer_datos(data)
    if errores:
        return jsonify({'success': False, 'error': ' '.join(errores)}), 400
    if empresadao.rucExiste(datos['ruc_nit'], excluir_id=id_empresa):
        return jsonify({'success': False, 'error': f"Ya existe una empresa con el RUC/NIT \"{datos['ruc_nit']}\"."}), 400

    try:
        empresadao.updateEmpresa(id_empresa, **datos, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_empresa': id_empresa}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar empresa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
