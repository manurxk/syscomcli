from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import date

class TimbradoDao:

    # ============================
    # OBTENER
    # ============================

    def getTimbrados(self, id_empresa=None):
        """Obtiene todos los timbrados, opcionalmente filtrados por empresa"""
        if id_empresa:
            sql = """
            SELECT 
                t.id_timbrado, t.id_empresa, t.numero_timbrado,
                t.fecha_inicio, t.fecha_vencimiento, t.tipo_documento,
                t.tipo_generacion, t.estado, t.est_timbrado, e.razon_social
            FROM timbrados t
            JOIN empresa e ON t.id_empresa = e.id_empresa
            WHERE t.id_empresa = %s
            ORDER BY t.fecha_inicio DESC
            """
            params = (id_empresa,)
        else:
            sql = """
            SELECT 
                t.id_timbrado, t.id_empresa, t.numero_timbrado,
                t.fecha_inicio, t.fecha_vencimiento, t.tipo_documento,
                t.tipo_generacion, t.estado, t.est_timbrado, e.razon_social
            FROM timbrados t
            JOIN empresa e ON t.id_empresa = e.id_empresa
            ORDER BY e.razon_social, t.fecha_inicio DESC
            """
            params = None
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            timbrados = cur.fetchall()
            return [{
                'id': t[0],
                'id_empresa': t[1],
                'numero_timbrado': t[2],
                'fecha_inicio': t[3].isoformat() if t[3] else None,
                'fecha_vencimiento': t[4].isoformat() if t[4] else None,
                'tipo_documento': t[5],
                'tipo_generacion': t[6],
                'estado': t[7],
                'estado_activo': t[8],
                'empresa': t[9]
            } for t in timbrados]
        except Exception as e:
            app.logger.error(f"Error al obtener timbrados: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTimbradoById(self, id_timbrado):
        """Obtiene un timbrado por ID"""
        sql = """
        SELECT 
            id_timbrado, id_empresa, numero_timbrado,
            fecha_inicio, fecha_vencimiento, tipo_documento,
            tipo_generacion, estado, est_timbrado, observaciones
        FROM timbrados
        WHERE id_timbrado = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_timbrado,))
            t = cur.fetchone()
            if t:
                return {
                    'id': t[0],
                    'id_empresa': t[1],
                    'numero_timbrado': t[2],
                    'fecha_inicio': t[3].isoformat() if t[3] else None,
                    'fecha_vencimiento': t[4].isoformat() if t[4] else None,
                    'tipo_documento': t[5],
                    'tipo_generacion': t[6],
                    'estado': t[7],
                    'estado_activo': t[8],
                    'observaciones': t[9]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener timbrado: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getTimbradoVigente(self, id_empresa, tipo_documento='factura'):
        """Obtiene el timbrado vigente para una empresa y tipo de documento"""
        sql = """
        SELECT 
            id_timbrado, numero_timbrado, fecha_inicio, fecha_vencimiento
        FROM timbrados
        WHERE id_empresa = %s 
            AND tipo_documento = %s
            AND estado = 'activo'
            AND est_timbrado = TRUE
            AND fecha_inicio <= CURRENT_DATE
            AND fecha_vencimiento >= CURRENT_DATE
        ORDER BY fecha_vencimiento DESC
        LIMIT 1
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa, tipo_documento))
            t = cur.fetchone()
            if t:
                return {
                    'id': t[0],
                    'numero_timbrado': t[1],
                    'fecha_inicio': t[2].isoformat() if t[2] else None,
                    'fecha_vencimiento': t[3].isoformat() if t[3] else None
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener timbrado vigente: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getTimbradosVigentes(self, id_empresa):
        """Obtiene todos los timbrados vigentes de una empresa"""
        sql = """
        SELECT 
            id_timbrado, numero_timbrado, tipo_documento,
            fecha_inicio, fecha_vencimiento
        FROM timbrados
        WHERE id_empresa = %s 
            AND estado = 'activo'
            AND est_timbrado = TRUE
            AND fecha_inicio <= CURRENT_DATE
            AND fecha_vencimiento >= CURRENT_DATE
        ORDER BY tipo_documento, fecha_vencimiento DESC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa,))
            timbrados = cur.fetchall()
            return [{
                'id': t[0],
                'numero_timbrado': t[1],
                'tipo_documento': t[2],
                'fecha_inicio': t[3].isoformat() if t[3] else None,
                'fecha_vencimiento': t[4].isoformat() if t[4] else None
            } for t in timbrados]
        except Exception as e:
            app.logger.error(f"Error al obtener timbrados vigentes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def verificarTimbradoVigente(self, id_timbrado):
        """Verifica si un timbrado está vigente"""
        sql = """
        SELECT fecha_inicio, fecha_vencimiento, estado
        FROM timbrados
        WHERE id_timbrado = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_timbrado,))
            resultado = cur.fetchone()
            if resultado:
                fecha_inicio, fecha_vencimiento, estado = resultado
                hoy = date.today()
                return (estado == 'activo' and 
                        fecha_inicio and fecha_inicio <= hoy and 
                        fecha_vencimiento and fecha_vencimiento >= hoy)
            return False
        except Exception as e:
            app.logger.error(f"Error al verificar timbrado vigente: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def getTimbradosPorVencer(self, dias_antes=30):
        """Obtiene timbrados que vencen en los próximos N días"""
        sql = """
        SELECT 
            t.id_timbrado, t.numero_timbrado, t.fecha_vencimiento,
            e.razon_social, e.id_empresa
        FROM timbrados t
        JOIN empresa e ON t.id_empresa = e.id_empresa
        WHERE t.estado = 'activo'
            AND t.fecha_vencimiento BETWEEN CURRENT_DATE AND (CURRENT_DATE + INTERVAL '%s days')
        ORDER BY t.fecha_vencimiento ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (dias_antes,))
            timbrados = cur.fetchall()
            return [{
                'id': t[0],
                'numero_timbrado': t[1],
                'fecha_vencimiento': t[2].isoformat() if t[2] else None,
                'empresa': t[3],
                'id_empresa': t[4]
            } for t in timbrados]
        except Exception as e:
            app.logger.error(f"Error al obtener timbrados por vencer: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def timbradoExiste(self, numero_timbrado, id_empresa):
        """Verifica si ya existe un timbrado con el mismo número en la empresa"""
        sql = "SELECT 1 FROM timbrados WHERE numero_timbrado = %s AND id_empresa = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (numero_timbrado, id_empresa))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarFechasTimbrado(self, fecha_inicio, fecha_vencimiento):
        """Valida que la fecha de vencimiento sea mayor o igual a la de inicio"""
        if not fecha_inicio or not fecha_vencimiento:
            return False
        return fecha_vencimiento >= fecha_inicio

    # ============================
    # CRUD
    # ============================

    def guardarTimbrado(self, datos, usuario=1):
        """Guarda un nuevo timbrado"""
        if not datos.get('id_empresa') or not datos.get('numero_timbrado'):
            app.logger.warning("ID empresa y número de timbrado son obligatorios")
            return False
        
        if self.timbradoExiste(datos['numero_timbrado'], datos['id_empresa']):
            app.logger.warning("Ya existe un timbrado con este número en la empresa")
            return False
        
        if not self.validarFechasTimbrado(datos.get('fecha_inicio'), datos.get('fecha_vencimiento')):
            app.logger.warning("Fecha de vencimiento debe ser mayor o igual a fecha de inicio")
            return False

        sql = """
        INSERT INTO timbrados (
            id_empresa, numero_timbrado, fecha_inicio, fecha_vencimiento,
            tipo_documento, tipo_generacion, estado, est_timbrado,
            observaciones, creacion_usuario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_timbrado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('id_empresa'),
                datos.get('numero_timbrado'),
                datos.get('fecha_inicio'),
                datos.get('fecha_vencimiento'),
                datos.get('tipo_documento', 'factura'),
                datos.get('tipo_generacion', 'electronico'),
                datos.get('estado', 'activo'),
                datos.get('est_timbrado', True),
                datos.get('observaciones'),
                usuario
            ))
            id_timbrado = cur.fetchone()[0]
            con.commit()
            return id_timbrado
        except Exception as e:
            app.logger.error(f"Error al insertar timbrado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateTimbrado(self, id_timbrado, datos, usuario=1):
        """Actualiza los datos de un timbrado"""
        sql = """
        UPDATE timbrados
        SET 
            numero_timbrado = %s,
            fecha_inicio = %s,
            fecha_vencimiento = %s,
            tipo_documento = %s,
            tipo_generacion = %s,
            estado = %s,
            est_timbrado = %s,
            observaciones = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME,
            modificacion_usuario = %s
        WHERE id_timbrado = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('numero_timbrado'),
                datos.get('fecha_inicio'),
                datos.get('fecha_vencimiento'),
                datos.get('tipo_documento', 'factura'),
                datos.get('tipo_generacion', 'electronico'),
                datos.get('estado', 'activo'),
                datos.get('est_timbrado', True),
                datos.get('observaciones'),
                usuario,
                id_timbrado
            ))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar timbrado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTimbrado(self, id_timbrado):
        """
        Elimina un timbrado (solo si no tiene relaciones)
        Retorna True si se eliminó, False si no se pudo, "en_uso" si está en uso
        """
        # Verificar si tiene facturas asociadas
        sql_check = "SELECT COUNT(*) FROM facturas WHERE id_timbrado = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (id_timbrado,))
            if cur.fetchone()[0] > 0:
                return "en_uso"
            
            sql = "DELETE FROM timbrados WHERE id_timbrado = %s"
            cur.execute(sql, (id_timbrado,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar timbrado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
