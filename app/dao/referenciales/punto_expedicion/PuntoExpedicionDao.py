from flask import current_app as app
from app.conexion.Conexion import Conexion

class PuntoExpedicionDao:
    """
    DAO para gestión de puntos de expedición
    Puntos de expedición dentro de un establecimiento (Caja 1, Consultorios, etc.)
    """

    # ============================
    # OBTENER
    # ============================

    def getPuntosExpedicion(self, id_establecimiento=None):
        """Obtiene todos los puntos de expedición, opcionalmente filtrados por establecimiento"""
        if id_establecimiento:
            sql = """
            SELECT 
                p.id_punto_expedicion, p.id_establecimiento, p.codigo_punto_expedicion,
                p.nombre_punto_expedicion, p.descripcion, p.tipo_punto, 
                p.permite_facturacion, p.est_punto_expedicion, e.nombre_establecimiento,
                e.codigo_establecimiento
            FROM puntos_expedicion p
            JOIN establecimientos e ON p.id_establecimiento = e.id_establecimiento
            WHERE p.id_establecimiento = %s
            ORDER BY p.codigo_punto_expedicion
            """
            params = (id_establecimiento,)
        else:
            sql = """
            SELECT 
                p.id_punto_expedicion, p.id_establecimiento, p.codigo_punto_expedicion,
                p.nombre_punto_expedicion, p.descripcion, p.tipo_punto, 
                p.permite_facturacion, p.est_punto_expedicion, e.nombre_establecimiento,
                e.codigo_establecimiento
            FROM puntos_expedicion p
            JOIN establecimientos e ON p.id_establecimiento = e.id_establecimiento
            ORDER BY e.nombre_establecimiento, p.codigo_punto_expedicion
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
            puntos = cur.fetchall()
            return [{
                'id': p[0],
                'id_establecimiento': p[1],
                'codigo_punto_expedicion': p[2],
                'nombre_punto_expedicion': p[3],
                'descripcion': p[4],
                'tipo_punto': p[5],
                'permite_facturacion': p[6],
                'estado': p[7],
                'establecimiento': p[8],
                'codigo_establecimiento': p[9] if len(p) > 9 else None
            } for p in puntos]
        except Exception as e:
            app.logger.error(f"Error al obtener puntos de expedición: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getPuntoExpedicionById(self, id_punto_expedicion):
        """Obtiene un punto de expedición por ID"""
        sql = """
        SELECT 
            id_punto_expedicion, id_establecimiento, codigo_punto_expedicion,
            nombre_punto_expedicion, descripcion, tipo_punto, permite_facturacion,
            ultimo_numero_usado, serie_actual, est_punto_expedicion
        FROM puntos_expedicion
        WHERE id_punto_expedicion = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_punto_expedicion,))
            p = cur.fetchone()
            if p:
                return {
                    'id': p[0],
                    'id_establecimiento': p[1],
                    'codigo_punto_expedicion': p[2],
                    'nombre_punto_expedicion': p[3],
                    'descripcion': p[4],
                    'tipo_punto': p[5],
                    'permite_facturacion': p[6],
                    'ultimo_numero_usado': p[7],
                    'serie_actual': p[8],
                    'estado': p[9]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener punto de expedición: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def getPuntosExpedicionPorEstablecimiento(self, id_establecimiento):
        """Obtiene todos los puntos de expedición de un establecimiento"""
        return self.getPuntosExpedicion(id_establecimiento)

    def getProximoNumero(self, id_punto_expedicion):
        """Obtiene el próximo número disponible para un punto de expedición"""
        sql = """
        SELECT ultimo_numero_usado, serie_actual
        FROM puntos_expedicion
        WHERE id_punto_expedicion = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_punto_expedicion,))
            p = cur.fetchone()
            if p:
                siguiente = p[0] + 1
                return {
                    'proximo_numero': siguiente,
                    'serie_actual': p[1],
                    'ultimo_numero_usado': p[0]
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener próximo número: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    # ============================
    # VALIDACIONES
    # ============================

    def puntoExpedicionExiste(self, codigo_punto_expedicion, id_establecimiento):
        """Verifica si ya existe un punto de expedición con el mismo código en el establecimiento"""
        sql = "SELECT 1 FROM puntos_expedicion WHERE codigo_punto_expedicion = %s AND id_establecimiento = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (codigo_punto_expedicion, id_establecimiento))
            return cur.fetchone() is not None
        finally:
            cur.close()
            con.close()

    # ============================
    # CRUD
    # ============================

    def guardarPuntoExpedicion(self, datos, usuario=1):
        """Guarda un nuevo punto de expedición"""
        if not datos.get('id_establecimiento') or not datos.get('nombre_punto_expedicion'):
            app.logger.warning("ID establecimiento y nombre son obligatorios")
            return False
        
        # Validar código (debe ser de 3 dígitos)
        codigo = datos.get('codigo_punto_expedicion')
        if codigo and len(codigo) != 3:
            app.logger.warning("El código de punto de expedición debe tener 3 dígitos")
            return False
        
        if codigo and self.puntoExpedicionExiste(codigo, datos['id_establecimiento']):
            app.logger.warning("Ya existe un punto de expedición con este código en el establecimiento")
            return False

        sql = """
        INSERT INTO puntos_expedicion (
            id_establecimiento, codigo_punto_expedicion, nombre_punto_expedicion,
            descripcion, tipo_punto, permite_facturacion,
            ultimo_numero_usado, serie_actual, est_punto_expedicion, creacion_usuario
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id_punto_expedicion
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                datos.get('id_establecimiento'),
                codigo,
                datos.get('nombre_punto_expedicion'),
                datos.get('descripcion'),
                datos.get('tipo_punto', 'caja'),
                datos.get('permite_facturacion', True),
                datos.get('ultimo_numero_usado', 0),
                datos.get('serie_actual'),
                datos.get('est_punto_expedicion', True),
                usuario
            ))
            id_punto_expedicion = cur.fetchone()[0]
            con.commit()
            return id_punto_expedicion
        except Exception as e:
            app.logger.error(f"Error al insertar punto de expedición: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updatePuntoExpedicion(self, id_punto_expedicion, datos, usuario=1):
        """Actualiza los datos de un punto de expedición"""
        # Validar código si se proporciona
        codigo = datos.get('codigo_punto_expedicion')
        if codigo and len(codigo) != 3:
            app.logger.warning("El código de punto de expedición debe tener 3 dígitos")
            return False
        
        sql = """
        UPDATE puntos_expedicion
        SET 
            codigo_punto_expedicion = %s,
            nombre_punto_expedicion = %s,
            descripcion = %s,
            tipo_punto = %s,
            permite_facturacion = %s,
            est_punto_expedicion = %s,
            modificacion_fecha = CURRENT_DATE,
            modificacion_hora = CURRENT_TIME,
            modificacion_usuario = %s
        WHERE id_punto_expedicion = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (
                codigo,
                datos.get('nombre_punto_expedicion'),
                datos.get('descripcion'),
                datos.get('tipo_punto', 'caja'),
                datos.get('permite_facturacion', True),
                datos.get('est_punto_expedicion', True),
                usuario,
                id_punto_expedicion
            ))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar punto de expedición: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deletePuntoExpedicion(self, id_punto_expedicion):
        """
        Elimina un punto de expedición (solo si no tiene relaciones)
        Retorna True si se eliminó, False si no se pudo, "en_uso" si está en uso
        """
        # Verificar si tiene facturas asociadas
        sql_check = "SELECT COUNT(*) FROM facturas WHERE id_punto_expedicion = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql_check, (id_punto_expedicion,))
            if cur.fetchone()[0] > 0:
                return "en_uso"
            
            sql = "DELETE FROM puntos_expedicion WHERE id_punto_expedicion = %s"
            cur.execute(sql, (id_punto_expedicion,))
            filas = cur.rowcount
            con.commit()
            return filas > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar punto de expedición: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
