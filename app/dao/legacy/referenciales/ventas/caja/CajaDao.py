# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CajaDao:

    def getCajas(self):
        sql = """
        SELECT id_caja, des_caja, cod_caja, caja_saldo_inicial, caja_saldo_actual, caja_estado, est_caja
        FROM cajas
        ORDER BY des_caja ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            cajas = cur.fetchall()
            return [{
                'id': c[0], 
                'descripcion': c[1], 
                'codigo': c[2] or '',
                'saldo_inicial': c[3],
                'saldo_actual': c[4],
                'estado_caja': c[5],
                'estado': c[6]
            } for c in cajas]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las cajas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCajaById(self, id_caja):
        sql = """
        SELECT id_caja, des_caja, cod_caja, caja_saldo_inicial, caja_saldo_actual, caja_estado, est_caja
        FROM cajas
        WHERE id_caja=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_caja,))
            caja = cur.fetchone()
            if caja:
                return {
                    "id": caja[0], 
                    "descripcion": caja[1], 
                    "codigo": caja[2] or '',
                    "saldo_inicial": caja[3],
                    "saldo_actual": caja[4],
                    "estado_caja": caja[5],
                    "estado": caja[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener caja: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def cajaExiste(self, descripcion):
        sql = "SELECT 1 FROM cajas WHERE LOWER(des_caja)=LOWER(%s)"
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
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .-]+$"
        return bool(re.match(patron, descripcion))

    def guardarCaja(self, descripcion, codigo=None, saldo_inicial=0, estado_caja='CERRADA', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.cajaExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False
        if estado_caja not in ['ABIERTA', 'CERRADA']:
            return False

        sql = """
        INSERT INTO cajas(des_caja, cod_caja, caja_saldo_inicial, caja_saldo_actual, caja_estado, est_caja, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_caja
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            saldo_inicial, saldo_inicial, estado_caja, estado, usuario))
            id_caja = cur.fetchone()[0]
            con.commit()
            return id_caja
        except Exception as e:
            app.logger.error(f"Error al insertar caja: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCaja(self, id_caja, descripcion, codigo=None, saldo_inicial=None, estado_caja=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False
        if estado_caja and estado_caja not in ['ABIERTA', 'CERRADA']:
            return False

        sql = """
        UPDATE cajas
        SET des_caja=%s, cod_caja=%s, est_caja=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        """
        params = [descripcion.upper(), codigo.upper() if codigo else None, estado]
        
        if saldo_inicial is not None:
            sql += ", caja_saldo_inicial=%s"
            params.append(saldo_inicial)
        
        if estado_caja:
            sql += ", caja_estado=%s"
            params.append(estado_caja)
        
        sql += " WHERE id_caja=%s"
        params.append(id_caja)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            params.insert(-1, usuario)
            cur.execute(sql, tuple(params))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar caja: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCaja(self, id_caja):
        sql = "DELETE FROM cajas WHERE id_caja=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_caja,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar caja: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

