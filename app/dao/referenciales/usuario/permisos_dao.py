"""
DAO para gestionar permisos de usuarios según su grupo
app/dao/referenciales/usuario/permisos_dao.py
"""
from app.conexion.Conexion import Conexion


class PermisosDao:
    
    def obtener_permisos_grupo(self, id_grupo):
        """
        Obtiene todos los permisos de un grupo específico
        
        Returns:
            list: Lista de diccionarios con permisos por página
        """
        permisoSQL = """
            SELECT 
                p.id_pagina,
                p.id_grupo,
                pg.des_pagina,
                pg.pag_direcc,
                m.des_modulo,
                m.id_modulo,
                p.leer,
                p.insertar,
                p.editar,
                p.borrar
            FROM permisos p
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
            WHERE p.id_grupo = %s 
            AND pg.est_pagina = TRUE
            AND m.est_modulo = TRUE
            ORDER BY m.des_modulo, pg.des_pagina
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(permisoSQL, (id_grupo,))
            permisos = cur.fetchall()
            
            lista_permisos = []
            for permiso in permisos:
                diccionario = {
                    'id_pagina': permiso[0],
                    'id_grupo': permiso[1],
                    'des_pagina': permiso[2],
                    'pag_direcc': permiso[3],
                    'des_modulo': permiso[4],
                    'id_modulo': permiso[5],
                    'leer': permiso[6],
                    'insertar': permiso[7],
                    'editar': permiso[8],
                    'borrar': permiso[9]
                }
                lista_permisos.append(diccionario)
            
            return lista_permisos
            
        except Exception as e:
            print(f"Error al obtener permisos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    
    def verificar_permiso_ruta(self, id_grupo, ruta, accion='leer'):
        """
        Verifica si un grupo tiene permiso para realizar una acción en una ruta
        
        Args:
            id_grupo (int): ID del grupo del usuario
            ruta (str): Ruta/dirección de la página (ej: '/modulos/paciente/paciente-index')
            accion (str): 'leer', 'insertar', 'editar', 'borrar'
        
        Returns:
            bool: True si tiene permiso, False si no
        """
        # Normalizar ruta (quitar parámetros y trailing slash)
        ruta_limpia = ruta.split('?')[0].rstrip('/')
        
        permisoSQL = f"""
            SELECT p.{accion}
            FROM permisos p
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            WHERE p.id_grupo = %s 
            AND pg.pag_direcc = %s
            AND pg.est_pagina = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(permisoSQL, (id_grupo, ruta_limpia))
            resultado = cur.fetchone()
            
            if resultado:
                return resultado[0]  # Retorna el valor del campo (True/False)
            return False
            
        except Exception as e:
            print(f"Error al verificar permiso: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    
    def verificar_permiso_modulo(self, id_grupo, nombre_modulo):
        """
        Verifica si un grupo tiene acceso a alguna página de un módulo
        
        Returns:
            bool: True si tiene al menos un permiso de lectura en el módulo
        """
        permisoSQL = """
            SELECT COUNT(*) 
            FROM permisos p
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
            WHERE p.id_grupo = %s 
            AND m.des_modulo = %s
            AND p.leer = TRUE
            AND pg.est_pagina = TRUE
            AND m.est_modulo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(permisoSQL, (id_grupo, nombre_modulo))
            resultado = cur.fetchone()
            return resultado[0] > 0 if resultado else False
            
        except Exception as e:
            print(f"Error al verificar módulo: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    
    def obtener_modulos_permitidos(self, id_grupo):
        """
        Obtiene lista de módulos a los que el grupo tiene acceso
        
        Returns:
            list: Lista de módulos con al menos un permiso de lectura
        """
        modulosSQL = """
            SELECT DISTINCT 
                m.id_modulo,
                m.des_modulo
            FROM permisos p
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
            WHERE p.id_grupo = %s 
            AND p.leer = TRUE
            AND pg.est_pagina = TRUE
            AND m.est_modulo = TRUE
            ORDER BY m.des_modulo
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(modulosSQL, (id_grupo,))
            modulos = cur.fetchall()
            
            lista_modulos = []
            for modulo in modulos:
                diccionario = {
                    'id_modulo': modulo[0],
                    'des_modulo': modulo[1]
                }
                lista_modulos.append(diccionario)
            
            return lista_modulos
            
        except Exception as e:
            print(f"Error al obtener módulos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    
    def obtener_paginas_por_modulo(self, id_grupo, id_modulo):
        """
        Obtiene páginas específicas de un módulo que el usuario puede acceder
        
        Returns:
            list: Lista de páginas con permisos
        """
        paginasSQL = """
            SELECT 
                pg.id_pagina,
                pg.des_pagina,
                pg.pag_direcc,
                p.leer,
                p.insertar,
                p.editar,
                p.borrar
            FROM permisos p
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            WHERE p.id_grupo = %s 
            AND pg.id_modulo = %s
            AND p.leer = TRUE
            AND pg.est_pagina = TRUE
            ORDER BY pg.des_pagina
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(paginasSQL, (id_grupo, id_modulo))
            paginas = cur.fetchall()
            
            lista_paginas = []
            for pagina in paginas:
                diccionario = {
                    'id_pagina': pagina[0],
                    'des_pagina': pagina[1],
                    'pag_direcc': pagina[2],
                    'leer': pagina[3],
                    'insertar': pagina[4],
                    'editar': pagina[5],
                    'borrar': pagina[6]
                }
                lista_paginas.append(diccionario)
            
            return lista_paginas
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    
    def es_administrador(self, id_grupo):
        """
        Verifica si el grupo es Administrador (id_grupo = 1)
        """
        grupoSQL = """
            SELECT des_grupo 
            FROM grupos 
            WHERE id_grupo = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(grupoSQL, (id_grupo,))
            resultado = cur.fetchone()
            
            if resultado:
                return resultado[0].upper() == 'ADMINISTRADOR'
            return False
            
        except Exception as e:
            print(f"Error: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def es_superadministrador(self, id_grupo):
        """
        Verifica si el grupo es Superadministrador
        
        Args:
            id_grupo: ID del grupo a verificar
        
        Returns:
            bool: True si es Superadministrador, False en caso contrario
        """
        if id_grupo is None:
            return False
        
        grupoSQL = """
            SELECT des_grupo 
            FROM grupos 
            WHERE id_grupo = %s AND est_grupo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(grupoSQL, (id_grupo,))
            resultado = cur.fetchone()
            
            if resultado:
                return resultado[0].upper() == 'SUPERADMINISTRADOR'
            return False
            
        except Exception as e:
            print(f"Error al verificar Superadministrador: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def obtener_permisos_usuario(self, id_usuario):
        """
        Obtiene todos los permisos de un usuario considerando sus roles múltiples
        Los permisos se combinan con UNION (si tiene permiso en cualquier rol, tiene permiso)
        
        Args:
            id_usuario: ID del usuario
        
        Returns:
            list: Lista de diccionarios con permisos por página
        """
        permisoSQL = """
            SELECT DISTINCT
                p.id_pagina,
                pg.des_pagina,
                pg.pag_direcc,
                m.des_modulo,
                m.id_modulo,
                BOOL_OR(p.leer) AS leer,
                BOOL_OR(p.insertar) AS insertar,
                BOOL_OR(p.editar) AS editar,
                BOOL_OR(p.borrar) AS borrar
            FROM usuarios_roles ur
            INNER JOIN permisos p ON ur.id_grupo = p.id_grupo
            INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
            INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
            WHERE ur.id_usuario = %s
            AND ur.activo = TRUE
            AND pg.est_pagina = TRUE
            AND m.est_modulo = TRUE
            GROUP BY p.id_pagina, pg.des_pagina, pg.pag_direcc, m.des_modulo, m.id_modulo
            ORDER BY m.des_modulo, pg.des_pagina
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(permisoSQL, (id_usuario,))
            permisos = cur.fetchall()
            
            lista_permisos = []
            for permiso in permisos:
                diccionario = {
                    'id_pagina': permiso[0],
                    'des_pagina': permiso[1],
                    'pag_direcc': permiso[2],
                    'des_modulo': permiso[3],
                    'id_modulo': permiso[4],
                    'leer': permiso[5],
                    'insertar': permiso[6],
                    'editar': permiso[7],
                    'borrar': permiso[8]
                }
                lista_permisos.append(diccionario)
            
            return lista_permisos
            
        except Exception as e:
            print(f"Error al obtener permisos del usuario: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()