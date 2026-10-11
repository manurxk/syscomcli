from datetime import date
from flask import Blueprint, render_template, session, \
    request, redirect, url_for, flash, current_app as app
from app.auth.services.auth_service import AuthService
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.dao.ventas.movimientos.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao
from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao

logmod = Blueprint('login', __name__, template_folder='../templates')

COOKIE_DISPOSITIVO_CONFIABLE = 'mfa_trust'


def _emitir_dispositivo_confiable(response, id_usuario):
    """Emite/renueva la cookie de 'dispositivo confiable' (60 días) tras un
    login con MFA validado (código correcto, o dispositivo ya confiable), para
    que el próximo login desde este mismo navegador se salte el código
    mientras la cookie no venza. Ver AuthService.DISPOSITIVO_CONFIABLE_DIAS.
    Revoca el token anterior de este mismo navegador (si traía uno) para que
    no quede 'Vigente' para siempre junto al nuevo."""
    AuthService.revocar_dispositivo_confiable_por_token(request.cookies.get(COOKIE_DISPOSITIVO_CONFIABLE))
    token = AuthService.crear_dispositivo_confiable(
        id_usuario, request.remote_addr, request.headers.get('User-Agent', '')
    )
    response.set_cookie(
        COOKIE_DISPOSITIVO_CONFIABLE, token,
        max_age=AuthService.DISPOSITIVO_CONFIABLE_DIAS * 24 * 60 * 60,
        httponly=True, samesite='Lax'
    )
    return response


# FUNCIÓN NUEVA AÑADIDA - SIN MODIFICAR NADA MÁS
def verificar_sesion():
    """Función para verificar si hay una sesión activa"""
    return 'usu_nick' in session


def _iniciar_sesion_flask(datos_usuario):
    """Vuelca los datos de AuthService en la sesión Flask. Usado por el login
    directo y por la confirmación de MFA (completar_login_mfa)."""
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

    advertencias = datos_usuario.get('advertencias', {})
    if advertencias.get('password_expira_en_dias'):
        flash(f'Su contraseña expira en {advertencias["password_expira_en_dias"]} días', 'warning')


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
            password=usuario_clave,
            token_dispositivo=request.cookies.get(COOKIE_DISPOSITIVO_CONFIABLE)
        )

        if exitoso:
            _iniciar_sesion_flask(datos_usuario)
            response = redirect(url_for('login.inicio'))
            if datos_usuario.get('mfa_habilitado'):
                response = _emitir_dispositivo_confiable(response, datos_usuario['id_usuario'])
            return response

        if datos_usuario and datos_usuario.get('requiere_vincular_correo'):
            # Password correcta, tiene MFA habilitado pero no tiene correo registrado
            session['mfa_pendiente_id_usuario'] = datos_usuario['id_usuario']
            flash(mensaje, 'info')
            return redirect(url_for('login.vincular_correo'))

        if datos_usuario and datos_usuario.get('requiere_mfa'):
            # Password correcta, falta el código de verificación por correo
            session['mfa_pendiente_id_usuario'] = datos_usuario['id_usuario']
            flash(mensaje, 'info')
            return redirect(url_for('login.verificar_mfa'))

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


@logmod.route('/login/recuperar-password', methods=['GET'])
def recuperar_password():
    """Formulario para solicitar la recuperación de contraseña (AJAX contra
    /api/v1/auth/recuperar-password, que ya existe y envía el correo)."""
    return render_template('recuperar-password.html')


@logmod.route('/login/resetear-password', methods=['GET'])
def resetear_password():
    """Formulario para elegir la nueva contraseña a partir del token recibido
    por correo (AJAX contra /api/v1/auth/confirmar-recuperacion)."""
    token = request.args.get('token', '')
    return render_template('resetear-password.html', token=token)


@logmod.route('/login/vincular-correo', methods=['GET', 'POST'])
def vincular_correo():
    """Paso previo al MFA cuando el usuario tiene MFA habilitado pero
    todavía no tiene un correo registrado (ver AuthService.login,
    rama requiere_vincular_correo)."""
    id_usuario = session.get('mfa_pendiente_id_usuario')
    if not id_usuario:
        flash('Inicie sesión nuevamente', 'warning')
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        correo = request.form.get('correo')
        exitoso, mensaje = AuthService.vincular_correo_y_enviar_mfa(id_usuario, correo)

        if exitoso:
            flash(mensaje, 'info')
            return redirect(url_for('login.verificar_mfa'))

        flash(mensaje, 'danger')
        return redirect(url_for('login.vincular_correo'))

    return render_template('vincular-correo.html')


@logmod.route('/login/verificar-mfa', methods=['GET', 'POST'])
def verificar_mfa():
    """Segundo paso del login cuando el usuario tiene MFA habilitado."""
    id_usuario = session.get('mfa_pendiente_id_usuario')
    if not id_usuario:
        flash('Inicie sesión nuevamente', 'warning')
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        codigo = request.form.get('codigo')

        exitoso, datos_usuario, mensaje = AuthService.completar_login_mfa(id_usuario, codigo)

        if exitoso:
            session.pop('mfa_pendiente_id_usuario', None)
            _iniciar_sesion_flask(datos_usuario)
            response = redirect(url_for('login.inicio'))
            response = _emitir_dispositivo_confiable(response, datos_usuario['id_usuario'])
            return response

        flash(mensaje, 'danger')
        return redirect(url_for('login.verificar_mfa'))

    return render_template('verificar-mfa.html')


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


@logmod.route('/idioma/<codigo>')
def cambiar_idioma(codigo):
    """Cambia el idioma de la interfaz (español/guaraní/inglés). Se guarda en
    una cookie de 1 año (no en sesión, para que sobreviva el login/logout).
    Funciona logueado o no — redirige a la página desde la que vino."""
    from app import IDIOMAS_DISPONIBLES
    destino = request.referrer or url_for('login.login')
    response = redirect(destino)
    if codigo in IDIOMAS_DISPONIBLES:
        response.set_cookie('idioma', codigo, max_age=365 * 24 * 60 * 60)
    return response


ROLES_DASHBOARD_META = [
    {'cod': 'ADMINISTRADOR', 'label': 'Administrador', 'icon': 'fa-gauge-high', 'color': '#7c3aed'},
    {'cod': 'CLINICO', 'label': 'Clínico', 'icon': 'fa-stethoscope', 'color': '#9333ea'},
    {'cod': 'RECEPCION', 'label': 'Recepción', 'icon': 'fa-headset', 'color': '#6b21a8'},
    {'cod': 'VENTAS', 'label': 'Ventas', 'icon': 'fa-cash-register', 'color': '#5b21b6'},
]


def _formato_guaranies(monto):
    return f"Gs. {int(monto or 0):,}".replace(',', '.')


def _construir_datos_dashboard(roles):
    """Arma las pestañas visibles y los datos de cada panel del dashboard de
    inicio, reusando los DAOs de cada módulo (mismo patrón que reporteIndex()).
    Cada bloque se protege individualmente para que un módulo caído no tumbe
    el resto del dashboard."""
    es_admin = 'ADMINISTRADOR' in roles or 'SUPERADMIN' in roles
    codigos_visibles = {'ADMINISTRADOR'} if es_admin else set()
    codigos_visibles |= {r for r in roles if r in ('CLINICO', 'RECEPCION', 'VENTAS')}

    roles_visibles = [r for r in ROLES_DASHBOARD_META if r['cod'] in codigos_visibles]
    data_por_rol = {}

    if 'ADMINISTRADOR' in codigos_visibles:
        panel = {'citas_hoy': 0, 'recordatorios_pendientes': 0, 'cajas_abiertas': '0/0',
                 'facturado_hoy_monto': _formato_guaranies(0), 'facturado_hoy_count': 0,
                 'cxc': [], 'intentos_fallidos': 0, 'eventos_auditoria': 0}
        try:
            hoy = date.today().isoformat()
            panel['citas_hoy'] = len(CitaDao().getCitas(desde=hoy, hasta=hoy))
            panel['recordatorios_pendientes'] = len(RecordatorioDao().getPendientesEnVentana(limite=100))

            cajas = AperturaCierreCajaDao().getEstadoCajas()
            abiertas = sum(1 for c in cajas if c.get('id_apertura_cierre'))
            panel['cajas_abiertas'] = f"{abiertas}/{len(cajas)}"

            facturas_hoy = FacturaDao().getFacturasHoy()
            panel['facturado_hoy_count'] = len(facturas_hoy)
            panel['facturado_hoy_monto'] = _formato_guaranies(sum(f['factura_total'] for f in facturas_hoy))

            panel['cxc'] = CuentaCobrarDao().getCuentasCobrarPendientes()[:5]

            panel['intentos_fallidos'] = AuthService.contar_intentos_fallidos_ip(request.remote_addr)
            panel['eventos_auditoria'] = AuditoriaDao().getEventos(pagina=1, por_pagina=5)['total']
        except Exception as e:
            app.logger.error(f"Error al construir panel de administrador: {str(e)}")
        data_por_rol['ADMINISTRADOR'] = panel

    if 'CLINICO' in codigos_visibles:
        panel = {'sin_especialista': True, 'citas': []}
        try:
            id_funcionario = session.get('id_funcionario')
            if id_funcionario:
                cita_dao = CitaDao()
                id_especialista = cita_dao.getEspecialistaPorFuncionario(id_funcionario)
                if id_especialista:
                    panel['sin_especialista'] = False
                    panel['citas'] = cita_dao.getCitasHoyByEspecialista(id_especialista)
        except Exception as e:
            app.logger.error(f"Error al construir panel clínico: {str(e)}")
        data_por_rol['CLINICO'] = panel

    if 'RECEPCION' in codigos_visibles:
        panel = {'citas': [], 'recordatorios_pendientes': 0}
        try:
            hoy = date.today().isoformat()
            panel['citas'] = CitaDao().getCitas(desde=hoy, hasta=hoy)
            panel['recordatorios_pendientes'] = len(RecordatorioDao().getPendientesEnVentana(limite=100))
        except Exception as e:
            app.logger.error(f"Error al construir panel de recepción: {str(e)}")
        data_por_rol['RECEPCION'] = panel

    if 'VENTAS' in codigos_visibles:
        panel = {'cajas_abiertas': '0/0', 'facturado_hoy_monto': _formato_guaranies(0),
                 'facturado_hoy_count': 0, 'cxc': []}
        try:
            cajas = AperturaCierreCajaDao().getEstadoCajas()
            abiertas = sum(1 for c in cajas if c.get('id_apertura_cierre'))
            panel['cajas_abiertas'] = f"{abiertas}/{len(cajas)}"

            facturas_hoy = FacturaDao().getFacturasHoy()
            panel['facturado_hoy_count'] = len(facturas_hoy)
            panel['facturado_hoy_monto'] = _formato_guaranies(sum(f['factura_total'] for f in facturas_hoy))

            panel['cxc'] = CuentaCobrarDao().getCuentasCobrarPendientes()[:5]
        except Exception as e:
            app.logger.error(f"Error al construir panel de ventas: {str(e)}")
        data_por_rol['VENTAS'] = panel

    return roles_visibles, data_por_rol


@logmod.route('/')
def inicio():
    if 'usu_nick' in session:
        roles_visibles, data_por_rol = _construir_datos_dashboard(session.get('roles', []))
        return render_template('inicio.html',
                               usuario=session.get('nombre_persona'),
                               grupo=session.get('grupo'),
                               roles=roles_visibles,
                               data_por_rol=data_por_rol)
    else:
        flash('Debes iniciar sesión primero', 'warning')
        return redirect(url_for('login.login'))