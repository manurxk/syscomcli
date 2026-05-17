from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date, timedelta

class FacturaDao:
    """DAO para gestionar facturas (facturación electrónica)"""
    
    def getFacturas(self):
        """Obtiene todas las facturas con sus datos completos"""
        facturaSQL = """
            SELECT
                f.id_factura,
                f.factura_numero,
                f.id_paciente,
                f.id_pedido,
                f.id_tipo_comprobante,
                f.id_condicion_venta,
                f.id_moneda,
                f.fecha_factura,
                f.fecha_vencimiento,
                f.factura_subtotal,
                f.factura_descuento,
                f.factura_impuestos,
                f.factura_total,
                f.codigo_sifen,
                f.numero_timbrado,
                f.observaciones,
                f.est_factura,
                f.fecha_creacion,
                f.id_empresa,
                f.id_timbrado,
                f.id_punto_expedicion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante,
                -- Datos de condición de venta
                cv.des_condicion_venta,
                -- Datos de estado de factura
                ef.des_estado_factura,
                -- Datos de moneda
                m.cod_moneda,
                -- Datos de empresa
                e.razon_social AS empresa_razon_social,
                e.ruc_nit AS empresa_ruc,
                -- Datos de timbrado
                t.numero_timbrado AS timbrado_numero,
                -- Datos de punto de expedición
                pe.nombre_punto_expedicion AS punto_expedicion_nombre
            FROM facturas f
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON f.id_tipo_comprobante = tc.id_tipo_comprobante
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            JOIN estados_factura ef ON f.est_factura = ef.id_estado_factura
            JOIN monedas m ON f.id_moneda = m.id_moneda
            LEFT JOIN empresa e ON f.id_empresa = e.id_empresa
            LEFT JOIN timbrados t ON f.id_timbrado = t.id_timbrado
            LEFT JOIN puntos_expedicion pe ON f.id_punto_expedicion = pe.id_punto_expedicion
            ORDER BY f.fecha_factura DESC, f.id_factura DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(facturaSQL)
            facturas = cur.fetchall()
            
            return [{
                'id_factura': fac[0],
                'factura_numero': fac[1],
                'id_paciente': fac[2],
                'id_pedido': fac[3],
                'id_tipo_comprobante': fac[4],
                'id_condicion_venta': fac[5],
                'id_moneda': fac[6],
                'fecha_factura': fac[7].strftime('%d/%m/%Y') if fac[7] else None,
                'fecha_vencimiento': fac[8].strftime('%d/%m/%Y') if fac[8] else None,
                'factura_subtotal': fac[9],
                'factura_descuento': fac[10],
                'factura_impuestos': fac[11],
                'factura_total': fac[12],
                'codigo_sifen': fac[13],
                'numero_timbrado': fac[14],
                'observaciones': fac[15],
                'est_factura': fac[16],
                'fecha_registro': fac[17].strftime('%d/%m/%Y') if fac[17] else None,
                'id_empresa': fac[18],
                'id_timbrado': fac[19],
                'id_punto_expedicion': fac[20],
                'historia_clinica': fac[21],
                'paciente_nombre': fac[22],
                'paciente_cedula': fac[23],
                'tipo_comprobante': fac[24],
                'condicion_venta': fac[25],
                'estado_factura': fac[26],
                'moneda': fac[27],
                'empresa_razon_social': fac[28],
                'empresa_ruc': fac[29],
                'timbrado_numero': fac[30],
                'punto_expedicion_nombre': fac[31]
            } for fac in facturas]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las facturas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getFacturaById(self, id_factura):
        """Obtiene una factura específica por ID con su detalle"""
        facturaSQL = """
            SELECT
                f.id_factura,
                f.factura_numero,
                f.id_paciente,
                f.id_pedido,
                f.id_tipo_comprobante,
                f.id_condicion_venta,
                f.id_moneda,
                f.fecha_factura,
                f.fecha_vencimiento,
                f.factura_subtotal,
                f.factura_descuento,
                f.factura_impuestos,
                f.factura_total,
                f.factura_total_letras,
                f.codigo_sifen,
                f.numero_timbrado,
                f.observaciones,
                f.est_factura,
                f.fecha_creacion,
                f.usuario_creacion,
                f.id_empresa,
                f.id_timbrado,
                f.id_punto_expedicion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                -- Datos del tipo de comprobante
                tc.des_tipo_comprobante,
                -- Datos de condición de venta
                cv.des_condicion_venta,
                cv.dias_credito,
                -- Datos de estado de factura
                ef.des_estado_factura,
                -- Datos de moneda
                m.cod_moneda,
                m.simbolo_moneda,
                -- Datos de empresa
                e.razon_social AS empresa_razon_social,
                e.ruc_nit AS empresa_ruc,
                -- Datos de timbrado
                t.numero_timbrado AS timbrado_numero,
                -- Datos de punto de expedición
                pe.nombre_punto_expedicion AS punto_expedicion_nombre
            FROM facturas f
            JOIN pacientes pac ON f.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN tipos_comprobantes tc ON f.id_tipo_comprobante = tc.id_tipo_comprobante
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            JOIN estados_factura ef ON f.est_factura = ef.id_estado_factura
            JOIN monedas m ON f.id_moneda = m.id_moneda
            LEFT JOIN empresa e ON f.id_empresa = e.id_empresa
            LEFT JOIN timbrados t ON f.id_timbrado = t.id_timbrado
            LEFT JOIN puntos_expedicion pe ON f.id_punto_expedicion = pe.id_punto_expedicion
            WHERE f.id_factura = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(facturaSQL, (id_factura,))
            fac = cur.fetchone()
            
            if not fac:
                return None
            
            return {
                'id_factura': fac[0],
                'factura_numero': fac[1],
                'id_paciente': fac[2],
                'id_pedido': fac[3],
                'id_tipo_comprobante': fac[4],
                'id_condicion_venta': fac[5],
                'id_moneda': fac[6],
                'fecha_factura': fac[7].strftime('%Y-%m-%d') if fac[7] else None,
                'fecha_vencimiento': fac[8].strftime('%Y-%m-%d') if fac[8] else None,
                'factura_subtotal': fac[9],
                'factura_descuento': fac[10],
                'factura_impuestos': fac[11],
                'factura_total': fac[12],
                'factura_total_letras': fac[13],
                'codigo_sifen': fac[14],
                'numero_timbrado': fac[15],
                'observaciones': fac[16],
                'est_factura': fac[17],
                'fecha_registro': fac[18].strftime('%Y-%m-%d') if fac[18] else None,
                'usuario_creacion': fac[19],
                'id_empresa': fac[20],
                'id_timbrado': fac[21],
                'id_punto_expedicion': fac[22],
                'historia_clinica': fac[23],
                'paciente_nombre': fac[24],
                'paciente_cedula': fac[25],
                'paciente_telefono': fac[26],
                'tipo_comprobante': fac[27],
                'condicion_venta': fac[28],
                'dias_credito': fac[29],
                'estado_factura': fac[30],
                'moneda': fac[31],
                'simbolo_moneda': fac[32],
                'empresa_razon_social': fac[33],
                'empresa_ruc': fac[34],
                'timbrado_numero': fac[35],
                'punto_expedicion_nombre': fac[36]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener factura por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getFacturaDetalle(self, id_factura):
        """Obtiene el detalle completo de una factura"""
        detalleSQL = """
            SELECT
                fd.id_factura_detalle,
                fd.id_factura,
                fd.id_tipo_item,
                fd.id_consulta,
                fd.item_descripcion,
                fd.item_cantidad,
                fd.item_precio_unitario,
                fd.item_descuento,
                fd.item_subtotal,
                fd.id_tipo_impuesto,
                fd.impuesto_porcentaje,
                fd.impuesto_monto,
                fd.item_total,
                ti.des_tipo_item,
                timp.des_tipo_impuesto
            FROM factura_detalle fd
            LEFT JOIN tipos_items ti ON fd.id_tipo_item = ti.id_tipo_item
            LEFT JOIN tipos_impuestos timp ON fd.id_tipo_impuesto = timp.id_tipo_impuesto
            WHERE fd.id_factura = %s
            ORDER BY fd.id_factura_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_factura,))
            detalles = cur.fetchall()
            
            return [{
                'id_factura_detalle': d[0],
                'id_factura': d[1],
                'id_tipo_item': d[2],
                'id_consulta': d[3],
                'item_descripcion': d[4],
                'item_cantidad': d[5],
                'item_precio_unitario': d[6],
                'item_descuento': d[7],
                'item_subtotal': d[8],
                'id_tipo_impuesto': d[9],
                'impuesto_porcentaje': float(d[10]) if d[10] else 0,
                'impuesto_monto': d[11],
                'item_total': d[12],
                'tipo_item': d[13] if d[13] else '',
                'tipo_impuesto': d[14] if d[14] else ''
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la factura: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroFactura(self, id_punto_expedicion=None, cur=None):
        """
        Genera un número único de factura usando el punto de expedición.
        Si no se proporciona id_punto_expedicion, usa el formato antiguo para retrocompatibilidad.
        Si se proporciona cur (cursor), usa esa conexión; si no, crea una nueva.
        """
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        if not id_punto_expedicion:
            # Formato antiguo para retrocompatibilidad
            if cur:
                # Usar cursor existente
                sql = """
                    SELECT factura_numero 
                    FROM facturas 
                    WHERE factura_numero LIKE %s
                    ORDER BY factura_numero DESC 
                    LIMIT 1
                """
                patron = f'FAC-{año}-{mes}-%'
                cur.execute(sql, (patron,))
                ultimo = cur.fetchone()
                
                if ultimo and ultimo[0]:
                    partes = ultimo[0].split('-')
                    if len(partes) == 4:
                        siguiente_num = int(partes[3]) + 1
                    else:
                        siguiente_num = 1
                else:
                    siguiente_num = 1
                
                return (f'FAC-{año}-{mes}-{siguiente_num:04d}', None)
            else:
                # Crear nueva conexión
                sql = """
                    SELECT factura_numero 
                    FROM facturas 
                    WHERE factura_numero LIKE %s
                    ORDER BY factura_numero DESC 
                    LIMIT 1
                """
                patron = f'FAC-{año}-{mes}-%'
                
                conexion = Conexion()
                con = conexion.getConexion()
                cur_temp = con.cursor()
                
                try:
                    cur_temp.execute(sql, (patron,))
                    ultimo = cur_temp.fetchone()
                    
                    if ultimo and ultimo[0]:
                        partes = ultimo[0].split('-')
                        if len(partes) == 4:
                            siguiente_num = int(partes[3]) + 1
                        else:
                            siguiente_num = 1
                    else:
                        siguiente_num = 1
                    
                    return (f'FAC-{año}-{mes}-{siguiente_num:04d}', None)
                    
                except Exception as e:
                    app.logger.error(f"Error al generar número de factura: {str(e)}")
                    return (f'FAC-{año}-{mes}-0001', None)
                finally:
                    cur_temp.close()
                    con.close()
        
        # Nuevo formato usando punto de expedición
        # Usar cursor existente si se proporciona, si no crear uno nuevo
        usar_cur_externo = (cur is not None)
        
        if not usar_cur_externo:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
        else:
            con = None  # No cerrar la conexión externa
        
        try:
            # Obtener datos del punto de expedición con bloqueo (FOR UPDATE)
            # para evitar condiciones de carrera
            sql = """
                SELECT 
                    pe.ultimo_numero_usado,
                    pe.codigo_punto_expedicion,
                    e.codigo_establecimiento
                FROM puntos_expedicion pe
                JOIN establecimientos e ON pe.id_establecimiento = e.id_establecimiento
                WHERE pe.id_punto_expedicion = %s
                FOR UPDATE
            """
            cur.execute(sql, (id_punto_expedicion,))
            punto_data = cur.fetchone()
            
            if not punto_data:
                app.logger.error(f"No se encontró punto de expedición con ID {id_punto_expedicion}")
                # Fallback al formato antiguo
                return (f'FAC-{año}-{mes}-0001', None)
            
            ultimo_numero = punto_data[0] or 0
            codigo_punto = punto_data[1]
            codigo_establecimiento = punto_data[2]
            
            # Incrementar número
            siguiente_num = ultimo_numero + 1
            
            # Actualizar último número usado en punto_expedicion
            update_sql = """
                UPDATE puntos_expedicion
                SET ultimo_numero_usado = %s
                WHERE id_punto_expedicion = %s
            """
            cur.execute(update_sql, (siguiente_num, id_punto_expedicion))
            
            # Retornar el número y el siguiente_numero para actualización posterior si es necesario
            # Formato: FAC-AÑO-MES-NUM (7 dígitos para número secuencial)
            numero_factura = f'FAC-{año}-{mes}-{siguiente_num:07d}'
            return (numero_factura, siguiente_num)
            
        except Exception as e:
            app.logger.error(f"Error al generar número de factura con punto de expedición: {str(e)}")
            if not usar_cur_externo and con:
                con.rollback()
            # Fallback al formato antiguo
            return (f'FAC-{año}-{mes}-0001', None)
        finally:
            if not usar_cur_externo:
                cur.close()
                con.close()
    
    def guardarFactura(self, id_paciente, id_tipo_comprobante, id_condicion_venta,
                      fecha_factura, id_moneda=1, id_pedido=None, fecha_vencimiento=None,
                      factura_subtotal=0, factura_descuento=0, factura_impuestos=0,
                      factura_total=0, codigo_sifen=None, numero_timbrado=None,
                      observaciones=None, est_factura=1, usuario_creacion='ADMIN',
                      id_empresa=None, id_timbrado=None, id_punto_expedicion=None):
        """Guarda una nueva factura"""
        
        if not all([id_paciente, id_tipo_comprobante, id_condicion_venta, fecha_factura]):
            app.logger.error("Faltan campos obligatorios para guardar factura")
            return None
        
        # Calcular fecha de vencimiento si es crédito
        if fecha_vencimiento is None:
            fecha_vencimiento = self._calcularFechaVencimiento(id_condicion_venta, fecha_factura)
        
        insertFacturaSQL = """
            INSERT INTO facturas(
                factura_numero, id_paciente, id_pedido, id_tipo_comprobante,
                id_condicion_venta, id_moneda, fecha_factura, fecha_vencimiento,
                factura_subtotal, factura_descuento, factura_impuestos, factura_total,
                codigo_sifen, numero_timbrado, observaciones, est_factura, usuario_creacion,
                id_empresa, id_timbrado, id_punto_expedicion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_factura
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Generar número de factura usando punto de expedición (dentro de la misma transacción)
            resultado = self._generarNumeroFactura(id_punto_expedicion, cur)
            if isinstance(resultado, tuple):
                factura_numero, siguiente_num = resultado
            else:
                # Retrocompatibilidad: si retorna solo string (formato antiguo)
                factura_numero = resultado
            
            app.logger.info(f"Insertando factura para paciente ID: {id_paciente}, número: {factura_numero}")
            
            cur.execute(insertFacturaSQL, (
                factura_numero,
                id_paciente,
                id_pedido,
                id_tipo_comprobante,
                id_condicion_venta,
                id_moneda,
                fecha_factura,
                fecha_vencimiento,
                factura_subtotal,
                factura_descuento,
                factura_impuestos,
                factura_total,
                codigo_sifen,
                numero_timbrado,
                observaciones,
                est_factura,
                usuario_creacion,
                id_empresa,
                id_timbrado,
                id_punto_expedicion
            ))
            
            factura_id = cur.fetchone()[0]
            
            # Generar cuenta a cobrar si es crédito
            self._generarCuentaCobrar(factura_id, id_paciente, factura_total, fecha_vencimiento)
            
            con.commit()
            
            app.logger.info(f"Factura guardada exitosamente con ID: {factura_id}")
            return factura_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar factura: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def _calcularFechaVencimiento(self, id_condicion_venta, fecha_factura):
        """Calcula la fecha de vencimiento basada en la condición de venta"""
        sql = "SELECT dias_credito FROM condiciones_venta WHERE id_condicion_venta = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_condicion_venta,))
            resultado = cur.fetchone()
            
            if resultado and resultado[0] and resultado[0] > 0:
                fecha_fac = datetime.strptime(fecha_factura, '%Y-%m-%d') if isinstance(fecha_factura, str) else fecha_factura
                fecha_venc = fecha_fac + timedelta(days=resultado[0])
                return fecha_venc.strftime('%Y-%m-%d') if isinstance(fecha_factura, str) else fecha_venc
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al calcular fecha de vencimiento: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def _generarCuentaCobrar(self, id_factura, id_paciente, monto_total, fecha_vencimiento):
        """Genera automáticamente una cuenta a cobrar si la factura es a crédito"""
        # Verificar si la condición de venta es crédito
        sql_condicion = """
            SELECT dias_credito 
            FROM facturas f
            JOIN condiciones_venta cv ON f.id_condicion_venta = cv.id_condicion_venta
            WHERE f.id_factura = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql_condicion, (id_factura,))
            resultado = cur.fetchone()
            
            # Si tiene días de crédito > 0, generar cuenta a cobrar
            if resultado and resultado[0] and resultado[0] > 0:
                # Generar número de cuenta
                año = datetime.now().year
                sql_numero = """
                    SELECT cuenta_numero 
                    FROM cuentas_cobrar 
                    WHERE cuenta_numero LIKE %s
                    ORDER BY cuenta_numero DESC 
                    LIMIT 1
                """
                patron = f'CTA-{año}-%'
                cur.execute(sql_numero, (patron,))
                ultimo = cur.fetchone()
                
                if ultimo and ultimo[0]:
                    partes = ultimo[0].split('-')
                    siguiente_num = int(partes[2]) + 1 if len(partes) > 2 else 1
                else:
                    siguiente_num = 1
                
                cuenta_numero = f'CTA-{año}-{siguiente_num:04d}'
                
                # Insertar cuenta a cobrar
                insertCuentaSQL = """
                    INSERT INTO cuentas_cobrar(
                        id_factura, id_paciente, cuenta_numero, fecha_emision,
                        fecha_vencimiento, monto_total, monto_pagado, monto_pendiente,
                        estado_cuenta_cobrar
                    )
                    VALUES(%s, %s, %s, CURRENT_TIMESTAMP, %s, %s, 0, %s, 'PENDIENTE')
                """
                
                cur.execute(insertCuentaSQL, (
                    id_factura,
                    id_paciente,
                    cuenta_numero,
                    fecha_vencimiento,
                    monto_total,
                    monto_total
                ))
                
                app.logger.info(f"Cuenta a cobrar generada: {cuenta_numero}")
        except Exception as e:
            app.logger.error(f"Error al generar cuenta a cobrar: {str(e)}")
            # No hacer rollback aquí, solo loguear el error
        finally:
            cur.close()
            con.close()
    
    def guardarFacturaDetalle(self, id_factura, item_descripcion, item_precio_unitario,
                             item_cantidad=1, item_descuento=0, id_tipo_item=None,
                             id_consulta=None, id_tipo_impuesto=None, impuesto_porcentaje=0,
                             observaciones=None):
        """Guarda un item en el detalle de una factura"""
        
        if not all([id_factura, item_descripcion, item_precio_unitario]):
            app.logger.error("Faltan campos obligatorios para guardar detalle de factura")
            return None
        
        # Calcular subtotal e impuesto
        item_subtotal = (item_precio_unitario * item_cantidad) - item_descuento
        impuesto_monto = int(item_subtotal * (impuesto_porcentaje / 100)) if impuesto_porcentaje > 0 else 0
        item_total = item_subtotal + impuesto_monto
        
        insertDetalleSQL = """
            INSERT INTO factura_detalle(
                id_factura, id_tipo_item, id_consulta, item_descripcion,
                item_cantidad, item_precio_unitario, item_descuento, item_subtotal,
                id_tipo_impuesto, impuesto_porcentaje, impuesto_monto, item_total
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_factura_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_factura,
                id_tipo_item,
                id_consulta,
                item_descripcion,
                item_cantidad,
                item_precio_unitario,
                item_descuento,
                item_subtotal,
                id_tipo_impuesto,
                impuesto_porcentaje,
                impuesto_monto,
                item_total
            ))
            
            detalle_id = cur.fetchone()[0]
            
            # Actualizar totales de la factura
            self._actualizarTotalesFactura(id_factura)
            
            con.commit()
            return detalle_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar detalle de factura: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def _actualizarTotalesFactura(self, id_factura):
        """Actualiza los totales de la factura basado en su detalle"""
        sql = """
            UPDATE facturas
            SET factura_subtotal = (
                SELECT COALESCE(SUM(item_subtotal), 0)
                FROM factura_detalle
                WHERE id_factura = %s
            ),
            factura_impuestos = (
                SELECT COALESCE(SUM(impuesto_monto), 0)
                FROM factura_detalle
                WHERE id_factura = %s
            ),
            factura_total = (
                SELECT COALESCE(SUM(item_total), 0)
                FROM factura_detalle
                WHERE id_factura = %s
            ) - COALESCE(factura_descuento, 0)
            WHERE id_factura = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_factura, id_factura, id_factura, id_factura))
            con.commit()
            
            # Actualizar cuenta a cobrar si existe
            self._actualizarCuentaCobrar(id_factura)
        except Exception as e:
            app.logger.error(f"Error al actualizar totales de la factura: {str(e)}")
            con.rollback()
        finally:
            cur.close()
            con.close()
    
    def _actualizarCuentaCobrar(self, id_factura):
        """Actualiza el monto de la cuenta a cobrar asociada"""
        sql = """
            UPDATE cuentas_cobrar
            SET monto_total = (
                SELECT factura_total FROM facturas WHERE id_factura = %s
            ),
            monto_pendiente = (
                SELECT factura_total FROM facturas WHERE id_factura = %s
            ) - monto_pagado
            WHERE id_factura = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_factura, id_factura, id_factura))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al actualizar cuenta a cobrar: {str(e)}")
            # No hacer rollback aquí
        finally:
            cur.close()
            con.close()
    
    def updateFactura(self, id_factura, fecha_factura=None, fecha_vencimiento=None,
                     factura_descuento=None, codigo_sifen=None, numero_timbrado=None,
                     observaciones=None, est_factura=None, usuario_modificacion='ADMIN'):
        """Actualiza una factura existente"""
        
        campos = []
        valores = []
        
        if fecha_factura:
            campos.append("fecha_factura = %s")
            valores.append(fecha_factura)
        if fecha_vencimiento is not None:
            campos.append("fecha_vencimiento = %s")
            valores.append(fecha_vencimiento)
        if factura_descuento is not None:
            campos.append("factura_descuento = %s")
            valores.append(factura_descuento)
            # Recalcular total
            self._actualizarTotalesFactura(id_factura)
        if codigo_sifen is not None:
            campos.append("codigo_sifen = %s")
            valores.append(codigo_sifen)
        if numero_timbrado is not None:
            campos.append("numero_timbrado = %s")
            valores.append(numero_timbrado)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_factura:
            campos.append("est_factura = %s")
            valores.append(est_factura)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_factura)
        
        updateSQL = f"""
            UPDATE facturas
            SET {', '.join(campos)}
            WHERE id_factura = %s
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
            app.logger.error(f"Error al actualizar factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def updateFacturaDetalle(self, id_factura_detalle, item_descripcion=None,
                            item_cantidad=None, item_precio_unitario=None,
                            item_descuento=None, id_tipo_item=None,
                            id_consulta=None, id_tipo_impuesto=None,
                            impuesto_porcentaje=None):
        """Actualiza un item del detalle de factura"""
        
        campos = []
        valores = []
        
        if item_descripcion:
            campos.append("item_descripcion = %s")
            valores.append(item_descripcion)
        if item_cantidad is not None:
            campos.append("item_cantidad = %s")
            valores.append(item_cantidad)
        if item_precio_unitario is not None:
            campos.append("item_precio_unitario = %s")
            valores.append(item_precio_unitario)
        if item_descuento is not None:
            campos.append("item_descuento = %s")
            valores.append(item_descuento)
        if id_tipo_item is not None:
            campos.append("id_tipo_item = %s")
            valores.append(id_tipo_item)
        if id_consulta is not None:
            campos.append("id_consulta = %s")
            valores.append(id_consulta)
        if id_tipo_impuesto is not None:
            campos.append("id_tipo_impuesto = %s")
            valores.append(id_tipo_impuesto)
        if impuesto_porcentaje is not None:
            campos.append("impuesto_porcentaje = %s")
            valores.append(impuesto_porcentaje)
        
        if not campos:
            return False
        
        # Recalcular subtotal e impuesto
        campos.append("item_subtotal = (item_precio_unitario * item_cantidad) - item_descuento")
        campos.append("impuesto_monto = (item_subtotal * impuesto_porcentaje / 100)")
        campos.append("item_total = item_subtotal + impuesto_monto")
        valores.append(id_factura_detalle)
        
        updateSQL = f"""
            UPDATE factura_detalle
            SET {', '.join(campos)}
            WHERE id_factura_detalle = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            
            # Obtener id_factura para actualizar totales
            cur.execute("SELECT id_factura FROM factura_detalle WHERE id_factura_detalle = %s", (id_factura_detalle,))
            id_factura = cur.fetchone()[0]
            self._actualizarTotalesFactura(id_factura)
            
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al actualizar detalle de factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteFacturaDetalle(self, id_factura_detalle):
        """Elimina un item del detalle de factura"""
        
        # Obtener id_factura antes de eliminar
        sql_factura = "SELECT id_factura FROM factura_detalle WHERE id_factura_detalle = %s"
        deleteSQL = "DELETE FROM factura_detalle WHERE id_factura_detalle = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql_factura, (id_factura_detalle,))
            resultado = cur.fetchone()
            
            if not resultado:
                return False
            
            id_factura = resultado[0]
            
            cur.execute(deleteSQL, (id_factura_detalle,))
            filas = cur.rowcount
            
            # Actualizar totales de la factura
            self._actualizarTotalesFactura(id_factura)
            
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar detalle de factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteFactura(self, id_factura):
        """Elimina una factura y su detalle"""
        
        deleteDetalleSQL = "DELETE FROM factura_detalle WHERE id_factura = %s"
        deleteCuentaSQL = "DELETE FROM cuentas_cobrar WHERE id_factura = %s"
        deleteFacturaSQL = "DELETE FROM facturas WHERE id_factura = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Eliminar detalle primero
            cur.execute(deleteDetalleSQL, (id_factura,))
            # Eliminar cuenta a cobrar si existe
            cur.execute(deleteCuentaSQL, (id_factura,))
            # Eliminar factura
            cur.execute(deleteFacturaSQL, (id_factura,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getFacturasPorPaciente(self, id_paciente):
        """Obtiene todas las facturas de un paciente"""
        sql = """
            SELECT
                f.id_factura,
                f.factura_numero,
                f.fecha_factura,
                f.factura_total,
                ef.des_estado_factura
            FROM facturas f
            JOIN estados_factura ef ON f.est_factura = ef.id_estado_factura
            WHERE f.id_paciente = %s
            ORDER BY f.fecha_factura DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_paciente,))
            facturas = cur.fetchall()
            
            return [{
                'id_factura': fac[0],
                'factura_numero': fac[1],
                'fecha_factura': fac[2].strftime('%d/%m/%Y') if fac[2] else None,
                'factura_total': fac[3],
                'estado_factura': fac[4]
            } for fac in facturas]
        except Exception as e:
            app.logger.error(f"Error al obtener facturas del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
