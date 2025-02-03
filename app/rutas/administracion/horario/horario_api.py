from flask import Blueprint, request, jsonify, current_app as app
from app.dao.agenda.horario.HorarioDao import HorarioDao
import datetime

horapi = Blueprint('horapi', __name__)

# Trae todos los horarios
@horapi.route('/horarios', methods=['GET'])
def getHorarios():
    hormod = HorarioDao()

    try:
        horarios = hormod.getHorarios()

        # Transformar fechas y horas a cadenas si es necesario
        for horario in horarios:
            if isinstance(horario['fecha'], (datetime.date, datetime.datetime)):
                horario['fecha'] = horario['fecha'].strftime('%Y-%m-%d')
            if isinstance(horario['hora'], datetime.time):
                horario['hora'] = horario['hora'].strftime('%H:%M')

        return jsonify({
            'success': True,
            'data': horarios,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los horarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Obtiene un horario por ID
@horapi.route('/horarios/<int:horario_id>', methods=['GET'])
def getHorario(horario_id):
    hormod = HorarioDao()

    try:
        horario = hormod.getHorarioById(horario_id)

        if horario:
            if isinstance(horario['fecha'], (datetime.date, datetime.datetime)):
                horario['fecha'] = horario['fecha'].strftime('%Y-%m-%d')
            if isinstance(horario['hora'], datetime.time):
                horario['hora'] = horario['hora'].strftime('%H:%M')

            return jsonify({
                'success': True,
                'data': horario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el horario con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo horario
@horapi.route('/horarios', methods=['POST'])
def addHorario():
    data = request.get_json()
    hormod = HorarioDao()

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

        horario_id = hormod.guardarHorario(nombrepaciente, motivoconsulta, medico, fecha, hora)

        if horario_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id': horario_id,
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
                'error': 'No se pudo guardar el horario. Consulte con el administrador.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al agregar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un horario
@horapi.route('/horarios/<int:horario_id>', methods=['PUT'])
def updateHorario(horario_id):
    data = request.get_json()
    hormod = HorarioDao()

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
        if hormod.updateHorario(horario_id, nombrepaciente, motivoconsulta, medico, fecha, hora):
            return jsonify({
                'success': True,
                'data': {
                    'id': horario_id,
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
                'error': 'No se encontró el horario con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un horario
@horapi.route('/horarios/<int:horario_id>', methods=['DELETE'])
def deleteHorario(horario_id):
    hormod = HorarioDao()

    try:
        if hormod.deleteHorario(horario_id):
            return jsonify({
                'success': True,
                'mensaje': f'Horario con ID {horario_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el horario con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar horario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500