# Sysclin - Proyecto educativo (trabajo de tesis de grado), no apto para producción.
# Ver AVISO_USO_EDUCATIVO.md

from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from app.auth.tasks.auth_tasks import configurar_tareas_programadas
from app.tasks.recordatorio_tasks import configurar_tarea_recordatorios
from app.tasks.agenda_tasks import configurar_tarea_agenda
from app.tasks.auditoria_tasks import configurar_tarea_auditoria
from app.tasks.scheduler_lock import adquirir_lock_scheduler
import logging
import os
import socket

# En modo servidor (gunicorn, FLASK_DEBUG=0) Flask solo muestra WARNING: se baja a INFO
# para conservar en el log los eventos operativos (scheduler, recordatorios, correos).
if not app.debug:
    app.logger.setLevel(logging.INFO)


def debe_iniciar_scheduler():
    """Las tareas programadas corren en UN solo proceso (si no, los recordatorios por
    WhatsApp salen repetidos). Dos protecciones:
    1. Con la recarga automática (FLASK_DEBUG=1), Werkzeug ejecuta run.py en el proceso
       que vigila los archivos y en el que atiende (WERKZEUG_RUN_MAIN=true): solo este último.
    2. Candado en PostgreSQL (app/tasks/scheduler_lock.py): si otro proceso o contenedor ya
       ejecuta las tareas (más workers de gunicorn, dos contenedores), este no las inicia."""
    if app.debug and os.environ.get('WERKZEUG_RUN_MAIN') != 'true':
        return False
    try:
        if adquirir_lock_scheduler():
            return True
        app.logger.warning("Tareas programadas NO iniciadas en este proceso: otro proceso ya las ejecuta (candado ocupado)")
    except Exception as e:
        app.logger.error(f"No se pudo verificar el candado del scheduler, no se inician tareas: {str(e)}")
    return False


# Configurar scheduler para tareas programadas
scheduler = BackgroundScheduler()

if debe_iniciar_scheduler():
    # Configurar tareas de autenticación (si existen)
    try:
        configurar_tareas_programadas(scheduler)
    except Exception as e:
        app.logger.warning(f"No se pudieron configurar tareas de autenticación: {str(e)}")

    # Configurar tarea de envío de recordatorios de citas (Fase B.4)
    try:
        configurar_tarea_recordatorios(scheduler)
    except Exception as e:
        app.logger.warning(f"No se pudo configurar la tarea de recordatorios: {str(e)}")

    # Configurar tarea diaria que extiende los turnos de la Agenda Médica
    try:
        configurar_tarea_agenda(scheduler)
    except Exception as e:
        app.logger.warning(f"No se pudo configurar la tarea de turnos de agenda: {str(e)}")

    try:
        configurar_tarea_auditoria(scheduler)
    except Exception as e:
        app.logger.warning(f"No se pudieron configurar las tareas de auditoría: {str(e)}")

    # Iniciar scheduler
    try:
        scheduler.start()
        app.logger.info(f"✅ Scheduler iniciado correctamente (pid {os.getpid()})")
    except Exception as e:
        app.logger.error(f"Error al iniciar scheduler: {str(e)}")


def obtener_ip_local():
    """Obtiene la IP local de la máquina"""
    try:
        # Crear un socket para obtener la IP local
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Conectar a un servidor externo (no envía datos)
        ip_local = s.getsockname()[0]
        s.close()
        return ip_local
    except Exception:
        return "No disponible"


if __name__ == "__main__":
    try:
        # ========================================
        # CONFIGURACIÓN DE RED
        # ========================================
        
        # host="0.0.0.0" permite conexiones desde cualquier IP en la red local
        # host="127.0.0.1" solo permite localhost (conexión local)
        
        HOST = "0.0.0.0"  # ← CAMBIO PRINCIPAL: Acepta conexiones externas
        PORT = 5000
        DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'  # 1 en local, 0 en el servidor (sin depurador de Werkzeug)
        
        # Obtener y mostrar la IP local
        ip_local = obtener_ip_local()
        
        print("\n" + "="*60)
        print("🚀 SERVIDOR FLASK INICIADO")
        print("="*60)
        print(f"📍 Acceso LOCAL:    http://127.0.0.1:{PORT}")
        print(f"🌐 Acceso en RED:   http://{ip_local}:{PORT}")
        print("="*60)
        print("💡 Para acceder desde otros dispositivos:")
        print(f"   1. Asegúrate de estar en la misma red WiFi")
        print(f"   2. Usa la URL: http://{ip_local}:{PORT}")
        print(f"   3. Verifica el firewall de Windows/Linux")
        print("="*60)
        print("⚠️  Presiona Ctrl+C para detener el servidor\n")
        
        # Iniciar servidor
        app.run(
            host=HOST,      # 0.0.0.0 = Acepta conexiones de cualquier IP
            port=PORT,      # Puerto 5000
            debug=DEBUG     # Modo debug activado
        )
        
    except KeyboardInterrupt:
        print("\n\n🛑 Deteniendo aplicación...")
        if scheduler.running:
            scheduler.shutdown()
        print("✅ Aplicación detenida correctamente")
        
    except Exception as e:
        app.logger.error(f"❌ Error en la aplicación: {str(e)}")
        if scheduler.running:
            scheduler.shutdown()
        print(f"❌ Error: {str(e)}")