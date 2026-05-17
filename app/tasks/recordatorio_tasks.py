"""
Tareas programadas para procesar recordatorios de citas
Ejecuta automáticamente el envío de recordatorios pendientes vía UltraMsg (WhatsApp)
Nueva estructura: una fila por cita con columnas booleanas para cada tipo
"""
from flask import current_app
from app import app
from app.dao.modulos.recordatorio.RecordatorioDao import RecordatorioDao
from app.services.UltraMsgService import UltraMsgService
from datetime import datetime


def procesar_recordatorios_pendientes():
    """
    Procesa recordatorios pendientes (24h y 12h) y los envía vía UltraMsg (WhatsApp)
    
    Esta función debe ejecutarse periódicamente (cada 5-10 minutos)
    mediante un scheduler (APScheduler o cron)
    
    Returns:
        dict: Estadísticas del procesamiento
    """
    # Usar contexto de aplicación para acceder a app.logger
    with app.app_context():
        app.logger.info("=== INICIANDO PROCESAMIENTO DE RECORDATORIOS ===")
        
        recordatorio_dao = RecordatorioDao()
        ultramsg_service = UltraMsgService()
        
        # Verificar si el servicio está disponible
        if not ultramsg_service.client_available:
            app.logger.warning(
                "⚠️ UltraMsg no está configurado. "
                "Configure ULTRAMSG_INSTANCE_ID y ULTRAMSG_TOKEN en variables de entorno."
            )
            return {
                'total': 0,
                'enviados': 0,
                'fallidos': 0,
                'errores': [{
                    'error': 'UltraMsg no configurado'
                }]
            }
        
        estadisticas = {
            'total': 0,
            'enviados': 0,
            'fallidos': 0,
            'errores': []
        }
        
        # Procesar recordatorios 24h
        app.logger.info("Procesando recordatorios 24h...")
        recordatorios_24h = recordatorio_dao.obtenerRecordatoriosPendientes24h(limite=100)
        app.logger.info(f"Se encontraron {len(recordatorios_24h)} recordatorios 24h pendientes")
        
        for recordatorio in recordatorios_24h:
            estadisticas['total'] += 1
            id_cita = recordatorio['id_cita']
            
            try:
                app.logger.info(
                    f"Procesando recordatorio 24h para cita {id_cita} "
                    f"(Paciente: {recordatorio['paciente_nombre_completo']})"
                )
                
                # Preparar datos para el envío
                telefono = recordatorio['telefono'] or recordatorio.get('paciente_telefono')
                nombre_paciente = recordatorio['paciente_nombre_completo'] or recordatorio['paciente_nombre_cache']
                cita_fecha = recordatorio['cita_fecha']
                cita_hora = recordatorio['cita_hora_inicio']
                especialista = recordatorio['especialista_nombre']
                especialidad = recordatorio['especialidad']
                motivo = recordatorio.get('cita_motivo')
                
                # Validar que tenemos datos mínimos
                if not telefono:
                    error_msg = f"Teléfono no disponible para recordatorio 24h de cita {id_cita}"
                    app.logger.warning(error_msg)
                    estadisticas['fallidos'] += 1
                    estadisticas['errores'].append({
                        'id_cita': id_cita,
                        'tipo': '24h',
                        'error': error_msg
                    })
                    continue
                
                # Enviar recordatorio (con reintentos automáticos integrados)
                resultado = ultramsg_service.enviar_recordatorio_cita(
                    telefono=telefono,
                    nombre_paciente=nombre_paciente,
                    cita_fecha=cita_fecha,
                    cita_hora=cita_hora,
                    especialista=especialista,
                    especialidad=especialidad,
                    motivo=motivo
                )
                
                # Manejar nuevo formato de retorno (puede incluir tipo_error)
                if len(resultado) == 4:
                    success, message_id, error, tipo_error = resultado
                else:
                    # Compatibilidad con formato anterior
                    success, message_id, error = resultado
                    tipo_error = None
                
                if success:
                    # Marcar como enviado
                    mensaje_texto = ultramsg_service._construir_mensaje_recordatorio(
                        nombre_paciente, cita_fecha, cita_hora,
                        especialista, especialidad, motivo
                    )
                    recordatorio_dao.marcar24hEnviado(
                        id_cita=id_cita,
                        message_id=message_id,
                        mensaje=mensaje_texto
                    )
                    estadisticas['enviados'] += 1
                    app.logger.info(
                        f"✅ Recordatorio 24h para cita {id_cita} enviado exitosamente "
                        f"(Message ID: {message_id})"
                    )
                else:
                    # No marcamos como fallido en BD, solo registramos el error
                    error_msg = error or "Error desconocido"
                    tipo_error_str = f" ({tipo_error.value})" if tipo_error else ""
                    estadisticas['fallidos'] += 1
                    estadisticas['errores'].append({
                        'id_cita': id_cita,
                        'tipo': '24h',
                        'error': error_msg,
                        'tipo_error': tipo_error.value if tipo_error else 'desconocido'
                    })
                    app.logger.warning(
                        f"❌ Recordatorio 24h para cita {id_cita} falló{tipo_error_str}: {error_msg}"
                    )
            
            except Exception as e:
                # Error inesperado al procesar este recordatorio
                error_msg = f"Error inesperado procesando recordatorio 24h de cita {id_cita}: {str(e)}"
                app.logger.error(error_msg, exc_info=True)
                estadisticas['fallidos'] += 1
                estadisticas['errores'].append({
                    'id_cita': id_cita,
                    'tipo': '24h',
                    'error': error_msg
                })
        
        # Procesar recordatorios 12h
        app.logger.info("Procesando recordatorios 12h...")
        recordatorios_12h = recordatorio_dao.obtenerRecordatoriosPendientes12h(limite=100)
        app.logger.info(f"Se encontraron {len(recordatorios_12h)} recordatorios 12h pendientes")
        
        for recordatorio in recordatorios_12h:
            estadisticas['total'] += 1
            id_cita = recordatorio['id_cita']
            
            try:
                app.logger.info(
                    f"Procesando recordatorio 12h para cita {id_cita} "
                    f"(Paciente: {recordatorio['paciente_nombre_completo']})"
                )
                
                # Preparar datos para el envío
                telefono = recordatorio['telefono'] or recordatorio.get('paciente_telefono')
                nombre_paciente = recordatorio['paciente_nombre_completo'] or recordatorio['paciente_nombre_cache']
                cita_fecha = recordatorio['cita_fecha']
                cita_hora = recordatorio['cita_hora_inicio']
                especialista = recordatorio['especialista_nombre']
                especialidad = recordatorio['especialidad']
                motivo = recordatorio.get('cita_motivo')
                
                # Validar que tenemos datos mínimos
                if not telefono:
                    error_msg = f"Teléfono no disponible para recordatorio 12h de cita {id_cita}"
                    app.logger.warning(error_msg)
                    estadisticas['fallidos'] += 1
                    estadisticas['errores'].append({
                        'id_cita': id_cita,
                        'tipo': '12h',
                        'error': error_msg
                    })
                    continue
                
                # Enviar recordatorio (con reintentos automáticos integrados)
                resultado = ultramsg_service.enviar_recordatorio_cita(
                    telefono=telefono,
                    nombre_paciente=nombre_paciente,
                    cita_fecha=cita_fecha,
                    cita_hora=cita_hora,
                    especialista=especialista,
                    especialidad=especialidad,
                    motivo=motivo
                )
                
                # Manejar nuevo formato de retorno (puede incluir tipo_error)
                if len(resultado) == 4:
                    success, message_id, error, tipo_error = resultado
                else:
                    # Compatibilidad con formato anterior
                    success, message_id, error = resultado
                    tipo_error = None
                
                if success:
                    # Marcar como enviado
                    mensaje_texto = ultramsg_service._construir_mensaje_recordatorio(
                        nombre_paciente, cita_fecha, cita_hora,
                        especialista, especialidad, motivo
                    )
                    recordatorio_dao.marcar12hEnviado(
                        id_cita=id_cita,
                        message_id=message_id,
                        mensaje=mensaje_texto
                    )
                    estadisticas['enviados'] += 1
                    app.logger.info(
                        f"✅ Recordatorio 12h para cita {id_cita} enviado exitosamente "
                        f"(Message ID: {message_id})"
                    )
                else:
                    # No marcamos como fallido en BD, solo registramos el error
                    error_msg = error or "Error desconocido"
                    tipo_error_str = f" ({tipo_error.value})" if tipo_error else ""
                    estadisticas['fallidos'] += 1
                    estadisticas['errores'].append({
                        'id_cita': id_cita,
                        'tipo': '12h',
                        'error': error_msg,
                        'tipo_error': tipo_error.value if tipo_error else 'desconocido'
                    })
                    app.logger.warning(
                        f"❌ Recordatorio 12h para cita {id_cita} falló{tipo_error_str}: {error_msg}"
                    )
            
            except Exception as e:
                # Error inesperado al procesar este recordatorio
                error_msg = f"Error inesperado procesando recordatorio 12h de cita {id_cita}: {str(e)}"
                app.logger.error(error_msg, exc_info=True)
                estadisticas['fallidos'] += 1
                estadisticas['errores'].append({
                    'id_cita': id_cita,
                    'tipo': '12h',
                    'error': error_msg
                })
        
        # Obtener métricas del servicio
        metricas_servicio = ultramsg_service.obtener_metricas()
        
        # Log de resumen detallado
        tasa_exito = (estadisticas['enviados'] / estadisticas['total']) * 100 if estadisticas['total'] > 0 else 0
        
        app.logger.info(
            f"=== PROCESAMIENTO COMPLETADO ===\n"
            f"Total procesados: {estadisticas['total']}\n"
            f"✅ Enviados: {estadisticas['enviados']}\n"
            f"❌ Fallidos: {estadisticas['fallidos']}\n"
            f"📊 Tasa de éxito: {tasa_exito:.1f}%\n"
            f"🔄 Reintentos realizados: {metricas_servicio.get('total_reintentos', 0)}\n"
            f"⏱️ Tiempo promedio de envío: {metricas_servicio.get('tiempo_promedio_envio', 0):.2f}s"
        )
        
        # Alertar si hay muchos fallos
        if estadisticas['fallidos'] > 0:
            if tasa_exito < 50:
                app.logger.error(
                    f"⚠️ ALERTA: Tasa de éxito muy baja ({tasa_exito:.1f}%). "
                    f"Revisar configuración de UltraMsg o conectividad."
                )
            elif tasa_exito < 80:
                app.logger.warning(
                    f"⚠️ ADVERTENCIA: Tasa de éxito baja ({tasa_exito:.1f}%). "
                    f"Revisar logs para más detalles."
                )
        
        # Agregar métricas del servicio a las estadísticas
        estadisticas['metricas_servicio'] = metricas_servicio
        
        return estadisticas


def configurar_tarea_recordatorios(scheduler):
    """
    Configura la tarea programada de recordatorios en el scheduler
    
    Args:
        scheduler: Instancia de APScheduler (BackgroundScheduler)
    
    Uso:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        configurar_tarea_recordatorios(scheduler)
        scheduler.start()
    """
    from app import app
    
    with app.app_context():
        scheduler.add_job(
            func=procesar_recordatorios_pendientes,
            trigger='interval',
            minutes=10,  # Ejecutar cada 10 minutos
            id='procesar_recordatorios',
            replace_existing=True,
            max_instances=1,  # Solo una instancia a la vez
            coalesce=True,  # Si se acumulan ejecuciones, ejecutar solo una
            misfire_grace_time=300  # 5 minutos de gracia si se pierde una ejecución
        )
        
        app.logger.info("✅ Tarea programada de recordatorios configurada (cada 10 minutos)")
