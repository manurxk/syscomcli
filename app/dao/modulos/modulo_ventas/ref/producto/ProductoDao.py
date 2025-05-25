from flask import current_app as app
from app.conexion.Conexion import Conexion
import psycopg2

class ProductoDao:

    def getProductos(self):
        sql = "SELECT id, descripcion, cantidad, precio_unitario FROM productos"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            rows = cur.fetchall()
            return [{"id": r[0], "descripcion": r[1], "cantidad": r[2], "precio_unitario": float(r[3])} for r in rows]
        except psycopg2.Error as e:
            app.logger.error(e)
            return []
        finally:
            cur.close()
            con.close()

    def getProductoById(self, id):
        sql = "SELECT id, descripcion, cantidad, precio_unitario FROM productos WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            row = cur.fetchone()
            if row:
                return {"id": row[0], "descripcion": row[1], "cantidad": row[2], "precio_unitario": float(row[3])}
            return None
        except psycopg2.Error as e:
            app.logger.error(e)
            return None
        finally:
            cur.close()
            con.close()

    def guardarProducto(self, descripcion, cantidad, precio_unitario):
        sql = """
        INSERT INTO productos (descripcion, cantidad, precio_unitario)
        VALUES (%s, %s, %s)
        RETURNING id
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, cantidad, precio_unitario))
            producto_id = cur.fetchone()[0]
            con.commit()
            return producto_id
        except psycopg2.Error as e:
            app.logger.error(e)
            return None
        finally:
            cur.close()
            con.close()

    def updateProducto(self, id, descripcion, cantidad, precio_unitario):
        sql = """
        UPDATE productos
        SET descripcion = %s, cantidad = %s, precio_unitario = %s
        WHERE id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (descripcion, cantidad, precio_unitario, id))
            con.commit()
            return cur.rowcount > 0
        except psycopg2.Error as e:
            app.logger.error(e)
            return False
        finally:
            cur.close()
            con.close()

    def deleteProducto(self, id):
        sql = "DELETE FROM productos WHERE id = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id,))
            con.commit()
            return cur.rowcount > 0
        except psycopg2.Error as e:
            app.logger.error(e)
            return False
        finally:
            cur.close()
            con.close()
