from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.ventas.movimientos.presupuesto.PresupuestoDao import PresupuestoDao
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.services.documento_ventas_pdf_service import DocumentoVentasPdfService
from app.auth.utils.decorators import role_required, permiso_requerido
from app.utils.mensajes_validacion import msg_obligatorio

presupuestoapi = Blueprint('presupuestoapi', __name__)

ROLES_PRES = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
# CONVERTIDO no se asigna a mano: solo lo pone /convertir-pedido al crear el pedido.
ESTADOS_VALIDOS = ('PENDIENTE', 'APROBADO', 'RECHAZADO', 'VENCIDO')


@presupuestoapi.route('/presupuestos', methods=['GET'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "LEER")
def getPresupuestos():
    """GET: lista los registros de presupuesto."""
    try:
        return jsonify({'success': True, 'data': PresupuestoDao().getPresupuestos(), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener presupuestos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['GET'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "LEER")
def getPresupuesto(id_presupuesto):
    """GET: devuelve presupuesto por su id; 404 si no existe."""
    try:
        registro = PresupuestoDao().getPresupuestoById(id_presupuesto)
        if not registro:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
        return jsonify({'success': True, 'data': registro, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/pei-vigente/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "LEER")
def getPeiVigentePresupuesto(id_paciente):
    """Referencia del PEI vigente para ligarlo al presupuesto (sin contenido clínico)."""
    try:
        return jsonify({'success': True, 'data': PresupuestoDao().getPeiReferencia(id_paciente), 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener PEI vigente (paciente {id_paciente}): {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/pdf', methods=['GET'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "LEER")
def getPresupuestoPdf(id_presupuesto):
    """PDF imprimible (PRESUPUESTO.html). Si está ligado a un PEI lo firma el especialista del PEI;
    si no, el profesional del presupuesto."""
    try:
        presupuesto = PresupuestoDao().getPresupuestoById(id_presupuesto)
        if not presupuesto:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
        ficha = FichaDao()
        id_especialista = presupuesto.get('pei_id_especialista')
        if not id_especialista and presupuesto.get('id_profesional'):
            id_especialista = CitaDao().getEspecialistaPorFuncionario(presupuesto['id_profesional'])
        firmante = (ficha.getDatosGenerador(id_especialista) if id_especialista else None) or {}
        buffer = DocumentoVentasPdfService().generar_presupuesto_pdf(
            presupuesto, ficha.getDatosPaciente(presupuesto['id_paciente']) or {}, firmante,
            DocumentoVentasPdfService.config_empresa(),
        )
        return send_file(buffer, mimetype='application/pdf', as_attachment=False,
                         download_name=f"presupuesto_{presupuesto['presupuesto_numero']}.pdf")
    except Exception as e:
        app.logger.error(f"Error al generar PDF del presupuesto {id_presupuesto}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos', methods=['POST'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "CREAR")
def addPresupuesto():
    """POST: valida los datos y registra presupuesto; devuelve el id nuevo (201)."""
    data = request.get_json() or {}

    if not data.get('id_paciente'):
        return jsonify({'success': False, 'error': msg_obligatorio('Paciente')}), 400
    if not data.get('fecha_presupuesto'):
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha del presupuesto')}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'El presupuesto debe tener al menos un ítem.'}), 400
    for d in detalles:
        if not d.get('item_descripcion'):
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una descripción.'}), 400
        if not d.get('item_cantidad') or float(d['item_cantidad']) <= 0:
            return jsonify({'success': False, 'error': 'Cada ítem debe tener una cantidad mayor a 0.'}), 400

    try:
        nuevo_id = PresupuestoDao().guardar(data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_presupuesto': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar presupuesto: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/estado', methods=['PUT'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "EDITAR")
def updateEstadoPresupuesto(id_presupuesto):
    """PUT: cambia el estado del presupuesto."""
    data = request.get_json() or {}
    nuevo_estado = data.get('presupuesto_estado')
    if nuevo_estado not in ESTADOS_VALIDOS:
        return jsonify({'success': False, 'error': 'Estado inválido.'}), 400

    dao = PresupuestoDao()
    if not dao.getPresupuestoById(id_presupuesto):
        return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404

    try:
        dao.actualizarEstado(id_presupuesto, nuevo_estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_presupuesto': id_presupuesto}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al actualizar estado del presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/convertir-pedido', methods=['POST'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "CREAR")
def convertirPresupuestoEnPedido(id_presupuesto):
    """POST: crea un pedido a partir de un presupuesto."""
    try:
        numero = PresupuestoDao().convertirEnPedido(id_presupuesto, usuario=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'pedido_numero': numero}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al convertir presupuesto en pedido: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['DELETE'])
@role_required(*ROLES_PRES)
@permiso_requerido("VENTAS", "ELIMINAR")
def deletePresupuesto(id_presupuesto):
    """DELETE: da de baja el presupuesto."""
    dao = PresupuestoDao()
    if not dao.getPresupuestoById(id_presupuesto):
        return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
    try:
        dao.desactivar(id_presupuesto, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': f'Presupuesto {id_presupuesto} desactivado.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
