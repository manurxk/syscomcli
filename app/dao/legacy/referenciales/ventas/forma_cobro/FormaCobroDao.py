# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class FormaCobroDao:

    def getFormasCobro(self):
        sql = """
        SELECT id_forma_cobro, des_forma_cobro, cod_forma_cobro, requiere_entidad, 
               permite_cuotas, est_forma_cobro
        FROM formas_cobro
        ORDER BY des_forma_cobro ASC
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            formas = cur.fetchall()
            return [{
                'id': f[0], 
                'descripcion': f[1], 
                'codigo': f[2] or '',
                'requiere_entidad': f[3],
                'permite_cuotas': f[4],
                'estado': f[5]
            } for f in formas]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las formas de cobro: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getFormaCobroById(self, id_forma_cobro):
        sql = """
        SELECT id_forma_cobro, des_forma_cobro, cod_forma_cobro, requiere_entidad, 
               permite_cuotas, est_forma_cobro
        FROM formas_cobro
        WHERE id_forma_cobro=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_forma_cobro,))
            forma = cur.fetchone()
            if forma:
                return {
                    "id": forma[0], 
                    "descripcion": forma[1], 
                    "codigo": forma[2] or '',
                    "requiere_entidad": forma[3],
                    "permite_cuotas": forma[4],
                    "estado": forma[5]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener forma de cobro: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def formaCobroExiste(self, descripcion):
        """Verifica si ya existe la forma de cobro con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM formas_cobro WHERE LOWER(des_forma_cobro)=LOWER(%s)"
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
        """Permite solo letras, números, acentos, espacios y puntos."""
        patron = r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .]+$"
        return bool(re.match(patron, descripcion))

    # ============================
    # CRUD
    # ============================

    def guardarFormaCobro(self, descripcion, codigo=None, requiere_entidad=False, 
                         permite_cuotas=False, estado='A'):
        # Validaciones
        if not descripcion or descripcion.strip() == "":
            app.logger.warning("Descripción vacía")
            return False
        
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida: solo letras, números, acentos, espacios y puntos")
            return False
        
        if self.formaCobroExiste(descripcion):
            app.logger.warning("La forma de cobro ya existe")
            return False

        if estado not in ['A', 'I']:
            app.logger.warning("Estado inválido: debe ser 'A' (Activo) o 'I' (Inactivo)")
            return False

        sql = """
        INSERT INTO formas_cobro(des_forma_cobro, cod_forma_cobro, requiere_entidad, 
                                permite_cuotas, est_forma_cobro, usuario_creacion)
        VALUES(%s, %s, %s, %s, %s, %s)
        RETURNING id_forma_cobro
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None, 
                            requiere_entidad, permite_cuotas, estado, usuario))
            id_forma_cobro = cur.fetchone()[0]
            con.commit()
            app.logger.info(f"Forma de cobro insertada con ID: {id_forma_cobro}")
            return id_forma_cobro
        except Exception as e:
            app.logger.error(f"Error al insertar forma de cobro: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateFormaCobro(self, id_forma_cobro, descripcion, codigo=None, 
                        requiere_entidad=False, permite_cuotas=False, estado='A'):
        # Validaciones
        if not descripcion or descripcion.strip() == "":
            app.logger.warning("Descripción vacía")
            return False
        
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida")
            return False

        if estado not in ['A', 'I']:
            app.logger.warning("Estado inválido")
            return False

        sql = """
        UPDATE formas_cobro
        SET des_forma_cobro=%s, cod_forma_cobro=%s, requiere_entidad=%s, 
            permite_cuotas=%s, est_forma_cobro=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_forma_cobro=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion.upper(), codigo.upper() if codigo else None,
                            requiere_entidad, permite_cuotas, estado, usuario, id_forma_cobro))
            filas = cur.rowcount
            con.commit()
            if filas > 0:
                app.logger.info(f"Forma de cobro {id_forma_cobro} actualizada")
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar forma de cobro: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteFormaCobro(self, id_forma_cobro):
        sql = "DELETE FROM formas_cobro WHERE id_forma_cobro=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_forma_cobro,))
            filas = cur.rowcount
            con.commit()
            if filas > 0:
                app.logger.info(f"Forma de cobro {id_forma_cobro} eliminada")
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar forma de cobro: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















