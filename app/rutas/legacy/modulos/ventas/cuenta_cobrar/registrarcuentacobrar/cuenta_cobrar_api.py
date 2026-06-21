from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao

cuenta_cobrar_api = Blueprint('cuenta_cobrar_api', __name__)

@cuenta_cobrar_api.route('/cuentas_cobrar', methods=['GET'])
def getAllCuentasCobrar():
    """Obtiene todas las cuentas a cobrar"""
    dao = CuentaCobrarDao()
    
    try:
        # Actualizar estados vencidas antes de obtener
        dao.actualizarEstadosVencidas()
        
        cuentas = dao.getCuentasCobrar()
        return jsonify({'success': True, 'data': cuentas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las cuentas a cobrar: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/<int:id_cuenta_cobrar>', methods=['GET'])
def getCuentaCobrar(id_cuenta_cobrar):
    """Obtiene una cuenta a cobrar específica por su ID con historial de cobranzas"""
    dao = CuentaCobrarDao()
    
    try:
        cuenta = dao.getCuentaCobrarById(id_cuenta_cobrar)
        
        if cuenta:
            # Obtener historial de cobranzas
            historial = dao.getHistorialCobranzas(id_cuenta_cobrar)
            cuenta['historial_cobranzas'] = historial
            
            return jsonify({'success': True, 'data': cuenta, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la cuenta a cobrar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la cuenta a cobrar: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/paciente/<int:id_paciente>', methods=['GET'])
def getCuentasCobrarPorPaciente(id_paciente):
    """Obtiene todas las cuentas a cobrar de un paciente"""
    dao = CuentaCobrarDao()
    
    try:
        cuentas = dao.getCuentasCobrarPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': cuentas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuentas a cobrar del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/estado/<estado>', methods=['GET'])
def getCuentasCobrarPorEstado(estado):
    """Obtiene cuentas a cobrar filtradas por estado"""
    dao = CuentaCobrarDao()
    
    try:
        cuentas = dao.getCuentasCobrarPorEstado(estado)
        return jsonify({'success': True, 'data': cuentas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuentas a cobrar por estado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/vencidas', methods=['GET'])
def getCuentasVencidas():
    """Obtiene todas las cuentas a cobrar vencidas"""
    dao = CuentaCobrarDao()
    
    try:
        cuentas = dao.getCuentasVencidas()
        return jsonify({'success': True, 'data': cuentas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cuentas vencidas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/<int:id_cuenta_cobrar>', methods=['PUT'])
def updateCuentaCobrar(id_cuenta_cobrar):
    """Actualiza una cuenta a cobrar existente"""
    data = request.get_json()
    dao = CuentaCobrarDao()
    
    try:
        resultado = dao.updateCuentaCobrar(
            id_cuenta_cobrar=id_cuenta_cobrar,
            fecha_vencimiento=data.get('fecha_vencimiento'),
            observaciones=data.get('observaciones'),
            numero_cuotas=data.get('numero_cuotas'),
            cuota_actual=data.get('cuota_actual'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Cuenta a cobrar actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la cuenta a cobrar.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar cuenta a cobrar: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/<int:id_cuenta_cobrar>/actualizar-estado', methods=['POST'])
def actualizarEstadoCuenta(id_cuenta_cobrar):
    """Actualiza el estado de una cuenta a cobrar"""
    dao = CuentaCobrarDao()
    
    try:
        resultado = dao.actualizarEstadoCuenta(id_cuenta_cobrar)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Estado actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el estado.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar estado: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cuenta_cobrar_api.route('/cuentas_cobrar/actualizar-vencidas', methods=['POST'])
def actualizarEstadosVencidas():
    """Actualiza el estado de todas las cuentas vencidas"""
    dao = CuentaCobrarDao()
    
    try:
        cantidad = dao.actualizarEstadosVencidas()
        return jsonify({
            'success': True,
            'data': {'cantidad_actualizadas': cantidad},
            'mensaje': f'Se actualizaron {cantidad} cuentas vencidas',
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar estados vencidas: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


















