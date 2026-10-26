from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.clinico.movimientos.orden.OrdenDao import OrdenDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.auth.utils.decorators import role_required
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.services.documento_clinico_pdf_service import DocumentoClinicoPdfService
from app.services.EmailService import EmailService
from app.services.UltraMsgService import UltraMsgService
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.utils.ficha_acceso import MENSAJE_SIN_ACCESO, puede_ver_ficha
from app.utils.mensajes_validacion import msg_obligatorio

ordenapi = Blueprint('ordenapi', __name__)

ROLES_ORDEN = ("ADMINISTRADOR", "CLINICO")


@ordenapi.route('/consultas/<int:id_consulta>/ordenes', methods=['GET'])
@role_required(*ROLES_ORDEN)
def getOrdenes(id_consulta):
    """GET: lista los órdenes de estudio de la consulta."""
    try:
        data = OrdenDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener órdenes de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/consultas/<int:id_consulta>/ordenes', methods=['POST'])
@role_required(*ROLES_ORDEN)
def addOrden(id_consulta):
    """POST: valida y registra orden de estudio en la consulta (201)."""
    data = request.get_json() or {}
    if not data.get('orden_fecha'):
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha de la orden')}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La orden debe tener al menos un ítem de estudio o análisis.'}), 400
    for d in detalles:
        if d.get('tipo_orden') not in ('ESTUDIO', 'ANALISIS'):
            return jsonify({'success': False, 'error': 'Cada ítem debe indicar tipo ESTUDIO o ANALISIS.'}), 400
        if d['tipo_orden'] == 'ESTUDIO' and not d.get('id_tipo_estudio'):
            return jsonify({'success': False, 'error': 'Seleccione el tipo de estudio en cada ítem.'}), 400
        if d['tipo_orden'] == 'ANALISIS' and not d.get('id_tipo_analisis'):
            return jsonify({'success': False, 'error': 'Seleccione el tipo de análisis en cada ítem.'}), 400

    consulta = ConsultaDao().getConsultaParaEditar(id_consulta)
    if not consulta:
        return jsonify({'success': False, 'error': 'La consulta no existe.'}), 404

    try:
        nuevo_id = OrdenDao().guardar(
            id_consulta, consulta['id_paciente'], consulta['id_especialista'],
            data, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_orden': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar orden de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/ordenes/<int:id_orden>', methods=['DELETE'])
@role_required(*ROLES_ORDEN)
def deleteOrden(id_orden):
    """DELETE: baja lógica de orden de estudio; 404 si no existe."""
    try:
        if OrdenDao().desactivar(id_orden, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar orden de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


def _generar_pdf_orden(id_orden):
    """(orden, paciente, buffer, empresa) de la orden, o (None, None, None, None) si no existe. Lo firma el especialista
    de la consulta, que es quien la emitió."""
    orden = OrdenDao().getParaImprimir(id_orden)
    if not orden:
        return None, None, None, None
    ficha = FichaDao()
    paciente = ficha.getDatosPaciente(orden['id_paciente']) or {}
    empresa = DocumentoClinicoPdfService.config_empresa()
    buffer = DocumentoClinicoPdfService().generar_orden_pdf(
        orden, paciente, ficha.getDatosGenerador(orden['id_especialista']) or {}, empresa)
    return orden, paciente, buffer, empresa


def _destinos_orden(paciente):
    """Correo y teléfono a los que se envía la orden: los del paciente; si es menor y no tiene teléfono propio, el de su madre o su padre."""
    telefono = paciente.get('telefono')
    if not telefono and paciente.get('es_menor'):
        telefono = paciente.get('madre_telefono') or paciente.get('padre_telefono')
    return {'correo': (paciente.get('correo') or '').strip() or None, 'telefono': (telefono or '').strip() or None}


@ordenapi.route('/ordenes/<int:id_orden>/destinos', methods=['GET'])
@role_required(*ROLES_ORDEN)
def getDestinosOrden(id_orden):
    """GET: a qué correo y teléfono se puede enviar la orden (los del paciente), para elegirlo en la pantalla."""
    try:
        orden = OrdenDao().getParaImprimir(id_orden)
        if not orden:
            return jsonify({'success': False, 'error': 'No se encontró el documento.'}), 404
        if not puede_ver_ficha(orden['id_paciente']):
            return jsonify({'success': False, 'error': MENSAJE_SIN_ACCESO}), 403
        paciente = FichaDao().getDatosPaciente(orden['id_paciente']) or {}
        return jsonify({'success': True, 'data': {'paciente': paciente.get('nombre_completo'), **_destinos_orden(paciente)}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener los destinos de la orden {id_orden}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/ordenes/<int:id_orden>/enviar', methods=['POST'])
@role_required(*ROLES_ORDEN)
def enviarOrden(id_orden):
    """POST: envía el PDF de la orden al paciente por correo y/o WhatsApp (`canales`: ['correo', 'whatsapp']), a los datos
    que el paciente tiene en su ficha. Cada canal sale por separado y se informa su resultado; cada envío exitoso queda
    en la auditoría. Solo quien puede ver la ficha del paciente."""
    canales = (request.get_json(silent=True) or {}).get('canales') or []
    canales = [c for c in dict.fromkeys(canales) if c in ('correo', 'whatsapp')]
    if not canales:
        return jsonify({'success': False, 'error': 'Elija al menos un canal: correo o WhatsApp.'}), 400
    try:
        orden, paciente, buffer, empresa = _generar_pdf_orden(id_orden)
        if not orden:
            return jsonify({'success': False, 'error': 'No se encontró el documento.'}), 404
        if not puede_ver_ficha(orden['id_paciente']):
            return jsonify({'success': False, 'error': MENSAJE_SIN_ACCESO}), 403

        pdf = buffer.getvalue()
        destinos = _destinos_orden(paciente)
        numero, nombre = orden['orden_numero'], paciente.get('nombre_completo') or 'paciente'
        clinica = empresa.get('nombre') or 'SYSCLIN'
        resultados = {}
        if 'correo' in canales:
            if not destinos['correo']:
                resultados['correo'] = {'ok': False, 'mensaje': 'El paciente no tiene correo registrado: cárguelo en su ficha de paciente.'}
            else:
                ok, error, _ = EmailService().enviar_orden_estudio(destinos['correo'], numero, nombre, pdf, clinica)
                resultados['correo'] = {'ok': ok, 'mensaje': f"Enviada a {destinos['correo']}." if ok else error}
        if 'whatsapp' in canales:
            if not destinos['telefono']:
                resultados['whatsapp'] = {'ok': False, 'mensaje': 'El paciente no tiene teléfono registrado: cárguelo en su ficha de paciente.'}
            else:
                ok, error = UltraMsgService().enviar_documento(
                    destinos['telefono'], f'orden_{numero}.pdf', pdf,
                    f'{clinica}: su orden de estudios {numero}. Preséntela en el laboratorio o centro donde se realice.')
                resultados['whatsapp'] = {'ok': ok, 'mensaje': f"Enviada al {destinos['telefono']}." if ok else error}

        for canal, r in resultados.items():
            if r['ok']:
                AuditoriaDao().registrar_evento(
                    id_usuario=session.get('id_usuario'), accion=AuditAccion.REPORT_EXPORT,
                    detalle=f"Envió por {'correo' if canal == 'correo' else 'WhatsApp'} la orden de estudios {numero} de {nombre}",
                    ip_origen=request.remote_addr)
        return jsonify({'success': any(r['ok'] for r in resultados.values()), 'data': resultados, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al enviar la orden {id_orden}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@ordenapi.route('/ordenes/<int:id_orden>/pdf', methods=['GET'])
@role_required(*ROLES_ORDEN)
def getOrdenPdf(id_orden):
    """PDF imprimible (ORDEN.html). Lo firma el especialista de la consulta, que es quien lo emitió."""
    try:
        orden, _, buffer, _ = _generar_pdf_orden(id_orden)
        if not orden:
            return jsonify({'success': False, 'error': 'No se encontró el documento.'}), 404
        return send_file(buffer, mimetype='application/pdf', as_attachment=False,
                         download_name=f"orden_{orden['orden_numero']}.pdf")
    except Exception as e:
        app.logger.error(f"Error al generar PDF de orden {id_orden}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
