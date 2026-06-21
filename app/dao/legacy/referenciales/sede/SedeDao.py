from flask import current_app as app
from app.conexion.Conexion import Conexion

class SedeDao:

    # ============================
    # OBTENER
    # ============================

    def getSedes(self, id_empresa=None):
        """Obtiene todas las sedes, opcionalmente filtradas por empresa"""
        if id_empresa:
            sql = """
            SELECT 
                s.id_sede, s.id_empresa, s.des_sede, s.codigo_sede,
                s.direccion, s.ciudad, s.departamento, s.telefono, s.email,
                s.es_principal, s.est_sede, e.razon_social
            FROM sedes s
            JOIN empresa e ON s.id_empresa = e.id_empresa
            WHERE s.id_empresa = %s
            ORDER BY s.es_principal DESC, s.des_sede
            """
            params = (id_empresa,)
        else:
            sql = """
            SELECT 
                s.id_sede, s.id_empresa, s.des_sede, s.codigo_sede,
                s.direccion, s.ciudad, s.departamento, s.telefono, s.email,
                s.es_principal, s.est_sede, e.razon_social
            FROM sedes s
            JOIN empresa e ON s.id_empresa = e.id_empresa
            ORDER BY e.razon_social, s.es_principal DESC, s.des_sede
            """
            params = None
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            if params:
                cur.execute(sql, params)
            else:
                cur.execute(sql)
            sedes = cur.fetchall()
            return [{
                'id': s[0],
                'id_empresa': s[1],
                'descripcion': s[2],
                'codigo_sede': s[3],
                'direccion': s[4],
                'ciudad': s[5],
                'departamento': s[6],
                'telefono': s[7],
                'email': s[8],
                'es_principal': s[9],
                'estado': s[10],
                'empresa': s[11]
            } for s in sedes]
        except Exception as e:
            app.logger.error(f"Error al obtener sedes: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getSedeById(self, id_sede):
        """Obtiene una sede por ID"""
        sql = """
        SELECT 
            id_sede, id_empresa, des_sede, codigo_sede,
            direccion, ciudad, departamento, codigo_postal,
            latitud, longitud, telefono, email, horario_atencion,
            es_principal, est_sede
        FROM sedes
        WHERE id_sede = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_sede,))
            s = cur.fetchone()
            if s:
                return {
                    'id': s[0],
                    'id_empresa': s[1],
                    'descripcion': s[2],
                    'codigo_sede': s[3],
                    'direccion': s[4],
                    'ciudad': s[5],
                    'departamento': s[6],
                    'codigo_postal': s[7],
                    'latitud': float(s[8]) if s[8] else None,
                    'longitud': float(s[9]) if s[9] else None,
                    'telefono': s[10],
                    'email': s[11],
                    'horario_atencion': s[12],
                    'es_principal': s[13],
                    'estado': s[14]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener sede: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getSedePrincipal(self, id_empresa):
        """Obtiene la sede principal de una empresa"""
        sql = """
        SELECT id_sede, des_sede, codigo_sede
        FROM sedes
        WHERE id_empresa = %s AND es_principal = TRUE AND est_sede = TRUE
        LIMIT 1
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_empresa,))
            s = cur.fetchone()
            if s:
                return {'id': s[0], 'descripcion': s[1], 'codigo_sede': s[2]}
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener sede principal: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getSedesPorEmpresa(self, id_empresa):
        """Obtiene todas las sedes de una empresa"""
        return self.getSedes(id_empresa)

    # ============================
    # VALIDACIONES
    # ============================

    def sedeExiste(self, codigo_sede, id_empresa):
        """Verifica si ya existe una sede con el mismo código en la empresa"""
        sql = "SELECT 1 FROM sedes WHERE codigo_sede = %s AND id_empresa = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (codigo_sede, id_empresa))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    # ============================
    # CRUD
    # ============================

    def guardarSede(self, datos, usuario=1):
        """Guarda una nueva sede"""
        if not datos.get('id_empresa') or not datos.get('des_sede'):
            app.logger.warning("ID empresa y descripción son obligatorios")
            return False
        
        if datos.get('codigo_sede') and self.sedeExiste(datos['codigo_sede'], datos['id_empresa']):
            app.logger.warning("Ya existe una sede con este código en la empresa")
            return False

        sql = """
        INSERT INTO sedes (
            id_empresa, des_sede, codigo_sede, direccion, ciudad, departamento,
            codigo_postal, latitud, longitud, telefono, email, horario_atencion,
            es_principal, est_sede, creacion_usuario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_sede
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('id_empresa'),
                datos.get('des_sede'),
                datos.get('codigo_sede'),
                datos.get('direccion'),
                datos.get('ciudad'),
                datos.get('departamento'),
                datos.get('codigo_postal'),
                datos.get('latitud'),
                datos.get('longitud'),
                datos.get('telefono'),
                datos.get('email'),
                datos.get('horario_atencion'),
                datos.get('es_principal', False),
                datos.get('est_sede', True),
                usuario
            ))
            id_sede = cur.fetchone()[0]
            con.commit()
            return id_sede
        except Exception as e:
            app.logger.error(f"Error al insertar sede: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateSede(self, id_sede, datos, usuario=1):
        """Actualiza los datos de una sede"""
        sql = """
        UPDATE sedes
        SET 
            des_sede = %s,
            codigo_sede = %s,
            direccion = %s,
            ciudad = %s,
            departamento = %s,
            codigo_postal = %s,
            latitud = %s,
            longitud = %s,
            telefono = %s,
            email = %s,
            horario_atencion = %s,
            es_principal = %s,
            est_sede = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME,
            modificacion_usuario = %s
        WHERE id_sede = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('des_sede'),
                datos.get('codigo_sede'),
                datos.get('direccion'),
                datos.get('ciudad'),
                datos.get('departamento'),
                datos.get('codigo_postal'),
                datos.get('latitud'),
                datos.get('longitud'),
                datos.get('telefono'),
                datos.get('email'),
                datos.get('horario_atencion'),
                datos.get('es_principal', False),
                datos.get('est_sede', True),
                usuario,
                id_sede
            ))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar sede: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteSede(self, id_sede):
        """
        Elimina una sede (solo si no tiene relaciones)
        Retorna True si se eliminó, False si no se pudo, "en_uso" si está en uso
        """
        # Verificar si tiene consultorios asociados
        sql_check = "SELECT COUNT(*) FROM consultorios WHERE id_sede = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (id_sede,))
            if cur.fetchone()[0] > 0:
                return "en_uso"
            
            sql = "DELETE FROM sedes WHERE id_sede = %s"
            cur.execute(sql, (id_sede,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar sede: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
