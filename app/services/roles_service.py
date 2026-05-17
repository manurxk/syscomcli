"""
Servicio para gestión de roles múltiples y validaciones de permisos
"""
from flask import session, current_app as app
from app.conexion.Conexion import Conexion
from app.auth.dao.user_dao import UsuarioDao


class RolesService:
    """Servicio para gestión de roles y permisos"""
    
    def __init__(self):
        self.usuario_dao = UsuarioDao()
    
    def puede_crear_usuario(self, id_usuario_actual=None) -> bool:
        """
        Verifica si el usuario puede crear nuevos usuarios
        Solo Superadministrador puede crear usuarios
        
        Args:
            id_usuario_actual: ID del usuario actual (opcional, usa session si no se proporciona)
        
        Returns:
            bool: True si puede crear usuarios, False en caso contrario
        """
        if id_usuario_actual is None:
            id_grupo = session.get('id_grupo')
        else:
            # Obtener id_grupo del usuario actual
            usuario = self.usuario_dao.getUsuarioById(id_usuario_actual)
            if not usuario:
                return False
            id_grupo = usuario.get('id_grupo')
        
        return self.es_superadmin(id_grupo)
    
    def puede_asignar_rol(self, id_usuario_actual, id_grupo_a_asignar) -> bool:
        """
        Verifica si el usuario puede asignar un rol específico
        
        Args:
            id_usuario_actual: ID del usuario que intenta asignar el rol
            id_grupo_a_asignar: ID del grupo/rol que se quiere asignar
        
        Returns:
            bool: True si puede asignar el rol, False en caso contrario
        """
        id_grupo_actual = session.get('id_grupo')
        
        # Superadmin puede asignar cualquier rol
        if self.es_superadmin(id_grupo_actual):
            return True
        
        # Admin solo puede asignar roles operativos
        if self.es_admin(id_grupo_actual):
            grupos_operativos = self.obtener_ids_grupos_operativos()
            return id_grupo_a_asignar in grupos_operativos
        
        return False
    
    def obtener_roles_permitidos(self, id_usuario_actual=None) -> list:
        """
        Obtiene lista de IDs de grupos que el usuario puede asignar
        EXCLUYE Administrador y Superadministrador para usuarios que no sean Superadmin
        
        Args:
            id_usuario_actual: ID del usuario actual (opcional)
        
        Returns:
            list: Lista de diccionarios con id_grupo y des_grupo
        """
        if id_usuario_actual is None:
            id_grupo = session.get('id_grupo')
            if not id_grupo:
                app.logger.warning("No se encontró id_grupo en la sesión")
                return []
        else:
            usuario = self.usuario_dao.getUsuarioById(id_usuario_actual)
            if not usuario:
                app.logger.warning(f"No se encontró usuario con ID {id_usuario_actual}")
                return []
            id_grupo = usuario.get('id_grupo')
        
        if not id_grupo:
            app.logger.warning("id_grupo es None o vacío")
            return []
        
        # Superadmin: todos los grupos (incluyendo Administrador y Superadministrador)
        if self.es_superadmin(id_grupo):
            app.logger.info(f"Usuario es Superadmin, devolviendo todos los grupos")
            return self.obtener_todos_los_grupos()
        
        # Admin: solo grupos operativos (EXCLUYE Administrador y Superadministrador)
        if self.es_admin(id_grupo):
            app.logger.info(f"Usuario es Admin, devolviendo solo grupos operativos")
            grupos_operativos = self.obtener_grupos_operativos()
            # Validación adicional: filtrar explícitamente Administrador y Superadministrador
            grupos_filtrados = [
                g for g in grupos_operativos 
                if g['des_grupo'].lower() not in ['administrador', 'superadministrador']
            ]
            return grupos_filtrados
        
        # Otros roles: no pueden asignar grupos
        app.logger.info(f"Usuario con id_grupo {id_grupo} no tiene permisos para asignar grupos")
        return []
    
    def obtener_ids_grupos_operativos(self) -> list:
        """
        Obtiene solo los IDs de grupos operativos (Recepcionista, Especialista, Ventas)
        
        Returns:
            list: Lista de IDs de grupos operativos
        """
        grupos = self.obtener_grupos_operativos()
        return [g['id_grupo'] for g in grupos]
    
    def obtener_grupos_operativos(self) -> list:
        """
        Obtiene grupos operativos (Recepcionista, Especialista, Ventas) con sus datos
        EXCLUYE explícitamente Administrador y Superadministrador
        
        Returns:
            list: Lista de diccionarios con id_grupo y des_grupo
        """
        sql = """
            SELECT id_grupo, des_grupo
            FROM grupos
            WHERE LOWER(des_grupo) IN ('recepcionista', 'especialista', 'ventas')
            AND LOWER(des_grupo) NOT IN ('administrador', 'superadministrador')
            AND est_grupo = TRUE
            ORDER BY des_grupo
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            grupos = cur.fetchall()
            
            return [{
                'id_grupo': g[0],
                'des_grupo': g[1]
            } for g in grupos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener grupos operativos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def obtener_todos_los_grupos(self) -> list:
        """
        Obtiene todos los grupos activos con sus datos
        
        Returns:
            list: Lista de diccionarios con id_grupo y des_grupo
        """
        sql = """
            SELECT id_grupo, des_grupo
            FROM grupos
            WHERE est_grupo = TRUE
            ORDER BY 
                CASE 
                    WHEN LOWER(des_grupo) = 'superadministrador' THEN 1
                    WHEN LOWER(des_grupo) = 'administrador' THEN 2
                    ELSE 3
                END,
                des_grupo
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            grupos = cur.fetchall()
            
            return [{
                'id_grupo': g[0],
                'des_grupo': g[1]
            } for g in grupos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los grupos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def es_superadmin(self, id_grupo) -> bool:
        """
        Verifica si un grupo es Superadministrador
        
        Args:
            id_grupo: ID del grupo a verificar
        
        Returns:
            bool: True si es Superadministrador, False en caso contrario
        """
        if id_grupo is None:
            return False
        
        sql = """
            SELECT COUNT(*) 
            FROM grupos
            WHERE id_grupo = %s 
            AND LOWER(des_grupo) = 'superadministrador'
            AND est_grupo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_grupo,))
            resultado = cur.fetchone()
            return resultado[0] > 0 if resultado else False
            
        except Exception as e:
            app.logger.error(f"Error al verificar Superadministrador: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def es_admin(self, id_grupo) -> bool:
        """
        Verifica si un grupo es Administrador
        
        Args:
            id_grupo: ID del grupo a verificar
        
        Returns:
            bool: True si es Administrador, False en caso contrario
        """
        if id_grupo is None:
            return False
        
        sql = """
            SELECT COUNT(*) 
            FROM grupos
            WHERE id_grupo = %s 
            AND LOWER(des_grupo) = 'administrador'
            AND est_grupo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_grupo,))
            resultado = cur.fetchone()
            return resultado[0] > 0 if resultado else False
            
        except Exception as e:
            app.logger.error(f"Error al verificar Administrador: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def obtener_id_grupo_superadmin(self) -> int:
        """
        Obtiene el ID del grupo Superadministrador
        
        Returns:
            int: ID del grupo Superadministrador, None si no existe
        """
        sql = """
            SELECT id_grupo
            FROM grupos
            WHERE LOWER(des_grupo) = 'superadministrador'
            AND est_grupo = TRUE
            LIMIT 1
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            resultado = cur.fetchone()
            return resultado[0] if resultado else None
            
        except Exception as e:
            app.logger.error(f"Error al obtener ID de Superadministrador: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def obtener_id_grupo_admin(self) -> int:
        """
        Obtiene el ID del grupo Administrador
        
        Returns:
            int: ID del grupo Administrador, None si no existe
        """
        sql = """
            SELECT id_grupo
            FROM grupos
            WHERE LOWER(des_grupo) = 'administrador'
            AND est_grupo = TRUE
            LIMIT 1
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql)
            resultado = cur.fetchone()
            return resultado[0] if resultado else None
            
        except Exception as e:
            app.logger.error(f"Error al obtener ID de Administrador: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()


