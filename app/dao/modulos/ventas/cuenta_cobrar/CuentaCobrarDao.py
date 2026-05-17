from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date, timedelta

class CuentaCobrarDao:
    """DAO para gestionar cuentas a cobrar"""
    
    def getCuentasCobrar(self):
        """Obtiene todas las cuentas a cobrar con sus datos completos"""
        cuentaSQL = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.fecha_emision,
                cc.fecha_vencimiento,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.numero_cuotas,
                cc.cuota_actual,
                cc.observaciones,
                cc.est_cuenta_cobrar,
                cc.fecha_creacion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos de la factura
                f.factura_numero,
                f.fecha_factura,
                f.factura_total,
                -- Calcular días de vencimiento
                CASE 
                    WHEN cc.est_cuenta_cobrar = 'VENCIDA' THEN -1
                    WHEN cc.fecha_vencimiento < CURRENT_DATE THEN 
                        EXTRACT(DAY FROM (CURRENT_DATE - cc.fecha_vencimiento))::INTEGER
                    WHEN cc.fecha_vencimiento >= CURRENT_DATE THEN 
                        EXTRACT(DAY FROM (cc.fecha_vencimiento - CURRENT_DATE))::INTEGER
                    ELSE 0
                END AS dias_vencimiento
            FROM cuentas_cobrar cc
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN facturas f ON cc.id_factura = f.id_factura
            ORDER BY cc.fecha_vencimiento ASC, cc.id_cuenta_cobrar DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(cuentaSQL)
            cuentas = cur.fetchall()
            
            return [{
                'id_cuenta_cobrar': cta[0],
                'cuenta_numero': cta[1],
                'id_factura': cta[2],
                'id_paciente': cta[3],
                'fecha_emision': cta[4].strftime('%d/%m/%Y') if cta[4] else None,
                'fecha_vencimiento': cta[5].strftime('%d/%m/%Y') if cta[5] else None,
                'monto_total': cta[6],
                'monto_pagado': cta[7],
                'monto_pendiente': cta[8],
                'numero_cuotas': cta[9],
                'cuota_actual': cta[10],
                'observaciones': cta[11],
                'est_cuenta_cobrar': cta[12],
                'fecha_registro': cta[13].strftime('%d/%m/%Y') if cta[13] else None,
                'historia_clinica': cta[14],
                'paciente_nombre': cta[15],
                'paciente_cedula': cta[16],
                'factura_numero': cta[17],
                'fecha_factura': cta[18].strftime('%d/%m/%Y') if cta[18] else None,
                'factura_total': cta[19],
                'dias_vencimiento': cta[20]
            } for cta in cuentas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las cuentas a cobrar: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCuentaCobrarById(self, id_cuenta_cobrar):
        """Obtiene una cuenta a cobrar específica por ID"""
        cuentaSQL = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.id_factura,
                cc.id_paciente,
                cc.fecha_emision,
                cc.fecha_vencimiento,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.numero_cuotas,
                cc.cuota_actual,
                cc.observaciones,
                cc.est_cuenta_cobrar,
                cc.fecha_creacion,
                cc.usuario_creacion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                pp.per_direccion AS paciente_direccion,
                -- Datos de la factura
                f.factura_numero,
                f.fecha_factura,
                f.factura_total,
                f.codigo_sifen
            FROM cuentas_cobrar cc
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN facturas f ON cc.id_factura = f.id_factura
            WHERE cc.id_cuenta_cobrar = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(cuentaSQL, (id_cuenta_cobrar,))
            cta = cur.fetchone()
            
            if not cta:
                return None
            
            return {
                'id_cuenta_cobrar': cta[0],
                'cuenta_numero': cta[1],
                'id_factura': cta[2],
                'id_paciente': cta[3],
                'fecha_emision': cta[4].strftime('%Y-%m-%d') if cta[4] else None,
                'fecha_vencimiento': cta[5].strftime('%Y-%m-%d') if cta[5] else None,
                'monto_total': cta[6],
                'monto_pagado': cta[7],
                'monto_pendiente': cta[8],
                'numero_cuotas': cta[9],
                'cuota_actual': cta[10],
                'observaciones': cta[11],
                'est_cuenta_cobrar': cta[12],
                'fecha_registro': cta[13].strftime('%Y-%m-%d') if cta[13] else None,
                'usuario_creacion': cta[14],
                'historia_clinica': cta[15],
                'paciente_nombre': cta[16],
                'paciente_cedula': cta[17],
                'paciente_telefono': cta[18],
                'paciente_direccion': cta[19],
                'factura_numero': cta[20],
                'fecha_factura': cta[21].strftime('%Y-%m-%d') if cta[21] else None,
                'factura_total': cta[22],
                'codigo_sifen': cta[23]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener cuenta a cobrar por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getCuentasCobrarPorPaciente(self, id_paciente):
        """Obtiene todas las cuentas a cobrar de un paciente"""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.fecha_vencimiento,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.est_cuenta_cobrar,
                f.factura_numero
            FROM cuentas_cobrar cc
            JOIN facturas f ON cc.id_factura = f.id_factura
            WHERE cc.id_paciente = %s
            ORDER BY cc.fecha_vencimiento ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_paciente,))
            cuentas = cur.fetchall()
            
            return [{
                'id_cuenta_cobrar': cta[0],
                'cuenta_numero': cta[1],
                'fecha_vencimiento': cta[2].strftime('%d/%m/%Y') if cta[2] else None,
                'monto_total': cta[3],
                'monto_pagado': cta[4],
                'monto_pendiente': cta[5],
                'est_cuenta_cobrar': cta[6],
                'factura_numero': cta[7]
            } for cta in cuentas]
        except Exception as e:
            app.logger.error(f"Error al obtener cuentas a cobrar del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCuentasCobrarPorEstado(self, estado):
        """Obtiene cuentas a cobrar filtradas por estado"""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.fecha_vencimiento,
                cc.monto_total,
                cc.monto_pagado,
                cc.monto_pendiente,
                cc.est_cuenta_cobrar,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                f.factura_numero
            FROM cuentas_cobrar cc
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN facturas f ON cc.id_factura = f.id_factura
            WHERE cc.est_cuenta_cobrar = %s
            ORDER BY cc.fecha_vencimiento ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (estado,))
            cuentas = cur.fetchall()
            
            return [{
                'id_cuenta_cobrar': cta[0],
                'cuenta_numero': cta[1],
                'fecha_vencimiento': cta[2].strftime('%d/%m/%Y') if cta[2] else None,
                'monto_total': cta[3],
                'monto_pagado': cta[4],
                'monto_pendiente': cta[5],
                'est_cuenta_cobrar': cta[6],
                'paciente_nombre': cta[7],
                'factura_numero': cta[8]
            } for cta in cuentas]
        except Exception as e:
            app.logger.error(f"Error al obtener cuentas a cobrar por estado: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCuentasVencidas(self):
        """Obtiene todas las cuentas a cobrar vencidas"""
        sql = """
            SELECT
                cc.id_cuenta_cobrar,
                cc.cuenta_numero,
                cc.fecha_vencimiento,
                cc.monto_pendiente,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                f.factura_numero,
                EXTRACT(DAY FROM (CURRENT_DATE - cc.fecha_vencimiento))::INTEGER AS dias_vencido
            FROM cuentas_cobrar cc
            JOIN pacientes pac ON cc.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN facturas f ON cc.id_factura = f.id_factura
            WHERE cc.fecha_vencimiento < CURRENT_DATE 
                AND cc.est_cuenta_cobrar IN ('PENDIENTE', 'PARCIAL')
            ORDER BY cc.fecha_vencimiento ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            cuentas = cur.fetchall()
            
            return [{
                'id_cuenta_cobrar': cta[0],
                'cuenta_numero': cta[1],
                'fecha_vencimiento': cta[2].strftime('%d/%m/%Y') if cta[2] else None,
                'monto_pendiente': cta[3],
                'paciente_nombre': cta[4],
                'factura_numero': cta[5],
                'dias_vencido': cta[6]
            } for cta in cuentas]
        except Exception as e:
            app.logger.error(f"Error al obtener cuentas vencidas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def actualizarEstadoCuenta(self, id_cuenta_cobrar):
        """Actualiza el estado de una cuenta a cobrar basado en montos y fecha"""
        # Primero actualizar montos pendientes
        sql_actualizar = """
            UPDATE cuentas_cobrar
            SET monto_pendiente = monto_total - monto_pagado
            WHERE id_cuenta_cobrar = %s
        """
        
        # Luego actualizar estado según montos y fecha
        sql_estado = """
            UPDATE cuentas_cobrar
            SET est_cuenta_cobrar = CASE
                WHEN monto_pagado = 0 AND fecha_vencimiento < CURRENT_DATE THEN 'VENCIDA'
                WHEN monto_pagado = 0 THEN 'PENDIENTE'
                WHEN monto_pagado >= monto_total THEN 'PAGADA'
                WHEN monto_pagado > 0 THEN 'PARCIAL'
                ELSE est_cuenta_cobrar
            END,
            fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_cuenta_cobrar = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql_actualizar, (id_cuenta_cobrar,))
            cur.execute(sql_estado, (id_cuenta_cobrar,))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al actualizar estado de cuenta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def registrarPago(self, id_cuenta_cobrar, monto_pago, usuario='ADMIN'):
        """Registra un pago parcial o total en una cuenta a cobrar"""
        sql = """
            UPDATE cuentas_cobrar
            SET monto_pagado = monto_pagado + %s,
                monto_pendiente = monto_total - (monto_pagado + %s),
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_cuenta_cobrar = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (monto_pago, monto_pago, usuario, id_cuenta_cobrar))
            con.commit()
            
            # Actualizar estado
            self.actualizarEstadoCuenta(id_cuenta_cobrar)
            
            return True
        except Exception as e:
            app.logger.error(f"Error al registrar pago: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def updateCuentaCobrar(self, id_cuenta_cobrar, fecha_vencimiento=None,
                           observaciones=None, numero_cuotas=None,
                           cuota_actual=None, usuario_modificacion='ADMIN'):
        """Actualiza una cuenta a cobrar existente"""
        
        campos = []
        valores = []
        
        if fecha_vencimiento:
            campos.append("fecha_vencimiento = %s")
            valores.append(fecha_vencimiento)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if numero_cuotas is not None:
            campos.append("numero_cuotas = %s")
            valores.append(numero_cuotas)
        if cuota_actual is not None:
            campos.append("cuota_actual = %s")
            valores.append(cuota_actual)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_cuenta_cobrar)
        
        updateSQL = f"""
            UPDATE cuentas_cobrar
            SET {', '.join(campos)}
            WHERE id_cuenta_cobrar = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            filas = cur.rowcount
            
            # Actualizar estado después de modificar
            self.actualizarEstadoCuenta(id_cuenta_cobrar)
            
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar cuenta a cobrar: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getHistorialCobranzas(self, id_cuenta_cobrar):
        """Obtiene el historial de cobranzas de una cuenta a cobrar"""
        sql = """
            SELECT
                c.id_cobranza,
                c.cobranza_numero,
                c.fecha_cobranza,
                c.monto_cobrado,
                fc.des_forma_cobro,
                c.observaciones,
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
                'observaciones': cob[5],
                'est_cobranza': cob[6]
            } for cob in cobranzas]
        except Exception as e:
            app.logger.error(f"Error al obtener historial de cobranzas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def actualizarEstadosVencidas(self):
        """Actualiza el estado de todas las cuentas vencidas"""
        sql = """
            UPDATE cuentas_cobrar
            SET est_cuenta_cobrar = 'VENCIDA',
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE fecha_vencimiento < CURRENT_DATE 
                AND est_cuenta_cobrar IN ('PENDIENTE', 'PARCIAL')
                AND monto_pendiente > 0
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            filas = cur.rowcount
            con.commit()
            return filas
        except Exception as e:
            app.logger.error(f"Error al actualizar estados vencidas: {str(e)}")
            con.rollback()
            return 0
        finally:
            cur.close()
            con.close()


















