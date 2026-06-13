"""
Funciones helper para templates Jinja2
app/utils/template_helpers.py

Uso en __init__.py:
    from app.utils.template_helpers import registrar_funciones_template
    registrar_funciones_template(app)
"""
from flask import session


def registrar_funciones_template(app):
    """
    Registra funciones globales en Jinja2
    Llamar desde __init__.py después de crear el app
    """
    
    @app.context_processor
    def utility_processor():
        return dict(
            # Verificación de roles
            es_admin=es_admin,
            es_recepcion=es_recepcion,
            es_especialista=es_especialista,
            es_ventas=es_ventas,
            es_superadmin=es_superadmin,
            es_admin_o_superadmin=es_admin_o_superadmin,  # ← NUEVO
            es_caja=es_caja,
            
            # Permisos
            puede_acceder_modulo=puede_acceder_modulo,
            tiene_permiso=tiene_permiso,
            
            # Info del usuario
            obtener_nombre_usuario=obtener_nombre_usuario,
            obtener_grupo_usuario=obtener_grupo_usuario,
            obtener_modulos_usuario=obtener_modulos_usuario,
            obtener_widgets_usuario=obtener_widgets_usuario,
            
            # Verificación avanzada de permisos
            tiene_permiso_accion=tiene_permiso_accion
        )


# ============================================================================
# FUNCIONES DE VERIFICACIÓN DE ROLES
# ============================================================================

def es_admin():
    """
    Verifica si el usuario actual es Administrador
    Soporta múltiples roles (verifica si tiene rol de Administrador)
    
    Returns:
        bool: True si es admin, False en caso contrario
    
    Uso en template:
        {% if es_admin() %}
            <a href="/admin/config">Configuración</a>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_admin()
    except Exception:
        # Fallback a verificación básica
        return session.get('id_grupo') == 1


def es_recepcion():
    """
    Verifica si el usuario actual es Recepcionista
    Soporta múltiples roles (verifica si tiene rol de Recepcionista)
    
    Returns:
        bool: True si es recepción, False en caso contrario
    
    Uso en template:
        {% if es_recepcion() %}
            <button>Agendar Cita</button>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_recepcionista()
    except Exception:
        # Fallback a verificación básica
        return session.get('id_grupo') == 2


def es_especialista():
    """
    Verifica si el usuario actual es Especialista (Médico/Psicólogo)
    Soporta múltiples roles (verifica si tiene rol de Especialista O registro en especialistas)
    Permite que un Admin que también es especialista sea detectado
    
    Returns:
        bool: True si es especialista, False en caso contrario
    
    Uso en template:
        {% if es_especialista() %}
            <a href="/consultorios">Mis Consultorios</a>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_especialista()
    except Exception:
        # Fallback: verificar por grupo_id o por registro en especialistas
        grupo_id = session.get('id_grupo')
        if grupo_id == 3:
            return True
        
        # Si no es grupo 3, verificar si tiene registro en especialistas
        # Esto permite que un Admin que también es especialista sea detectado
        try:
            from app.utils.especialista_helper import obtener_id_especialista_usuario
            id_especialista = obtener_id_especialista_usuario()
            return id_especialista is not None
        except Exception:
            return False


def es_ventas():
    """
    Verifica si el usuario actual es del grupo Ventas
    Soporta múltiples roles (verifica si tiene rol de Ventas)
    
    Returns:
        bool: True si es ventas, False en caso contrario
    
    Uso en template:
        {% if es_ventas() %}
            <a href="/ventas">Panel de Ventas</a>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_ventas()
    except Exception:
        # Fallback a verificación básica
        return session.get('id_grupo') == 4


def es_superadmin():
    """
    Verifica si el usuario actual es Superadministrador
    Soporta múltiples roles (verifica si tiene rol de Superadministrador)
    
    Returns:
        bool: True si es superadmin, False en caso contrario
    
    Uso en template:
        {% if es_superadmin() %}
            <a href="/usuarios">Gestión de Usuarios</a>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_superadmin()
    except Exception:
        # Fallback a verificación básica
        grupo_id = session.get('id_grupo')
        grupo_nombre = session.get('grupo', '').upper()
        
        if grupo_id == 5:
            return True
        
        return grupo_nombre == 'SUPERADMINISTRADOR'


def es_caja():
    """
    Verifica si el usuario actual es Cajero
    Soporta múltiples roles (verifica si tiene rol de de Caja)
    
    Returns:
        bool: True si es caja, False en caso contrario
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.es_caja()
    except Exception:
        # Fallback a verificación básica
        grupo_id = session.get('id_grupo')
        grupo_nombre = session.get('grupo', '').upper()
        
        if grupo_id == 6:
            return True
            
        return grupo_nombre == 'CAJA'


def es_admin_o_superadmin():
    """
    Verifica si el usuario es Administrador o Superadministrador
    Útil para mostrar opciones que ambos pueden ver
    
    Returns:
        bool: True si es admin o superadmin
    """
    return es_admin() or es_superadmin()


# ============================================================================
# FUNCIONES DE VERIFICACIÓN DE PERMISOS
# ============================================================================

def puede_acceder_modulo(nombre_modulo):
    """
    Verifica si el usuario puede acceder a un módulo específico
    Usa el servicio de módulos para verificar acceso basado en roles
    
    Args:
        nombre_modulo (str): Nombre del módulo a verificar
        
    Returns:
        bool: True si tiene acceso, False en caso contrario
    
    Uso en template:
        {% if puede_acceder_modulo('dashboard') %}
            <li><a href="/dashboard">Dashboard</a></li>
        {% endif %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        return modulos_service.tiene_acceso_modulo(nombre_modulo)
    except Exception as e:
        # Fallback a verificación básica si falla el servicio
        if 'id_grupo' not in session:
            return False
        
        grupo_id = session.get('id_grupo')
        
        # Admin y Superadmin tienen acceso a todo
        if grupo_id == 1 or grupo_id == 5:
            return True
        
        # Intentar verificar desde la BD como fallback
        try:
            from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
            permisos_dao = PermisosDao()
            return permisos_dao.verificar_permiso_modulo(grupo_id, nombre_modulo)
        except Exception:
            return False


def tiene_permiso(ruta):
    """
    Verifica si el usuario tiene permiso para acceder a una ruta específica
    
    Args:
        ruta (str): Ruta a verificar (ej: '/modulos/funcionario/funcionario-index')
        
    Returns:
        bool: True si tiene permiso, False en caso contrario
    
    Uso en template:
        {% if tiene_permiso('/modulos/paciente/crear') %}
            <a href="/modulos/paciente/crear">Nuevo Paciente</a>
        {% endif %}
    """
    if 'id_grupo' not in session:
        return False
    
    grupo_id = session.get('id_grupo')
    
    # Admin y Superadmin tienen acceso a todo
    if grupo_id == 1 or grupo_id == 5:
        return True
    
    if not grupo_id:
        return False
    
    try:
        from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
        dao = PermisosDao()
        return dao.verificar_permiso_ruta(grupo_id, ruta)
    except Exception as e:
        print(f"Error verificando permiso: {str(e)}")
        return False


def tiene_permiso_accion(accion, ruta=None):
    """
    Verifica si el usuario tiene permiso para una acción específica en una ruta
    
    Args:
        accion (str): Acción a verificar ('insertar', 'actualizar', 'eliminar', 'consultar')
        ruta (str, optional): Ruta específica. Si es None, solo verifica por grupo
        
    Returns:
        bool: True si tiene permiso, False en caso contrario
    
    Uso en template:
        {% if tiene_permiso_accion('insertar', '/modulos/paciente/crear') %}
            <button class="btn-primary">Guardar</button>
        {% endif %}
        
        {% if tiene_permiso_accion('eliminar', '/modulos/paciente/eliminar') %}
            <button class="btn-danger">Eliminar</button>
        {% endif %}
    """
    if 'id_grupo' not in session:
        return False
    
    from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
    
    id_grupo = session.get('id_grupo')
    permisos_dao = PermisosDao()
    
    # Administrador y Superadministrador siempre tienen permiso
    try:
        if permisos_dao.es_administrador(id_grupo):
            return True
    except Exception:
        # Si falla el método, verificar por ID
        if id_grupo == 1 or id_grupo == 5:
            return True
    
    # Si no se especifica ruta, verificar solo por grupo
    if not ruta:
        return True
    
    try:
        return permisos_dao.verificar_permiso_ruta(id_grupo, ruta, accion)
    except Exception as e:
        print(f"Error verificando permiso con acción: {str(e)}")
        return False


# ============================================================================
# FUNCIONES DE INFORMACIÓN DEL USUARIO
# ============================================================================

def obtener_nombre_usuario():
    """
    Obtiene el nombre completo del usuario actual
    
    Returns:
        str: Nombre completo o 'Usuario'
    
    Uso en template:
        <span>Bienvenido, {{ obtener_nombre_usuario() }}</span>
    """
    return session.get('nombre_persona', 'Usuario')


def obtener_grupo_usuario():
    """
    Obtiene el nombre del grupo/rol del usuario actual
    
    Returns:
        str: Nombre del grupo o 'Sin rol'
    
    Uso en template:
        <span class="badge">{{ obtener_grupo_usuario() }}</span>
    """
    return session.get('grupo', 'Sin rol')


def obtener_modulos_usuario():
    """
    Obtiene lista de módulos a los que el usuario tiene acceso
    Útil para construir menús dinámicos
    Soporta múltiples roles (combina módulos de todos los roles del usuario)
    
    Returns:
        list: Lista de módulos (strings) accesibles
    
    Uso en template:
        <ul class="menu">
        {% for modulo in obtener_modulos_usuario() %}
            <li>
                <a href="/{{ modulo }}">{{ modulo|title }}</a>
            </li>
        {% endfor %}
        </ul>
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        modulos = modulos_service.obtener_modulos_usuario()
        return sorted(list(modulos))  # Retornar como lista ordenada
    except Exception as e:
        # Fallback a verificación desde BD
        if 'id_grupo' not in session:
            return []
        
        try:
            from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
            id_grupo = session.get('id_grupo')
            permisos_dao = PermisosDao()
            return permisos_dao.obtener_modulos_permitidos(id_grupo)
        except Exception:
            return []


def obtener_widgets_usuario():
    """
    Obtiene lista de widgets disponibles para el dashboard del usuario
    Soporta múltiples roles (combina widgets de todos los roles del usuario)
    
    Returns:
        list: Lista de widgets (strings) disponibles para el dashboard
    
    Uso en template:
        {% for widget in obtener_widgets_usuario() %}
            <div class="widget-{{ widget }}">...</div>
        {% endfor %}
    """
    try:
        from app.services.modulos_service import ModulosService
        modulos_service = ModulosService()
        widgets = modulos_service.obtener_widgets_usuario()
        return sorted(list(widgets))  # Retornar como lista ordenada
    except Exception as e:
        return []


# ============================================================================
# FUNCIONES AUXILIARES (OPCIONALES)
# ============================================================================

def obtener_iniciales_usuario():
    """
    Obtiene las iniciales del usuario (útil para avatares)
    
    Returns:
        str: Iniciales del usuario (ej: 'JD' para Juan Díaz)
    
    Uso en template:
        <div class="avatar">{{ obtener_iniciales_usuario() }}</div>
    """
    nombre = session.get('nombre_persona', 'U')
    palabras = nombre.split()
    
    if len(palabras) >= 2:
        return f"{palabras[0][0]}{palabras[1][0]}".upper()
    elif len(palabras) == 1:
        return palabras[0][:2].upper()
    else:
        return 'U'


def usuario_autenticado():
    """
    Verifica si hay un usuario autenticado en la sesión
    
    Returns:
        bool: True si hay usuario autenticado
    
    Uso en template:
        {% if usuario_autenticado() %}
            <a href="/perfil">Mi Perfil</a>
        {% else %}
            <a href="/login">Iniciar Sesión</a>
        {% endif %}
    """
    return 'id_usuario' in session and session.get('id_usuario') is not None


















# """
# Helper functions para usar en templates Jinja2
# Agregar en __init__.py para disponibilidad global

# En tu __init__.py, después de crear la app:

#     from app.utils.template_helpers import registrar_funciones_template
#     registrar_funciones_template(app)
# """

# from flask import session


# def tiene_permiso(accion, ruta=None):
#     """
#     Verifica si el usuario actual tiene un permiso específico
    
#     Uso en template:
#         {% if tiene_permiso('insertar', '/modulos/paciente/crear') %}
#             <button>Crear Paciente</button>
#         {% endif %}
#     """
#     if 'id_grupo' not in session:
#         return False
    
#     from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
    
#     id_grupo = session.get('id_grupo')
#     permisos_dao = PermisosDao()
    
#     # Administrador siempre tiene permiso
#     if permisos_dao.es_administrador(id_grupo):
#         return True
    
#     # Si no se especifica ruta, verificar solo por grupo
#     if not ruta:
#         return True
    
#     return permisos_dao.verificar_permiso_ruta(id_grupo, ruta, accion)


# def es_admin():
#     """
#     Verifica si el usuario actual es Administrador
    
#     Uso en template:
#         {% if es_admin() %}
#             <a href="/admin/config">Configuración</a>
#         {% endif %}
#     """
#     if 'grupo' not in session:
#         return False
    
#     return session.get('grupo', '').upper() == 'ADMINISTRADOR'


# def es_recepcion():
#     """
#     Verifica si el usuario es Recepcionista
#     """
#     if 'grupo' not in session:
#         return False
    
#     return session.get('grupo', '').upper() == 'RECEPCIONISTA'


# def es_especialista():
#     """
#     Verifica si el usuario es Especialista
#     """
#     if 'grupo' not in session:
#         return False
    
#     return session.get('grupo', '').upper() == 'ESPECIALISTA'


# def puede_acceder_modulo(nombre_modulo):
#     """
#     Verifica si el usuario tiene acceso a un módulo completo
    
#     Uso en template:
#         {% if puede_acceder_modulo('Agendamiento') %}
#             <li><a href="/agenda">Agenda</a></li>
#         {% endif %}
#     """
#     if 'id_grupo' not in session:
#         return False
    
#     from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
    
#     id_grupo = session.get('id_grupo')
#     permisos_dao = PermisosDao()
    
#     if permisos_dao.es_administrador(id_grupo):
#         return True
    
#     return permisos_dao.verificar_permiso_modulo(id_grupo, nombre_modulo)


# def obtener_modulos_usuario():
#     """
#     Obtiene lista de módulos a los que el usuario tiene acceso
#     Para construir menús dinámicos
    
#     Uso en template:
#         {% for modulo in obtener_modulos_usuario() %}
#             <li>{{ modulo.des_modulo }}</li>
#         {% endfor %}
#     """
#     if 'id_grupo' not in session:
#         return []
    
#     from app.dao.referenciales.generales.usuario.permisos_dao import PermisosDao
    
#     id_grupo = session.get('id_grupo')
#     permisos_dao = PermisosDao()
    
#     return permisos_dao.obtener_modulos_permitidos(id_grupo)


# def registrar_funciones_template(app):
#     """
#     Registra todas las funciones helper en el contexto de Jinja2
#     Llamar esto en __init__.py después de crear la app
#     """
#     app.jinja_env.globals.update(
#         tiene_permiso=tiene_permiso,
#         es_admin=es_admin,
#         es_recepcion=es_recepcion,
#         es_especialista=es_especialista,
#         puede_acceder_modulo=puede_acceder_modulo,
#         obtener_modulos_usuario=obtener_modulos_usuario
#     )