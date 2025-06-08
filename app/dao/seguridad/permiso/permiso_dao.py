# app/dao/seguridad/seguridad_dao.py

from flask import current_app as app
from app.conexion.Conexion import Conexion

class SeguridadDao:

    # --- USUARIOS ---

    def getUsuarios(self):
        query = """
        SELECT usu_id, usu_nick, usu_clave, usu_estado
        FROM usuarios
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            usuarios = cur.fetchall()
            return [{'usu_id': u[0], 'usu_nick': u[1], 'clave': u[2], 'estado': u[3]} for u in usuarios]
        except Exception as e:
            app.logger.error(f"Error al obtener usuarios: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # --- GRUPOS ---

    def getGrupos(self):
        query = "SELECT grupo_id, nombre FROM grupos"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            grupos = cur.fetchall()
            return [{'grupo_id': g[0], 'nombre': g[1]} for g in grupos]
        except Exception as e:
            app.logger.error(f"Error al obtener grupos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # --- PÁGINAS ---

    def getPaginas(self):
        query = "SELECT pagina_id, nombre, ruta FROM paginas"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query)
            paginas = cur.fetchall()
            return [{'pagina_id': p[0], 'nombre': p[1], 'ruta': p[2]} for p in paginas]
        except Exception as e:
            app.logger.error(f"Error al obtener páginas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    # --- PERMISOS ---

    def getPermisosPorGrupo(self, grupo_id):
        query = """
        SELECT p.pagina_id, pag.nombre, pag.ruta
        FROM permisos p
        JOIN paginas pag ON pag.pagina_id = p.pagina_id
        WHERE p.grupo_id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (grupo_id,))
            permisos = cur.fetchall()
            return [{'pagina_id': r[0], 'nombre': r[1], 'ruta': r[2]} for r in permisos]
        except Exception as e:
            app.logger.error(f"Error al obtener permisos por grupo: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def asignarPermisoAGrupo(self, grupo_id, pagina_id):
        query = """
        INSERT INTO permisos (grupo_id, pagina_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (grupo_id, pagina_id))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al asignar permiso: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def eliminarPermisoAGrupo(self, grupo_id, pagina_id):
        query = """
        DELETE FROM permisos WHERE grupo_id = %s AND pagina_id = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(query, (grupo_id, pagina_id))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar permiso: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()


