from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.nota_credito.NotaCreditoDao import NotaCreditoDao

nota_credito_api = Blueprint('nota_credito_api', __name__)

@nota_credito_api.route('/notas_credito', methods=['GET'])
def getAllNotasCredito():
    """Obtiene todas las notas de crédito"""
    dao = NotaCreditoDao()
    
    try:
        notas = dao.getNotasCredito()
        return jsonify({'success': True, 'data': notas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las notas de crédito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@nota_credito_api.route('/notas_credito/<int:id_nota_credito>', methods=['GET'])
def getNotaCredito(id_nota_credito):
    """Obtiene una nota de crédito específica por su ID con su detalle"""
    dao = NotaCreditoDao()
    
    try:
        nota = dao.getNotaCreditoById(id_nota_credito)
        
        if nota:
            # Obtener detalle
            detalle = dao.getNotaCreditoDetalle(id_nota_credito)
            nota['detalle'] = detalle
            
            return jsonify({'success': True, 'data': nota, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la nota de crédito.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la nota de crédito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@nota_credito_api.route('/notas_credito', methods=['POST'])
def addNotaCredito():
    """Crea una nueva nota de crédito"""
    data = request.get_json()
    dao = NotaCreditoDao()
    
    campos_requeridos = ['id_factura', 'id_tipo_comprobante', 'motivo_nota_credito', 'monto_total']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        nota_id = dao.guardarNotaCredito(
            id_factura=data['id_factura'],
            id_tipo_comprobante=data['id_tipo_comprobante'],
            motivo_nota_credito=data['motivo_nota_credito'],
            monto_total=int(data['monto_total']),
            codigo_sifen=data.get('codigo_sifen'),
            numero_timbrado=data.get('numero_timbrado'),
            observaciones=data.get('observaciones'),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if nota_id:
            # Guardar detalles si existen
            detalles = data.get('detalles', [])
            for detalle in detalles:
                dao.guardarNotaCreditoDetalle(
                    id_nota_credito=nota_id,
                    item_descripcion=detalle.get('item_descripcion'),
                    item_cantidad=detalle.get('item_cantidad', 1),
                    item_precio_unitario=int(detalle.get('item_precio_unitario', 0)),
                    monto_total=int(detalle.get('monto_total', 0)),
                    id_factura_detalle=detalle.get('id_factura_detalle')
                )
            
            return jsonify({
                'success': True,
                'data': {'id_nota_credito': nota_id, 'mensaje': 'Nota de crédito registrada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar la nota de crédito.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear nota de crédito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_credito_api.route('/notas_credito/<int:id_nota_credito>/detalle', methods=['POST'])
def addNotaCreditoDetalle(id_nota_credito):
    """Agrega un detalle a una nota de crédito"""
    data = request.get_json()
    dao = NotaCreditoDao()
    
    campos_requeridos = ['item_descripcion', 'monto_total']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarNotaCreditoDetalle(
            id_nota_credito=id_nota_credito,
            item_descripcion=data['item_descripcion'],
            item_cantidad=data.get('item_cantidad', 1),
            item_precio_unitario=int(data.get('item_precio_unitario', 0)),
            monto_total=int(data['monto_total']),
            id_factura_detalle=data.get('id_factura_detalle')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_nota_credito_detalle': detalle_id, 'mensaje': 'Detalle agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el detalle.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de nota de crédito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_credito_api.route('/notas_credito/<int:id_nota_credito>', methods=['PUT'])
def updateNotaCredito(id_nota_credito):
    """Actualiza una nota de crédito existente"""
    data = request.get_json()
    dao = NotaCreditoDao()
    
    try:
        resultado = dao.updateNotaCredito(
            id_nota_credito=id_nota_credito,
            motivo_nota_credito=data.get('motivo_nota_credito'),
            observaciones=data.get('observaciones'),
            est_nota_credito=data.get('est_nota_credito'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Nota de crédito actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la nota de crédito.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar nota de crédito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_credito_api.route('/notas_credito/<int:id_nota_credito>/anular', methods=['POST'])
def anularNotaCredito(id_nota_credito):
    """Anula una nota de crédito"""
    data = request.get_json()
    dao = NotaCreditoDao()
    
    motivo = data.get('motivo_anulacion', 'Sin motivo especificado')
    
    try:
        resultado = dao.anularNotaCredito(
            id_nota_credito=id_nota_credito,
            motivo_anulacion=motivo,
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Nota de crédito anulada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular la nota de crédito.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al anular nota de crédito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_credito_api.route('/notas_credito/factura/<int:id_factura>', methods=['GET'])
def getNotasCreditoPorFactura(id_factura):
    """Obtiene todas las notas de crédito de una factura"""
    dao = NotaCreditoDao()
    
    try:
        notas = dao.getNotasCreditoPorFactura(id_factura)
        return jsonify({'success': True, 'data': notas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas de crédito de la factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















