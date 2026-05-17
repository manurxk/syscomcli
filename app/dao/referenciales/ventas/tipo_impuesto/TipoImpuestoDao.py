# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoImpuestoDao:

    def getTiposImpuestos(self):
        sql = """
        SELECT id_tipo_impuesto, des_tipo_impuesto, cod_tipo_impuesto, porcentaje_impuesto, 
               tipo_calculo, est_tipo_impuesto
        FROM tipos_impuestos
        ORDER BY des_tipo_impuesto ASC
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
                'porcentaje': float(t[3]) if t[3] else 0,
                'tipo_calculo': t[4] or 'PORCENTAJE',
                'estado': t[5]
            } for t in tipos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de impuestos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTipoImpuestoById(self, id_tipo_impuesto):
        sql = """
        SELECT id_tipo_impuesto, des_tipo_impuesto, cod_tipo_impuesto, porcentaje_impuesto, 
               tipo_calculo, est_tipo_impuesto
        FROM tipos_impuestos
        WHERE id_tipo_impuesto=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_impuesto,))
            tipo = cur.fetchone()
            if tipo:
                return {
                    "id": tipo[0], 
                    "descripcion": tipo[1], 
                    "codigo": tipo[2] or '',
                    "porcentaje": float(tipo[3]) if tipo[3] else 0,
                    "tipo_calculo": tipo[4] or 'PORCENTAJE',
                    "estado": tipo[5]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de impuesto: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def tipoImpuestoExiste(self, descripcion):
        sql = "SELECT 1 FROM tipos_impuestos WHERE LOWER(des_tipo_impuesto)=LOWER(%s)"
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

    def guardarTipoImpuesto(self, descripcion, codigo=None, porcentaje=0, tipo_calculo='PORCENTAJE', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.tipoImpuestoExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO tipos_impuestos(des_tipo_impuesto, cod_tipo_impuesto, porcentaje_impuesto, 
                                   tipo_calculo, est_tipo_impuesto, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING id_tipo_impuesto
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            porcentaje, tipo_calculo, estado, usuario))
            id_tipo_impuesto = cur.fetchone()[0]
            con.commit()
            return id_tipo_impuesto
        except Exception as e:
            app.logger.error(f"Error al insertar tipo de impuesto: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateTipoImpuesto(self, id_tipo_impuesto, descripcion, codigo=None, porcentaje=0, tipo_calculo='PORCENTAJE', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE tipos_impuestos
        SET des_tipo_impuesto=%s, cod_tipo_impuesto=%s, porcentaje_impuesto=%s, 
            tipo_calculo=%s, est_tipo_impuesto=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_tipo_impuesto=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            porcentaje, tipo_calculo, estado, usuario, id_tipo_impuesto))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de impuesto: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTipoImpuesto(self, id_tipo_impuesto):
        sql = "DELETE FROM tipos_impuestos WHERE id_tipo_impuesto=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_impuesto,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de impuesto: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















