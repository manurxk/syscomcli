#!/usr/bin/env python
"""
Script de prueba para enviar un mensaje de prueba con UltraMsg
"""
from app import app
from app.services.UltraMsgService import UltraMsgService
from datetime import datetime, timedelta

print("=" * 60)
print("PRUEBA DE ENVÍO ULTRAMSG")
print("=" * 60)

with app.app_context():
    # Verificar configuración
    print("\n1. Verificando configuración...")
    print("-" * 60)
    
    instance_id = app.config.get('ULTRAMSG_INSTANCE_ID')
    token = app.config.get('ULTRAMSG_TOKEN')
    api_url = app.config.get('ULTRAMSG_API_URL')
    
    print(f"Instance ID: {instance_id}")
    print(f"Token: {token[:10]}... (primeros 10 caracteres)" if token else "Token: NO CONFIGURADO")
    print(f"API URL: {api_url}")
    print(f"\n📱 Número de WhatsApp Business (desde el cual se envían): 0991301397")
    
    if not instance_id or not token:
        print("\n❌ ERROR: Configuración incompleta")
        print("Verifica que ULTRAMSG_INSTANCE_ID y ULTRAMSG_TOKEN estén configurados")
        exit(1)
    
    # Inicializar servicio
    print("\n2. Inicializando servicio...")
    print("-" * 60)
    
    try:
        service = UltraMsgService()
        
        if not service.client_available:
            print("❌ ERROR: Servicio no disponible")
            exit(1)
        
        print("✅ Servicio inicializado correctamente")
        print(f"   - Rate Limit: {service.rate_limit} msg/min")
        print(f"   - Max Retries: {service.max_retries}")
        
    except Exception as e:
        print(f"❌ ERROR al inicializar servicio: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
    
    # Solicitar número de destino
    print("\n3. Configuración de prueba...")
    print("-" * 60)
    print("📱 Número de WhatsApp Business (origen): 0991301397")
    print("   (Este es el número desde el cual se enviarán los mensajes)")
    print()
    
    # Solicitar número de destino para prueba
    telefono_destino = input("Ingresa el número de teléfono DESTINO para la prueba (ej: 0981123456): ").strip()
    
    if not telefono_destino:
        print("❌ No se ingresó número de destino. Cancelando prueba.")
        exit(1)
    
    print(f"\n📞 Número de destino: {telefono_destino}")
    print("   (Este número recibirá el mensaje de prueba)")
    
    # Preparar datos de prueba
    print("\n4. Preparando mensaje de prueba...")
    print("-" * 60)
    
    # Fecha y hora de prueba (mañana a las 10:00)
    fecha_cita = datetime.now() + timedelta(days=1)
    hora_cita = datetime.strptime("10:00", "%H:%M").time()
    
    print(f"Fecha cita: {fecha_cita.strftime('%d/%m/%Y')}")
    print(f"Hora cita: {hora_cita.strftime('%H:%M')}")
    
    # Enviar mensaje de prueba simple primero
    print("\n5. Enviando mensaje simple de prueba...")
    print("-" * 60)
    
    try:
        mensaje_simple = "🧪 Mensaje de prueba desde Angasys - Sistema de Gestión Médica"
        print(f"Enviando: {mensaje_simple}")
        print(f"Desde: 0991301397 → Hacia: {telefono_destino}")
        
        success, message_id, error = service.enviar_mensaje_simple(
            telefono=telefono_destino,
            mensaje=mensaje_simple
        )
        
        if success:
            print(f"✅ Mensaje simple enviado exitosamente!")
            print(f"   Message ID: {message_id}")
            print(f"   Revisa el WhatsApp del número {telefono_destino} para confirmar")
        else:
            print(f"❌ Error al enviar mensaje simple: {error}")
            print("\n¿Deseas continuar con el recordatorio completo? (s/n): ", end="")
            continuar = input().strip().lower()
            if continuar != 's':
                exit(1)
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
    
    # Esperar un poco antes del siguiente mensaje
    import time
    print("\n⏳ Esperando 3 segundos antes del siguiente mensaje...")
    time.sleep(3)
    
    # Enviar recordatorio completo
    print("\n6. Enviando recordatorio completo de prueba...")
    print("-" * 60)
    
    try:
        print("Enviando recordatorio de cita...")
        print(f"Desde: 0991301397 → Hacia: {telefono_destino}")
        
        resultado = service.enviar_recordatorio_cita(
            telefono=telefono_destino,
            nombre_paciente="Juan Pérez",
            cita_fecha=fecha_cita,
            cita_hora=hora_cita,
            especialista="Dr. Carlos González",
            especialidad="Cardiología",
            motivo="Control de presión arterial"
        )
        
        # Manejar formato de retorno
        if len(resultado) == 4:
            success, message_id, error, tipo_error = resultado
        else:
            success, message_id, error = resultado
            tipo_error = None
        
        if success:
            print(f"✅ Recordatorio enviado exitosamente!")
            print(f"   Message ID: {message_id}")
            print(f"   Revisa el WhatsApp del número {telefono_destino} para confirmar")
        else:
            print(f"❌ Error al enviar recordatorio: {error}")
            if tipo_error:
                print(f"   Tipo de error: {tipo_error.value}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)
    
    # Mostrar métricas
    print("\n7. Métricas del servicio:")
    print("-" * 60)
    
    metricas = service.obtener_metricas()
    print(f"Total enviados: {metricas['total_enviados']}")
    print(f"Total fallidos: {metricas['total_fallidos']}")
    print(f"Tasa de éxito: {metricas['tasa_exito']}%")
    print(f"Tiempo promedio: {metricas['tiempo_promedio_envio']:.2f}s")
    
    print("\n" + "=" * 60)
    print("✅ PRUEBA COMPLETADA")
    print("=" * 60)
    print(f"\n📱 Los mensajes fueron enviados desde: 0991301397")
    print(f"📞 Revisa el WhatsApp del número: {telefono_destino}")
    print("\n💡 NOTA: En producción, los mensajes se enviarán automáticamente")
    print("   a los números de teléfono de los pacientes registrados en el sistema.")
