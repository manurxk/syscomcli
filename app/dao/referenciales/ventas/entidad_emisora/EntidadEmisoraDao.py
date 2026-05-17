# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class EntidadEmisoraDao:

    def getEntidadesEmisoras(self):
        sql = """
        SELECT id_entidad_emisora, des_entidad_emisora, cod_entidad_emisora, ruc_entidad, 
               telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora
        FROM entidades_emisoras
        ORDER BY des_entidad_emisora ASC
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
                'tipo_entidad': e[6] or '',
                'estado': e[7]
            } for e in entidades]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las entidades emisoras: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEntidadEmisoraById(self, id_entidad_emisora):
        sql = """
        SELECT id_entidad_emisora, des_entidad_emisora, cod_entidad_emisora, ruc_entidad, 
               telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora
        FROM entidades_emisoras
        WHERE id_entidad_emisora=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_entidad_emisora,))
            entidad = cur.fetchone()
            if entidad:
                return {
                    "id": entidad[0], 
                    "descripcion": entidad[1], 
                    "codigo": entidad[2] or '',
                    "ruc": entidad[3] or '',
                    "telefono": entidad[4] or '',
                    "email": entidad[5] or '',
                    "tipo_entidad": entidad[6] or '',
                    "estado": entidad[7]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener entidad emisora: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def entidadEmisoraExiste(self, descripcion):
        sql = "SELECT 1 FROM entidades_emisoras WHERE LOWER(des_entidad_emisora)=LOWER(%s)"
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

    def guardarEntidadEmisora(self, descripcion, codigo=None, ruc=None, telefono=None, email=None, tipo_entidad=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if self.entidadEmisoraExiste(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        INSERT INTO entidades_emisoras(des_entidad_emisora, cod_entidad_emisora, ruc_entidad, 
                                      telefono_entidad, email_entidad, tipo_entidad, est_entidad_emisora, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_entidad_emisora
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            ruc, telefono, email, tipo_entidad.upper() if tipo_entidad else None, estado, usuario))
            id_entidad_emisora = cur.fetchone()[0]
            con.commit()
            return id_entidad_emisora
        except Exception as e:
            app.logger.error(f"Error al insertar entidad emisora: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateEntidadEmisora(self, id_entidad_emisora, descripcion, codigo=None, ruc=None, telefono=None, email=None, tipo_entidad=None, estado='A'):
        if not descripcion or descripcion.strip() == "":
            return False
        if not self.validarDescripcion(descripcion):
            return False
        if estado not in ['A', 'I']:
            return False

        sql = """
        UPDATE entidades_emisoras
        SET des_entidad_emisora=%s, cod_entidad_emisora=%s, ruc_entidad=%s, 
            telefono_entidad=%s, email_entidad=%s, tipo_entidad=%s, est_entidad_emisora=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_entidad_emisora=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            ruc, telefono, email, tipo_entidad.upper() if tipo_entidad else None, estado, usuario, id_entidad_emisora))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar entidad emisora: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEntidadEmisora(self, id_entidad_emisora):
        sql = "DELETE FROM entidades_emisoras WHERE id_entidad_emisora=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_entidad_emisora,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar entidad emisora: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















