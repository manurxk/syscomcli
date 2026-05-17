from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime
from app.dao.modulos.ventas.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao

class CobranzaDao:
    """DAO para gestionar cobranzas"""
    
    def getCobranzas(self):
        """Obtiene todas las cobranzas con sus datos completos"""
        cobranzaSQL = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.id_cuenta_cobrar,
                c.id_factura,
                c.id_caja,
                c.id_forma_cobro,
                c.fecha_cobranza,
                c.monto_cobrado,
                c.observaciones,
                c.est_cobranza,
                c.fecha_creacion,
                -- Datos de la cuenta a cobrar
                cc.cuenta_numero,
                cc.monto_pendiente AS monto_pendiente_cuenta,
                -- Datos de la factura
                f.factura_numero,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos de la forma de cobro
                fc.des_forma_cobro,
                -- Datos de la caja
                caja.des_caja
            FROM cobranzas c
            JOIN cuentas_cobrar cc ON c.id_cuenta_cobrar = cc.id_cuenta_cobrar
            JOIN facturas f ON c.id_factura = f.id_factura
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN formas_cobro fc ON c.id_forma_cobro = fc.id_forma_cobro
            JOIN cajas caja ON c.id_caja = caja.id_caja
            ORDER BY c.fecha_cobranza DESC, c.id_cobranza DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(cobranzaSQL)
            cobranzas = cur.fetchall()
            
            return [{
                'id_cobranza': cob[0],
                'cobranza_numero': cob[1],
                'id_cuenta_cobrar': cob[2],
                'id_factura': cob[3],
                'id_caja': cob[4],
                'id_forma_cobro': cob[5],
                'fecha_cobranza': cob[6].strftime('%d/%m/%Y %H:%M') if cob[6] else None,
                'monto_cobrado': cob[7],
                'observaciones': cob[8],
                'est_cobranza': cob[9],
                'fecha_registro': cob[10].strftime('%d/%m/%Y') if cob[10] else None,
                'cuenta_numero': cob[11],
                'monto_pendiente_cuenta': cob[12],
                'factura_numero': cob[13],
                'historia_clinica': cob[14],
                'paciente_nombre': cob[15],
                'paciente_cedula': cob[16],
                'forma_cobro': cob[17],
                'caja': cob[18]
            } for cob in cobranzas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las cobranzas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCobranzaById(self, id_cobranza):
        """Obtiene una cobranza específica por ID con su detalle"""
        cobranzaSQL = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.id_cuenta_cobrar,
                c.id_factura,
                c.id_caja,
                c.id_forma_cobro,
                c.fecha_cobranza,
                c.monto_cobrado,
                c.observaciones,
                c.est_cobranza,
                c.fecha_creacion,
                c.usuario_creacion,
                -- Datos de la cuenta a cobrar
                cc.cuenta_numero,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                -- Datos de la factura
                f.factura_numero,
                f.factura_total,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos de la forma de cobro
                fc.des_forma_cobro,
                -- Datos de la caja
                caja.des_caja
            FROM cobranzas c
            JOIN cuentas_cobrar cc ON c.id_cuenta_cobrar = cc.id_cuenta_cobrar
            JOIN facturas f ON c.id_factura = f.id_factura
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN formas_cobro fc ON c.id_forma_cobro = fc.id_forma_cobro
            JOIN cajas caja ON c.id_caja = caja.id_caja
            WHERE c.id_cobranza = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(cobranzaSQL, (id_cobranza,))
            cob = cur.fetchone()
            
            if not cob:
                return None
            
            return {
                'id_cobranza': cob[0],
                'cobranza_numero': cob[1],
                'id_cuenta_cobrar': cob[2],
                'id_factura': cob[3],
                'id_caja': cob[4],
                'id_forma_cobro': cob[5],
                'fecha_cobranza': cob[6].strftime('%Y-%m-%d %H:%M:%S') if cob[6] else None,
                'monto_cobrado': cob[7],
                'observaciones': cob[8],
                'est_cobranza': cob[9],
                'fecha_registro': cob[10].strftime('%Y-%m-%d') if cob[10] else None,
                'usuario_creacion': cob[11],
                'cuenta_numero': cob[12],
                'monto_total_cuenta': cob[13],
                'monto_pagado_cuenta': cob[14],
                'monto_pendiente_cuenta': cob[15],
                'factura_numero': cob[16],
                'factura_total': cob[17],
                'historia_clinica': cob[18],
                'paciente_nombre': cob[19],
                'paciente_cedula': cob[20],
                'forma_cobro': cob[21],
                'caja': cob[22]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener cobranza por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getCobranzaDetalle(self, id_cobranza):
        """Obtiene el detalle completo de una cobranza"""
        detalleSQL = """
            SELECT
                cd.id_cobranza_detalle,
                cd.id_cobranza,
                cd.id_forma_cobro,
                cd.id_marca_tarjeta,
                cd.id_entidad_adherida,
                cd.id_entidad_emisora,
                cd.numero_cheque,
                cd.numero_tarjeta,
                cd.numero_cuotas,
                cd.monto_cobrado,
                cd.observaciones,
                fc.des_forma_cobro,
                mt.des_marca_tarjeta,
                ea.des_entidad_adherida,
                ee.des_entidad_emisora
            FROM cobranza_detalle cd
            JOIN formas_cobro fc ON cd.id_forma_cobro = fc.id_forma_cobro
            LEFT JOIN marcas_tarjeta mt ON cd.id_marca_tarjeta = mt.id_marca_tarjeta
            LEFT JOIN entidades_adheridas ea ON cd.id_entidad_adherida = ea.id_entidad_adherida
            LEFT JOIN entidades_emisoras ee ON cd.id_entidad_emisora = ee.id_entidad_emisora
            WHERE cd.id_cobranza = %s
            ORDER BY cd.id_cobranza_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_cobranza,))
            detalles = cur.fetchall()
            
            return [{
                'id_cobranza_detalle': d[0],
                'id_cobranza': d[1],
                'id_forma_cobro': d[2],
                'id_marca_tarjeta': d[3],
                'id_entidad_adherida': d[4],
                'id_entidad_emisora': d[5],
                'numero_cheque': d[6],
                'numero_tarjeta': d[7],
                'numero_cuotas': d[8],
                'monto_cobrado': d[9],
                'observaciones': d[10],
                'forma_cobro': d[11],
                'marca_tarjeta': d[12] if d[12] else '',
                'entidad_adherida': d[13] if d[13] else '',
                'entidad_emisora': d[14] if d[14] else ''
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la cobranza: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroCobranza(self):
        """Genera un número único de cobranza"""
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT cobranza_numero 
            FROM cobranzas 
            WHERE cobranza_numero LIKE %s
            ORDER BY cobranza_numero DESC 
            LIMIT 1
        """
        patron = f'COB-{año}-{mes}-%'
        
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
            
            return f'COB-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de cobranza: {str(e)}")
            return f'COB-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def guardarCobranza(self, id_cuenta_cobrar, id_factura, id_caja, id_forma_cobro,
                       monto_cobrado, observaciones=None, est_cobranza='REGISTRADA',
                       usuario_creacion='ADMIN'):
        """Guarda una nueva cobranza y actualiza la cuenta a cobrar"""
        
        if not all([id_cuenta_cobrar, id_factura, id_caja, id_forma_cobro, monto_cobrado]):
            app.logger.error("Faltan campos obligatorios para guardar cobranza")
            return None
        
        # Generar número de cobranza
        cobranza_numero = self._generarNumeroCobranza()
        
        insertCobranzaSQL = """
            INSERT INTO cobranzas(
                cobranza_numero, id_cuenta_cobrar, id_factura, id_caja,
                id_forma_cobro, monto_cobrado, observaciones, est_cobranza, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_cobranza
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando cobranza para cuenta ID: {id_cuenta_cobrar}")
            
            cur.execute(insertCobranzaSQL, (
                cobranza_numero,
                id_cuenta_cobrar,
                id_factura,
                id_caja,
                id_forma_cobro,
                monto_cobrado,
                observaciones,
                est_cobranza,
                usuario_creacion
            ))
            
            cobranza_id = cur.fetchone()[0]
            
            # Actualizar cuenta a cobrar
            cuenta_dao = CuentaCobrarDao()
            cuenta_dao.registrarPago(id_cuenta_cobrar, monto_cobrado, usuario_creacion)
            
            con.commit()
            
            app.logger.info(f"Cobranza guardada exitosamente con ID: {cobranza_id}")
            return cobranza_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar cobranza: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarCobranzaDetalle(self, id_cobranza, id_forma_cobro, monto_cobrado,
                               id_marca_tarjeta=None, id_entidad_adherida=None,
                               id_entidad_emisora=None, numero_cheque=None,
                               numero_tarjeta=None, numero_cuotas=1, observaciones=None):
        """Guarda un detalle de cobranza (para múltiples formas de pago)"""
        
        if not all([id_cobranza, id_forma_cobro, monto_cobrado]):
            app.logger.error("Faltan campos obligatorios para guardar detalle de cobranza")
            return None
        
        insertDetalleSQL = """
            INSERT INTO cobranza_detalle(
                id_cobranza, id_forma_cobro, id_marca_tarjeta, id_entidad_adherida,
                id_entidad_emisora, numero_cheque, numero_tarjeta, numero_cuotas,
                monto_cobrado, observaciones
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_cobranza_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_cobranza,
                id_forma_cobro,
                id_marca_tarjeta,
                id_entidad_adherida,
                id_entidad_emisora,
                numero_cheque,
                numero_tarjeta,
                numero_cuotas,
                monto_cobrado,
                observaciones
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            return detalle_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar detalle de cobranza: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def updateCobranza(self, id_cobranza, observaciones=None, est_cobranza=None,
                      usuario_modificacion='ADMIN'):
        """Actualiza una cobranza existente"""
        
        campos = []
        valores = []
        
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_cobranza:
            campos.append("est_cobranza = %s")
            valores.append(est_cobranza)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_cobranza)
        
        updateSQL = f"""
            UPDATE cobranzas
            SET {', '.join(campos)}
            WHERE id_cobranza = %s
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
            app.logger.error(f"Error al actualizar cobranza: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def anularCobranza(self, id_cobranza, motivo_anulacion, usuario='ADMIN'):
        """Anula una cobranza y revierte el pago en la cuenta a cobrar"""
        
        # Obtener datos de la cobranza
        cobranza = self.getCobranzaById(id_cobranza)
        if not cobranza:
            return False
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Anular cobranza
            cur.execute("""
                UPDATE cobranzas
                SET est_cobranza = 'ANULADA',
                    observaciones = COALESCE(observaciones || E'\\n', '') || 'ANULADA: ' || %s,
                    fecha_modificacion = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_cobranza = %s
            """, (motivo_anulacion, usuario, id_cobranza))
            
            # Revertir pago en cuenta a cobrar
            cuenta_dao = CuentaCobrarDao()
            # Restar el monto pagado
            cur.execute("""
                UPDATE cuentas_cobrar
                SET monto_pagado = monto_pagado - %s,
                    monto_pendiente = monto_total - (monto_pagado - %s),
                    fecha_modificacion = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_cuenta_cobrar = %s
            """, (cobranza['monto_cobrado'], cobranza['monto_cobrado'], usuario, cobranza['id_cuenta_cobrar']))
            
            # Actualizar estado de la cuenta
            cuenta_dao.actualizarEstadoCuenta(cobranza['id_cuenta_cobrar'])
            
            con.commit()
            return True
            
        except Exception as e:
            app.logger.error(f"Error al anular cobranza: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getCobranzasPorCuenta(self, id_cuenta_cobrar):
        """Obtiene todas las cobranzas de una cuenta a cobrar"""
        sql = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.fecha_cobranza,
                c.monto_cobrado,
                fc.des_forma_cobro,
                c.est_cobranza
            FROM cobranzas c
            JOIN formas_cobro fc ON c.id_forma_cobro = fc.id_forma_cobro
            WHERE c.id_cuenta_cobrar = %s
            ORDER BY c.fecha_cobranza DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_cuenta_cobrar,))
            cobranzas = cur.fetchall()
            
            return [{
                'id_cobranza': cob[0],
                'cobranza_numero': cob[1],
                'fecha_cobranza': cob[2].strftime('%d/%m/%Y %H:%M') if cob[2] else None,
                'monto_cobrado': cob[3],
                'forma_cobro': cob[4],
                'est_cobranza': cob[5]
            } for cob in cobranzas]
        except Exception as e:
            app.logger.error(f"Error al obtener cobranzas de la cuenta: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















