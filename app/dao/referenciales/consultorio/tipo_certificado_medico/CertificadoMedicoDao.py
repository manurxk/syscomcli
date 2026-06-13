import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class TipoCertificadoMedicoDao:

    def getTiposCertificadosMedicos(self):
        sql = """
        SELECT id_tipo_certificado, des_tipo_certificado, est_tipo_certificado
        FROM tipos_certificados_medicos
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            tipos_certificados = cur.fetchall()
            return [{'id': t[0], 'descripcion': t[1], 'estado': t[2]} for t in tipos_certificados]
        except Exception as e:
            app.logger.error(f"Error al obtener todos los tipos de certificados médicos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getTipoCertificadoMedicoById(self, id_tipo_certificado):
        sql = """
        SELECT id_tipo_certificado, des_tipo_certificado, est_tipo_certificado
        FROM tipos_certificados_medicos
        WHERE id_tipo_certificado=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_certificado,))
            tipo_certificado = cur.fetchone()
            if tipo_certificado:
                return {"id": tipo_certificado[0], "descripcion": tipo_certificado[1], "estado": tipo_certificado[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener tipo de certificado médico: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def tipoCertificadoMedicoExiste(self, descripcion):
        """Verifica si ya existe el tipo de certificado médico con el mismo nombre (case-insensitive)."""
        sql = "SELECT 1 FROM tipos_certificados_medicos WHERE LOWER(des_tipo_certificado)=LOWER(%s)"
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

    def guardarTipoCertificadoMedico(self, descripcion, estado='A'):
        # Validaciones
        if not descripcion or descripcion.strip() == "":
            app.logger.warning("Descripción vacía")
            return False
        
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida: solo letras, números, acentos, espacios y puntos")
            return False
        
        if self.tipoCertificadoMedicoExiste(descripcion):
            app.logger.warning("El tipo de certificado médico ya existe")
            return False

        if estado not in ['A', 'I']:
            app.logger.warning("Estado inválido: debe ser 'A' (Activo) o 'I' (Inactivo)")
            return False

        sql = """
        INSERT INTO tipos_certificados_medicos(des_tipo_certificado, est_tipo_certificado, usuario_creacion)
        VALUES(%s, %s, %s)
        RETURNING id_tipo_certificado
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion, estado, usuario))
            id_tipo_certificado = cur.fetchone()[0]
            con.commit()
            app.logger.info(f"Tipo de certificado médico insertado con ID: {id_tipo_certificado}")
            return id_tipo_certificado
        except Exception as e:
            app.logger.error(f"Error al insertar tipo de certificado médico: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateTipoCertificadoMedico(self, id_tipo_certificado, descripcion, estado='A'):
        # Validaciones
        if not descripcion or descripcion.strip() == "":
            app.logger.warning("Descripción vacía")
            return False
        
        if not self.validarDescripcion(descripcion):
            app.logger.warning("Descripción inválida: solo letras, números, acentos, espacios y puntos")
            return False

        if estado not in ['A', 'I']:
            app.logger.warning("Estado inválido")
            return False

        sql = """
        UPDATE tipos_certificados_medicos
        SET des_tipo_certificado=%s, est_tipo_certificado=%s, 
            usuario_modificacion=%s, fecha_modificacion=CURRENT_TIMESTAMP
        WHERE id_tipo_certificado=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            usuario = app.config.get('USUARIO_ACTUAL', 'SISTEMA')
            cur.execute(sql, (descripcion, estado, usuario, id_tipo_certificado))
            filas = cur.rowcount
            con.commit()
            if filas > 0:
                app.logger.info(f"Tipo de certificado médico {id_tipo_certificado} actualizado")
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar tipo de certificado médico: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteTipoCertificadoMedico(self, id_tipo_certificado):
        sql = "DELETE FROM tipos_certificados_medicos WHERE id_tipo_certificado=%s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_tipo_certificado,))
            filas = cur.rowcount
            con.commit()
            if filas > 0:
                app.logger.info(f"Tipo de certificado médico {id_tipo_certificado} eliminado")
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar tipo de certificado médico: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


















