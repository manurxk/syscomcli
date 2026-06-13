#!/usr/bin/env python
"""
Script de prueba para verificar configuración de UltraMsg
"""
import os
import sys

print("=" * 60)
print("VERIFICACIÓN DE CONFIGURACIÓN ULTRAMSG")
print("=" * 60)

# 1. Verificar variables de entorno del sistema
print("\n1. Variables de entorno del sistema:")
print("-" * 60)
instance_id_env = os.getenv('ULTRAMSG_INSTANCE_ID')
token_env = os.getenv('ULTRAMSG_TOKEN')
api_url_env = os.getenv('ULTRAMSG_API_URL')

if instance_id_env:
    print(f"✅ ULTRAMSG_INSTANCE_ID: {instance_id_env}")
else:
    print("❌ ULTRAMSG_INSTANCE_ID: NO CONFIGURADO")

if token_env:
    print(f"✅ ULTRAMSG_TOKEN: {token_env[:10]}... (primeros 10 caracteres)")
else:
    print("❌ ULTRAMSG_TOKEN: NO CONFIGURADO")

if api_url_env:
    print(f"✅ ULTRAMSG_API_URL: {api_url_env}")
else:
    print("⚠️ ULTRAMSG_API_URL: NO CONFIGURADO (se usará default)")

# 2. Intentar importar app y verificar configuración
print("\n2. Configuración en Flask app:")
print("-" * 60)
try:
    from app import app
    
    with app.app_context():
        instance_id = app.config.get('ULTRAMSG_INSTANCE_ID')
        token = app.config.get('ULTRAMSG_TOKEN')
        api_url = app.config.get('ULTRAMSG_API_URL', 'https://api.ultramsg.com')
        
        if instance_id:
            print(f"✅ Instance ID: {instance_id}")
        else:
            print("❌ Instance ID: NO CONFIGURADO")
        
        if token:
            print(f"✅ Token: {token[:10]}... (primeros 10 caracteres)")
        else:
            print("❌ Token: NO CONFIGURADO")
        
        print(f"✅ API URL: {api_url}")
        
        # 3. Probar inicialización del servicio
        print("\n3. Inicialización del servicio:")
        print("-" * 60)
        try:
            from app.services.UltraMsgService import UltraMsgService
            
            service = UltraMsgService()
            
            if service.client_available:
                print("✅ UltraMsgService inicializado correctamente")
                print(f"   - Instance ID: {service.instance_id}")
                print(f"   - API URL: {service.api_url}")
                print(f"   - Rate Limit: {service.rate_limit} msg/min")
                print(f"   - Max Retries: {service.max_retries}")
            else:
                print("❌ UltraMsgService NO está disponible")
                print("   Razón: Configuración incompleta")
        except Exception as e:
            print(f"❌ Error al inicializar servicio: {str(e)}")
            import traceback
            traceback.print_exc()
            
except Exception as e:
    print(f"❌ Error al importar app: {str(e)}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 4. Resumen y recomendaciones
print("\n4. Resumen:")
print("-" * 60)

if instance_id_env and token_env:
    print("✅ Variables de entorno configuradas correctamente")
    if instance_id and token:
        print("✅ Configuración en Flask app correcta")
        print("\n🎉 ¡Todo está configurado correctamente!")
    else:
        print("⚠️ Variables de entorno existen pero no se cargaron en Flask")
        print("   Recomendación: Reiniciar la aplicación")
else:
    print("❌ Variables de entorno NO están configuradas")
    print("\n📝 Para configurar, ejecuta:")
    print("   export ULTRAMSG_INSTANCE_ID='tu_instance_id'")
    print("   export ULTRAMSG_TOKEN='tu_token'")
    print("   export ULTRAMSG_API_URL='https://api.ultramsg.com'  # Opcional")
    print("\n   O crea un archivo .env en la raíz del proyecto con:")
    print("   ULTRAMSG_INSTANCE_ID=tu_instance_id")
    print("   ULTRAMSG_TOKEN=tu_token")
    print("   ULTRAMSG_API_URL=https://api.ultramsg.com")

print("\n" + "=" * 60)

