"""
API para estadísticas del dashboard según el rol del usuario
app/modulos/dashboard/dashboard_api.py
"""
from flask import Blueprint, jsonify, session
from datetime import datetime, date, timedelta
from app.conexion.Conexion import Conexion

dashboardapi = Blueprint('dashboardapi', __name__)


@dashboardapi.route('/api/v1/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    Devuelve estadísticas personalizadas según el grupo del usuario
    """
    try:
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id')
        
        if not grupo_id or not usuario_id:
            return jsonify({
                'success': False,
                'error': 'Usuario no autenticado'
            }), 401
        
        conexion = Conexion()
        
        # IDs de grupos (ajustar según tu BD)
        ADMIN = 1
        RECEPCION = 2
        ESPECIALISTA = 3
        
        estadisticas = {}
        
        # ===============================================
        # ADMINISTRADOR - Estadísticas Globales
        # ===============================================
        if grupo_id == ADMIN:
            # Total usuarios activos
            sql_usuarios = "SELECT COUNT(*) as total FROM usuarios WHERE est_usuario = TRUE"
            total_usuarios = conexion.consultar(sql_usuarios)
            estadisticas['total_usuarios'] = total_usuarios[0]['total'] if total_usuarios else 0
            
            # Ingresos del mes actual (si tienes tabla de pagos)
            # Si NO tienes tabla de pagos, simula con cantidad de consultas * precio promedio
            sql_ingresos = """
                SELECT COUNT(*) * 150000 as ingresos 
                FROM consultas 
                WHERE EXTRACT(MONTH FROM fecha_consulta) = EXTRACT(MONTH FROM CURRENT_DATE)
                  AND EXTRACT(YEAR FROM fecha_consulta) = EXTRACT(YEAR FROM CURRENT_DATE)
            """
            ingresos = conexion.consultar(sql_ingresos)
            estadisticas['ingresos_mes'] = ingresos[0]['ingresos'] if ingresos and ingresos[0]['ingresos'] else 0
            
            # Citas de hoy
            sql_citas_hoy = """
                SELECT COUNT(*) as total 
                FROM citas 
                WHERE fecha_cita = CURRENT_DATE
                  AND estado_cita != 'cancelada'
            """
            citas_hoy = conexion.consultar(sql_citas_hoy)
            estadisticas['citas_hoy'] = citas_hoy[0]['total'] if citas_hoy else 0
            
            # Pacientes activos (con al menos una cita en los últimos 6 meses)
            sql_pacientes = """
                SELECT COUNT(DISTINCT id_paciente) as total 
                FROM citas 
                WHERE fecha_cita >= CURRENT_DATE - INTERVAL '6 months'
            """
            pacientes = conexion.consultar(sql_pacientes)
            estadisticas['pacientes_activos'] = pacientes[0]['total'] if pacientes else 0
        
        # ===============================================
        # RECEPCIONISTA - Estadísticas de Agendamiento
        # ===============================================
        elif grupo_id == RECEPCION:
            # Citas de hoy
            sql_citas_hoy = """
                SELECT COUNT(*) as total 
                FROM citas 
                WHERE fecha_cita = CURRENT_DATE
                  AND estado_cita != 'cancelada'
            """
            citas_hoy = conexion.consultar(sql_citas_hoy)
            estadisticas['citas_hoy'] = citas_hoy[0]['total'] if citas_hoy else 0
            
            # Citas pendientes de confirmar
            sql_pendientes = """
                SELECT COUNT(*) as total 
                FROM citas 
                WHERE fecha_cita >= CURRENT_DATE
                  AND (estado_cita = 'pendiente' OR estado_cita = 'agendada')
            """
            pendientes = conexion.consultar(sql_pendientes)
            estadisticas['citas_pendientes'] = pendientes[0]['total'] if pendientes else 0
            
            # Citas confirmadas para hoy
            sql_confirmadas = """
                SELECT COUNT(*) as total 
                FROM citas 
                WHERE fecha_cita = CURRENT_DATE
                  AND estado_cita = 'confirmada'
            """
            confirmadas = conexion.consultar(sql_confirmadas)
            estadisticas['citas_confirmadas'] = confirmadas[0]['total'] if confirmadas else 0
            
            # Próxima cita (hora más cercana)
            sql_proxima = """
                SELECT 
                    TO_CHAR(hora_cita, 'HH24:MI') as hora,
                    p.nom_paciente || ' ' || p.ape_paciente as paciente
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                WHERE c.fecha_cita = CURRENT_DATE
                  AND c.hora_cita > CURRENT_TIME
                  AND c.estado_cita != 'cancelada'
                ORDER BY c.hora_cita ASC
                LIMIT 1
            """
            proxima = conexion.consultar(sql_proxima)
            if proxima and len(proxima) > 0:
                estadisticas['proxima_cita'] = f"{proxima[0]['hora']} - {proxima[0]['paciente']}"
            else:
                estadisticas['proxima_cita'] = 'Sin citas pendientes'
        
        # ===============================================
        # ESPECIALISTA - Estadísticas Clínicas
        # ===============================================
        elif grupo_id == ESPECIALISTA:
            # Obtener ID del funcionario asociado al usuario
            sql_funcionario = """
                SELECT id_funcionario 
                FROM funcionarios 
                WHERE id_usuario = %s
            """
            funcionario = conexion.consultar(sql_funcionario, (usuario_id,))
            
            if funcionario and len(funcionario) > 0:
                id_funcionario = funcionario[0]['id_funcionario']
                
                # Pacientes asignados (distintos pacientes que tuvo en los últimos 6 meses)
                sql_pacientes = """
                    SELECT COUNT(DISTINCT c.id_paciente) as total
                    FROM citas c
                    WHERE c.id_funcionario = %s
                      AND c.fecha_cita >= CURRENT_DATE - INTERVAL '6 months'
                """
                pacientes = conexion.consultar(sql_pacientes, (id_funcionario,))
                estadisticas['pacientes_asignados'] = pacientes[0]['total'] if pacientes else 0
                
                # Consultas de hoy
                sql_consultas = """
                    SELECT COUNT(*) as total
                    FROM citas c
                    WHERE c.id_funcionario = %s
                      AND c.fecha_cita = CURRENT_DATE
                      AND c.estado_cita != 'cancelada'
                """
                consultas = conexion.consultar(sql_consultas, (id_funcionario,))
                estadisticas['consultas_hoy'] = consultas[0]['total'] if consultas else 0
                
                # Informes pendientes (consultas completadas sin informe final)
                # Esto depende de tu estructura - ajusta según tengas
                sql_pendientes = """
                    SELECT COUNT(*) as total
                    FROM consultas co
                    INNER JOIN citas c ON co.id_cita = c.id_cita
                    WHERE c.id_funcionario = %s
                      AND co.estado_consulta = 'en_proceso'
                """
                pendientes = conexion.consultar(sql_pendientes, (id_funcionario,))
                estadisticas['informes_pendientes'] = pendientes[0]['total'] if pendientes else 0
                
                # Próxima sesión
                sql_proxima = """
                    SELECT 
                        TO_CHAR(c.hora_cita, 'HH24:MI') as hora,
                        p.nom_paciente || ' ' || p.ape_paciente as paciente
                    FROM citas c
                    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                    WHERE c.id_funcionario = %s
                      AND c.fecha_cita = CURRENT_DATE
                      AND c.hora_cita > CURRENT_TIME
                      AND c.estado_cita != 'cancelada'
                    ORDER BY c.hora_cita ASC
                    LIMIT 1
                """
                proxima = conexion.consultar(sql_proxima, (id_funcionario,))
                if proxima and len(proxima) > 0:
                    estadisticas['proxima_sesion'] = f"{proxima[0]['hora']} - {proxima[0]['paciente']}"
                else:
                    estadisticas['proxima_sesion'] = 'Sin sesiones hoy'
            else:
                # Usuario sin funcionario asociado
                estadisticas['pacientes_asignados'] = 0
                estadisticas['consultas_hoy'] = 0
                estadisticas['informes_pendientes'] = 0
                estadisticas['proxima_sesion'] = 'Sin sesiones'
        
        conexion.desconectar()
        
        return jsonify({
            'success': True,
            **estadisticas
        })
        
    except Exception as e:
        print(f"Error en estadísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@dashboardapi.route('/api/v1/citas-hoy', methods=['GET'])
def obtener_citas_hoy():
    """
    Devuelve las citas del día actual
    """
    try:
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id')
        
        conexion = Conexion()
        
        # Si es especialista, filtrar solo sus citas
        if grupo_id == 3:  # ESPECIALISTA
            sql_funcionario = "SELECT id_funcionario FROM funcionarios WHERE id_usuario = %s"
            funcionario = conexion.consultar(sql_funcionario, (usuario_id,))
            
            if funcionario and len(funcionario) > 0:
                id_funcionario = funcionario[0]['id_funcionario']
                
                sql = """
                    SELECT 
                        TO_CHAR(c.hora_cita, 'HH24:MI') as hora,
                        p.nom_paciente || ' ' || p.ape_paciente as paciente,
                        f.nom_funcionario || ' ' || f.ape_funcionario as profesional,
                        e.des_especialidad as especialidad,
                        c.obs_cita as observacion,
                        c.estado_cita as estado
                    FROM citas c
                    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                    INNER JOIN funcionarios f ON c.id_funcionario = f.id_funcionario
                    LEFT JOIN especialidades e ON f.id_especialidad = e.id_especialidad
                    WHERE c.fecha_cita = CURRENT_DATE
                      AND c.id_funcionario = %s
                      AND c.estado_cita != 'cancelada'
                    ORDER BY c.hora_cita ASC
                """
                citas = conexion.consultar(sql, (id_funcionario,))
            else:
                citas = []
        else:
            # Admin o Recepción ven todas las citas
            sql = """
                SELECT 
                    TO_CHAR(c.hora_cita, 'HH24:MI') as hora,
                    p.nom_paciente || ' ' || p.ape_paciente as paciente,
                    f.nom_funcionario || ' ' || f.ape_funcionario as profesional,
                    e.des_especialidad as especialidad,
                    c.obs_cita as observacion,
                    c.estado_cita as estado
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN funcionarios f ON c.id_funcionario = f.id_funcionario
                LEFT JOIN especialidades e ON f.id_especialidad = e.id_especialidad
                WHERE c.fecha_cita = CURRENT_DATE
                  AND c.estado_cita != 'cancelada'
                ORDER BY c.hora_cita ASC
            """
            citas = conexion.consultar(sql)
        
        conexion.desconectar()
        
        return jsonify({
            'success': True,
            'citas': citas if citas else []
        })
        
    except Exception as e:
        print(f"Error cargando citas: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'citas': []
        }), 500


@dashboardapi.route('/api/v1/citas-manana', methods=['GET'])
def obtener_citas_manana():
    """
    Devuelve las citas de mañana
    """
    try:
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id')
        
        conexion = Conexion()
        fecha_manana = date.today() + timedelta(days=1)
        
        # Si es especialista, filtrar solo sus citas
        if grupo_id == 3:  # ESPECIALISTA
            sql_funcionario = "SELECT id_funcionario FROM funcionarios WHERE id_usuario = %s"
            funcionario = conexion.consultar(sql_funcionario, (usuario_id,))
            
            if funcionario and len(funcionario) > 0:
                id_funcionario = funcionario[0]['id_funcionario']
                
                sql = """
                    SELECT 
                        TO_CHAR(c.hora_cita, 'HH24:MI') as hora,
                        p.nom_paciente || ' ' || p.ape_paciente as paciente,
                        f.nom_funcionario || ' ' || f.ape_funcionario as profesional,
                        e.des_especialidad as especialidad,
                        c.obs_cita as observacion,
                        c.estado_cita as estado
                    FROM citas c
                    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                    INNER JOIN funcionarios f ON c.id_funcionario = f.id_funcionario
                    LEFT JOIN especialidades e ON f.id_especialidad = e.id_especialidad
                    WHERE c.fecha_cita = %s
                      AND c.id_funcionario = %s
                      AND c.estado_cita != 'cancelada'
                    ORDER BY c.hora_cita ASC
                """
                citas = conexion.consultar(sql, (fecha_manana, id_funcionario))
            else:
                citas = []
        else:
            # Admin o Recepción ven todas las citas
            sql = """
                SELECT 
                    TO_CHAR(c.hora_cita, 'HH24:MI') as hora,
                    p.nom_paciente || ' ' || p.ape_paciente as paciente,
                    f.nom_funcionario || ' ' || f.ape_funcionario as profesional,
                    e.des_especialidad as especialidad,
                    c.obs_cita as observacion,
                    c.estado_cita as estado
                FROM citas c
                INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
                INNER JOIN funcionarios f ON c.id_funcionario = f.id_funcionario
                LEFT JOIN especialidades e ON f.id_especialidad = e.id_especialidad
                WHERE c.fecha_cita = %s
                  AND c.estado_cita != 'cancelada'
                ORDER BY c.hora_cita ASC
            """
            citas = conexion.consultar(sql, (fecha_manana,))
        
        conexion.desconectar()
        
        return jsonify({
            'success': True,
            'citas': citas if citas else []
        })
        
    except Exception as e:
        print(f"Error cargando citas de mañana: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'citas': []
        }), 500