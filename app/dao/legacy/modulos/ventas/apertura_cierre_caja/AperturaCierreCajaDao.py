from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class AperturaCierreCajaDao:
    """DAO para gestionar aperturas y cierres de caja"""
    
    def getAperturasCierres(self):
        """Obtiene todas las aperturas y cierres de caja"""
        aperturaSQL = """
            SELECT
                ac.id_apertura_cierre,
                ac.id_caja,
                ac.id_usuario,
                ac.tipo_operacion,
                ac.fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                ac.fecha_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos del usuario
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario_nombre
            FROM aperturas_cierre_caja ac
            JOIN cajas caja ON ac.id_caja = caja.id_caja
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            ORDER BY ac.fecha_operacion DESC, ac.id_apertura_cierre DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(aperturaSQL)
            aperturas = cur.fetchall()
            
            return [{
                'id_apertura_cierre': ap[0],
                'id_caja': ap[1],
                'id_usuario': ap[2],
                'tipo_operacion': ap[3],
                'fecha_operacion': ap[4].strftime('%d/%m/%Y %H:%M') if ap[4] else None,
                'saldo_inicial': ap[5],
                'saldo_final': ap[6],
                'monto_efectivo': ap[7],
                'monto_cheques': ap[8],
                'monto_tarjetas': ap[9],
                'monto_transferencias': ap[10],
                'observaciones': ap[11],
                'est_apertura_cierre': ap[12],
                'fecha_registro': ap[13].strftime('%d/%m/%Y') if ap[13] else None,
                'caja': ap[14],
                'usuario': ap[15]
            } for ap in aperturas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las aperturas/cierres: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getAperturaCierreById(self, id_apertura_cierre):
        """Obtiene una apertura/cierre específica por ID"""
        aperturaSQL = """
            SELECT
                ac.id_apertura_cierre,
                ac.id_caja,
                ac.id_usuario,
                ac.tipo_operacion,
                ac.fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                ac.fecha_creacion,
                ac.usuario_creacion,
                -- Datos de la caja
                caja.des_caja,
                -- Datos del usuario
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario_nombre
            FROM aperturas_cierre_caja ac
            JOIN cajas caja ON ac.id_caja = caja.id_caja
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE ac.id_apertura_cierre = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(aperturaSQL, (id_apertura_cierre,))
            ap = cur.fetchone()
            
            if not ap:
                return None
            
            return {
                'id_apertura_cierre': ap[0],
                'id_caja': ap[1],
                'id_usuario': ap[2],
                'tipo_operacion': ap[3],
                'fecha_operacion': ap[4].strftime('%Y-%m-%d %H:%M:%S') if ap[4] else None,
                'saldo_inicial': ap[5],
                'saldo_final': ap[6],
                'monto_efectivo': ap[7],
                'monto_cheques': ap[8],
                'monto_tarjetas': ap[9],
                'monto_transferencias': ap[10],
                'observaciones': ap[11],
                'est_apertura_cierre': ap[12],
                'fecha_registro': ap[13].strftime('%Y-%m-%d') if ap[13] else None,
                'usuario_creacion': ap[14],
                'caja': ap[15],
                'usuario': ap[16]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener apertura/cierre por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getAperturaActivaPorCaja(self, id_caja):
        """Obtiene la apertura activa de una caja específica"""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.fecha_operacion,
                ac.saldo_inicial,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias
            FROM aperturas_cierre_caja ac
            WHERE ac.id_caja = %s
                AND ac.tipo_operacion = 'APERTURA'
                AND ac.est_apertura_cierre = 'A'
            ORDER BY ac.fecha_operacion DESC
            LIMIT 1
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_caja,))
            ap = cur.fetchone()
            
            if not ap:
                return None
            
            return {
                'id_apertura_cierre': ap[0],
                'fecha_operacion': ap[1].strftime('%Y-%m-%d %H:%M:%S') if ap[1] else None,
                'saldo_inicial': ap[2],
                'monto_efectivo': ap[3],
                'monto_cheques': ap[4],
                'monto_tarjetas': ap[5],
                'monto_transferencias': ap[6]
            }
        except Exception as e:
            app.logger.error(f"Error al obtener apertura activa: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getAperturasCierresPorCaja(self, id_caja):
        """Obtiene todas las aperturas/cierres de una caja específica"""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.tipo_operacion,
                ac.fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.est_apertura_cierre,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario_nombre
            FROM aperturas_cierre_caja ac
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE ac.id_caja = %s
            ORDER BY ac.fecha_operacion DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_caja,))
            aperturas = cur.fetchall()
            
            return [{
                'id_apertura_cierre': ap[0],
                'tipo_operacion': ap[1],
                'fecha_operacion': ap[2].strftime('%d/%m/%Y %H:%M') if ap[2] else None,
                'saldo_inicial': ap[3],
                'saldo_final': ap[4],
                'est_apertura_cierre': ap[5],
                'usuario': ap[6]
            } for ap in aperturas]
        except Exception as e:
            app.logger.error(f"Error al obtener aperturas/cierres de la caja: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarApertura(self, id_caja, id_usuario, saldo_inicial=0,
                       observaciones=None, usuario_creacion='ADMIN'):
        """Registra una apertura de caja"""
        
        if not all([id_caja, id_usuario]):
            app.logger.error("Faltan campos obligatorios para guardar apertura")
            return None
        
        # Verificar que no haya una apertura activa
        apertura_activa = self.getAperturaActivaPorCaja(id_caja)
        if apertura_activa:
            app.logger.error(f"Ya existe una apertura activa para la caja {id_caja}")
            return None
        
        insertAperturaSQL = """
            INSERT INTO aperturas_cierre_caja(
                id_caja, id_usuario, tipo_operacion, saldo_inicial,
                monto_efectivo, monto_cheques, monto_tarjetas, monto_transferencias,
                observaciones, est_apertura_cierre, usuario_creacion
            )
            VALUES(%s, %s, 'APERTURA', %s, %s, %s, %s, %s, %s, 'A', %s)
            RETURNING id_apertura_cierre
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando apertura de caja ID: {id_caja}")
            
            cur.execute(insertAperturaSQL, (
                id_caja,
                id_usuario,
                saldo_inicial,
                saldo_inicial,  # monto_efectivo inicial igual al saldo inicial
                0,  # monto_cheques
                0,  # monto_tarjetas
                0,  # monto_transferencias
                observaciones,
                usuario_creacion
            ))
            
            apertura_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Apertura guardada exitosamente con ID: {apertura_id}")
            return apertura_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar apertura: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarCierre(self, id_caja, id_usuario, saldo_final,
                     monto_efectivo=0, monto_cheques=0, monto_tarjetas=0,
                     monto_transferencias=0, observaciones=None,
                     usuario_creacion='ADMIN'):
        """Registra un cierre de caja"""
        
        if not all([id_caja, id_usuario, saldo_final is not None]):
            app.logger.error("Faltan campos obligatorios para guardar cierre")
            return None
        
        # Verificar que haya una apertura activa
        apertura_activa = self.getAperturaActivaPorCaja(id_caja)
        if not apertura_activa:
            app.logger.error(f"No hay apertura activa para la caja {id_caja}")
            return None
        
        # Cerrar la apertura activa
        updateAperturaSQL = """
            UPDATE aperturas_cierre_caja
            SET est_apertura_cierre = 'C',
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_apertura_cierre = %s
        """
        
        # Insertar el cierre
        insertCierreSQL = """
            INSERT INTO aperturas_cierre_caja(
                id_caja, id_usuario, tipo_operacion, saldo_inicial,
                saldo_final, monto_efectivo, monto_cheques, monto_tarjetas,
                monto_transferencias, observaciones, est_apertura_cierre, usuario_creacion
            )
            VALUES(%s, %s, 'CIERRE', %s, %s, %s, %s, %s, %s, %s, 'C', %s)
            RETURNING id_apertura_cierre
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando cierre de caja ID: {id_caja}")
            
            # Cerrar apertura activa
            cur.execute(updateAperturaSQL, (usuario_creacion, apertura_activa['id_apertura_cierre']))
            
            # Insertar cierre
            cur.execute(insertCierreSQL, (
                id_caja,
                id_usuario,
                apertura_activa['saldo_inicial'],
                saldo_final,
                monto_efectivo,
                monto_cheques,
                monto_tarjetas,
                monto_transferencias,
                observaciones,
                usuario_creacion
            ))
            
            cierre_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Cierre guardado exitosamente con ID: {cierre_id}")
            return cierre_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar cierre: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def calcularSaldoEsperado(self, id_caja):
        """Calcula el saldo esperado de una caja basado en las operaciones"""
        # Obtener apertura activa
        apertura = self.getAperturaActivaPorCaja(id_caja)
        if not apertura:
            return None
        
        # Calcular total de cobranzas desde la apertura
        sql = """
            SELECT
                COALESCE(SUM(
                    CASE WHEN cd.id_forma_cobro = (SELECT id_forma_cobro FROM formas_cobro WHERE cod_forma_cobro = 'EFECTIVO' LIMIT 1) 
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_efectivo,
                COALESCE(SUM(
                    CASE WHEN cd.id_forma_cobro = (SELECT id_forma_cobro FROM formas_cobro WHERE cod_forma_cobro = 'CHEQUE' LIMIT 1) 
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_cheques,
                COALESCE(SUM(
                    CASE WHEN cd.id_forma_cobro IN (
                        SELECT id_forma_cobro FROM formas_cobro 
                        WHERE cod_forma_cobro IN ('TARJETA_CREDITO', 'TARJETA_DEBITO') 
                    )
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_tarjetas,
                COALESCE(SUM(
                    CASE WHEN cd.id_forma_cobro = (SELECT id_forma_cobro FROM formas_cobro WHERE cod_forma_cobro = 'TRANSFERENCIA' LIMIT 1) 
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_transferencias
            FROM cobranzas c
            JOIN cobranza_detalle cd ON c.id_cobranza = cd.id_cobranza
            WHERE c.id_caja = %s
                AND c.fecha_cobranza >= %s
                AND c.est_cobranza = 'REGISTRADA'
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_caja, apertura['fecha_operacion']))
            resultado = cur.fetchone()
            
            if resultado:
                return {
                    'saldo_inicial': apertura['saldo_inicial'],
                    'total_efectivo': resultado[0],
                    'total_cheques': resultado[1],
                    'total_tarjetas': resultado[2],
                    'total_transferencias': resultado[3],
                    'saldo_esperado': apertura['saldo_inicial'] + resultado[0] + resultado[1] + resultado[2] + resultado[3]
                }
            else:
                return {
                    'saldo_inicial': apertura['saldo_inicial'],
                    'total_efectivo': 0,
                    'total_cheques': 0,
                    'total_tarjetas': 0,
                    'total_transferencias': 0,
                    'saldo_esperado': apertura['saldo_inicial']
                }
        except Exception as e:
            app.logger.error(f"Error al calcular saldo esperado: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def updateAperturaCierre(self, id_apertura_cierre, observaciones=None,
                            usuario_modificacion='ADMIN'):
        """Actualiza una apertura/cierre existente"""
        
        campos = []
        valores = []
        
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_apertura_cierre)
        
        updateSQL = f"""
            UPDATE aperturas_cierre_caja
            SET {', '.join(campos)}
            WHERE id_apertura_cierre = %s
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
            app.logger.error(f"Error al actualizar apertura/cierre: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getHistorialCaja(self, id_caja, fecha_desde=None, fecha_hasta=None):
        """Obtiene el historial completo de una caja en un rango de fechas"""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.tipo_operacion,
                ac.fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario_nombre
            FROM aperturas_cierre_caja ac
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE ac.id_caja = %s
        """
        
        valores = [id_caja]
        
        if fecha_desde:
            sql += " AND DATE(ac.fecha_operacion) >= %s"
            valores.append(fecha_desde)
        if fecha_hasta:
            sql += " AND DATE(ac.fecha_operacion) <= %s"
            valores.append(fecha_hasta)
        
        sql += " ORDER BY ac.fecha_operacion DESC"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, tuple(valores))
            historial = cur.fetchall()
            
            return [{
                'id_apertura_cierre': h[0],
                'tipo_operacion': h[1],
                'fecha_operacion': h[2].strftime('%d/%m/%Y %H:%M') if h[2] else None,
                'saldo_inicial': h[3],
                'saldo_final': h[4],
                'monto_efectivo': h[5],
                'monto_cheques': h[6],
                'monto_tarjetas': h[7],
                'monto_transferencias': h[8],
                'observaciones': h[9],
                'est_apertura_cierre': h[10],
                'usuario': h[11]
            } for h in historial]
        except Exception as e:
            app.logger.error(f"Error al obtener historial de caja: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()




