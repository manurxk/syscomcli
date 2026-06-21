from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime

class InsumoDao:
    """DAO para gestionar insumos médicos con control de stock"""
    
    def getAllInsumos(self):
        """Obtiene todos los insumos activos"""
        insumoSQL = """
            SELECT
                i.id_insumo,
                i.des_insumo,
                i.insumo_unidad_medida,
                i.stock_actual,
                i.stock_minimo,
                i.insumo_precio_unitario,
                i.est_insumo,
                i.fecha_creacion,
                i.usuario_creacion,
                CASE 
                    WHEN i.stock_actual <= i.stock_minimo THEN 'BAJO'
                    WHEN i.stock_actual <= (i.stock_minimo * 1.5) THEN 'MEDIO'
                    ELSE 'NORMAL'
                END AS estado_stock
            FROM insumos i
            WHERE i.est_insumo = 'A'
            ORDER BY i.des_insumo ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insumoSQL)
            insumos = cur.fetchall()
            
            return [{
                'id_insumo': ins[0],
                'des_insumo': ins[1],
                'insumo_unidad_medida': ins[2],
                'insumo_stock_actual': ins[3],  # Mantener nombre en respuesta para compatibilidad
                'stock_actual': ins[3],
                'insumo_stock_minimo': ins[4],  # Mantener nombre en respuesta para compatibilidad
                'stock_minimo': ins[4],
                'insumo_precio_unitario': ins[5],
                'est_insumo': ins[6],
                'fecha_creacion': ins[7].strftime('%d/%m/%Y') if ins[7] else None,
                'usuario_creacion': ins[8],
                'estado_stock': ins[9]
            } for ins in insumos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los insumos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getInsumoById(self, id_insumo):
        """Obtiene un insumo específico por ID"""
        insumoSQL = """
            SELECT
                i.id_insumo,
                i.des_insumo,
                i.insumo_unidad_medida,
                i.stock_actual,
                i.stock_minimo,
                i.insumo_precio_unitario,
                i.est_insumo,
                i.fecha_creacion,
                i.usuario_creacion
            FROM insumos i
            WHERE i.id_insumo = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insumoSQL, (id_insumo,))
            ins = cur.fetchone()
            
            if not ins:
                return None
            
            return {
                'id_insumo': ins[0],
                'des_insumo': ins[1],
                'insumo_unidad_medida': ins[2],
                'insumo_stock_actual': ins[3],  # Mantener nombre en respuesta para compatibilidad
                'stock_actual': ins[3],
                'insumo_stock_minimo': ins[4],  # Mantener nombre en respuesta para compatibilidad
                'stock_minimo': ins[4],
                'insumo_precio_unitario': ins[5],
                'est_insumo': ins[6],
                'fecha_creacion': ins[7].strftime('%Y-%m-%d') if ins[7] else None,
                'usuario_creacion': ins[8]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener insumo por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def insumoExiste(self, descripcion, id_insumo=None):
        """Verifica si ya existe un insumo con el mismo nombre (case-insensitive)"""
        sql = """
            SELECT 1 FROM insumos 
            WHERE LOWER(des_insumo) = LOWER(%s)
        """
        params = [descripcion]
        
        if id_insumo:
            sql += " AND id_insumo != %s"
            params.append(id_insumo)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, tuple(params))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()
    
    def guardarInsumo(self, des_insumo, insumo_unidad_medida='UNIDAD',
                     insumo_stock_actual=0, insumo_stock_minimo=0,
                     insumo_precio_unitario=None, usuario_creacion='ADMIN'):
        """Guarda un nuevo insumo"""
        
        if not des_insumo or des_insumo.strip() == '':
            app.logger.error("La descripción del insumo es obligatoria")
            return None
        
        if self.insumoExiste(des_insumo):
            app.logger.warning(f"El insumo '{des_insumo}' ya existe")
            return None
        
        insertInsumoSQL = """
            INSERT INTO insumos(
                des_insumo, insumo_unidad_medida, stock_actual,
                stock_minimo, insumo_precio_unitario, est_insumo, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, 'A', %s)
            RETURNING id_insumo
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando insumo: {des_insumo}")
            
            cur.execute(insertInsumoSQL, (
                des_insumo.strip(),
                insumo_unidad_medida,
                insumo_stock_actual,
                insumo_stock_minimo,
                insumo_precio_unitario,
                usuario_creacion
            ))
            
            insumo_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Insumo guardado exitosamente con ID: {insumo_id}")
            return insumo_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar insumo: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def updateInsumo(self, id_insumo, des_insumo=None, insumo_unidad_medida=None,
                    insumo_stock_actual=None, insumo_stock_minimo=None,
                    insumo_precio_unitario=None, usuario_modificacion='ADMIN'):
        """Actualiza un insumo existente"""
        
        # Construir la consulta dinámicamente
        campos = []
        valores = []
        
        if des_insumo is not None:
            if self.insumoExiste(des_insumo, id_insumo):
                app.logger.warning(f"El insumo '{des_insumo}' ya existe")
                return False
            campos.append("des_insumo = %s")
            valores.append(des_insumo.strip())
        
        if insumo_unidad_medida is not None:
            campos.append("insumo_unidad_medida = %s")
            valores.append(insumo_unidad_medida)
        
        if insumo_stock_actual is not None:
            campos.append("stock_actual = %s")
            valores.append(insumo_stock_actual)
        
        if insumo_stock_minimo is not None:
            campos.append("stock_minimo = %s")
            valores.append(insumo_stock_minimo)
        
        if insumo_precio_unitario is not None:
            campos.append("insumo_precio_unitario = %s")
            valores.append(insumo_precio_unitario)
        
        if not campos:
            app.logger.warning("No hay campos para actualizar")
            return False
        
        valores.append(usuario_modificacion)
        valores.append(id_insumo)
        
        updateSQL = f"""
            UPDATE insumos
            SET {', '.join(campos)}, usuario_modificacion = %s
            WHERE id_insumo = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, tuple(valores))
            con.commit()
            app.logger.info(f"Insumo {id_insumo} actualizado exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar insumo: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def actualizarStock(self, id_insumo, cantidad, operacion='SUMAR'):
        """Actualiza el stock de un insumo (SUMAR o RESTAR)"""
        if operacion == 'SUMAR':
            updateSQL = """
                UPDATE insumos
                SET stock_actual = stock_actual + %s
                WHERE id_insumo = %s
            """
        else:  # RESTAR
            updateSQL = """
                UPDATE insumos
                SET stock_actual = GREATEST(0, stock_actual - %s)
                WHERE id_insumo = %s
            """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (cantidad, id_insumo))
            con.commit()
            return True
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar stock: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteInsumo(self, id_insumo):
        """Elimina lógicamente un insumo"""
        deleteSQL = """
            UPDATE insumos
            SET est_insumo = 'I'
            WHERE id_insumo = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_insumo,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar insumo: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def getInsumosBajoStock(self):
        """Obtiene insumos con stock bajo (stock actual <= stock mínimo)"""
        insumoSQL = """
            SELECT
                i.id_insumo,
                i.des_insumo,
                i.insumo_unidad_medida,
                i.stock_actual,
                i.stock_minimo,
                (i.stock_minimo - i.stock_actual) AS diferencia
            FROM insumos i
            WHERE i.est_insumo = 'A'
            AND i.stock_actual <= i.stock_minimo
            ORDER BY diferencia DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insumoSQL)
            insumos = cur.fetchall()
            
            return [{
                'id_insumo': ins[0],
                'des_insumo': ins[1],
                'insumo_unidad_medida': ins[2],
                'insumo_stock_actual': ins[3],  # Mantener nombre en respuesta para compatibilidad
                'stock_actual': ins[3],
                'insumo_stock_minimo': ins[4],  # Mantener nombre en respuesta para compatibilidad
                'stock_minimo': ins[4],
                'diferencia': ins[5]
            } for ins in insumos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener insumos bajo stock: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

