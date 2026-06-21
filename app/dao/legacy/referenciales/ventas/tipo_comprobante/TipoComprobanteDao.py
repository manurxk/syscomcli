# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoComprobanteDao:

    def getTiposComprobantes(self):
        sql = """
        SELECT id_tipo_comprobante, des_tipo_comprobante, cod_tipo_comprobante, codigo_sifen, 
               requiere_timbrado, tipo_documento, est_tipo_comprobante
        FROM tipos_comprobantes
        ORDER BY des_tipo_comprobante ASC
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
                'codigo_sifen': t[3] or '',
                'requiere_timbrado': t[4],
                'tipo_documento': t[5] or '',
                'estado': t[6]
            } for t in tipos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de comprobantes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTipoComprobanteById(self, id_tipo_comprobante):
        sql = """
        SELECT id_tipo_comprobante, des_tipo_comprobante, cod_tipo_comprobante, codigo_sifen, 
               requiere_timbrado, tipo_documento, est_tipo_comprobante
        FROM tipos_comprobantes
        WHERE id_tipo_comprobante=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_comprobante,))
            tipo = cur.fetchone()
            if tipo:
                return {
                    "id": tipo[0], 
                    "descripcion": tipo[1], 
                    "codigo": tipo[2] or '',
                    "codigo_sifen": tipo[3] or '',
                    "requiere_timbrado": tipo[4],
                    "tipo_documento": tipo[5] or '',
                    "estado": tipo[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de comprobante: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def tipoComprobanteExiste(self, descripcion):
        sql = "SELECT 1 FROM tipos_comprobantes WHERE LOWER(des_tipo_comprobante)=LOWER(%s)"
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

    def guardarTipoComprobante(self, descripcion, codigo=None, codigo_sifen=None, requiere_timbrado=True, tipo_documento=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.tipoComprobanteExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO tipos_comprobantes(des_tipo_comprobante, cod_tipo_comprobante, codigo_sifen, 
                                      requiere_timbrado, tipo_documento, est_tipo_comprobante, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_tipo_comprobante
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            codigo_sifen, requiere_timbrado, tipo_documento.upper() if tipo_documento else None, estado, usuario))
            id_tipo_comprobante = cur.fetchone()[0]
            con.commit()
            return id_tipo_comprobante
        except Exception as e:
            app.logger.error(f"Error al insertar tipo de comprobante: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateTipoComprobante(self, id_tipo_comprobante, descripcion, codigo=None, codigo_sifen=None, requiere_timbrado=True, tipo_documento=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE tipos_comprobantes
        SET des_tipo_comprobante=%s, cod_tipo_comprobante=%s, codigo_sifen=%s, 
            requiere_timbrado=%s, tipo_documento=%s, est_tipo_comprobante=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_tipo_comprobante=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            codigo_sifen, requiere_timbrado, tipo_documento.upper() if tipo_documento else None, estado, usuario, id_tipo_comprobante))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de comprobante: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTipoComprobante(self, id_tipo_comprobante):
        sql = "DELETE FROM tipos_comprobantes WHERE id_tipo_comprobante=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_comprobante,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de comprobante: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















