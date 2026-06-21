from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.services.UltraMsgService import UltraMsgService
from app.auth.utils.decorators import role_required

recordatorioapi = Blueprint('recordatorioapi', __name__)

# ============================================
# CONSULTAS DE RECORDATORIOS
# ============================================

@recordatorioapi.route('/recordatorios', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getAllRecordatorios():
    """
    Obtiene listado de recordatorios con filtros opcionales
    
    Query params:
        - estado: inmediato, 24h, 12h (filtra por tipo enviado)
        - fecha_desde: YYYY-MM-DD
        - fecha_hasta: YYYY-MM-DD
        - id_cita: filtrar por cita específica
        - page: número de página (default: 1)
        - per_page: registros por página (default: 50)
    """
    recordatorio_dao = RecordatorioDao()
    
    try:
        # Obtener parámetros de filtro
        estado = request.args.get('estado')
        fecha_desde = request.args.get('fecha_desde')
        fecha_hasta = request.args.get('fecha_hasta')
        id_cita = request.args.get('id_cita', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        solo_enviados_param = request.args.get('solo_enviados', 'false')
        solo_enviados = solo_enviados_param.lower() == 'true' if solo_enviados_param else False
        app.logger.debug(f"Parámetro solo_enviados recibido: '{solo_enviados_param}', convertido a: {solo_enviados}")
        
        # Usar método del DAO
        recordatorios, total = recordatorio_dao.getAllRecordatorios(
            estado=estado,
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            id_cita=id_cita,
            page=page,
            per_page=per_page,
            solo_enviados=solo_enviados
        )
        
        app.logger.info(f"Recordatorios encontrados: {len(recordatorios)}, Total: {total}, Filtros: estado={estado}, solo_enviados={solo_enviados}")
        
        return jsonify({
            'success': True,
            'data': recordatorios,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page if total > 0 else 0
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en getAllRecordatorios: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@recordatorioapi.route('/recordatorios/<int:id_recordatorio>', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getRecordatorio(id_recordatorio):
    """Obtiene detalles de un recordatorio específico por ID"""
    from app.conexion.Conexion import Conexion
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        selectSQL = """
            SELECT 
                r.id_recordatorio,
                r.id_cita,
                r.recordatorio_cita_fecha,
                r.recordatorio_cita_hora_inicio,
                r.recordatorio_telefono,
                r.recordatorio_paciente_nombre,
                r.recordatorio_inmediato_enviado,
                r.recordatorio_inmediato_fecha_enviado,
                r.recordatorio_inmediato_ultramsg_id,
                r.recordatorio_inmediato_mensaje,
                r.recordatorio_24h_enviado,
                r.recordatorio_24h_fecha_programada,
                r.recordatorio_24h_fecha_enviado,
                r.recordatorio_24h_ultramsg_id,
                r.recordatorio_24h_mensaje,
                r.recordatorio_12h_enviado,
                r.recordatorio_12h_fecha_programada,
                r.recordatorio_12h_fecha_enviado,
                r.recordatorio_12h_ultramsg_id,
                r.recordatorio_12h_mensaje,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre_completo,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                c.cita_motivo
            FROM recordatorios r
            JOIN citas c ON r.id_cita = c.id_cita
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            WHERE r.id_recordatorio = %s
        """
        
        cur.execute(selectSQL, (id_recordatorio,))
        r = cur.fetchone()
        
        if not r:
            return jsonify({
                'success': False,
                'error': 'Recordatorio no encontrado'
            }), 404
        
        recordatorio = {
            'id_recordatorio': r[0],
            'id_cita': r[1],
            'cita_fecha': r[2].strftime('%d/%m/%Y') if r[2] else None,
            'cita_hora_inicio': r[3].strftime('%H:%M') if r[3] else None,
            'telefono': r[4],
            'paciente_nombre_cache': r[5],
            'inmediato': {
                'enviado': r[6],
                'fecha_enviado': r[7].strftime('%Y-%m-%d %H:%M:%S') if r[7] else None,
                'ultramsg_id': r[8],
                'mensaje': r[9]
            },
            '24h': {
                'enviado': r[10],
                'fecha_programada': r[11].strftime('%Y-%m-%d %H:%M:%S') if r[11] else None,
                'fecha_enviado': r[12].strftime('%Y-%m-%d %H:%M:%S') if r[12] else None,
                'ultramsg_id': r[13],
                'mensaje': r[14]
            },
            '12h': {
                'enviado': r[15],
                'fecha_programada': r[16].strftime('%Y-%m-%d %H:%M:%S') if r[16] else None,
                'fecha_enviado': r[17].strftime('%Y-%m-%d %H:%M:%S') if r[17] else None,
                'ultramsg_id': r[18],
                'mensaje': r[19]
            },
            'paciente_nombre_completo': r[20],
            'especialista_nombre': r[21],
            'especialidad': r[22],
            'cita_motivo': r[23]
        }
        
        return jsonify({
            'success': True,
            'data': recordatorio
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener recordatorio: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    finally:
        cur.close()
        con.close()


@recordatorioapi.route('/citas/<int:id_cita>/recordatorios', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getRecordatoriosPorCita(id_cita):
    """Obtiene el recordatorio de una cita específica (una sola fila con todos los tipos)"""
    recordatorio_dao = RecordatorioDao()
    
    try:
        app.logger.debug(f"Obteniendo recordatorio para cita {id_cita}")
        recordatorio = recordatorio_dao.getRecordatorioPorCita(id_cita)
        
        if not recordatorio:
            return jsonify({
                'success': True,
                'data': None,
                'mensaje': 'No se encontró recordatorio para esta cita'
            }), 200
        
        app.logger.info(f"Recordatorio encontrado para cita {id_cita}")
        
        return jsonify({
            'success': True,
            'data': recordatorio
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener recordatorio de cita {id_cita}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@recordatorioapi.route('/citas/<int:id_cita>/recordatorios/reenviar/<tipo>', methods=['POST'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def reenviarRecordatorioPorTipo(id_cita, tipo):
    """
    Reenvía un recordatorio manualmente por tipo
    
    Args:
        id_cita: ID de la cita
        tipo: 'inmediato', '24h', o '12h'
    """
    if tipo not in ['inmediato', '24h', '12h']:
        return jsonify({
            'success': False,
            'error': 'Tipo de recordatorio inválido. Debe ser: inmediato, 24h o 12h'
        }), 400
    
    recordatorio_dao = RecordatorioDao()
    ultramsg_service = UltraMsgService()
    
    try:
        # Verificar que el servicio está disponible
        if not ultramsg_service.client_available:
            return jsonify({
                'success': False,
                'error': 'UltraMsg no está configurado. Configure ULTRAMSG_INSTANCE_ID y ULTRAMSG_TOKEN.'
            }), 503
        
        # Obtener datos del recordatorio y la cita
        from app.conexion.Conexion import Conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        selectSQL = """
            SELECT 
                r.recordatorio_telefono,
                r.recordatorio_paciente_nombre,
                r.recordatorio_cita_fecha,
                r.recordatorio_cita_hora_inicio,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
                esp.des_especialidad,
                c.cita_motivo,
                pm.pam_tel_madre,
                pm.pam_tel_padre,
                CASE WHEN DATE_PART('year', AGE(pa_per.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor
            FROM recordatorios r
            JOIN citas c ON r.id_cita = c.id_cita
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
            JOIN pacientes pa ON c.id_paciente = pa.id_paciente
            JOIN personas pa_per ON pa.id_persona = pa_per.id_persona
            LEFT JOIN pacientes_menores pm ON pa.id_paciente = pm.id_paciente
            WHERE r.id_cita = %s
        """
        
        cur.execute(selectSQL, (id_cita,))
        r = cur.fetchone()
        
        if not r:
            return jsonify({
                'success': False,
                'error': 'Recordatorio no encontrado para esta cita'
            }), 404
        
        telefono_destino = r[0]
        es_menor = r[9]
        if es_menor:
            telefono_tutor = r[7] or r[8]
            if telefono_tutor:
                telefono_destino = telefono_tutor
                
        # Enviar recordatorio
        resultado = ultramsg_service.enviar_recordatorio_cita(
            telefono=telefono_destino,
            nombre_paciente=r[1],
            cita_fecha=r[2],
            cita_hora=r[3],
            especialista=r[4],
            especialidad=r[5],
            motivo=r[6]
        )
        
        # Manejar nuevo formato de retorno
        if len(resultado) == 4:
            success, message_id, error, tipo_error = resultado
        else:
            success, message_id, error = resultado
            tipo_error = None
        
        if success:
            # Construir mensaje
            mensaje_texto = ultramsg_service._construir_mensaje_recordatorio(
                r[1], r[2], r[3], r[4], r[5], r[6]
            )
            
            # Marcar según el tipo
            if tipo == 'inmediato':
                recordatorio_dao.marcarInmediatoEnviado(id_cita, message_id, mensaje_texto)
            elif tipo == '24h':
                recordatorio_dao.marcar24hEnviado(id_cita, message_id, mensaje_texto)
            elif tipo == '12h':
                recordatorio_dao.marcar12hEnviado(id_cita, message_id, mensaje_texto)
            
            return jsonify({
                'success': True,
                'mensaje': f'Recordatorio {tipo} reenviado exitosamente',
                'message_id': message_id
            }), 200
        else:
            error_msg = error or "Error desconocido"
            return jsonify({
                'success': False,
                'error': error_msg,
                'tipo_error': tipo_error.value if tipo_error else 'desconocido'
            }), 500
        
    except Exception as e:
        app.logger.error(f"Error al reenviar recordatorio {tipo}: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    finally:
        if 'cur' in locals():
            cur.close()
        if 'con' in locals():
            con.close()


@recordatorioapi.route('/recordatorios/estadisticas', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getEstadisticas():
    """Obtiene estadísticas de recordatorios"""
    from app.conexion.Conexion import Conexion
    from datetime import date, timedelta
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        inicio_semana = hoy - timedelta(days=hoy.weekday())
        inicio_mes = date(hoy.year, hoy.month, 1)
        
        statsSQL = """
            SELECT 
                COUNT(*) as total_recordatorios,
                COUNT(*) FILTER (WHERE recordatorio_inmediato_enviado = TRUE) as total_inmediatos_enviados,
                COUNT(*) FILTER (WHERE recordatorio_24h_enviado = TRUE) as total_24h_enviados,
                COUNT(*) FILTER (WHERE recordatorio_12h_enviado = TRUE) as total_12h_enviados,
                COUNT(*) FILTER (WHERE recordatorio_inmediato_enviado = TRUE AND DATE(recordatorio_inmediato_fecha_enviado) = %s) as inmediatos_hoy,
                COUNT(*) FILTER (WHERE recordatorio_24h_enviado = TRUE AND DATE(recordatorio_24h_fecha_enviado) = %s) as recordatorios_24h_hoy,
                COUNT(*) FILTER (WHERE recordatorio_12h_enviado = TRUE AND DATE(recordatorio_12h_fecha_enviado) = %s) as recordatorios_12h_hoy,
                COUNT(*) FILTER (WHERE recordatorio_inmediato_enviado = TRUE AND DATE(recordatorio_inmediato_fecha_enviado) >= %s) as inmediatos_semana,
                COUNT(*) FILTER (WHERE recordatorio_24h_enviado = TRUE AND DATE(recordatorio_24h_fecha_enviado) >= %s) as recordatorios_24h_semana,
                COUNT(*) FILTER (WHERE recordatorio_12h_enviado = TRUE AND DATE(recordatorio_12h_fecha_enviado) >= %s) as recordatorios_12h_semana,
                COUNT(*) FILTER (WHERE recordatorio_inmediato_enviado = TRUE AND DATE(recordatorio_inmediato_fecha_enviado) >= %s) as inmediatos_mes,
                COUNT(*) FILTER (WHERE recordatorio_24h_enviado = TRUE AND DATE(recordatorio_24h_fecha_enviado) >= %s) as recordatorios_24h_mes,
                COUNT(*) FILTER (WHERE recordatorio_12h_enviado = TRUE AND DATE(recordatorio_12h_fecha_enviado) >= %s) as recordatorios_12h_mes
            FROM recordatorios
        """
        
        cur.execute(statsSQL, (
            hoy, hoy, hoy,  # Hoy para cada tipo
            inicio_semana, inicio_semana, inicio_semana,  # Semana para cada tipo
            inicio_mes, inicio_mes, inicio_mes  # Mes para cada tipo
        ))
        stats = cur.fetchone()
        
        total = stats[0]
        total_enviados = stats[1] + stats[2] + stats[3]
        tasa_exito = (total_enviados / (total * 3) * 100) if total > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'total_recordatorios': total,
                'total_inmediatos_enviados': stats[1],
                'total_24h_enviados': stats[2],
                'total_12h_enviados': stats[3],
                'total_enviados': total_enviados,
                'inmediatos_hoy': stats[4],
                'recordatorios_24h_hoy': stats[5],
                'recordatorios_12h_hoy': stats[6],
                'inmediatos_semana': stats[7],
                'recordatorios_24h_semana': stats[8],
                'recordatorios_12h_semana': stats[9],
                'inmediatos_mes': stats[10],
                'recordatorios_24h_mes': stats[11],
                'recordatorios_12h_mes': stats[12],
                'tasa_exito': round(tasa_exito, 2)
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
    finally:
        cur.close()
        con.close()


@recordatorioapi.route('/recordatorios/procesar', methods=['POST'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def procesarRecordatorios():
    """
    Procesa recordatorios pendientes manualmente
    Ejecuta la tarea de procesamiento de recordatorios
    """
    try:
        from app.tasks.recordatorio_tasks import procesar_recordatorios_pendientes
        
        # Ejecutar procesamiento (ya maneja su propio contexto de aplicación)
        estadisticas = procesar_recordatorios_pendientes()
        
        if estadisticas is None:
            return jsonify({
                'success': False,
                'error': 'Error al procesar recordatorios: No se pudo obtener estadísticas'
            }), 500
        
        return jsonify({
            'success': True,
            'data': estadisticas,
            'mensaje': f'Procesados {estadisticas["total"]} recordatorios. Enviados: {estadisticas["enviados"]}, Fallidos: {estadisticas["fallidos"]}'
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al procesar recordatorios manualmente: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Error al procesar recordatorios: {str(e)}'
        }), 500


@recordatorioapi.route('/recordatorios/metricas', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getMetricasUltraMsg():
    """Obtiene métricas del servicio UltraMsg"""
    try:
        ultramsg_service = UltraMsgService()
        
        if not ultramsg_service.client_available:
            return jsonify({
                'success': False,
                'error': 'UltraMsg no está configurado'
            }), 503
        
        metricas = ultramsg_service.obtener_metricas()
        
        return jsonify({
            'success': True,
            'data': metricas
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener métricas: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500


@recordatorioapi.route('/recordatorios/verificar-creacion/<int:id_cita>', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def verificarRecordatoriosCita(id_cita):
    """
    Verifica si existe recordatorio para una cita
    Útil para debugging y verificación
    """
    recordatorio_dao = RecordatorioDao()
    
    try:
        recordatorio = recordatorio_dao.getRecordatorioPorCita(id_cita)
        
        # Obtener información de la cita
        from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
        cita_dao = CitaDao()
        cita = cita_dao.getCitaById(id_cita)
        
        return jsonify({
            'success': True,
            'data': {
                'id_cita': id_cita,
                'cita_info': cita,
                'recordatorio_existe': recordatorio is not None,
                'recordatorio': recordatorio,
                'resumen': {
                    'inmediato_enviado': recordatorio['inmediato_enviado'] if recordatorio else False,
                    '24h_enviado': recordatorio['24h_enviado'] if recordatorio else False,
                    '12h_enviado': recordatorio['12h_enviado'] if recordatorio else False
                } if recordatorio else None
            }
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al verificar recordatorios: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Error interno del servidor'
        }), 500
