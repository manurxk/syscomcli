"""
Dashboard Unificado - Rutas de vistas y APIs con control de roles
app/routes/seguridad/dashboard.py
"""
from flask import Blueprint, render_template, jsonify, session, redirect, url_for, current_app as app
from datetime import date, datetime, timedelta
from app.conexion.Conexion import Conexion
from app.dao.DashboardDao import DashboardDao
from app.dao.AuditoriaDao import AuditoriaDao

dashboard = Blueprint('dashboard', __name__)
# ============================================================================
# FUNCIONES AUXILIARES - CONTROL DE ROLES
# ============================================================================

def es_admin():
    """Verifica si el usuario es administrador (soporta múltiples roles)"""
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_admin()
    except Exception:
        return session.get('id_grupo') == 1


def es_recepcion():
    """Verifica si el usuario es recepcionista (soporta múltiples roles)"""
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_recepcionista()
    except Exception:
        return session.get('id_grupo') == 2


def es_especialista():
    """
    Verifica si el usuario es especialista (soporta múltiples roles)
    Verifica tanto por roles como por existencia de registro en especialistas
    """
    try:
        from app.services.modulos_service import ModulosService
        from app.utils.especialista_helper import obtener_id_especialista_usuario
        modulos_service = ModulosService()
        resultado = modulos_service.es_especialista()
        app.logger.info(f"DEBUG dashboard.es_especialista: resultado ModulosService={resultado}")
        
        # Si ModulosService retorna False, verificar directamente
        if not resultado:
            id_especialista = obtener_id_especialista_usuario()
            resultado = id_especialista is not None
            app.logger.info(f"DEBUG dashboard.es_especialista: verificación directa, id_especialista={id_especialista}, resultado={resultado}")
        
        return resultado
    except Exception as e:
        app.logger.error(f"Error en es_especialista: {str(e)}", exc_info=True)
        # Fallback: verificar por grupo_id o por registro en especialistas
        grupo_id = session.get('id_grupo')
        if grupo_id == 3:
            return True
        
        # Si no es grupo 3, verificar si tiene registro en especialistas
        try:
            from app.utils.especialista_helper import obtener_id_especialista_usuario
            id_especialista = obtener_id_especialista_usuario()
            app.logger.info(f"DEBUG dashboard.es_especialista fallback: id_especialista={id_especialista}")
            return id_especialista is not None
        except Exception as e2:
            app.logger.error(f"Error en fallback es_especialista: {str(e2)}")
            return False


def es_ventas():
    """Verifica si el usuario es del grupo Ventas (soporta múltiples roles)"""
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_ventas()
    except Exception:
        return session.get('id_grupo') == 4


def es_superadmin():
    """Verifica si el usuario es Superadministrador (soporta múltiples roles)"""
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_superadmin()
    except Exception:
        grupo_id = session.get('id_grupo')
        grupo_nombre = session.get('grupo', '').upper()
        
        if grupo_id == 5:
            return True
        
        return grupo_nombre == 'SUPERADMINISTRADOR'


def obtener_nombre_usuario():
    """Obtiene el nombre del usuario de la sesión"""
    return session.get('nombre_persona', 'Usuario')


# ============================================================================
# RUTAS DE VISTAS
# ============================================================================

@dashboard.route('/')
@dashboard.route('/dashboard')
def index():
    """
    Página principal del dashboard - Dashboard dinámico según el rol del usuario
    """
    # Verificar si el usuario está logueado
    # CORREGIDO: Usar 'id_usuario' en lugar de 'id'
    if 'id_usuario' not in session:
        return redirect(url_for('login.login'))
    
    # Obtener módulos y widgets del usuario usando el servicio de módulos
    try:
        from app.services.modulos_service import ModulosService
        from app.services.modulos_detalles import obtener_modulos_con_detalles
        
        modulos_service = ModulosService()
        modulos_accesibles = list(modulos_service.obtener_modulos_usuario())
        widgets_disponibles = list(modulos_service.obtener_widgets_usuario())
        roles_usuario = modulos_service.obtener_roles_activos_usuario()
        modulos_con_detalles = obtener_modulos_con_detalles(modulos_accesibles)
    except Exception as e:
        app.logger.error(f"Error al obtener módulos del usuario: {str(e)}")
        modulos_accesibles = []
        widgets_disponibles = []
        roles_usuario = []
        modulos_con_detalles = []
    
    # Preparar datos del usuario para el template
    data_usuario = {
        "esAdmin": es_admin(),
        "esRecepcion": es_recepcion(),
        "esEspecialista": es_especialista(),
        "esVentas": es_ventas(),
        "esSuperadmin": es_superadmin(),
        "grupoId": session.get('id_grupo', 0),
        "nombre": obtener_nombre_usuario(),
        "modulos": modulos_accesibles,
        "widgets": widgets_disponibles,
        "roles": roles_usuario,
        "modulos_con_detalles": modulos_con_detalles
    }
    
    return render_template('inicio.html', data_usuario=data_usuario)


@dashboard.route('/referenciales')
def referenciales():
    """
    Vista consolidada de todos los referenciales del sistema
    Solo para administradores
    """
    if not es_admin() and not es_superadmin():
        return redirect(url_for('dashboard.index'))
    
    return render_template('referenciales.html')


# ============================================================================
# API - ESTADÍSTICAS SEGÚN ROL DEL USUARIO
# ============================================================================

@dashboard.route('/api/v1/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    Devuelve estadísticas personalizadas según el grupo del usuario
    ADMIN: Total usuarios, ingresos, citas hoy, pacientes activos
    RECEPCION: Citas hoy, pendientes, confirmadas, próxima cita
    ESPECIALISTA: Pacientes asignados, consultas hoy, informes pendientes, próxima sesión
    """
    try:
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id_usuario')  # CORREGIDO
        
        if not grupo_id or not usuario_id:
            return jsonify({
                'success': False,
                'error': 'Usuario no autenticado'
            }), 401
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        hoy = date.today()
        estadisticas = {}
        
        # Verificar si el usuario tiene múltiples roles
        es_admin_rol = es_admin()
        es_especialista_rol = es_especialista()
        
        dashboard_dao = DashboardDao()
        auditoria_dao = AuditoriaDao()
        
        # ===============================================
        # ADMINISTRADOR Y SUPERADMINISTRADOR - Estadísticas Globales
        # ===============================================
        if es_admin_rol or es_superadmin():  # ADMIN o SUPERADMIN
            # Total usuarios activos
            cur.execute("SELECT COUNT(*) FROM usuarios WHERE usu_estado = TRUE")
            estadisticas['total_usuarios'] = cur.fetchone()[0]
            
            # MÉTRICAS ESTRATÉGICAS
            # ===============================================
            
            # Métrica base para todos los admin
            estadisticas['ingresos_mes'] = dashboard_dao.get_ingresos_mes_actual()

            if es_superadmin():
                # Ingresos mes actual (Real)
                estadisticas['ingresos_mes'] = dashboard_dao.get_ingresos_mes_actual()
                
                # Ingresos mes anterior (Comparativa)
                primer_dia_mes = hoy.replace(day=1)
                ultimo_dia_mes_ant = primer_dia_mes - timedelta(days=1)
                primer_dia_mes_ant = ultimo_dia_mes_ant.replace(day=1)
                cur.execute("""
                    SELECT COALESCE(SUM(factura_total), 0.0)
                    FROM facturas
                    WHERE fecha_factura >= %s AND fecha_factura <= %s
                """, (primer_dia_mes_ant, ultimo_dia_mes_ant))
                estadisticas['ingresos_mes_anterior'] = float(cur.fetchone()[0])
                
                # Pacientes nuevos este mes (Real)
                estadisticas['pacientes_nuevos_mes'] = dashboard_dao.get_pacientes_nuevos_mes()

                # Tasa de ocupación (Real)
                estadisticas['tasa_ocupacion_mes'] = dashboard_dao.get_tasa_ocupacion()
                
                # Alertas de seguridad (Real)
                estadisticas['alertas_seguridad'] = dashboard_dao.get_alertas_seguridad()

                # Citas por especialidad (Real)
                estadisticas['citas_por_especialidad'] = dashboard_dao.get_conteo_citas_por_especialidad()

                # Actividad reciente (Real, usando AuditoriaDao)
                estadisticas['actividad_reciente'] = auditoria_dao.obtener_actividad_sistema(limite=10)

                # Tendencia de citas (Últimos 7 días)
                tendencia = []
                for i in range(6, -1, -1):
                    dia = hoy - timedelta(days=i)
                    cur.execute("""
                        SELECT COUNT(*) 
                        FROM citas 
                        WHERE cita_fecha = %s AND cita_activo = TRUE
                    """, (dia,))
                    count = cur.fetchone()[0]
                    tendencia.append({
                        'fecha': dia.strftime('%d/%m'),
                        'cantidad': count
                    })
                estadisticas['tendencia_citas'] = tendencia

            # Citas de hoy (Para Admin mantiene vista operativa, Superadmin usará stats generales)
            cur.execute("""
                SELECT COUNT(*) 
                FROM citas 
                WHERE cita_fecha = %s
                  AND cita_activo = TRUE
            """, (hoy,))
            estadisticas['citas_hoy'] = cur.fetchone()[0]
            
            # Pacientes activos (con al menos una cita en los últimos 6 meses)
            seis_meses_atras = hoy - timedelta(days=180)
            cur.execute("""
                SELECT COUNT(DISTINCT id_paciente) 
                FROM citas 
                WHERE cita_fecha >= %s
                  AND cita_activo = TRUE
            """, (seis_meses_atras,))
            estadisticas['pacientes_activos'] = cur.fetchone()[0]
            
            # Si también es especialista, agregar estadísticas de especialista
            if es_especialista_rol:
                # Obtener ID del especialista asociado al usuario
                try:
                    cur.execute("""
                        SELECT e.id_especialista 
                        FROM especialistas e
                        JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                        JOIN usuarios u ON u.id_funcionario = f.id_funcionario
                        WHERE u.id_usuario = %s
                    """, (usuario_id,))
                    resultado = cur.fetchone()
                except Exception as e:
                    app.logger.error(f"Error al obtener id_especialista: {str(e)}")
                    resultado = None
                
                if resultado:
                    id_especialista = resultado[0]
                    
                    # Citas de hoy del especialista
                    cur.execute("""
                        SELECT COUNT(*) 
                        FROM citas 
                        WHERE id_especialista = %s
                          AND cita_fecha = %s
                          AND cita_activo = TRUE
                    """, (id_especialista, hoy))
                    estadisticas['citas_hoy_especialista'] = cur.fetchone()[0]
                    
                    # Pacientes asignados (distintos en los últimos 6 meses)
                    seis_meses_atras = hoy - timedelta(days=180)
                    cur.execute("""
                        SELECT COUNT(DISTINCT id_paciente)
                        FROM citas
                        WHERE id_especialista = %s
                          AND cita_fecha >= %s
                          AND cita_activo = TRUE
                    """, (id_especialista, seis_meses_atras))
                    estadisticas['pacientes_asignados'] = cur.fetchone()[0]
                    
                    # Historias clínicas pendientes
                    cur.execute("""
                        SELECT COUNT(*)
                        FROM citas c
                        JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                        WHERE c.id_especialista = %s
                          AND (ec.est_cita_nombre = 'COMPLETADA' OR ec.est_cita_nombre = 'ATENDIDA')
                          AND (c.cita_observaciones IS NULL OR c.cita_observaciones = '')
                          AND c.cita_activo = TRUE
                    """, (id_especialista,))
                    estadisticas['historias_pendientes'] = cur.fetchone()[0]

                    # Si es Admin+Especialista (pero NO Superadmin), le damos el dashboard estratégico personal
                    if not es_superadmin():
                        estadisticas['ingresos_mes'] = dashboard_dao.get_ingresos_mes_actual()
                        estadisticas['pacientes_nuevos_mes'] = dashboard_dao.get_pacientes_nuevos_mes()
                        estadisticas['tasa_ocupacion_mes'] = dashboard_dao.get_tasa_ocupacion()
                        estadisticas['alertas_seguridad'] = dashboard_dao.get_alertas_seguridad()
                        estadisticas['citas_por_especialidad'] = dashboard_dao.get_conteo_citas_por_especialidad()
                        estadisticas['actividad_reciente'] = auditoria_dao.obtener_actividad_sistema(limite=10)

                        tendencia = []
                        for i in range(6, -1, -1):
                            dia = hoy - timedelta(days=i)
                            cur.execute("""
                                SELECT COUNT(*) 
                                FROM citas 
                                WHERE id_especialista = %s AND cita_fecha = %s AND cita_activo = TRUE
                            """, (id_especialista, dia))
                            count = cur.fetchone()[0]
                            tendencia.append({
                                'fecha': dia.strftime('%d/%m'),
                                'cantidad': count
                            })
                        estadisticas['tendencia_citas'] = tendencia
        
        # ===============================================
        # RECEPCIONISTA - Estadísticas de Agendamiento
        # ===============================================
        elif grupo_id == 2:  # RECEPCION
            # Citas de hoy
            cur.execute("""
                SELECT COUNT(*) 
                FROM citas 
                WHERE cita_fecha = %s
                  AND cita_activo = TRUE
            """, (hoy,))
            estadisticas['citas_hoy'] = cur.fetchone()[0]
            
            # Citas pendientes de confirmar
            cur.execute("""
                SELECT COUNT(*) 
                FROM citas c
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.cita_fecha >= %s
                  AND ec.est_cita_nombre IN ('PENDIENTE', 'AGENDADA')
                  AND c.cita_activo = TRUE
            """, (hoy,))
            estadisticas['citas_pendientes'] = cur.fetchone()[0]
            
            # Citas confirmadas para hoy
            cur.execute("""
                SELECT COUNT(*) 
                FROM citas c
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.cita_fecha = %s
                  AND ec.est_cita_nombre = 'CONFIRMADA'
                  AND c.cita_activo = TRUE
            """, (hoy,))
            estadisticas['citas_confirmadas'] = cur.fetchone()[0]
            
            # Pacientes activos
            seis_meses_atras = hoy - timedelta(days=180)
            cur.execute("""
                SELECT COUNT(DISTINCT id_paciente) 
                FROM citas 
                WHERE cita_fecha >= %s
                  AND cita_activo = TRUE
            """, (seis_meses_atras,))
            estadisticas['pacientes_activos'] = cur.fetchone()[0]

            # ===============================================
            # MÉTRICAS ESTRATÉGICAS PARA RECEPCIÓN - NUEVO
            # ===============================================

            estadisticas['ingresos_mes'] = dashboard_dao.get_ingresos_mes_actual()
            estadisticas['pacientes_nuevos_mes'] = dashboard_dao.get_pacientes_nuevos_mes()
            estadisticas['tasa_ocupacion_mes'] = dashboard_dao.get_tasa_ocupacion()
            estadisticas['alertas_seguridad'] = dashboard_dao.get_alertas_seguridad()
            estadisticas['citas_por_especialidad'] = dashboard_dao.get_conteo_citas_por_especialidad()
            estadisticas['actividad_reciente'] = auditoria_dao.obtener_actividad_sistema(limite=10)
            
            
            tendencia = []
            for i in range(6, -1, -1):
                dia = hoy - timedelta(days=i)
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM citas 
                    WHERE cita_fecha = %s AND cita_activo = TRUE
                """, (dia,))
                count = cur.fetchone()[0]
                tendencia.append({
                    'fecha': dia.strftime('%d/%m'),
                    'cantidad': count
                })
            estadisticas['tendencia_citas'] = tendencia
        
        # ===============================================
        # ESPECIALISTA - Estadísticas Clínicas
        # ===============================================
        elif es_especialista_rol:  # ESPECIALISTA (puede ser solo especialista o admin+especialista)
            # Obtener ID del especialista asociado al usuario
            try:
                cur.execute("""
                    SELECT e.id_especialista 
                    FROM especialistas e
                    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                    JOIN usuarios u ON u.id_funcionario = f.id_funcionario
                    WHERE u.id_usuario = %s
                """, (usuario_id,))
                resultado = cur.fetchone()
            except Exception as e:
                app.logger.error(f"Error al obtener id_especialista (Especialista block): {str(e)}")
                resultado = None
            
            if resultado:
                id_especialista = resultado[0]
                
                # Citas de hoy del especialista
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM citas 
                    WHERE id_especialista = %s
                      AND cita_fecha = %s
                      AND cita_activo = TRUE
                """, (id_especialista, hoy))
                estadisticas['citas_hoy'] = cur.fetchone()[0]
                
                # Pacientes asignados (distintos en los últimos 6 meses)
                seis_meses_atras = hoy - timedelta(days=180)
                cur.execute("""
                    SELECT COUNT(DISTINCT id_paciente)
                    FROM citas
                    WHERE id_especialista = %s
                      AND cita_fecha >= %s
                      AND cita_activo = TRUE
                """, (id_especialista, seis_meses_atras))
                estadisticas['pacientes_asignados'] = cur.fetchone()[0]
                
                # Historias clínicas pendientes
                cur.execute("""
                    SELECT COUNT(*)
                    FROM citas c
                    JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                    WHERE c.id_especialista = %s
                      AND (ec.est_cita_nombre = 'COMPLETADA' OR ec.est_cita_nombre = 'ATENDIDA')
                      AND (c.cita_observaciones IS NULL OR c.cita_observaciones = '')
                      AND c.cita_activo = TRUE
                """, (id_especialista,))
                estadisticas['historias_pendientes'] = cur.fetchone()[0]

                # ===============================================
                # MÉTRICAS ESTRATÉGICAS PARA ESPECIALISTA - NUEVO
                # ===============================================

                estadisticas['ingresos_mes'] = dashboard_dao.get_ingresos_mes_actual()
                estadisticas['pacientes_nuevos_mes'] = dashboard_dao.get_pacientes_nuevos_mes()
                estadisticas['tasa_ocupacion_mes'] = dashboard_dao.get_tasa_ocupacion()
                estadisticas['alertas_seguridad'] = dashboard_dao.get_alertas_seguridad()
                estadisticas['citas_por_especialidad'] = dashboard_dao.get_conteo_citas_por_especialidad()
                estadisticas['actividad_reciente'] = auditoria_dao.obtener_actividad_sistema(limite=10)

                # Tendencia de citas (Últimos 7 días) del Especialista
                tendencia = []
                for i in range(6, -1, -1):
                    dia = hoy - timedelta(days=i)
                    cur.execute("""
                        SELECT COUNT(*) 
                        FROM citas 
                        WHERE id_especialista = %s AND cita_fecha = %s AND cita_activo = TRUE
                    """, (id_especialista, dia))
                    count = cur.fetchone()[0]
                    tendencia.append({
                        'fecha': dia.strftime('%d/%m'),
                        'cantidad': count
                    })
                estadisticas['tendencia_citas'] = tendencia

            else:
                # Usuario sin especialista asociado
                estadisticas['citas_hoy'] = 0
                estadisticas['pacientes_asignados'] = 0
                estadisticas['historias_pendientes'] = 0
        
        # ===============================================
        # VENTAS - Estadísticas de Facturación y Ventas
        # ===============================================
        elif grupo_id == 4:  # VENTAS
            primer_dia_mes = hoy.replace(day=1)
            
            # Facturas del mes actual
            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM facturas 
                    WHERE fecha_factura >= %s
                """, (primer_dia_mes,))
                estadisticas['facturas_mes'] = cur.fetchone()[0]
            except Exception:
                estadisticas['facturas_mes'] = 0
            
            # Ventas del mes actual (total facturado)
            try:
                cur.execute("""
                    SELECT COALESCE(SUM(factura_total), 0) 
                    FROM facturas 
                    WHERE fecha_factura >= %s
                """, (primer_dia_mes,))
                estadisticas['ventas_mes'] = cur.fetchone()[0] or 0
            except Exception:
                estadisticas['ventas_mes'] = 0
            
            # Facturas de hoy
            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM facturas 
                    WHERE DATE(fecha_factura) = %s
                """, (hoy,))
                estadisticas['facturas_hoy'] = cur.fetchone()[0]
            except Exception:
                estadisticas['facturas_hoy'] = 0
            
            # Ventas de hoy (total facturado hoy)
            try:
                cur.execute("""
                    SELECT COALESCE(SUM(factura_total), 0) 
                    FROM facturas 
                    WHERE DATE(fecha_factura) = %s
                """, (hoy,))
                estadisticas['ventas_hoy'] = cur.fetchone()[0] or 0
            except Exception:
                estadisticas['ventas_hoy'] = 0
            
            # Cuentas por cobrar pendientes
            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM cuentas_cobrar 
                    WHERE fecha_vencimiento >= %s
                      AND monto_pendiente > 0
                """, (hoy,))
                estadisticas['cuentas_cobrar'] = cur.fetchone()[0]
            except Exception:
                estadisticas['cuentas_cobrar'] = 0
            
            # Pedidos pendientes
            try:
                cur.execute("""
                    SELECT COUNT(*) 
                    FROM pedidos 
                    WHERE est_pedido IN (SELECT id_estado_pedido FROM estados_pedido WHERE des_estado_pedido LIKE '%PENDIENTE%')
                """)
                estadisticas['pedidos_pendientes'] = cur.fetchone()[0]
            except Exception:
                estadisticas['pedidos_pendientes'] = 0
        
        cur.close()
        con.close()
        
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


# ============================================================================
# API - ESTADÍSTICAS GENERALES (Para widgets del dashboard)
# ============================================================================

@dashboard.route('/api/estadisticas')
def estadisticas_generales():
    """API para obtener estadísticas generales del dashboard (widgets)"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        
        # 1. Citas de hoy
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas 
            WHERE cita_fecha = %s 
                AND cita_activo = TRUE
        """, (hoy,))
        citas_hoy = cur.fetchone()[0]
        
        # 2. Pacientes activos (con al menos 1 cita en los últimos 6 meses)
        seis_meses_atras = hoy - timedelta(days=180)
        cur.execute("""
            SELECT COUNT(DISTINCT id_paciente) 
            FROM citas 
            WHERE cita_fecha >= %s 
                AND cita_activo = TRUE
        """, (seis_meses_atras,))
        pacientes_activos = cur.fetchone()[0]
        
        # 3. Profesionales activos (especialistas)
        cur.execute("""
            SELECT COUNT(*) 
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            WHERE f.fun_estado = TRUE
        """)
        profesionales = cur.fetchone()[0]
        
        # 4. Citas pendientes (estado PENDIENTE o sin confirmar)
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= %s 
                AND ec.est_cita_nombre IN ('PENDIENTE', 'CONFIRMADA')
                AND c.cita_activo = TRUE
        """, (hoy,))
        pendientes = cur.fetchone()[0]
        
        return jsonify({
            'success': True,
            'citas_hoy': citas_hoy,
            'pacientes_activos': pacientes_activos,
            'profesionales': profesionales,
            'pendientes': pendientes
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


# ============================================================================
# API - CITAS
# ============================================================================

@dashboard.route('/api/v1/citas-hoy')
def citas_hoy():
    """API para obtener las citas del día actual"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id_usuario')  # CORREGIDO
        
        # Si es especialista, filtrar solo sus citas (puede ser admin+especialista)
        if es_especialista():
            # Usar el helper que ya funciona correctamente
            from app.utils.especialista_helper import obtener_id_especialista_usuario
            id_especialista = obtener_id_especialista_usuario()
            
            if id_especialista:
                citasSQL = """
                    SELECT
                        c.id_cita,
                        c.cita_hora_inicio,
                        CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                        c.id_paciente,
                        CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                        c.id_especialista,
                        esp.des_especialidad,
                        ec.est_cita_nombre,
                        ec.est_cita_color,
                        c.cita_observaciones
                    FROM citas c
                    JOIN pacientes p ON c.id_paciente = p.id_paciente
                    JOIN personas pp ON p.id_persona = pp.id_persona
                    JOIN especialistas e ON c.id_especialista = e.id_especialista
                    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                    JOIN personas pe ON f.id_persona = pe.id_persona
                    JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                    JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                    WHERE c.cita_fecha = %s
                        AND c.id_especialista = %s
                        AND c.cita_activo = TRUE
                    ORDER BY c.cita_hora_inicio
                """
                cur.execute(citasSQL, (hoy, id_especialista))
            else:
                app.logger.warning(f"DEBUG citas_hoy: No se encontró id_especialista para usuario_id={usuario_id}")
                return jsonify({'success': True, 'citas': [], 'total': 0})
        else:
            # Admin o Recepción ven todas las citas
            citasSQL = """
                SELECT
                    c.id_cita,
                    c.cita_hora_inicio,
                    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                    c.id_paciente,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                    c.id_especialista,
                    esp.des_especialidad,
                    ec.est_cita_nombre,
                    ec.est_cita_color,
                    c.cita_observaciones
                FROM citas c
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.cita_fecha = %s
                    AND c.cita_activo = TRUE
                ORDER BY c.cita_hora_inicio
            """
            cur.execute(citasSQL, (hoy,))
        
        citas = cur.fetchall()
        
        citas_data = []
        for cita in citas:
            # Mapear el estado
            estado_nombre = cita[7].lower()
            if 'confirmada' in estado_nombre or 'confirm' in estado_nombre:
                estado = 'confirmada'
            elif 'pendiente' in estado_nombre or 'pend' in estado_nombre:
                estado = 'pendiente'
            elif 'completada' in estado_nombre or 'atendida' in estado_nombre:
                estado = 'completada'
            elif 'cancelada' in estado_nombre or 'cancel' in estado_nombre:
                estado = 'cancelada'
            else:
                estado = 'pendiente'
            
            citas_data.append({
                'id': cita[0],
                'hora': cita[1].strftime('%H:%M') if cita[1] else 'N/A',
                'paciente': cita[2],
                'paciente_id': cita[3],
                'profesional': cita[4],
                'profesional_id': cita[5],
                'especialidad': cita[6],
                'estado': estado,
                'estado_original': cita[7],
                'color': cita[8],
                'observacion': cita[9] or ''
            })
        
        return jsonify({
            'success': True,
            'citas': citas_data,
            'total': len(citas_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


@dashboard.route('/api/v1/citas-manana')
def citas_manana():
    """API para obtener las citas de mañana"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        manana = date.today() + timedelta(days=1)
        grupo_id = session.get('id_grupo')
        usuario_id = session.get('id_usuario')  # CORREGIDO
        
        # Si es especialista, filtrar solo sus citas (puede ser admin+especialista)
        if es_especialista():
            # Usar el helper que ya funciona correctamente
            from app.utils.especialista_helper import obtener_id_especialista_usuario
            id_especialista = obtener_id_especialista_usuario()
            
            if id_especialista:
                citasSQL = """
                    SELECT
                        c.id_cita,
                        c.cita_hora_inicio,
                        CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                        c.id_paciente,
                        CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                        c.id_especialista,
                        esp.des_especialidad,
                        ec.est_cita_nombre,
                        ec.est_cita_color,
                        c.cita_observaciones
                    FROM citas c
                    JOIN pacientes p ON c.id_paciente = p.id_paciente
                    JOIN personas pp ON p.id_persona = pp.id_persona
                    JOIN especialistas e ON c.id_especialista = e.id_especialista
                    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                    JOIN personas pe ON f.id_persona = pe.id_persona
                    JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                    JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                    WHERE c.cita_fecha = %s
                        AND c.id_especialista = %s
                        AND c.cita_activo = TRUE
                    ORDER BY c.cita_hora_inicio
                """
                cur.execute(citasSQL, (manana, id_especialista))
            else:
                app.logger.warning(f"DEBUG citas_manana: No se encontró id_especialista para usuario_id={usuario_id}")
                return jsonify({'success': True, 'citas': [], 'total': 0})
        else:
            # Admin o Recepción ven todas las citas
            citasSQL = """
                SELECT
                    c.id_cita,
                    c.cita_hora_inicio,
                    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                    c.id_paciente,
                    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                    c.id_especialista,
                    esp.des_especialidad,
                    ec.est_cita_nombre,
                    ec.est_cita_color,
                    c.cita_observaciones
                FROM citas c
                JOIN pacientes p ON c.id_paciente = p.id_paciente
                JOIN personas pp ON p.id_persona = pp.id_persona
                JOIN especialistas e ON c.id_especialista = e.id_especialista
                JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
                JOIN personas pe ON f.id_persona = pe.id_persona
                JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
                JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
                WHERE c.cita_fecha = %s
                    AND c.cita_activo = TRUE
                ORDER BY c.cita_hora_inicio
            """
            cur.execute(citasSQL, (manana,))
        
        citas = cur.fetchall()
        
        citas_data = []
        for cita in citas:
            # Mapear el estado
            estado_nombre = cita[7].lower()
            if 'confirmada' in estado_nombre or 'confirm' in estado_nombre:
                estado = 'confirmada'
            elif 'pendiente' in estado_nombre or 'pend' in estado_nombre:
                estado = 'pendiente'
            elif 'completada' in estado_nombre or 'atendida' in estado_nombre:
                estado = 'completada'
            elif 'cancelada' in estado_nombre or 'cancel' in estado_nombre:
                estado = 'cancelada'
            else:
                estado = 'pendiente'
            
            citas_data.append({
                'id': cita[0],
                'hora': cita[1].strftime('%H:%M') if cita[1] else 'N/A',
                'paciente': cita[2],
                'paciente_id': cita[3],
                'profesional': cita[4],
                'profesional_id': cita[5],
                'especialidad': cita[6],
                'estado': estado,
                'estado_original': cita[7],
                'color': cita[8],
                'observacion': cita[9] or ''
            })
        
        return jsonify({
            'success': True,
            'citas': citas_data,
            'total': len(citas_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


# ============================================================================
# API - PROXIMAS CITAS (Los siguientes endpoints NO necesitan cambios)
# ============================================================================

@dashboard.route('/api/proximas-citas')
def proximas_citas():
    """API para obtener las próximas citas (próximos 7 días)"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        semana_siguiente = hoy + timedelta(days=7)
        
        citasSQL = """
            SELECT
                c.id_cita,
                c.cita_fecha,
                c.cita_hora_inicio,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                ec.est_cita_nombre
            FROM citas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha BETWEEN %s AND %s
                AND ec.est_cita_nombre IN ('PENDIENTE', 'CONFIRMADA')
                AND c.cita_activo = TRUE
            ORDER BY c.cita_fecha, c.cita_hora_inicio
            LIMIT 10
        """
        
        cur.execute(citasSQL, (hoy, semana_siguiente))
        citas = cur.fetchall()
        
        citas_data = []
        for cita in citas:
            citas_data.append({
                'id': cita[0],
                'fecha': cita[1].strftime('%d/%m/%Y'),
                'hora': cita[2].strftime('%H:%M') if cita[2] else 'N/A',
                'paciente': cita[3],
                'profesional': cita[4],
                'estado': cita[5]
            })
        
        return jsonify({
            'success': True,
            'citas': citas_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


# ============================================================================
# RESTO DE LAS APIs (No necesitan cambios ya que no usan id_usuario)
# ============================================================================

@dashboard.route('/api/debug-especialista', methods=['GET'])
def debug_especialista():
    """Endpoint de debug para verificar si el usuario es especialista"""
    from app.utils.especialista_helper import obtener_id_especialista_usuario, es_especialista
    from app.utils.template_helpers import es_especialista as es_especialista_template
    from app.services.modulos_service import ModulosService
    
    usuario_id = session.get('id_usuario')
    grupo_id = session.get('id_grupo')
    grupo_nombre = session.get('grupo', '')
    
    # Obtener información del especialista
    id_especialista = obtener_id_especialista_usuario()
    
    # Verificar con diferentes métodos
    modulos_service = ModulosService()
    es_especialista_modulos = modulos_service.es_especialista()
    es_especialista_helper = es_especialista()
    es_especialista_template_func = es_especialista_template()
    
    # Verificar en BD directamente
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    info_bd = None
    try:
        cur.execute("""
            SELECT 
                u.id_usuario,
                u.id_funcionario,
                f.id_funcionario,
                e.id_especialista,
                p.per_nombre || ' ' || p.per_apellido as nombre_completo
            FROM usuarios u
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE u.id_usuario = %s
        """, (usuario_id,))
        info_bd = cur.fetchone()
    except Exception as e:
        app.logger.error(f"Error en debug: {str(e)}")
    finally:
        cur.close()
        con.close()
    
    return jsonify({
        'usuario_id': usuario_id,
        'grupo_id': grupo_id,
        'grupo_nombre': grupo_nombre,
        'id_especialista': id_especialista,
        'es_especialista_modulos_service': es_especialista_modulos,
        'es_especialista_helper': es_especialista_helper,
        'es_especialista_template': es_especialista_template_func,
        'info_bd': {
            'id_usuario': info_bd[0] if info_bd else None,
            'id_funcionario': info_bd[1] if info_bd else None,
            'funcionario_existe': info_bd[2] is not None if info_bd else False,
            'id_especialista_bd': info_bd[3] if info_bd else None,
            'nombre_completo': info_bd[4] if info_bd else None
        } if info_bd else None
    }), 200


@dashboard.route('/api/pacientes-recientes')
def pacientes_recientes():
    """API para obtener los últimos pacientes registrados
    Si el usuario es especialista (incluso si también es admin), muestra solo sus pacientes
    """
    from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        # Verificar si debe filtrar por especialista
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        
        # Si no puede ver todos, obtener su id_especialista (funciona incluso si es admin+especialista)
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
        
        pacientesSQL = """
            SELECT
                pac.id_paciente,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
                p.per_cedula,
                p.per_telefono,
                p.per_fecha_inscripcion,
                (SELECT COUNT(*) FROM citas WHERE id_paciente = pac.id_paciente AND cita_activo = TRUE) as total_citas,
                (SELECT MAX(cita_fecha) FROM citas WHERE id_paciente = pac.id_paciente AND cita_activo = TRUE) as ultima_cita
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
        """
        
        # Agregar filtro por especialista si aplica
        if id_especialista:
            pacientesSQL += """
                INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
                WHERE pp.id_especialista = %s AND pp.activo = TRUE
            """
            pacientesSQL += " ORDER BY p.per_fecha_inscripcion DESC LIMIT 5"
            cur.execute(pacientesSQL, (id_especialista,))
        else:
            pacientesSQL += " ORDER BY p.per_fecha_inscripcion DESC LIMIT 5"
            cur.execute(pacientesSQL)
        
        pacientes = cur.fetchall()
        
        pacientes_data = []
        for pac in pacientes:
            pacientes_data.append({
                'id': pac[0],
                'nombre': pac[1],
                'cedula': pac[2],
                'telefono': pac[3] or 'N/A',
                'fecha_registro': pac[4].strftime('%d/%m/%Y') if pac[4] else 'N/A',
                'total_citas': pac[5],
                'ultima_cita': pac[6].strftime('%d/%m/%Y') if pac[6] else 'Sin citas'
            })
        
        return jsonify({
            'success': True,
            'pacientes': pacientes_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()




# ============================================================================
# API - ESTADÍSTICAS ADICIONALES
# ============================================================================

@dashboard.route('/api/estadisticas-mensuales')
def estadisticas_mensuales():
    """API para obtener estadísticas del mes actual"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        primer_dia_mes = hoy.replace(day=1)
        
        # Citas del mes
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas 
            WHERE cita_fecha >= %s 
                AND cita_activo = TRUE
        """, (primer_dia_mes,))
        citas_mes = cur.fetchone()[0]
        
        # Nuevos pacientes del mes
        cur.execute("""
            SELECT COUNT(*) 
            FROM personas 
            WHERE per_fecha_inscripcion >= %s
        """, (primer_dia_mes,))
        nuevos_pacientes = cur.fetchone()[0]
        
        # Citas completadas del mes
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= %s
                AND (ec.est_cita_nombre = 'COMPLETADA' OR ec.est_cita_nombre = 'ATENDIDA')
                AND c.cita_activo = TRUE
        """, (primer_dia_mes,))
        citas_completadas = cur.fetchone()[0]
        
        # Citas canceladas del mes
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha >= %s
                AND ec.est_cita_nombre = 'CANCELADA'
                AND c.cita_activo = TRUE
        """, (primer_dia_mes,))
        citas_canceladas = cur.fetchone()[0]
        
        # Calcular tasa de asistencia
        tasa_asistencia = 0
        if citas_mes > 0:
            tasa_asistencia = round((citas_completadas / citas_mes) * 100, 2)
        
        return jsonify({
            'success': True,
            'citas_mes': citas_mes,
            'nuevos_pacientes': nuevos_pacientes,
            'citas_completadas': citas_completadas,
            'citas_canceladas': citas_canceladas,
            'tasa_asistencia': tasa_asistencia
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


@dashboard.route('/api/especialidades-populares')
def especialidades_populares():
    """API para obtener las especialidades más solicitadas"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        un_mes_atras = date.today() - timedelta(days=30)
        
        especialidadesSQL = """
            SELECT 
                esp.des_especialidad,
                COUNT(c.id_cita) as total
            FROM especialidades esp
            JOIN citas c ON c.id_especialidad = esp.id_especialidad
            WHERE c.cita_fecha >= %s
                AND c.cita_activo = TRUE
            GROUP BY esp.id_especialidad, esp.des_especialidad
            ORDER BY COUNT(c.id_cita) DESC
            LIMIT 5
        """
        
        cur.execute(especialidadesSQL, (un_mes_atras,))
        especialidades = cur.fetchall()
        
        especialidades_data = []
        for esp in especialidades:
            especialidades_data.append({
                'especialidad': esp[0],
                'total': esp[1]
            })
        
        return jsonify({
            'success': True,
            'especialidades': especialidades_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


@dashboard.route('/api/profesionales-activos')
def profesionales_activos():
    """API para obtener profesionales activos con sus estadísticas"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        primer_dia_mes = hoy.replace(day=1)
        
        profesionalesSQL = """
            SELECT
                e.id_especialista,
                CONCAT(p.per_nombre, ' ', p.per_apellido) AS nombre_completo,
                esp.des_especialidad,
                (SELECT COUNT(*) FROM citas WHERE id_especialista = e.id_especialista 
                 AND cita_fecha = %s AND cita_activo = TRUE) as citas_hoy,
                (SELECT COUNT(*) FROM citas WHERE id_especialista = e.id_especialista 
                 AND cita_fecha >= %s AND cita_activo = TRUE) as citas_mes
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialidades esp ON e.id_especialidad = esp.id_especialidad
            WHERE f.fun_estado = TRUE
            ORDER BY p.per_nombre
        """
        
        cur.execute(profesionalesSQL, (hoy, primer_dia_mes))
        profesionales = cur.fetchall()
        
        profesionales_data = []
        for prof in profesionales:
            profesionales_data.append({
                'id': prof[0],
                'nombre': prof[1],
                'especialidad': prof[2] or 'N/A',
                'citas_hoy': prof[3],
                'citas_mes': prof[4]
            })
        
        return jsonify({
            'success': True,
            'profesionales': profesionales_data
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()


@dashboard.route('/api/alertas')
def alertas():
    """API para obtener alertas y notificaciones importantes"""
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        hoy = date.today()
        manana = hoy + timedelta(days=1)
        alertas_data = []
        
        # 1. Citas sin confirmar para mañana
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha = %s
                AND ec.est_cita_nombre = 'PENDIENTE'
                AND c.cita_activo = TRUE
        """, (manana,))
        
        citas_sin_confirmar = cur.fetchone()[0]
        if citas_sin_confirmar > 0:
            alertas_data.append({
                'tipo': 'warning',
                'mensaje': f'{citas_sin_confirmar} cita(s) sin confirmar para mañana',
                'icono': 'exclamation-triangle'
            })
        
        # 2. Pacientes sin citas en los últimos 3 meses
        tres_meses_atras = hoy - timedelta(days=90)
        cur.execute("""
            SELECT COUNT(DISTINCT pac.id_paciente)
            FROM pacientes pac
            WHERE NOT EXISTS (
                SELECT 1 FROM citas c 
                WHERE c.id_paciente = pac.id_paciente 
                    AND c.cita_fecha >= %s
                    AND c.cita_activo = TRUE
            )
        """, (tres_meses_atras,))
        
        pacientes_sin_citas = cur.fetchone()[0]
        if pacientes_sin_citas > 0:
            alertas_data.append({
                'tipo': 'info',
                'mensaje': f'{pacientes_sin_citas} paciente(s) sin citas en 3 meses',
                'icono': 'info-circle'
            })
        
        # 3. Citas de hoy pendientes
        cur.execute("""
            SELECT COUNT(*) 
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            WHERE c.cita_fecha = %s
                AND ec.est_cita_nombre = 'PENDIENTE'
                AND c.cita_activo = TRUE
        """, (hoy,))
        
        citas_pendientes_hoy = cur.fetchone()[0]
        if citas_pendientes_hoy > 0:
            alertas_data.append({
                'tipo': 'primary',
                'mensaje': f'{citas_pendientes_hoy} cita(s) pendiente(s) hoy',
                'icono': 'calendar-check'
            })
        
        return jsonify({
            'success': True,
            'alertas': alertas_data,
            'total': len(alertas_data)
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        cur.close()
        con.close()