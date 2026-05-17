from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.receta.RecetaDao import RecetaDao
from app.conexion.Conexion import Conexion

recetaapi = Blueprint('recetaapi', __name__)


@recetaapi.route('/recetas', methods=['GET'])
def getAllRecetas():
    """Obtiene la lista completa de recetas activas"""
    dao = RecetaDao()
    try:
        recetas = dao.getRecetas()
        return jsonify({'success': True, 'data': recetas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las recetas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas/<int:id_receta>', methods=['GET'])
def getReceta(id_receta):
    """Obtiene una receta específica con su detalle"""
    dao = RecetaDao()
    try:
        receta = dao.getRecetaById(id_receta)
        if receta:
            detalle = dao.getRecetaDetalle(id_receta)
            receta['detalle'] = detalle
            return jsonify({'success': True, 'data': receta, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la receta.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la receta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas', methods=['POST'])
def addReceta():
    """Crea una nueva receta"""
    data = request.get_json()
    dao = RecetaDao()
    
    campos_requeridos = ['id_consulta', 'id_paciente', 'id_profesional', 'receta_fecha']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        receta_id = dao.guardarReceta(
            id_consulta=data['id_consulta'],
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            receta_fecha=data['receta_fecha'],
            receta_validez_dias=data.get('receta_validez_dias', 30),
            receta_indicaciones_generales=data.get('receta_indicaciones_generales'),
            receta_observaciones=data.get('receta_observaciones'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if receta_id:
            return jsonify({
                'success': True,
                'data': {'id_receta': receta_id, 'mensaje': 'Receta creada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la receta.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar receta: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recetaapi.route('/recetas/<int:id_receta>/detalle', methods=['POST'])
def addRecetaDetalle(id_receta):
    """Agrega un medicamento al detalle de una receta"""
    data = request.get_json()
    dao = RecetaDao()
    
    campos_requeridos = ['id_medicamento', 'medicamento_dosis', 'medicamento_frecuencia', 'medicamento_duracion']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarRecetaDetalle(
            id_receta=id_receta,
            id_medicamento=data['id_medicamento'],
            medicamento_dosis=data['medicamento_dosis'],
            medicamento_frecuencia=data['medicamento_frecuencia'],
            medicamento_duracion=data['medicamento_duracion'],
            medicamento_cantidad=data.get('medicamento_cantidad'),
            medicamento_indicaciones=data.get('medicamento_indicaciones'),
            medicamento_posologia=data.get('medicamento_posologia')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_receta_detalle': detalle_id, 'mensaje': 'Medicamento agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el medicamento a la receta.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de receta: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recetaapi.route('/recetas/<int:id_receta>', methods=['PUT'])
def updateReceta(id_receta):
    """Actualiza una receta existente"""
    data = request.get_json()
    dao = RecetaDao()
    
    if not dao.getRecetaById(id_receta):
        return jsonify({'success': False, 'error': 'No se encontró la receta.'}), 404
    
    try:
        resultado = dao.updateReceta(
            id_receta=id_receta,
            receta_observaciones=data.get('receta_observaciones'),
            receta_indicaciones_generales=data.get('receta_indicaciones_generales'),
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_receta': id_receta, 'mensaje': 'Receta actualizada exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la receta.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar receta: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@recetaapi.route('/recetas/<int:id_receta>', methods=['DELETE'])
def deleteReceta(id_receta):
    """Elimina lógicamente una receta"""
    dao = RecetaDao()
    try:
        if dao.deleteReceta(id_receta):
            return jsonify({
                'success': True,
                'mensaje': f'Receta con ID {id_receta} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la receta o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar receta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas/<int:id_receta>/detalle/<int:id_detalle>', methods=['DELETE'])
def deleteRecetaDetalle(id_receta, id_detalle):
    """Elimina un medicamento del detalle de una receta"""
    dao = RecetaDao()
    
    try:
        # Verificar que la receta existe
        receta = dao.getRecetaById(id_receta)
        if not receta:
            return jsonify({'success': False, 'error': 'No se encontró la receta.'}), 404
        
        detalle = dao.getRecetaDetalle(id_receta)
        item_existe = any(d['id_receta_detalle'] == id_detalle for d in detalle)
        
        if not item_existe:
            return jsonify({'success': False, 'error': 'No se encontró el medicamento.'}), 404
        
        # Eliminar el medicamento (DELETE físico ya que es detalle)
        deleteSQL = "DELETE FROM receta_detalle WHERE id_receta_detalle = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_detalle,))
            con.commit()
            
            return jsonify({
                'success': True,
                'mensaje': 'Medicamento eliminado correctamente.',
                'error': None
            }), 200
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar medicamento: {str(e)}")
            return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de receta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas/paciente/<int:id_paciente>', methods=['GET'])
def getRecetasPorPaciente(id_paciente):
    """Obtiene todas las recetas de un paciente"""
    dao = RecetaDao()
    try:
        recetas = dao.getRecetasPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': recetas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recetas del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

