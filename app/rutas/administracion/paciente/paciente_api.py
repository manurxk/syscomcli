from flask import Blueprint, request, jsonify, current_app as app
from app.dao.persona.paciente.PacienteDao import PacienteDao

pacapi = Blueprint('pacapi', __name__)

# Trae todos los pacientes
@pacapi.route('/pacientes', methods=['GET'])
def getPacientes():
    pacientedao = PacienteDao()

    try:
        pacientes = pacientedao.getPacientes()

        return jsonify({
            'success': True,
            'data': pacientes,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los pacientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pacapi.route('/pacientes/<int:paciente_id>', methods=['GET'])
def getPaciente(paciente_id):
    pacientedao = PacienteDao()

    try:
        paciente = pacientedao.getPacienteById(paciente_id)

        if paciente:
            return jsonify({
                'success': True,
                'data': paciente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener el paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo paciente
@pacapi.route('/pacientes', methods=['POST'])
def addPaciente():
    data = request.get_json()
    pacientedao = PacienteDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula','id_genero', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        id_genero = data['id_genero']
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']

        paciente_id = pacientedao.guardarPaciente(nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad)
        
        if paciente_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': paciente_id, 'nombre': nombre, 'apellido': apellido, 
                        'cedula': cedula, 'id_genero': id_genero, 
                        'id_estado_civil': id_estado_civil, 
                        'telefono_emergencia': telefono_emergencia, 
                        'id_ciudad': id_ciudad},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el paciente. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pacapi.route('/pacientes/<int:paciente_id>', methods=['PUT'])
def updatePaciente(paciente_id):
    data = request.get_json()
    pacientedao = PacienteDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula','id_genero', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        id_genero = data['id_genero']
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']

        if pacientedao.updatePaciente(paciente_id, nombre, apellido, cedula, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
            return jsonify({
                'success': True,
                'data': {'id': paciente_id, 'nombre': nombre, 'apellido': apellido,
                        'cedula': cedula, 'id_genero': id_genero,
                        'id_estado_civil': id_estado_civil,
                        'telefono_emergencia': telefono_emergencia,
                        'id_ciudad': id_ciudad},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@pacapi.route('/pacientes/<int:paciente_id>', methods=['DELETE'])
def deletePaciente(paciente_id):
    pacientedao = PacienteDao()

    try:
        if pacientedao.deletePaciente(paciente_id):
            return jsonify({
                'success': True,
                'mensaje': f'Paciente con ID {paciente_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500