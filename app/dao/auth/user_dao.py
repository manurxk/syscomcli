from app.core.base_dao import BaseDAO
from werkzeug.security import generate_password_hash

MAX_ROLES_POR_USUARIO = 3
# Tope de usuarios activos vinculados a funcionarios (el superadmin técnico sin funcionario no cuenta).
MAX_USUARIOS_CON_FUNCIONARIO = 10


class UsuarioDao(BaseDAO):
    """Acceso a datos de usuarios, sus roles y la autenticación."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getUsuarios(self):
        """Lista todos los usuarios con su rol principal y datos de funcionario."""
        sql = """
            SELECT
                u.id_usuario,
                u.usu_nick,
                u.est_usuario,
                u.usu_nro_intentos,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, 'Sin funcionario') AS funcionario,
                COALESCE(c.des_cargo, 'Sin cargo') AS cargo,
                COALESCE(rp.cod_rol, 'Sin rol') AS rol_principal,
                u.fecha_creacion,
                f.id_funcionario,
                esta_usuario_bloqueado(u.id_usuario) AS esta_bloqueado,
                u.bloqueado_hasta,
                u.motivo_bloqueo
            FROM usuarios u
            LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
            LEFT JOIN personas p ON p.id_persona = f.id_persona
            LEFT JOIN cargos c ON c.id_cargo = f.id_cargo
            LEFT JOIN usuarios_roles ur_p ON ur_p.id_usuario = u.id_usuario AND ur_p.es_rol_principal = TRUE
            LEFT JOIN roles rp ON rp.id_rol = ur_p.id_rol
            ORDER BY u.id_usuario DESC
        """
        filas = self.execute_query(sql)
        for fila in filas:
            roles = self.obtener_roles_usuario(fila["id_usuario"])
            fila["roles"] = roles
            fila["roles_adicionales"] = [r["cod_rol"] for r in roles if not r["es_rol_principal"]]
            fila["total_roles"] = len(roles)
        return filas

    def getUsuarioById(self, id_usuario):
        """Devuelve el usuario por su id, o None si no existe."""
        sql = """
            SELECT
                u.id_usuario,
                u.usu_nick,
                u.est_usuario,
                u.usu_nro_intentos,
                u.id_funcionario,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, 'Sin funcionario') AS funcionario,
                COALESCE(c.des_cargo, 'Sin cargo') AS cargo
            FROM usuarios u
            LEFT JOIN funcionarios f ON f.id_funcionario = u.id_funcionario
            LEFT JOIN personas p ON p.id_persona = f.id_persona
            LEFT JOIN cargos c ON c.id_cargo = f.id_cargo
            WHERE u.id_usuario = %s
        """
        usuario = self.execute_query_one(sql, (id_usuario,))
        if usuario:
            usuario["roles"] = self.obtener_roles_usuario(id_usuario)
        return usuario

    def getFuncionariosSinUsuario(self):
        """Funcionarios activos que todavía no tienen usuario asignado."""
        sql = """
            SELECT
                f.id_funcionario,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                c.des_cargo,
                p.per_cedula
            FROM funcionarios f
            INNER JOIN personas p ON p.id_persona = f.id_persona
            INNER JOIN cargos c ON c.id_cargo = f.id_cargo
            LEFT JOIN usuarios u ON u.id_funcionario = f.id_funcionario
            WHERE f.est_funcionario = TRUE
              AND u.id_usuario IS NULL
            ORDER BY p.per_nombre
        """
        return self.execute_query(sql)

    def validarUsernameDisponible(self, username, id_usuario=None):
        """Indica si el nombre de usuario está libre; `id_usuario` omite al propio usuario al editar."""
        if id_usuario:
            sql = "SELECT id_usuario FROM usuarios WHERE usu_nick = %s AND id_usuario != %s"
            params = (username, id_usuario)
        else:
            sql = "SELECT id_usuario FROM usuarios WHERE usu_nick = %s"
            params = (username,)
        return self.execute_query_one(sql, params) is None

    def guardarUsuario(self, username, password, id_funcionario, id_rol, est_usuario=True, usuario_creacion=None):
        """Crea un usuario nuevo y le asigna id_rol como rol principal."""
        if not self.validarUsernameDisponible(username):
            return None

        if self.execute_query_one("SELECT id_usuario FROM usuarios WHERE id_funcionario = %s", (id_funcionario,)):
            return None

        password_hash = generate_password_hash(password, method='pbkdf2:sha256')

        sql_usuario = """
            INSERT INTO usuarios (
                usu_nick, usu_clave, id_funcionario, est_usuario,
                clave_nunca_expira, requiere_cambio_clave, fecha_cambio_clave, usuario_creacion
            )
            VALUES (%s, %s, %s, %s, TRUE, FALSE, NOW(), %s)
            RETURNING id_usuario
        """
        fila = self.execute_query_one(
            sql_usuario,
            (username, password_hash, id_funcionario, est_usuario, usuario_creacion),
            commit=True
        )
        if not fila:
            return None
        id_usuario = fila["id_usuario"]

        sql_rol = """
            INSERT INTO usuarios_roles (id_usuario, id_rol, es_rol_principal, usuario_creacion)
            VALUES (%s, %s, TRUE, %s)
        """
        self.execute_query(sql_rol, (id_usuario, id_rol, usuario_creacion), commit=True)

        return id_usuario

    def updateUsuario(self, id_usuario, username, est_usuario, password=None, usuario_modificacion=None):
        """Actualiza datos básicos del usuario (no toca roles, ver cambiar_rol_principal)."""
        if not self.validarUsernameDisponible(username, id_usuario):
            return False

        if password:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            sql = """
                UPDATE usuarios
                SET usu_nick = %s, usu_clave = %s, est_usuario = %s,
                    clave_nunca_expira = TRUE, requiere_cambio_clave = FALSE, fecha_cambio_clave = NOW(),
                    usuario_modificacion = %s
                WHERE id_usuario = %s
            """
            params = (username, password_hash, est_usuario, usuario_modificacion, id_usuario)
        else:
            sql = """
                UPDATE usuarios
                SET usu_nick = %s, est_usuario = %s, usuario_modificacion = %s
                WHERE id_usuario = %s
            """
            params = (username, est_usuario, usuario_modificacion, id_usuario)

        return self.execute_query(sql, params, commit=True) > 0

    def desactivarUsuario(self, id_usuario, usuario_modificacion=None):
        """Da de baja (lógica) al usuario; devuelve True si modificó una fila."""
        sql = """
            UPDATE usuarios
            SET est_usuario = FALSE, usuario_modificacion = %s
            WHERE id_usuario = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_usuario), commit=True) > 0

    def resetearIntentos(self, id_usuario, usuario_modificacion=None):
        """Desbloqueo manual: limpia el contador de intentos fallidos y el
        bloqueo activo (incluido el indefinido del nivel 3, que no se autolevanta
        con el tiempo) y reinicia la escalada: el próximo bloqueo vuelve a ser
        el de 5 intentos / 30 min (ver migrations/104)."""
        sql = """
            UPDATE usuarios
            SET usu_nro_intentos = 0,
                nivel_escalada_bloqueo = 0,
                fecha_bloqueo = NULL,
                bloqueado_hasta = NULL,
                motivo_bloqueo = NULL,
                usuario_modificacion = %s
            WHERE id_usuario = %s
        """
        return self.execute_query(sql, (usuario_modificacion, id_usuario), commit=True) > 0

    # ============================================
    # ROLES MÚLTIPLES (usuarios_roles)
    # ============================================

    def obtener_roles_usuario(self, id_usuario):
        """Todos los roles activos de un usuario (principal primero)."""
        sql = """
            SELECT
                ur.id_usuario_rol,
                r.id_rol,
                r.cod_rol,
                r.des_rol,
                ur.es_rol_principal,
                ur.fecha_creacion
            FROM usuarios_roles ur
            INNER JOIN roles r ON r.id_rol = ur.id_rol
            WHERE ur.id_usuario = %s AND ur.est_usuario_rol = TRUE
            ORDER BY ur.es_rol_principal DESC, ur.fecha_creacion ASC
        """
        return self.execute_query(sql, (id_usuario,))

    def obtener_rol_principal(self, id_usuario):
        """Devuelve el rol principal activo del usuario, o None."""
        sql = """
            SELECT r.id_rol, r.cod_rol, r.des_rol, ur.id_usuario_rol
            FROM usuarios_roles ur
            INNER JOIN roles r ON r.id_rol = ur.id_rol
            WHERE ur.id_usuario = %s AND ur.es_rol_principal = TRUE AND ur.est_usuario_rol = TRUE
            LIMIT 1
        """
        return self.execute_query_one(sql, (id_usuario,))

    def contar_usuarios_activos_con_funcionario(self):
        """Cuenta los usuarios activos vinculados a un funcionario (para el tope de usuarios)."""
        sql = "SELECT COUNT(*) AS total FROM usuarios WHERE est_usuario = TRUE AND id_funcionario IS NOT NULL"
        fila = self.execute_query_one(sql)
        return fila["total"] if fila else 0

    def contar_roles_activos(self, id_usuario):
        """Cuenta los roles activos del usuario (para el tope de roles por usuario)."""
        sql = "SELECT COUNT(*) AS total FROM usuarios_roles WHERE id_usuario = %s AND est_usuario_rol = TRUE"
        fila = self.execute_query_one(sql, (id_usuario,))
        return fila["total"] if fila else 0

    def asignar_rol_usuario(self, id_usuario, id_rol, es_principal=False, usuario_creacion=None):
        """Asigna un rol a un usuario (máximo 3 roles activos simultáneos)."""
        if self.contar_roles_activos(id_usuario) >= MAX_ROLES_POR_USUARIO:
            return None

        if self.execute_query_one(
            "SELECT id_usuario_rol FROM usuarios_roles WHERE id_usuario = %s AND id_rol = %s AND est_usuario_rol = TRUE",
            (id_usuario, id_rol)
        ):
            return None

        if es_principal:
            self.execute_query(
                "UPDATE usuarios_roles SET es_rol_principal = FALSE WHERE id_usuario = %s AND es_rol_principal = TRUE",
                (id_usuario,), commit=True
            )

        sql = """
            INSERT INTO usuarios_roles (id_usuario, id_rol, es_rol_principal, usuario_creacion)
            VALUES (%s, %s, %s, %s)
            RETURNING id_usuario_rol
        """
        fila = self.execute_query_one(sql, (id_usuario, id_rol, es_principal, usuario_creacion), commit=True)
        return fila["id_usuario_rol"] if fila else None

    def remover_rol_usuario(self, id_usuario, id_rol, usuario_modificacion=None):
        """Quita un rol (soft delete). No permite remover el único rol del usuario."""
        if self.contar_roles_activos(id_usuario) <= 1:
            return False

        rol_info = self.execute_query_one(
            "SELECT es_rol_principal FROM usuarios_roles WHERE id_usuario = %s AND id_rol = %s AND est_usuario_rol = TRUE",
            (id_usuario, id_rol)
        )
        if not rol_info:
            return False

        if rol_info["es_rol_principal"]:
            otro_rol = self.execute_query_one(
                "SELECT id_rol FROM usuarios_roles WHERE id_usuario = %s AND id_rol != %s AND est_usuario_rol = TRUE LIMIT 1",
                (id_usuario, id_rol)
            )
            if otro_rol:
                self.execute_query(
                    "UPDATE usuarios_roles SET es_rol_principal = TRUE, usuario_modificacion = %s WHERE id_usuario = %s AND id_rol = %s",
                    (usuario_modificacion, id_usuario, otro_rol["id_rol"]), commit=True
                )

        return self.execute_query(
            "UPDATE usuarios_roles SET est_usuario_rol = FALSE, usuario_modificacion = %s WHERE id_usuario = %s AND id_rol = %s AND est_usuario_rol = TRUE",
            (usuario_modificacion, id_usuario, id_rol), commit=True
        ) > 0

    def cambiar_rol_principal(self, id_usuario, nuevo_id_rol_principal, usuario_modificacion=None):
        """Cambia cuál de los roles ya asignados es el principal."""
        existe = self.execute_query_one(
            "SELECT id_usuario_rol FROM usuarios_roles WHERE id_usuario = %s AND id_rol = %s AND est_usuario_rol = TRUE",
            (id_usuario, nuevo_id_rol_principal)
        )
        if not existe:
            return False

        self.execute_query(
            "UPDATE usuarios_roles SET es_rol_principal = FALSE, usuario_modificacion = %s WHERE id_usuario = %s AND es_rol_principal = TRUE",
            (usuario_modificacion, id_usuario), commit=True
        )
        self.execute_query(
            "UPDATE usuarios_roles SET es_rol_principal = TRUE, usuario_modificacion = %s WHERE id_usuario = %s AND id_rol = %s",
            (usuario_modificacion, id_usuario, nuevo_id_rol_principal), commit=True
        )
        return True
