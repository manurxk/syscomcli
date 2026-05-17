from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.recaudacion.RecaudacionDao import RecaudacionDao

recaudacion_api = Blueprint('recaudacion_api', __name__)

@recaudacion_api.route('/recaudaciones', methods=['GET'])
def getAllRecaudaciones():
    """Obtiene todas las recaudaciones"""
    dao = RecaudacionDao()
    
    try:
        recaudaciones = dao.getRecaudaciones()
        return jsonify({'success': True, 'data': recaudaciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las recaudaciones: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacion_api.route('/recaudaciones/<int:id_recaudacion>', methods=['GET'])
def getRecaudacion(id_recaudacion):
    """Obtiene una recaudación específica por su ID"""
    dao = RecaudacionDao()
    
    try:
        recaudacion = dao.getRecaudacionById(id_recaudacion)
        
        if recaudacion:
            return jsonify({'success': True, 'data': recaudacion, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la recaudación.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la recaudación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacion_api.route('/recaudaciones/caja/<int:id_caja>', methods=['GET'])
def getRecaudacionesPorCaja(id_caja):
    """Obtiene todas las recaudaciones de una caja"""
    dao = RecaudacionDao()
    
    try:
        recaudaciones = dao.getRecaudacionesPorCaja(id_caja)
        return jsonify({'success': True, 'data': recaudaciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recaudaciones de la caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacion_api.route('/recaudaciones/pendientes', methods=['GET'])
def getRecaudacionesPendientes():
    """Obtiene todas las recaudaciones pendientes de depositar"""
    dao = RecaudacionDao()
    
    try:
        recaudaciones = dao.getRecaudacionesPendientes()
        return jsonify({'success': True, 'data': recaudaciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recaudaciones pendientes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recaudacion_api.route('/recaudaciones', methods=['POST'])
def addRecaudacion():
    """Crea una nueva recaudación"""
    data = request.get_json()
    dao = RecaudacionDao()
    
    campos_requeridos = ['id_caja', 'id_deposito', 'id_usuario', 'monto_total']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        recaudacion_id = dao.guardarRecaudacion(
            id_caja=data['id_caja'],
            id_deposito=data['id_deposito'],
            id_usuario=data['id_usuario'],
            monto_total=int(data['monto_total']),
            monto_efectivo=int(data.get('monto_efectivo', 0)),
            monto_cheques=int(data.get('monto_cheques', 0)),
            monto_tarjetas=int(data.get('monto_tarjetas', 0)),
            fecha_deposito=data.get('fecha_deposito'),
            observaciones=data.get('observaciones'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if recaudacion_id:
            return jsonify({
                'success': True,
                'data': {'id_recaudacion': recaudacion_id, 'mensaje': 'Recaudación registrada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar la recaudación.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear recaudación: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recaudacion_api.route('/recaudaciones/<int:id_recaudacion>', methods=['PUT'])
def updateRecaudacion(id_recaudacion):
    """Actualiza una recaudación existente"""
    data = request.get_json()
    dao = RecaudacionDao()
    
    try:
        resultado = dao.updateRecaudacion(
            id_recaudacion=id_recaudacion,
            fecha_deposito=data.get('fecha_deposito'),
            monto_total=data.get('monto_total'),
            monto_efectivo=data.get('monto_efectivo'),
            monto_cheques=data.get('monto_cheques'),
            monto_tarjetas=data.get('monto_tarjetas'),
            observaciones=data.get('observaciones'),
            est_recaudacion=data.get('est_recaudacion'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Recaudación actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la recaudación.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar recaudación: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recaudacion_api.route('/recaudaciones/<int:id_recaudacion>/depositar', methods=['POST'])
def marcarComoDepositada(id_recaudacion):
    """Marca una recaudación como depositada"""
    data = request.get_json()
    dao = RecaudacionDao()
    
    fecha_deposito = data.get('fecha_deposito')
    
    if not fecha_deposito:
        return jsonify({
            'success': False,
            'error': 'La fecha de depósito es obligatoria.'
        }), 400
    
    try:
        resultado = dao.marcarComoDepositada(
            id_recaudacion=id_recaudacion,
            fecha_deposito=fecha_deposito,
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Recaudación marcada como depositada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo marcar como depositada.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al marcar como depositada: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recaudacion_api.route('/recaudaciones/<int:id_recaudacion>/anular', methods=['POST'])
def anularRecaudacion(id_recaudacion):
    """Anula una recaudación"""
    data = request.get_json()
    dao = RecaudacionDao()
    
    motivo = data.get('motivo_anulacion', 'Sin motivo especificado')
    
    try:
        resultado = dao.anularRecaudacion(
            id_recaudacion=id_recaudacion,
            motivo_anulacion=motivo,
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Recaudación anulada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular la recaudación.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al anular recaudación: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


















