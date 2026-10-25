from flask import Blueprint, request, jsonify, current_app as app, session, send_file
from app.dao.clinico.movimientos.ficha.FichaDao import FichaDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.services.ficha_html_pdf_service import FichaHtmlPdfService
from app.auth.utils.decorators import role_required

fichaapi = Blueprint('fichaapi', __name__)

ROLES_FICHA = ("ADMINISTRADOR", "CLINICO")

# Secciones que la plantilla FICHA.html realmente renderiza (ver ficha_html_pdf_service.py).
SECCIONES_PDF = ('anamnesis', 'diagnosticos', 'tratamientos_activos', 'proximas_citas')


def _resolver_id_especialista():
    """Devuelve el id de especialista del usuario en sesión, o None si no es especialista."""
    id_funcionario = session.get('id_funcionario')
    if not id_funcionario:
        return None
    return CitaDao().getEspecialistaPorFuncionario(id_funcionario)


@fichaapi.route('/clinico/ficha/<int:id_paciente>', methods=['GET'])
@role_required(*ROLES_FICHA)
def getFicha(id_paciente):
    """GET: ficha clínica completa del paciente; 404 si no existe."""
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
    """GET: genera y devuelve el PDF de la ficha clínica del paciente."""
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

        secciones_param = request.args.get('secciones')
        if secciones_param is not None:
            seleccionadas = {s.strip() for s in secciones_param.split(',') if s.strip()}
            for clave in SECCIONES_PDF:
                if clave not in seleccionadas:
                    data[clave] = None

        generador = FichaDao().getDatosGenerador(id_especialista)

        empresa = EmpresaDao().getEmpresaPrincipal() or {}
        ruc = f"{empresa.get('ruc_nit', '')}-{empresa.get('digito_verificador', '')}" if empresa.get('ruc_nit') else ''
        config_empresa = {
            'nombre': empresa.get('nombre_comercial') or empresa.get('razon_social', ''),
            'direccion': empresa.get('direccion', ''),
            'telefono': empresa.get('telefono') or empresa.get('celular', ''),
            'ruc': ruc,
            'sitio_web': empresa.get('sitio_web', ''),
        }

        buffer = FichaHtmlPdfService().generar_ficha_html_pdf(data, config_empresa=config_empresa, generado_por=generador)
        nombre_archivo = f"ficha_medica_{id_paciente}.pdf"
        return send_file(buffer, mimetype='application/pdf',
                          as_attachment=False, download_name=nombre_archivo)
    except Exception as e:
        app.logger.error(f"Error al generar PDF de ficha (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'No se pudo generar el PDF.'}), 500


@fichaapi.route('/clinico/ficha/<int:id_paciente>/notas', methods=['GET'])
@role_required(*ROLES_FICHA)
def getNotas(id_paciente):
    """GET: notas clínicas del paciente."""
    try:
        data = FichaDao().getNotasPaciente(id_paciente)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener notas (paciente {id_paciente}): {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@fichaapi.route('/clinico/ficha/<int:id_paciente>/notas', methods=['POST'])
@role_required(*ROLES_FICHA)
def addNota(id_paciente):
    """POST: agrega una nota clínica del especialista al paciente."""
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
    """DELETE: baja lógica de la nota clínica; 404 si no existe."""
    try:
        ok = FichaDao().eliminarNota(id_nota, usuario_modificacion=session.get('id_usuario'))
        if not ok:
            return jsonify({'success': False, 'error': 'Nota no encontrada.'}), 404
        return jsonify({'success': True, 'data': None, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al eliminar nota {id_nota}: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
