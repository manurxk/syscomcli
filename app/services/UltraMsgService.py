# /app/services/UltraMsgService.py
"""
Servicio para envío de mensajes WhatsApp mediante UltraMsg API
Reemplaza la funcionalidad anterior de TwilioService

Fase 2: Mejoras y Optimizaciones
- Sistema de reintentos con backoff exponencial
- Rate limiting
- Categorización de errores
- Métricas y monitoreo
"""
import requests
from flask import current_app as app
from datetime import datetime, timedelta
import logging
import time
from enum import Enum
from collections import deque
from threading import Lock

logger = logging.getLogger(__name__)


class TipoError(Enum):
    """Tipos de errores para categorización"""
    TEMPORAL = "temporal"  # Error temporal, se puede reintentar
    PERMANENTE = "permanente"  # Error permanente, no reintentar
    RATE_LIMIT = "rate_limit"  # Límite de rate alcanzado
    CONFIGURACION = "configuracion"  # Error de configuración
    DESCONOCIDO = "desconocido"  # Error desconocido


class UltraMsgService:
    """
    Servicio para envío de mensajes WhatsApp usando UltraMsg API
    
    Requiere configuración en variables de entorno:
    - ULTRAMSG_INSTANCE_ID: ID de la instancia de UltraMsg
    - ULTRAMSG_TOKEN: Token de autenticación de UltraMsg
    - ULTRAMSG_API_URL: URL base de la API (opcional, default: https://api.ultramsg.com)
    
    Configuración opcional:
    - ULTRAMSG_MAX_RETRIES: Máximo de reintentos (default: 3)
    - ULTRAMSG_RATE_LIMIT: Límite de mensajes por minuto (default: 20)
    """
    
    def __init__(self):
        """Inicializa cliente UltraMsg desde configuración"""
        self.instance_id = app.config.get('ULTRAMSG_INSTANCE_ID')
        self.token = app.config.get('ULTRAMSG_TOKEN')
        self.api_url = app.config.get('ULTRAMSG_API_URL', 'https://api.ultramsg.com')
        
        # Configuración de reintentos
        self.max_retries = int(app.config.get('ULTRAMSG_MAX_RETRIES', 3))
        self.retry_delays = [1, 2, 4]  # Backoff exponencial en segundos
        
        # Configuración de rate limiting
        self.rate_limit = int(app.config.get('ULTRAMSG_RATE_LIMIT', 20))  # mensajes por minuto
        self.rate_window = 60  # ventana de tiempo en segundos
        self.message_timestamps = deque(maxlen=self.rate_limit)
        self.rate_lock = Lock()
        
        # Métricas
        self.metrics = {
            'total_enviados': 0,
            'total_fallidos': 0,
            'total_reintentos': 0,
            'errores_temporales': 0,
            'errores_permanentes': 0,
            'rate_limits': 0,
            'ultimo_envio': None,
            'tiempo_promedio_envio': 0.0
        }
        
        if not all([self.instance_id, self.token]):
            app.logger.warning(
                "Configuración de UltraMsg incompleta. "
                "Algunas funciones pueden no estar disponibles."
            )
            self.client_available = False
        else:
            self.client_available = True
            app.logger.info(
                f"Cliente UltraMsg inicializado correctamente "
                f"(Rate limit: {self.rate_limit} msg/min, Max retries: {self.max_retries})"
            )
    
    def enviar_recordatorio_cita(self, telefono, nombre_paciente, cita_fecha, 
                                  cita_hora, especialista, especialidad, motivo=None):
        """
        Envía recordatorio de cita por WhatsApp con reintentos automáticos
        
        Args:
            telefono: Número de teléfono del paciente
            nombre_paciente: Nombre del paciente
            cita_fecha: Fecha de la cita
            cita_hora: Hora de la cita
            especialista: Nombre del especialista
            especialidad: Nombre de la especialidad
            motivo: Motivo de la cita (opcional)
        
        Returns:
            tuple: (success: bool, message_id: str, error: str, tipo_error: TipoError)
        """
        if not self.client_available:
            error_msg = "Cliente UltraMsg no inicializado. Verifique la configuración."
            app.logger.error(error_msg)
            return (False, None, error_msg, TipoError.CONFIGURACION)
        
        try:
            # Validar teléfono
            if not telefono:
                error_msg = "Teléfono no proporcionado"
                app.logger.error(error_msg)
                return (False, None, error_msg, TipoError.PERMANENTE)
            
            # Formatear teléfono
            telefono_formateado = self._formatear_telefono(telefono)
            app.logger.debug(f"Teléfono formateado: {telefono_formateado}")
            
            # Construir mensaje
            mensaje = self._construir_mensaje_recordatorio(
                nombre_paciente, cita_fecha, cita_hora, 
                especialista, especialidad, motivo
            )
            
            # Enviar con reintentos automáticos
            return self._enviar_con_reintentos(telefono_formateado, mensaje)
        
        except Exception as e:
            error_msg = f"Error inesperado enviando mensaje: {str(e)}"
            app.logger.error(error_msg, exc_info=True)
            self.metrics['total_fallidos'] += 1
            return (False, None, error_msg, TipoError.DESCONOCIDO)
    
    def _enviar_con_reintentos(self, telefono, mensaje):
        """
        Envía mensaje con sistema de reintentos y rate limiting
        
        Args:
            telefono: Número de teléfono formateado
            mensaje: Texto del mensaje
        
        Returns:
            tuple: (success: bool, message_id: str, error: str, tipo_error: TipoError)
        """
        inicio_tiempo = time.time()
        
        # Aplicar rate limiting
        self._aplicar_rate_limit()
        
        # Intentar envío con reintentos
        ultimo_error = None
        ultimo_tipo_error = TipoError.DESCONOCIDO
        
        for intento in range(self.max_retries + 1):
            try:
                if intento > 0:
                    # Esperar antes de reintentar (backoff exponencial)
                    delay = self.retry_delays[min(intento - 1, len(self.retry_delays) - 1)]
                    app.logger.info(
                        f"Reintentando envío (intento {intento + 1}/{self.max_retries + 1}) "
                        f"después de {delay} segundos..."
                    )
                    time.sleep(delay)
                    self.metrics['total_reintentos'] += 1
                
                # Enviar mensaje
                success, message_id, error, tipo_error = self._enviar_mensaje(telefono, mensaje)
                
                if success:
                    # Actualizar métricas
                    tiempo_envio = time.time() - inicio_tiempo
                    self._actualizar_metricas_exitoso(tiempo_envio)
                    
                    app.logger.info(
                        f"✅ WhatsApp enviado exitosamente a {telefono} "
                        f"(Message ID: {message_id}, Intentos: {intento + 1})"
                    )
                    return (True, message_id, None, None)
                else:
                    ultimo_error = error
                    ultimo_tipo_error = tipo_error
                    
                    # Si es error permanente, no reintentar
                    if tipo_error == TipoError.PERMANENTE:
                        app.logger.warning(
                            f"❌ Error permanente, no se reintentará: {error}"
                        )
                        self.metrics['errores_permanentes'] += 1
                        break
                    
                    # Si es error de configuración, no reintentar
                    if tipo_error == TipoError.CONFIGURACION:
                        app.logger.error(f"❌ Error de configuración: {error}")
                        break
                    
                    # Si es rate limit, esperar más tiempo
                    if tipo_error == TipoError.RATE_LIMIT:
                        app.logger.warning(f"⏳ Rate limit alcanzado, esperando...")
                        self.metrics['rate_limits'] += 1
                        # Esperar hasta que se libere espacio en la ventana
                        self._esperar_rate_limit()
                        continue
                    
                    # Error temporal, continuar con reintentos
                    if intento < self.max_retries:
                        app.logger.warning(
                            f"⚠️ Error temporal (intento {intento + 1}/{self.max_retries + 1}): {error}"
                        )
                        self.metrics['errores_temporales'] += 1
                    else:
                        app.logger.error(
                            f"❌ Falló después de {self.max_retries + 1} intentos: {error}"
                        )
                        self.metrics['errores_temporales'] += 1
            
            except Exception as e:
                ultimo_error = f"Excepción inesperada: {str(e)}"
                ultimo_tipo_error = TipoError.DESCONOCIDO
                app.logger.error(f"Error en intento {intento + 1}: {ultimo_error}", exc_info=True)
        
        # Todos los intentos fallaron
        self.metrics['total_fallidos'] += 1
        return (False, None, ultimo_error or "Error desconocido", ultimo_tipo_error)
    
    def _enviar_mensaje(self, telefono, mensaje):
        """
        Envía un mensaje individual (sin reintentos)
        
        Returns:
            tuple: (success: bool, message_id: str, error: str, tipo_error: TipoError)
        """
        try:
            url = f"{self.api_url}/{self.instance_id}/messages/chat"
            
            payload = {
                "token": self.token,
                "to": telefono,
                "body": mensaje
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            # Procesar respuesta
            if response.status_code == 200:
                response_data = response.json()
                message_id = response_data.get('id') or response_data.get('messageId') or response_data.get('sent')
                
                if message_id:
                    return (True, str(message_id), None, None)
                else:
                    # Respuesta exitosa pero sin ID
                    return (True, "sent", None, None)
            
            elif response.status_code == 401:
                # No autorizado - error de configuración
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('error', 'No autorizado. Verifique credenciales.')
                return (False, None, error_msg, TipoError.CONFIGURACION)
            
            elif response.status_code == 429:
                # Rate limit
                error_msg = "Límite de rate alcanzado. Demasiadas peticiones."
                return (False, None, error_msg, TipoError.RATE_LIMIT)
            
            elif response.status_code >= 500:
                # Error del servidor - temporal
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('error', f"Error del servidor: {response.status_code}")
                return (False, None, error_msg, TipoError.TEMPORAL)
            
            else:
                # Otros errores - pueden ser permanentes o temporales
                error_data = response.json() if response.content else {}
                error_msg = error_data.get('error', f"Error HTTP {response.status_code}")
                
                # Determinar si es permanente basado en el código
                if response.status_code in [400, 404]:
                    tipo_error = TipoError.PERMANENTE
                else:
                    tipo_error = TipoError.TEMPORAL
                
                return (False, None, error_msg, tipo_error)
        
        except requests.exceptions.Timeout:
            return (False, None, "Timeout: El servidor no respondió a tiempo.", TipoError.TEMPORAL)
        
        except requests.exceptions.ConnectionError:
            return (False, None, "Error de conexión. Verifique su conexión a internet.", TipoError.TEMPORAL)
        
        except requests.exceptions.RequestException as e:
            return (False, None, f"Error de petición: {str(e)}", TipoError.TEMPORAL)
        
        except Exception as e:
            return (False, None, f"Error inesperado: {str(e)}", TipoError.DESCONOCIDO)
    
    def _aplicar_rate_limit(self):
        """
        Aplica rate limiting antes de enviar un mensaje
        Espera si es necesario para respetar el límite
        """
        with self.rate_lock:
            ahora = time.time()
            
            # Limpiar timestamps fuera de la ventana
            while self.message_timestamps and self.message_timestamps[0] < ahora - self.rate_window:
                self.message_timestamps.popleft()
            
            # Si estamos en el límite, esperar
            if len(self.message_timestamps) >= self.rate_limit:
                tiempo_espera = self.rate_window - (ahora - self.message_timestamps[0])
                if tiempo_espera > 0:
                    app.logger.debug(f"Rate limit alcanzado, esperando {tiempo_espera:.1f} segundos...")
                    time.sleep(tiempo_espera)
                    # Limpiar timestamps después de esperar
                    ahora = time.time()
                    while self.message_timestamps and self.message_timestamps[0] < ahora - self.rate_window:
                        self.message_timestamps.popleft()
            
            # Agregar timestamp del mensaje actual
            self.message_timestamps.append(ahora)
    
    def _esperar_rate_limit(self):
        """Espera hasta que haya espacio en la ventana de rate limit"""
        with self.rate_lock:
            if self.message_timestamps:
                ahora = time.time()
                tiempo_espera = self.rate_window - (ahora - self.message_timestamps[0])
                if tiempo_espera > 0:
                    time.sleep(tiempo_espera)
    
    def _actualizar_metricas_exitoso(self, tiempo_envio):
        """Actualiza métricas después de un envío exitoso"""
        self.metrics['total_enviados'] += 1
        self.metrics['ultimo_envio'] = datetime.now()
        
        # Calcular tiempo promedio (media móvil simple)
        if self.metrics['tiempo_promedio_envio'] == 0:
            self.metrics['tiempo_promedio_envio'] = tiempo_envio
        else:
            # Media móvil exponencial
            alpha = 0.3
            self.metrics['tiempo_promedio_envio'] = (
                alpha * tiempo_envio + (1 - alpha) * self.metrics['tiempo_promedio_envio']
            )
    
    
    def _formatear_telefono(self, telefono):
        """
        Formatea teléfono al formato internacional requerido por UltraMsg
        Ejemplo: 0981123456 -> 595981123456 (sin el +)
        
        Args:
            telefono: Número de teléfono en cualquier formato
        
        Returns:
            str: Número formateado sin el símbolo +
        """
        # Remover espacios, guiones, paréntesis y el símbolo +
        telefono = ''.join(filter(lambda c: c.isdigit() or c == '+', str(telefono)))
        
        # Si empieza con +, removerlo
        if telefono.startswith('+'):
            telefono = telefono[1:]
        
        # Si empieza con 0, reemplazar por 595 (código de Paraguay)
        if telefono.startswith('0'):
            telefono = '595' + telefono[1:]
        
        # Si no tiene código país, agregar 595
        if not telefono.startswith('595'):
            telefono = '595' + telefono
        
        return telefono
    
    
    def _construir_mensaje_recordatorio(self, nombre, fecha, hora, 
                                         especialista, especialidad, motivo):
        """
        Construye mensaje de recordatorio personalizado
        
        Args:
            nombre: Nombre del paciente
            fecha: Fecha de la cita
            hora: Hora de la cita
            especialista: Nombre del especialista
            especialidad: Nombre de la especialidad
            motivo: Motivo de la cita (opcional)
        
        Returns:
            str: Mensaje formateado
        """
        # Formatear fecha
        if isinstance(fecha, datetime):
            fecha_formateada = fecha.strftime('%d/%m/%Y')
        elif isinstance(fecha, str):
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                fecha_formateada = fecha
        else:
            fecha_formateada = str(fecha)
        
        # Formatear hora
        if hasattr(hora, 'strftime'):
            hora_formateada = hora.strftime('%H:%M')
        elif isinstance(hora, str):
            # Intentar formatear si viene como string
            try:
                hora_obj = datetime.strptime(hora, '%H:%M:%S')
                hora_formateada = hora_obj.strftime('%H:%M')
            except:
                hora_formateada = hora
        else:
            hora_formateada = str(hora)
        
        # Construir mensaje
        mensaje = f"""🏥 *Recordatorio de Cita Médica*

Hola {nombre},

Le recordamos su cita:
📅 Fecha: {fecha_formateada}
🕐 Hora: {hora_formateada}
👨‍⚕️ Profesional: {especialista}
🩺 Especialidad: {especialidad}"""
        
        if motivo:
            mensaje += f"\n📋 Motivo: {motivo}"
        
        mensaje += """

Por favor confirme su asistencia respondiendo:
✅ SI - para confirmar
❌ NO - para cancelar

¡Gracias!"""
        
        return mensaje
    
    def enviar_notificacion_cita_creada_editada(self, telefono, nombre_paciente, cita_fecha, 
                                                 cita_hora, especialista, especialidad, 
                                                 nombre_clinica="Sysclin", es_edicion=False):
        """
        Envía notificación inmediata cuando se crea o edita una cita
        
        Args:
            telefono: Número de teléfono del paciente
            nombre_paciente: Nombre del paciente
            cita_fecha: Fecha de la cita
            cita_hora: Hora de la cita
            especialista: Nombre del especialista
            especialidad: Nombre de la especialidad
            nombre_clinica: Nombre de la clínica (opcional, default: "Sysclin")
            es_edicion: True si es edición, False si es creación
        
        Returns:
            tuple: (success: bool, message_id: str, error: str, tipo_error: TipoError)
        """
        if not self.client_available:
            error_msg = "Cliente UltraMsg no inicializado. Verifique la configuración."
            app.logger.error(error_msg)
            return (False, None, error_msg, TipoError.CONFIGURACION)
        
        try:
            # Validar teléfono
            if not telefono:
                error_msg = "Teléfono no proporcionado"
                app.logger.error(error_msg)
                return (False, None, error_msg, TipoError.PERMANENTE)
            
            # Formatear teléfono
            telefono_formateado = self._formatear_telefono(telefono)
            app.logger.debug(f"Teléfono formateado: {telefono_formateado}")
            
            # Construir mensaje
            mensaje = self._construir_mensaje_cita_creada_editada(
                nombre_paciente, cita_fecha, cita_hora, 
                especialista, especialidad, nombre_clinica, es_edicion
            )
            
            # Enviar con reintentos automáticos
            return self._enviar_con_reintentos(telefono_formateado, mensaje)
        
        except Exception as e:
            error_msg = f"Error inesperado enviando notificación: {str(e)}"
            app.logger.error(error_msg, exc_info=True)
            self.metrics['total_fallidos'] += 1
            return (False, None, error_msg, TipoError.DESCONOCIDO)
    
    def _construir_mensaje_cita_creada_editada(self, nombre, fecha, hora, 
                                                especialista, especialidad, 
                                                nombre_clinica, es_edicion):
        """
        Construye mensaje de notificación de cita creada/editada
        
        Args:
            nombre: Nombre del paciente
            fecha: Fecha de la cita
            hora: Hora de la cita
            especialista: Nombre del especialista
            especialidad: Nombre de la especialidad
            nombre_clinica: Nombre de la clínica
            es_edicion: True si es edición, False si es creación
        
        Returns:
            str: Mensaje formateado
        """
        # Formatear fecha
        if isinstance(fecha, datetime):
            fecha_formateada = fecha.strftime('%d/%m/%Y')
        elif isinstance(fecha, str):
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
                fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
            except:
                fecha_formateada = fecha
        else:
            fecha_formateada = str(fecha)
        
        # Formatear hora
        if hasattr(hora, 'strftime'):
            hora_formateada = hora.strftime('%H:%M')
        elif isinstance(hora, str):
            try:
                # Intentar diferentes formatos
                if ':' in hora:
                    partes = hora.split(':')
                    hora_formateada = f"{partes[0]}:{partes[1]}"
                else:
                    hora_formateada = hora
            except:
                hora_formateada = hora
        else:
            hora_formateada = str(hora)
        
        # Construir mensaje
        accion = "actualizada" if es_edicion else "creada"
        emoji_accion = "✏️" if es_edicion else "✅"
        
        mensaje = f"""{emoji_accion} *Su Cita ha sido {accion.upper()}*

Hola {nombre},

Su cita médica ha sido {accion} con los siguientes detalles:

📅 *Fecha:* {fecha_formateada}
🕐 *Hora:* {hora_formateada}
👨‍⚕️ *Profesional:* {especialista}
🩺 *Especialidad:* {especialidad}
🏥 *Clínica:* {nombre_clinica}

Recuerde que recibirá recordatorios automáticos 24 horas y 12 horas antes de su cita.

¡Gracias por confiar en nosotros!"""
        
        return mensaje
    
    
    def verificar_estado_mensaje(self, message_id):
        """
        Consulta el estado de un mensaje enviado
        
        Args:
            message_id: ID del mensaje de UltraMsg
            
        Returns:
            dict: Estado del mensaje con 'status', 'error_code', 'error_message'
            None si hay error
        """
        if not self.client_available:
            app.logger.error("Cliente UltraMsg no inicializado")
            return None
        
        try:
            # UltraMsg puede tener diferentes endpoints para verificar estado
            # Consultar documentación para el endpoint correcto
            url = f"{self.api_url}/{self.instance_id}/messages/{message_id}"
            
            params = {
                "token": self.token
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                estado = {
                    'status': data.get('status', 'unknown'),
                    'error_code': data.get('error_code'),
                    'error_message': data.get('error_message'),
                    'timestamp': data.get('timestamp')
                }
                app.logger.debug(f"Estado del mensaje {message_id}: {estado['status']}")
                return estado
            else:
                app.logger.warning(f"No se pudo verificar estado del mensaje {message_id}")
                return None
                
        except Exception as e:
            app.logger.error(f"Error verificando estado del mensaje {message_id}: {str(e)}", exc_info=True)
            return None
    
    
    def enviar_mensaje_simple(self, telefono, mensaje):
        """
        Envía un mensaje simple de texto con reintentos automáticos
        
        Args:
            telefono: Número de teléfono del destinatario
            mensaje: Texto del mensaje
        
        Returns:
            tuple: (success: bool, message_id: str, error: str)
        """
        if not self.client_available:
            error_msg = "Cliente UltraMsg no inicializado. Verifique la configuración."
            return (False, None, error_msg)
        
        try:
            telefono_formateado = self._formatear_telefono(telefono)
            success, message_id, error, _ = self._enviar_con_reintentos(telefono_formateado, mensaje)
            return (success, message_id, error)
        except Exception as e:
            error_msg = f"Error enviando mensaje: {str(e)}"
            app.logger.error(error_msg, exc_info=True)
            return (False, None, error_msg)
    
    def obtener_metricas(self):
        """
        Obtiene métricas del servicio
        
        Returns:
            dict: Diccionario con métricas
        """
        tasa_exito = 0.0
        if self.metrics['total_enviados'] + self.metrics['total_fallidos'] > 0:
            total = self.metrics['total_enviados'] + self.metrics['total_fallidos']
            tasa_exito = (self.metrics['total_enviados'] / total) * 100
        
        return {
            **self.metrics,
            'tasa_exito': round(tasa_exito, 2),
            'rate_limit_actual': len(self.message_timestamps),
            'rate_limit_maximo': self.rate_limit
        }
    
    def resetear_metricas(self):
        """Resetea las métricas del servicio"""
        self.metrics = {
            'total_enviados': 0,
            'total_fallidos': 0,
            'total_reintentos': 0,
            'errores_temporales': 0,
            'errores_permanentes': 0,
            'rate_limits': 0,
            'ultimo_envio': None,
            'tiempo_promedio_envio': 0.0
        }
        app.logger.info("Métricas del servicio UltraMsg reseteadas")

