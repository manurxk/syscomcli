# Configuración de UltraMsg para Recordatorios WhatsApp

**Fecha:** 2026-01-22  
**Sistema:** Sysclin - Sistema de Gestión Médica

---

## 📋 Requisitos Previos

1. **Cuenta en UltraMsg**
   - Crear cuenta en [https://ultramsg.com](https://ultramsg.com)
   - Verificar email y completar registro

2. **Número de WhatsApp Business**
   - Tener un número de WhatsApp Business verificado
   - O usar un número personal para pruebas (limitado)

3. **Credenciales de API**
   - Instance ID de UltraMsg
   - Token de autenticación de UltraMsg

---

## 🔧 Configuración Paso a Paso

### Paso 1: Crear Cuenta en UltraMsg

1. Ir a [https://ultramsg.com](https://ultramsg.com)
2. Hacer clic en "Sign Up" o "Registrarse"
3. Completar formulario de registro
4. Verificar email

### Paso 2: Configurar Instancia

1. Iniciar sesión en UltraMsg
2. Ir a "Instances" o "Instancias"
3. Crear nueva instancia
4. Conectar con WhatsApp (escaneando código QR)
5. Copiar **Instance ID** y **Token**

### Paso 3: Configurar Variables de Entorno

#### Opción A: Variables de Entorno del Sistema

**Linux/Mac:**
```bash
export ULTRAMSG_INSTANCE_ID="tu_instance_id_aqui"
export ULTRAMSG_TOKEN="tu_token_aqui"
export ULTRAMSG_API_URL="https://api.ultramsg.com"  # Opcional
```

**Windows (PowerShell):**
```powershell
$env:ULTRAMSG_INSTANCE_ID="tu_instance_id_aqui"
$env:ULTRAMSG_TOKEN="tu_token_aqui"
$env:ULTRAMSG_API_URL="https://api.ultramsg.com"  # Opcional
```

**Windows (CMD):**
```cmd
set ULTRAMSG_INSTANCE_ID=tu_instance_id_aqui
set ULTRAMSG_TOKEN=tu_token_aqui
set ULTRAMSG_API_URL=https://api.ultramsg.com
```

#### Opción B: Archivo .env (Recomendado para desarrollo)

Crear archivo `.env` en la raíz del proyecto:

```env
ULTRAMSG_INSTANCE_ID=tu_instance_id_aqui
ULTRAMSG_TOKEN=tu_token_aqui
ULTRAMSG_API_URL=https://api.ultramsg.com
```

**Nota:** Si usas `.env`, necesitarás instalar `python-dotenv`:
```bash
pip install python-dotenv
```

Y cargar en `app/__init__.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Opción C: Configuración Directa (No recomendado para producción)

Editar `app/__init__.py` directamente:

```python
app.config['ULTRAMSG_INSTANCE_ID'] = 'tu_instance_id_aqui'
app.config['ULTRAMSG_TOKEN'] = 'tu_token_aqui'
app.config['ULTRAMSG_API_URL'] = 'https://api.ultramsg.com'
```

---

## 🗄️ Configuración de Base de Datos (Opcional)

Para tracking de mensajes, ejecutar script SQL:

```bash
psql -U tu_usuario -d tu_base_de_datos -f app/varios/SQL/add_ultramsg_column.sql
```

O ejecutar manualmente en PostgreSQL:

```sql
ALTER TABLE recordatorios 
ADD COLUMN IF NOT EXISTS recordatorio_ultramsg_id VARCHAR(100);
```

---

## ✅ Verificación de Configuración

### 1. Verificar Variables de Entorno

En Python:
```python
import os
print("Instance ID:", os.getenv('ULTRAMSG_INSTANCE_ID'))
print("Token:", os.getenv('ULTRAMSG_TOKEN')[:10] + "...")  # Solo primeros 10 caracteres
```

### 2. Probar Servicio

```python
from app.services.UltraMsgService import UltraMsgService

service = UltraMsgService()
if service.client_available:
    print("✅ UltraMsg configurado correctamente")
else:
    print("❌ UltraMsg no está configurado")
```

### 3. Probar Envío

```python
from app.services.UltraMsgService import UltraMsgService

service = UltraMsgService()
success, message_id, error = service.enviar_mensaje_simple(
    telefono="+595981123456",  # Tu número de prueba
    mensaje="Mensaje de prueba"
)

if success:
    print(f"✅ Mensaje enviado. ID: {message_id}")
else:
    print(f"❌ Error: {error}")
```

---

## 🔍 Solución de Problemas

### Error: "Cliente UltraMsg no inicializado"

**Causa:** Variables de entorno no configuradas

**Solución:**
1. Verificar que las variables estén definidas
2. Reiniciar la aplicación después de configurar variables
3. Verificar que `app.config` tenga los valores correctos

### Error: "Error HTTP 401" o "Unauthorized"

**Causa:** Token o Instance ID incorrectos

**Solución:**
1. Verificar credenciales en UltraMsg Dashboard
2. Regenerar token si es necesario
3. Verificar que Instance ID sea correcto

### Error: "Número inválido"

**Causa:** Formato de número incorrecto

**Solución:**
- Los números deben estar en formato internacional sin el símbolo +
- Ejemplo: `595981123456` (no `+595981123456` o `0981123456`)
- El servicio formatea automáticamente, pero verifica el formato original

### Error: "Timeout" o "Connection Error"

**Causa:** Problemas de conectividad o UltraMsg no disponible

**Solución:**
1. Verificar conexión a internet
2. Verificar estado de UltraMsg en su sitio web
3. Reintentar después de unos minutos

---

## 📊 Monitoreo

### Logs

El sistema registra todas las operaciones en los logs:

```
INFO: Cliente UltraMsg inicializado correctamente
INFO: Intentando enviar WhatsApp a 595981123456
INFO: WhatsApp enviado exitosamente. Message ID: xxxxx
```

### Verificar Estado de Mensajes

```python
from app.services.UltraMsgService import UltraMsgService

service = UltraMsgService()
estado = service.verificar_estado_mensaje("message_id_aqui")
print(estado)
```

---

## 🔐 Seguridad

### Buenas Prácticas

1. **Nunca commitees credenciales en el código**
   - Usar siempre variables de entorno
   - Agregar `.env` a `.gitignore`

2. **Rotar tokens periódicamente**
   - Cambiar token cada 3-6 meses
   - Regenerar en caso de compromiso

3. **Limitar acceso a credenciales**
   - Solo personal autorizado
   - Usar secretos en producción (AWS Secrets Manager, etc.)

4. **Monitorear uso**
   - Revisar logs regularmente
   - Alertar sobre actividad sospechosa

---

## 📚 Referencias

- [Documentación UltraMsg](https://ultramsg.com/docs)
- [API Reference](https://ultramsg.com/docs/api)
- [Pricing](https://ultramsg.com/pricing)

---

## ✅ Checklist de Configuración

- [ ] Cuenta creada en UltraMsg
- [ ] Instancia configurada y conectada
- [ ] Credenciales obtenidas (Instance ID y Token)
- [ ] Variables de entorno configuradas
- [ ] Script SQL ejecutado (opcional)
- [ ] Servicio probado con mensaje de prueba
- [ ] Logs verificados
- [ ] Sistema de recordatorios funcionando

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

