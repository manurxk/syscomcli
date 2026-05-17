# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EntidadAdheridaDao:

    def getEntidadesAdheridas(self):
        sql = """
        SELECT id_entidad_adherida, des_entidad_adherida, cod_entidad_adherida, ruc_entidad, 
               telefono_entidad, email_entidad, est_entidad_adherida
        FROM entidades_adheridas
        ORDER BY des_entidad_adherida ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            entidades = cur.fetchall()
            return [{
                'id': e[0], 
                'descripcion': e[1], 
                'codigo': e[2] or '',
                'ruc': e[3] or '',
                'telefono': e[4] or '',
                'email': e[5] or '',
                'estado': e[6]
            } for e in entidades]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las entidades adheridas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEntidadAdheridaById(self, id_entidad_adherida):
        sql = """
        SELECT id_entidad_adherida, des_entidad_adherida, cod_entidad_adherida, ruc_entidad, 
               telefono_entidad, email_entidad, est_entidad_adherida
        FROM entidades_adheridas
        WHERE id_entidad_adherida=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_entidad_adherida,))
            entidad = cur.fetchone()
            if entidad:
                return {
                    "id": entidad[0], 
                    "descripcion": entidad[1], 
                    "codigo": entidad[2] or '',
                    "ruc": entidad[3] or '',
                    "telefono": entidad[4] or '',
                    "email": entidad[5] or '',
                    "estado": entidad[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener entidad adherida: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def entidadAdheridaExiste(self, descripcion):
        sql = "SELECT 1 FROM entidades_adheridas WHERE LOWER(des_entidad_adherida)=LOWER(%s)"
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

    def guardarEntidadAdherida(self, descripcion, codigo=None, ruc=None, telefono=None, email=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.entidadAdheridaExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO entidades_adheridas(des_entidad_adherida, cod_entidad_adherida, ruc_entidad, 
                                      telefono_entidad, email_entidad, est_entidad_adherida, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_entidad_adherida
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            ruc, telefono, email, estado, usuario))
            id_entidad_adherida = cur.fetchone()[0]
            con.commit()
            return id_entidad_adherida
        except Exception as e:
            app.logger.error(f"Error al insertar entidad adherida: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateEntidadAdherida(self, id_entidad_adherida, descripcion, codigo=None, ruc=None, telefono=None, email=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE entidades_adheridas
        SET des_entidad_adherida=%s, cod_entidad_adherida=%s, ruc_entidad=%s, 
            telefono_entidad=%s, email_entidad=%s, est_entidad_adherida=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_entidad_adherida=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            ruc, telefono, email, estado, usuario, id_entidad_adherida))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar entidad adherida: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEntidadAdherida(self, id_entidad_adherida):
        sql = "DELETE FROM entidades_adheridas WHERE id_entidad_adherida=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_entidad_adherida,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar entidad adherida: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















