import time
from datetime import date, datetime
from flask import Blueprint, render_template, session, \
    request, redirect, url_for, flash, current_app as app
from app.auth.services.auth_service import AuthService
from app.auth.utils.password_validator import validar_politica_password
from app.dao.auth.auth_dao import AuthDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao
from app.dao.ventas.movimientos.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao
from app.dao.ventas.movimientos.factura.FacturaDao import FacturaDao
from app.dao.agendamiento.lista_espera.ListaEsperaDao import ListaEsperaDao
from app.dao.reporte.ReporteDao import ReporteDao
from app.core.moneda import get_moneda, formatear

logmod = Blueprint('login', __name__, template_folder='../templates')

COOKIE_DISPOSITIVO_CONFIABLE = 'mfa_trust'
COOKIE_RECORDAR_USUARIO = 'recordar_usuario'
RECORDAR_USUARIO_DIAS = 30


def _aplicar_recordarme(response, usuario_nombre, recordar):
    """'Recordarme': guarda SOLO el nombre de usuario (nunca la contraseña) en
    una cookie de 30 días para precargarlo en el próximo login. Si el checkbox
    viene destildado, borra la cookie."""
    if recordar and usuario_nombre:
        response.set_cookie(
            COOKIE_RECORDAR_USUARIO, usuario_nombre.strip(),
            max_age=RECORDAR_USUARIO_DIAS * 24 * 60 * 60,
            httponly=True, samesite='Lax'
        )
    else:
        response.delete_cookie(COOKIE_RECORDAR_USUARIO)
    return response


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
        inicio_login = time.perf_counter()
        exitoso, datos_usuario, mensaje = AuthService.login(
            usuario_nombre=usuario_nombre,
            password=usuario_clave,
            token_dispositivo=request.cookies.get(COOKIE_DISPOSITIVO_CONFIABLE)
        )
        # Duración del procesamiento del login (verificación de clave, bloqueos,
        # sesión). Solo el nombre de usuario y la IP: nunca la contraseña.
        if exitoso:
            resultado = 'OK'
        elif datos_usuario and (datos_usuario.get('requiere_mfa') or datos_usuario.get('requiere_vincular_correo')):
            resultado = 'PASO_MFA'
        else:
            resultado = 'FALLIDO'
        app.logger.info(
            f"LOGIN_TIEMPO usuario='{usuario_nombre}' resultado={resultado} "
            f"duracion_ms={(time.perf_counter() - inicio_login) * 1000:.0f} ip={request.remote_addr}"
        )

        recordar = request.form.get('recordar') == '1'

        if exitoso:
            _iniciar_sesion_flask(datos_usuario)
            response = redirect(url_for('login.inicio'))
            if datos_usuario.get('mfa_habilitado'):
                response = _emitir_dispositivo_confiable(response, datos_usuario['id_usuario'])
            return _aplicar_recordarme(response, usuario_nombre, recordar)

        if datos_usuario and datos_usuario.get('requiere_vincular_correo'):
            # Password correcta, tiene MFA habilitado pero no tiene correo registrado
            session['mfa_pendiente_id_usuario'] = datos_usuario['id_usuario']
            flash(mensaje, 'info')
            return _aplicar_recordarme(redirect(url_for('login.vincular_correo')), usuario_nombre, recordar)

        if datos_usuario and datos_usuario.get('requiere_mfa'):
            # Password correcta, falta el código de verificación por correo
            session['mfa_pendiente_id_usuario'] = datos_usuario['id_usuario']
            flash(mensaje, 'info')
            return _aplicar_recordarme(redirect(url_for('login.verificar_mfa')), usuario_nombre, recordar)

        id_usuario_audit = datos_usuario.get('id_usuario', 0) if datos_usuario else 0
        AuditoriaDao().registrar_evento(
            id_usuario=id_usuario_audit,
            accion=AuditAccion.LOGIN_FAILED,
            detalle=f"Intento fallido (usuario intentado: '{usuario_nombre}')",
            ip_origen=request.remote_addr
        )

        # Contraseña correcta, pero debe cambiarla (generada por el administrador o vencida):
        # no hay sesión todavía, solo el usuario pendiente de cambio
        if datos_usuario and (datos_usuario.get('requiere_cambio_password') or datos_usuario.get('password_expirada')):
            session['cambio_pendiente_id_usuario'] = datos_usuario['id_usuario']
            session['cambio_pendiente_nick'] = datos_usuario['usu_nick']
            flash(mensaje, 'info')
            return _aplicar_recordarme(redirect(url_for('login.cambiar_password_obligatorio')),
                                       usuario_nombre, recordar)

        flash(mensaje, 'danger')
        return redirect(url_for('login.login'))

    # si es GET
    usuario_recordado = request.cookies.get(COOKIE_RECORDAR_USUARIO, '')
    return render_template('login.html', usuario_recordado=usuario_recordado)


@logmod.route('/login/cambiar-password', methods=['GET', 'POST'])
def cambiar_password_obligatorio():
    """Cambio de contraseña obligatorio en el primer ingreso (la generó el administrador) o cuando
    venció. Se llega desde el login, con la contraseña actual ya verificada (ver AuthService.login,
    pasos 5 y 6); todavía no hay sesión."""
    id_usuario = session.get('cambio_pendiente_id_usuario')
    nick = session.get('cambio_pendiente_nick')
    if not id_usuario or not nick:
        flash('Inicie sesión nuevamente', 'warning')
        return redirect(url_for('login.login'))

    if request.method == 'POST':
        actual = request.form.get('password_actual') or ''
        nueva = request.form.get('password_nueva') or ''
        confirmacion = request.form.get('password_confirmacion') or ''

        if nueva != confirmacion:
            flash('La nueva contraseña y su confirmación no coinciden', 'danger')
            return redirect(url_for('login.cambiar_password_obligatorio'))
        if nueva == actual:
            flash('La nueva contraseña debe ser distinta de la actual', 'danger')
            return redirect(url_for('login.cambiar_password_obligatorio'))

        usuario = AuthService.buscar_usuario_seguridad(nick)
        if not usuario:
            flash('Inicie sesión nuevamente', 'warning')
            return redirect(url_for('login.login'))

        valido, mensaje = validar_politica_password(password=nueva, usuario_data=usuario, username=nick)
        if not valido:
            flash(mensaje, 'danger')
            return redirect(url_for('login.cambiar_password_obligatorio'))

        exitoso, mensaje = AuthDao().cambiar_password(
            id_usuario=id_usuario, password_actual=actual, password_nueva=nueva,
            password_hash_actual=usuario['usu_clave'])
        if not exitoso:
            flash(mensaje, 'danger')
            return redirect(url_for('login.cambiar_password_obligatorio'))

        AuditoriaDao().registrar_evento(
            id_usuario=id_usuario,
            accion=AuditAccion.PASSWORD_CHANGE,
            detalle="Cambio de contraseña obligatorio en el ingreso",
            ip_origen=request.remote_addr
        )
        session.pop('cambio_pendiente_id_usuario', None)
        session.pop('cambio_pendiente_nick', None)
        flash('Contraseña actualizada. Ingrese con su nueva contraseña.', 'info')
        return redirect(url_for('login.login'))

    return render_template('cambiar-password.html', usuario=nick)


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
    {'cod': 'ADMINISTRADOR', 'label': 'Administrador', 'icon': 'fa-gauge-high', 'color': '#3f3dc4'},
    {'cod': 'CLINICO', 'label': 'Clínico', 'icon': 'fa-stethoscope', 'color': '#0e7490'},
    {'cod': 'RECEPCION', 'label': 'Recepción', 'icon': 'fa-headset', 'color': '#0f766e'},
    {'cod': 'VENTAS', 'label': 'Ventas', 'icon': 'fa-cash-register', 'color': '#475569'},
]


def _moneda_local():
    """Moneda local para formatear los totales del dashboard (mismo criterio que ReporteDao)."""
    try:
        return get_moneda()
    except Exception:
        return {'decimales_moneda': 0, 'es_moneda_local': True, 'simbolo_moneda': 'Gs.'}


def _citas_por_estado(fecha, id_especialista=None):
    """{cod_estado_cita: cantidad} del día, reusando la estadística de Reportes."""
    filas = ReporteDao().getAgendamientoReport(fecha, fecha, id_especialista)
    return {f['estado']: f['cantidad'] for f in filas}


def _panel_administrador(hoy, moneda, soporte=False):
    """Cifras del día para el Administrador. La cuenta de soporte (Superadministrador) no ve datos de pacientes ni de
    ventas: recibe el panel vacío, marcado con 'soporte'."""
    panel = {'soporte': soporte, 'citas': {}, 'citas_total': 0, 'ventas': {}, 'cajas_abiertas': 0, 'cajas_total': 0,
             'cxc': {}, 'vencidas': [], 'seguridad': {}, 'recordatorios_pendientes': 0,
             'lista_espera': 0, 'consultas_abiertas': 0}
    if soporte:
        return panel
    try:
        reporte_dao = ReporteDao()
        panel['citas'] = _citas_por_estado(hoy)
        panel['citas_total'] = sum(panel['citas'].values())

        ventas = reporte_dao.getVentasDia(hoy)
        ventas['facturado_fmt'] = formatear(ventas['facturado'], moneda)
        panel['ventas'] = ventas

        cajas = AperturaCierreCajaDao().getEstadoCajas()
        panel['cajas_total'] = len(cajas)
        panel['cajas_abiertas'] = sum(1 for c in cajas if c.get('id_apertura_cierre'))

        cxc = reporte_dao.getResumenCuentasCobrar()
        cxc['monto_pendiente_fmt'] = formatear(cxc['monto_pendiente'], moneda)
        panel['cxc'] = cxc
        panel['vencidas'] = CuentaCobrarDao().getCuentasVencidas(limite=5)
        for v in panel['vencidas']:
            v['monto_pendiente_fmt'] = formatear(v['monto_pendiente'], v)

        panel['seguridad'] = reporte_dao.getResumenSeguridad(horas=24)
        panel['recordatorios_pendientes'] = len(RecordatorioDao().getPendientesEnVentana(limite=100))
        panel['lista_espera'] = len(ListaEsperaDao().getListaEspera())
        panel['consultas_abiertas'] = reporte_dao.getResumenConsultas(hoy)['abiertas']
    except Exception as e:
        app.logger.error(f"Error al construir panel de administrador: {str(e)}")
    return panel


def _panel_clinico(hoy):
    panel = {'sin_especialista': True, 'citas': [], 'proxima': None, 'atendidos': 0,
             'pendientes': 0, 'hora_fin': None, 'consultas': {'consultas_dia': 0, 'abiertas': 0}}
    try:
        id_funcionario = session.get('id_funcionario')
        if id_funcionario:
            cita_dao = CitaDao()
            id_especialista = cita_dao.getEspecialistaPorFuncionario(id_funcionario)
            if id_especialista:
                panel['sin_especialista'] = False
                citas = cita_dao.getCitasHoyByEspecialista(id_especialista)
                panel['citas'] = citas
                panel['atendidos'] = sum(1 for c in citas if c['cod_estado_cita'] == 'COMPLETADA')
                panel['pendientes'] = sum(1 for c in citas
                                          if c['cod_estado_cita'] in ('AGENDADA', 'CONFIRMADA', 'EN_CONSULTA'))
                panel['hora_fin'] = citas[-1]['cita_hora_fin'] if citas else None
                # Próximo paciente: la consulta en curso o la primera cita por atender desde ahora
                ahora = datetime.now().strftime('%H:%M')
                panel['proxima'] = (
                    next((c for c in citas if c['cod_estado_cita'] == 'EN_CONSULTA'), None)
                    or next((c for c in citas if c['cod_estado_cita'] in ('AGENDADA', 'CONFIRMADA')
                             and c['cita_hora_fin'] >= ahora), None))
                panel['consultas'] = ReporteDao().getResumenConsultas(hoy, id_especialista)
    except Exception as e:
        app.logger.error(f"Error al construir panel clínico: {str(e)}")
    return panel


def _panel_recepcion(hoy):
    panel = {'citas': [], 'por_estado': {}, 'especialistas': 0, 'recordatorios_pendientes': 0,
             'lista_espera': []}
    try:
        # hasta = fin del día: cita_inicio es TIMESTAMP y la fecha sola cortaba a las 00:00
        citas = CitaDao().getCitas(desde=hoy, hasta=f"{hoy} 23:59:59")
        for c in citas:
            c['hora'] = c['cita_inicio'].split(' ')[1] if c.get('cita_inicio') else ''
            panel['por_estado'][c['cod_estado_cita']] = panel['por_estado'].get(c['cod_estado_cita'], 0) + 1
        panel['citas'] = citas
        panel['especialistas'] = len({c['id_especialista'] for c in citas})
        panel['recordatorios_pendientes'] = len(RecordatorioDao().getPendientesEnVentana(limite=100))
        panel['lista_espera'] = ListaEsperaDao().getListaEspera()
    except Exception as e:
        app.logger.error(f"Error al construir panel de recepción: {str(e)}")
    return panel


def _panel_ventas(hoy, moneda):
    panel = {'caja_abierta': None, 'cajas_total': 0, 'ventas': {}, 'cxc': {}, 'vencidas': [],
             'facturas': []}
    try:
        reporte_dao = ReporteDao()
        cajas = AperturaCierreCajaDao().getEstadoCajas()
        panel['cajas_total'] = len(cajas)
        panel['caja_abierta'] = next((c for c in cajas if c.get('id_apertura_cierre')), None)

        ventas = reporte_dao.getVentasDia(hoy)
        ventas['facturado_fmt'] = formatear(ventas['facturado'], moneda)
        ventas['cobrado_fmt'] = formatear(ventas['cobrado'], moneda)
        ventas['porcentaje_cobrado'] = (round(ventas['cobrado'] * 100 / ventas['facturado'])
                                        if ventas['facturado'] else 0)
        panel['ventas'] = ventas

        cxc = reporte_dao.getResumenCuentasCobrar()
        cxc['monto_pendiente_fmt'] = formatear(cxc['monto_pendiente'], moneda)
        cxc['monto_vencido_fmt'] = formatear(cxc['monto_vencido'], moneda)
        panel['cxc'] = cxc

        panel['vencidas'] = CuentaCobrarDao().getCuentasVencidas(limite=5)
        for v in panel['vencidas']:
            v['monto_pendiente_fmt'] = formatear(v['monto_pendiente'], v)
        panel['facturas'] = FacturaDao().getUltimasFacturas(limite=5)
        for f in panel['facturas']:
            f['total_fmt'] = formatear(f['factura_total'], f)
    except Exception as e:
        app.logger.error(f"Error al construir panel de ventas: {str(e)}")
    return panel


def _construir_datos_dashboard(roles):
    """Arma las pestañas visibles y los datos de cada panel del dashboard de
    inicio. Las cifras salen de las estadísticas reutilizables de ReporteDao y
    de los DAOs de cada módulo. Cada panel se protege individualmente para que
    un módulo caído no tumbe el resto del dashboard."""
    es_admin = 'ADMINISTRADOR' in roles or 'SUPERADMIN' in roles
    codigos_visibles = {'ADMINISTRADOR'} if es_admin else set()
    codigos_visibles |= {r for r in roles if r in ('CLINICO', 'RECEPCION', 'VENTAS')}

    roles_visibles = [r for r in ROLES_DASHBOARD_META if r['cod'] in codigos_visibles]
    if 'ADMINISTRADOR' not in roles and 'SUPERADMIN' in roles:   # cuenta de soporte: su propio banner
        roles_visibles = [dict(r, label='de soporte', icon='fa-screwdriver-wrench', color='#475569')
                          if r['cod'] == 'ADMINISTRADOR' else r for r in roles_visibles]
    hoy = date.today().isoformat()
    moneda = _moneda_local()
    data_por_rol = {}

    if 'ADMINISTRADOR' in codigos_visibles:
        data_por_rol['ADMINISTRADOR'] = _panel_administrador(hoy, moneda, soporte='ADMINISTRADOR' not in roles)
    if 'CLINICO' in codigos_visibles:
        data_por_rol['CLINICO'] = _panel_clinico(hoy)
    if 'RECEPCION' in codigos_visibles:
        data_por_rol['RECEPCION'] = _panel_recepcion(hoy)
    if 'VENTAS' in codigos_visibles:
        data_por_rol['VENTAS'] = _panel_ventas(hoy, moneda)

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