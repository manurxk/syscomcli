from flask import current_app as app
from app.dao.modulos.ventas.libro_ventas.LibroVentasDao import LibroVentasDao
from app.conexion.Conexion import Conexion
from datetime import datetime, date, timedelta
from decimal import Decimal, ROUND_HALF_UP


def numero_a_letras(monto) -> str:
    """Convierte un monto numérico (int o Decimal) a su representación en letras en español paraguayo.
    Rango soportado: 0 a 999.999.999
    Ejemplo: 950000 -> 'Novecientos cincuenta mil Guaraníes'
    """
    UNIDADES = [
        '', 'un', 'dos', 'tres', 'cuatro', 'cinco',
        'seis', 'siete', 'ocho', 'nueve', 'diez',
        'once', 'doce', 'trece', 'catorce', 'quince',
        'dieciséis', 'diecisiete', 'dieciocho', 'diecinueve',
        'veinte', 'veintiún', 'veintidós', 'veintitrés', 'veinticuatro',
        'veinticinco', 'veintiséis', 'veintisiete', 'veintiocho', 'veintinueve'
    ]
    DECENAS = [
        '', '', 'veinte', 'treinta', 'cuarenta', 'cincuenta',
        'sesenta', 'setenta', 'ochenta', 'noventa'
    ]
    CENTENAS = [
        '', 'cien', 'doscientos', 'trescientos', 'cuatrocientos', 'quinientos',
        'seiscientos', 'setecientos', 'ochocientos', 'novecientos'
    ]

    def _cientos(n: int) -> str:
        if n == 0:
            return ''
        c = n // 100
        resto = n % 100
        texto_c = ''
        if c > 0:
            if c == 1 and resto > 0:
                texto_c = 'ciento'
            elif c == 1:
                texto_c = 'cien'
            else:
                texto_c = CENTENAS[c]
        texto_r = ''
        if 1 <= resto <= 29:
            texto_r = UNIDADES[resto]
            if resto == 21:
                texto_r = 'veintiún'
        elif resto >= 30:
            d = resto // 10
            u = resto % 10
            texto_r = DECENAS[d]
            if u > 0:
                texto_r += ' y ' + UNIDADES[u]
        partes = [p for p in [texto_c, texto_r] if p]
        return ' '.join(partes)

    monto_int = int(Decimal(str(monto)).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    if monto_int == 0:
        return 'Cero Guaraníes'
    if monto_int < 0 or monto_int > 999_999_999:
        raise ValueError(f'Monto fuera de rango para numero_a_letras: {monto_int}')

    millones = monto_int // 1_000_000
    miles = (monto_int % 1_000_000) // 1_000
    resto = monto_int % 1_000

    partes = []
    if millones > 0:
        if millones == 1:
            partes.append('un millón')
        else:
            partes.append(_cientos(millones) + ' millones')
    if miles > 0:
        if miles == 1:
            partes.append('mil')
        else:
            partes.append(_cientos(miles) + ' mil')
    if resto > 0:
        partes.append(_cientos(resto))

    texto = ' '.join(partes)
    # Sentence case: Primera letra en mayúscula
    texto = texto[0].upper() + texto[1:] if texto else ''
    
    # Pluralidad del Guaraní
    moneda = 'Guaraní' if monto_int == 1 else 'Guaraníes'
    return f'{texto} {moneda}'



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
                pe.nombre_punto_expedicion AS punto_expedicion_nombre,
                -- Presupuesto de origen (Fase 1)
                f.id_presupuesto
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
                'punto_expedicion_nombre': fac[36],
                'id_presupuesto': fac[37]  # FK de trazabilidad presupuesto (Fase 1)
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
                fd.item_precio_con_iva,
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
                'item_precio_unitario': d[6],         # base sin IVA (campo fiscal)
                'item_precio_con_iva': d[7] if d[7] else d[6],  # precio c/IVA para pantalla (P4)
                'item_descuento': d[8],
                'item_subtotal': d[9],
                'id_tipo_impuesto': d[10],
                'impuesto_porcentaje': float(d[11]) if d[11] else 0,
                'impuesto_monto': d[12],
                'item_total': d[13],
                'tipo_item': d[14] if d[14] else '',
                'tipo_impuesto': d[15] if d[15] else ''
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle de la factura {id_factura}: {str(e)}")
            import traceback
            app.logger.error(traceback.format_exc())
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
                      id_empresa=None, id_timbrado=None, id_punto_expedicion=None,
                      id_presupuesto=None):
        """Guarda una nueva factura.
        
        Args:
            id_presupuesto: FK opcional al presupuesto de origen. Permite
                trazabilidad directa presupuesto -> factura (Fase 1).
        """
        
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
                factura_total_letras,
                codigo_sifen, numero_timbrado, observaciones, est_factura, usuario_creacion,
                id_empresa, id_timbrado, id_punto_expedicion,
                factura_cdc, factura_estado_sifen, factura_xml_generado, factura_timbrado_id,
                id_presupuesto
            )
            VALUES(
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s
            )
            RETURNING id_factura
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Obtener configuración de emisión SIFEN (Valida timbrado vigente automáticamente)
            from app.services.sifen_config_service import SifenConfigService, SifenConfigException
            from app.utils.sifen_cdc_utils import SifenCDCUtils

            try:
                config_emis = SifenConfigService.get_config_emision(id_empresa=id_empresa, id_punto_expedicion=id_punto_expedicion)
                
                # Asegurar valores desde la config oficial
                numero_timbrado = config_emis.timbrado_numero
                id_punto_expedicion = config_emis.id_punto_expedicion
                id_timbrado_real = config_emis.timbrado_numero # No tenemos el ID del timbrado explicitamente, usar name o buscar
                
                factura_numero = f"{config_emis.establecimiento_codigo}-{config_emis.punto_expedicion_codigo}-{str(config_emis.siguiente_numero).zfill(7)}"
                
                # Actualizar el último número usado
                cur.execute("UPDATE puntos_expedicion SET ultimo_numero_usado = %s WHERE id_punto_expedicion = %s", 
                            (config_emis.siguiente_numero, id_punto_expedicion))
                
                # Generar CDC Real
                if not codigo_sifen:
                    codigo_sifen = SifenCDCUtils.generar_cdc_real(
                        tipo_documento="01", # Factura
                        ruc_emisor=config_emis.ruc_emisor,
                        dv_ruc_emisor=config_emis.digito_verificador,
                        establecimiento=config_emis.establecimiento_codigo,
                        punto_expedicion=config_emis.punto_expedicion_codigo,
                        numero_documento=str(config_emis.siguiente_numero),
                        tipo_contribuyente="2" if config_emis.ruc_emisor.startswith("8") else "1",
                        fecha_emision_yyyymmdd=fecha_factura.replace("-", "")[:8] if isinstance(fecha_factura, str) else fecha_factura.strftime("%Y%m%d")
                    )
            
            except SifenConfigException as e:
                # Todo: SIFEN_REAL: Bloquear si no hay timbrado activo.
                app.logger.warning(f"Advertencia SIFEN (Puede fallar en PRODUCCION): {str(e)}")
                # Fallback al sistema anterior temporalmente si la BD no está bien configurada
                resultado = self._generarNumeroFactura(id_punto_expedicion, cur)
                if isinstance(resultado, tuple):
                    factura_numero, _ = resultado
                else:
                    factura_numero = resultado

            app.logger.info(f"Insertando factura para paciente ID: {id_paciente}, número: {factura_numero}")

            # Generar texto del total en letras (P1)
            try:
                total_letras = numero_a_letras(factura_total)
            except Exception:
                total_letras = None

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
                total_letras,           # factura_total_letras
                codigo_sifen,
                numero_timbrado,
                observaciones,
                est_factura,
                usuario_creacion,
                id_empresa,
                id_timbrado,
                id_punto_expedicion,
                codigo_sifen,           # factura_cdc
                'PENDIENTE',            # factura_estado_sifen
                None,                   # factura_xml_generado
                id_timbrado,            # factura_timbrado_id
                id_presupuesto          # FK de trazabilidad (Fase 1)
            ))
            
            factura_id = cur.fetchone()[0]
            # Register entry in libro_ventas for reporting
            try:
                libro_dao = LibroVentasDao()
                libro_dao.registrarEntradaLibroVentas(
                    libro_fecha=fecha_factura,
                    tipo_comprobante='FACTURA',
                    numero_comprobante=factura_numero,
                    id_paciente=id_paciente,
                    monto_gravado=factura_subtotal,
                    monto_exento=0,
                    monto_iva=factura_impuestos,
                    monto_total=factura_total,
                    id_factura=factura_id
                )
            except Exception as e:
                app.logger.error(f"Error al registrar entrada en libro de ventas para factura {factura_id}: {str(e)}")
            
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
        
        # Calcular descomposición de IVA (El precio unitario ingresado ya contiene IVA)
        precio_con_iva_orig = Decimal(str(item_precio_unitario))  # precio que el usuario ingresó (con IVA)
        cantidad = Decimal(str(item_cantidad))
        descuento = Decimal(str(item_descuento))
        tasa = Decimal(str(impuesto_porcentaje))
        
        # El total de la operación es lo que el cliente paga
        item_total_dec = (precio_con_iva_orig * cantidad) - descuento
        
        # Extraer base e IVA: base = total / (1 + tasa/100)
        divisor = Decimal('1') + (tasa / Decimal('100'))
        item_subtotal_dec = (item_total_dec / divisor).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
        impuesto_monto_dec = item_total_dec - item_subtotal_dec
        
        # Precio unitario base (sin IVA) — se guarda en item_precio_unitario para la lógica fiscal
        item_precio_unitario_base = (item_subtotal_dec / cantidad).quantize(Decimal('1'), rounding=ROUND_HALF_UP) if cantidad > 0 else Decimal('0')
        
        item_subtotal = int(item_subtotal_dec)
        impuesto_monto = int(impuesto_monto_dec)
        item_total = int(item_total_dec)
        item_precio_unitario_final = int(item_precio_unitario_base)  # base sin IVA (campo fiscal)
        item_precio_con_iva_int = int(precio_con_iva_orig)           # precio original c/IVA (P4: para pantalla/PDF)
        
        insertDetalleSQL = """
            INSERT INTO factura_detalle(
                id_factura, id_tipo_item, id_consulta, item_descripcion,
                item_cantidad, item_precio_unitario, item_precio_con_iva, item_descuento, item_subtotal,
                id_tipo_impuesto, impuesto_porcentaje, impuesto_monto, item_total
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                item_precio_unitario_final,    # base sin IVA
                item_precio_con_iva_int,        # precio original c/IVA (P4)
                item_descuento,
                item_subtotal,
                id_tipo_impuesto,
                impuesto_porcentaje,
                impuesto_monto,
                item_total
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            
            # Actualizar totales de la factura (en nueva transacción)
            self._actualizarTotalesFactura(id_factura)
            
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

            # Actualizar factura_total_letras (P1) después del commit de totales
            try:
                cur.execute("SELECT factura_total FROM facturas WHERE id_factura = %s", (id_factura,))
                row = cur.fetchone()
                if row and row[0] is not None:
                    letras = numero_a_letras(row[0])
                    cur.execute("UPDATE facturas SET factura_total_letras = %s WHERE id_factura = %s", (letras, id_factura))
                    con.commit()
            except Exception as e_letras:
                app.logger.warning(f"No se pudo actualizar factura_total_letras: {str(e_letras)}")

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
        """Actualiza un item del detalle de factura con descompocisión de IVA"""
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # 1. Obtener datos actuales para el cálculo
            cur.execute("""
                SELECT item_cantidad, item_precio_unitario, item_descuento, impuesto_porcentaje, item_total
                FROM factura_detalle WHERE id_factura_detalle = %s
            """, (id_factura_detalle,))
            actual = cur.fetchone()
            if not actual:
                return False
                
            # 2. Determinar valores finales (nuevos o actuales)
            c_cant = item_cantidad if item_cantidad is not None else actual[0]
            desc = item_descuento if item_descuento is not None else actual[2]
            tasa = impuesto_porcentaje if impuesto_porcentaje is not None else actual[3]
            
            # Si recibimos un precio nuevo, viene CON IVA. 
            # Si no recibimos, el que está en la base YA ES BASE (según nueva lógica).
            if item_precio_unitario is not None:
                p_con_iva = item_precio_unitario
            else:
                # Recalcular p_con_iva original para mantener el total si no se cambió el precio
                p_con_iva = (int(actual[4]) + int(actual[2])) / int(actual[0]) if actual[0] > 0 else 0
            
            # 3. Calcular descompocisión de IVA en Python para precisión
            from decimal import Decimal, ROUND_HALF_UP
            d_p = Decimal(str(p_con_iva))
            d_c = Decimal(str(c_cant))
            d_d = Decimal(str(desc))
            d_t = Decimal(str(tasa))
            
            total_ope = (d_p * d_c) - d_d
            divisor = Decimal('1') + (d_t / Decimal('100'))
            base_total = (total_ope / divisor).quantize(Decimal('1'), rounding=ROUND_HALF_UP)
            iva_monto = total_ope - base_total
            precio_unit_base = (base_total / d_c).quantize(Decimal('1'), rounding=ROUND_HALF_UP) if d_c > 0 else Decimal('0')
            
            # 4. Construir el Update
            campos = []
            valores = []
            
            if item_descripcion is not None:
                campos.append("item_descripcion = %s")
                valores.append(item_descripcion)
            
            # Siempre actualizamos los campos de cálculo para mantener consistencia
            campos.append("item_cantidad = %s")
            valores.append(int(c_cant))
            campos.append("item_precio_unitario = %s")
            valores.append(int(precio_unit_base))
            campos.append("item_descuento = %s")
            valores.append(int(desc))
            campos.append("impuesto_porcentaje = %s")
            valores.append(int(tasa))
            campos.append("item_subtotal = %s")
            valores.append(int(base_total))
            campos.append("impuesto_monto = %s")
            valores.append(int(iva_monto))
            campos.append("item_total = %s")
            valores.append(int(total_ope))
            
            if id_tipo_item is not None:
                campos.append("id_tipo_item = %s")
                valores.append(id_tipo_item)
            if id_consulta is not None:
                campos.append("id_consulta = %s")
                valores.append(id_consulta)
            if id_tipo_impuesto is not None:
                campos.append("id_tipo_impuesto = %s")
                valores.append(id_tipo_impuesto)
            
            valores.append(id_factura_detalle)
            
            updateSQL = f"UPDATE factura_detalle SET {', '.join(campos)} WHERE id_factura_detalle = %s"
            cur.execute(updateSQL, tuple(valores))
            con.commit()
            
            # 5. Obtener id_factura para actualizar totales de la cabecera
            cur.execute("SELECT id_factura FROM factura_detalle WHERE id_factura_detalle = %s", (id_factura_detalle,))
            res_fac = cur.fetchone()
            if res_fac:
                self._actualizarTotalesFactura(res_fac[0])
            
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
