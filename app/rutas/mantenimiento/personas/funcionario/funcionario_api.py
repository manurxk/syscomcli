from flask import Blueprint, request, jsonify, current_app as app, session
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.auth.utils.decorators import role_required


funcionarioapi = Blueprint('funcionarioapi', __name__)




# ============================================
# OBTENER TODOS LOS FUNCIONARIOS
# ============================================
@funcionarioapi.route('/funcionarios', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getFuncionarios():
    """Obtiene la lista completa de funcionarios"""
    funcionariodao = FuncionarioDao()
    
    try:
        funcionarios = funcionariodao.getFuncionarios()
        
        return jsonify({
            'success': True,
            'data': funcionarios,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener todos los funcionarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER SOLO ESPECIALISTAS
# ============================================
@funcionarioapi.route('/funcionarios/especialistas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA")
def getFuncionariosEspecialistas():
    """Obtiene solo los funcionarios que son especialistas"""
    funcionariodao = FuncionarioDao()
    
    try:
        especialistas = funcionariodao.getFuncionariosEspecialistas()
        
        return jsonify({
            'success': True,
            'data': especialistas,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER ESPECIALIDADES POR ESPECIALISTA
# ============================================
@funcionarioapi.route('/funcionarios/especialistas/<int:id_especialista>/especialidades', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA")
def getEspecialidadesEspecialista(id_especialista):
    """Obtiene las especialidades de un especialista por su id_especialista"""
    funcionariodao = FuncionarioDao()
    
    try:
        especialidades = funcionariodao.getEspecialidadesByEspecialista(id_especialista)
        
        return jsonify({
            'success': True,
            'data': especialidades,
            'error': None
        }), 200
    
    except Exception as e:
        app.logger.error(f"Error al obtener especialidades del especialista: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ============================================
# OBTENER FUNCIONARIO POR ID
# ============================================
@funcionarioapi.route('/funcionarios/<int:id_funcionario>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getFuncionario(id_funcionario):
    """Obtiene un funcionario específico por su ID"""
    funcionariodao = FuncionarioDao()
    
    try:
        funcionario = funcionariodao.getFuncionarioById(id_funcionario)
        
        if funcionario:
            return jsonify({
                'success': True,
                'data': funcionario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario con el ID proporcionado.'
            }), 404
    
    except Exception as e:
        app.logger.error(f"Error al obtener el funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ============================================
# OBTENER FUNCIONARIO PARA EDITAR
# ============================================
@funcionarioapi.route('/funcionarios/<int:id_funcionario>/editar', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getFuncionarioParaEditar(id_funcionario):
    """Obtiene funcionario con IDs originales para formulario de edición"""
    funcionariodao = FuncionarioDao()

    try:
        funcionario = funcionariodao.getFuncionarioParaEditar(id_funcionario)

        if funcionario:
            return jsonify({
                'success': True,
                'data': funcionario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener funcionario para editar: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ============================================
# CREAR NUEVO FUNCIONARIO
# ============================================
@funcionarioapi.route('/funcionarios', methods=['POST'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def addFuncionario():
    """Crea un nuevo funcionario con todos sus datos"""
    data = request.get_json()
    funcionariodao = FuncionarioDao()

    # Campos obligatorios
    campos_requeridos = [
        'nombre', 'apellido', 'cedula', 'telefono', 'id_cargo'
    ]

    # Validar campos obligatorios
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar si es especialista
    if funcionariodao.es_cargo_especialista(data['id_cargo']):
        if not data.get('esp_matricula'):
            return jsonify({
                'success': False,
                'error': 'La matrícula es obligatoria para especialistas.'
            }), 400
        
        especialidades = data.get('especialidades', [])
        if not especialidades or len(especialidades) == 0:
            return jsonify({
                'success': False,
                'error': 'Debe seleccionar al menos una especialidad.'
            }), 400

    try:
        funcionario_id = funcionariodao.guardarFuncionario(
            # Datos de persona (obligatorios)
            nombre=data['nombre'],
            apellido=data['apellido'],
            cedula=data['cedula'],
            telefono=data['telefono'],
            fecha_nacimiento=data.get('fecha_nacimiento'),

            # Datos de persona (opcionales)
            genero_id=data.get('id_genero'),
            estado_civil_id=data.get('id_estado_civil'),
            correo=data.get('correo'),
            domicilio=data.get('domicilio'),
            ciudad_id=data.get('id_ciudad'),
            ciudad_nacimiento_id=data.get('id_ciudad_nacimiento'),
            nivel_instruccion_id=data.get('id_nivel_instruccion'),
            profesion_id=data.get('id_profesion'),

            # Datos de funcionario
            id_cargo=data['id_cargo'],
            est_funcionario=data.get('activo', True),
            usuario_creacion=session.get('id_usuario'),

            # Datos de especialista (condicionales)
            esp_matricula=data.get('esp_matricula'),
            especialidades=data.get('especialidades', []),
            esp_color_agenda=data.get('esp_color_agenda', '#3498db')
        )

        if funcionario_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id_funcionario': funcionario_id,
                    'mensaje': 'Funcionario creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el funcionario. Consulte con el administrador.'
            }), 500

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al agregar funcionario: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno del servidor. Consulte con el administrador.'
        }), 500


# ============================================
# ACTUALIZAR FUNCIONARIO EXISTENTE
# ============================================
@funcionarioapi.route('/funcionarios/<int:id_funcionario>', methods=['PUT'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def updateFuncionario(id_funcionario):
    """Actualiza un funcionario existente con todos sus datos"""
    data = request.get_json()
    funcionariodao = FuncionarioDao()
    app.logger.info(f"Datos recibidos para actualizar: {data}")

    # Verificar que el funcionario existe
    funcionario_existente = funcionariodao.getFuncionarioById(id_funcionario)
    if not funcionario_existente:
        return jsonify({
            'success': False,
            'error': 'No se encontró el funcionario con el ID proporcionado.'
        }), 404

    # Campos obligatorios
    campos_requeridos = [
        'nombre', 'apellido', 'cedula', 'telefono', 'id_cargo'
    ]

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar si es especialista
    if funcionariodao.es_cargo_especialista(data['id_cargo']):
        if not data.get('esp_matricula'):
            return jsonify({
                'success': False,
                'error': 'La matrícula es obligatoria para especialistas.'
            }), 400
        
        especialidades = data.get('especialidades', [])
        if not especialidades or len(especialidades) == 0:
            return jsonify({
                'success': False,
                'error': 'Debe seleccionar al menos una especialidad.'
            }), 400

    try:
        resultado = funcionariodao.updateFuncionario(
            id_funcionario=id_funcionario,

            # Datos de persona
            nombre=data['nombre'],
            apellido=data['apellido'],
            cedula=data['cedula'],
            fecha_nacimiento=data.get('fecha_nacimiento'),
            genero_id=data.get('id_genero'),
            estado_civil_id=data.get('id_estado_civil'),
            telefono=data['telefono'],
            correo=data.get('correo'),
            domicilio=data.get('domicilio'),
            ciudad_id=data.get('id_ciudad'),
            ciudad_nacimiento_id=data.get('id_ciudad_nacimiento'),
            nivel_instruccion_id=data.get('id_nivel_instruccion'),
            profesion_id=data.get('id_profesion'),

            # Datos de funcionario
            id_cargo=data['id_cargo'],
            est_funcionario=data.get('activo', True),
            usuario_modificacion=session.get('id_usuario'),

            # Datos de especialista
            esp_matricula=data.get('esp_matricula'),
            especialidades=data.get('especialidades', []),
            esp_color_agenda=data.get('esp_color_agenda', '#3498db')
        )

        if resultado:
            return jsonify({
                'success': True,
                'data': {
                    'id_funcionario': id_funcionario,
                    'mensaje': 'Funcionario actualizado exitosamente'
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el funcionario.'
            }), 500

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar funcionario: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno del servidor. Consulte con el administrador.'
        }), 500


# ============================================
# DESACTIVAR FUNCIONARIO
# ============================================
@funcionarioapi.route('/funcionarios/<int:id_funcionario>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def deleteFuncionario(id_funcionario):
    """Desactiva un funcionario (soft-delete)"""
    funcionariodao = FuncionarioDao()

    try:
        if funcionariodao.desactivarFuncionario(id_funcionario, session.get('id_usuario')):
            return jsonify({
                'success': True,
                'mensaje': f'Funcionario con ID {id_funcionario} desactivado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el funcionario con el ID proporcionado o no se pudo desactivar.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al desactivar funcionario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500