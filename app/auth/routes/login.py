from flask import Blueprint, render_template, session, \
    request, redirect, url_for, flash, current_app as app
from app.auth.services.auth_service import AuthService
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion

logmod = Blueprint('login', __name__, template_folder='../templates')


# FUNCIÓN NUEVA AÑADIDA - SIN MODIFICAR NADA MÁS
def verificar_sesion():
    """Función para verificar si hay una sesión activa"""
    return 'usu_nick' in session


@logmod.route('/login', methods=['GET', 'POST'])
def login():
    """
    Login mejorado usando AuthService
    Mantiene compatibilidad con formularios HTML tradicionales
    """
    if request.method == 'POST':
        # datos del form
        usuario_nombre = request.form.get('usuario_nombre')
        usuario_clave = request.form.get('usuario_clave')

        if not usuario_nombre or not usuario_clave:
            flash('Usuario y contraseña son requeridos', 'danger')
            return redirect(url_for('login.login'))

        # Usar servicio de autenticación mejorado
        exitoso, datos_usuario, mensaje = AuthService.login(
            usuario_nombre=usuario_nombre,
            password=usuario_clave
        )

        if exitoso:
            # Guardar en sesión Flask
            session.clear()
            session.permanent = True
            session['id_usuario'] = datos_usuario['id_usuario']
            
            AuditoriaDao().registrar_evento(
                id_usuario=datos_usuario['id_usuario'],
                accion=AuditAccion.LOGIN,
                detalle=f"Login exitoso desde {request.remote_addr}",
                ip_origen=request.remote_addr
            )
            session['usu_nick'] = datos_usuario['usu_nick']
            session['nombre_persona'] = datos_usuario['nombre_completo']
            session['grupo'] = datos_usuario['grupo']
            session['roles'] = datos_usuario.get('roles', [])
            session['id_funcionario'] = datos_usuario.get('id_funcionario')
            session['session_token'] = datos_usuario.get('session_token')
            
            # Mostrar advertencias si existen
            advertencias = datos_usuario.get('advertencias', {})
            if advertencias.get('password_expira_en_dias'):
                flash(f'Su contraseña expira en {advertencias["password_expira_en_dias"]} días', 'warning')
            
            return redirect(url_for('login.inicio'))
        else:
            id_usuario_audit = datos_usuario.get('id_usuario', 0) if datos_usuario else 0
            AuditoriaDao().registrar_evento(
                id_usuario=id_usuario_audit,
                accion=AuditAccion.LOGIN_FAILED,
                detalle=f"Intento fallido (usuario intentado: '{usuario_nombre}')",
                ip_origen=request.remote_addr
            )
            
            # Verificar si requiere cambio de password
            if datos_usuario and 'requiere_cambio_password' in datos_usuario:
                flash('Debe cambiar su contraseña antes de continuar', 'warning')
                # Redirigir a página de cambio de contraseña
                # return redirect(url_for('auth.cambiar_password'))
            
            flash(mensaje, 'danger')
            return redirect(url_for('login.login'))

    # si es GET
    return render_template('login.html')


@logmod.route('/logout')
def logout():
    """
    Logout mejorado que cierra sesión en BD
    """
    session_token = session.get('session_token')
    
    id_usuario = session.get('id_usuario')
    if id_usuario:
        AuditoriaDao().registrar_evento(
            id_usuario=id_usuario,
            accion=AuditAccion.LOGOUT,
            detalle=f"Logout explícito desde {request.remote_addr}",
            ip_origen=request.remote_addr
        )
    
    if session_token:
        AuthService.cerrar_sesion(session_token, tipo_cierre='LOGOUT')
    
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login.login'))


@logmod.route('/')
def inicio():
    if 'usu_nick' in session:
        return render_template('inicio.html',
                               usuario=session.get('nombre_persona'),
                               grupo=session.get('grupo'))
    else:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login.login'))