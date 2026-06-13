from flask import current_app as app, session
from app.conexion.Conexion import Conexion

class CitaLogDao:
    
    def get_logs_por_cita(self, id_cita):
        """
        Obtiene el historial de cambios de estado de una cita.
        """
        logSQL = """
            SELECT
                id_cita_log,
                estado_anterior,
                estado_nuevo,
                motivo_cambio,
                usuario_cambio,
                fecha_cambio
            FROM citas_log_estados
            WHERE id_cita = %s
            ORDER BY fecha_cambio ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(logSQL, (id_cita,))
            logs = cur.fetchall()
            
            return [{
                'id_cita_log': l[0],
                'estado_anterior': l[1],
                'estado_nuevo': l[2],
                'motivo_cambio': l[3],
                'usuario_cambio': l[4],
                'fecha_cambio': l[5].strftime('%d/%m/%Y %H:%M:%S') if l[5] else None
            } for l in logs]
            
        except Exception as e:
            app.logger.error(f"Error al obtener logs de la cita {id_cita}: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
            
    def registrar_cambio(self, id_cita, estado_nuevo, estado_anterior=None, motivo_cambio=None, usuario=None):
        """
        Registra un cambio de estado en el log de la cita.
        """
        # Intentar obtener el usuario de la sesión si no se provee
        if not usuario:
            usuario = session.get('usuario_username', 'SISTEMA')
            
        insertSQL = """
            INSERT INTO citas_log_estados(
                id_cita, estado_anterior, estado_nuevo, motivo_cambio, usuario_cambio
            ) VALUES (%s, %s, %s, %s, %s)
            RETURNING id_cita_log
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertSQL, (
                id_cita,
                estado_anterior,
                estado_nuevo,
                motivo_cambio,
                usuario
            ))
            
            id_log = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Log registrado para cita {id_cita}: {estado_anterior} -> {estado_nuevo}")
            return id_log
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al registrar log para la cita {id_cita}: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
