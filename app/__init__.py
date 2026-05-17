from datetime import timedelta
import os

from flask import Flask, redirect, request, session, url_for
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

csrf = CSRFProtect()
csrf.init_app(app)

app.secret_key = b'***REMOVED***'
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=60)

# ============================================================================
# CONFIGURACIÓN DE ULTRAMSG (WhatsApp Notifications)
# ============================================================================
# Si no hay variables de entorno, usar valores directos (solo para desarrollo)
# Para producción, usar variables de entorno:
# export ULTRAMSG_INSTANCE_ID="***REMOVED***"
# export ULTRAMSG_TOKEN="***REMOVED***"
app.config['ULTRAMSG_INSTANCE_ID'] = os.getenv('ULTRAMSG_INSTANCE_ID', '***REMOVED***')
app.config['ULTRAMSG_TOKEN'] = os.getenv('ULTRAMSG_TOKEN', '***REMOVED***')
app.config['ULTRAMSG_API_URL'] = os.getenv('ULTRAMSG_API_URL', 'https://api.ultramsg.com')

# Nombre de la clínica para notificaciones (configurable)
app.config['NOMBRE_CLINICA'] = os.getenv('NOMBRE_CLINICA', 'Angasys')

MODULO_REFERENCIALES = "/referenciales"
MODULO_GESTION = "/modulos"
API_V1 = "/api/v1"


@app.context_processor
def inject_csrf_token():
    """Hace disponible csrf_token() en todos los templates."""
    from flask_wtf.csrf import generate_csrf
    from app.config.version import get_version, get_version_full, RELEASE_DATE
    from datetime import datetime

    return dict(
        csrf_token=generate_csrf,
        app_version=get_version(),
        app_version_full=get_version_full(),
        app_release_date=RELEASE_DATE,
        current_year=datetime.now().year
    )


@app.before_request
def require_login():
    """
    Middleware de autenticación mejorado (FASE 2)
    Usa verificar_sesion_mejorada si está disponible, sino usa método tradicional
    """
    # Intentar usar middleware mejorado
    try:
        from app.auth.middleware.auth_middleware import verificar_sesion_mejorada
        resultado = verificar_sesion_mejorada()
        if resultado:
            return resultado
        # Si retorna None, continuar normalmente
    except Exception as e:
        # Si hay error, usar método tradicional (compatibilidad hacia atrás)
        app.logger.warning(f"Error en middleware mejorado, usando método tradicional: {str(e)}")
        
        # Endpoints públicos
        public_endpoints = {
            "login.login", 
            "login.logout", 
            "static",
            "informacion.privacidad",
            "informacion.soporte",
            "informacion.contacto",
            "auth.login",
            "auth.solicitar_recuperacion",
            "auth.confirmar_recuperacion"
        }

        if request.endpoint in public_endpoints or request.endpoint is None:
            return None

        # Permitir archivos estáticos aunque el endpoint sea None
        if request.path.startswith("/static"):
            return None

        if "usu_nick" not in session:
            if request.path.startswith('/api/'):
                from flask import jsonify
                return jsonify({
                    'success': False,
                    'error': 'No autenticado'
                }), 401
            else:
                return redirect(url_for("login.login"))

## ============================================================================
# BLUEPRINTS PRINCIPALES - DASHBOARD Y SEGURIDAD
# ============================================================================

# ✅ DASHBOARD UNIFICADO (con control de sesión, roles y todas las APIs)
from app.rutas.seguridad.dashboard import dashboard
app.register_blueprint(dashboard, url_prefix="/")

# ✅ ERROR HANDLERS
from app.rutas.seguridad.error_handlers import error_bp
app.register_blueprint(error_bp)

# ✅ BÚSQUEDA GLOBAL
from app.rutas.seguridad.busqueda_api import busquedaapi
app.register_blueprint(busquedaapi, url_prefix=API_V1)

# ============================================================================
# COMENTAR O ELIMINAR ESTOS BLUEPRINTS (ya están unificados arriba)
# ============================================================================

# ❌ COMENTAR ESTAS LÍNEAS:
# from app.rutas.dashboard.dashboard.dashboard_routes import dashboardmod
# app.register_blueprint(dashboardmod, url_prefix='/')

# ❌ COMENTAR ESTA LÍNEA:
# from app.rutas.dashboard.dashboard.dashboard_api import dashboardapi
# app.register_blueprint(dashboardapi, url_prefix=API_V1)

# ============================================================================
# BLUEPRINTS - LOGIN Y AUTENTICACIÓN
# ============================================================================

# Autenticación centralizada en app/auth/
from app.auth import login_blueprint, auth_api_blueprint, admin_auth_api_blueprint
app.register_blueprint(login_blueprint)
app.register_blueprint(auth_api_blueprint)
app.register_blueprint(admin_auth_api_blueprint)

# ============================================================================
# BLUEPRINTS - INFORMACIÓN (PÁGINAS PÚBLICAS)
# ============================================================================

from app.rutas.seguridad.informacion.informacion_routes import informacionmod
app.register_blueprint(informacionmod)


# ============================================================================
# BLUEPRINTS - MÓDULOS REFERENCIALES
# ============================================================================

# Ciudad
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
app.register_blueprint(ciumod, url_prefix=f'{MODULO_REFERENCIALES}/ciudad')
app.register_blueprint(ciuapi, url_prefix=API_V1)

# Especialidad
from app.rutas.referenciales.especialidad.especialidad_routes import espmod
from app.rutas.referenciales.especialidad.especialidad_api import espapi
app.register_blueprint(espmod, url_prefix=f'{MODULO_REFERENCIALES}/especialidad')
app.register_blueprint(espapi, url_prefix=API_V1)

# Género
from app.rutas.referenciales.genero.genero_routes import genmod
from app.rutas.referenciales.genero.genero_api import genapi
app.register_blueprint(genmod, url_prefix=f'{MODULO_REFERENCIALES}/genero')
app.register_blueprint(genapi, url_prefix=API_V1)

# Estado Civil
from app.rutas.referenciales.estado_civil.estado_civil_routes import ecivmod
from app.rutas.referenciales.estado_civil.estado_civil_api import ecapi
app.register_blueprint(ecivmod, url_prefix=f'{MODULO_REFERENCIALES}/estado-civil')
app.register_blueprint(ecapi, url_prefix=API_V1)

# Nivel de Instrucción
from app.rutas.referenciales.nivel_instruccion.nivel_instruccion_routes import nivmod
from app.rutas.referenciales.nivel_instruccion.nivel_instruccion_api import nivapi
app.register_blueprint(nivmod, url_prefix=f'{MODULO_REFERENCIALES}/nivel-instruccion')
app.register_blueprint(nivapi, url_prefix=API_V1)

# Ocupación/Profesión
from app.rutas.referenciales.ocupacion.profesion_routes import profmod
from app.rutas.referenciales.ocupacion.profesion_api import profapi
app.register_blueprint(profmod, url_prefix=f'{MODULO_REFERENCIALES}/profesion')
app.register_blueprint(profapi, url_prefix=API_V1)

# Día
from app.rutas.referenciales.dia.dia_routes import diamod
from app.rutas.referenciales.dia.dia_api import diaapi
app.register_blueprint(diamod, url_prefix=f'{MODULO_REFERENCIALES}/dia')
app.register_blueprint(diaapi, url_prefix=API_V1)

# Consultorio
from app.rutas.referenciales.consultorio.consultorio_routes import consmod
from app.rutas.referenciales.consultorio.consultorio_api import consapi
app.register_blueprint(consmod, url_prefix=f'{MODULO_REFERENCIALES}/consultorio')
app.register_blueprint(consapi, url_prefix=API_V1)

# Cargo
from app.rutas.referenciales.cargo.cargo_routes import cargomod
from app.rutas.referenciales.cargo.cargo_api import cargoapi
app.register_blueprint(cargomod, url_prefix=f'{MODULO_REFERENCIALES}/cargo')
app.register_blueprint(cargoapi, url_prefix=API_V1)

# Grupo
from app.rutas.referenciales.grupo.grupo_routes import grupomod
from app.rutas.referenciales.grupo.grupo_api import grupoapi
app.register_blueprint(grupomod, url_prefix=f'{MODULO_REFERENCIALES}/grupo')
app.register_blueprint(grupoapi, url_prefix=API_V1)

# Módulo
from app.rutas.referenciales.modulo.modulo_routes import modmod
from app.rutas.referenciales.modulo.modulo_api import modapi
app.register_blueprint(modmod, url_prefix=f'{MODULO_REFERENCIALES}/modulo')
app.register_blueprint(modapi, url_prefix=API_V1)

# Medicamento
from app.rutas.referenciales.medicamento.medicamento_routes import medmod
from app.rutas.referenciales.medicamento.medicamento_api import medapi
app.register_blueprint(medmod, url_prefix='/medicamento')
app.register_blueprint(medapi, url_prefix=API_V1)

# Signos
from app.rutas.referenciales.signo.signo_routes import signomod
from app.rutas.referenciales.signo.signo_api import signoapi
app.register_blueprint(signomod, url_prefix='/signo')
app.register_blueprint(signoapi, url_prefix=API_V1)

# Síntomas
from app.rutas.referenciales.sintoma.sintoma_routes import sintmod
from app.rutas.referenciales.sintoma.sintoma_api import sintapi
app.register_blueprint(sintmod, url_prefix='/sintoma')
app.register_blueprint(sintapi, url_prefix=API_V1)

# Tipo de Análisis
from app.rutas.referenciales.tipo_analisis.analisis_routes import tipoanalisismod
from app.rutas.referenciales.tipo_analisis.analisis_api import tipo_analisis_api
app.register_blueprint(tipoanalisismod, url_prefix='/tipo-analisis')
app.register_blueprint(tipo_analisis_api, url_prefix=API_V1)

# Tipo de Estudio
from app.rutas.referenciales.tipo_estudio.estudio_routes import tipo_estudio_mod
from app.rutas.referenciales.tipo_estudio.estudio_api import tipo_estudio_api
app.register_blueprint(tipo_estudio_mod, url_prefix='/tipo-estudio')
app.register_blueprint(tipo_estudio_api, url_prefix=API_V1)

# Tipo de Procedimiento
from app.rutas.referenciales.tipo_procedimiento.procedimiento_routes import tipo_procedimiento_mod
from app.rutas.referenciales.tipo_procedimiento.procedimiento_api import tipo_procedimiento_api
app.register_blueprint(tipo_procedimiento_mod, url_prefix='/tipo-procedimiento')
app.register_blueprint(tipo_procedimiento_api, url_prefix=API_V1)

# Tipo de Tratamiento
from app.rutas.referenciales.tipo_tratamiento.tratamiento_routes import tipotratamientomod
from app.rutas.referenciales.tipo_tratamiento.tratamiento_api import tipo_tratamiento_api
app.register_blueprint(tipotratamientomod, url_prefix='/tipo-tratamiento')
app.register_blueprint(tipo_tratamiento_api, url_prefix=API_V1)

# Tipo Certificado Médico
from app.rutas.referenciales.tipo_certificado_medico.certificado_medico_routes import tipo_certificado_medico_mod
from app.rutas.referenciales.tipo_certificado_medico.certificado_medico_api import tipo_certificado_medico_api
app.register_blueprint(tipo_certificado_medico_mod, url_prefix='/tipo-certificado-medico')
app.register_blueprint(tipo_certificado_medico_api, url_prefix=API_V1)

# Diagnóstico
from app.rutas.referenciales.diagnostico.diagnostico_routes import diagmod
from app.rutas.referenciales.diagnostico.diagnostico_api import diagapi
app.register_blueprint(diagmod, url_prefix=f'{MODULO_REFERENCIALES}/diagnostico')
app.register_blueprint(diagapi, url_prefix=API_V1)

# ============================================================================
# BLUEPRINTS - REFERENCIALES DE VENTAS
# ============================================================================

# Forma de Cobro
from app.rutas.referenciales.ventas.forma_cobro.forma_cobro_routes import forma_cobro_mod
from app.rutas.referenciales.ventas.forma_cobro.forma_cobro_api import forma_cobro_api
app.register_blueprint(forma_cobro_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/forma-cobro')
app.register_blueprint(forma_cobro_api, url_prefix=API_V1)

# Marca Tarjeta
from app.rutas.referenciales.ventas.marca_tarjeta.marca_tarjeta_routes import marca_tarjeta_mod
from app.rutas.referenciales.ventas.marca_tarjeta.marca_tarjeta_api import marca_tarjeta_api
app.register_blueprint(marca_tarjeta_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/marca-tarjeta')
app.register_blueprint(marca_tarjeta_api, url_prefix=API_V1)

# Entidad Adherida
from app.rutas.referenciales.ventas.entidad_adherida.entidad_adherida_routes import entidad_adherida_mod
from app.rutas.referenciales.ventas.entidad_adherida.entidad_adherida_api import entidad_adherida_api
app.register_blueprint(entidad_adherida_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/entidad-adherida')
app.register_blueprint(entidad_adherida_api, url_prefix=API_V1)

# Entidad Emisora
from app.rutas.referenciales.ventas.entidad_emisora.entidad_emisora_routes import entidad_emisora_mod
from app.rutas.referenciales.ventas.entidad_emisora.entidad_emisora_api import entidad_emisora_api
app.register_blueprint(entidad_emisora_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/entidad-emisora')
app.register_blueprint(entidad_emisora_api, url_prefix=API_V1)

# Caja
from app.rutas.referenciales.ventas.caja.caja_routes import caja_mod
from app.rutas.referenciales.ventas.caja.caja_api import caja_api
app.register_blueprint(caja_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/caja')
app.register_blueprint(caja_api, url_prefix=API_V1)

# Tipo de Item
from app.rutas.referenciales.ventas.tipo_item.tipo_item_routes import tipo_item_mod
from app.rutas.referenciales.ventas.tipo_item.tipo_item_api import tipo_item_api
app.register_blueprint(tipo_item_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/tipo-item')
app.register_blueprint(tipo_item_api, url_prefix=API_V1)

# Depósito
from app.rutas.referenciales.ventas.deposito.deposito_routes import deposito_mod
from app.rutas.referenciales.ventas.deposito.deposito_api import deposito_api
app.register_blueprint(deposito_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/deposito')
app.register_blueprint(deposito_api, url_prefix=API_V1)

# Tipo de Impuesto
from app.rutas.referenciales.ventas.tipo_impuesto.tipo_impuesto_routes import tipo_impuesto_mod
from app.rutas.referenciales.ventas.tipo_impuesto.tipo_impuesto_api import tipo_impuesto_api
app.register_blueprint(tipo_impuesto_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/tipo-impuesto')
app.register_blueprint(tipo_impuesto_api, url_prefix=API_V1)

# Condición de Venta
from app.rutas.referenciales.ventas.condicion_venta.condicion_venta_routes import condicion_venta_mod
from app.rutas.referenciales.ventas.condicion_venta.condicion_venta_api import condicion_venta_api
app.register_blueprint(condicion_venta_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/condicion-venta')
app.register_blueprint(condicion_venta_api, url_prefix=API_V1)

# Tipo de Comprobante
from app.rutas.referenciales.ventas.tipo_comprobante.tipo_comprobante_routes import tipo_comprobante_mod
from app.rutas.referenciales.ventas.tipo_comprobante.tipo_comprobante_api import tipo_comprobante_api
app.register_blueprint(tipo_comprobante_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/tipo-comprobante')
app.register_blueprint(tipo_comprobante_api, url_prefix=API_V1)

# Estado de Factura
from app.rutas.referenciales.ventas.estado_factura.estado_factura_routes import estado_factura_mod
from app.rutas.referenciales.ventas.estado_factura.estado_factura_api import estado_factura_api
app.register_blueprint(estado_factura_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/estado-factura')
app.register_blueprint(estado_factura_api, url_prefix=API_V1)

# Moneda
from app.rutas.referenciales.ventas.moneda.moneda_routes import moneda_mod
from app.rutas.referenciales.ventas.moneda.moneda_api import moneda_api
app.register_blueprint(moneda_mod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/moneda')
app.register_blueprint(moneda_api, url_prefix=API_V1)

# Items / Servicios (catálogo de productos/servicios de ventas)
from app.rutas.referenciales.ventas.items_servicios.item_servicio_routes import item_servicio
from app.rutas.referenciales.ventas.items_servicios.item_servicio_api import itemapi
app.register_blueprint(item_servicio, url_prefix=f'{MODULO_REFERENCIALES}/ventas/items-servicios')
app.register_blueprint(itemapi, url_prefix=API_V1)

# ============================================================================
# BLUEPRINTS - CONFIGURACIÓN DE VENTAS (Empresa, Sedes, Timbrados, etc.)
# ============================================================================

# Empresa
from app.rutas.referenciales.empresa.empresa_routes import empresamod
from app.rutas.referenciales.empresa.empresa_api import empresaapi
app.register_blueprint(empresamod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/empresa')
app.register_blueprint(empresaapi, url_prefix=API_V1)

# Sede
from app.rutas.referenciales.sede.sede_routes import sedemod
from app.rutas.referenciales.sede.sede_api import sedeapi
app.register_blueprint(sedemod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/sede')
app.register_blueprint(sedeapi, url_prefix=API_V1)

# Timbrado
from app.rutas.referenciales.timbrado.timbrado_routes import timbradomod
from app.rutas.referenciales.timbrado.timbrado_api import timbradoapi
app.register_blueprint(timbradomod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/timbrado')
app.register_blueprint(timbradoapi, url_prefix=API_V1)

# Establecimiento
from app.rutas.referenciales.establecimiento.establecimiento_routes import establecimientomod
from app.rutas.referenciales.establecimiento.establecimiento_api import establecimientoapi
app.register_blueprint(establecimientomod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/establecimiento')
app.register_blueprint(establecimientoapi, url_prefix=API_V1)

# Punto de Expedición
from app.rutas.referenciales.punto_expedicion.punto_expedicion_routes import puntoexpedicionmod
from app.rutas.referenciales.punto_expedicion.punto_expedicion_api import puntoexpedicionapi
app.register_blueprint(puntoexpedicionmod, url_prefix=f'{MODULO_REFERENCIALES}/ventas/punto-expedicion')
app.register_blueprint(puntoexpedicionapi, url_prefix=API_V1)


# ============================================================================
# BLUEPRINTS - GESTIÓN DE PERSONAS
# ============================================================================

# Paciente
from app.rutas.gestionar_personas.paciente.paciente_routes import pacientemod
from app.rutas.gestionar_personas.paciente.paciente_api import pacienteapi
app.register_blueprint(pacientemod, url_prefix=f'{MODULO_GESTION}/paciente')
app.register_blueprint(pacienteapi, url_prefix=API_V1)

# Funcionario
from app.rutas.gestionar_personas.funcionario.funcionario_routes import funcionariomod
from app.rutas.gestionar_personas.funcionario.funcionario_api import funcionarioapi
app.register_blueprint(funcionariomod, url_prefix=f'{MODULO_GESTION}/funcionario')
app.register_blueprint(funcionarioapi, url_prefix=API_V1)

# Usuario
from app.rutas.seguridad.usuario.usuario_routes import usumod
from app.rutas.seguridad.usuario.usuario_api import usuarioapi
app.register_blueprint(usumod, url_prefix=f'{MODULO_GESTION}/usuario')
app.register_blueprint(usuarioapi, url_prefix=API_V1)

from app.rutas.gestionar_personas.perfil.perfil_routes import perfilmod
from app.rutas.gestionar_personas.perfil.perfil_api import perfilapi

# Registrar blueprints
app.register_blueprint(perfilmod, url_prefix=f'{MODULO_GESTION}/perfil')
app.register_blueprint(perfilapi, url_prefix=API_V1)



# ============================================================================
# BLUEPRINTS - MÓDULOS DE AGENDAMIENTO Y CITAS
# ============================================================================

# Agenda Médica
from app.rutas.modulos.agenda_medica.agenda_medica_routes import agendamod
from app.rutas.modulos.agenda_medica.agenda_medica_api import agendaapi
app.register_blueprint(agendamod, url_prefix='/agenda')
app.register_blueprint(agendaapi, url_prefix=API_V1)

# Citas
from app.rutas.modulos.cita.cita_routes import citamod
from app.rutas.modulos.cita.cita_api import citaapi
app.register_blueprint(citamod, url_prefix='/cita')
app.register_blueprint(citaapi, url_prefix=API_V1)

# Recordatorios
from app.rutas.modulos.recordatorio.recordatorio_routes import recordatoriomod
from app.rutas.modulos.recordatorio.recordatorio_api import recordatorioapi
app.register_blueprint(recordatoriomod, url_prefix='/recordatorio')
app.register_blueprint(recordatorioapi, url_prefix=API_V1)



# ============================================================================
# BLUEPRINTS - MÓDULOS DE CONSULTAS MÉDICAS
# ============================================================================

# Registrar Consulta
from app.rutas.modulos.consulta.registrarconsulta.registrarconsulta_routes import consultamod
from app.rutas.modulos.consulta.registrarconsulta.registrarconsulta_api import consultaapi
app.register_blueprint(consultamod, url_prefix='/consulta')
app.register_blueprint(consultaapi, url_prefix=API_V1)

# Derivaciones
from app.rutas.modulos.derivacion.derivacion_routes import derivacionmod
from app.rutas.modulos.derivacion.derivacion_api import derivacionapi
app.register_blueprint(derivacionmod, url_prefix='/derivacion')
app.register_blueprint(derivacionapi, url_prefix=API_V1)

# Registrar Diagnóstico
from app.rutas.modulos.consulta.registrardiagnostico.registrardiagnostico_routes import diagnosticomod
from app.rutas.modulos.consulta.registrardiagnostico.registrardiagnostico_api import registrodiagnosticoapi
app.register_blueprint(diagnosticomod, url_prefix='/diagnostico')
app.register_blueprint(registrodiagnosticoapi, url_prefix=API_V1)

# Registrar Tratamiento
from app.rutas.modulos.consulta.registrartratamiento.registrartratamiento_routes import tratamientomod
from app.rutas.modulos.consulta.registrartratamiento.registrartratamiento_api import registrotratamientoapi
app.register_blueprint(tratamientomod, url_prefix='/tratamiento')
app.register_blueprint(registrotratamientoapi, url_prefix=API_V1)

# Registrar Procedimiento
from app.rutas.modulos.consulta.registrarprocedimiento.registrarprocedimiento_routes import procedimientomod
from app.rutas.modulos.consulta.registrarprocedimiento.registrarprocedimiento_api import registroprocedimientoapi
app.register_blueprint(procedimientomod, url_prefix='/procedimiento')
app.register_blueprint(registroprocedimientoapi, url_prefix=API_V1)

# Anamnesis
from app.rutas.modulos.consulta.anamnesis.anamnesis_routes import anamnesismod
from app.rutas.modulos.consulta.anamnesis.anamnesis_api import anamnesisapi
app.register_blueprint(anamnesismod, url_prefix='/anamnesis')
app.register_blueprint(anamnesisapi, url_prefix=API_V1)

# ============================================================================
# BLUEPRINTS - MÓDULOS NUEVOS (FALTANTES)
# ============================================================================

# Presupuestos
from app.rutas.modulos.presupuesto.registrarpresupuesto.registrarpresupuesto_routes import presupuestomod
from app.rutas.modulos.presupuesto.registrarpresupuesto.registrarpresupuesto_api import presupuestoapi
app.register_blueprint(presupuestomod, url_prefix='/presupuesto')
app.register_blueprint(presupuestoapi, url_prefix=API_V1)

# Pedidos (Ventas)
from app.rutas.modulos.ventas.pedido.registrarpedido.pedido_routes import pedidomod
from app.rutas.modulos.ventas.pedido.registrarpedido.pedido_api import pedidoapi
app.register_blueprint(pedidomod, url_prefix='/pedido')
app.register_blueprint(pedidoapi, url_prefix=API_V1)

# Facturas (Ventas)
from app.rutas.modulos.ventas.factura.registrarfactura.factura_routes import facturamod
from app.rutas.modulos.ventas.factura.registrarfactura.factura_api import facturaapi
app.register_blueprint(facturamod, url_prefix='/factura')
app.register_blueprint(facturaapi, url_prefix=API_V1)

# Cuentas a Cobrar (Ventas)
from app.rutas.modulos.ventas.cuenta_cobrar.registrarcuentacobrar.cuenta_cobrar_routes import cuenta_cobrar_mod
from app.rutas.modulos.ventas.cuenta_cobrar.registrarcuentacobrar.cuenta_cobrar_api import cuenta_cobrar_api
app.register_blueprint(cuenta_cobrar_mod, url_prefix='/cuenta-cobrar')
app.register_blueprint(cuenta_cobrar_api, url_prefix=API_V1)

# Cobranzas (Ventas)
from app.rutas.modulos.ventas.cobranza.registrarcobranza.cobranza_routes import cobranza_mod
from app.rutas.modulos.ventas.cobranza.registrarcobranza.cobranza_api import cobranza_api
app.register_blueprint(cobranza_mod, url_prefix='/cobranza')
app.register_blueprint(cobranza_api, url_prefix=API_V1)

# Apertura/Cierre de Caja (Ventas)
from app.rutas.modulos.ventas.apertura_cierre_caja.registraraperturacierrecaja.apertura_cierre_caja_routes import apertura_cierre_caja_mod
from app.rutas.modulos.ventas.apertura_cierre_caja.registraraperturacierrecaja.apertura_cierre_caja_api import apertura_cierre_caja_api
app.register_blueprint(apertura_cierre_caja_mod, url_prefix='/apertura-cierre-caja')
app.register_blueprint(apertura_cierre_caja_api, url_prefix=API_V1)

# Arqueo de Caja (Ventas)
from app.rutas.modulos.ventas.arqueo_caja.registrararqueocaja.arqueo_caja_routes import arqueo_caja_mod
from app.rutas.modulos.ventas.arqueo_caja.registrararqueocaja.arqueo_caja_api import arqueo_caja_api
app.register_blueprint(arqueo_caja_mod, url_prefix='/arqueo-caja')
app.register_blueprint(arqueo_caja_api, url_prefix=API_V1)

# Recaudaciones (Ventas)
from app.rutas.modulos.ventas.recaudacion.registrarrecaudacion.recaudacion_routes import recaudacion_mod
from app.rutas.modulos.ventas.recaudacion.registrarrecaudacion.recaudacion_api import recaudacion_api
app.register_blueprint(recaudacion_mod, url_prefix='/recaudacion')
app.register_blueprint(recaudacion_api, url_prefix=API_V1)

# Notas de Crédito (Ventas)
from app.rutas.modulos.ventas.nota_credito.registrarnotacredito.nota_credito_routes import nota_credito_mod
from app.rutas.modulos.ventas.nota_credito.registrarnotacredito.nota_credito_api import nota_credito_api
app.register_blueprint(nota_credito_mod, url_prefix='/nota-credito')
app.register_blueprint(nota_credito_api, url_prefix=API_V1)

# Notas de Débito (Ventas)
from app.rutas.modulos.ventas.nota_debito.registrarnotadebito.nota_debito_routes import nota_debito_mod
from app.rutas.modulos.ventas.nota_debito.registrarnotadebito.nota_debito_api import nota_debito_api
app.register_blueprint(nota_debito_mod, url_prefix='/nota-debito')
app.register_blueprint(nota_debito_api, url_prefix=API_V1)

# Libro de Ventas (Ventas)
from app.rutas.modulos.ventas.libro_ventas.registrarlibroventas.libro_ventas_routes import libro_ventas_mod
from app.rutas.modulos.ventas.libro_ventas.registrarlibroventas.libro_ventas_api import libro_ventas_api
app.register_blueprint(libro_ventas_mod, url_prefix='/libro-ventas')
app.register_blueprint(libro_ventas_api, url_prefix=API_V1)

# Recetas
from app.rutas.modulos.receta.registrarreceta.registrarreceta_routes import recetamod
from app.rutas.modulos.receta.registrarreceta.registrarreceta_api import recetaapi
app.register_blueprint(recetamod, url_prefix='/receta')
app.register_blueprint(recetaapi, url_prefix=API_V1)

# Órdenes de Estudios
from app.rutas.modulos.orden_estudio.registrarordenestudio.registrarordenestudio_routes import ordenestudiomod
from app.rutas.modulos.orden_estudio.registrarordenestudio.registrarordenestudio_api import ordenestudioapi
app.register_blueprint(ordenestudiomod, url_prefix='/orden-estudio')
app.register_blueprint(ordenestudioapi, url_prefix=API_V1)

# Certificados Médicos
from app.rutas.modulos.certificado_medico.registrarcertificadomedico.registrarcertificadomedico_routes import certificadomedicomod
from app.rutas.modulos.certificado_medico.registrarcertificadomedico.registrarcertificadomedico_api import certificadomedicoapi
app.register_blueprint(certificadomedicomod, url_prefix='/certificado-medico')
app.register_blueprint(certificadomedicoapi, url_prefix=API_V1)

# Insumos
from app.rutas.modulos.insumo.registrarinsumo.registrarinsumo_routes import insumomod
from app.rutas.modulos.insumo.registrarinsumo.registrarinsumo_api import insumoapi
app.register_blueprint(insumomod, url_prefix='/insumo')
app.register_blueprint(insumoapi, url_prefix=API_V1)


# ============================================================================
# BLUEPRINTS - FICHA MÉDICA
# ============================================================================

from app.rutas.modulos.ficha.ficha_routes import fichamedmod
from app.rutas.modulos.ficha.ficha_api import fichamedicaapi
app.register_blueprint(fichamedmod, url_prefix='/ficha-medica')
app.register_blueprint(fichamedicaapi, url_prefix=API_V1)


# ============================================================================
# ✅ REGISTRAR FUNCIONES HELPER PARA TEMPLATES
# ============================================================================

from app.utils.template_helpers import registrar_funciones_template
registrar_funciones_template(app)


# ============================================================================
# NOTAS IMPORTANTES
# ============================================================================

"""
📋 ORDEN DE REGISTRO:
1. Dashboard y seguridad (primero)
2. Módulos referenciales
3. Gestión de personas
4. Agendamiento y citas
5. Consultas médicas
6. Template helpers (AL FINAL)

🔧 PREFIJOS CONFIGURADOS:
- MODULO_REFERENCIALES = "/referenciales"
- MODULO_GESTION = "/modulos"
- API_V1 = "/api/v1"

✨ FUNCIONES DISPONIBLES EN TEMPLATES:
- es_admin()
- es_recepcion()
- es_especialista()
- puede_acceder_modulo(nombre)
- tiene_permiso(ruta)
- tiene_permiso_accion(accion, ruta)
- obtener_nombre_usuario()
- obtener_grupo_usuario()
- obtener_modulos_usuario()
- obtener_iniciales_usuario()
- usuario_autenticado()

📌 DASHBOARD APIS:
- GET /api/v1/estadisticas
- GET /api/v1/citas-hoy
- GET /api/v1/citas-manana
"""