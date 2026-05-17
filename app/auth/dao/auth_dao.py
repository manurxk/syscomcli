"""
DAO para operaciones de autenticación y seguridad
FASE 2: MEJORAS DE SEGURIDAD
"""
from typing import Tuple, Optional, Dict
from flask import current_app as app
from app.conexion.Conexion import Conexion
from werkzeug.security import generate_password_hash


class AuthDao:
    """Data Access Object para operaciones de autenticación"""
    
    @staticmethod
    def obtener_historial_passwords(id_usuario: int, limite: int = 5) -> list:
        """
        Obtiene el historial de contraseñas de un usuario
        """
        sql = """
            SELECT password_hash, fecha_cambio, motivo_cambio
            FROM password_history
            WHERE id_usuario = %s
            ORDER BY fecha_cambio DESC
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario, limite))
            rows = cur.fetchall()
            
            historial = []
            for row in rows:
                historial.append({
                    'password_hash': row[0],
                    'fecha_cambio': row[1],
                    'motivo_cambio': row[2]
                })
            
            return historial
        except Exception as e:
            app.logger.error(f"Error al obtener historial passwords: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def guardar_password_history(
        id_usuario: int,
        password_hash: str,
        cambiado_por: int = None,
        motivo_cambio: str = 'usuario'
    ) -> bool:
        """
        Guarda una contraseña en el historial
        """
        sql = """
            INSERT INTO password_history 
            (id_usuario, password_hash, cambiado_por, motivo_cambio)
            VALUES (%s, %s, %s, %s)
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario, password_hash, cambiado_por, motivo_cambio))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar historial password: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def limpiar_historial_antiguo(id_usuario: int, mantener: int = 5) -> bool:
        """
        Elimina registros antiguos del historial, manteniendo solo los últimos N
        """
        sql = """
            DELETE FROM password_history
            WHERE id_usuario = %s
            AND id_history NOT IN (
                SELECT id_history
                FROM password_history
                WHERE id_usuario = %s
                ORDER BY fecha_cambio DESC
                LIMIT %s
            )
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario, id_usuario, mantener))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al limpiar historial: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def cambiar_password(
        id_usuario: int,
        password_actual: str,
        password_nueva: str,
        password_hash_actual: str
    ) -> Tuple[bool, str]:
        """
        Cambia la contraseña de un usuario
        
        Returns:
            Tuple[bool, str]: (exitoso, mensaje_error)
        """
        from werkzeug.security import check_password_hash
        
        # Verificar password actual
        if not check_password_hash(password_hash_actual, password_actual):
            return False, "La contraseña actual es incorrecta"
        
        # Obtener historial
        historial = AuthDao.obtener_historial_passwords(id_usuario, limite=5)
        
        # Generar hash de nueva contraseña
        # Usar pbkdf2:sha256 para mantener consistencia con el resto del sistema
        password_nueva_hash = generate_password_hash(password_nueva, method='pbkdf2:sha256')
        
        # Verificar que no esté en historial
        for registro in historial:
            if registro['password_hash'] == password_nueva_hash:
                return False, "No puede reutilizar una contraseña reciente"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Guardar password actual en historial
            AuthDao.guardar_password_history(
                id_usuario=id_usuario,
                password_hash=password_hash_actual,
                motivo_cambio='usuario'
            )
            
            # Actualizar password
            sql = """
                UPDATE usuarios 
                SET usu_clave = %s,
                    fecha_cambio_password = CURRENT_TIMESTAMP,
                    requiere_cambio_password = FALSE
                WHERE id_usuario = %s
            """
            cur.execute(sql, (password_nueva_hash, id_usuario))
            
            # Cerrar todas las sesiones excepto la actual (si se pasa token)
            # Esto se maneja desde el servicio
            
            con.commit()
            
            # Limpiar historial antiguo
            AuthDao.limpiar_historial_antiguo(id_usuario, mantener=5)
            
            app.logger.info(f"Password cambiado exitosamente para usuario {id_usuario}")
            return True, "Contraseña cambiada exitosamente"
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al cambiar password: {str(e)}")
            return False, f"Error al cambiar contraseña: {str(e)}"
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def crear_password_reset_token(id_usuario: int, ip_solicitud: str, email_destino: str = None) -> Optional[str]:
        """
        Crea un token de recuperación de contraseña
        
        Returns:
            str: Token UUID generado, None si hay error
        """
        import uuid
        from datetime import datetime, timedelta
        
        token = str(uuid.uuid4())
        fecha_expiracion = datetime.now() + timedelta(hours=24)
        
        sql = """
            INSERT INTO password_reset_tokens
            (token, id_usuario, fecha_expiracion, ip_solicitud, email_destino)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING token
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (token, id_usuario, fecha_expiracion, ip_solicitud, email_destino))
            token_generado = cur.fetchone()[0]
            con.commit()
            return token_generado
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al crear token reset: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def validar_password_reset_token(token: str) -> Optional[Dict]:
        """
        Valida un token de recuperación de contraseña
        
        Returns:
            Dict con datos del token si es válido, None si no
        """
        sql = """
            SELECT id_token, id_usuario, fecha_expiracion, usado, email_destino
            FROM password_reset_tokens
            WHERE token = %s AND usado = FALSE AND fecha_expiracion > CURRENT_TIMESTAMP
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (token,))
            row = cur.fetchone()
            
            if row:
                return {
                    'id_token': row[0],
                    'id_usuario': row[1],
                    'fecha_expiracion': row[2],
                    'usado': row[3],
                    'email_destino': row[4]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al validar token reset: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def marcar_token_como_usado(token: str) -> bool:
        """
        Marca un token de recuperación como usado
        """
        sql = """
            UPDATE password_reset_tokens
            SET usado = TRUE, fecha_uso = CURRENT_TIMESTAMP
            WHERE token = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (token,))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al marcar token como usado: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    @staticmethod
    def resetear_password_con_token(token: str, password_nueva: str) -> Tuple[bool, str]:
        """
        Resetea la contraseña usando un token de recuperación
        
        Returns:
            Tuple[bool, str]: (exitoso, mensaje_error)
        """
        # Validar token
        token_data = AuthDao.validar_password_reset_token(token)
        if not token_data:
            return False, "Token inválido o expirado"
        
        id_usuario = token_data['id_usuario']
        
        # Obtener historial
        historial = AuthDao.obtener_historial_passwords(id_usuario, limite=5)
        
        # Generar hash de nueva contraseña
        # Usar pbkdf2:sha256 para mantener consistencia con el resto del sistema
        password_nueva_hash = generate_password_hash(password_nueva, method='pbkdf2:sha256')
        
        # Verificar que no esté en historial
        for registro in historial:
            if registro['password_hash'] == password_nueva_hash:
                return False, "No puede reutilizar una contraseña reciente"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Obtener password actual para guardarlo en historial
            sql = "SELECT usu_clave FROM usuarios WHERE id_usuario = %s"
            cur.execute(sql, (id_usuario,))
            password_actual_hash = cur.fetchone()[0]
            
            # Guardar password actual en historial
            AuthDao.guardar_password_history(
                id_usuario=id_usuario,
                password_hash=password_actual_hash,
                motivo_cambio='recuperacion'
            )
            
            # Actualizar password
            sql = """
                UPDATE usuarios 
                SET usu_clave = %s,
                    fecha_cambio_password = CURRENT_TIMESTAMP,
                    requiere_cambio_password = FALSE,
                    usu_nro_intentos = 0,
                    fecha_bloqueo = NULL,
                    motivo_bloqueo = NULL,
                    bloqueado_hasta = NULL
                WHERE id_usuario = %s
            """
            cur.execute(sql, (password_nueva_hash, id_usuario))
            
            # Marcar token como usado
            AuthDao.marcar_token_como_usado(token)
            
            # Cerrar todas las sesiones del usuario
            sql = """
                UPDATE sesiones
                SET sesion_activa = FALSE,
                    fecha_cierre = CURRENT_TIMESTAMP,
                    tipo_cierre = 'security'
                WHERE id_usuario = %s AND sesion_activa = TRUE
            """
            cur.execute(sql, (id_usuario,))
            
            con.commit()
            
            # Limpiar historial antiguo
            AuthDao.limpiar_historial_antiguo(id_usuario, mantener=5)
            
            app.logger.info(f"Password reseteado exitosamente para usuario {id_usuario} con token")
            return True, "Contraseña restablecida exitosamente"
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al resetear password: {str(e)}")
            return False, f"Error al restablecer contraseña: {str(e)}"
        finally:
            cur.close()
            con.close()

