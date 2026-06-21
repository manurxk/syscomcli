"""
API para gestionar derivaciones entre especialistas
"""
from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.modulos.consultorio.derivacion.DerivacionDao import DerivacionDao
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes

derivacionapi = Blueprint('derivacionapi', __name__)


# ============================================
# CRUD BÁSICO DE DERIVACIONES
# ============================================

@derivacionapi.route('/derivaciones', methods=['GET'])
def getAllDerivaciones():
    """Obtiene todas las derivaciones (filtradas por especialista si aplica)"""
    dao = DerivacionDao()
    
    try:
        app.logger.info("DEBUG getAllDerivaciones API: Obteniendo todas las derivaciones")
        derivaciones = dao.getDerivaciones()
        app.logger.info(f"DEBUG getAllDerivaciones API: Retornando {len(derivaciones)} derivaciones")
        return jsonify({'success': True, 'data': derivaciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener derivaciones: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/pendientes', methods=['GET'])
def getDerivacionesPendientes():
    """Obtiene derivaciones pendientes recibidas por el especialista logueado"""
    dao = DerivacionDao()
    
    try:
        app.logger.info("DEBUG getDerivacionesPendientes API: Obteniendo derivaciones pendientes")
        derivaciones = dao.getDerivacionesPendientes()
        app.logger.info(f"DEBUG getDerivacionesPendientes API: Retornando {len(derivaciones)} derivaciones")
        return jsonify({'success': True, 'data': derivaciones, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener derivaciones pendientes: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>', methods=['GET'])
def getDerivacion(id_derivacion):
    """Obtiene una derivación específica por ID"""
    dao = DerivacionDao()
    
    try:
        app.logger.info(f"DEBUG getDerivacion API: Obteniendo derivación ID {id_derivacion}")
        derivacion = dao.getDerivacionById(id_derivacion)
        
        if derivacion:
            app.logger.info(f"DEBUG getDerivacion API: Derivación encontrada")
            return jsonify({'success': True, 'data': derivacion, 'error': None}), 200
        else:
            app.logger.warning(f"DEBUG getDerivacion API: Derivación {id_derivacion} no encontrada")
            return jsonify({'success': False, 'error': 'No se encontró la derivación.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener derivación: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@derivacionapi.route('/derivaciones', methods=['POST'])
def crearDerivacion():
    """Crea una nueva derivación (soporta especialistas internos y externos)"""
    data = request.get_json()
    dao = DerivacionDao()
    
    # Validar campos obligatorios básicos
    if 'id_paciente' not in data or not data['id_paciente']:
        return jsonify({
            'success': False,
            'error': 'El campo id_paciente es obligatorio.'
        }), 400
    
    if 'motivo_derivacion' not in data or not data.get('motivo_derivacion'):
        return jsonify({
            'success': False,
            'error': 'El campo motivo_derivacion es obligatorio.'
        }), 400
    
    # Obtener id_especialista_origen del usuario logueado
    id_especialista_origen = obtener_id_especialista_usuario()
    if not id_especialista_origen:
        return jsonify({
            'success': False,
            'error': 'Debe ser un especialista para crear derivaciones.'
        }), 403
    
    # Determinar si es derivación externa o interna
    es_externo = data.get('es_externo', False)
    
    if es_externo:
        # Validar campos para especialista externo
        if not data.get('externo_nombre'):
            return jsonify({
                'success': False,
                'error': 'Para especialista externo, el nombre es obligatorio.'
            }), 400
    else:
        # Validar campos para especialista interno
        if 'id_especialista_destino' not in data or not data['id_especialista_destino']:
            return jsonify({
                'success': False,
                'error': 'Debe seleccionar un especialista destino o marcar como externo.'
            }), 400
        
        # Validar que no se derive a sí mismo
        if id_especialista_origen == data['id_especialista_destino']:
            return jsonify({
                'success': False,
                'error': 'No puedes derivar un paciente a ti mismo.'
            }), 400
    
    try:
        app.logger.info(f"DEBUG crearDerivacion API: id_paciente={data['id_paciente']}, id_especialista_origen={id_especialista_origen}, id_especialista_destino={data.get('id_especialista_destino')}, es_externo={es_externo}")
        
        id_derivacion = dao.crearDerivacion(
            id_paciente=data['id_paciente'],
            id_especialista_origen=id_especialista_origen,
            id_especialista_destino=data.get('id_especialista_destino'),
            motivo_derivacion=data['motivo_derivacion'],
            observaciones=data.get('observaciones'),
            urgencia=data.get('urgencia', 'NORMAL'),
            usuario_creacion=session.get('usu_nick', 'SISTEMA'),
            es_externo=es_externo,
            externo_nombre=data.get('externo_nombre'),
            externo_apellido=data.get('externo_apellido'),
            externo_telefono=data.get('externo_telefono'),
            externo_matricula=data.get('externo_matricula')
        )
        
        app.logger.info(f"DEBUG crearDerivacion API: id_derivacion retornado={id_derivacion}")
        
        if id_derivacion:
            return jsonify({
                'success': True,
                'data': {'id_derivacion': id_derivacion, 'mensaje': 'Derivación creada exitosamente'},
                'error': None
            }), 201
        else:
            app.logger.warning("DEBUG crearDerivacion API: No se pudo crear la derivación (retornó None)")
            return jsonify({
                'success': False,
                'error': 'No se pudo crear la derivación. Verifique los datos.'
            }), 500
    except Exception as e:
        app.logger.error(f"DEBUG crearDerivacion API: Excepción capturada: {str(e)}", exc_info=True)
        app.logger.error(f"Error al crear derivación: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>/aceptar', methods=['PATCH'])
def aceptarDerivacion(id_derivacion):
    """Acepta una derivación pendiente"""
    dao = DerivacionDao()
    usuario_id = session.get('id_usuario')
    
    if not usuario_id:
        return jsonify({
            'success': False,
            'error': 'Debe estar logueado para aceptar derivaciones.'
        }), 401
    
    try:
        if dao.aceptarDerivacion(id_derivacion, usuario_id):
            return jsonify({
                'success': True,
                'mensaje': 'Derivación aceptada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo aceptar la derivación. Verifique que esté pendiente.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al aceptar derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>/rechazar', methods=['PATCH'])
def rechazarDerivacion(id_derivacion):
    """Rechaza una derivación pendiente"""
    data = request.get_json()
    dao = DerivacionDao()
    usuario_id = session.get('id_usuario')
    
    if not usuario_id:
        return jsonify({
            'success': False,
            'error': 'Debe estar logueado para rechazar derivaciones.'
        }), 401
    
    motivo_rechazo = data.get('motivo_rechazo', 'Sin motivo especificado')
    
    try:
        if dao.rechazarDerivacion(id_derivacion, usuario_id, motivo_rechazo):
            return jsonify({
                'success': True,
                'mensaje': 'Derivación rechazada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo rechazar la derivación. Verifique que esté pendiente.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al rechazar derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@derivacionapi.route('/derivaciones/<int:id_derivacion>/cancelar', methods=['PATCH'])
def cancelarDerivacion(id_derivacion):
    """Cancela una derivación pendiente (solo el especialista origen)"""
    dao = DerivacionDao()
    usuario_id = session.get('id_usuario')
    
    if not usuario_id:
        return jsonify({
            'success': False,
            'error': 'Debe estar logueado para cancelar derivaciones.'
        }), 401
    
    try:
        if dao.cancelarDerivacion(id_derivacion, usuario_id):
            return jsonify({
                'success': True,
                'mensaje': 'Derivación cancelada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo cancelar la derivación. Solo el especialista origen puede cancelar.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al cancelar derivación: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS AUXILIARES
# ============================================

@derivacionapi.route('/especialistas-disponibles', methods=['GET'])
def getEspecialistasDisponibles():
    """Obtiene lista de especialistas disponibles para derivación (excluye al logueado)"""
    try:
        dao = DerivacionDao()
        id_especialista_actual = obtener_id_especialista_usuario()
        
        app.logger.info(f"GET /especialistas-disponibles - id_especialista_actual: {id_especialista_actual}")
        
        # Si no es especialista, puede ver todos los especialistas
        especialistas = dao.getEspecialistasDisponibles(excluir_especialista=id_especialista_actual)
        app.logger.info(f"Especialistas retornados: {len(especialistas)}")
        
        return jsonify({
            'success': True, 
            'data': especialistas, 
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas disponibles: {str(e)}", exc_info=True)
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False, 
            'error': f'Ocurrió un error interno: {str(e)}',
            'data': []
        }), 500

