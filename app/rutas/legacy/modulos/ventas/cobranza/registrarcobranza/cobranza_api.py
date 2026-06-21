from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.cobranza.CobranzaDao import CobranzaDao

cobranza_api = Blueprint('cobranza_api', __name__)

@cobranza_api.route('/cobranzas', methods=['GET'])
def getAllCobranzas():
    """Obtiene todas las cobranzas"""
    dao = CobranzaDao()
    
    try:
        cobranzas = dao.getCobranzas()
        return jsonify({'success': True, 'data': cobranzas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las cobranzas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cobranza_api.route('/cobranzas/<int:id_cobranza>', methods=['GET'])
def getCobranza(id_cobranza):
    """Obtiene una cobranza específica por su ID con su detalle"""
    dao = CobranzaDao()
    
    try:
        cobranza = dao.getCobranzaById(id_cobranza)
        
        if cobranza:
            # Obtener detalle
            detalle = dao.getCobranzaDetalle(id_cobranza)
            cobranza['detalle'] = detalle
            
            return jsonify({'success': True, 'data': cobranza, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la cobranza.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la cobranza: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@cobranza_api.route('/cobranzas', methods=['POST'])
def addCobranza():
    """Crea una nueva cobranza"""
    data = request.get_json()
    dao = CobranzaDao()
    
    campos_requeridos = ['id_cuenta_cobrar', 'id_factura', 'id_caja', 'id_forma_cobro', 'monto_cobrado']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        cobranza_id = dao.guardarCobranza(
            id_cuenta_cobrar=data['id_cuenta_cobrar'],
            id_factura=data['id_factura'],
            id_caja=data['id_caja'],
            id_forma_cobro=data['id_forma_cobro'],
            monto_cobrado=int(data['monto_cobrado']),
            observaciones=data.get('observaciones'),
            est_cobranza=data.get('est_cobranza', 'REGISTRADA'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if cobranza_id:
            # Guardar detalles si existen
            detalles = data.get('detalles', [])
            for detalle in detalles:
                dao.guardarCobranzaDetalle(
                    id_cobranza=cobranza_id,
                    id_forma_cobro=detalle.get('id_forma_cobro'),
                    monto_cobrado=int(detalle.get('monto_cobrado', 0)),
                    id_marca_tarjeta=detalle.get('id_marca_tarjeta'),
                    id_entidad_adherida=detalle.get('id_entidad_adherida'),
                    id_entidad_emisora=detalle.get('id_entidad_emisora'),
                    numero_cheque=detalle.get('numero_cheque'),
                    numero_tarjeta=detalle.get('numero_tarjeta'),
                    numero_cuotas=detalle.get('numero_cuotas', 1),
                    observaciones=detalle.get('observaciones')
                )
            
            return jsonify({
                'success': True,
                'data': {'id_cobranza': cobranza_id, 'mensaje': 'Cobranza registrada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar la cobranza.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear cobranza: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cobranza_api.route('/cobranzas/<int:id_cobranza>/detalle', methods=['POST'])
def addCobranzaDetalle(id_cobranza):
    """Agrega un detalle a una cobranza"""
    data = request.get_json()
    dao = CobranzaDao()
    
    campos_requeridos = ['id_forma_cobro', 'monto_cobrado']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarCobranzaDetalle(
            id_cobranza=id_cobranza,
            id_forma_cobro=data['id_forma_cobro'],
            monto_cobrado=int(data['monto_cobrado']),
            id_marca_tarjeta=data.get('id_marca_tarjeta'),
            id_entidad_adherida=data.get('id_entidad_adherida'),
            id_entidad_emisora=data.get('id_entidad_emisora'),
            numero_cheque=data.get('numero_cheque'),
            numero_tarjeta=data.get('numero_tarjeta'),
            numero_cuotas=data.get('numero_cuotas', 1),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_cobranza_detalle': detalle_id, 'mensaje': 'Detalle agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el detalle.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de cobranza: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cobranza_api.route('/cobranzas/<int:id_cobranza>', methods=['PUT'])
def updateCobranza(id_cobranza):
    """Actualiza una cobranza existente"""
    data = request.get_json()
    dao = CobranzaDao()
    
    try:
        resultado = dao.updateCobranza(
            id_cobranza=id_cobranza,
            observaciones=data.get('observaciones'),
            est_cobranza=data.get('est_cobranza'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Cobranza actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la cobranza.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar cobranza: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cobranza_api.route('/cobranzas/<int:id_cobranza>/anular', methods=['POST'])
def anularCobranza(id_cobranza):
    """Anula una cobranza y revierte el pago"""
    data = request.get_json()
    dao = CobranzaDao()
    
    motivo = data.get('motivo_anulacion', 'Sin motivo especificado')
    
    try:
        resultado = dao.anularCobranza(
            id_cobranza=id_cobranza,
            motivo_anulacion=motivo,
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Cobranza anulada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular la cobranza.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al anular cobranza: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@cobranza_api.route('/cobranzas/cuenta/<int:id_cuenta_cobrar>', methods=['GET'])
def getCobranzasPorCuenta(id_cuenta_cobrar):
    """Obtiene todas las cobranzas de una cuenta a cobrar"""
    dao = CobranzaDao()
    
    try:
        cobranzas = dao.getCobranzasPorCuenta(id_cuenta_cobrar)
        return jsonify({'success': True, 'data': cobranzas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cobranzas de la cuenta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















