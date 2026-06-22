from flask import Blueprint, request, jsonify, current_app as app
from app.dao.auth.user_dao import UsuarioDao

usuarioapi = Blueprint('usuarioapi', __name__)

# ============================================
# DEBUG - VERIFICAR SESIÓN Y PERMISOS
# ============================================
@usuarioapi.route('/usuarios/debug', methods=['GET'])
def debugUsuarios():
    """Ruta de debug para verificar sesión y permisos"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    usuariodao = UsuarioDao()
    
    id_grupo_actual = session.get('id_grupo')
    id_usuario_actual = session.get('id_usuario')
    
    # Verificar roles múltiples
    roles_usuario = []
    es_superadmin_por_grupo = False
    es_superadmin_por_roles = False
    
    if id_grupo_actual:
        es_superadmin_por_grupo = roles_service.es_superadmin(id_grupo_actual)
    
    if id_usuario_actual:
        roles_usuario = usuariodao.obtener_roles_usuario(id_usuario_actual)
        for rol in roles_usuario:
            if roles_service.es_superadmin(rol['id_grupo']):
                es_superadmin_por_roles = True
                break
    
    # Obtener todos los usuarios (sin filtro)
    todos_los_usuarios = usuariodao.getUsuarios()
    
    return jsonify({
        'success': True,
        'debug': {
            'id_usuario': id_usuario_actual,
            'id_grupo': id_grupo_actual,
            'es_superadmin_por_grupo': es_superadmin_por_grupo,
            'es_superadmin_por_roles': es_superadmin_por_roles,
            'es_superadmin_total': es_superadmin_por_grupo or es_superadmin_por_roles,
            'roles_usuario': roles_usuario,
            'total_usuarios_en_bd': len(todos_los_usuarios),
            'sesion_completa': dict(session)
        }
    }), 200

# ============================================
# OBTENER TODOS LOS USUARIOS
# ============================================
@usuarioapi.route('/usuarios', methods=['GET'])
def getUsuarios():
    """Obtiene la lista completa de usuarios (filtrada según permisos)"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    usuariodao = UsuarioDao()
    
    try:
        usuarios = usuariodao.getUsuarios()
        id_grupo_actual = session.get('id_grupo')
        id_usuario_actual = session.get('id_usuario')
        
        # Verificar si es Superadministrador (verificar también roles múltiples)
        es_superadmin = False
        es_superadmin_por_grupo = False
        es_superadmin_por_roles = False
        
        # Verificar por id_grupo de sesión
        if id_grupo_actual:
            try:
                es_superadmin_por_grupo = roles_service.es_superadmin(id_grupo_actual)
                es_superadmin = es_superadmin_por_grupo
                app.logger.info(f"DEBUG getUsuarios: Verificación por grupo - id_grupo={id_grupo_actual}, es_superadmin={es_superadmin_por_grupo}")
            except Exception as e:
                app.logger.error(f"Error al verificar superadmin por grupo: {str(e)}")
        
        # Si no es superadmin por id_grupo, verificar en roles múltiples
        if not es_superadmin and id_usuario_actual:
            try:
                roles_usuario = usuariodao.obtener_roles_usuario(id_usuario_actual)
                app.logger.info(f"DEBUG getUsuarios: Verificando roles múltiples - total roles: {len(roles_usuario)}")
                for rol in roles_usuario:
                    if roles_service.es_superadmin(rol['id_grupo']):
                        es_superadmin_por_roles = True
                        es_superadmin = True
                        app.logger.info(f"DEBUG getUsuarios: Superadmin detectado por rol - id_grupo={rol['id_grupo']}")
                        break
            except Exception as e:
                app.logger.error(f"Error al verificar superadmin por roles: {str(e)}")
        
        app.logger.info(f"DEBUG getUsuarios: id_grupo_actual={id_grupo_actual}, id_usuario_actual={id_usuario_actual}, es_superadmin_por_grupo={es_superadmin_por_grupo}, es_superadmin_por_roles={es_superadmin_por_roles}, es_superadmin={es_superadmin}, total_usuarios={len(usuarios)}")
        
        # Si es Superadministrador, ver todos los usuarios
        if es_superadmin:
            usuarios_filtrados = usuarios
            app.logger.info(f"DEBUG getUsuarios: Superadmin detectado, devolviendo {len(usuarios_filtrados)} usuarios sin filtrar")
        # Si es Administrador, filtrar usuarios con roles administrativos
        elif roles_service.es_admin(id_grupo_actual):
            id_grupo_superadmin = roles_service.obtener_id_grupo_superadmin()
            id_grupo_admin = roles_service.obtener_id_grupo_admin()
            
            # Filtrar usuarios que NO tengan rol de Superadmin o Admin
            usuarios_filtrados = []
            for usuario in usuarios:
                id_grupo_principal = usuario.get('id_grupo_principal')
                roles_adicionales = usuario.get('roles_adicionales', [])
                
                # Verificar si tiene rol de Superadmin o Admin
                tiene_rol_admin = (id_grupo_principal == id_grupo_superadmin or 
                                  id_grupo_principal == id_grupo_admin)
                
                # Verificar en roles adicionales
                if not tiene_rol_admin:
                    # Obtener IDs de grupos de roles adicionales
                    roles_usuario = usuariodao.obtener_roles_usuario(usuario['id_usuario'])
                    ids_grupos = [r['id_grupo'] for r in roles_usuario]
                    tiene_rol_admin = (id_grupo_superadmin in ids_grupos or 
                                      id_grupo_admin in ids_grupos)
                
                # Solo incluir si NO tiene rol administrativo
                if not tiene_rol_admin:
                    usuarios_filtrados.append(usuario)
        else:
            # Otros roles no deberían ver esta página, pero por seguridad retornar vacío
            usuarios_filtrados = []
        
        app.logger.info(f"DEBUG getUsuarios: Retornando {len(usuarios_filtrados)} usuarios filtrados")
        
        # Log adicional para debugging
        if len(usuarios_filtrados) == 0 and len(usuarios) > 0:
            app.logger.warning(f"⚠️ ADVERTENCIA: Hay {len(usuarios)} usuarios en BD pero se retornan 0. es_superadmin={es_superadmin}, id_grupo_actual={id_grupo_actual}")
        
        return jsonify({
            'success': True,
            'data': usuarios_filtrados,
            'error': None,
            'debug': {
                'total_usuarios_bd': len(usuarios),
                'total_usuarios_filtrados': len(usuarios_filtrados),
                'es_superadmin': es_superadmin,
                'es_superadmin_por_grupo': es_superadmin_por_grupo,
                'es_superadmin_por_roles': es_superadmin_por_roles,
                'id_grupo_actual': id_grupo_actual,
                'id_usuario_actual': id_usuario_actual
            }
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER USUARIO POR ID
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>', methods=['GET'])
def getUsuario(id_usuario):
    """Obtiene un usuario específico por su ID"""
    usuariodao = UsuarioDao()
    
    try:
        usuario = usuariodao.getUsuarioById(id_usuario)
        
        if usuario:
            return jsonify({
                'success': True,
                'data': usuario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado.'
            }), 404
    
    except Exception as e:
        app.logger.error(f"Error al obtener usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER FUNCIONARIOS SIN USUARIO
# ============================================
@usuarioapi.route('/funcionarios/sin-usuario', methods=['GET'])
def getFuncionariosSinUsuario():
    """Obtiene funcionarios que no tienen usuario asignado"""
    usuariodao = UsuarioDao()
    
    try:
        funcionarios = usuariodao.getFuncionariosSinUsuario()
        
        return jsonify({
            'success': True,
            'data': funcionarios,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener funcionarios sin usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# VALIDAR USERNAME DISPONIBLE
# ============================================
@usuarioapi.route('/usuarios/validar-username', methods=['POST'])
def validarUsername():
    """Valida que un username esté disponible"""
    data = request.get_json()
    usuariodao = UsuarioDao()
    
    username = data.get('username')
    id_usuario = data.get('id_usuario')  # Para edición
    
    if not username:
        return jsonify({
            'success': False,
            'error': 'El username es requerido'
        }), 400
    
    try:
        disponible = usuariodao.validarUsernameDisponible(username, id_usuario)
        
        return jsonify({
            'success': True,
            'data': {'disponible': disponible},
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al validar username: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al validar el username.'
        }), 500


# ============================================
# CREAR NUEVO USUARIO
# ============================================
@usuarioapi.route('/usuarios', methods=['POST'])
def addUsuario():
    """Crea un nuevo usuario - SOLO Superadministrador"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    
    # Validar que el usuario actual puede crear usuarios
    if not roles_service.puede_crear_usuario():
        return jsonify({
            'success': False,
            'error': 'No tienes permisos para crear usuarios. Solo el Superadministrador puede crear usuarios.'
        }), 403
    
    data = request.get_json()
    usuariodao = UsuarioDao()
    
    # Campos obligatorios
    campos_requeridos = ['username', 'password', 'id_funcionario', 'id_grupo']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    # Validar que puede asignar el rol seleccionado
    id_grupo = data.get('id_grupo')
    if not roles_service.puede_asignar_rol(session.get('id_usuario'), id_grupo):
        return jsonify({
            'success': False,
            'error': 'No tienes permisos para asignar el rol seleccionado.'
        }), 403
    
    # Validar longitud de contraseña
    if len(data['password']) < 6:
        return jsonify({
            'success': False,
            'error': 'La contraseña debe tener al menos 6 caracteres.'
        }), 400
    
    # Validar confirmación de contraseña
    if data.get('password') != data.get('password_confirmacion'):
        return jsonify({
            'success': False,
            'error': 'Las contraseñas no coinciden.'
        }), 400
    
    try:
        usuario_id = usuariodao.guardarUsuario(
            username=data['username'],
            password=data['password'],
            id_funcionario=data['id_funcionario'],
            id_grupo=data['id_grupo'],
            usu_estado=data.get('usu_estado', True),
            creacion_usuario=session.get('id_usuario', 1)
        )
        
        if usuario_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_usuario': usuario_id,
                    'mensaje': 'Usuario creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear el usuario. Verifique que el username no exista o que el funcionario no tenga usuario asignado.'
            }), 500
    
    except Exception as e:
        app.logger.error(f"Error al crear usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


# ============================================
# ACTUALIZAR USUARIO EXISTENTE
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>', methods=['PUT'])
def updateUsuario(id_usuario):
    """Actualiza un usuario existente"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    data = request.get_json()
    usuariodao = UsuarioDao()
    
    # Verificar que el usuario existe
    usuario_existente = usuariodao.getUsuarioById(id_usuario)
    if not usuario_existente:
        return jsonify({
            'success': False,
            'error': 'No se encontró el usuario con el ID proporcionado.'
        }), 404
    
    # Campos obligatorios
    if not data.get('username') or not data.get('id_grupo'):
        return jsonify({
            'success': False,
            'error': 'Username y grupo son obligatorios.'
        }), 400
    
    # Validar que puede editar este usuario específico
    id_grupo_usuario_editado = usuario_existente.get('id_grupo')
    
    # Si el usuario a editar tiene rol de Admin o Superadmin
    id_grupo_superadmin = roles_service.obtener_id_grupo_superadmin()
    id_grupo_admin = roles_service.obtener_id_grupo_admin()
    
    if id_grupo_usuario_editado in [id_grupo_superadmin, id_grupo_admin]:
        # Solo Superadministrador puede editar usuarios Admin/Superadmin
        if not roles_service.es_superadmin(session.get('id_grupo')):
            return jsonify({
                'success': False,
                'error': 'No tienes permisos para editar usuarios con rol de Administrador o Superadministrador.'
            }), 403
    
    # Validar que puede asignar el rol seleccionado
    nuevo_id_grupo = data.get('id_grupo')
    if nuevo_id_grupo:
        if not roles_service.puede_asignar_rol(session.get('id_usuario'), nuevo_id_grupo):
            return jsonify({
                'success': False,
                'error': 'No tienes permisos para asignar el rol seleccionado.'
            }), 403
        
        # Validar que no intente cambiar a Admin/Superadmin si no es Superadmin
        if nuevo_id_grupo in [id_grupo_superadmin, id_grupo_admin]:
            if not roles_service.es_superadmin(session.get('id_grupo')):
                return jsonify({
                    'success': False,
                    'error': 'Solo el Superadministrador puede asignar roles de Administrador o Superadministrador.'
                }), 403
    
    # Si hay contraseña, validar (solo Superadmin puede cambiar contraseñas)
    password = None
    if data.get('password'):
        if not roles_service.puede_crear_usuario():
            return jsonify({
                'success': False,
                'error': 'Solo el Superadministrador puede cambiar contraseñas de usuarios.'
            }), 403
        
        if len(data['password']) < 6:
            return jsonify({
                'success': False,
                'error': 'La contraseña debe tener al menos 6 caracteres.'
            }), 400
        
        if data.get('password') != data.get('password_confirmacion'):
            return jsonify({
                'success': False,
                'error': 'Las contraseñas no coinciden.'
            }), 400
        
        password = data['password']
    
    try:
        resultado = usuariodao.updateUsuario(
            id_usuario=id_usuario,
            username=data['username'],
            id_grupo=data['id_grupo'],
            usu_estado=data.get('usu_estado', True),
            password=password,
            modificacion_usuario=session.get('id_usuario', 1)
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {
                    'id_usuario': id_usuario,
                    'mensaje': 'Usuario actualizado exitosamente'
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el usuario. Verifique que el username no esté en uso.'
            }), 500
    
    except Exception as e:
        app.logger.error(f"Error al actualizar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


# ============================================
# DESACTIVAR USUARIO (SOFT DELETE)
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/desactivar', methods=['PATCH'])
def desactivarUsuario(id_usuario):
    """Desactiva un usuario (soft delete)"""
    usuariodao = UsuarioDao()
    
    try:
        if usuariodao.desactivarUsuario(id_usuario):
            return jsonify({
                'success': True,
                'mensaje': f'Usuario {id_usuario} desactivado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo desactivar el usuario.'
            }), 500
    
    except Exception as e:
        app.logger.error(f"Error al desactivar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# RESETEAR INTENTOS DE LOGIN
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/resetear-intentos', methods=['PATCH'])
def resetearIntentos(id_usuario):
    """Resetea el contador de intentos fallidos de login"""
    usuariodao = UsuarioDao()
    
    try:
        if usuariodao.resetearIntentos(id_usuario):
            return jsonify({
                'success': True,
                'mensaje': f'Intentos reseteados para usuario {id_usuario}.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo resetear los intentos.'
            }), 500
    
    except Exception as e:
        app.logger.error(f"Error al resetear intentos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER ROLES PERMITIDOS PARA ASIGNAR
# ============================================
@usuarioapi.route('/usuarios/roles-permitidos', methods=['GET'])
def getRolesPermitidos():
    """Obtiene la lista de roles que el usuario actual puede asignar"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    
    try:
        roles_permitidos = roles_service.obtener_roles_permitidos()
        
        return jsonify({
            'success': True,
            'data': roles_permitidos,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener roles permitidos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ============================================
# VERIFICAR SI PUEDE CREAR USUARIOS
# ============================================
@usuarioapi.route('/usuarios/puede-crear', methods=['GET'])
def puedeCrearUsuario():
    """Verifica si el usuario actual puede crear usuarios"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    
    try:
        puede_crear = roles_service.puede_crear_usuario()
        
        return jsonify({
            'success': True,
            'data': {
                'puede_crear': puede_crear
            },
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al verificar permisos de creación: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ============================================
# OBTENER ROLES DE UN USUARIO
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/roles', methods=['GET'])
def getRolesUsuario(id_usuario):
    """Obtiene todos los roles activos de un usuario"""
    usuariodao = UsuarioDao()
    
    try:
        roles = usuariodao.obtener_roles_usuario(id_usuario)
        
        return jsonify({
            'success': True,
            'data': roles,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener roles del usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ============================================
# ASIGNAR ROL ADICIONAL A USUARIO
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/roles', methods=['POST'])
def asignarRolUsuario(id_usuario):
    """Asigna un rol adicional a un usuario"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    data = request.get_json()
    usuariodao = UsuarioDao()
    
    # Validar campos
    if not data.get('id_grupo'):
        return jsonify({
            'success': False,
            'error': 'El campo id_grupo es obligatorio.'
        }), 400
    
    id_grupo = data.get('id_grupo')
    es_principal = data.get('es_principal', False)
    
    # Validar permisos
    if not roles_service.puede_asignar_rol(session.get('id_usuario'), id_grupo):
        return jsonify({
            'success': False,
            'error': 'No tienes permisos para asignar este rol.'
        }), 403
    
    try:
        id_usuario_rol = usuariodao.asignar_rol_usuario(
            id_usuario=id_usuario,
            id_grupo=id_grupo,
            es_principal=es_principal,
            asignado_por=session.get('id_usuario')
        )
        
        if id_usuario_rol:
            return jsonify({
                'success': True,
                'data': {
                    'id_usuario_rol': id_usuario_rol,
                    'mensaje': 'Rol asignado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo asignar el rol. Verifique que el usuario no tenga ya 3 roles activos o que el rol no esté ya asignado.'
            }), 400
    
    except Exception as e:
        app.logger.error(f"Error al asignar rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


# ============================================
# REMOVER ROL DE USUARIO
# ============================================
@usuarioapi.route('/usuarios/<int:id_usuario>/roles/<int:id_grupo>', methods=['DELETE'])
def removerRolUsuario(id_usuario, id_grupo):
    """Remueve un rol de un usuario"""
    from flask import session
    from app.services.roles_service import RolesService
    
    roles_service = RolesService()
    usuariodao = UsuarioDao()
    
    # Validar permisos
    if not roles_service.puede_asignar_rol(session.get('id_usuario'), id_grupo):
        return jsonify({
            'success': False,
            'error': 'No tienes permisos para remover este rol.'
        }), 403
    
    try:
        resultado = usuariodao.remover_rol_usuario(id_usuario, id_grupo)
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {
                    'mensaje': 'Rol removido exitosamente'
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo remover el rol. Verifique que el usuario tenga más de un rol activo.'
            }), 400
    
    except Exception as e:
        app.logger.error(f"Error al remover rol: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500