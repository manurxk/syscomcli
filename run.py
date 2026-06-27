from app import app
from apscheduler.schedulers.background import BackgroundScheduler
from app.auth.tasks.auth_tasks import configurar_tareas_programadas
from app.tasks.recordatorio_tasks import configurar_tarea_recordatorios
import socket

# Configurar scheduler para tareas programadas
scheduler = BackgroundScheduler()

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

# Iniciar scheduler
try:
    scheduler.start()
    app.logger.info("✅ Scheduler iniciado correctamente")
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
        DEBUG = True
        
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
        scheduler.shutdown()
        print("✅ Aplicación detenida correctamente")
        
    except Exception as e:
        app.logger.error(f"❌ Error en la aplicación: {str(e)}")
        scheduler.shutdown()
        print(f"❌ Error: {str(e)}")