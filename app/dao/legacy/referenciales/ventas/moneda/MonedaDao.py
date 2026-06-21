# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class MonedaDao:

    def getMonedas(self):
        sql = """
        SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, 
               es_moneda_local, tasa_cambio, est_moneda
        FROM monedas
        ORDER BY es_moneda_local DESC, des_moneda ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            monedas = cur.fetchall()
            return [{
                'id': m[0], 
                'descripcion': m[1], 
                'codigo': m[2],
                'simbolo': m[3] or '',
                'decimales': m[4],
                'es_moneda_local': m[5],
                'tasa_cambio': float(m[6]) if m[6] else 1.0,
                'estado': m[7]
            } for m in monedas]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las monedas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getMonedaById(self, id_moneda):
        sql = """
        SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, 
               es_moneda_local, tasa_cambio, est_moneda
        FROM monedas
        WHERE id_moneda=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_moneda,))
            moneda = cur.fetchone()
            if moneda:
                return {
                    "id": moneda[0], 
                    "descripcion": moneda[1], 
                    "codigo": moneda[2],
                    "simbolo": moneda[3] or '',
                    "decimales": moneda[4],
                    "es_moneda_local": moneda[5],
                    "tasa_cambio": float(moneda[6]) if moneda[6] else 1.0,
                    "estado": moneda[7]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener moneda: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getMonedaLocal(self):
        """Obtiene la moneda local del sistema (es_moneda_local = TRUE)"""
        sql = """
        SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, 
               es_moneda_local, tasa_cambio, est_moneda
        FROM monedas
        WHERE es_moneda_local = TRUE AND est_moneda = 'A'
        ORDER BY id_moneda ASC
        LIMIT 1
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            moneda = cur.fetchone()
            if moneda:
                return {
                    "id": moneda[0], 
                    "descripcion": moneda[1], 
                    "codigo": moneda[2],
                    "simbolo": moneda[3] or '',
                    "decimales": moneda[4],
                    "es_moneda_local": moneda[5],
                    "tasa_cambio": float(moneda[6]) if moneda[6] else 1.0,
                    "estado": moneda[7]
                }
            # Si no hay moneda local, obtener la primera moneda activa
            sql_fallback = """
            SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, 
                   es_moneda_local, tasa_cambio, est_moneda
            FROM monedas
            WHERE est_moneda = 'A'
            ORDER BY id_moneda ASC
            LIMIT 1
            """
            cur.execute(sql_fallback)
            moneda = cur.fetchone()
            if moneda:
                return {
                    "id": moneda[0], 
                    "descripcion": moneda[1], 
                    "codigo": moneda[2],
                    "simbolo": moneda[3] or '',
                    "decimales": moneda[4],
                    "es_moneda_local": moneda[5],
                    "tasa_cambio": float(moneda[6]) if moneda[6] else 1.0,
                    "estado": moneda[7]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener moneda local: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def monedaExiste(self, codigo):
        sql = "SELECT 1 FROM monedas WHERE UPPER(cod_moneda)=UPPER(%s)"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (codigo,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarDescripcion(self, descripcion):
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    def guardarMoneda(self, descripcion, codigo, simbolo=None, decimales=0, es_moneda_local=False, tasa_cambio=1.0, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not codigo or codigo.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.monedaExiste(codigo):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO monedas(des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, 
                           es_moneda_local, tasa_cambio, est_moneda, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_moneda
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper(), simbolo, decimales, 
                            es_moneda_local, tasa_cambio, estado, usuario))
            id_moneda = cur.fetchone()[0]
            con.commit()
            return id_moneda
        except Exception as e:
            app.logger.error(f"Error al insertar moneda: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateMoneda(self, id_moneda, descripcion, codigo, simbolo=None, decimales=0, es_moneda_local=False, tasa_cambio=1.0, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not codigo or codigo.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE monedas
        SET des_moneda=%s, cod_moneda=%s, simbolo_moneda=%s, decimales_moneda=%s, 
            es_moneda_local=%s, tasa_cambio=%s, est_moneda=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_moneda=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper(), simbolo, decimales,
                            es_moneda_local, tasa_cambio, estado, usuario, id_moneda))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar moneda: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteMoneda(self, id_moneda):
        sql = "DELETE FROM monedas WHERE id_moneda=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_moneda,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar moneda: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
