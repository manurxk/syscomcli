# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MarcaTarjetaDao:

    def getMarcasTarjeta(self):
        sql = """
        SELECT id_marca_tarjeta, des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta
        FROM marcas_tarjeta
        ORDER BY des_marca_tarjeta ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            marcas = cur.fetchall()
            return [{'id': m[0], 'descripcion': m[1], 'codigo': m[2] or '', 'estado': m[3]} for m in marcas]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las marcas de tarjeta: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getMarcaTarjetaById(self, id_marca_tarjeta):
        sql = """
        SELECT id_marca_tarjeta, des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta
        FROM marcas_tarjeta
        WHERE id_marca_tarjeta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_marca_tarjeta,))
            marca = cur.fetchone()
            if marca:
                return {"id": marca[0], "descripcion": marca[1], "codigo": marca[2] or '', "estado": marca[3]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener marca de tarjeta: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def marcaTarjetaExiste(self, descripcion):
        sql = "SELECT 1 FROM marcas_tarjeta WHERE LOWER(des_marca_tarjeta)=LOWER(%s)"
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

    def guardarMarcaTarjeta(self, descripcion, codigo=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.marcaTarjetaExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO marcas_tarjeta(des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta, usuario_creacion)
        VALUES(%s, %s, %s, %s)
        RETURNING id_marca_tarjeta
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, estado, usuario))
            id_marca_tarjeta = cur.fetchone()[0]
            con.commit()
            return id_marca_tarjeta
        except Exception as e:
            app.logger.error(f"Error al insertar marca de tarjeta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateMarcaTarjeta(self, id_marca_tarjeta, descripcion, codigo=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE marcas_tarjeta
        SET des_marca_tarjeta=%s, cod_marca_tarjeta=%s, est_marca_tarjeta=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_marca_tarjeta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, estado, usuario, id_marca_tarjeta))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar marca de tarjeta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteMarcaTarjeta(self, id_marca_tarjeta):
        sql = "DELETE FROM marcas_tarjeta WHERE id_marca_tarjeta=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_marca_tarjeta,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar marca de tarjeta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















