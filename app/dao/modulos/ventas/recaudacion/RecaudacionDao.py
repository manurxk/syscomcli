from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class RecaudacionDao:
    """DAO para gestionar recaudaciones a depositar"""
    
    def getRecaudaciones(self):
        """Obtiene todas las recaudaciones"""
        recaudacionSQL = """
            SELECT
                r.id_recaudacion,
                r.id_caja,
                r.id_deposito,
                r.id_usuario,
                r.recaudacion_numero,
                r.fecha_recaudacion,
                r.fecha_deposito,
                r.monto_total,
                r.monto_efectivo,
                r.monto_cheques,
                r.monto_tarjetas,
                r.observaciones,
                r.est_recaudacion,
                r.fecha_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos del depósito
                dep.des_deposito,
                -- Datos del usuario
                u.usuario_nombre
            FROM recaudaciones r
            JOIN cajas caja ON r.id_caja = caja.id_caja
            JOIN depositos dep ON r.id_deposito = dep.id_deposito
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            ORDER BY r.fecha_recaudacion DESC, r.id_recaudacion DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(recaudacionSQL)
            recaudaciones = cur.fetchall()
            
            return [{
                'id_recaudacion': rec[0],
                'id_caja': rec[1],
                'id_deposito': rec[2],
                'id_usuario': rec[3],
                'recaudacion_numero': rec[4],
                'fecha_recaudacion': rec[5].strftime('%d/%m/%Y %H:%M') if rec[5] else None,
                'fecha_deposito': rec[6].strftime('%d/%m/%Y') if rec[6] else None,
                'monto_total': rec[7],
                'monto_efectivo': rec[8],
                'monto_cheques': rec[9],
                'monto_tarjetas': rec[10],
                'observaciones': rec[11],
                'est_recaudacion': rec[12],
                'fecha_registro': rec[13].strftime('%d/%m/%Y') if rec[13] else None,
                'caja': rec[14],
                'deposito': rec[15],
                'usuario': rec[16]
            } for rec in recaudaciones]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las recaudaciones: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getRecaudacionById(self, id_recaudacion):
        """Obtiene una recaudación específica por ID"""
        recaudacionSQL = """
            SELECT
                r.id_recaudacion,
                r.id_caja,
                r.id_deposito,
                r.id_usuario,
                r.recaudacion_numero,
                r.fecha_recaudacion,
                r.fecha_deposito,
                r.monto_total,
                r.monto_efectivo,
                r.monto_cheques,
                r.monto_tarjetas,
                r.observaciones,
                r.est_recaudacion,
                r.fecha_creacion,
                r.usuario_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos del depósito
                dep.des_deposito,
                -- Datos del usuario
                u.usuario_nombre
            FROM recaudaciones r
            JOIN cajas caja ON r.id_caja = caja.id_caja
            JOIN depositos dep ON r.id_deposito = dep.id_deposito
            JOIN usuarios u ON r.id_usuario = u.id_usuario
            WHERE r.id_recaudacion = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(recaudacionSQL, (id_recaudacion,))
            rec = cur.fetchone()
            
            if not rec:
                return None
            
            return {
                'id_recaudacion': rec[0],
                'id_caja': rec[1],
                'id_deposito': rec[2],
                'id_usuario': rec[3],
                'recaudacion_numero': rec[4],
                'fecha_recaudacion': rec[5].strftime('%Y-%m-%d %H:%M:%S') if rec[5] else None,
                'fecha_deposito': rec[6].strftime('%Y-%m-%d') if rec[6] else None,
                'monto_total': rec[7],
                'monto_efectivo': rec[8],
                'monto_cheques': rec[9],
                'monto_tarjetas': rec[10],
                'observaciones': rec[11],
                'est_recaudacion': rec[12],
                'fecha_registro': rec[13].strftime('%Y-%m-%d') if rec[13] else None,
                'usuario_creacion': rec[14],
                'caja': rec[15],
                'deposito': rec[16],
                'usuario': rec[17]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener recaudación por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getRecaudacionesPorCaja(self, id_caja):
        """Obtiene todas las recaudaciones de una caja específica"""
        sql = """
            SELECT
                r.id_recaudacion,
                r.recaudacion_numero,
                r.fecha_recaudacion,
                r.fecha_deposito,
                r.monto_total,
                r.est_recaudacion,
                dep.des_deposito
            FROM recaudaciones r
            JOIN depositos dep ON r.id_deposito = dep.id_deposito
            WHERE r.id_caja = %s
            ORDER BY r.fecha_recaudacion DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_caja,))
            recaudaciones = cur.fetchall()
            
            return [{
                'id_recaudacion': rec[0],
                'recaudacion_numero': rec[1],
                'fecha_recaudacion': rec[2].strftime('%d/%m/%Y %H:%M') if rec[2] else None,
                'fecha_deposito': rec[3].strftime('%d/%m/%Y') if rec[3] else None,
                'monto_total': rec[4],
                'est_recaudacion': rec[5],
                'deposito': rec[6]
            } for rec in recaudaciones]
        except Exception as e:
            app.logger.error(f"Error al obtener recaudaciones de la caja: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getRecaudacionesPendientes(self):
        """Obtiene todas las recaudaciones pendientes de depositar"""
        sql = """
            SELECT
                r.id_recaudacion,
                r.recaudacion_numero,
                r.fecha_recaudacion,
                r.monto_total,
                caja.des_caja,
                dep.des_deposito
            FROM recaudaciones r
            JOIN cajas caja ON r.id_caja = caja.id_caja
            JOIN depositos dep ON r.id_deposito = dep.id_deposito
            WHERE r.est_recaudacion = 'PENDIENTE'
            ORDER BY r.fecha_recaudacion ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            recaudaciones = cur.fetchall()
            
            return [{
                'id_recaudacion': rec[0],
                'recaudacion_numero': rec[1],
                'fecha_recaudacion': rec[2].strftime('%d/%m/%Y %H:%M') if rec[2] else None,
                'monto_total': rec[3],
                'caja': rec[4],
                'deposito': rec[5]
            } for rec in recaudaciones]
        except Exception as e:
            app.logger.error(f"Error al obtener recaudaciones pendientes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroRecaudacion(self):
        """Genera un número único de recaudación"""
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT recaudacion_numero 
            FROM recaudaciones 
            WHERE recaudacion_numero LIKE %s
            ORDER BY recaudacion_numero DESC 
            LIMIT 1
        """
        patron = f'REC-{año}-{mes}-%'
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (patron,))
            ultimo = cur.fetchone()
            
            if ultimo and ultimo[0]:
                # Extraer el número secuencial
                partes = ultimo[0].split('-')
                if len(partes) == 4:
                    siguiente_num = int(partes[3]) + 1
                else:
                    siguiente_num = 1
            else:
                siguiente_num = 1
            
            return f'REC-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de recaudación: {str(e)}")
            return f'REC-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def guardarRecaudacion(self, id_caja, id_deposito, id_usuario,
                          monto_total, monto_efectivo=0, monto_cheques=0,
                          monto_tarjetas=0, fecha_deposito=None,
                          observaciones=None, usuario_creacion='ADMIN'):
        """Registra una nueva recaudación"""
        
        if not all([id_caja, id_deposito, id_usuario, monto_total]):
            app.logger.error("Faltan campos obligatorios para guardar recaudación")
            return None
        
        # Validar que los montos sumen el total
        suma_montos = monto_efectivo + monto_cheques + monto_tarjetas
        if suma_montos != monto_total:
            app.logger.warning(f"La suma de montos ({suma_montos}) no coincide con el total ({monto_total})")
        
        # Generar número de recaudación
        recaudacion_numero = self._generarNumeroRecaudacion()
        
        insertRecaudacionSQL = """
            INSERT INTO recaudaciones(
                id_caja, id_deposito, id_usuario, recaudacion_numero,
                fecha_recaudacion, fecha_deposito, monto_total,
                monto_efectivo, monto_cheques, monto_tarjetas,
                observaciones, est_recaudacion, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, 'PENDIENTE', %s)
            RETURNING id_recaudacion
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando recaudación para caja ID: {id_caja}")
            
            cur.execute(insertRecaudacionSQL, (
                id_caja,
                id_deposito,
                id_usuario,
                recaudacion_numero,
                fecha_deposito,
                monto_total,
                monto_efectivo,
                monto_cheques,
                monto_tarjetas,
                observaciones,
                usuario_creacion
            ))
            
            recaudacion_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Recaudación guardada exitosamente con ID: {recaudacion_id}")
            return recaudacion_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar recaudación: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def updateRecaudacion(self, id_recaudacion, fecha_deposito=None,
                         monto_total=None, monto_efectivo=None,
                         monto_cheques=None, monto_tarjetas=None,
                         observaciones=None, est_recaudacion=None,
                         usuario_modificacion='ADMIN'):
        """Actualiza una recaudación existente"""
        
        campos = []
        valores = []
        
        if fecha_deposito is not None:
            campos.append("fecha_deposito = %s")
            valores.append(fecha_deposito)
        if monto_total is not None:
            campos.append("monto_total = %s")
            valores.append(monto_total)
        if monto_efectivo is not None:
            campos.append("monto_efectivo = %s")
            valores.append(monto_efectivo)
        if monto_cheques is not None:
            campos.append("monto_cheques = %s")
            valores.append(monto_cheques)
        if monto_tarjetas is not None:
            campos.append("monto_tarjetas = %s")
            valores.append(monto_tarjetas)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_recaudacion:
            campos.append("est_recaudacion = %s")
            valores.append(est_recaudacion)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_recaudacion)
        
        updateSQL = f"""
            UPDATE recaudaciones
            SET {', '.join(campos)}
            WHERE id_recaudacion = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar recaudación: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def marcarComoDepositada(self, id_recaudacion, fecha_deposito, usuario='ADMIN'):
        """Marca una recaudación como depositada"""
        return self.updateRecaudacion(
            id_recaudacion=id_recaudacion,
            fecha_deposito=fecha_deposito,
            est_recaudacion='DEPOSITADA',
            usuario_modificacion=usuario
        )
    
    def anularRecaudacion(self, id_recaudacion, motivo_anulacion, usuario='ADMIN'):
        """Anula una recaudación"""
        return self.updateRecaudacion(
            id_recaudacion=id_recaudacion,
            observaciones=motivo_anulacion,
            est_recaudacion='ANULADA',
            usuario_modificacion=usuario
        )

