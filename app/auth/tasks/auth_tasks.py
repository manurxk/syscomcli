"""
Tareas programadas para mantenimiento de autenticación
FASE 2: MEJORAS DE SEGURIDAD

Ejecutar con cron o scheduler:
- limpiar_sesiones_expiradas: cada 15 minutos
- limpiar_tokens_expirados: cada 1 hora
"""
from flask import current_app as app
from app.conexion.Conexion import Conexion


def limpiar_sesiones_expiradas():
    """
    Limpia sesiones expiradas usando función PostgreSQL
    Ejecutar cada 15 minutos
    """
    sql = "SELECT limpiar_sesiones_expiradas()"
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        cur.execute(sql)
        cantidad_cerradas = cur.fetchone()[0]
        con.commit()
        
        if cantidad_cerradas > 0:
            app.logger.info(f"TAREA: {cantidad_cerradas} sesiones expiradas cerradas")
        
        return cantidad_cerradas
    except Exception as e:
        con.rollback()
        app.logger.error(f"Error en limpiar_sesiones_expiradas: {str(e)}")
        return 0
    finally:
        cur.close()
        con.close()


def limpiar_tokens_expirados():
    """
    Elimina tokens de recuperación expirados (más de 7 días)
    Ejecutar cada 1 hora
    """
    sql = """
        DELETE FROM password_reset_tokens 
        WHERE fecha_expiracion < NOW() - INTERVAL '7 days'
    """
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        cur.execute(sql)
        cantidad_eliminados = cur.rowcount
        con.commit()
        
        if cantidad_eliminados > 0:
            app.logger.info(f"TAREA: {cantidad_eliminados} tokens expirados eliminados")
        
        return cantidad_eliminados
    except Exception as e:
        con.rollback()
        app.logger.error(f"Error en limpiar_tokens_expirados: {str(e)}")
        return 0
    finally:
        cur.close()
        con.close()


def limpiar_historial_antiguo():
    """
    Limpia historial de contraseñas antiguo (mantener solo últimos 5 por usuario)
    Ejecutar diariamente
    """
    sql = """
        DELETE FROM password_history
        WHERE id_history NOT IN (
            SELECT id_history
            FROM (
                SELECT id_history, 
                       ROW_NUMBER() OVER (PARTITION BY id_usuario ORDER BY fecha_cambio DESC) as rn
                FROM password_history
            ) ranked
            WHERE rn <= 5
        )
    """
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        cur.execute(sql)
        cantidad_eliminados = cur.rowcount
        con.commit()
        
        if cantidad_eliminados > 0:
            app.logger.info(f"TAREA: {cantidad_eliminados} registros antiguos de historial eliminados")
        
        return cantidad_eliminados
    except Exception as e:
        con.rollback()
        app.logger.error(f"Error en limpiar_historial_antiguo: {str(e)}")
        return 0
    finally:
        cur.close()
        con.close()


# Ejemplo de uso con APScheduler (opcional)
def configurar_tareas_programadas(scheduler):
    """
    Configura las tareas programadas usando APScheduler
    
    Uso:
        from apscheduler.schedulers.background import BackgroundScheduler
        scheduler = BackgroundScheduler()
        configurar_tareas_programadas(scheduler)
        scheduler.start()
    """
    # Limpiar sesiones expiradas cada 15 minutos
    scheduler.add_job(
        func=limpiar_sesiones_expiradas,
        trigger='interval',
        minutes=15,
        id='limpiar_sesiones',
        replace_existing=True
    )
    
    # Limpiar tokens expirados cada 1 hora
    scheduler.add_job(
        func=limpiar_tokens_expirados,
        trigger='interval',
        hours=1,
        id='limpiar_tokens',
        replace_existing=True
    )
    
    # Limpiar historial antiguo diariamente a las 2 AM
    scheduler.add_job(
        func=limpiar_historial_antiguo,
        trigger='cron',
        hour=2,
        minute=0,
        id='limpiar_historial',
        replace_existing=True
    )
    
    app.logger.info("Tareas programadas de autenticación configuradas")


