# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoItemDao:

    def getTiposItems(self):
        sql = """
        SELECT id_tipo_item, des_tipo_item, cod_tipo_item, tipo_item_categoria, 
               requiere_stock, est_tipo_item
        FROM tipos_items
        ORDER BY des_tipo_item ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            tipos = cur.fetchall()
            return [{
                'id': t[0], 
                'descripcion': t[1], 
                'codigo': t[2] or '',
                'categoria': t[3] or '',
                'requiere_stock': t[4],
                'estado': t[5]
            } for t in tipos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de items: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTipoItemById(self, id_tipo_item):
        sql = """
        SELECT id_tipo_item, des_tipo_item, cod_tipo_item, tipo_item_categoria, 
               requiere_stock, est_tipo_item
        FROM tipos_items
        WHERE id_tipo_item=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_item,))
            tipo = cur.fetchone()
            if tipo:
                return {
                    "id": tipo[0], 
                    "descripcion": tipo[1], 
                    "codigo": tipo[2] or '',
                    "categoria": tipo[3] or '',
                    "requiere_stock": tipo[4],
                    "estado": tipo[5]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de item: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def tipoItemExiste(self, descripcion):
        sql = "SELECT 1 FROM tipos_items WHERE LOWER(des_tipo_item)=LOWER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarDescripcion(self, descripcion):
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def guardarTipoItem(self, descripcion, codigo=None, categoria=None, requiere_stock=False, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.tipoItemExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO tipos_items(des_tipo_item, cod_tipo_item, tipo_item_categoria, 
                              requiere_stock, est_tipo_item, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING id_tipo_item
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            categoria.upper() if categoria else None, requiere_stock, estado, usuario))
            id_tipo_item = cur.fetchone()[0]
            con.commit()
            return id_tipo_item
        except Exception as e:
            app.logger.error(f"Error al insertar tipo de item: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateTipoItem(self, id_tipo_item, descripcion, codigo=None, categoria=None, requiere_stock=False, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE tipos_items
        SET des_tipo_item=%s, cod_tipo_item=%s, tipo_item_categoria=%s, 
            requiere_stock=%s, est_tipo_item=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_tipo_item=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            categoria.upper() if categoria else None, requiere_stock, estado, usuario, id_tipo_item))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de item: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTipoItem(self, id_tipo_item):
        sql = "DELETE FROM tipos_items WHERE id_tipo_item=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_item,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de item: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















