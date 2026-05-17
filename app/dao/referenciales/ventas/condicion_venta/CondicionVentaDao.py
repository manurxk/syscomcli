# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CondicionVentaDao:

    def getCondicionesVenta(self):
        sql = """
        SELECT id_condicion_venta, des_condicion_venta, cod_condicion_venta, dias_credito, 
               permite_cuotas, numero_cuotas_max, est_condicion_venta
        FROM condiciones_venta
        ORDER BY dias_credito ASC, des_condicion_venta ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            condiciones = cur.fetchall()
            return [{
                'id': c[0], 
                'descripcion': c[1], 
                'codigo': c[2] or '',
                'dias_credito': c[3],
                'permite_cuotas': c[4],
                'numero_cuotas_max': c[5],
                'estado': c[6]
            } for c in condiciones]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las condiciones de venta: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCondicionVentaById(self, id_condicion_venta):
        sql = """
        SELECT id_condicion_venta, des_condicion_venta, cod_condicion_venta, dias_credito, 
               permite_cuotas, numero_cuotas_max, est_condicion_venta
        FROM condiciones_venta
        WHERE id_condicion_venta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_condicion_venta,))
            condicion = cur.fetchone()
            if condicion:
                return {
                    "id": condicion[0], 
                    "descripcion": condicion[1], 
                    "codigo": condicion[2] or '',
                    "dias_credito": condicion[3],
                    "permite_cuotas": condicion[4],
                    "numero_cuotas_max": condicion[5],
                    "estado": condicion[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener condición de venta: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def condicionVentaExiste(self, descripcion):
        sql = "SELECT 1 FROM condiciones_venta WHERE LOWER(des_condicion_venta)=LOWER(%s)"
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

    def guardarCondicionVenta(self, descripcion, codigo=None, dias_credito=0, permite_cuotas=False, numero_cuotas_max=1, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.condicionVentaExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO condiciones_venta(des_condicion_venta, cod_condicion_venta, dias_credito, 
                                     permite_cuotas, numero_cuotas_max, est_condicion_venta, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_condicion_venta
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            dias_credito, permite_cuotas, numero_cuotas_max, estado, usuario))
            id_condicion_venta = cur.fetchone()[0]
            con.commit()
            return id_condicion_venta
        except Exception as e:
            app.logger.error(f"Error al insertar condición de venta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCondicionVenta(self, id_condicion_venta, descripcion, codigo=None, dias_credito=0, permite_cuotas=False, numero_cuotas_max=1, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE condiciones_venta
        SET des_condicion_venta=%s, cod_condicion_venta=%s, dias_credito=%s, 
            permite_cuotas=%s, numero_cuotas_max=%s, est_condicion_venta=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_condicion_venta=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            dias_credito, permite_cuotas, numero_cuotas_max, estado, usuario, id_condicion_venta))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar condición de venta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCondicionVenta(self, id_condicion_venta):
        sql = "DELETE FROM condiciones_venta WHERE id_condicion_venta=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_condicion_venta,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar condición de venta: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















