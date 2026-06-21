from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.nota_debito.NotaDebitoDao import NotaDebitoDao

nota_debito_api = Blueprint('nota_debito_api', __name__)

@nota_debito_api.route('/notas_debito', methods=['GET'])
def getAllNotasDebito():
    """Obtiene todas las notas de débito"""
    dao = NotaDebitoDao()
    
    try:
        notas = dao.getNotasDebito()
        return jsonify({'success': True, 'data': notas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las notas de débito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@nota_debito_api.route('/notas_debito/<int:id_nota_debito>', methods=['GET'])
def getNotaDebito(id_nota_debito):
    """Obtiene una nota de débito específica por su ID con su detalle"""
    dao = NotaDebitoDao()
    
    try:
        nota = dao.getNotaDebitoById(id_nota_debito)
        
        if nota:
            # Obtener detalle
            detalle = dao.getNotaDebitoDetalle(id_nota_debito)
            nota['detalle'] = detalle
            
            return jsonify({'success': True, 'data': nota, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la nota de débito.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la nota de débito: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@nota_debito_api.route('/notas_debito', methods=['POST'])
def addNotaDebito():
    """Crea una nueva nota de débito"""
    data = request.get_json()
    dao = NotaDebitoDao()
    
    campos_requeridos = ['id_factura', 'id_tipo_comprobante', 'motivo_nota_debito', 'monto_total']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        nota_id = dao.guardarNotaDebito(
            id_factura=data['id_factura'],
            id_tipo_comprobante=data['id_tipo_comprobante'],
            motivo_nota_debito=data['motivo_nota_debito'],
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
                dao.guardarNotaDebitoDetalle(
                    id_nota_debito=nota_id,
                    item_descripcion=detalle.get('item_descripcion'),
                    item_cantidad=detalle.get('item_cantidad', 1),
                    item_precio_unitario=int(detalle.get('item_precio_unitario', 0)),
                    monto_total=int(detalle.get('monto_total', 0)),
                    id_factura_detalle=detalle.get('id_factura_detalle')
                )
            
            return jsonify({
                'success': True,
                'data': {'id_nota_debito': nota_id, 'mensaje': 'Nota de débito registrada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar la nota de débito.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear nota de débito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_debito_api.route('/notas_debito/<int:id_nota_debito>/detalle', methods=['POST'])
def addNotaDebitoDetalle(id_nota_debito):
    """Agrega un detalle a una nota de débito"""
    data = request.get_json()
    dao = NotaDebitoDao()
    
    campos_requeridos = ['item_descripcion', 'monto_total']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarNotaDebitoDetalle(
            id_nota_debito=id_nota_debito,
            item_descripcion=data['item_descripcion'],
            item_cantidad=data.get('item_cantidad', 1),
            item_precio_unitario=int(data.get('item_precio_unitario', 0)),
            monto_total=int(data['monto_total']),
            id_factura_detalle=data.get('id_factura_detalle')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_nota_debito_detalle': detalle_id, 'mensaje': 'Detalle agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el detalle.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de nota de débito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_debito_api.route('/notas_debito/<int:id_nota_debito>', methods=['PUT'])
def updateNotaDebito(id_nota_debito):
    """Actualiza una nota de débito existente"""
    data = request.get_json()
    dao = NotaDebitoDao()
    
    try:
        resultado = dao.updateNotaDebito(
            id_nota_debito=id_nota_debito,
            motivo_nota_debito=data.get('motivo_nota_debito'),
            observaciones=data.get('observaciones'),
            est_nota_debito=data.get('est_nota_debito'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Nota de débito actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la nota de débito.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar nota de débito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_debito_api.route('/notas_debito/<int:id_nota_debito>/anular', methods=['POST'])
def anularNotaDebito(id_nota_debito):
    """Anula una nota de débito"""
    data = request.get_json()
    dao = NotaDebitoDao()
    
    motivo = data.get('motivo_anulacion', 'Sin motivo especificado')
    
    try:
        resultado = dao.anularNotaDebito(
            id_nota_debito=id_nota_debito,
            motivo_anulacion=motivo,
            usuario=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Nota de débito anulada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo anular la nota de débito.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al anular nota de débito: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@nota_debito_api.route('/notas_debito/factura/<int:id_factura>', methods=['GET'])
def getNotasDebitoPorFactura(id_factura):
    """Obtiene todas las notas de débito de una factura"""
    dao = NotaDebitoDao()
    
    try:
        notas = dao.getNotasDebitoPorFactura(id_factura)
        return jsonify({'success': True, 'data': notas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas de débito de la factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















