"""
Helper para obtener información del especialista del usuario logueado
"""
from flask import session, current_app as app
from app.conexion.Conexion import Conexion


def obtener_id_especialista_usuario():
    """
    Obtiene el id_especialista del usuario logueado
    Funciona incluso si el usuario tiene múltiples roles (ej: Admin + Especialista)
    
    Returns:
        int|None: id_especialista si el usuario tiene un funcionario asociado que es especialista, None en caso contrario
    """
    usuario_id = session.get('id_usuario')
    grupo_id = session.get('id_grupo')
    
    app.logger.info(f"DEBUG especialista_helper: grupo_id={grupo_id}, usuario_id={usuario_id}")
    
    if not usuario_id:
        app.logger.info(f"DEBUG especialista_helper: Falta usuario_id")
        return None
    
    conexion = Conexion()
    con = conexion.getConexion()
    cur = con.cursor()
    
    try:
        # Buscar si el usuario tiene un funcionario asociado que sea especialista
        # Esto funciona independientemente del grupo_id (permite Admin+Especialista, etc.)
        cur.execute("""
            SELECT e.id_especialista 
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN usuarios u ON u.id_funcionario = f.id_funcionario
            WHERE u.id_usuario = %s
        """, (usuario_id,))
        
        resultado = cur.fetchone()
        if resultado:
            id_especialista = resultado[0]
            app.logger.info(f"DEBUG especialista_helper: id_especialista encontrado={id_especialista} (usuario con grupo_id={grupo_id})")
            return id_especialista
        app.logger.warning(f"DEBUG especialista_helper: No se encontró especialista para usuario_id={usuario_id} (grupo_id={grupo_id})")
        return None
        
    except Exception as e:
        app.logger.error(f"Error al obtener id_especialista: {str(e)}", exc_info=True)
        return None
    finally:
        cur.close()
        con.close()


def es_especialista():
    """
    Verifica si el usuario logueado es especialista
    Verifica tanto por grupo_id como por existencia de registro en especialistas
    
    Returns:
        bool: True si es especialista (por grupo o por tener registro), False en caso contrario
    """
    grupo_id = session.get('id_grupo')
    usuario_id = session.get('id_usuario')
    
    # Si el grupo_id es 3, definitivamente es especialista
    if grupo_id == 3:
        return True
    
    # Si no, verificar si tiene un registro en especialistas (permite Admin+Especialista, etc.)
    if usuario_id:
        id_especialista = obtener_id_especialista_usuario()
        return id_especialista is not None
    
    return False


def puede_ver_todos_pacientes():
    """
    Verifica si el usuario puede ver todos los pacientes
    (Admin o Recepcionista)
    
    Returns:
        bool: True si puede ver todos, False si solo sus pacientes
    """
    grupo_id = session.get('id_grupo')
    puede_ver = grupo_id in [1, 2]
    app.logger.info(f"DEBUG puede_ver_todos_pacientes: grupo_id={grupo_id}, puede_ver={puede_ver}")
    # Admin (1) y Recepcionista (2) ven todos
    return puede_ver

