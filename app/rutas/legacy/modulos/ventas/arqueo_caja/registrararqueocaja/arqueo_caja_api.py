from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.arqueo_caja.ArqueoCajaDao import ArqueoCajaDao

arqueo_caja_api = Blueprint('arqueo_caja_api', __name__)

@arqueo_caja_api.route('/arqueos_caja', methods=['GET'])
def getAllArqueos():
    """Obtiene todos los arqueos de caja"""
    dao = ArqueoCajaDao()
    
    try:
        arqueos = dao.getArqueos()
        return jsonify({'success': True, 'data': arqueos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los arqueos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueo_caja_api.route('/arqueos_caja/<int:id_arqueo>', methods=['GET'])
def getArqueo(id_arqueo):
    """Obtiene un arqueo específico por su ID"""
    dao = ArqueoCajaDao()
    
    try:
        arqueo = dao.getArqueoById(id_arqueo)
        
        if arqueo:
            return jsonify({'success': True, 'data': arqueo, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el arqueo.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el arqueo: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueo_caja_api.route('/arqueos_caja/caja/<int:id_caja>', methods=['GET'])
def getArqueosPorCaja(id_caja):
    """Obtiene todos los arqueos de una caja"""
    dao = ArqueoCajaDao()
    
    try:
        arqueos = dao.getArqueosPorCaja(id_caja)
        return jsonify({'success': True, 'data': arqueos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener arqueos de la caja: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueo_caja_api.route('/arqueos_caja/apertura_cierre/<int:id_apertura_cierre>', methods=['GET'])
def getArqueosPorAperturaCierre(id_apertura_cierre):
    """Obtiene todos los arqueos de una apertura/cierre"""
    dao = ArqueoCajaDao()
    
    try:
        arqueos = dao.getArqueosPorAperturaCierre(id_apertura_cierre)
        return jsonify({'success': True, 'data': arqueos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener arqueos de la apertura/cierre: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@arqueo_caja_api.route('/arqueos_caja', methods=['POST'])
def addArqueo():
    """Crea un nuevo arqueo de caja"""
    data = request.get_json()
    dao = ArqueoCajaDao()
    
    campos_requeridos = ['id_apertura_cierre', 'id_caja', 'monto_real']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        arqueo_id = dao.guardarArqueo(
            id_apertura_cierre=data['id_apertura_cierre'],
            id_caja=data['id_caja'],
            monto_real=int(data['monto_real']),
            observaciones=data.get('observaciones'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if arqueo_id:
            return jsonify({
                'success': True,
                'data': {'id_arqueo': arqueo_id, 'mensaje': 'Arqueo registrado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar el arqueo.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear arqueo: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@arqueo_caja_api.route('/arqueos_caja/<int:id_arqueo>', methods=['PUT'])
def updateArqueo(id_arqueo):
    """Actualiza un arqueo existente"""
    data = request.get_json()
    dao = ArqueoCajaDao()
    
    try:
        resultado = dao.updateArqueo(
            id_arqueo=id_arqueo,
            monto_real=data.get('monto_real'),
            observaciones=data.get('observaciones'),
            est_arqueo=data.get('est_arqueo'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Arqueo actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el arqueo.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar arqueo: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@arqueo_caja_api.route('/arqueos_caja/<int:id_arqueo>/conciliar', methods=['POST'])
def conciliarArqueo(id_arqueo):
    """Marca un arqueo como conciliado"""
    data = request.get_json()
    dao = ArqueoCajaDao()
    
    try:
        resultado = dao.conciliarArqueo(
            id_arqueo=id_arqueo,
            observaciones_conciliacion=data.get('observaciones'),
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Arqueo conciliado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo conciliar el arqueo.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al conciliar arqueo: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@arqueo_caja_api.route('/arqueos_caja/apertura_cierre/<int:id_apertura_cierre>/calcular', methods=['GET'])
def calcularMontoEsperado(id_apertura_cierre):
    """Calcula el monto esperado para un arqueo"""
    id_caja = request.args.get('id_caja')
    
    if not id_caja:
        return jsonify({
            'success': False,
            'error': 'El parámetro id_caja es obligatorio.'
        }), 400
    
    dao = ArqueoCajaDao()
    
    try:
        monto_esperado = dao.calcularMontoEsperado(int(id_apertura_cierre), int(id_caja))
        
        if monto_esperado is not None:
            return jsonify({
                'success': True,
                'data': {'monto_esperado': monto_esperado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo calcular el monto esperado.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al calcular monto esperado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















