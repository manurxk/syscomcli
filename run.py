from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from app.tasks.recordatorio_tasks import configurar_tarea_recordatorios
from app.auth.tasks.auth_tasks import configurar_tareas_programadas

# Configurar scheduler para tareas programadas
scheduler = BackgroundScheduler()

# Configurar tareas de autenticación (si existen)
try:
    configurar_tareas_programadas(scheduler)
except Exception as e:
    app.logger.warning(f"No se pudieron configurar tareas de autenticación: {str(e)}")

# Configurar tarea de recordatorios
try:
    configurar_tarea_recordatorios(scheduler)
except Exception as e:
    app.logger.error(f"Error al configurar tarea de recordatorios: {str(e)}")

# Iniciar scheduler
try:
    scheduler.start()
    app.logger.info("✅ Scheduler iniciado correctamente")
except Exception as e:
    app.logger.error(f"Error al iniciar scheduler: {str(e)}")

if __name__ == "__main__":
    # Escucha solo en localhost (127.0.0.1) para desarrollo local
    # Solo accesible desde la misma máquina
    try:
        app.run(host="127.0.0.1", port=5000, debug=True)
    except KeyboardInterrupt:
        app.logger.info("Deteniendo aplicación...")
        scheduler.shutdown()
    except Exception as e:
        app.logger.error(f"Error en la aplicación: {str(e)}")
        scheduler.shutdown()