from flask import Blueprint, request, jsonify, current_app as app
from app.dao.persona.medico.MedicoDao import MedicoDao

medicoapi = Blueprint('medicoapi', __name__)

# Trae todos los médicos
@medicoapi.route('/medicos', methods=['GET'])
def getMedicos():
    medicoDao = MedicoDao()

    try:
        medicos = medicoDao.getMedicos()

        return jsonify({
            'success': True,
            'data': medicos,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todos los médicos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un médico por ID
@medicoapi.route('/medicos/<int:medico_id>', methods=['GET'])
def getMedico(medico_id):
    medicoDao = MedicoDao()

    try:
        medico = medicoDao.getMedicoById(medico_id)

        if medico:
            return jsonify({
                'success': True,
                'data': medico,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener el médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo médico
@medicoapi.route('/medicos', methods=['POST'])
def addMedico():
    data = request.get_json()
    medicoDao = MedicoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad']

    # Verificar si faltan campos o son vacíos
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
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']
        # Otros campos como especialidad, correo, etc., también pueden ser agregados si es necesario

        medico_id = medicoDao.guardarMedico(nombre, apellido, cedula, id_estado_civil, telefono_emergencia, id_ciudad)
        
        if medico_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': medico_id, 'nombre': nombre, 'apellido': apellido, 'cedula': cedula, 'id_estado_civil': id_estado_civil, 'telefono_emergencia': telefono_emergencia, 'id_ciudad': id_ciudad},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el médico. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un médico
@medicoapi.route('/medicos/<int:medico_id>', methods=['PUT'])
def updateMedico(medico_id):
    data = request.get_json()
    medicoDao = MedicoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad']

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
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']

        if medicoDao.updateMedico(medico_id, nombre, apellido, cedula, id_estado_civil, telefono_emergencia, id_ciudad):
            return jsonify({
                'success': True,
                'data': {'id': medico_id, 'nombre': nombre, 'apellido': apellido, 'cedula': cedula, 'id_estado_civil': id_estado_civil, 'telefono_emergencia': telefono_emergencia, 'id_ciudad': id_ciudad},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Elimina un médico
@medicoapi.route('/medicos/<int:medico_id>', methods=['DELETE'])
def deleteMedico(medico_id):
    medicoDao = MedicoDao()

    try:
        if medicoDao.deleteMedico(medico_id):
            return jsonify({
                'success': True,
                'mensaje': f'Médico con ID {medico_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el médico con el ID proporcionado o no se pudo eliminar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
