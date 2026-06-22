"""
Servicio para gestión de módulos y permisos por rol
Define qué módulos puede acceder cada rol del sistema
"""
from flask import session, current_app as app
from typing import List, Dict, Set
from app.services.roles_service import RolesService


class ModulosService:
    """Servicio para gestión de módulos accesibles por rol"""
    
    # Definición de módulos por rol
    MODULOS_POR_ROL = {
        'SUPERADMINISTRADOR': {
            'modulos': [
                'dashboard',
                'gestion_clinicas',
                'configuracion_global',
                'gestion_administradores',
                'reportes_consolidados',
                'configuracion_precios_planes',
                'logs_auditoria',
                'respaldos_mantenimiento',
                # También tiene acceso a módulos de Administrador
                'dashboard_admin',
                'gestion_usuarios_clinica',
                'asignacion_roles_permisos',
                'reportes_financieros',
                'configuracion_clinica',
                'gestion_especialistas_agenda',
                'reportes_desempeno',
                'inventario_recursos',
                'configuracion_precios_locales',
            ],
            'widgets_dashboard': [
                'metricas_globales',
                'usuarios_sistema',
                'clinicas_sedes',
                'reportes_consolidados',
            ]
        },
        'ADMINISTRADOR': {
            'modulos': [
                'dashboard',
                'dashboard_admin',
                'gestion_usuarios_clinica',
                'asignacion_roles_permisos',
                'reportes_financieros',
                'configuracion_clinica',
                'gestion_especialistas_agenda',
                'reportes_desempeno',
                'inventario_recursos',
                'configuracion_precios_locales',
                # También puede tener acceso a módulos de otros roles si tiene múltiples roles
            ],
            'widgets_dashboard': [
                'metricas_generales',
                'usuarios_activos',
                'citas_hoy',
                'pacientes_activos',
                'ingresos_mes',
            ]
        },
        'ESPECIALISTA': {
            'modulos': [
                'dashboard',
                'mi_agenda_personal',
                'mis_pacientes_asignados',
                'historias_clinicas',
                'sesiones_programadas',
                'notas_evolucion',
                'planes_tratamiento',
                'documentos_evaluaciones',
                'reportes_mis_pacientes',
                'disponibilidad_horaria',
                'derivaciones',  # Tabla de derivaciones para especialistas
            ],
            'widgets_dashboard': [
                'mis_proximas_citas',
                'pacientes_asignados',
                'derivaciones_pendientes',
                'historias_pendientes',
            ]
        },
        'RECEPCIONISTA': {
            'modulos': [
                'dashboard',
                'agenda_general',
                'crear_modificar_citas',
                'gestion_pacientes',
                'checkin_checkout',
                'confirmar_citas',
                'lista_espera',
                'llamadas_recordatorios',
                'consulta_disponibilidad',
            ],
            'widgets_dashboard': [
                'citas_dia',
                'citas_pendientes',
                'pacientes_hoy',
                'lista_espera',
            ]
        },
        'VENTAS': {
            'modulos': [
                'dashboard',
                'registro_nuevos_pacientes',
                'seguimiento_prospectos',
                'cotizaciones_paquetes',
                'conversiones',
                'gestion_pagos_cobros',
                'facturacion',
                'reportes_ventas',
                'comisiones',
            ],
            'widgets_dashboard': [
                'pipeline_ventas',
                'facturas_mes',
                'ventas_hoy',
                'cuentas_cobrar',
            ]
        },
        'CAJA': {
            'modulos': [
                'dashboard',
                'gestion_pagos_cobros',
                'facturacion',
                'reportes_ventas',
            ],
            'widgets_dashboard': [
                'facturas_mes',
                'ventas_hoy',
                'cuentas_cobrar',
            ]
        }
    }
    # Mapeo de IDs de grupos a nombres (ajustar según tu BD)
    ID_GRUPO_A_NOMBRE = {
        1: 'ADMINISTRADOR',
        2: 'RECEPCIONISTA',
        3: 'ESPECIALISTA',
        4: 'VENTAS',
        5: 'SUPERADMINISTRADOR',
        6: 'CAJA',
    }
    
    def __init__(self):
        self.roles_service = RolesService()
    
    def obtener_roles_usuario(self, id_usuario=None) -> List[Dict]:
        """
        Obtiene todos los roles activos del usuario desde la tabla usuarios_roles
        Soporta múltiples roles por usuario (hasta 3 roles simultáneos)
        
        Args:
            id_usuario: ID del usuario (opcional, usa session si no se proporciona)
        
        Returns:
            List[Dict]: Lista de roles con id_grupo y des_grupo
        """
        from app.dao.auth.user_dao import UsuarioDao
        usuario_dao = UsuarioDao()
        
        # Si no se proporciona id_usuario, usar el de la sesión
        if id_usuario is None:
            id_usuario = session.get('id_usuario')
            if not id_usuario:
                # Fallback: intentar obtener desde id_grupo de la sesión
                id_grupo = session.get('id_grupo')
                grupo_nombre = session.get('grupo', '').upper()
                
                if not id_grupo:
                    return []
                
                # Retornar solo el rol de la sesión como fallback
                return [{
                    'id_grupo': id_grupo,
                    'des_grupo': grupo_nombre
                }]
        
        # Obtener todos los roles activos desde usuarios_roles
        try:
            roles = usuario_dao.obtener_roles_usuario(id_usuario)
            
            if roles:
                # Convertir a formato esperado
                return [{
                    'id_grupo': rol.get('id_grupo'),
                    'des_grupo': rol.get('des_grupo', '').upper()
                } for rol in roles]
            else:
                # Si no hay roles en usuarios_roles, usar fallback a id_grupo del usuario
                usuario = usuario_dao.getUsuarioById(id_usuario)
                
                if not usuario:
                    return []
                
                id_grupo = usuario.get('id_grupo')
                grupo_nombre = usuario.get('grupo', '').upper()
                
                if id_grupo:
                    return [{
                        'id_grupo': id_grupo,
                        'des_grupo': grupo_nombre
                    }]
                
                return []
                
        except Exception as e:
            app.logger.error(f"Error al obtener roles del usuario {id_usuario}: {str(e)}")
            # Fallback: usar id_grupo del usuario
            try:
                usuario = usuario_dao.getUsuarioById(id_usuario)
                if usuario:
                    id_grupo = usuario.get('id_grupo')
                    grupo_nombre = usuario.get('grupo', '').upper()
                    if id_grupo:
                        return [{
                            'id_grupo': id_grupo,
                            'des_grupo': grupo_nombre
                        }]
            except Exception:
                pass
            
            return []
    
    def obtener_nombre_grupo(self, id_grupo: int) -> str:
        """
        Obtiene el nombre del grupo dado su ID
        
        Args:
            id_grupo: ID del grupo
        
        Returns:
            str: Nombre del grupo en mayúsculas
        """
        # Primero intentar desde el mapeo
        nombre = self.ID_GRUPO_A_NOMBRE.get(id_grupo)
        if nombre:
            return nombre
        
        # Si no está en el mapeo, consultar BD
        from app.conexion.Conexion import Conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("""
                SELECT UPPER(des_grupo) 
                FROM grupos 
                WHERE id_grupo = %s AND est_grupo = TRUE
            """, (id_grupo,))
            resultado = cur.fetchone()
            return resultado[0] if resultado else ''
        except Exception as e:
            app.logger.error(f"Error al obtener nombre de grupo: {str(e)}")
            return ''
        finally:
            cur.close()
            con.close()
    
    def obtener_modulos_rol(self, nombre_rol: str) -> List[str]:
        """
        Obtiene los módulos accesibles para un rol específico
        
        Args:
            nombre_rol: Nombre del rol en mayúsculas (ej: 'ADMINISTRADOR')
        
        Returns:
            List[str]: Lista de módulos accesibles
        """
        nombre_rol = nombre_rol.upper()
        modulos_data = self.MODULOS_POR_ROL.get(nombre_rol, {})
        return modulos_data.get('modulos', [])
    
    def obtener_widgets_rol(self, nombre_rol: str) -> List[str]:
        """
        Obtiene los widgets del dashboard para un rol específico
        
        Args:
            nombre_rol: Nombre del rol en mayúsculas
        
        Returns:
            List[str]: Lista de widgets para el dashboard
        """
        nombre_rol = nombre_rol.upper()
        modulos_data = self.MODULOS_POR_ROL.get(nombre_rol, {})
        return modulos_data.get('widgets_dashboard', [])
    
    def obtener_modulos_usuario(self, id_usuario=None) -> Set[str]:
        """
        Obtiene todos los módulos accesibles para el usuario actual
        Si tiene múltiples roles, combina todos los módulos (UNION)
        
        Args:
            id_usuario: ID del usuario (opcional, usa session si no se proporciona)
        
        Returns:
            Set[str]: Conjunto de módulos únicos accesibles
        """
        roles = self.obtener_roles_usuario(id_usuario)
        
        if not roles:
            return set()
        
        modulos_combinados = set()
        
        for rol in roles:
            nombre_rol = rol.get('des_grupo', '').upper()
            modulos_rol = self.obtener_modulos_rol(nombre_rol)
            modulos_combinados.update(modulos_rol)
        
        return modulos_combinados
    
    def obtener_widgets_usuario(self, id_usuario=None) -> Set[str]:
        """
        Obtiene todos los widgets del dashboard para el usuario actual
        Combina widgets de todos sus roles
        
        Args:
            id_usuario: ID del usuario (opcional, usa session si no se proporciona)
        
        Returns:
            Set[str]: Conjunto de widgets únicos para el dashboard
        """
        roles = self.obtener_roles_usuario(id_usuario)
        
        if not roles:
            return set()
        
        widgets_combinados = set()
        
        for rol in roles:
            nombre_rol = rol.get('des_grupo', '').upper()
            widgets_rol = self.obtener_widgets_rol(nombre_rol)
            widgets_combinados.update(widgets_rol)
        
        return widgets_combinados
    
    def tiene_acceso_modulo(self, nombre_modulo: str, id_usuario=None) -> bool:
        """
        Verifica si el usuario tiene acceso a un módulo específico
        
        Args:
            nombre_modulo: Nombre del módulo a verificar
            id_usuario: ID del usuario (opcional, usa session si no se proporciona)
        
        Returns:
            bool: True si tiene acceso, False en caso contrario
        """
        modulos_usuario = self.obtener_modulos_usuario(id_usuario)
        return nombre_modulo in modulos_usuario
    
    def obtener_roles_activos_usuario(self, id_usuario=None) -> List[str]:
        """
        Obtiene lista de nombres de roles activos del usuario
        
        Args:
            id_usuario: ID del usuario (opcional, usa session si no se proporciona)
        
        Returns:
            List[str]: Lista de nombres de roles
        """
        roles = self.obtener_roles_usuario(id_usuario)
        return [rol.get('des_grupo', '').upper() for rol in roles if rol.get('des_grupo')]
    
    def es_superadmin(self, id_usuario=None) -> bool:
        """Verifica si el usuario es Superadministrador"""
        roles = self.obtener_roles_usuario(id_usuario)
        return any(rol.get('des_grupo', '').upper() == 'SUPERADMINISTRADOR' for rol in roles)
    
    def es_admin(self, id_usuario=None) -> bool:
        """Verifica si el usuario es Administrador"""
        roles = self.obtener_roles_usuario(id_usuario)
        return any(rol.get('des_grupo', '').upper() == 'ADMINISTRADOR' for rol in roles)
    
    def es_especialista(self, id_usuario=None) -> bool:
        """
        Verifica si el usuario es Especialista
        Verifica tanto por roles como por existencia de registro en especialistas
        (permite Admin+Especialista, etc.)
        """
        # Primero verificar por roles
        roles = self.obtener_roles_usuario(id_usuario)
        if any(rol.get('des_grupo', '').upper() == 'ESPECIALISTA' for rol in roles):
            return True
        
        # Si no tiene rol ESPECIALISTA, verificar si tiene registro en especialistas
        # Esto permite que un Admin que también es especialista sea detectado
        if id_usuario is None:
            id_usuario = session.get('id_usuario')
        
        if not id_usuario:
            return False
        
        # Verificar si el usuario tiene un funcionario asociado que sea especialista
        try:
            from app.utils.especialista_helper import obtener_id_especialista_usuario
            id_especialista = obtener_id_especialista_usuario()
            return id_especialista is not None
        except Exception as e:
            app.logger.error(f"Error verificando si es especialista: {str(e)}")
            return False
    
    def es_recepcionista(self, id_usuario=None) -> bool:
        """Verifica si el usuario es Recepcionista"""
        roles = self.obtener_roles_usuario(id_usuario)
        return any(rol.get('des_grupo', '').upper() == 'RECEPCIONISTA' for rol in roles)
    
    def es_ventas(self, id_usuario=None) -> bool:
        """Verifica si el usuario es Ventas"""
        roles = self.obtener_roles_usuario(id_usuario)
        return any(rol.get('des_grupo', '').upper() == 'VENTAS' for rol in roles)

    def es_caja(self, id_usuario=None) -> bool:
        """Verifica si el usuario es Caja"""
        roles = self.obtener_roles_usuario(id_usuario)
        return any(rol.get('des_grupo', '').upper() == 'CAJA' for rol in roles)
