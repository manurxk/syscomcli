from flask import Blueprint, request, jsonify, current_app as app
from app.dao.persona.medico.MedicoDao import MedicoDao
from app.dao.referenciales.estado_civil import Estado_civilDao
from app.dao.referenciales.especialidad.EspecialidadDao import EspecialidadDao
from app.dao.referenciales.ciudad.CiudadDao import CiudadDao
 
medapi = Blueprint('medapi', __name__)

# Trae todas las medicos
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
        app.logger.error(f"Error al obtener todas las medicos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@medapi.route('/medicos/<int:medico_id>', methods=['GET'])
def getMedico(medico_id):
    medicodao = MedicoDao()

    try:
        medico = medicodao.getMedicosById(medico_id)

        if medico:
            return jsonify({
                'success': True,
                'data': medico,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener la persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega una nueva persona
@medapi.route('/medicos', methods=['POST'])
def addMedico():
    
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar que el JSON no esté vacío y tenga las propiedades necesarias
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'sexo', 'telefono', 'correo', 'matricula', 'id_especialidad', 'fecha_nacimiento', 'id_estado_civil', 'direccion', 'id_ciudad']
    
    # Verificar si faltan campos o son vacíos
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    # Verificar existencia de la especialidad, estado_civil y ciudad
    try:
        estado_civil_dao = Estado_civilDao()
        especialidad_dao = EspecialidadDao()
        ciudad_dao = CiudadDao()

        estado_civil_valido = estado_civil_dao.obtenerEstadoCivilPorId(data['id_estado_civil'])
        especialidad_valida = especialidad_dao.obtenerEspecialidadPorId(data['id_especialidad'])
        ciudad_valida = ciudad_dao.obtenerCiudadPorId(data['id_ciudad'])

        if not estado_civil_valido:
            return jsonify({'success': False, 'error': 'El estado civil no existe.'}), 400
        if not especialidad_valida:
            return jsonify({'success': False, 'error': 'La especialidad no existe.'}), 400
        if not ciudad_valida:
            return jsonify({'success': False, 'error': 'La ciudad no existe.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ocurrió un error al validar las claves foráneas: {str(e)}'}), 500

    # Procesar la solicitud
    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        sexo = data['sexo'].strip()  # Agregando strip() por si tiene espacios alrededor
        telefono = data['telefono'].strip()
        correo = data['correo'].strip()
        matricula = data['matricula'].strip()
        id_especialidad = data['id_especialidad']
        fecha_nacimiento = data['fecha_nacimiento']
        id_estado_civil = data['id_estado_civil']
        direccion = data['direccion'].strip()
        id_ciudad = data['id_ciudad']

        # Guardar el nuevo médico en la base de datos
        medico_id = medicodao.guardarMedico(
            nombre, apellido, cedula, sexo, telefono, correo, matricula,
            id_especialidad, fecha_nacimiento, id_estado_civil, direccion, id_ciudad
        )

        if medico_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_medico': medico_id, 'nombre': nombre, 'apellido': apellido, 
                         'cedula': cedula, 'sexo': sexo, 'telefono': telefono, 'correo': correo, 
                         'matricula': matricula, 'id_especialidad': id_especialidad, 'fecha_nacimiento': fecha_nacimiento, 
                         'id_estado_civil': id_estado_civil, 'direccion': direccion, 'id_ciudad': id_ciudad},
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



















@medapi.route('/medicos/<int:medico_id>', methods=['PUT'])
def updateMedico(medico_id):
    data = request.get_json()
    medicodao = MedicoDao()

    # Validar campos obligatorios
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'sexo', 'telefono', 'correo', 'matricula', 'id_especialidad', 'fecha_nacimiento', 'id_estado_civil', 'direccion', 'id_ciudad']
    
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    # Verificar existencia de las claves foráneas
    try:
        estado_civil_dao = Estado_civilDao()
        especialidad_dao = EspecialidadDao()
        ciudad_dao = CiudadDao()

        estado_civil_valido = estado_civil_dao.obtenerEstadoCivilPorId(data['id_estado_civil'])
        especialidad_valida = especialidad_dao.obtenerEspecialidadPorId(data['id_especialidad'])
        ciudad_valida = ciudad_dao.obtenerCiudadPorId(data['id_ciudad'])

        if not estado_civil_valido:
            return jsonify({'success': False, 'error': 'El estado civil no existe.'}), 400
        if not especialidad_valida:
            return jsonify({'success': False, 'error': 'La especialidad no existe.'}), 400
        if not ciudad_valida:
            return jsonify({'success': False, 'error': 'La ciudad no existe.'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': f'Ocurrió un error al validar las claves foráneas: {str(e)}'}), 500

    # Actualizar el médico
    try:
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

        medico_id = medicodao.guardarMedico(
            nombre, apellido, cedula, sexo, telefono, correo, matricula,
            id_especialidad, fecha_nacimiento, id_estado_civil, direccion, id_ciudad
        )

        if medico_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_medico': medico_id, 'nombre': nombre, 'apellido': apellido, 
                         'cedula': cedula, 'sexo': sexo, 'telefono': telefono, 'correo': correo, 
                         'matricula': matricula, 'id_especialidad': id_especialidad, 'fecha_nacimiento': fecha_nacimiento, 
                         'id_estado_civil': id_estado_civil, 'direccion': direccion, 'id_ciudad': id_ciudad},
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

@medapi.route('/medicos/<int:medico_id>', methods=['DELETE'])
def deleteMedico(medico_id):
    medicodao = MedicoDao()

    try:
        # Verificar si el médico tiene dependencias (por ejemplo, citas o registros) que impidan la eliminación
        if medicodao.tieneDependencias(medico_id):
            return jsonify({
                'success': False,
                'error': 'El médico tiene dependencias (citas, registros) que impiden su eliminación.'
            }), 400

        # Eliminar el médico si no tiene dependencias
        if medicodao.deleteMedico(medico_id):
            # Registrar la acción exitosa
            app.logger.info(f"Médico con ID {medico_id} eliminado correctamente.")
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
        # Registrar el error para diagnósticos
        app.logger.error(f"Error al eliminar medico con ID {medico_id}: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
