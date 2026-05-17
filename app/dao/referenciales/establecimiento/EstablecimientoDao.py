from flask import current_app as app
from app.conexion.Conexion import Conexion

class EstablecimientoDao:
    """
    DAO para gestión de establecimientos
    Establecimientos según numeración DNIT (001=matriz, 002=sucursal1, etc.)
    """

    # ============================
    # OBTENER
    # ============================

    def getEstablecimientos(self, id_sede=None):
        """Obtiene todos los establecimientos, opcionalmente filtrados por sede"""
        if id_sede:
            sql = """
            SELECT 
                e.id_establecimiento, e.id_sede, e.codigo_establecimiento, 
                e.nombre_establecimiento, e.descripcion, e.es_principal, 
                e.est_establecimiento, s.des_sede
            FROM establecimientos e
            JOIN sedes s ON e.id_sede = s.id_sede
            WHERE e.id_sede = %s
            ORDER BY e.es_principal DESC, e.codigo_establecimiento
            """
            params = (id_sede,)
        else:
            sql = """
            SELECT 
                e.id_establecimiento, e.id_sede, e.codigo_establecimiento, 
                e.nombre_establecimiento, e.descripcion, e.es_principal, 
                e.est_establecimiento, s.des_sede
            FROM establecimientos e
            JOIN sedes s ON e.id_sede = s.id_sede
            ORDER BY s.des_sede, e.es_principal DESC, e.codigo_establecimiento
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
            establecimientos = cur.fetchall()
            return [{
                'id': est[0],
                'id_sede': est[1],
                'codigo_establecimiento': est[2],
                'nombre_establecimiento': est[3],
                'descripcion': est[4],
                'es_principal': est[5],
                'estado': est[6],
                'sede': est[7]
            } for est in establecimientos]
        except Exception as e:
            app.logger.error(f"Error al obtener establecimientos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getEstablecimientoById(self, id_establecimiento):
        """Obtiene un establecimiento por ID"""
        sql = """
        SELECT 
            id_establecimiento, id_sede, codigo_establecimiento,
            nombre_establecimiento, descripcion, es_principal, est_establecimiento
        FROM establecimientos
        WHERE id_establecimiento = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_establecimiento,))
            est = cur.fetchone()
            if est:
                return {
                    'id': est[0],
                    'id_sede': est[1],
                    'codigo_establecimiento': est[2],
                    'nombre_establecimiento': est[3],
                    'descripcion': est[4],
                    'es_principal': est[5],
                    'estado': est[6]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener establecimiento: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getEstablecimientosPorSede(self, id_sede):
        """Obtiene todos los establecimientos de una sede"""
        return self.getEstablecimientos(id_sede)

    # ============================
    # VALIDACIONES
    # ============================

    def establecimientoExiste(self, codigo_establecimiento, id_sede):
        """Verifica si ya existe un establecimiento con el mismo código en la sede"""
        sql = "SELECT 1 FROM establecimientos WHERE codigo_establecimiento = %s AND id_sede = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (codigo_establecimiento, id_sede))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    # ============================
    # CRUD
    # ============================

    def guardarEstablecimiento(self, datos, usuario=1):
        """Guarda un nuevo establecimiento"""
        if not datos.get('id_sede') or not datos.get('nombre_establecimiento'):
            app.logger.warning("ID sede y nombre son obligatorios")
            return False
        
        # Validar código (debe ser de 3 dígitos)
        codigo = datos.get('codigo_establecimiento')
        if codigo and len(codigo) != 3:
            app.logger.warning("El código de establecimiento debe tener 3 dígitos")
            return False
        
        if codigo and self.establecimientoExiste(codigo, datos['id_sede']):
            app.logger.warning("Ya existe un establecimiento con este código en la sede")
            return False

        sql = """
        INSERT INTO establecimientos (
            id_sede, codigo_establecimiento, nombre_establecimiento,
            descripcion, es_principal, est_establecimiento, creacion_usuario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING id_establecimiento
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('id_sede'),
                codigo,
                datos.get('nombre_establecimiento'),
                datos.get('descripcion'),
                datos.get('es_principal', False),
                datos.get('est_establecimiento', True),
                usuario
            ))
            id_establecimiento = cur.fetchone()[0]
            con.commit()
            return id_establecimiento
        except Exception as e:
            app.logger.error(f"Error al insertar establecimiento: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateEstablecimiento(self, id_establecimiento, datos, usuario=1):
        """Actualiza los datos de un establecimiento"""
        # Validar código si se proporciona
        codigo = datos.get('codigo_establecimiento')
        if codigo and len(codigo) != 3:
            app.logger.warning("El código de establecimiento debe tener 3 dígitos")
            return False
        
        sql = """
        UPDATE establecimientos
        SET 
            codigo_establecimiento = %s,
            nombre_establecimiento = %s,
            descripcion = %s,
            es_principal = %s,
            est_establecimiento = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME,
            modificacion_usuario = %s
        WHERE id_establecimiento = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                codigo,
                datos.get('nombre_establecimiento'),
                datos.get('descripcion'),
                datos.get('es_principal', False),
                datos.get('est_establecimiento', True),
                usuario,
                id_establecimiento
            ))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar establecimiento: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteEstablecimiento(self, id_establecimiento):
        """
        Elimina un establecimiento (solo si no tiene relaciones)
        Retorna True si se eliminó, False si no se pudo, "en_uso" si está en uso
        """
        # Verificar si tiene puntos de expedición asociados
        sql_check = "SELECT COUNT(*) FROM puntos_expedicion WHERE id_establecimiento = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (id_establecimiento,))
            if cur.fetchone()[0] > 0:
                return "en_uso"
            
            sql = "DELETE FROM establecimientos WHERE id_establecimiento = %s"
            cur.execute(sql, (id_establecimiento,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar establecimiento: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
