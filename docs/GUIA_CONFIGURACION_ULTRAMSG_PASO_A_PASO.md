# Guía Paso a Paso: Configuración de Credenciales UltraMsg

**Fecha:** 2026-01-22  
**Sistema:** Angasys - Sistema de Gestión Médica  
**Objetivo:** Crear cuenta y configurar credenciales de UltraMsg para WhatsApp

---

## 📋 Tabla de Contenidos

1. [Crear Cuenta en UltraMsg](#1-crear-cuenta-en-ultramsg)
2. [Verificar Email](#2-verificar-email)
3. [Crear Instancia](#3-crear-instancia)
4. [Conectar WhatsApp](#4-conectar-whatsapp)
5. [Obtener Credenciales](#5-obtener-credenciales)
6. [Configurar en el Sistema](#6-configurar-en-el-sistema)
7. [Probar Configuración](#7-probar-configuración)
8. [Solución de Problemas](#8-solución-de-problemas)

---

## 1. Crear Cuenta en UltraMsg

### Paso 1.1: Acceder al Sitio Web

1. Abre tu navegador web
2. Ve a: **https://ultramsg.com**
3. Haz clic en el botón **"Sign Up"** o **"Registrarse"** (generalmente en la esquina superior derecha)

### Paso 1.2: Completar Formulario de Registro

En la página de registro, completa los siguientes campos:

- **Email:** Tu dirección de correo electrónico válida
- **Password:** Crea una contraseña segura (mínimo 8 caracteres)
- **Confirm Password:** Repite la contraseña
- **Name:** Tu nombre completo (opcional pero recomendado)

**Ejemplo:**
```
Email: tu_email@ejemplo.com
Password: ********
Confirm Password: ********
Name: Tu Nombre
```

### Paso 1.3: Aceptar Términos y Condiciones

- ✅ Marca la casilla "I agree to the Terms and Conditions" o "Acepto los Términos y Condiciones"
- Haz clic en **"Sign Up"** o **"Registrarse"**

### Paso 1.4: Verificar Registro

- Deberías ver un mensaje de confirmación
- Revisa tu correo electrónico para el email de verificación

---

## 2. Verificar Email

### Paso 2.1: Revisar Bandeja de Entrada

1. Abre tu cliente de correo electrónico
2. Busca un email de **UltraMsg** con el asunto: "Verify your email" o "Verifica tu email"
3. Si no lo encuentras, revisa la carpeta de **Spam** o **Correo no deseado**

### Paso 2.2: Hacer Clic en el Enlace de Verificación

1. Abre el email de UltraMsg
2. Haz clic en el botón **"Verify Email"** o **"Verificar Email"**
3. O copia y pega el enlace de verificación en tu navegador

### Paso 2.3: Confirmar Verificación

- Serás redirigido a la página de UltraMsg
- Deberías ver un mensaje: "Email verified successfully" o "Email verificado exitosamente"
- Ahora puedes iniciar sesión

---

## 3. Crear Instancia

### Paso 3.1: Iniciar Sesión

1. Ve a **https://ultramsg.com**
2. Haz clic en **"Login"** o **"Iniciar Sesión"**
3. Ingresa tu email y contraseña
4. Haz clic en **"Login"**

### Paso 3.2: Acceder al Dashboard

- Después de iniciar sesión, serás redirigido al **Dashboard** o **Panel de Control**
- En el menú lateral, busca la opción **"Instances"** o **"Instancias"**
- Haz clic en **"Instances"**

### Paso 3.3: Crear Nueva Instancia

1. En la página de Instances, busca el botón **"+ New Instance"** o **"+ Nueva Instancia"**
2. Haz clic en el botón
3. Se abrirá un formulario o modal para crear la instancia

### Paso 3.4: Configurar Instancia

Completa los siguientes campos:

- **Instance Name:** Nombre descriptivo (ej: "Angasys-Produccion" o "Angasys-Desarrollo")
- **Description:** Descripción opcional (ej: "Instancia para recordatorios de citas médicas")

**Ejemplo:**
```
Instance Name: Angasys-Produccion
Description: Instancia para envío de recordatorios de citas por WhatsApp
```

4. Haz clic en **"Create"** o **"Crear"**

---

## 4. Conectar WhatsApp

### Paso 4.1: Seleccionar Instancia

- Después de crear la instancia, deberías verla en la lista
- Haz clic en el nombre de tu instancia para abrirla

### Paso 4.2: Iniciar Conexión

1. En la página de detalles de la instancia, busca la sección **"Connection"** o **"Conexión"**
2. Busca el botón **"Connect WhatsApp"** o **"Conectar WhatsApp"**
3. Haz clic en el botón

### Paso 4.3: Escanear Código QR

1. Se mostrará un **código QR** en la pantalla
2. Abre **WhatsApp** en tu teléfono móvil
3. Ve a **Configuración** → **Dispositivos vinculados** (o **Linked Devices**)
4. Toca **"Vincular un dispositivo"** o **"Link a Device"**
5. Escanea el código QR que aparece en la pantalla de UltraMsg

### Paso 4.4: Confirmar Conexión

- Después de escanear el código QR, WhatsApp se conectará
- En UltraMsg deberías ver un mensaje: **"Connected"** o **"Conectado"**
- El estado de la instancia cambiará a **"Active"** o **"Activa"**

**⚠️ Nota Importante:**
- El teléfono debe estar conectado a internet
- WhatsApp debe estar actualizado
- No cierres la ventana del navegador mientras escaneas

---

## 5. Obtener Credenciales

### Paso 5.1: Acceder a Credenciales

1. En la página de detalles de tu instancia, busca la sección **"API Credentials"** o **"Credenciales API"**
2. O busca la pestaña/sección **"Settings"** o **"Configuración"**
3. Haz clic en esa sección

### Paso 5.2: Encontrar Instance ID

- Busca el campo **"Instance ID"** o **"ID de Instancia"**
- Es un identificador único, generalmente un string alfanumérico
- **Ejemplo:** `instance1234567890` o `inst_abc123xyz`

**📝 Copia este valor** - Lo necesitarás para la configuración

### Paso 5.3: Encontrar Token

- Busca el campo **"Token"** o **"API Token"**
- Es una cadena de caracteres más larga, generalmente un hash
- **Ejemplo:** `abc123def456ghi789jkl012mno345pqr678stu901vwx234yz`

**📝 Copia este valor** - Lo necesitarás para la configuración

### Paso 5.4: Verificar URL de API

- La URL de la API generalmente es: **`https://api.ultramsg.com`**
- Verifica en la documentación de UltraMsg si hay una URL diferente
- Anota esta URL también

### Paso 5.5: Guardar Credenciales de Forma Segura

**⚠️ IMPORTANTE:**
- Guarda estas credenciales en un lugar seguro
- **NO** las compartas públicamente
- **NO** las subas a repositorios Git públicos
- Considera usar un gestor de contraseñas

**Ejemplo de cómo guardar:**
```
UltraMsg Credentials - Angasys
==============================
Instance ID: instance1234567890
Token: abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
API URL: https://api.ultramsg.com
Fecha de creación: 2026-01-22
```

---

## 6. Configurar en el Sistema

### Paso 6.1: Configurar Variables de Entorno

Tienes tres opciones para configurar las credenciales:

#### Opción A: Variables de Entorno del Sistema (Recomendado para Producción)

**Linux/Mac:**
```bash
export ULTRAMSG_INSTANCE_ID="instance1234567890"
export ULTRAMSG_TOKEN="abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
export ULTRAMSG_API_URL="https://api.ultramsg.com"
```

**Windows (PowerShell):**
```powershell
$env:ULTRAMSG_INSTANCE_ID="instance1234567890"
$env:ULTRAMSG_TOKEN="abc123def456ghi789jkl012mno345pqr678stu901vwx234yz"
$env:ULTRAMSG_API_URL="https://api.ultramsg.com"
```

**Windows (CMD):**
```cmd
set ULTRAMSG_INSTANCE_ID=instance1234567890
set ULTRAMSG_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
set ULTRAMSG_API_URL=https://api.ultramsg.com
```

#### Opción B: Archivo .env (Recomendado para Desarrollo)

1. Crea un archivo llamado `.env` en la raíz del proyecto:
```bash
cd /home/armando/Documentos/PERSONAL/GIT/Angasys
touch .env
```

2. Edita el archivo `.env` y agrega:
```env
ULTRAMSG_INSTANCE_ID=instance1234567890
ULTRAMSG_TOKEN=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
ULTRAMSG_API_URL=https://api.ultramsg.com
```

3. **IMPORTANTE:** Agrega `.env` a `.gitignore` para no subirlo a Git:
```bash
echo ".env" >> .gitignore
```

4. Si usas `.env`, instala `python-dotenv`:
```bash
pip install python-dotenv
```

5. Agrega al inicio de `app/__init__.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

#### Opción C: Configuración Directa (Solo para Pruebas)

Edita `app/__init__.py` directamente (NO recomendado para producción):

```python
app.config['ULTRAMSG_INSTANCE_ID'] = 'instance1234567890'
app.config['ULTRAMSG_TOKEN'] = 'abc123def456ghi789jkl012mno345pqr678stu901vwx234yz'
app.config['ULTRAMSG_API_URL'] = 'https://api.ultramsg.com'
```

### Paso 6.2: Reiniciar la Aplicación

Después de configurar las variables de entorno:

1. **Detén** la aplicación si está corriendo (Ctrl+C)
2. **Reinicia** la aplicación:
```bash
python run.py
```

O si usas otro método:
```bash
flask run
```

---

## 7. Probar Configuración

### Paso 7.1: Verificar que las Variables Estén Cargadas

Abre una consola Python en el contexto de la aplicación:

```python
from app import app
with app.app_context():
    print("Instance ID:", app.config.get('ULTRAMSG_INSTANCE_ID'))
    print("Token:", app.config.get('ULTRAMSG_TOKEN')[:10] + "...")  # Solo primeros 10 caracteres
    print("API URL:", app.config.get('ULTRAMSG_API_URL'))
```

**Salida esperada:**
```
Instance ID: instance1234567890
Token: abc123def4...
API URL: https://api.ultramsg.com
```

Si ves `None`, las variables no están configuradas correctamente.

### Paso 7.2: Probar Inicialización del Servicio

```python
from app.services.UltraMsgService import UltraMsgService

service = UltraMsgService()
if service.client_available:
    print("✅ UltraMsg configurado correctamente")
    print(f"Instance ID: {service.instance_id}")
else:
    print("❌ UltraMsg no está configurado")
    print("Verifica las variables de entorno")
```

**Salida esperada:**
```
✅ UltraMsg configurado correctamente
Instance ID: instance1234567890
```

### Paso 7.3: Enviar Mensaje de Prueba

**⚠️ IMPORTANTE:** Usa tu propio número de teléfono para pruebas

```python
from app.services.UltraMsgService import UltraMsgService

service = UltraMsgService()

# Reemplaza con TU número de teléfono (formato internacional sin +)
success, message_id, error = service.enviar_mensaje_simple(
    telefono="595981123456",  # Tu número de prueba
    mensaje="🧪 Mensaje de prueba desde Angasys"
)

if success:
    print(f"✅ Mensaje enviado exitosamente!")
    print(f"Message ID: {message_id}")
    print("Revisa tu WhatsApp para confirmar la recepción")
else:
    print(f"❌ Error al enviar mensaje: {error}")
```

**Salida esperada:**
```
✅ Mensaje enviado exitosamente!
Message ID: xxxxx
Revisa tu WhatsApp para confirmar la recepción
```

### Paso 7.4: Probar Recordatorio Completo

```python
from app.services.UltraMsgService import UltraMsgService
from datetime import datetime, timedelta

service = UltraMsgService()

# Fecha y hora de prueba (mañana a las 10:00)
fecha_cita = datetime.now() + timedelta(days=1)
hora_cita = datetime.strptime("10:00", "%H:%M").time()

success, message_id, error = service.enviar_recordatorio_cita(
    telefono="595981123456",  # Tu número de prueba
    nombre_paciente="Juan Pérez",
    cita_fecha=fecha_cita,
    cita_hora=hora_cita,
    especialista="Dr. Carlos González",
    especialidad="Cardiología",
    motivo="Control de presión arterial"
)

if success:
    print(f"✅ Recordatorio enviado exitosamente!")
    print(f"Message ID: {message_id}")
else:
    print(f"❌ Error: {error}")
```

---

## 8. Solución de Problemas

### Problema 1: "Cliente UltraMsg no inicializado"

**Síntomas:**
- El servicio retorna `client_available = False`
- Mensajes de error sobre configuración incompleta

**Soluciones:**

1. **Verificar que las variables estén definidas:**
```bash
# Linux/Mac
echo $ULTRAMSG_INSTANCE_ID
echo $ULTRAMSG_TOKEN

# Windows PowerShell
echo $env:ULTRAMSG_INSTANCE_ID
echo $env:ULTRAMSG_TOKEN
```

2. **Verificar que no haya espacios en las variables:**
```bash
# Incorrecto (con espacios)
export ULTRAMSG_INSTANCE_ID = "instance123"

# Correcto (sin espacios)
export ULTRAMSG_INSTANCE_ID="instance123"
```

3. **Reiniciar la aplicación** después de configurar variables

4. **Verificar que `app/__init__.py` tenga la configuración:**
```python
app.config['ULTRAMSG_INSTANCE_ID'] = os.getenv('ULTRAMSG_INSTANCE_ID')
app.config['ULTRAMSG_TOKEN'] = os.getenv('ULTRAMSG_TOKEN')
```

### Problema 2: "Error HTTP 401" o "Unauthorized"

**Síntomas:**
- Error 401 al intentar enviar mensajes
- Mensaje "Unauthorized" en los logs

**Soluciones:**

1. **Verificar que el Token sea correcto:**
   - Ve a UltraMsg Dashboard
   - Copia el Token nuevamente
   - Asegúrate de copiar todo el token (puede ser largo)

2. **Verificar que el Instance ID sea correcto:**
   - Confirma que estás usando el Instance ID de la instancia correcta
   - Verifica que la instancia esté activa

3. **Regenerar Token si es necesario:**
   - En UltraMsg Dashboard, busca opción "Regenerate Token"
   - Copia el nuevo token
   - Actualiza la variable de entorno

### Problema 3: "Número inválido" o "Invalid number"

**Síntomas:**
- Error al enviar mensaje
- Mensaje sobre número inválido

**Soluciones:**

1. **Verificar formato del número:**
   - Debe estar en formato internacional sin el símbolo +
   - Ejemplo correcto: `595981123456`
   - Ejemplo incorrecto: `+595981123456` o `0981123456`

2. **El servicio formatea automáticamente, pero verifica:**
   - Números que empiezan con 0 se convierten a 595
   - Números con + se remueve el +
   - Si persiste el error, verifica el número original

3. **Verificar que el número tenga WhatsApp:**
   - El número debe tener WhatsApp activo
   - Debe estar registrado en WhatsApp

### Problema 4: "Timeout" o "Connection Error"

**Síntomas:**
- Timeout al intentar enviar
- Error de conexión

**Soluciones:**

1. **Verificar conexión a internet:**
```bash
ping api.ultramsg.com
```

2. **Verificar que UltraMsg esté disponible:**
   - Ve a https://ultramsg.com
   - Verifica el estado del servicio

3. **Aumentar timeout (si es necesario):**
   - En `UltraMsgService.py`, el timeout está en 30 segundos
   - Puedes aumentarlo si tienes conexión lenta

4. **Verificar firewall/proxy:**
   - Asegúrate de que no haya firewall bloqueando
   - Si usas proxy, configúralo en requests

### Problema 5: WhatsApp no se conecta

**Síntomas:**
- No puedes escanear el código QR
- La conexión no se establece

**Soluciones:**

1. **Verificar que WhatsApp esté actualizado:**
   - Actualiza WhatsApp a la última versión

2. **Usar otro navegador:**
   - Prueba con Chrome, Firefox, o Edge

3. **Limpiar caché del navegador:**
   - Limpia cookies y caché
   - Intenta en modo incógnito

4. **Verificar que el teléfono tenga internet:**
   - El teléfono debe estar conectado a WiFi o datos móviles

5. **Reintentar la conexión:**
   - Desconecta la instancia
   - Vuelve a conectar

### Problema 6: No recibo mensajes

**Síntomas:**
- El sistema dice que envió el mensaje
- Pero no llega a WhatsApp

**Soluciones:**

1. **Verificar que la instancia esté conectada:**
   - Ve a UltraMsg Dashboard
   - Verifica que el estado sea "Connected" o "Conectado"

2. **Verificar el número de destino:**
   - Confirma que el número sea correcto
   - Verifica que tenga WhatsApp activo

3. **Revisar logs del sistema:**
   - Busca errores en los logs
   - Verifica el Message ID retornado

4. **Probar con tu propio número primero:**
   - Envía un mensaje de prueba a tu número
   - Si funciona, el problema puede ser el número de destino

---

## ✅ Checklist Final

Antes de considerar la configuración completa, verifica:

- [ ] Cuenta creada en UltraMsg
- [ ] Email verificado
- [ ] Instancia creada
- [ ] WhatsApp conectado (estado "Connected")
- [ ] Instance ID copiado
- [ ] Token copiado
- [ ] Variables de entorno configuradas
- [ ] Aplicación reiniciada
- [ ] Servicio inicializa correctamente (`client_available = True`)
- [ ] Mensaje de prueba enviado exitosamente
- [ ] Mensaje recibido en WhatsApp
- [ ] Recordatorio completo probado

---

## 📚 Recursos Adicionales

- **Documentación UltraMsg:** https://ultramsg.com/docs
- **API Reference:** https://ultramsg.com/docs/api
- **Soporte:** support@ultramsg.com
- **Dashboard:** https://ultramsg.com/dashboard

---

## 🔐 Seguridad

**Recordatorios importantes:**

1. **Nunca compartas tus credenciales públicamente**
2. **No subas el archivo .env a Git** (debe estar en .gitignore)
3. **Rota el token periódicamente** (cada 3-6 meses)
4. **Usa diferentes instancias para desarrollo y producción**
5. **Monitorea el uso de la API** en el Dashboard de UltraMsg

---

**Documento creado:** 2026-01-22  
**Última actualización:** 2026-01-22  
**Versión:** 1.0

---

## 📞 Soporte

Si después de seguir esta guía aún tienes problemas:

1. Revisa la sección de [Solución de Problemas](#8-solución-de-problemas)
2. Consulta la documentación oficial de UltraMsg
3. Contacta al soporte de UltraMsg: support@ultramsg.com
4. Revisa los logs del sistema para más detalles del error

