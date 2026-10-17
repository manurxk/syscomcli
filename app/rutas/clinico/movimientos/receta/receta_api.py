from flask import Blueprint, request, jsonify, current_app as app, session, send_file

from app.dao.clinico.movimientos.receta.RecetaDao import RecetaDao
from app.dao.clinico.movimientos.consulta.ConsultaDao import ConsultaDao
from app.auth.utils.decorators import role_required
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.services.documento_clinico_pdf_service import DocumentoClinicoPdfService

recetaapi = Blueprint('recetaapi', __name__)

ROLES_RECETA = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@recetaapi.route('/consultas/<int:id_consulta>/recetas', methods=['GET'])
@role_required(*ROLES_RECETA)
def getRecetas(id_consulta):
    try:
        data = RecetaDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener recetas de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/consultas/<int:id_consulta>/recetas', methods=['POST'])
@role_required(*ROLES_RECETA)
def addReceta(id_consulta):
    data = request.get_json() or {}
    if not data.get('receta_fecha'):
        return jsonify({'success': False, 'error': 'La fecha de la receta es obligatoria.'}), 400

    detalles = data.get('detalles') or []
    if not detalles:
        return jsonify({'success': False, 'error': 'La receta debe tener al menos un medicamento.'}), 400
    for d in detalles:
        if not d.get('id_medicamento'):
            return jsonify({'success': False, 'error': 'Seleccione el medicamento en cada ítem.'}), 400
        if not (d.get('medicamento_dosis') or '').strip():
            return jsonify({'success': False, 'error': 'Indique la dosis en cada ítem.'}), 400
        if not (d.get('medicamento_frecuencia') or '').strip():
            return jsonify({'success': False, 'error': 'Indique la frecuencia en cada ítem.'}), 400

    consulta = ConsultaDao().getConsultaParaEditar(id_consulta)
    if not consulta:
        return jsonify({'success': False, 'error': 'La consulta no existe.'}), 404

    try:
        nuevo_id = RecetaDao().guardar(
            id_consulta, consulta['id_paciente'], consulta['id_especialista'],
            data, usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_receta': nuevo_id}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al guardar receta de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas/<int:id_receta>', methods=['DELETE'])
@role_required(*ROLES_RECETA)
def deleteReceta(id_receta):
    try:
        if RecetaDao().desactivar(id_receta, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar receta de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@recetaapi.route('/recetas/<int:id_receta>/pdf', methods=['GET'])
@role_required(*ROLES_RECETA)
def getRecetaPdf(id_receta):
    """PDF imprimible (RECETA.html). Lo firma el especialista de la consulta, que es quien lo emitió."""
    try:
        receta = RecetaDao().getParaImprimir(id_receta)
        if not receta:
            return jsonify({'success': False, 'error': 'No se encontró el documento.'}), 404
        ficha = FichaDao()
        buffer = DocumentoClinicoPdfService().generar_receta_pdf(
            receta, ficha.getDatosPaciente(receta['id_paciente']) or {},
            ficha.getDatosGenerador(receta['id_especialista']) or {},
            DocumentoClinicoPdfService.config_empresa(),
        )
        return send_file(buffer, mimetype='application/pdf', as_attachment=False,
                         download_name=f"receta_{receta['receta_numero']}.pdf")
    except Exception as e:
        app.logger.error(f"Error al generar PDF de receta {id_receta}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
