from flask import Blueprint, request, jsonify, current_app as app, session, send_file
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.services.pdf_service import FichaMedicaPDFService
from app.auth.utils.decorators import role_required

fichaapi = Blueprint('fichaapi', __name__)

ROLES_FICHA = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


def _resolver_id_especialista():
    id_funcionario = session.get('id_funcionario')
    if not id_funcionario:
        return None
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario)


@fichaapi.route('/clinico/ficha/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_FICHA)
def getFicha(id_paciente):
    try:
        data = FichaDao().getFichaCompleta(id_paciente)
        if not data or not data.get('paciente'):
            return jsonify({'success': False, 'error': 'Paciente no encontrado.'}), 404
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener ficha (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@fichaapi.route('/clinico/ficha/<int:id_paciente>/pdf', methods=['GET'])
@role_required(*ROLES_FICHA)
def getFichaPdf(id_paciente):
    id_especialista = _resolver_id_especialista()
    if not id_especialista:
        return jsonify({
            'success': False,
            'error': 'Solo un especialista puede generar la ficha médica en PDF.'
        }), 403

    try:
        data = FichaDao().getFichaCompleta(id_paciente)
        if not data or not data.get('paciente'):
            return jsonify({'success': False, 'error': 'Paciente no encontrado.'}), 404

        generador = FichaDao().getDatosGenerador(id_especialista)
        buffer = FichaMedicaPDFService().generar_ficha_completa(data, generado_por=generador)
        nombre_archivo = f"ficha_medica_{id_paciente}.pdf"
        return send_file(buffer, mimetype='application/pdf',
                          as_attachment=False, download_name=nombre_archivo)
    except Exception as e:
        app.logger.error(f"Error al generar PDF de ficha (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'No se pudo generar el PDF.'}), 500


@fichaapi.route('/clinico/ficha/<int:id_paciente>/notas', methods=['GET'])
@role_required(*ROLES_FICHA)
def getNotas(id_paciente):
    try:
        data = FichaDao().getNotasPaciente(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@fichaapi.route('/clinico/ficha/<int:id_paciente>/notas', methods=['POST'])
@role_required(*ROLES_FICHA)
def addNota(id_paciente):
    body = request.get_json() or {}
    contenido = (body.get('nota_contenido') or '').strip()
    if not contenido:
        return jsonify({'success': False, 'error': 'El contenido de la nota no puede estar vacío.'}), 400

    id_especialista = _resolver_id_especialista()
    if not id_especialista:
        return jsonify({'success': False, 'error': 'No se pudo determinar el especialista. Verificá tu perfil.'}), 400

    try:
        id_nota = FichaDao().guardarNota(
            id_paciente, id_especialista, contenido,
            usuario_creacion=session.get('id_usuario')
        )
        return jsonify({'success': True, 'data': {'id_nota': id_nota}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar nota (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@fichaapi.route('/clinico/ficha/notas/<int:id_nota>', methods=['DELETE'])
@role_required(*ROLES_FICHA)
def deleteNota(id_nota):
    try:
        ok = FichaDao().eliminarNota(id_nota)
        if not ok:
            return jsonify({'success': False, 'error': 'Nota no encontrada.'}), 404
        return jsonify({'success': True, 'data': None, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al eliminar nota {id_nota}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
