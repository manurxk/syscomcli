from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao

apertura_cierre_caja_api = Blueprint('apertura_cierre_caja_api', __name__)

@apertura_cierre_caja_api.route('/aperturas_cierres', methods=['GET'])
def getAllAperturasCierres():
    """Obtiene todas las aperturas y cierres de caja"""
    dao = AperturaCierreCajaDao()
    
    try:
        aperturas = dao.getAperturasCierres()
        return jsonify({'success': True, 'data': aperturas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las aperturas/cierres: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/<int:id_apertura_cierre>', methods=['GET'])
def getAperturaCierre(id_apertura_cierre):
    """Obtiene una apertura/cierre específica por su ID"""
    dao = AperturaCierreCajaDao()
    
    try:
        apertura = dao.getAperturaCierreById(id_apertura_cierre)
        
        if apertura:
            return jsonify({'success': True, 'data': apertura, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la apertura/cierre.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la apertura/cierre: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/caja/<int:id_caja>/activa', methods=['GET'])
def getAperturaActiva(id_caja):
    """Obtiene la apertura activa de una caja"""
    dao = AperturaCierreCajaDao()
    
    try:
        apertura = dao.getAperturaActivaPorCaja(id_caja)
        
        if apertura:
            # Calcular saldo esperado
            saldo_esperado = dao.calcularSaldoEsperado(id_caja)
            apertura['saldo_esperado'] = saldo_esperado
            
            return jsonify({'success': True, 'data': apertura, 'error': None}), 200
        else:
            return jsonify({'success': False, 'data': None, 'error': 'No hay apertura activa para esta caja.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener apertura activa: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/caja/<int:id_caja>', methods=['GET'])
def getAperturasCierresPorCaja(id_caja):
    """Obtiene todas las aperturas/cierres de una caja"""
    dao = AperturaCierreCajaDao()
    
    try:
        aperturas = dao.getAperturasCierresPorCaja(id_caja)
        return jsonify({'success': True, 'data': aperturas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener aperturas/cierres de la caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/apertura', methods=['POST'])
def addApertura():
    """Registra una nueva apertura de caja"""
    data = request.get_json()
    dao = AperturaCierreCajaDao()
    
    campos_requeridos = ['id_caja', 'id_usuario']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        apertura_id = dao.guardarApertura(
            id_caja=data['id_caja'],
            id_usuario=data['id_usuario'],
            saldo_inicial=int(data.get('saldo_inicial', 0)),
            observaciones=data.get('observaciones'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if apertura_id:
            return jsonify({
                'success': True,
                'data': {'id_apertura_cierre': apertura_id, 'mensaje': 'Apertura registrada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar la apertura. Verifique que no haya una apertura activa para esta caja.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear apertura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/cierre', methods=['POST'])
def addCierre():
    """Registra un nuevo cierre de caja"""
    data = request.get_json()
    dao = AperturaCierreCajaDao()
    
    campos_requeridos = ['id_caja', 'id_usuario', 'saldo_final']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        cierre_id = dao.guardarCierre(
            id_caja=data['id_caja'],
            id_usuario=data['id_usuario'],
            saldo_final=int(data['saldo_final']),
            monto_efectivo=int(data.get('monto_efectivo', 0)),
            monto_cheques=int(data.get('monto_cheques', 0)),
            monto_tarjetas=int(data.get('monto_tarjetas', 0)),
            monto_transferencias=int(data.get('monto_transferencias', 0)),
            observaciones=data.get('observaciones'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if cierre_id:
            return jsonify({
                'success': True,
                'data': {'id_apertura_cierre': cierre_id, 'mensaje': 'Cierre registrado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar el cierre. Verifique que haya una apertura activa para esta caja.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear cierre: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/<int:id_apertura_cierre>', methods=['PUT'])
def updateAperturaCierre(id_apertura_cierre):
    """Actualiza una apertura/cierre existente"""
    data = request.get_json()
    dao = AperturaCierreCajaDao()
    
    try:
        resultado = dao.updateAperturaCierre(
            id_apertura_cierre=id_apertura_cierre,
            observaciones=data.get('observaciones'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Apertura/Cierre actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la apertura/cierre.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar apertura/cierre: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/caja/<int:id_caja>/saldo-esperado', methods=['GET'])
def getSaldoEsperado(id_caja):
    """Calcula el saldo esperado de una caja"""
    dao = AperturaCierreCajaDao()
    
    try:
        saldo = dao.calcularSaldoEsperado(id_caja)
        
        if saldo:
            return jsonify({'success': True, 'data': saldo, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo calcular el saldo esperado.'}), 500
    except Exception as e:
        app.logger.error(f"Error al calcular saldo esperado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@apertura_cierre_caja_api.route('/aperturas_cierres/caja/<int:id_caja>/historial', methods=['GET'])
def getHistorialCaja(id_caja):
    """Obtiene el historial de una caja"""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    dao = AperturaCierreCajaDao()
    
    try:
        historial = dao.getHistorialCaja(id_caja, fecha_desde, fecha_hasta)
        return jsonify({'success': True, 'data': historial, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener historial de caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















