from flask import Blueprint, request, jsonify, session, current_app as app
from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
from app.services.UltraMsgService import UltraMsgService
from app.auth.utils.decorators import role_required

citaapi = Blueprint('citaapi', __name__)


# ============================================
# CRUD BÁSICO DE CITAS
# ============================================

@citaapi.route('/citas', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getAllCitas():
    """Obtiene la lista completa de citas activas"""
    citadao = CitaDao()
    
    try:
        citas = citadao.getAllCitas()
        return jsonify({'success': True, 'data': citas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las citas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


@citaapi.route('/citas/<int:id_cita>', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCita(id_cita):
    """Obtiene una cita específica por su ID"""
    citadao = CitaDao()
    
    try:
        cita = citadao.getCitaById(id_cita)
        
        if cita:
            return jsonify({'success': True, 'data': cita, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la cita con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


@citaapi.route('/citas/<int:id_cita>/editar', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitaParaEditar(id_cita):
    """Obtiene cita con IDs originales para formulario de edición"""
    citadao = CitaDao()

    try:
        cita = citadao.getCitaParaEditar(id_cita)

        if cita:
            return jsonify({'success': True, 'data': cita, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la cita.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener cita para editar: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@citaapi.route('/citas/<int:id_cita>/logs', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitaLogs(id_cita):
    """Obtiene el historial de estados de una cita"""
    from app.dao.modulos.agendamiento.cita.CitaLogDao import CitaLogDao
    log_dao = CitaLogDao()

    try:
        logs = log_dao.get_logs_por_cita(id_cita)
        return jsonify({'success': True, 'data': logs, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener logs de cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

@citaapi.route('/pacientes/registro-rapido', methods=['POST'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA")
def registroPacienteRapido():
    """
    Registro rápido de paciente desde módulo de citas
    Body: { nombre, apellido, cedula, fecha_nacimiento }
    """
    data = request.get_json()
    citadao = CitaDao()
    
    # Validar campos requeridos
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'fecha_nacimiento']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio'
            }), 400
    
    try:
        paciente = citadao.registrarPacienteRapido(
            nombre=data['nombre'],
            apellido=data['apellido'],
            cedula=data['cedula'],
            fecha_nacimiento=data['fecha_nacimiento']
        )
        
        if paciente:
            return jsonify({
                'success': True,
                'data': paciente,
                'mensaje': 'Paciente registrado exitosamente'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo registrar el paciente. Verifique que la cédula no esté duplicada.'
            }), 400
    
    except Exception as e:
        app.logger.error(f"Error en registro rápido: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        }), 500







@citaapi.route('/citas', methods=['POST'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def addCita():
    """Crea una nueva cita médica"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    citadao = CitaDao()

    campos_requeridos = [
        'id_paciente', 'id_agenda_horario', 'id_especialista', 
        'id_especialidad', 'cita_fecha', 'cita_hora_inicio', 
        'cita_hora_fin', 'cita_tipo', 'cita_motivo'
    ]

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    try:
        cita_id = citadao.guardarCita(
            id_paciente=data['id_paciente'],
            id_agenda_horario=data['id_agenda_horario'],
            id_especialista=data['id_especialista'],
            id_especialidad=data['id_especialidad'],
            cita_fecha=data['cita_fecha'],
            cita_hora_inicio=data['cita_hora_inicio'],
            cita_hora_fin=data['cita_hora_fin'],
            cita_tipo=data['cita_tipo'],
            cita_motivo=data['cita_motivo'],
            cita_creacion_usuario=id_usuario,  # Usar usuario de sesión
            id_estado_cita=data.get('id_estado_cita', 1),  # AGENDADA por defecto
            cita_observaciones=data.get('cita_observaciones'),
            cita_numero_sesion=data.get('cita_numero_sesion')
        )

        if cita_id is not None:
            # Enviar notificación inmediata si está habilitada
            enviar_notificacion = data.get('enviar_notificacion', False)
            notificacion_enviada = False
            notificacion_error = None
            
            if enviar_notificacion:
                try:
                    # Obtener datos completos de la cita para la notificación
                    cita_completa = citadao.getCitaById(cita_id)
                    if cita_completa:
                        # Obtener teléfono del paciente
                        from app.dao.gestionar_personas.paciente.PacienteDao import PacienteDao
                        paciente_dao = PacienteDao()
                        paciente = paciente_dao.getPacienteById(data['id_paciente'])
                        
                        telefono_tutor = paciente.get('tel_madre') or paciente.get('tel_padre') if paciente.get('es_menor') else None
                        telefono_destino = telefono_tutor or paciente.get('telefono')
                        
                        if paciente and telefono_destino:
                            ultramsg_service = UltraMsgService()
                            
                            # Obtener nombre de clínica (configurable, default: "Sysclin")
                            nombre_clinica = app.config.get('NOMBRE_CLINICA', 'Sysclin')
                            
                            # Enviar notificación
                            resultado = ultramsg_service.enviar_notificacion_cita_creada_editada(
                                telefono=telefono_destino,
                                nombre_paciente=cita_completa.get('paciente_nombre', 'Paciente'),
                                cita_fecha=data['cita_fecha'],
                                cita_hora=data['cita_hora_inicio'],
                                especialista=cita_completa.get('especialista_nombre', 'Especialista'),
                                especialidad=cita_completa.get('especialidad', 'Especialidad'),
                                nombre_clinica=nombre_clinica,
                                es_edicion=False
                            )
                            
                            if len(resultado) == 4:
                                success, message_id, error, tipo_error = resultado
                            else:
                                success, message_id, error = resultado
                                tipo_error = None
                            
                            if success:
                                notificacion_enviada = True
                                app.logger.info(
                                    f"✅ Notificación de cita creada enviada a {telefono_destino} "
                                    f"(Message ID: {message_id})"
                                )
                                
                                # Registrar en BD como recordatorio inmediato
                                try:
                                    from app.dao.modulos.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
                                    from datetime import datetime, timedelta
                                    recordatorio_dao = RecordatorioDao()
                                    
                                    # Obtener el mensaje que se envió
                                    mensaje_texto = ultramsg_service._construir_mensaje_cita_creada_editada(
                                        nombre=cita_completa.get('paciente_nombre', 'Paciente'),
                                        fecha=data['cita_fecha'],
                                        hora=data['cita_hora_inicio'],
                                        especialista=cita_completa.get('especialista_nombre', 'Especialista'),
                                        especialidad=cita_completa.get('especialidad', 'Especialidad'),
                                        nombre_clinica=nombre_clinica,
                                        es_edicion=False
                                    )
                                    
                                    # Calcular fechas programadas para recordatorios 24h y 12h
                                    cita_datetime = datetime.strptime(
                                        f"{data['cita_fecha']} {data['cita_hora_inicio']}", 
                                        '%Y-%m-%d %H:%M:%S'
                                    )
                                    fecha_24h = cita_datetime - timedelta(hours=24)
                                    fecha_12h = cita_datetime - timedelta(hours=12)
                                    
                                    # Crear o actualizar recordatorio (una fila por cita)
                                    recordatorio_dao.crearOActualizarRecordatorio(
                                        id_cita=cita_id,
                                        cita_fecha=data['cita_fecha'],
                                        cita_hora_inicio=data['cita_hora_inicio'],
                                        telefono=telefono_destino,
                                        paciente_nombre=cita_completa.get('paciente_nombre', 'Paciente'),
                                        fecha_24h=fecha_24h,
                                        fecha_12h=fecha_12h,
                                        usuario_creacion=id_usuario
                                    )
                                    
                                    # Marcar inmediato como enviado
                                    if recordatorio_dao.marcarInmediatoEnviado(
                                        id_cita=cita_id,
                                        message_id=message_id,
                                        mensaje=mensaje_texto
                                    ):
                                        app.logger.info(f"✅ Recordatorio inmediato registrado en BD para cita {cita_id}")
                                    else:
                                        app.logger.warning(f"⚠️ No se pudo marcar recordatorio inmediato como enviado")
                                        
                                except Exception as e:
                                    app.logger.error(
                                        f"Error al registrar recordatorio inmediato en BD: {str(e)}", 
                                        exc_info=True
                                    )
                            else:
                                notificacion_error = error
                                app.logger.warning(
                                    f"⚠️ No se pudo enviar notificación de cita creada: {error}"
                                )
                        else:
                            app.logger.warning(
                                f"⚠️ Paciente {data['id_paciente']} no tiene teléfono registrado. "
                                f"No se enviará notificación."
                            )
                except Exception as e:
                    app.logger.error(
                        f"Error al enviar notificación de cita creada: {str(e)}", 
                        exc_info=True
                    )
                    notificacion_error = str(e)
            
            mensaje_respuesta = 'Cita creada exitosamente'
            if enviar_notificacion:
                if notificacion_enviada:
                    mensaje_respuesta += '. Notificación enviada al paciente.'
                elif notificacion_error:
                    mensaje_respuesta += f'. Notificación no enviada: {notificacion_error}'
            
            return jsonify({
                'success': True,
                'data': {
                    'id_cita': cita_id, 
                    'mensaje': mensaje_respuesta,
                    'notificacion_enviada': notificacion_enviada
                },
                'error': None
            }), 201
        else:
            # Mensaje de error más descriptivo que cubre todas las posibles causas
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la cita. Posibles causas: la fecha no coincide con el día de la semana configurado en la agenda, la hora no es válida para la agenda, o existe un solapamiento con otra cita del mismo especialista o del mismo paciente en ese horario.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar cita: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@citaapi.route('/citas/<int:id_cita>', methods=['PUT'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def updateCita(id_cita):
    """Actualiza una cita existente"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    citadao = CitaDao()

    cita_existente = citadao.getCitaById(id_cita)
    if not cita_existente:
        return jsonify({'success': False, 'error': 'No se encontró la cita con el ID proporcionado.'}), 404

    campos_requeridos = [
        'cita_fecha', 'cita_hora_inicio', 'cita_hora_fin',
        'cita_tipo', 'cita_motivo', 'id_estado_cita'
    ]

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    try:
        resultado = citadao.updateCita(
            id_cita=id_cita,
            cita_fecha=data['cita_fecha'],
            cita_hora_inicio=data['cita_hora_inicio'],
            cita_hora_fin=data['cita_hora_fin'],
            cita_tipo=data['cita_tipo'],
            cita_motivo=data['cita_motivo'],
            cita_observaciones=data.get('cita_observaciones'),
            cita_numero_sesion=data.get('cita_numero_sesion'),
            id_estado_cita=data['id_estado_cita'],
            modificacion_usuario=id_usuario  # Usar usuario de sesión
        )

        if resultado:
            # Enviar notificación inmediata si está habilitada
            enviar_notificacion = data.get('enviar_notificacion', False)
            notificacion_enviada = False
            notificacion_error = None
            
            if enviar_notificacion:
                try:
                    # Obtener datos completos de la cita actualizada
                    cita_actualizada = citadao.getCitaById(id_cita)
                    if cita_actualizada:
                        # Obtener teléfono del paciente
                        from app.dao.gestionar_personas.paciente.PacienteDao import PacienteDao
                        paciente_dao = PacienteDao()
                        paciente = paciente_dao.getPacienteById(cita_actualizada['id_paciente'])
                        
                        
                        telefono_tutor = paciente.get('tel_madre') or paciente.get('tel_padre') if paciente.get('es_menor') else None
                        telefono_destino = telefono_tutor or paciente.get('telefono')
                        
                        if paciente and telefono_destino:
                            ultramsg_service = UltraMsgService()
                            
                            # Obtener nombre de clínica (configurable, default: "Sysclin")
                            nombre_clinica = app.config.get('NOMBRE_CLINICA', 'Sysclin')
                            
                            # Enviar notificación
                            resultado_notif = ultramsg_service.enviar_notificacion_cita_creada_editada(
                                telefono=telefono_destino,
                                nombre_paciente=cita_actualizada.get('paciente_nombre', 'Paciente'),
                                cita_fecha=data['cita_fecha'],
                                cita_hora=data['cita_hora_inicio'],
                                especialista=cita_actualizada.get('especialista_nombre', 'Especialista'),
                                especialidad=cita_actualizada.get('especialidad', 'Especialidad'),
                                nombre_clinica=nombre_clinica,
                                es_edicion=True
                            )
                            
                            if len(resultado_notif) == 4:
                                success, message_id, error, tipo_error = resultado_notif
                            else:
                                success, message_id, error = resultado_notif
                                tipo_error = None
                            
                            if success:
                                notificacion_enviada = True
                                app.logger.info(
                                    f"✅ Notificación de cita actualizada enviada a {telefono_destino} "
                                    f"(Message ID: {message_id})"
                                )
                                
                                # Registrar en BD como recordatorio inmediato
                                try:
                                    from app.dao.modulos.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
                                    from datetime import datetime, timedelta
                                    recordatorio_dao = RecordatorioDao()
                                    
                                    # Obtener el mensaje que se envió
                                    mensaje_texto = ultramsg_service._construir_mensaje_cita_creada_editada(
                                        nombre=cita_actualizada.get('paciente_nombre', 'Paciente'),
                                        fecha=data['cita_fecha'],
                                        hora=data['cita_hora_inicio'],
                                        especialista=cita_actualizada.get('especialista_nombre', 'Especialista'),
                                        especialidad=cita_actualizada.get('especialidad', 'Especialidad'),
                                        nombre_clinica=nombre_clinica,
                                        es_edicion=True
                                    )
                                    
                                    # Calcular fechas programadas para recordatorios 24h y 12h
                                    cita_datetime = datetime.strptime(
                                        f"{data['cita_fecha']} {data['cita_hora_inicio']}", 
                                        '%Y-%m-%d %H:%M:%S'
                                    )
                                    fecha_24h = cita_datetime - timedelta(hours=24)
                                    fecha_12h = cita_datetime - timedelta(hours=12)
                                    
                                    # Crear o actualizar recordatorio (una fila por cita)
                                    recordatorio_dao.crearOActualizarRecordatorio(
                                        id_cita=id_cita,
                                        cita_fecha=data['cita_fecha'],
                                        cita_hora_inicio=data['cita_hora_inicio'],
                                        telefono=telefono_destino,
                                        paciente_nombre=cita_actualizada.get('paciente_nombre', 'Paciente'),
                                        fecha_24h=fecha_24h,
                                        fecha_12h=fecha_12h,
                                        usuario_creacion=id_usuario
                                    )
                                    
                                    # Marcar inmediato como enviado
                                    if recordatorio_dao.marcarInmediatoEnviado(
                                        id_cita=id_cita,
                                        message_id=message_id,
                                        mensaje=mensaje_texto
                                    ):
                                        app.logger.info(f"✅ Recordatorio inmediato registrado en BD para cita {id_cita}")
                                    else:
                                        app.logger.warning(f"⚠️ No se pudo marcar recordatorio inmediato como enviado")
                                        
                                except Exception as e:
                                    app.logger.error(
                                        f"Error al registrar recordatorio inmediato en BD: {str(e)}", 
                                        exc_info=True
                                    )
                            else:
                                notificacion_error = error
                                app.logger.warning(
                                    f"⚠️ No se pudo enviar notificación de cita actualizada: {error}"
                                )
                        else:
                            app.logger.warning(
                                f"⚠️ Paciente {cita_actualizada['id_paciente']} no tiene teléfono registrado. "
                                f"No se enviará notificación."
                            )
                except Exception as e:
                    app.logger.error(
                        f"Error al enviar notificación de cita actualizada: {str(e)}", 
                        exc_info=True
                    )
                    notificacion_error = str(e)
            
            mensaje_respuesta = 'Cita actualizada exitosamente'
            if enviar_notificacion:
                if notificacion_enviada:
                    mensaje_respuesta += '. Notificación enviada al paciente.'
                elif notificacion_error:
                    mensaje_respuesta += f'. Notificación no enviada: {notificacion_error}'
            
            return jsonify({
                'success': True,
                'data': {
                    'id_cita': id_cita, 
                    'mensaje': mensaje_respuesta,
                    'notificacion_enviada': notificacion_enviada
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la cita. Posibles causas: existe un solapamiento con otra cita del mismo especialista o del mismo paciente en ese horario, o la cita no fue encontrada.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar cita: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@citaapi.route('/citas/<int:id_cita>', methods=['DELETE'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA")
def deleteCita(id_cita):
    """Elimina lógicamente una cita"""
    citadao = CitaDao()

    try:
        if citadao.deleteCita(id_cita):
            return jsonify({
                'success': True,
                'mensaje': f'Cita con ID {id_cita} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la cita con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


# ============================================
# ENDPOINTS PARA MODALES DE BÚSQUEDA
# ============================================

@citaapi.route('/pacientes', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getPacientes():
    """Obtiene lista de pacientes para modales"""
    citadao = CitaDao()
    
    try:
        pacientes = citadao.getPacientes()
        return jsonify({'success': True, 'data': pacientes, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener pacientes: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/especialistas', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getEspecialistas():
    """Obtiene lista de especialistas para modales
    Si se proporciona id_especialidad como parámetro de query, filtra solo los especialistas vinculados a esa especialidad
    Endpoint compartido entre citas y agenda médica
    Ejemplo: /api/v1/especialistas?id_especialidad=1"""
    citadao = CitaDao()
    
    try:
        # Obtener parámetro opcional id_especialidad de la query string
        id_especialidad = request.args.get('id_especialidad', type=int)
        
        especialistas = citadao.getEspecialistas(id_especialidad=id_especialidad)
        app.logger.info(f"Cita API /especialistas: Retornando {len(especialistas) if especialistas else 0} especialistas" + 
                       (f" (filtrados por especialidad {id_especialidad})" if id_especialidad else ""))
        
        if not especialistas:
            app.logger.warning("Cita API: No se encontraron especialistas activos" + 
                              (f" para la especialidad {id_especialidad}" if id_especialidad else ""))
        
        return jsonify({
            'success': True, 
            'data': especialistas if especialistas else [], 
            'error': None,
            'total': len(especialistas) if especialistas else 0
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas en Cita API: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'error': f'Ocurrió un error interno: {str(e)}',
            'data': []
        }), 500


@citaapi.route('/especialidades', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getEspecialidades():
    """Obtiene lista de especialidades para modales"""
    citadao = CitaDao()
    
    try:
        especialidades = citadao.getEspecialidades()
        app.logger.info(f"Cita API /especialidades: Retornando {len(especialidades) if especialidades else 0} especialidades")
        
        if not especialidades:
            app.logger.warning("Cita API: No se encontraron especialidades activas")
        
        return jsonify({
            'success': True, 
            'data': especialidades if especialidades else [], 
            'error': None,
            'total': len(especialidades) if especialidades else 0
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialidades en Cita API: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'error': f'Ocurrió un error interno: {str(e)}',
            'data': []
        }), 500


@citaapi.route('/estados-citas', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getEstadosCitas():
    """Obtiene lista de estados de citas"""
    citadao = CitaDao()
    
    try:
        estados = citadao.getEstadosCitas()
        return jsonify({'success': True, 'data': estados, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estados de citas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# CONSULTA DE CUPOS DISPONIBLES
# ============================================

@citaapi.route('/cupos/especialidad/<int:id_especialidad>', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCuposPorEspecialidad(id_especialidad):
    """
    Obtiene cupos disponibles para una especialidad.
    Query params: fecha_inicio (YYYY-MM-DD), fecha_fin (YYYY-MM-DD)
    """
    citadao = CitaDao()
    
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        if not fecha_inicio or not fecha_fin:
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar fecha_inicio y fecha_fin como parámetros.'
            }), 400
        
        cupos = citadao.getCuposDisponiblesPorEspecialidad(id_especialidad, fecha_inicio, fecha_fin)
        return jsonify({'success': True, 'data': cupos, 'error': None}), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener cupos por especialidad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/cupos/especialista/<int:id_especialista>', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCuposPorEspecialista(id_especialista):
    """
    Obtiene cupos disponibles para un especialista.
    Query params: fecha_inicio (YYYY-MM-DD), fecha_fin (YYYY-MM-DD)
    """
    citadao = CitaDao()
    
    try:
        fecha_inicio = request.args.get('fecha_inicio')
        fecha_fin = request.args.get('fecha_fin')
        
        app.logger.info(f"API: Solicitud de cupos para especialista {id_especialista}, fecha_inicio={fecha_inicio}, fecha_fin={fecha_fin}")
        
        if not fecha_inicio or not fecha_fin:
            app.logger.warning(f"API: Faltan parámetros fecha_inicio o fecha_fin")
            return jsonify({
                'success': False,
                'error': 'Debe proporcionar fecha_inicio y fecha_fin como parámetros.'
            }), 400
        
        cupos = citadao.getCuposDisponiblesPorEspecialista(id_especialista, fecha_inicio, fecha_fin)
        
        app.logger.info(f"API: Se retornaron {len(cupos)} cupos para especialista {id_especialista}")
        if len(cupos) == 0:
            app.logger.warning(f"API: ⚠️ No se encontraron cupos. Verificar configuración de agenda para especialista {id_especialista}")
        
        return jsonify({'success': True, 'data': cupos, 'error': None}), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener cupos por especialista: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500

# ============================================
# CAMBIO DE ESTADO DE CITAS
# ============================================

@citaapi.route('/citas/<int:id_cita>/confirmar', methods=['PATCH'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def confirmarCita(id_cita):
    """Confirma una cita (atajo para cambiar estado a CONFIRMADA)"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    citadao = CitaDao()
    
    usuario_id = id_usuario  # Usar usuario de sesión
    
    try:
        resultado = citadao.confirmarCita(id_cita, usuario_id)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Cita confirmada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo confirmar la cita.'}), 400
    
    except Exception as e:
        app.logger.error(f"Error al confirmar cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/cancelar', methods=['PATCH'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def cancelarCita(id_cita):
    """Cancela una cita (atajo para cambiar estado a CANCELADA)"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    citadao = CitaDao()
    
    usuario_id = id_usuario  # Usar usuario de sesión
    
    try:
        resultado = citadao.cancelarCita(id_cita, usuario_id)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Cita cancelada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo cancelar la cita.'}), 400
    
    except Exception as e:
        app.logger.error(f"Error al cancelar cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/<int:id_cita>/estado', methods=['PATCH'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def cambiarEstadoCita(id_cita):
    """
    Cambia el estado de una cita.
    Body: { "id_estado_cita": 2 }
    """
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    citadao = CitaDao()
    
    if 'id_estado_cita' not in data:
        return jsonify({'success': False, 'error': 'Debe proporcionar id_estado_cita.'}), 400
    
    usuario_id = id_usuario  # Usar usuario de sesión
    
    try:
        resultado = citadao.cambiarEstadoCita(id_cita, data['id_estado_cita'], usuario_id)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Estado de la cita actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo cambiar el estado de la cita.'}), 400
    
    except Exception as e:
        app.logger.error(f"Error al cambiar estado de cita: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# CONSULTAS ADICIONALES (OPCIONALES)
# ============================================

@citaapi.route('/citas/paciente/<int:id_paciente>', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitasByPaciente(id_paciente):
    """Obtiene todas las citas de un paciente"""
    citadao = CitaDao()
    
    try:
        citas = citadao.getCitasByPaciente(id_paciente)
        return jsonify({'success': True, 'data': citas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener citas del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@citaapi.route('/citas/especialista/<int:id_especialista>', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitasByEspecialista(id_especialista):
    """Obtiene todas las citas de un especialista"""
    citadao = CitaDao()
    
    try:
        citas = citadao.getCitasByEspecialista(id_especialista)
        return jsonify({'success': True, 'data': citas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener citas del especialista: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
    




# En app/rutas/modulos/cita/cita_api.py

@citaapi.route('/citas/<int:id_cita>', methods=['GET'])
def get_cita_detalle(id_cita):
    """GET /api/v1/citas/<id>"""
    try:
        from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
        
        cita_dao = CitaDao()
        cita = cita_dao.getCitaById(id_cita)
        
        if not cita:
            return jsonify({
                'success': False,
                'message': 'Cita no encontrada'
            }), 404
        
        return jsonify({
            'success': True,
            'data': cita
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500





# ============================================
# ENDPOINTS PARA DASHBOARD
# ============================================

@citaapi.route('/citas-hoy', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitasHoy():
    """Obtiene las citas programadas para hoy con información completa"""
    citadao = CitaDao()
    
    try:
        from datetime import date
        hoy = date.today()
        
        citas = citadao.getCitasByFecha(hoy, hoy)
        
        # Transformar al formato esperado por el frontend
        citas_formateadas = []
        for cita in citas:
            citas_formateadas.append({
                'id_cita': cita['id_cita'],
                'hora': cita['hora'],
                'paciente': cita['paciente'],
                'profesional': cita['especialista'],
                'especialidad': cita['especialidad'],
                'observacion': cita.get('tipo', ''),
                'estado': cita.get('estado', 'pendiente').lower()
            })
        
        return jsonify({
            'success': True,
            'citas': citas_formateadas,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener citas de hoy: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al obtener las citas de hoy.'
        }), 500


@citaapi.route('/citas-manana', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getCitasManana():
    """Obtiene las citas programadas para mañana con información completa"""
    citadao = CitaDao()
    
    try:
        from datetime import date, timedelta
        manana = date.today() + timedelta(days=1)
        
        citas = citadao.getCitasByFecha(manana, manana)
        
        # Transformar al formato esperado por el frontend
        citas_formateadas = []
        for cita in citas:
            citas_formateadas.append({
                'id_cita': cita['id_cita'],
                'hora': cita['hora'],
                'paciente': cita['paciente'],
                'profesional': cita['especialista'],
                'especialidad': cita['especialidad'],
                'observacion': cita.get('tipo', ''),
                'estado': cita.get('estado', 'pendiente').lower()
            })
        
        return jsonify({
            'success': True,
            'citas': citas_formateadas,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener citas de mañana: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al obtener las citas de mañana.'
        }), 500


@citaapi.route('/estadisticas', methods=['GET'])
@role_required("SUPERADMINISTRADOR", "ADMINISTRADOR", "ADMIN", "RECEPCIONISTA", "ESPECIALISTA")
def getEstadisticas():
    """Obtiene estadísticas generales para el dashboard"""
    citadao = CitaDao()
    
    try:
        from datetime import date
        hoy = date.today()
        
        # Obtener citas de hoy
        citas_hoy = citadao.getCitasByFecha(hoy, hoy)
        
        # Contar citas por estado
        pendientes = sum(1 for c in citas_hoy if c.get('estado', '').upper() in ['AGENDADA', 'PENDIENTE'])
        
        # Obtener totales generales
        todas_citas = citadao.getAllCitas()
        pacientes_activos = len(set(c['id_paciente'] for c in todas_citas))
        profesionales = len(citadao.getEspecialistas())
        
        return jsonify({
            'success': True,
            'citas_hoy': len(citas_hoy),
            'pacientes_activos': pacientes_activos,
            'profesionales': profesionales,
            'pendientes': pendientes,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al obtener las estadísticas.'
        }), 500


