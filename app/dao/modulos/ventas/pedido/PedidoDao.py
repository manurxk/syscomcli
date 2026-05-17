from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class PedidoDao:
    """DAO para gestionar pedidos de clientes/pacientes"""
    
    def getPedidos(self):
        """Obtiene todos los pedidos con sus datos completos"""
        pedidoSQL = """
            SELECT
                p.id_pedido,
                p.pedido_numero,
                p.id_paciente,
                p.id_profesional,
                p.fecha_pedido,
                p.fecha_entrega,
                p.pedido_subtotal,
                p.pedido_descuento,
                p.pedido_total,
                p.observaciones,
                p.est_pedido,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional (si existe)
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                p.fecha_creacion
            FROM pedidos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            ORDER BY p.fecha_pedido DESC, p.id_pedido DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(pedidoSQL)
            pedidos = cur.fetchall()
            
            return [{
                'id_pedido': ped[0],
                'pedido_numero': ped[1],
                'id_paciente': ped[2],
                'id_profesional': ped[3],
                'fecha_pedido': ped[4].strftime('%d/%m/%Y') if ped[4] else None,
                'fecha_entrega': ped[5].strftime('%d/%m/%Y') if ped[5] else None,
                'pedido_subtotal': ped[6],
                'pedido_descuento': ped[7],
                'pedido_total': ped[8],
                'observaciones': ped[9],
                'est_pedido': ped[10],
                'historia_clinica': ped[11],
                'paciente_nombre': ped[12],
                'paciente_cedula': ped[13],
                'profesional_nombre': ped[14] if ped[14] else '',
                'fecha_registro': ped[15].strftime('%d/%m/%Y') if ped[15] else None
            } for ped in pedidos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los pedidos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getPedidoById(self, id_pedido):
        """Obtiene un pedido específico por ID con su detalle"""
        pedidoSQL = """
            SELECT
                p.id_pedido,
                p.pedido_numero,
                p.id_paciente,
                p.id_profesional,
                p.fecha_pedido,
                p.fecha_entrega,
                p.pedido_subtotal,
                p.pedido_descuento,
                p.pedido_total,
                p.observaciones,
                p.est_pedido,
                p.fecha_creacion,
                p.usuario_creacion,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre
            FROM pedidos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            LEFT JOIN funcionarios f ON p.id_profesional = f.id_funcionario
            LEFT JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.id_pedido = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(pedidoSQL, (id_pedido,))
            ped = cur.fetchone()
            
            if not ped:
                return None
            
            return {
                'id_pedido': ped[0],
                'pedido_numero': ped[1],
                'id_paciente': ped[2],
                'id_profesional': ped[3],
                'fecha_pedido': ped[4].strftime('%Y-%m-%d') if ped[4] else None,
                'fecha_entrega': ped[5].strftime('%Y-%m-%d') if ped[5] else None,
                'pedido_subtotal': ped[6],
                'pedido_descuento': ped[7],
                'pedido_total': ped[8],
                'observaciones': ped[9],
                'est_pedido': ped[10],
                'fecha_registro': ped[11].strftime('%Y-%m-%d') if ped[11] else None,
                'usuario_creacion': ped[12],
                'historia_clinica': ped[13],
                'paciente_nombre': ped[14],
                'paciente_cedula': ped[15],
                'paciente_telefono': ped[16],
                'profesional_nombre': ped[17] if ped[17] else ''
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener pedido por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getPedidoDetalle(self, id_pedido):
        """Obtiene el detalle completo de un pedido"""
        detalleSQL = """
            SELECT
                pd.id_pedido_detalle,
                pd.id_pedido,
                pd.id_tipo_item,
                pd.id_consulta,
                pd.item_descripcion,
                pd.item_cantidad,
                pd.item_precio_unitario,
                pd.item_descuento,
                pd.item_subtotal,
                pd.observaciones,
                ti.des_tipo_item
            FROM pedido_detalle pd
            LEFT JOIN tipos_items ti ON pd.id_tipo_item = ti.id_tipo_item
            WHERE pd.id_pedido = %s
            ORDER BY pd.id_pedido_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_pedido,))
            detalles = cur.fetchall()
            
            return [{
                'id_pedido_detalle': d[0],
                'id_pedido': d[1],
                'id_tipo_item': d[2],
                'id_consulta': d[3],
                'item_descripcion': d[4],
                'item_cantidad': d[5],
                'item_precio_unitario': d[6],
                'item_descuento': d[7],
                'item_subtotal': d[8],
                'observaciones': d[9],
                'tipo_item': d[10] if d[10] else ''
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle del pedido: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroPedido(self):
        """Genera un número único de pedido"""
        from datetime import datetime
        año = datetime.now().year
        mes = datetime.now().strftime('%m')
        
        # Buscar el último número del mes
        sql = """
            SELECT pedido_numero 
            FROM pedidos 
            WHERE pedido_numero LIKE %s
            ORDER BY pedido_numero DESC 
            LIMIT 1
        """
        patron = f'PED-{año}-{mes}-%'
        
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
            
            return f'PED-{año}-{mes}-{siguiente_num:04d}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de pedido: {str(e)}")
            return f'PED-{año}-{mes}-0001'
        finally:
            cur.close()
            con.close()
    
    def guardarPedido(self, id_paciente, fecha_pedido, fecha_entrega=None,
                     id_profesional=None, pedido_subtotal=0, pedido_descuento=0,
                     pedido_total=0, observaciones=None, est_pedido='PENDIENTE',
                     usuario_creacion='ADMIN'):
        """Guarda un nuevo pedido"""
        
        if not all([id_paciente, fecha_pedido]):
            app.logger.error("Faltan campos obligatorios para guardar pedido")
            return None
        
        # Generar número de pedido
        pedido_numero = self._generarNumeroPedido()
        
        insertPedidoSQL = """
            INSERT INTO pedidos(
                pedido_numero, id_paciente, id_profesional, fecha_pedido,
                fecha_entrega, pedido_subtotal, pedido_descuento, pedido_total,
                observaciones, est_pedido, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_pedido
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando pedido para paciente ID: {id_paciente}")
            
            cur.execute(insertPedidoSQL, (
                pedido_numero,
                id_paciente,
                id_profesional,
                fecha_pedido,
                fecha_entrega,
                pedido_subtotal,
                pedido_descuento,
                pedido_total,
                observaciones,
                est_pedido,
                usuario_creacion
            ))
            
            pedido_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Pedido guardado exitosamente con ID: {pedido_id}")
            return pedido_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar pedido: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarPedidoDetalle(self, id_pedido, item_descripcion, item_precio_unitario,
                            item_cantidad=1, item_descuento=0, id_tipo_item=None,
                            id_consulta=None, observaciones=None):
        """Guarda un item en el detalle de un pedido"""
        
        if not all([id_pedido, item_descripcion, item_precio_unitario]):
            app.logger.error("Faltan campos obligatorios para guardar detalle de pedido")
            return None
        
        item_subtotal = (item_precio_unitario * item_cantidad) - item_descuento
        
        insertDetalleSQL = """
            INSERT INTO pedido_detalle(
                id_pedido, id_tipo_item, id_consulta, item_descripcion,
                item_cantidad, item_precio_unitario, item_descuento, item_subtotal,
                observaciones
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_pedido_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_pedido,
                id_tipo_item,
                id_consulta,
                item_descripcion,
                item_cantidad,
                item_precio_unitario,
                item_descuento,
                item_subtotal,
                observaciones
            ))
            
            detalle_id = cur.fetchone()[0]
            
            # Actualizar totales del pedido
            self._actualizarTotalesPedido(id_pedido)
            
            con.commit()
            return detalle_id
            
        except Exception as e:
            app.logger.error(f"Error al guardar detalle de pedido: {str(e)}")
            con.rollback()
            return None
        finally:
            cur.close()
            con.close()
    
    def _actualizarTotalesPedido(self, id_pedido):
        """Actualiza los totales del pedido basado en su detalle"""
        sql = """
            UPDATE pedidos
            SET pedido_subtotal = (
                SELECT COALESCE(SUM(item_subtotal), 0)
                FROM pedido_detalle
                WHERE id_pedido = %s
            ),
            pedido_total = (
                SELECT COALESCE(SUM(item_subtotal), 0)
                FROM pedido_detalle
                WHERE id_pedido = %s
            ) - pedido_descuento
            WHERE id_pedido = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_pedido, id_pedido, id_pedido))
            con.commit()
        except Exception as e:
            app.logger.error(f"Error al actualizar totales del pedido: {str(e)}")
            con.rollback()
        finally:
            cur.close()
            con.close()
    
    def updatePedido(self, id_pedido, fecha_pedido=None, fecha_entrega=None,
                    id_profesional=None, pedido_descuento=None, observaciones=None,
                    est_pedido=None, usuario_modificacion='ADMIN'):
        """Actualiza un pedido existente"""
        
        campos = []
        valores = []
        
        if fecha_pedido:
            campos.append("fecha_pedido = %s")
            valores.append(fecha_pedido)
        if fecha_entrega is not None:
            campos.append("fecha_entrega = %s")
            valores.append(fecha_entrega)
        if id_profesional is not None:
            campos.append("id_profesional = %s")
            valores.append(id_profesional)
        if pedido_descuento is not None:
            campos.append("pedido_descuento = %s")
            valores.append(pedido_descuento)
            # Recalcular total
            self._actualizarTotalesPedido(id_pedido)
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        if est_pedido:
            campos.append("est_pedido = %s")
            valores.append(est_pedido)
        
        if not campos:
            return False
        
        campos.append("fecha_modificacion = CURRENT_TIMESTAMP")
        campos.append("usuario_modificacion = %s")
        valores.append(usuario_modificacion)
        valores.append(id_pedido)
        
        updateSQL = f"""
            UPDATE pedidos
            SET {', '.join(campos)}
            WHERE id_pedido = %s
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
            app.logger.error(f"Error al actualizar pedido: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def updatePedidoDetalle(self, id_pedido_detalle, item_descripcion=None,
                           item_cantidad=None, item_precio_unitario=None,
                           item_descuento=None, id_tipo_item=None,
                           id_consulta=None, observaciones=None):
        """Actualiza un item del detalle de pedido"""
        
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
        if observaciones is not None:
            campos.append("observaciones = %s")
            valores.append(observaciones)
        
        if not campos:
            return False
        
        # Recalcular subtotal
        campos.append("item_subtotal = (item_precio_unitario * item_cantidad) - item_descuento")
        valores.append(id_pedido_detalle)
        
        updateSQL = f"""
            UPDATE pedido_detalle
            SET {', '.join(campos)}
            WHERE id_pedido_detalle = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            
            # Obtener id_pedido para actualizar totales
            cur.execute("SELECT id_pedido FROM pedido_detalle WHERE id_pedido_detalle = %s", (id_pedido_detalle,))
            id_pedido = cur.fetchone()[0]
            self._actualizarTotalesPedido(id_pedido)
            
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al actualizar detalle de pedido: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def deletePedidoDetalle(self, id_pedido_detalle):
        """Elimina un item del detalle de pedido"""
        
        # Obtener id_pedido antes de eliminar
        sql_pedido = "SELECT id_pedido FROM pedido_detalle WHERE id_pedido_detalle = %s"
        deleteSQL = "DELETE FROM pedido_detalle WHERE id_pedido_detalle = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql_pedido, (id_pedido_detalle,))
            resultado = cur.fetchone()
            
            if not resultado:
                return False
            
            id_pedido = resultado[0]
            
            cur.execute(deleteSQL, (id_pedido_detalle,))
            filas = cur.rowcount
            
            # Actualizar totales del pedido
            self._actualizarTotalesPedido(id_pedido)
            
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar detalle de pedido: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def deletePedido(self, id_pedido):
        """Elimina un pedido y su detalle"""
        
        deleteDetalleSQL = "DELETE FROM pedido_detalle WHERE id_pedido = %s"
        deletePedidoSQL = "DELETE FROM pedidos WHERE id_pedido = %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Eliminar detalle primero
            cur.execute(deleteDetalleSQL, (id_pedido,))
            # Eliminar pedido
            cur.execute(deletePedidoSQL, (id_pedido,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar pedido: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getPedidosPorPaciente(self, id_paciente):
        """Obtiene todos los pedidos de un paciente"""
        sql = """
            SELECT
                p.id_pedido,
                p.pedido_numero,
                p.fecha_pedido,
                p.pedido_total,
                p.est_pedido
            FROM pedidos p
            WHERE p.id_paciente = %s
            ORDER BY p.fecha_pedido DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_paciente,))
            pedidos = cur.fetchall()
            
            return [{
                'id_pedido': ped[0],
                'pedido_numero': ped[1],
                'fecha_pedido': ped[2].strftime('%d/%m/%Y') if ped[2] else None,
                'pedido_total': ped[3],
                'est_pedido': ped[4]
            } for ped in pedidos]
        except Exception as e:
            app.logger.error(f"Error al obtener pedidos del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















