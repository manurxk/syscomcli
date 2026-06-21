from flask import current_app as app
from app.conexion.Conexion import Conexion
from werkzeug.security import generate_password_hash, check_password_hash

class UsuarioDao:
    
    def getUsuarios(self, id_usuario_filtro=None):
        """
        Obtiene todos los usuarios con sus datos relacionados y roles múltiples
        
        Args:
            id_usuario_filtro: ID del usuario actual para filtrar según permisos (opcional)
        
        Returns:
            list: Lista de usuarios con sus roles
        """
        usuariosSQL = """
            SELECT 
                u.id_usuario,
                u.usu_nick,
                u.usu_estado,
                u.usu_nro_intentos,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, 'Sin funcionario') AS funcionario,
                COALESCE(c.des_cargo, 'Sin cargo') AS cargo,
                COALESCE(g.des_grupo, 'Sin grupo') AS grupo,
                u.id_grupo AS id_grupo_principal,
                u.creacion_fecha,
                f.id_funcionario
            FROM usuarios u
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN cargos c ON f.id_cargo = c.id_cargo
            LEFT JOIN grupos g ON u.id_grupo = g.id_grupo
            ORDER BY u.id_usuario DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(usuariosSQL)
            usuarios = cur.fetchall()
            
            resultado = []
            for u in usuarios:
                id_usuario = u[0]
                
                # Obtener todos los roles activos del usuario
                roles = self.obtener_roles_usuario(id_usuario)
                rol_principal = next((r for r in roles if r['es_rol_principal']), None)
                roles_adicionales = [r for r in roles if not r['es_rol_principal']]
                
                # Construir lista de nombres de roles adicionales
                nombres_roles_adicionales = [r['des_grupo'] for r in roles_adicionales]
                
                usuario_data = {
                    'id_usuario': id_usuario,
                    'username': u[1],
                    'activo': u[2],
                    'intentos': u[3] if u[3] is not None else 0,
                    'funcionario': u[4] if u[4] else 'Sin funcionario',
                    'cargo': u[5] if u[5] else 'Sin cargo',
                    'grupo': rol_principal['des_grupo'] if rol_principal else (u[6] if u[6] else 'Sin grupo'),
                    'id_grupo_principal': rol_principal['id_grupo'] if rol_principal else (u[7] if u[7] else None),
                    'roles_adicionales': nombres_roles_adicionales,
                    'total_roles': len(roles),
                    'fecha_creacion': u[8].strftime('%d/%m/%Y') if u[8] else None,
                    'id_funcionario': u[9] if u[9] else None
                }
                
                resultado.append(usuario_data)
            
            app.logger.info(f"Se obtuvieron {len(resultado)} usuarios con roles múltiples")
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener usuarios: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()

    def getUsuarioById(self, id_usuario):
        """Obtiene un usuario específico por ID"""
        usuarioSQL = """
            SELECT 
                u.id_usuario,
                u.usu_nick,
                u.usu_estado,
                u.usu_nro_intentos,
                u.id_funcionario,
                u.id_grupo,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, 'Sin funcionario') AS funcionario,
                COALESCE(c.des_cargo, 'Sin cargo') AS cargo,
                COALESCE(g.des_grupo, 'Sin grupo') AS grupo
            FROM usuarios u
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN cargos c ON f.id_cargo = c.id_cargo
            LEFT JOIN grupos g ON u.id_grupo = g.id_grupo
            WHERE u.id_usuario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(usuarioSQL, (id_usuario,))
            u = cur.fetchone()
            
            if not u:
                app.logger.warning(f"Usuario con ID {id_usuario} no encontrado")
                return None
            
            return {
                'id_usuario': u[0],
                'username': u[1],
                'activo': u[2],
                'intentos': u[3] if u[3] is not None else 0,
                'id_funcionario': u[4],
                'id_grupo': u[5],
                'funcionario': u[6] if u[6] else 'Sin funcionario',
                'cargo': u[7] if u[7] else 'Sin cargo',
                'grupo': u[8] if u[8] else 'Sin grupo'
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener usuario por ID: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()

    def getFuncionariosSinUsuario(self):
        """Obtiene funcionarios que NO tienen usuario asignado"""
        funcionariosSQL = """
            SELECT 
                f.id_funcionario,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                c.des_cargo,
                p.per_cedula
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN cargos c ON f.id_cargo = c.id_cargo
            LEFT JOIN usuarios u ON f.id_funcionario = u.id_funcionario
            WHERE f.fun_estado = TRUE 
              AND u.id_usuario IS NULL
            ORDER BY p.per_nombre
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(funcionariosSQL)
            funcionarios = cur.fetchall()
            
            return [{
                'id_funcionario': f[0],
                'nombre_completo': f[1],
                'cargo': f[2],
                'cedula': f[3]
            } for f in funcionarios]
            
        except Exception as e:
            app.logger.error(f"Error al obtener funcionarios sin usuario: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def validarUsernameDisponible(self, username, id_usuario=None):
        """Valida que el username no esté en uso"""
        if id_usuario:
            sql = "SELECT id_usuario FROM usuarios WHERE usu_nick = %s AND id_usuario != %s"
            params = (username, id_usuario)
        else:
            sql = "SELECT id_usuario FROM usuarios WHERE usu_nick = %s"
            params = (username,)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, params)
            resultado = cur.fetchone()
            return resultado is None
            
        except Exception as e:
            app.logger.error(f"Error al validar username: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def guardarUsuario(self, username, password, id_funcionario, id_grupo, 
                       usu_estado=True, creacion_usuario=1):
        """Crea un nuevo usuario con contraseña encriptada"""
        
        # Validar que el username no exista
        if not self.validarUsernameDisponible(username):
            app.logger.error(f"El username {username} ya existe")
            return None
        
        # Validar que el funcionario no tenga usuario
        checkFuncionarioSQL = """
            SELECT id_usuario FROM usuarios WHERE id_funcionario = %s
        """
        
        insertUsuarioSQL = """
            INSERT INTO usuarios(usu_nick, usu_clave, id_funcionario, id_grupo, 
                               usu_estado, creacion_usuario, creacion_fecha, creacion_hora,
                               password_nunca_expira, requiere_cambio_password, fecha_cambio_password)
            VALUES(%s, %s, %s, %s, %s, %s, CURRENT_DATE, CURRENT_TIME, TRUE, FALSE, NOW())
            RETURNING id_usuario
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar que el funcionario no tenga usuario
            cur.execute(checkFuncionarioSQL, (id_funcionario,))
            if cur.fetchone():
                app.logger.error(f"El funcionario {id_funcionario} ya tiene un usuario asignado")
                return None
            
            # Encriptar contraseña usando pbkdf2:sha256 para mantener consistencia
            # Esto asegura que todos los hashes en la BD sean del mismo tipo
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            
            # Insertar usuario
            cur.execute(insertUsuarioSQL, (username, password_hash, id_funcionario, 
                                          id_grupo, usu_estado, creacion_usuario))
            usuario_id = cur.fetchone()[0]
            
            # Crear registro en usuarios_roles (rol principal)
            insertRolSQL = """
                INSERT INTO usuarios_roles (
                    id_usuario, id_grupo, es_rol_principal, activo, asignado_por
                )
                VALUES (%s, %s, TRUE, TRUE, %s)
            """
            cur.execute(insertRolSQL, (usuario_id, id_grupo, creacion_usuario))
            
            con.commit()
            app.logger.info(f"Usuario {username} creado exitosamente con ID: {usuario_id} y rol {id_grupo}")
            return usuario_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar usuario: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def updateUsuario(self, id_usuario, username, id_grupo, usu_estado, 
                     password=None, modificacion_usuario=1):
        """Actualiza un usuario existente (NO cambia el funcionario)"""
        
        # Validar username disponible
        if not self.validarUsernameDisponible(username, id_usuario):
            app.logger.error(f"El username {username} ya existe")
            return False
        
        # Obtener el rol principal actual
        rol_principal_actual = self.obtener_rol_principal(id_usuario)
        id_grupo_actual = rol_principal_actual['id_grupo'] if rol_principal_actual else None
        
        # Si hay contraseña, actualizar todo incluyendo contraseña
        if password:
            updateSQL = """
                UPDATE usuarios
                SET usu_nick = %s, 
                    usu_clave = %s,
                    id_grupo = %s, 
                    usu_estado = %s,
                    password_nunca_expira = TRUE,
                    requiere_cambio_password = FALSE,
                    fecha_cambio_password = NOW(),
                    modificacion_fecha = CURRENT_DATE,
                    modificacion_hora = CURRENT_TIME,
                    modificacion_usuario = %s
                WHERE id_usuario = %s
            """
            # Usar pbkdf2:sha256 para mantener consistencia con el resto del sistema
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            params = (username, password_hash, id_grupo, usu_estado, modificacion_usuario, id_usuario)
        else:
            # Sin contraseña, solo actualizar los demás campos
            updateSQL = """
                UPDATE usuarios
                SET usu_nick = %s, 
                    id_grupo = %s, 
                    usu_estado = %s,
                    modificacion_fecha = CURRENT_DATE,
                    modificacion_hora = CURRENT_TIME,
                    modificacion_usuario = %s
                WHERE id_usuario = %s
            """
            params = (username, id_grupo, usu_estado, modificacion_usuario, id_usuario)
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, params)
            
            # Si cambió el rol principal, actualizar usuarios_roles
            if id_grupo_actual != id_grupo:
                # Verificar si el nuevo rol ya está asignado
                checkRolSQL = """
                    SELECT id_usuario_rol
                    FROM usuarios_roles
                    WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
                """
                cur.execute(checkRolSQL, (id_usuario, id_grupo))
                rol_existente = cur.fetchone()
                
                if rol_existente:
                    # El rol ya existe, solo cambiar a principal
                    # Desmarcar todos los roles principales
                    updatePrincipalSQL = """
                        UPDATE usuarios_roles
                        SET es_rol_principal = FALSE
                        WHERE id_usuario = %s AND es_rol_principal = TRUE
                    """
                    cur.execute(updatePrincipalSQL, (id_usuario,))
                    
                    # Marcar el nuevo rol como principal
                    updateNuevoSQL = """
                        UPDATE usuarios_roles
                        SET es_rol_principal = TRUE
                        WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
                    """
                    cur.execute(updateNuevoSQL, (id_usuario, id_grupo))
                else:
                    # Asignar nuevo rol como principal
                    # Primero desmarcar otros roles principales
                    updatePrincipalSQL = """
                        UPDATE usuarios_roles
                        SET es_rol_principal = FALSE
                        WHERE id_usuario = %s AND es_rol_principal = TRUE
                    """
                    cur.execute(updatePrincipalSQL, (id_usuario,))
                    
                    # Insertar nuevo rol como principal
                    insertRolSQL = """
                        INSERT INTO usuarios_roles (
                            id_usuario, id_grupo, es_rol_principal, activo, asignado_por
                        )
                        VALUES (%s, %s, TRUE, TRUE, %s)
                    """
                    cur.execute(insertRolSQL, (id_usuario, id_grupo, modificacion_usuario))
            
            con.commit()
            app.logger.info(f"Usuario {id_usuario} actualizado exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar usuario: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def desactivarUsuario(self, id_usuario):
        """Desactiva un usuario (soft delete)"""
        desactivarSQL = """
            UPDATE usuarios
            SET usu_estado = FALSE,
                modificacion_fecha = CURRENT_DATE,
                modificacion_hora = CURRENT_TIME
            WHERE id_usuario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(desactivarSQL, (id_usuario,))
            con.commit()
            app.logger.info(f"Usuario {id_usuario} desactivado exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al desactivar usuario: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def resetearIntentos(self, id_usuario):
        """Resetea el contador de intentos fallidos de login"""
        resetSQL = """
            UPDATE usuarios
            SET usu_nro_intentos = 0,
                modificacion_fecha = CURRENT_DATE,
                modificacion_hora = CURRENT_TIME
            WHERE id_usuario = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(resetSQL, (id_usuario,))
            con.commit()
            app.logger.info(f"Intentos reseteados para usuario {id_usuario}")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al resetear intentos: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    # ============================================
    # MÉTODOS PARA ROLES MÚLTIPLES (usuarios_roles)
    # ============================================
    
    def obtener_roles_usuario(self, id_usuario):
        """
        Obtiene todos los roles activos de un usuario
        
        Args:
            id_usuario: ID del usuario
        
        Returns:
            list: Lista de diccionarios con información de roles
        """
        sql = """
            SELECT 
                ur.id_usuario_rol,
                ur.id_grupo,
                g.des_grupo,
                ur.es_rol_principal,
                ur.activo,
                ur.fecha_asignacion,
                ur.asignado_por,
                COALESCE(u2.usu_nick, 'SISTEMA') AS asignado_por_nombre
            FROM usuarios_roles ur
            INNER JOIN grupos g ON ur.id_grupo = g.id_grupo
            LEFT JOIN usuarios u2 ON ur.asignado_por = u2.id_usuario
            WHERE ur.id_usuario = %s AND ur.activo = TRUE
            ORDER BY ur.es_rol_principal DESC, ur.fecha_asignacion ASC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario,))
            roles = cur.fetchall()
            
            resultado = []
            for r in roles:
                resultado.append({
                    'id_usuario_rol': r[0],
                    'id_grupo': r[1],
                    'des_grupo': r[2],
                    'es_rol_principal': r[3],
                    'activo': r[4],
                    'fecha_asignacion': r[5].strftime('%d/%m/%Y %H:%M') if r[5] else None,
                    'asignado_por': r[6],
                    'asignado_por_nombre': r[7]
                })
            
            return resultado
            
        except Exception as e:
            app.logger.error(f"Error al obtener roles del usuario {id_usuario}: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def obtener_rol_principal(self, id_usuario):
        """
        Obtiene el rol principal de un usuario
        
        Args:
            id_usuario: ID del usuario
        
        Returns:
            dict: Diccionario con información del rol principal, None si no existe
        """
        sql = """
            SELECT 
                ur.id_grupo,
                g.des_grupo,
                ur.id_usuario_rol
            FROM usuarios_roles ur
            INNER JOIN grupos g ON ur.id_grupo = g.id_grupo
            WHERE ur.id_usuario = %s 
            AND ur.es_rol_principal = TRUE 
            AND ur.activo = TRUE
            LIMIT 1
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario,))
            resultado = cur.fetchone()
            
            if resultado:
                return {
                    'id_grupo': resultado[0],
                    'des_grupo': resultado[1],
                    'id_usuario_rol': resultado[2]
                }
            return None
            
        except Exception as e:
            app.logger.error(f"Error al obtener rol principal del usuario {id_usuario}: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def contar_roles_activos(self, id_usuario):
        """
        Cuenta cuántos roles activos tiene un usuario
        
        Args:
            id_usuario: ID del usuario
        
        Returns:
            int: Cantidad de roles activos
        """
        sql = """
            SELECT COUNT(*)
            FROM usuarios_roles
            WHERE id_usuario = %s AND activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(sql, (id_usuario,))
            resultado = cur.fetchone()
            return resultado[0] if resultado else 0
            
        except Exception as e:
            app.logger.error(f"Error al contar roles del usuario {id_usuario}: {str(e)}")
            return 0
        finally:
            cur.close()
            con.close()
    
    def asignar_rol_usuario(self, id_usuario, id_grupo, es_principal=False, asignado_por=None):
        """
        Asigna un rol a un usuario
        
        Args:
            id_usuario: ID del usuario
            id_grupo: ID del grupo/rol a asignar
            es_principal: Si es True, marca este rol como principal (y desmarca otros)
            asignado_por: ID del usuario que asigna el rol
        
        Returns:
            int: ID del registro creado, None si hay error
        """
        # Validar que no exceda 3 roles activos
        cantidad_roles = self.contar_roles_activos(id_usuario)
        if cantidad_roles >= 3:
            app.logger.warning(f"Usuario {id_usuario} ya tiene 3 roles activos (máximo permitido)")
            return None
        
        # Validar que el rol no esté ya asignado
        checkSQL = """
            SELECT id_usuario_rol
            FROM usuarios_roles
            WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
        """
        
        insertSQL = """
            INSERT INTO usuarios_roles (
                id_usuario, id_grupo, es_rol_principal, activo, asignado_por
            )
            VALUES (%s, %s, %s, TRUE, %s)
            RETURNING id_usuario_rol
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar si ya existe el rol asignado
            cur.execute(checkSQL, (id_usuario, id_grupo))
            if cur.fetchone():
                app.logger.warning(f"El usuario {id_usuario} ya tiene el rol {id_grupo} asignado")
                return None
            
            # Si es rol principal, desmarcar otros roles principales
            if es_principal:
                updateSQL = """
                    UPDATE usuarios_roles
                    SET es_rol_principal = FALSE
                    WHERE id_usuario = %s AND es_rol_principal = TRUE
                """
                cur.execute(updateSQL, (id_usuario,))
            
            # Insertar nuevo rol
            cur.execute(insertSQL, (id_usuario, id_grupo, es_principal, asignado_por))
            id_usuario_rol = cur.fetchone()[0]
            
            # Si es rol principal, actualizar también usuarios.id_grupo (compatibilidad)
            if es_principal:
                updateUsuarioSQL = """
                    UPDATE usuarios
                    SET id_grupo = %s
                    WHERE id_usuario = %s
                """
                cur.execute(updateUsuarioSQL, (id_grupo, id_usuario))
            
            con.commit()
            app.logger.info(f"Rol {id_grupo} asignado al usuario {id_usuario} exitosamente")
            return id_usuario_rol
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al asignar rol al usuario {id_usuario}: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def remover_rol_usuario(self, id_usuario, id_grupo):
        """
        Remueve un rol de un usuario (soft delete - marca como inactivo)
        
        Args:
            id_usuario: ID del usuario
            id_grupo: ID del grupo/rol a remover
        
        Returns:
            bool: True si se removió exitosamente, False en caso contrario
        """
        # Validar que no sea el único rol
        cantidad_roles = self.contar_roles_activos(id_usuario)
        if cantidad_roles <= 1:
            app.logger.warning(f"No se puede remover el único rol del usuario {id_usuario}")
            return False
        
        # Obtener información del rol a remover
        checkSQL = """
            SELECT es_rol_principal, id_usuario_rol
            FROM usuarios_roles
            WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
        """
        
        updateSQL = """
            UPDATE usuarios_roles
            SET activo = FALSE
            WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar que existe el rol
            cur.execute(checkSQL, (id_usuario, id_grupo))
            rol_info = cur.fetchone()
            
            if not rol_info:
                app.logger.warning(f"El usuario {id_usuario} no tiene el rol {id_grupo} asignado")
                return False
            
            es_principal = rol_info[0]
            
            # Si es el rol principal, asignar otro rol como principal
            if es_principal:
                # Buscar otro rol activo para hacerlo principal
                otro_rolSQL = """
                    SELECT id_grupo
                    FROM usuarios_roles
                    WHERE id_usuario = %s 
                    AND id_grupo != %s 
                    AND activo = TRUE
                    LIMIT 1
                """
                cur.execute(otro_rolSQL, (id_usuario, id_grupo))
                otro_rol = cur.fetchone()
                
                if otro_rol:
                    # Hacer el otro rol principal
                    updatePrincipalSQL = """
                        UPDATE usuarios_roles
                        SET es_rol_principal = TRUE
                        WHERE id_usuario = %s AND id_grupo = %s
                    """
                    cur.execute(updatePrincipalSQL, (id_usuario, otro_rol[0]))
                    
                    # Actualizar usuarios.id_grupo
                    updateUsuarioSQL = """
                        UPDATE usuarios
                        SET id_grupo = %s
                        WHERE id_usuario = %s
                    """
                    cur.execute(updateUsuarioSQL, (otro_rol[0], id_usuario))
            
            # Remover el rol (marcar como inactivo)
            cur.execute(updateSQL, (id_usuario, id_grupo))
            
            con.commit()
            app.logger.info(f"Rol {id_grupo} removido del usuario {id_usuario} exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al remover rol del usuario {id_usuario}: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def cambiar_rol_principal(self, id_usuario, nuevo_id_grupo_principal):
        """
        Cambia el rol principal de un usuario
        
        Args:
            id_usuario: ID del usuario
            nuevo_id_grupo_principal: ID del nuevo grupo/rol principal
        
        Returns:
            bool: True si se cambió exitosamente, False en caso contrario
        """
        # Verificar que el usuario tenga el rol asignado
        checkSQL = """
            SELECT id_usuario_rol
            FROM usuarios_roles
            WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
        """
        
        updateSQL = """
            UPDATE usuarios_roles
            SET es_rol_principal = FALSE
            WHERE id_usuario = %s AND es_rol_principal = TRUE
        """
        
        updateNuevoSQL = """
            UPDATE usuarios_roles
            SET es_rol_principal = TRUE
            WHERE id_usuario = %s AND id_grupo = %s AND activo = TRUE
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Verificar que el rol existe y está activo
            cur.execute(checkSQL, (id_usuario, nuevo_id_grupo_principal))
            if not cur.fetchone():
                app.logger.warning(f"El usuario {id_usuario} no tiene el rol {nuevo_id_grupo_principal} asignado")
                return False
            
            # Desmarcar todos los roles principales
            cur.execute(updateSQL, (id_usuario,))
            
            # Marcar el nuevo rol como principal
            cur.execute(updateNuevoSQL, (id_usuario, nuevo_id_grupo_principal))
            
            # Actualizar usuarios.id_grupo
            updateUsuarioSQL = """
                UPDATE usuarios
                SET id_grupo = %s
                WHERE id_usuario = %s
            """
            cur.execute(updateUsuarioSQL, (nuevo_id_grupo_principal, id_usuario))
            
            con.commit()
            app.logger.info(f"Rol principal cambiado a {nuevo_id_grupo_principal} para usuario {id_usuario}")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al cambiar rol principal del usuario {id_usuario}: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()