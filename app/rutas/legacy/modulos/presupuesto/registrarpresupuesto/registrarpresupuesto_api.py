from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.presupuesto.PresupuestoDao import PresupuestoDao
from app.conexion.Conexion import Conexion

presupuestoapi = Blueprint('presupuestoapi', __name__)


# ============================================
# CRUD BÁSICO DE PRESUPUESTOS
# ============================================

@presupuestoapi.route('/presupuestos', methods=['GET'])
def getAllPresupuestos():
    """Obtiene la lista completa de presupuestos activos"""
    dao = PresupuestoDao()
    
    try:
        presupuestos = dao.getPresupuestos()
        return jsonify({'success': True, 'data': presupuestos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los presupuestos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['GET'])
def getPresupuesto(id_presupuesto):
    """Obtiene un presupuesto específico por su ID con su detalle"""
    dao = PresupuestoDao()
    
    try:
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        
        if presupuesto:
            # Obtener detalle
            detalle = dao.getPresupuestoDetalle(id_presupuesto)
            presupuesto['detalle'] = detalle
            
            return jsonify({'success': True, 'data': presupuesto, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos', methods=['POST'])
def addPresupuesto():
    """Crea un nuevo presupuesto"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    # Validar campos obligatorios
    campos_requeridos = ['id_paciente', 'id_profesional', 'presupuesto_fecha']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400
    
    try:
        presupuesto_id = dao.guardarPresupuesto(
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            presupuesto_fecha=data['presupuesto_fecha'],
            presupuesto_validez_dias=data.get('presupuesto_validez_dias', 30),
            presupuesto_estado=data.get('presupuesto_estado', 'PENDIENTE'),
            id_consulta=data.get('id_consulta'),
            presupuesto_observaciones=data.get('presupuesto_observaciones'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if presupuesto_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_presupuesto': presupuesto_id,
                    'mensaje': 'Presupuesto creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/detalle', methods=['POST'])
def addPresupuestoDetalle(id_presupuesto):
    """Agrega un item al detalle de un presupuesto"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    campos_requeridos = ['des_item', 'precio_unitario']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarPresupuestoDetalle(
            id_presupuesto=id_presupuesto,
            des_item=data['des_item'],
            precio_unitario=int(data['precio_unitario']),  # Convertir a entero (guaraníes)
            cantidad=data.get('cantidad', 1),
            id_tipo_procedimiento=data.get('id_tipo_procedimiento'),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_presupuesto_detalle': detalle_id, 'mensaje': 'Item agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el item al presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/detalle/<int:id_detalle>', methods=['DELETE'])
def deletePresupuestoDetalle(id_presupuesto, id_detalle):
    """Elimina un item del detalle de un presupuesto"""
    dao = PresupuestoDao()
    
    try:
        # Verificar que el detalle existe y pertenece al presupuesto
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        if not presupuesto:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
        
        detalle = dao.getPresupuestoDetalle(id_presupuesto)
        item_existe = any(d['id_presupuesto_detalle'] == id_detalle for d in detalle)
        
        if not item_existe:
            return jsonify({'success': False, 'error': 'No se encontró el item.'}), 404
        
        # Eliminar el item (DELETE físico ya que es detalle)
        deleteSQL = "DELETE FROM presupuesto_detalle WHERE id_presupuesto_detalle = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_detalle,))
            con.commit()
            
            # Actualizar totales del presupuesto
            dao._actualizarTotalesPresupuesto(id_presupuesto)
            
            return jsonify({
                'success': True,
                'mensaje': 'Item eliminado correctamente.',
                'error': None
            }), 200
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar item: {str(e)}")
            return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['PUT'])
def updatePresupuesto(id_presupuesto):
    """Actualiza un presupuesto existente"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    # Validar que existe el presupuesto
    presupuesto_existente = dao.getPresupuestoById(id_presupuesto)
    if not presupuesto_existente:
        return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
    
    try:
        resultado = dao.updatePresupuesto(
            id_presupuesto=id_presupuesto,
            presupuesto_estado=data.get('presupuesto_estado'),
            presupuesto_descuento=int(data.get('presupuesto_descuento', 0)) if data.get('presupuesto_descuento') else None,
            presupuesto_observaciones=data.get('presupuesto_observaciones'),
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_presupuesto': id_presupuesto, 'mensaje': 'Presupuesto actualizado exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['DELETE'])
def deletePresupuesto(id_presupuesto):
    """Elimina lógicamente un presupuesto"""
    dao = PresupuestoDao()
    
    try:
        if dao.deletePresupuesto(id_presupuesto):
            return jsonify({
                'success': True,
                'mensaje': f'Presupuesto con ID {id_presupuesto} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el presupuesto o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS DE FILTRADO
# ============================================

@presupuestoapi.route('/presupuestos/paciente/<int:id_paciente>', methods=['GET'])
def getPresupuestosPorPaciente(id_paciente):
    """Obtiene todos los presupuestos de un paciente"""
    dao = PresupuestoDao()
    
    try:
        presupuestos = dao.getPresupuestosPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': presupuestos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener presupuestos del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

