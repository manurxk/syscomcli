from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.lista_espera.ListaEsperaDao import ListaEsperaDao
from app.auth.utils.decorators import role_required

listaesperaapi = Blueprint('listaesperaapi', __name__)

ROLES_LISTA_ESPERA = ("ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA")


@listaesperaapi.route('/lista-espera', methods=['GET'])
@role_required(*ROLES_LISTA_ESPERA)
def getListaEspera():
    try:
        id_agenda_horario = request.args.get('id_agenda_horario', type=int)
        data = ListaEsperaDao().getListaEspera(id_agenda_horario)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener lista de espera: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@listaesperaapi.route('/lista-espera', methods=['POST'])
@role_required(*ROLES_LISTA_ESPERA)
def addListaEspera():
    data = request.get_json() or {}
    id_agenda_horario = data.get('id_agenda_horario')
    id_paciente = data.get('id_paciente')

    if not id_agenda_horario:
        return jsonify({'success': False, 'error': 'El campo "id_agenda_horario" es obligatorio.'}), 400
    if not id_paciente:
        return jsonify({'success': False, 'error': 'El campo "id_paciente" es obligatorio.'}), 400

    try:
        id_lista_espera = ListaEsperaDao().agregarOReactivar(
            id_agenda_horario, id_paciente,
            motivo=data.get('motivo'),
            prioridad=data.get('prioridad', 0),
            usuario_creacion=session.get('id_usuario'),
        )
        return jsonify({'success': True, 'data': {'id_lista_espera': id_lista_espera}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al agregar a lista de espera: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@listaesperaapi.route('/lista-espera/<int:id_lista_espera>/estado', methods=['PATCH'])
@role_required(*ROLES_LISTA_ESPERA)
def cambiarEstadoListaEspera(id_lista_espera):
    data = request.get_json() or {}
    nuevo_estado = data.get('estado')

    if not ListaEsperaDao().getListaEsperaById(id_lista_espera):
        return jsonify({'success': False, 'error': 'No se encontró el registro indicado.'}), 404

    try:
        ListaEsperaDao().cambiarEstado(id_lista_espera, nuevo_estado, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': 'Estado actualizado correctamente.', 'error': None}), 200
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al cambiar estado de lista de espera: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@listaesperaapi.route('/lista-espera/<int:id_lista_espera>', methods=['DELETE'])
@role_required(*ROLES_LISTA_ESPERA)
def desactivarListaEspera(id_lista_espera):
    if not ListaEsperaDao().getListaEsperaById(id_lista_espera):
        return jsonify({'success': False, 'error': 'No se encontró el registro indicado.'}), 404

    try:
        ListaEsperaDao().desactivar(id_lista_espera, usuario_modificacion=session.get('id_usuario'))
        return jsonify({'success': True, 'mensaje': 'Registro retirado de la lista de espera.', 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al desactivar lista de espera: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
