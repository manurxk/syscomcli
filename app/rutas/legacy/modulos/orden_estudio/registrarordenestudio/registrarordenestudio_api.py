from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.orden_estudio.OrdenEstudioDao import OrdenEstudioDao
from app.conexion.Conexion import Conexion

ordenestudioapi = Blueprint('ordenestudioapi', __name__)


# ============================================
# CRUD BÁSICO DE ÓRDENES DE ESTUDIOS
# ============================================

@ordenestudioapi.route('/ordenes-estudios', methods=['GET'])
def getAllOrdenesEstudios():
    """Obtiene la lista completa de órdenes de estudios activas"""
    dao = OrdenEstudioDao()
    
    try:
        ordenes = dao.getAllOrdenesEstudios()
        return jsonify({'success': True, 'data': ordenes, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las órdenes de estudios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenestudioapi.route('/ordenes-estudios/<int:id_orden_estudio>', methods=['GET'])
def getOrdenEstudio(id_orden_estudio):
    """Obtiene una orden de estudio específica por su ID con su detalle"""
    dao = OrdenEstudioDao()
    
    try:
        orden = dao.getOrdenEstudioById(id_orden_estudio)
        
        if orden:
            # Obtener detalle
            detalle = dao.getOrdenEstudioDetalle(id_orden_estudio)
            orden['detalle'] = detalle
            
            return jsonify({'success': True, 'data': orden, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la orden de estudio.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenestudioapi.route('/ordenes-estudios', methods=['POST'])
def addOrdenEstudio():
    """Crea una nueva orden de estudio"""
    data = request.get_json()
    dao = OrdenEstudioDao()
    
    # Validar campos obligatorios
    campos_requeridos = ['id_consulta', 'id_paciente', 'id_profesional', 'orden_fecha', 'orden_tipo']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400
    
    try:
        orden_id = dao.guardarOrdenEstudio(
            id_consulta=data['id_consulta'],
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            orden_fecha=data['orden_fecha'],
            orden_tipo=data['orden_tipo'],
            orden_estado=data.get('orden_estado', 'PENDIENTE'),
            orden_observaciones=data.get('orden_observaciones'),
            orden_indicaciones=data.get('orden_indicaciones'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if orden_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_orden_estudio': orden_id,
                    'mensaje': 'Orden de estudio creada exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la orden de estudio.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@ordenestudioapi.route('/ordenes-estudios/<int:id_orden_estudio>/detalle', methods=['POST'])
def addOrdenEstudioDetalle(id_orden_estudio):
    """Agrega un estudio al detalle de una orden"""
    data = request.get_json()
    dao = OrdenEstudioDao()
    
    campos_requeridos = ['des_estudio']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarOrdenEstudioDetalle(
            id_orden_estudio=id_orden_estudio,
            des_estudio=data['des_estudio'],
            id_tipo_estudio=data.get('id_tipo_estudio'),
            id_tipo_analisis=data.get('id_tipo_analisis'),
            estudio_estado=data.get('estudio_estado', 'PENDIENTE'),
            estudio_resultado=data.get('estudio_resultado'),
            estudio_fecha_realizacion=data.get('estudio_fecha_realizacion'),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_orden_detalle': detalle_id, 'mensaje': 'Estudio agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el estudio a la orden.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@ordenestudioapi.route('/ordenes-estudios/<int:id_orden_estudio>', methods=['PUT'])
def updateOrdenEstudio(id_orden_estudio):
    """Actualiza una orden de estudio existente"""
    data = request.get_json()
    dao = OrdenEstudioDao()
    
    # Validar que existe la orden
    orden_existente = dao.getOrdenEstudioById(id_orden_estudio)
    if not orden_existente:
        return jsonify({'success': False, 'error': 'No se encontró la orden de estudio.'}), 404
    
    try:
        resultado = dao.updateOrdenEstudio(
            id_orden_estudio=id_orden_estudio,
            orden_estado=data.get('orden_estado'),
            orden_observaciones=data.get('orden_observaciones'),
            orden_indicaciones=data.get('orden_indicaciones'),
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_orden_estudio': id_orden_estudio, 'mensaje': 'Orden de estudio actualizada exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la orden de estudio.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@ordenestudioapi.route('/ordenes-estudios/<int:id_orden_estudio>/detalle/<int:id_detalle>', methods=['DELETE'])
def deleteOrdenEstudioDetalle(id_orden_estudio, id_detalle):
    """Elimina un estudio del detalle de una orden"""
    dao = OrdenEstudioDao()
    
    try:
        # Verificar que la orden existe
        orden = dao.getOrdenEstudioById(id_orden_estudio)
        if not orden:
            return jsonify({'success': False, 'error': 'No se encontró la orden de estudio.'}), 404
        
        detalle = dao.getOrdenEstudioDetalle(id_orden_estudio)
        item_existe = any(d['id_orden_detalle'] == id_detalle for d in detalle)
        
        if not item_existe:
            return jsonify({'success': False, 'error': 'No se encontró el estudio.'}), 404
        
        # Eliminar el estudio (DELETE físico ya que es detalle)
        deleteSQL = "DELETE FROM orden_estudio_detalle WHERE id_orden_detalle = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_detalle,))
            con.commit()
            
            return jsonify({
                'success': True,
                'mensaje': 'Estudio eliminado correctamente.',
                'error': None
            }), 200
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar estudio: {str(e)}")
            return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenestudioapi.route('/ordenes-estudios/<int:id_orden_estudio>', methods=['DELETE'])
def deleteOrdenEstudio(id_orden_estudio):
    """Elimina lógicamente una orden de estudio"""
    dao = OrdenEstudioDao()
    
    try:
        if dao.deleteOrdenEstudio(id_orden_estudio):
            return jsonify({
                'success': True,
                'mensaje': f'Orden de estudio con ID {id_orden_estudio} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la orden de estudio o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar orden de estudio: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

