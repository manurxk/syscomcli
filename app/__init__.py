from flask import Flask
from flask_wtf.csrf import CSRFProtect

from app.config.settings import init_settings
from app.middleware import init_middleware
from app.auth import login_blueprint
from app.rutas.mantenimiento.personas.funcionario.funcionario_routes import funcionariomod
from app.rutas.mantenimiento.personas.funcionario.funcionario_api import funcionarioapi
from app.rutas.mantenimiento.personas.paciente.paciente_routes import pacientemod
from app.rutas.mantenimiento.personas.paciente.paciente_api import pacienteapi
from app.rutas.mantenimiento.usuario.usuario_routes import usuariomod
from app.rutas.mantenimiento.usuario.usuario_api import usuarioapi
from app.rutas.mantenimiento.referenciales.referenciales_api import referencialesapi
from app.rutas.mantenimiento.referenciales.referenciales_routes import referencialesmod
from app.rutas.mantenimiento.referenciales.cargo.cargo_routes import cargomod
from app.rutas.mantenimiento.referenciales.cargo.cargo_api import cargoapi
from app.rutas.mantenimiento.referenciales.permisos.permisos_routes import permisosmod
from app.rutas.mantenimiento.referenciales.permisos.permisos_api import permisosapi
from app.rutas.mantenimiento.referenciales.empresa.empresa_routes import empresamod
from app.rutas.mantenimiento.referenciales.empresa.empresa_api import empresaapi
from app.rutas.mantenimiento.referenciales.sede.sede_routes import sedemod
from app.rutas.mantenimiento.referenciales.sede.sede_api import sedeapi
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_routes import consultoriomod
from app.rutas.mantenimiento.referenciales.consultorio.consultorio_api import consultorioapi
from app.rutas.agendamiento.referenciales.especialidad.especialidad_routes import especialidadmod
from app.rutas.agendamiento.referenciales.especialidad.especialidad_api import especialidadapi
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_routes import agendahorariosmod
from app.rutas.agendamiento.agenda_horarios.agenda_horarios_api import agendahorariosapi
from app.rutas.agendamiento.cita.cita_routes import citamod
from app.rutas.agendamiento.cita.cita_api import citaapi
from app.rutas.agendamiento.lista_espera.lista_espera_routes import listaesperamod
from app.rutas.agendamiento.lista_espera.lista_espera_api import listaesperaapi
from app.rutas.agendamiento.mi_agenda.mi_agenda_routes import miagendamod
from app.rutas.agendamiento.mi_agenda.mi_agenda_api import miagendaapi
from app.rutas.clinico.referenciales.signo.signo_routes import signomod
from app.rutas.clinico.referenciales.signo.signo_api import signoapi
from app.rutas.clinico.referenciales.sintoma.sintoma_routes import sintomamod
from app.rutas.clinico.referenciales.sintoma.sintoma_api import sintomaapi
from app.rutas.clinico.referenciales.diagnostico.diagnostico_routes import diagnosticomod
from app.rutas.clinico.referenciales.diagnostico.diagnostico_api import diagnosticoapi
from app.rutas.clinico.referenciales.medicamento.medicamento_routes import medicamentomod
from app.rutas.clinico.referenciales.medicamento.medicamento_api import medicamentoapi
from app.rutas.clinico.referenciales.tipo_analisis.tipo_analisis_routes import tipo_analisismod
from app.rutas.clinico.referenciales.tipo_analisis.tipo_analisis_api import tipoanalisisapi
from app.rutas.clinico.referenciales.tipo_estudio.tipo_estudio_routes import tipo_estudiomod
from app.rutas.clinico.referenciales.tipo_estudio.tipo_estudio_api import tipoestudioapi
from app.rutas.clinico.referenciales.tipo_procedimiento.tipo_procedimiento_routes import tipo_procedimientomod
from app.rutas.clinico.referenciales.tipo_procedimiento.tipo_procedimiento_api import tipoprocedimientoapi
from app.rutas.clinico.referenciales.tipo_tratamiento.tipo_tratamiento_routes import tipo_tratamientomod
from app.rutas.clinico.referenciales.tipo_tratamiento.tipo_tratamiento_api import tipotratamientoapi
from app.rutas.clinico.referenciales.tipo_certificado_medico.tipo_certificado_medico_routes import tipo_certificado_medicomod
from app.rutas.clinico.referenciales.tipo_certificado_medico.tipo_certificado_medico_api import tipocertificadomedicoapi
from app.rutas.clinico.referenciales.instrumento.instrumento_routes import instrumentomod
from app.rutas.clinico.referenciales.instrumento.instrumento_api import instrumentoapi
from app.rutas.clinico.referenciales.insumo.insumo_routes import insumomod
from app.rutas.clinico.referenciales.insumo.insumo_api import insumoapi
from app.rutas.clinico.movimientos.consulta.consulta_routes import consultamod
from app.rutas.clinico.movimientos.consulta.consulta_api import consultaapi
from app.rutas.clinico.movimientos.consulta.anamnesis_api import anamnesisapi
from app.rutas.clinico.movimientos.registro_clinico.registro_clinico_api import registroclinicoapi
from app.rutas.clinico.movimientos.tratamiento.tratamiento_api import tratamientoapi
from app.rutas.clinico.movimientos.orden.orden_api import ordenapi
from app.rutas.clinico.movimientos.receta.receta_api import recetaapi
from app.rutas.clinico.movimientos.certificado_medico.certificado_medico_api import certificadomedicoapi
from app.rutas.clinico.movimientos.pei.pei_routes import peimod
from app.rutas.clinico.movimientos.pei.pei_api import peiapi
from app.rutas.clinico.movimientos.ficha.ficha_routes import fichamod
from app.rutas.clinico.movimientos.ficha.ficha_api import fichaapi
from app.rutas.clinico.movimientos.derivacion.derivacion_api import derivacionapi
from app.rutas.ventas.referenciales.moneda.moneda_routes import monedamod
from app.rutas.ventas.referenciales.moneda.moneda_api import monedaapi
from app.rutas.ventas.referenciales.condicion_venta.condicion_venta_routes import condicionventamod
from app.rutas.ventas.referenciales.condicion_venta.condicion_venta_api import condicionventaapi
from app.rutas.ventas.referenciales.forma_cobro.forma_cobro_routes import formacobromod
from app.rutas.ventas.referenciales.forma_cobro.forma_cobro_api import formacobroapi
from app.rutas.ventas.referenciales.tipo_comprobante.tipo_comprobante_routes import tipocomprobantemod
from app.rutas.ventas.referenciales.tipo_comprobante.tipo_comprobante_api import tipocomprobanteapi
from app.rutas.ventas.referenciales.tipo_impuesto.tipo_impuesto_routes import tipoimpuestomod
from app.rutas.ventas.referenciales.tipo_impuesto.tipo_impuesto_api import tipoimpuestoapi
from app.rutas.ventas.referenciales.tipo_item.tipo_item_routes import tipoitemmod
from app.rutas.ventas.referenciales.tipo_item.tipo_item_api import tipoitemapi
from app.rutas.ventas.referenciales.marca_tarjeta.marca_tarjeta_routes import marcatarjetamod
from app.rutas.ventas.referenciales.marca_tarjeta.marca_tarjeta_api import marcatarjetaapi
from app.rutas.ventas.referenciales.entidad_adherida.entidad_adherida_routes import entidadadheridamod
from app.rutas.ventas.referenciales.entidad_adherida.entidad_adherida_api import entidadadheridaapi
from app.rutas.ventas.referenciales.entidad_emisora.entidad_emisora_routes import entidademisoramod
from app.rutas.ventas.referenciales.entidad_emisora.entidad_emisora_api import entidademisoraapi
from app.rutas.ventas.referenciales.estado_factura.estado_factura_routes import estadofacturamod
from app.rutas.ventas.referenciales.estado_factura.estado_factura_api import estadofacturaapi
from app.rutas.ventas.referenciales.caja.caja_routes import cajamod
from app.rutas.ventas.referenciales.caja.caja_api import cajaapi
from app.rutas.ventas.referenciales.deposito.deposito_routes import depositomod
from app.rutas.ventas.referenciales.deposito.deposito_api import depositoapi
from app.rutas.ventas.referenciales.item_servicio.item_servicio_routes import itemserviciomod
from app.rutas.ventas.referenciales.item_servicio.item_servicio_api import itemservicioapi
from app.rutas.ventas.movimientos.pedido.pedido_routes import pedidomod
from app.rutas.ventas.movimientos.pedido.pedido_api import pedidoapi
from app.rutas.ventas.movimientos.presupuesto.presupuesto_routes import presupuestomod
from app.rutas.ventas.movimientos.presupuesto.presupuesto_api import presupuestoapi
from app.rutas.ventas.movimientos.apertura_cierre_caja.apertura_cierre_caja_routes import aperturacierrecajamod
from app.rutas.ventas.movimientos.apertura_cierre_caja.apertura_cierre_caja_api import aperturacierrecajaapi
from app.rutas.ventas.movimientos.arqueo_caja.arqueo_caja_routes import arqueocajamod
from app.rutas.ventas.movimientos.arqueo_caja.arqueo_caja_api import arqueocajaapi
from app.rutas.ventas.referenciales.timbrado.timbrado_routes import timbradomod
from app.rutas.ventas.referenciales.timbrado.timbrado_api import timbradoapi
from app.rutas.ventas.referenciales.punto_expedicion.punto_expedicion_routes import puntoexpedicionmod
from app.rutas.ventas.referenciales.punto_expedicion.punto_expedicion_api import puntoexpedicionapi
from app.rutas.ventas.movimientos.factura.factura_routes import facturamod
from app.rutas.ventas.movimientos.factura.factura_api import facturaapi
from app.rutas.ventas.movimientos.remision.remision_routes import remisionmod
from app.rutas.ventas.movimientos.remision.remision_api import remisionapi
from app.rutas.ventas.movimientos.nota_credito.nota_credito_routes import notacreditomod
from app.rutas.ventas.movimientos.nota_credito.nota_credito_api import notacreditoapi
from app.rutas.ventas.movimientos.nota_debito.nota_debito_routes import notadebitomod
from app.rutas.ventas.movimientos.nota_debito.nota_debito_api import notadebitoapi
from app.rutas.ventas.movimientos.cuenta_cobrar.cuenta_cobrar_routes import cuentacobrarmod
from app.rutas.ventas.movimientos.cuenta_cobrar.cuenta_cobrar_api import cuentacobrarapi
from app.rutas.ventas.movimientos.cobranza.cobranza_routes import cobranzamod
from app.rutas.ventas.movimientos.cobranza.cobranza_api import cobranzaapi
from app.rutas.ventas.movimientos.recaudacion.recaudacion_routes import recaudacionmod
from app.rutas.ventas.movimientos.recaudacion.recaudacion_api import recaudacionapi
from app.rutas.ventas.movimientos.libro_ventas.libro_ventas_routes import libroventasmod
from app.rutas.ventas.movimientos.libro_ventas.libro_ventas_api import libroventasapi
from app.context_processors import init_context_processors
from app.utils.template_helpers import registrar_funciones_template

# Initialize the Flask application
app = Flask(__name__)

# Initialize Extensions
csrf = CSRFProtect()
csrf.init_app(app)

# Load Settings and Configuration
init_settings(app)

# Initialize Middleware
init_middleware(app)

# Register Blueprints (Routes)
app.register_blueprint(login_blueprint)
app.register_blueprint(funcionariomod, url_prefix='/mantenimiento/funcionario')
app.register_blueprint(funcionarioapi, url_prefix='/api/v1')
app.register_blueprint(pacientemod, url_prefix='/mantenimiento/paciente')
app.register_blueprint(pacienteapi, url_prefix='/api/v1')
app.register_blueprint(usuariomod, url_prefix='/mantenimiento/usuario')
app.register_blueprint(usuarioapi, url_prefix='/api/v1')
app.register_blueprint(referencialesapi, url_prefix='/api/v1')
app.register_blueprint(referencialesmod, url_prefix='/mantenimiento/referenciales')
app.register_blueprint(cargomod, url_prefix='/mantenimiento/referenciales/cargo')
app.register_blueprint(cargoapi, url_prefix='/api/v1')
app.register_blueprint(permisosmod, url_prefix='/mantenimiento/referenciales/permisos')
app.register_blueprint(permisosapi, url_prefix='/api/v1')
app.register_blueprint(empresamod, url_prefix='/mantenimiento/referenciales/empresa')
app.register_blueprint(empresaapi, url_prefix='/api/v1')
app.register_blueprint(sedemod, url_prefix='/mantenimiento/referenciales/sede')
app.register_blueprint(sedeapi, url_prefix='/api/v1')
app.register_blueprint(consultoriomod, url_prefix='/mantenimiento/referenciales/consultorio')
app.register_blueprint(consultorioapi, url_prefix='/api/v1')
app.register_blueprint(especialidadmod, url_prefix='/agendamiento/referenciales/especialidad')
app.register_blueprint(especialidadapi, url_prefix='/api/v1')
app.register_blueprint(agendahorariosmod, url_prefix='/agendamiento/agenda-horarios')
app.register_blueprint(agendahorariosapi, url_prefix='/api/v1')
app.register_blueprint(citamod, url_prefix='/agendamiento/citas')
app.register_blueprint(citaapi, url_prefix='/api/v1')
app.register_blueprint(listaesperamod, url_prefix='/agendamiento/lista-espera')
app.register_blueprint(listaesperaapi, url_prefix='/api/v1')
app.register_blueprint(miagendamod, url_prefix='/agendamiento')
app.register_blueprint(miagendaapi, url_prefix='/api/v1')
app.register_blueprint(signomod, url_prefix='/clinico/referenciales/signo')
app.register_blueprint(signoapi, url_prefix='/api/v1')
app.register_blueprint(sintomamod, url_prefix='/clinico/referenciales/sintoma')
app.register_blueprint(sintomaapi, url_prefix='/api/v1')
app.register_blueprint(diagnosticomod, url_prefix='/clinico/referenciales/diagnostico')
app.register_blueprint(diagnosticoapi, url_prefix='/api/v1')
app.register_blueprint(medicamentomod, url_prefix='/clinico/referenciales/medicamento')
app.register_blueprint(medicamentoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_analisismod, url_prefix='/clinico/referenciales/tipo-analisis')
app.register_blueprint(tipoanalisisapi, url_prefix='/api/v1')
app.register_blueprint(tipo_estudiomod, url_prefix='/clinico/referenciales/tipo-estudio')
app.register_blueprint(tipoestudioapi, url_prefix='/api/v1')
app.register_blueprint(tipo_procedimientomod, url_prefix='/clinico/referenciales/tipo-procedimiento')
app.register_blueprint(tipoprocedimientoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_tratamientomod, url_prefix='/clinico/referenciales/tipo-tratamiento')
app.register_blueprint(tipotratamientoapi, url_prefix='/api/v1')
app.register_blueprint(tipo_certificado_medicomod, url_prefix='/clinico/referenciales/tipo-certificado-medico')
app.register_blueprint(tipocertificadomedicoapi, url_prefix='/api/v1')
app.register_blueprint(instrumentomod, url_prefix='/clinico/referenciales/instrumento')
app.register_blueprint(instrumentoapi, url_prefix='/api/v1')
app.register_blueprint(insumomod, url_prefix='/clinico/referenciales/insumo')
app.register_blueprint(insumoapi, url_prefix='/api/v1')
app.register_blueprint(consultamod, url_prefix='/clinico/consulta')
app.register_blueprint(consultaapi, url_prefix='/api/v1')
app.register_blueprint(anamnesisapi, url_prefix='/api/v1')
app.register_blueprint(registroclinicoapi, url_prefix='/api/v1')
app.register_blueprint(tratamientoapi, url_prefix='/api/v1')
app.register_blueprint(ordenapi, url_prefix='/api/v1')
app.register_blueprint(recetaapi, url_prefix='/api/v1')
app.register_blueprint(certificadomedicoapi, url_prefix='/api/v1')
app.register_blueprint(peimod, url_prefix='/clinico/pei')
app.register_blueprint(peiapi, url_prefix='/api/v1')
app.register_blueprint(fichamod, url_prefix='/clinico/ficha')
app.register_blueprint(fichaapi, url_prefix='/api/v1')
app.register_blueprint(derivacionapi, url_prefix='/api/v1')
app.register_blueprint(monedamod, url_prefix='/ventas/referenciales/moneda')
app.register_blueprint(monedaapi, url_prefix='/api/v1')
app.register_blueprint(condicionventamod, url_prefix='/ventas/referenciales/condicion-venta')
app.register_blueprint(condicionventaapi, url_prefix='/api/v1')
app.register_blueprint(formacobromod, url_prefix='/ventas/referenciales/forma-cobro')
app.register_blueprint(formacobroapi, url_prefix='/api/v1')
app.register_blueprint(tipocomprobantemod, url_prefix='/ventas/referenciales/tipo-comprobante')
app.register_blueprint(tipocomprobanteapi, url_prefix='/api/v1')
app.register_blueprint(tipoimpuestomod, url_prefix='/ventas/referenciales/tipo-impuesto')
app.register_blueprint(tipoimpuestoapi, url_prefix='/api/v1')
app.register_blueprint(tipoitemmod, url_prefix='/ventas/referenciales/tipo-item')
app.register_blueprint(tipoitemapi, url_prefix='/api/v1')
app.register_blueprint(marcatarjetamod, url_prefix='/ventas/referenciales/marca-tarjeta')
app.register_blueprint(marcatarjetaapi, url_prefix='/api/v1')
app.register_blueprint(entidadadheridamod, url_prefix='/ventas/referenciales/entidad-adherida')
app.register_blueprint(entidadadheridaapi, url_prefix='/api/v1')
app.register_blueprint(entidademisoramod, url_prefix='/ventas/referenciales/entidad-emisora')
app.register_blueprint(entidademisoraapi, url_prefix='/api/v1')
app.register_blueprint(estadofacturamod, url_prefix='/ventas/referenciales/estado-factura')
app.register_blueprint(estadofacturaapi, url_prefix='/api/v1')
app.register_blueprint(cajamod, url_prefix='/ventas/referenciales/caja')
app.register_blueprint(cajaapi, url_prefix='/api/v1')
app.register_blueprint(depositomod, url_prefix='/ventas/referenciales/deposito')
app.register_blueprint(depositoapi, url_prefix='/api/v1')
app.register_blueprint(itemserviciomod, url_prefix='/ventas/referenciales/item-servicio')
app.register_blueprint(itemservicioapi, url_prefix='/api/v1')
app.register_blueprint(pedidomod, url_prefix='/ventas/movimientos/pedido')
app.register_blueprint(pedidoapi, url_prefix='/api/v1')
app.register_blueprint(presupuestomod, url_prefix='/ventas/movimientos/presupuesto')
app.register_blueprint(presupuestoapi, url_prefix='/api/v1')
app.register_blueprint(aperturacierrecajamod, url_prefix='/ventas/movimientos/caja')
app.register_blueprint(aperturacierrecajaapi, url_prefix='/api/v1')
app.register_blueprint(arqueocajamod, url_prefix='/ventas/movimientos/arqueo-caja')
app.register_blueprint(arqueocajaapi, url_prefix='/api/v1')
app.register_blueprint(timbradomod, url_prefix='/ventas/referenciales/timbrado')
app.register_blueprint(timbradoapi, url_prefix='/api/v1')
app.register_blueprint(puntoexpedicionmod, url_prefix='/ventas/referenciales/punto-expedicion')
app.register_blueprint(puntoexpedicionapi, url_prefix='/api/v1')
app.register_blueprint(facturamod, url_prefix='/ventas/movimientos/factura')
app.register_blueprint(facturaapi, url_prefix='/api/v1')
app.register_blueprint(remisionmod, url_prefix='/ventas/movimientos/remision')
app.register_blueprint(remisionapi, url_prefix='/api/v1')
app.register_blueprint(notacreditomod, url_prefix='/ventas/movimientos/nota-credito')
app.register_blueprint(notacreditoapi, url_prefix='/api/v1')
app.register_blueprint(notadebitomod, url_prefix='/ventas/movimientos/nota-debito')
app.register_blueprint(notadebitoapi, url_prefix='/api/v1')
app.register_blueprint(cuentacobrarmod, url_prefix='/ventas/movimientos/cuenta-cobrar')
app.register_blueprint(cuentacobrarapi, url_prefix='/api/v1')
app.register_blueprint(cobranzamod, url_prefix='/ventas/movimientos/cobranza')
app.register_blueprint(cobranzaapi, url_prefix='/api/v1')
app.register_blueprint(recaudacionmod, url_prefix='/ventas/movimientos/recaudacion')
app.register_blueprint(recaudacionapi, url_prefix='/api/v1')
app.register_blueprint(libroventasmod, url_prefix='/ventas/movimientos/libro-ventas')
app.register_blueprint(libroventasapi, url_prefix='/api/v1')

# Context processors y helpers de template
init_context_processors(app)
registrar_funciones_template(app)

# TODO (post fase ventas): restaurar el scheduler de presupuestos cuando
# PresupuestoDao se migre a la estructura nueva.