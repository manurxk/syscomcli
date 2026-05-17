# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EstadoFacturaDao:

    def getEstadosFactura(self):
        sql = """
        SELECT id_estado_factura, des_estado_factura, cod_estado_factura, permite_modificacion, 
               permite_anulacion, color_estado, est_estado_factura
        FROM estados_factura
        ORDER BY des_estado_factura ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            estados = cur.fetchall()
            return [{
                'id': e[0], 
                'descripcion': e[1], 
                'codigo': e[2] or '',
                'permite_modificacion': e[3],
                'permite_anulacion': e[4],
                'color': e[5] or 'secondary',
                'estado': e[6]
            } for e in estados]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los estados de factura: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEstadoFacturaById(self, id_estado_factura):
        sql = """
        SELECT id_estado_factura, des_estado_factura, cod_estado_factura, permite_modificacion, 
               permite_anulacion, color_estado, est_estado_factura
        FROM estados_factura
        WHERE id_estado_factura=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_estado_factura,))
            estado = cur.fetchone()
            if estado:
                return {
                    "id": estado[0], 
                    "descripcion": estado[1], 
                    "codigo": estado[2] or '',
                    "permite_modificacion": estado[3],
                    "permite_anulacion": estado[4],
                    "color": estado[5] or 'secondary',
                    "estado": estado[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener estado de factura: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def estadoFacturaExiste(self, descripcion):
        sql = "SELECT 1 FROM estados_factura WHERE LOWER(des_estado_factura)=LOWER(%s)"
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

    def guardarEstadoFactura(self, descripcion, codigo=None, permite_modificacion=True, 
                             permite_anulacion=True, color='secondary', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.estadoFacturaExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO estados_factura(des_estado_factura, cod_estado_factura, permite_modificacion, 
                                   permite_anulacion, color_estado, est_estado_factura, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_estado_factura
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            permite_modificacion, permite_anulacion, color, estado, usuario))
            id_estado_factura = cur.fetchone()[0]
            con.commit()
            return id_estado_factura
        except Exception as e:
            app.logger.error(f"Error al insertar estado de factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateEstadoFactura(self, id_estado_factura, descripcion, codigo=None, 
                           permite_modificacion=True, permite_anulacion=True, color='secondary', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE estados_factura
        SET des_estado_factura=%s, cod_estado_factura=%s, permite_modificacion=%s, 
            permite_anulacion=%s, color_estado=%s, est_estado_factura=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_estado_factura=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            permite_modificacion, permite_anulacion, color, estado, usuario, id_estado_factura))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar estado de factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEstadoFactura(self, id_estado_factura):
        sql = "DELETE FROM estados_factura WHERE id_estado_factura=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_estado_factura,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar estado de factura: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















