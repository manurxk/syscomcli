from flask import Blueprint, request, jsonify, current_app as app
from app.dao.especialista.EspecialistaDao import EspecialistaDao

especiapi = Blueprint('especiapi', __name__)

# Trae todos los especialistas
@especiapi.route('/especialistas', methods=['GET'])
def getEspecialistas():
    especialistaDao = EspecialistaDao()

    try:
        especialistas = especialistaDao.getEspecialistas()
        return jsonify({
            'success': True,
            'data': especialistas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los especialistas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Trae un especialista por ID
@especiapi.route('/especialistas/<int:especialista_id>', methods=['GET'])
def getEspecialista(especialista_id):
    especialistaDao = EspecialistaDao()

    try:
        especialista = especialistaDao.getEspecialistaById(especialista_id)

        if especialista:
            return jsonify({
                'success': True,
                'data': especialista,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el especialista con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el especialista: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Agrega un nuevo especialista
@especiapi.route('/especialistas', methods=['POST'])
def addEspecialista():
    data = request.get_json()
    especialistaDao = EspecialistaDao()

    # Validar campos requeridos
    campos_requeridos = ['nombre', 'apellido', 'cedula', 'sexo', 'fecha_nacimiento', 'telefono', 'correo', 'matricula', 'id_especialidad',  'id_estado_civil', 'direccion', 'id_ciudad']
    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
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
        fecha_nacimiento = data['fecha_nacimiento']
        telefono = data['telefono'].strip()
        correo = data['correo'].strip()
        matricula = data['matricula'].strip()
        id_especialidad = data['id_especialidad']
        id_estado_civil = data['id_estado_civil']
        direccion = data['direccion'].strip()
        id_ciudad = data['id_ciudad']

        # Llamar al método DAO para insertar el especialista
        especialista_id = especialistaDao.guardarEspecialista(
            nombre, apellido, cedula, sexo, fecha_nacimiento,
            telefono, correo, matricula, id_especialidad, id_estado_civil, direccion, id_ciudad
        )

        if especialista_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id_especialista': especialista_id,  # Aquí agregamos id_especialista que es devuelto por la base de datos
                    'nombre': nombre,
                    'apellido': apellido,
                    'cedula': cedula,
                    'sexo': sexo,
                    'fecha_nacimiento': fecha_nacimiento,
                    'telefono': telefono,
                    'correo': correo,
                    'matricula': matricula,
                    'id_especialidad': id_especialidad,
                    'id_estado_civil': id_estado_civil,
                    'direccion': direccion,
                    'id_ciudad': id_ciudad
                },
                'error': None
            }), 201

        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el especialista.'}), 500
    
    except Exception as e:
        # Manejo de errores y registros de logs
        app.logger.error(f"Error al agregar especialista: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# Actualizar un especialista
@especiapi.route('/especialistas/<int:especialista_id>', methods=['PUT'])
def updateEspecialista(especialista_id):
    data = request.get_json()
    especialistaDao = EspecialistaDao()

    # Validar que se envíen datos
    if not data:
        return jsonify({'success': False, 'error': 'No se enviaron datos para actualizar.'}), 400

    # Lista de campos requeridos
    campos_requeridos = [
        'nombre', 'apellido', 'cedula', 'sexo', 'fecha_nacimiento', 'telefono', 'correo',
        'matricula', 'id_especialidad', 'id_estado_civil', 'direccion', 'id_ciudad'
    ]

    # Validar que todos los campos estén presentes y no vacíos
    for campo in campos_requeridos:
        if campo not in data or (isinstance(data[campo], str) and not data[campo].strip()):
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    try:
        # Convertir valores a mayúsculas o limpiar espacios
        especialista_data = {
            'id': especialista_id,
            'nombre': data.get('nombre', '').strip().upper(),
            'apellido': data.get('apellido', '').strip().upper(),
            'cedula': data.get('cedula', '').strip(),
            'sexo': data.get('sexo', '').strip().upper(),
            'fecha_nacimiento': data.get('fecha_nacimiento', '').strip(),
            'telefono': data.get('telefono', '').strip(),
            'correo': data.get('correo', '').strip(),
            'matricula': data.get('matricula', '').strip(),
            'id_especialidad': int(data.get('id_especialidad', 0)) if data.get('id_especialidad') else None,
            'id_estado_civil': int(data.get('id_estado_civil', 0)) if data.get('id_estado_civil') else None,
            'direccion': data.get('direccion', '').strip().upper(),
            'id_ciudad': int(data.get('id_ciudad', 0)) if data.get('id_ciudad') else None
        }

        # Validar que los campos numéricos sean valores válidos
        for campo in ['id_especialidad', 'id_estado_civil', 'id_ciudad']:
            if especialista_data[campo] is None:
                return jsonify({'success': False, 'error': f'El campo {campo} debe ser un número válido.'}), 400

        # Llamar a la función de actualización en el DAO
        resultado = especialistaDao.updateEspecialista(
            especialista_data['nombre'],
            especialista_data['apellido'],
            especialista_data['cedula'],
            especialista_data['sexo'],
            especialista_data['fecha_nacimiento'],
            especialista_data['telefono'],
            especialista_data['correo'],
            especialista_data['matricula'],
            especialista_data['id_especialidad'],
            especialista_data['id_estado_civil'],
            especialista_data['direccion'],
            especialista_data['id_ciudad']
        )


        if resultado:
            return jsonify({'success': True, 'data': especialista_data, 'message': 'Especialista actualizado correctamente'}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el especialista. Puede que no exista.'}), 404

    except ValueError as ve:
        app.logger.error(f"Error de conversión de datos: {str(ve)}")
        return jsonify({'success': False, 'error': 'Error en los datos enviados. Verifique los formatos.'}), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar el especialista: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


# Eliminar un especialista
@especiapi.route('/especialistas/<int:especialista_id>', methods=['DELETE'])
def deleteEspecialista(especialista_id):
    app.logger.info(f"Solicitud DELETE recibida para eliminar especialista con ID: {especialista_id}")
    especialistaDao = EspecialistaDao()
    try:
        if especialistaDao.deleteEspecialista(especialista_id):
            return jsonify({
                'success': True,
                'mensaje': f'Especialista con ID {especialista_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el especialista para eliminar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar el especialista: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
