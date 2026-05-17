"""
Decoradores para controlar acceso basado en roles y permisos
"""
from functools import wraps
from flask import session, redirect, url_for, flash, abort, request


def require_group(*grupos_permitidos):
    """
    Verifica si el usuario pertenece a uno de los grupos permitidos
    
    Uso:
        @require_group('Administrador', 'Recepcionista')
        def mi_ruta():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'grupo' not in session:
                flash('Debes iniciar sesión primero', 'warning')
                return redirect(url_for('login.login'))
            
            grupo_usuario = session.get('grupo', '').upper()
            grupos_upper = [g.upper() for g in grupos_permitidos]
            
            if grupo_usuario not in grupos_upper:
                flash(f'⛔ Acceso denegado. Se requiere rol: {", ".join(grupos_permitidos)}', 'danger')
                return redirect(url_for('login.inicio'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_permission(accion='leer'):
    """
    Verifica permisos específicos basándose en la ruta actual
    
    Args:
        accion: 'leer', 'insertar', 'editar', 'borrar'
    
    Uso:
        @require_permission('insertar')
        def crear_paciente():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id_grupo' not in session:
                flash('Debes iniciar sesión primero', 'warning')
                return redirect(url_for('login.login'))
            
            from app.dao.referenciales.usuario.permisos_dao import PermisosDao
            
            id_grupo = session.get('id_grupo')
            permisos_dao = PermisosDao()
            
            # Si es superadministrador, permitir siempre
            if permisos_dao.es_superadministrador(id_grupo):
                return f(*args, **kwargs)
            
            # Si es administrador, permitir siempre (excepto creación de usuarios)
            if permisos_dao.es_administrador(id_grupo):
                return f(*args, **kwargs)
            
            # Obtener la ruta actual
            ruta_actual = request.path
            
            # Verificar permiso
            tiene_permiso = permisos_dao.verificar_permiso_ruta(id_grupo, ruta_actual, accion)
            
            if not tiene_permiso:
                accion_texto = {
                    'leer': 'ver',
                    'insertar': 'crear',
                    'editar': 'modificar',
                    'borrar': 'eliminar'
                }.get(accion, accion)
                
                flash(f'⛔ No tienes permiso para {accion_texto} en esta sección', 'danger')
                return redirect(url_for('login.inicio'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_only(f):
    """
    Decorador que permite acceso SOLO a Administradores
    
    Uso:
        @admin_only
        def eliminar_usuario():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_grupo' not in session:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('login.login'))
        
        from app.dao.referenciales.usuario.permisos_dao import PermisosDao
        
        permisos_dao = PermisosDao()
        id_grupo = session.get('id_grupo')
        
        # Superadministrador también tiene acceso
        if permisos_dao.es_superadministrador(id_grupo):
            return f(*args, **kwargs)
        
        if not permisos_dao.es_administrador(id_grupo):
            flash('⛔ Esta acción requiere permisos de Administrador', 'danger')
            return redirect(url_for('login.inicio'))
        
        return f(*args, **kwargs)
    return decorated_function


def superadmin_only(f):
    """
    Decorador que permite acceso SOLO a Superadministrador
    
    Uso:
        @superadmin_only
        def crear_usuario():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id_grupo' not in session:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('login.login'))
        
        from app.dao.referenciales.usuario.permisos_dao import PermisosDao
        
        permisos_dao = PermisosDao()
        id_grupo = session.get('id_grupo')
        
        if not permisos_dao.es_superadministrador(id_grupo):
            flash('⛔ Esta acción requiere permisos de Superadministrador', 'danger')
            return redirect(url_for('login.inicio'))
        
        return f(*args, **kwargs)
    return decorated_function


def recepcion_o_admin(f):
    """
    Permite acceso a Recepcionistas y Administradores
    
    Uso:
        @recepcion_o_admin
        def agendar_cita():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'grupo' not in session:
            flash('Debes iniciar sesión primero', 'warning')
            return redirect(url_for('login.login'))
        
        grupo = session.get('grupo', '').upper()
        
        if grupo not in ['ADMINISTRADOR', 'RECEPCIONISTA']:
            flash('⛔ Acceso solo para Recepción y Administradores', 'danger')
            return redirect(url_for('login.inicio'))
        
        return f(*args, **kwargs)
    return decorated_function


def check_module_access(nombre_modulo):
    """
    Verifica si el usuario tiene acceso a un módulo completo
    
    Uso:
        @check_module_access('Agendamiento')
        def listar_citas():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'id_grupo' not in session:
                flash('Debes iniciar sesión primero', 'warning')
                return redirect(url_for('login.login'))
            
            from app.dao.referenciales.usuario.permisos_dao import PermisosDao
            
            id_grupo = session.get('id_grupo')
            permisos_dao = PermisosDao()
            
            # Superadministrador y Administrador tienen acceso a todo
            if permisos_dao.es_superadministrador(id_grupo) or permisos_dao.es_administrador(id_grupo):
                return f(*args, **kwargs)
            
            # Verificar acceso al módulo
            tiene_acceso = permisos_dao.verificar_permiso_modulo(id_grupo, nombre_modulo)
            
            if not tiene_acceso:
                flash(f'⛔ No tienes acceso al módulo: {nombre_modulo}', 'danger')
                return redirect(url_for('login.inicio'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator