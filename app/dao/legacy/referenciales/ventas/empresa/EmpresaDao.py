import re
from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import date, datetime

class EmpresaDao:

    # ============================
    # OBTENER
    # ============================

    def getEmpresas(self):
        """Obtiene todas las empresas"""
        sql = """
        SELECT 
            id_empresa, ruc_nit, razon_social, nombre_comercial,
            tipo_contribuyente, direccion, ciudad, departamento,
            telefono, email, est_empresa, es_principal
        FROM empresa
        ORDER BY es_principal DESC, razon_social
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            empresas = cur.fetchall()
            return [{
                'id': e[0],
                'ruc_nit': e[1],
                'razon_social': e[2],
                'nombre_comercial': e[3],
                'tipo_contribuyente': e[4],
                'direccion': e[5],
                'ciudad': e[6],
                'departamento': e[7],
                'telefono': e[8],
                'email': e[9],
                'estado': e[10],
                'es_principal': e[11]
            } for e in empresas]
        except Exception as e:
            app.logger.error(f"Error al obtener empresas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEmpresaById(self, id_empresa):
        """Obtiene una empresa por ID con todos sus datos"""
        sql = """
        SELECT 
            id_empresa, ruc_nit, digito_verificador, razon_social, nombre_comercial,
            tipo_contribuyente, departamento, distrito, ciudad, direccion,
            numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            representante_legal_nombre, representante_legal_apellido,
            representante_legal_ci, representante_legal_cargo,
            facturador_electronico, fecha_habilitacion_sifen, grupo_obligatoriedad,
            ambiente_sifen, certificado_firma_digital_path,
            certificado_firma_digital_serial, certificado_firma_digital_fecha_vencimiento,
            codigo_seguridad_contribuyente, actividad_economica_principal,
            logo_path, horario_atencion, es_principal, est_empresa
        FROM empresa
        WHERE id_empresa = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa,))
            e = cur.fetchone()
            if e:
                return {
                    'id': e[0],
                    'ruc_nit': e[1],
                    'digito_verificador': e[2],
                    'razon_social': e[3],
                    'nombre_comercial': e[4],
                    'tipo_contribuyente': e[5],
                    'departamento': e[6],
                    'distrito': e[7],
                    'ciudad': e[8],
                    'direccion': e[9],
                    'numero_casa': e[10],
                    'codigo_postal': e[11],
                    'telefono': e[12],
                    'celular': e[13],
                    'email': e[14],
                    'sitio_web': e[15],
                    'representante_legal_nombre': e[16],
                    'representante_legal_apellido': e[17],
                    'representante_legal_ci': e[18],
                    'representante_legal_cargo': e[19],
                    'facturador_electronico': e[20],
                    'fecha_habilitacion_sifen': e[21],
                    'grupo_obligatoriedad': e[22],
                    'ambiente_sifen': e[23],
                    'certificado_firma_digital_path': e[24],
                    'certificado_firma_digital_serial': e[25],
                    'certificado_firma_digital_fecha_vencimiento': e[26],
                    'codigo_seguridad_contribuyente': e[27],
                    'actividad_economica_principal': e[28],
                    'logo_path': e[29],
                    'horario_atencion': e[30],
                    'es_principal': e[31],
                    'estado': e[32]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener empresa: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getEmpresaPrincipal(self):
        """Obtiene los datos de la empresa marcada como principal"""
        sql = """
        SELECT 
            id_empresa, ruc_nit, digito_verificador, razon_social, nombre_comercial,
            tipo_contribuyente, departamento, distrito, ciudad, direccion,
            numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            actividad_economica_principal, logo_path, es_principal
        FROM empresa
        WHERE es_principal = TRUE AND est_empresa = TRUE
        LIMIT 1
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            e = cur.fetchone()
            if e:
                return {
                    'id': e[0],
                    'ruc_nit': e[1],
                    'digito_verificador': e[2],
                    'razon_social': e[3],
                    'nombre_comercial': e[4],
                    'tipo_contribuyente': e[5],
                    'departamento': e[6],
                    'distrito': e[7],
                    'ciudad': e[8],
                    'direccion': e[9],
                    'numero_casa': e[10],
                    'codigo_postal': e[11],
                    'telefono': e[12],
                    'celular': e[13],
                    'email': e[14],
                    'sitio_web': e[15],
                    'actividad_economica': e[16],
                    'logo_path': e[17],
                    'es_principal': e[18]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener empresa principal: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()


    def getEmpresaPorRUC(self, ruc):
        """Obtiene una empresa por RUC"""
        sql = "SELECT id_empresa, ruc_nit, razon_social FROM empresa WHERE ruc_nit = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (ruc,))
            e = cur.fetchone()
            if e:
                return {'id': e[0], 'ruc_nit': e[1], 'razon_social': e[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener empresa por RUC: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getDatosEmpresaParaSIFEN(self, id_empresa):
        """Obtiene los datos de empresa necesarios para generar XML SIFEN"""
        sql = """
        SELECT 
            ruc_nit, digito_verificador, razon_social, nombre_comercial,
            direccion, numero_casa, ciudad, departamento, distrito,
            telefono, email, codigo_seguridad_contribuyente
        FROM empresa
        WHERE id_empresa = %s AND est_empresa = TRUE
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa,))
            e = cur.fetchone()
            if e:
                return {
                    'ruc': e[0],
                    'digito_verificador': e[1],
                    'razon_social': e[2],
                    'nombre_comercial': e[3],
                    'direccion': e[4],
                    'numero_casa': e[5] or '',
                    'ciudad': e[6],
                    'departamento': e[7],
                    'distrito': e[8],
                    'telefono': e[9],
                    'email': e[10],
                    'codigo_seguridad_contribuyente': e[11]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener datos SIFEN de empresa: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def empresaExiste(self, ruc_nit):
        """Verifica si ya existe una empresa con el mismo RUC"""
        sql = "SELECT 1 FROM empresa WHERE ruc_nit = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (ruc_nit,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    def validarRUC(self, ruc_nit):
        """Valida formato básico de RUC (6-20 caracteres, solo números)"""
        if not ruc_nit:
            return False
        # Remover guiones si existen
        ruc_limpio = ruc_nit.replace('-', '')
        # Debe ser numérico y tener entre 6 y 20 dígitos
        return ruc_limpio.isdigit() and 6 <= len(ruc_limpio) <= 20

    def validarEmail(self, email):
        """Valida formato de email"""
        if not email:
            return False
        patron = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return bool(re.match(patron, email))

    def verificarCertificadoVigente(self, id_empresa):
        """Verifica si el certificado digital está vigente"""
        sql = """
        SELECT certificado_firma_digital_fecha_vencimiento
        FROM empresa
        WHERE id_empresa = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa,))
            resultado = cur.fetchone()
            if resultado and resultado[0]:
                fecha_vencimiento = resultado[0]
                return fecha_vencimiento >= date.today()
            return False
        except Exception as e:
            app.logger.error(f"Error al verificar certificado: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    # ============================
    # CRUD
    # ============================

    def guardarEmpresa(self, datos, usuario=1):
        """
        Guarda una nueva empresa
        datos: dict con todos los campos de la empresa
        """
        # Validaciones básicas
        if not datos.get('ruc_nit') or not datos.get('razon_social'):
            app.logger.warning("RUC y razón social son obligatorios")
            return False
        
        if not self.validarRUC(datos['ruc_nit']):
            app.logger.warning("RUC inválido")
            return False
        
        if self.empresaExiste(datos['ruc_nit']):
            app.logger.warning("Ya existe una empresa con este RUC")
            return False

        sql = """
        INSERT INTO empresa (
            ruc_nit, digito_verificador, razon_social, nombre_comercial,
            tipo_contribuyente, departamento, distrito, ciudad, direccion,
            numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            representante_legal_nombre, representante_legal_apellido,
            representante_legal_ci, representante_legal_cargo,
            actividad_economica_principal, horario_atencion,
            es_principal, est_empresa, creacion_usuario
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        RETURNING id_empresa
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('ruc_nit'),
                datos.get('digito_verificador', ''),
                datos.get('razon_social'),
                datos.get('nombre_comercial'),
                datos.get('tipo_contribuyente', 'persona_juridica'),
                datos.get('departamento'),
                datos.get('distrito'),
                datos.get('ciudad'),
                datos.get('direccion'),
                datos.get('numero_casa'),
                datos.get('codigo_postal'),
                datos.get('telefono'),
                datos.get('celular'),
                datos.get('email'),
                datos.get('sitio_web'),
                datos.get('representante_legal_nombre'),
                datos.get('representante_legal_apellido'),
                datos.get('representante_legal_ci'),
                datos.get('representante_legal_cargo'),
                datos.get('actividad_economica_principal'),
                datos.get('horario_atencion'),
                datos.get('es_principal', False),
                datos.get('est_empresa', True),
                usuario
            ))
            id_empresa = cur.fetchone()[0]
            con.commit()
            return id_empresa
        except Exception as e:
            app.logger.error(f"Error al insertar empresa: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateEmpresa(self, id_empresa, datos, usuario=1):
        """Actualiza los datos de una empresa"""
        sql = """
        UPDATE empresa
        SET 
            razon_social = %s,
            nombre_comercial = %s,
            tipo_contribuyente = %s,
            departamento = %s,
            distrito = %s,
            ciudad = %s,
            direccion = %s,
            numero_casa = %s,
            codigo_postal = %s,
            telefono = %s,
            celular = %s,
            email = %s,
            sitio_web = %s,
            representante_legal_nombre = %s,
            representante_legal_apellido = %s,
            representante_legal_ci = %s,
            representante_legal_cargo = %s,
            actividad_economica_principal = %s,
            horario_atencion = %s,
            est_empresa = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME,
            modificacion_usuario = %s
        WHERE id_empresa = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('razon_social'),
                datos.get('nombre_comercial'),
                datos.get('tipo_contribuyente', 'persona_juridica'),
                datos.get('departamento'),
                datos.get('distrito'),
                datos.get('ciudad'),
                datos.get('direccion'),
                datos.get('numero_casa'),
                datos.get('codigo_postal'),
                datos.get('telefono'),
                datos.get('celular'),
                datos.get('email'),
                datos.get('sitio_web'),
                datos.get('representante_legal_nombre'),
                datos.get('representante_legal_apellido'),
                datos.get('representante_legal_ci'),
                datos.get('representante_legal_cargo'),
                datos.get('actividad_economica_principal'),
                datos.get('horario_atencion'),
                datos.get('est_empresa', True),
                usuario,
                id_empresa
            ))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar empresa: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEmpresa(self, id_empresa):
        """
        Elimina una empresa (solo si no tiene relaciones)
        Retorna True si se eliminó, False si no se pudo, "en_uso" si está en uso
        """
        # Verificar si tiene sedes asociadas
        sql_check = "SELECT COUNT(*) FROM sedes WHERE id_empresa = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (id_empresa,))
            if cur.fetchone()[0] > 0:
                return "en_uso"
            
            sql = "DELETE FROM empresa WHERE id_empresa = %s"
            cur.execute(sql, (id_empresa,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar empresa: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateLogo(self, id_empresa, logo_path):
        """Actualiza la ruta del logo de la empresa"""
        sql = """
        UPDATE empresa
        SET
            logo_path = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME
        WHERE id_empresa = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (logo_path, id_empresa))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar logo: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def actualizarCertificadoDigital(self, id_empresa, path, password_encrypted, serial=None, fecha_vencimiento=None):
        """Actualiza la información del certificado digital"""
        sql = """
        UPDATE empresa
        SET 
            certificado_firma_digital_path = %s,
            certificado_firma_digital_password_encrypted = %s,
            certificado_firma_digital_serial = %s,
            certificado_firma_digital_fecha_vencimiento = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME
        WHERE id_empresa = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (path, password_encrypted, serial, fecha_vencimiento, id_empresa))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar certificado: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
