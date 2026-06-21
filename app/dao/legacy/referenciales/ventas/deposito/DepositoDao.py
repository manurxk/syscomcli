# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class DepositoDao:

    def getDepositos(self):
        sql = """
        SELECT id_deposito, des_deposito, cod_deposito, tipo_deposito, numero_cuenta, 
               banco_deposito, ruc_banco, moneda_deposito, est_deposito
        FROM depositos
        ORDER BY des_deposito ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            depositos = cur.fetchall()
            return [{
                'id': d[0], 
                'descripcion': d[1], 
                'codigo': d[2] or '',
                'tipo_deposito': d[3],
                'numero_cuenta': d[4] or '',
                'banco': d[5] or '',
                'ruc_banco': d[6] or '',
                'moneda': d[7] or 'PYG',
                'estado': d[8]
            } for d in depositos]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los depósitos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getDepositoById(self, id_deposito):
        sql = """
        SELECT id_deposito, des_deposito, cod_deposito, tipo_deposito, numero_cuenta, 
               banco_deposito, ruc_banco, moneda_deposito, est_deposito
        FROM depositos
        WHERE id_deposito=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_deposito,))
            deposito = cur.fetchone()
            if deposito:
                return {
                    "id": deposito[0], 
                    "descripcion": deposito[1], 
                    "codigo": deposito[2] or '',
                    "tipo_deposito": deposito[3],
                    "numero_cuenta": deposito[4] or '',
                    "banco": deposito[5] or '',
                    "ruc_banco": deposito[6] or '',
                    "moneda": deposito[7] or 'PYG',
                    "estado": deposito[8]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener depósito: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def depositoExiste(self, descripcion):
        sql = "SELECT 1 FROM depositos WHERE LOWER(des_deposito)=LOWER(%s)"
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

    def guardarDeposito(self, descripcion, codigo=None, tipo_deposito='BANCO', numero_cuenta=None, banco=None, ruc_banco=None, moneda='PYG', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.depositoExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO depositos(des_deposito, cod_deposito, tipo_deposito, numero_cuenta, 
                             banco_deposito, ruc_banco, moneda_deposito, est_deposito, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_deposito
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            tipo_deposito.upper(), numero_cuenta, banco.upper() if banco else None, 
                            ruc_banco, moneda.upper(), estado, usuario))
            id_deposito = cur.fetchone()[0]
            con.commit()
            return id_deposito
        except Exception as e:
            app.logger.error(f"Error al insertar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateDeposito(self, id_deposito, descripcion, codigo=None, tipo_deposito='BANCO', numero_cuenta=None, banco=None, ruc_banco=None, moneda='PYG', estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE depositos
        SET des_deposito=%s, cod_deposito=%s, tipo_deposito=%s, numero_cuenta=%s, 
            banco_deposito=%s, ruc_banco=%s, moneda_deposito=%s, est_deposito=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_deposito=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            tipo_deposito.upper(), numero_cuenta, banco.upper() if banco else None,
                            ruc_banco, moneda.upper(), estado, usuario, id_deposito))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteDeposito(self, id_deposito):
        sql = "DELETE FROM depositos WHERE id_deposito=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_deposito,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar depósito: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















