from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime
from app.dao.modulos.ventas.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao

class ArqueoCajaDao:
    """DAO para gestionar arqueos de caja"""
    
    def getArqueos(self):
        """Obtiene todos los arqueos de caja"""
        arqueoSQL = """
            SELECT
                a.id_arqueo,
                a.id_apertura_cierre,
                a.id_caja,
                a.fecha_arqueo,
                a.arqueo_numero,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.observaciones,
                a.est_arqueo,
                a.fecha_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos de la apertura/cierre
                ac.tipo_operacion,
                ac.fecha_operacion AS fecha_apertura_cierre
            FROM arqueos_caja a
            JOIN cajas caja ON a.id_caja = caja.id_caja
            JOIN aperturas_cierre_caja ac ON a.id_apertura_cierre = ac.id_apertura_cierre
            ORDER BY a.fecha_arqueo DESC, a.id_arqueo DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(arqueoSQL)
            arqueos = cur.fetchall()
            
            return [{
                'id_arqueo': arq[0],
                'id_apertura_cierre': arq[1],
                'id_caja': arq[2],
                'fecha_arqueo': arq[3].strftime('%d/%m/%Y %H:%M') if arq[3] else None,
                'arqueo_numero': arq[4],
                'monto_esperado': arq[5],
                'monto_real': arq[6],
                'diferencia': arq[7],
                'observaciones': arq[8],
                'est_arqueo': arq[9],
                'fecha_registro': arq[10].strftime('%d/%m/%Y') if arq[10] else None,
                'caja': arq[11],
                'tipo_operacion': arq[12],
                'fecha_apertura_cierre': arq[13].strftime('%d/%m/%Y %H:%M') if arq[13] else None
            } for arq in arqueos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los arqueos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getArqueoById(self, id_arqueo):
        """Obtiene un arqueo específico por ID"""
        arqueoSQL = """
            SELECT
                a.id_arqueo,
                a.id_apertura_cierre,
                a.id_caja,
                a.fecha_arqueo,
                a.arqueo_numero,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.observaciones,
                a.est_arqueo,
                a.fecha_creacion,
                a.usuario_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos de la apertura/cierre
                ac.tipo_operacion,
                ac.fecha_operacion AS fecha_apertura_cierre,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias
            FROM arqueos_caja a
            JOIN cajas caja ON a.id_caja = caja.id_caja
            JOIN aperturas_cierre_caja ac ON a.id_apertura_cierre = ac.id_apertura_cierre
            WHERE a.id_arqueo = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(arqueoSQL, (id_arqueo,))
            arq = cur.fetchone()
            
            if not arq:
                return None
            
            return {
                'id_arqueo': arq[0],
                'id_apertura_cierre': arq[1],
                'id_caja': arq[2],
                'fecha_arqueo': arq[3].strftime('%Y-%m-%d %H:%M:%S') if arq[3] else None,
                'arqueo_numero': arq[4],
                'monto_esperado': arq[5],
                'monto_real': arq[6],
                'diferencia': arq[7],
                'observaciones': arq[8],
                'est_arqueo': arq[9],
                'fecha_registro': arq[10].strftime('%Y-%m-%d') if arq[10] else None,
                'usuario_creacion': arq[11],
                'caja': arq[12],
                'tipo_operacion': arq[13],
                'fecha_apertura_cierre': arq[14].strftime('%Y-%m-%d %H:%M:%S') if arq[14] else None,
                'saldo_inicial': arq[15],
                'saldo_final': arq[16],
                'monto_efectivo': arq[17],
                'monto_cheques': arq[18],
                'monto_tarjetas': arq[19],
                'monto_transferencias': arq[20]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener arqueo por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getArqueosPorCaja(self, id_caja):
        """Obtiene todos los arqueos de una caja específica"""
        sql = """
            SELECT
                a.id_arqueo,
                a.fecha_arqueo,
                a.arqueo_numero,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.est_arqueo
            FROM arqueos_caja a
            WHERE a.id_caja = %s
            ORDER BY a.fecha_arqueo DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_caja,))
            arqueos = cur.fetchall()
            
            return [{
                'id_arqueo': arq[0],
                'fecha_arqueo': arq[1].strftime('%d/%m/%Y %H:%M') if arq[1] else None,
                'arqueo_numero': arq[2],
                'monto_esperado': arq[3],
                'monto_real': arq[4],
                'diferencia': arq[5],
                'est_arqueo': arq[6]
            } for arq in arqueos]
        except Exception as e:
            app.logger.error(f"Error al obtener arqueos de la caja: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getArqueosPorAperturaCierre(self, id_apertura_cierre):
        """Obtiene todos los arqueos de una apertura/cierre específica"""
        sql = """
            SELECT
                a.id_arqueo,
                a.fecha_arqueo,
                a.arqueo_numero,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.est_arqueo
            FROM arqueos_caja a
            WHERE a.id_apertura_cierre = %s
            ORDER BY a.fecha_arqueo DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_apertura_cierre,))
            arqueos = cur.fetchall()
            
            return [{
                'id_arqueo': arq[0],
                'fecha_arqueo': arq[1].strftime('%d/%m/%Y %H:%M') if arq[1] else None,
                'arqueo_numero': arq[2],
                'monto_esperado': arq[3],
                'monto_real': arq[4],
                'diferencia': arq[5],
                'est_arqueo': arq[6]
            } for arq in arqueos]
        except Exception as e:
            app.logger.error(f"Error al obtener arqueos de la apertura/cierre: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroArqueo(self):
        """Genera un número único de arqueo"""
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT arqueo_numero 
            FROM arqueos_caja 
            WHERE arqueo_numero LIKE %s
            ORDER BY arqueo_numero DESC 
            LIMIT 1
        """
        patron = f'ARQ-{año}-{mes}-%'
        
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
            
            return f'ARQ-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de arqueo: {str(e)}")
            return f'ARQ-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def calcularMontoEsperado(self, id_apertura_cierre, id_caja):
        """Calcula el monto esperado basado en la apertura/cierre y las cobranzas"""
        apertura_dao = AperturaCierreCajaDao()
        
        # Obtener información de la apertura/cierre
        sql = """
            SELECT
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.fecha_operacion
            FROM aperturas_cierre_caja ac
            WHERE ac.id_apertura_cierre = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_apertura_cierre,))
            apertura = cur.fetchone()
            
            if not apertura:
                return None
            
            saldo_inicial = apertura[0] or 0
            saldo_final = apertura[1]
            fecha_operacion = apertura[6]
            
            # Si hay saldo final, usar ese (es un cierre)
            if saldo_final is not None:
                return saldo_final
            
            # Si no hay saldo final, calcular desde la apertura hasta ahora
            # Sumar todas las cobranzas desde la apertura
            sql_cobranzas = """
                SELECT
                    COALESCE(SUM(cd.monto_cobrado), 0) AS total_cobrado
                FROM cobranzas c
                JOIN cobranza_detalle cd ON c.id_cobranza = cd.id_cobranza
                WHERE c.id_caja = %s
                    AND c.fecha_cobranza >= %s
                    AND c.est_cobranza = 'REGISTRADA'
            """
            
            cur.execute(sql_cobranzas, (id_caja, fecha_operacion))
            resultado = cur.fetchone()
            total_cobrado = resultado[0] if resultado else 0
            
            return saldo_inicial + total_cobrado
            
        except Exception as e:
            app.logger.error(f"Error al calcular monto esperado: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarArqueo(self, id_apertura_cierre, id_caja, monto_real,
                     observaciones=None, usuario_creacion='ADMIN'):
        """Registra un nuevo arqueo de caja"""
        
        if not all([id_apertura_cierre, id_caja, monto_real is not None]):
            app.logger.error("Faltan campos obligatorios para guardar arqueo")
            return None
        
        # Calcular monto esperado
        monto_esperado = self.calcularMontoEsperado(id_apertura_cierre, id_caja)
        if monto_esperado is None:
            app.logger.error("No se pudo calcular el monto esperado")
            return None
        
        # Calcular diferencia
        diferencia = monto_real - monto_esperado
        
        # Determinar estado según diferencia
        if diferencia == 0:
            est_arqueo = 'CONCILIADO'
        elif abs(diferencia) <= 1000:  # Diferencia menor o igual a 1000 Gs.
            est_arqueo = 'CONCILIADO'
        else:
            est_arqueo = 'CON_DIFERENCIA'
        
        # Generar número de arqueo
        arqueo_numero = self._generarNumeroArqueo()
        
        insertArqueoSQL = """
            INSERT INTO arqueos_caja(
                id_apertura_cierre, id_caja, fecha_arqueo, arqueo_numero,
                monto_esperado, monto_real, diferencia, observaciones,
                est_arqueo, usuario_creacion
            )
            VALUES(%s, %s, CURRENT_TIMESTAMP, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_arqueo
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando arqueo para caja ID: {id_caja}")
            
            cur.execute(insertArqueoSQL, (
                id_apertura_cierre,
                id_caja,
                arqueo_numero,
                monto_esperado,
                monto_real,
                diferencia,
                observaciones,
                est_arqueo,
                usuario_creacion
            ))
            
            arqueo_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Arqueo guardado exitosamente con ID: {arqueo_id}")
            return arqueo_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar arqueo: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def updateArqueo(self, id_arqueo, monto_real=None, observaciones=None,
                    est_arqueo=None, usuario_modificacion='ADMIN'):
        """Actualiza un arqueo existente"""
        
        # Si se actualiza monto_real, recalcular diferencia y estado
        if monto_real is not None:
            # Obtener monto esperado del arqueo
            arqueo = self.getArqueoById(id_arqueo)
            if not arqueo:
                return False
            
            diferencia = monto_real - arqueo['monto_esperado']
            
            # Determinar estado según diferencia
            if diferencia == 0:
                nuevo_estado = 'CONCILIADO'
            elif abs(diferencia) <= 1000:
                nuevo_estado = 'CONCILIADO'
            else:
                nuevo_estado = 'CON_DIFERENCIA'
            
            if est_arqueo is None:
                est_arqueo = nuevo_estado
        
        campos = []
        valores = []
        
        if monto_real is not None:
            campos.append("monto_real = %s")
            valores.append(monto_real)
            campos.append("diferencia = %s")
            valores.append(diferencia)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_arqueo:
            campos.append("est_arqueo = %s")
            valores.append(est_arqueo)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_arqueo)
        
        updateSQL = f"""
            UPDATE arqueos_caja
            SET {', '.join(campos)}
            WHERE id_arqueo = %s
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
            app.logger.error(f"Error al actualizar arqueo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def conciliarArqueo(self, id_arqueo, observaciones_conciliacion=None, usuario='ADMIN'):
        """Marca un arqueo como conciliado"""
        return self.updateArqueo(
            id_arqueo=id_arqueo,
            est_arqueo='CONCILIADO',
            observaciones=observaciones_conciliacion,
            usuario_modificacion=usuario
        )


















