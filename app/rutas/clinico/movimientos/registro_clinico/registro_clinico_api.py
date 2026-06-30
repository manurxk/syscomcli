from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.clinico.movimientos.registro_clinico.RegistroDiagnosticoDao import RegistroDiagnosticoDao
from app.dao.clinico.movimientos.registro_clinico.RegistroSignoDao import RegistroSignoDao
from app.dao.clinico.movimientos.registro_clinico.RegistroSintomaDao import RegistroSintomaDao
from app.dao.clinico.movimientos.registro_clinico.RegistroProcedimientoDao import RegistroProcedimientoDao
from app.dao.clinico.movimientos.registro_clinico.RegistroInsumoDao import RegistroInsumoDao
from app.auth.utils.decorators import role_required

registroclinicoapi = Blueprint('registroclinicoapi', __name__)

ROLES_REGISTRO_CLINICO = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


# ============================================================================
# DIAGNÓSTICOS
# ============================================================================
@registroclinicoapi.route('/consultas/<int:id_consulta>/diagnosticos', methods=['GET'])
@role_required(*ROLES_REGISTRO_CLINICO)
def getRegistroDiagnosticos(id_consulta):
    try:
        data = RegistroDiagnosticoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener diagnósticos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/consultas/<int:id_consulta>/diagnosticos', methods=['POST'])
@role_required(*ROLES_REGISTRO_CLINICO)
def addRegistroDiagnostico(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_diagnostico'):
        return jsonify({'success': False, 'error': 'El diagnóstico es obligatorio.'}), 400

    try:
        nuevo_id = RegistroDiagnosticoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_registro_diagnostico': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar diagnóstico de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/registro-diagnosticos/<int:id_registro_diagnostico>', methods=['DELETE'])
@role_required(*ROLES_REGISTRO_CLINICO)
def deleteRegistroDiagnostico(id_registro_diagnostico):
    try:
        if RegistroDiagnosticoDao().desactivar(id_registro_diagnostico, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar diagnóstico de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================================================
# SIGNOS
# ============================================================================
@registroclinicoapi.route('/consultas/<int:id_consulta>/signos', methods=['GET'])
@role_required(*ROLES_REGISTRO_CLINICO)
def getRegistroSignos(id_consulta):
    try:
        data = RegistroSignoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener signos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/consultas/<int:id_consulta>/signos', methods=['POST'])
@role_required(*ROLES_REGISTRO_CLINICO)
def addRegistroSigno(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_signo'):
        return jsonify({'success': False, 'error': 'El signo es obligatorio.'}), 400

    try:
        nuevo_id = RegistroSignoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_registro_signo': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar signo de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/registro-signos/<int:id_registro_signo>', methods=['DELETE'])
@role_required(*ROLES_REGISTRO_CLINICO)
def deleteRegistroSigno(id_registro_signo):
    try:
        if RegistroSignoDao().desactivar(id_registro_signo, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar signo de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================================================
# SÍNTOMAS
# ============================================================================
@registroclinicoapi.route('/consultas/<int:id_consulta>/sintomas', methods=['GET'])
@role_required(*ROLES_REGISTRO_CLINICO)
def getRegistroSintomas(id_consulta):
    try:
        data = RegistroSintomaDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener síntomas de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/consultas/<int:id_consulta>/sintomas', methods=['POST'])
@role_required(*ROLES_REGISTRO_CLINICO)
def addRegistroSintoma(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_sintoma'):
        return jsonify({'success': False, 'error': 'El síntoma es obligatorio.'}), 400

    try:
        nuevo_id = RegistroSintomaDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_registro_sintoma': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar síntoma de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/registro-sintomas/<int:id_registro_sintoma>', methods=['DELETE'])
@role_required(*ROLES_REGISTRO_CLINICO)
def deleteRegistroSintoma(id_registro_sintoma):
    try:
        if RegistroSintomaDao().desactivar(id_registro_sintoma, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar síntoma de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================================================
# PROCEDIMIENTOS
# ============================================================================
@registroclinicoapi.route('/consultas/<int:id_consulta>/procedimientos', methods=['GET'])
@role_required(*ROLES_REGISTRO_CLINICO)
def getRegistroProcedimientos(id_consulta):
    try:
        data = RegistroProcedimientoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener procedimientos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/consultas/<int:id_consulta>/procedimientos', methods=['POST'])
@role_required(*ROLES_REGISTRO_CLINICO)
def addRegistroProcedimiento(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_tipo_procedimiento'):
        return jsonify({'success': False, 'error': 'El tipo de procedimiento es obligatorio.'}), 400

    try:
        nuevo_id = RegistroProcedimientoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_registro_procedimiento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar procedimiento de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/registro-procedimientos/<int:id_registro_procedimiento>', methods=['DELETE'])
@role_required(*ROLES_REGISTRO_CLINICO)
def deleteRegistroProcedimiento(id_registro_procedimiento):
    try:
        if RegistroProcedimientoDao().desactivar(id_registro_procedimiento, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar procedimiento de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================================================
# INSUMOS (descuenta/repone stock del catálogo `insumos`)
# ============================================================================
@registroclinicoapi.route('/consultas/<int:id_consulta>/insumos', methods=['GET'])
@role_required(*ROLES_REGISTRO_CLINICO)
def getRegistroInsumos(id_consulta):
    try:
        data = RegistroInsumoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener insumos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/consultas/<int:id_consulta>/insumos', methods=['POST'])
@role_required(*ROLES_REGISTRO_CLINICO)
def addRegistroInsumo(id_consulta):
    data = request.get_json() or {}
    if not data.get('id_insumo'):
        return jsonify({'success': False, 'error': 'El insumo es obligatorio.'}), 400
    try:
        cantidad = float(data.get('registro_cantidad') or 0)
    except (TypeError, ValueError):
        cantidad = 0
    if cantidad <= 0:
        return jsonify({'success': False, 'error': 'La cantidad debe ser mayor a cero.'}), 400
    data['registro_cantidad'] = cantidad

    try:
        nuevo_id = RegistroInsumoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_registro_insumo': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar insumo de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@registroclinicoapi.route('/registro-insumos/<int:id_registro_insumo>', methods=['DELETE'])
@role_required(*ROLES_REGISTRO_CLINICO)
def deleteRegistroInsumo(id_registro_insumo):
    try:
        if RegistroInsumoDao().desactivar(id_registro_insumo, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar insumo de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
