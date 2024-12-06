from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.agenda.AgendaDao import AgendaDao
import datetime

ageapi = Blueprint('ageapi', __name__)

# Trae todas las agendas
@ageapi.route('/agendas', methods=['GET'])
def getAgendas():
    agemod = AgendaDao()

    try:
        agendas = agemod.getAgendas()

        # Transformar fechas y horas a cadenas si es necesario
        for agenda in agendas:
            if isinstance(agenda['fecha'], (datetime.date, datetime.datetime)):
                agenda['fecha'] = agenda['fecha'].strftime('%Y-%m-%d')
            if isinstance(agenda['hora'], datetime.time):
                agenda['hora'] = agenda['hora'].strftime('%H:%M')

        return jsonify({
            'success': True,
            'data': agendas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las agendas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtiene una agenda por ID
@ageapi.route('/agendas/<int:agenda_id>', methods=['GET'])
def getAgenda(agenda_id):
    agemod = AgendaDao()

    try:
        agenda = agemod.getAgendaById(agenda_id)

        if agenda:
            if isinstance(agenda['fecha'], (datetime.date, datetime.datetime)):
                agenda['fecha'] = agenda['fecha'].strftime('%Y-%m-%d')
            if isinstance(agenda['hora'], datetime.time):
                agenda['hora'] = agenda['hora'].strftime('%H:%M')

            return jsonify({
                'success': True,
                'data': agenda,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener agenda: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva agenda
@ageapi.route('/agendas', methods=['POST'])
def addAgenda():
    data = request.get_json()
    agemod = AgendaDao()

    campos_requeridos = ['nombrepaciente', 'motivoconsulta', 'medico', 'fecha', 'hora']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombrepaciente = data['nombrepaciente'].upper()
        motivoconsulta = data['motivoconsulta'].upper()
        medico = data['medico'].upper()
        fecha = data['fecha']
        hora = data['hora']

        agenda_id = agemod.guardarAgenda(nombrepaciente, motivoconsulta, medico, fecha, hora)

        if agenda_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': agenda_id,
                    'nombrepaciente': nombrepaciente,
                    'motivoconsulta': motivoconsulta,
                    'medico': medico,
                    'fecha': fecha,
                    'hora': hora
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la agenda. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar agenda: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza una agenda
@ageapi.route('/agendas/<int:agenda_id>', methods=['PUT'])
def updateAgenda(agenda_id):
    data = request.get_json()
    agemod = AgendaDao()

    campos_requeridos = ['nombrepaciente', 'motivoconsulta', 'medico', 'fecha', 'hora']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    nombrepaciente = data['nombrepaciente'].upper()
    motivoconsulta = data['motivoconsulta'].upper()
    medico = data['medico'].upper()
    fecha = data['fecha']
    hora = data['hora']

    try:
        if agemod.updateAgenda(agenda_id, nombrepaciente, motivoconsulta, medico, fecha, hora):
            return jsonify({
                'success': True,
                'data': {
                    'id': agenda_id,
                    'nombrepaciente': nombrepaciente,
                    'motivoconsulta': motivoconsulta,
                    'medico': medico,
                    'fecha': fecha,
                    'hora': hora
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar agenda: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina una agenda
@ageapi.route('/agendas/<int:agenda_id>', methods=['DELETE'])
def deleteAgenda(agenda_id):
    agemod = AgendaDao()

    try:
        if agemod.deleteAgenda(agenda_id):
            return jsonify({
                'success': True,
                'mensaje': f'Agenda con ID {agenda_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar agenda: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
