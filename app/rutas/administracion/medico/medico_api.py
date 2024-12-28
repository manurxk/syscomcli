from flask import Blueprint, request, jsonify, current_app as app
from app.dao.persona.medico.MedicoDao import MedicoDao
 
medapi = Blueprint('medapi', __name__)

# Trae todos los médicos
@medapi.route('/medicos', methods=['GET'])
def getMedicos():
    medicodao = MedicoDao()

    try:
        medicos = medicodao.getMedicos()
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
@medapi.route('/medicos/<int:medico_id>', methods=['GET'])
def getMedico(medico_id):
    medicodao = MedicoDao()

    try:
        medico = medicodao.getMedicoById(medico_id)

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
@medapi.route('/medicos', methods=['POST'])
def addMedico():
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar campos requeridos
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'sexo', 'telefono', 'correo', 'matricula', 'id_especialidad', 'fecha_nacimiento', 'id_estado_civil', 'direccion', 'id_ciudad']
    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
            return jsonify({
            'success': False, 
            'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        # Procesar los datos y asegurarse de que todo esté correctamente formateado
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        sexo = data['sexo']
        telefono = data['telefono'].strip()
        correo = data['correo'].strip()
        matricula = data['matricula'].strip()
        id_especialidad = data['id_especialidad']
        fecha_nacimiento = data['fecha_nacimiento']
        id_estado_civil = data['id_estado_civil']
        direccion = data['direccion'].strip()
        id_ciudad = data['id_ciudad']

        # Llamar al método DAO para insertar el médico
        medico_id = medicodao.guardarMedico(
            nombre, apellido, cedula, sexo, telefono, correo, matricula, 
            id_especialidad, fecha_nacimiento, id_estado_civil, direccion, id_ciudad
        )

        if medico_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id_medico': medico_id,  # Aquí agregamos id_medico que es devuelto por la base de datos
                    'nombre': nombre,
                    'apellido': apellido,
                    'cedula': cedula,
                    'sexo': sexo,
                    'telefono': telefono,
                    'correo': correo,
                    'matricula': matricula,
                    'id_especialidad': id_especialidad,
                    'fecha_nacimiento': fecha_nacimiento,
                    'id_estado_civil': id_estado_civil,
                    'direccion': direccion,
                    'id_ciudad': id_ciudad
                },
                'error': None
            }), 201

        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el médico.'}), 500
    
    except Exception as e:
        # Manejo de errores y registros de logs
        app.logger.error(f"Error al agregar médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualiza un médico
@medapi.route('/medicos/<int:medico_id>', methods=['PUT'])
def updateMedico(medico_id):
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar campos requeridos
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'sexo', 'telefono', 'correo', 'matricula', 'id_especialidad', 'fecha_nacimiento', 'id_estado_civil', 'direccion', 'id_ciudad']
    for campo in campos_requeridos:
        if campo not in data or not data[campo].strip():
           return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        # Procesar los datos
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        sexo = data['sexo']
        telefono = data['telefono'].strip()
        correo = data['correo'].strip()
        matricula = data['matricula'].strip()
        id_especialidad = data['id_especialidad']
        fecha_nacimiento = data['fecha_nacimiento']
        id_estado_civil = data['id_estado_civil']
        direccion = data['direccion'].strip()
        id_ciudad = data['id_ciudad']

        medico_id = medicodao.guardarMedico(nombre, apellido, cedula, sexo, telefono, correo, matricula, id_especialidad, fecha_nacimiento, id_estado_civil, direccion, id_ciudad)

        if medico_id  is not None:
            return jsonify({
                'success': True,
                'data': {'id_medico': medico_id, 'nombre': nombre, 'apellido': apellido, 'cedula': cedula, 'sexo': sexo, 'telefono': telefono, 'correo': correo, 'matricula': matricula, 'id_especialidad': id_especialidad, 'fecha_nacimiento': fecha_nacimiento, 'id_estado_civil': id_estado_civil, 'direccion': direccion, 'id_ciudad': id_ciudad},
                'error': None
        }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el médico.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar el médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Eliminar un médico
@medapi.route('/medicos/<int:medico_id>', methods=['DELETE'])
def deleteMedico(medico_id):
    app.logger.info(f"Solicitud DELETE recibida para eliminar médico con ID: {medico_id}")
    medicodao = MedicoDao()
    try:
        if medicodao.deleteMedico(medico_id):
            return jsonify({
                'success': True,
                'mensaje': f'Médico con ID {medico_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el médico para eliminar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar el médico: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
