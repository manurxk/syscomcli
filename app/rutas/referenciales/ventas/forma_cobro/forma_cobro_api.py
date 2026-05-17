from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ventas.forma_cobro.FormaCobroDao import FormaCobroDao

forma_cobro_api = Blueprint('forma_cobro_api', __name__)

# ===============================
# Trae todas las formas de cobro
# ===============================
@forma_cobro_api.route('/formas_cobro', methods=['GET'])
def getFormasCobro():
    forma_cobro_dao = FormaCobroDao()

    try:
        formas_cobro = forma_cobro_dao.getFormasCobro()

        return jsonify({
            'success': True,
            'data': formas_cobro,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener todas las formas de cobro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae una forma de cobro por ID
# ===============================
@forma_cobro_api.route('/formas_cobro/<int:forma_cobro_id>', methods=['GET'])
def getFormaCobro(forma_cobro_id):
    forma_cobro_dao = FormaCobroDao()

    try:
        forma_cobro = forma_cobro_dao.getFormaCobroById(forma_cobro_id)

        if forma_cobro:
            return jsonify({
                'success': True,
                'data': forma_cobro,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la forma de cobro con el ID proporcionado.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener forma de cobro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega una nueva forma de cobro
# ===============================
@forma_cobro_api.route('/formas_cobro', methods=['POST'])
def addFormaCobro():
    data = request.get_json()
    forma_cobro_dao = FormaCobroDao()

    campos_requeridos = ['descripcion', 'estado']

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
        if campo == 'descripcion' and (data[campo] is None or len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': 'La descripción no puede estar vacía.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        requiere_entidad = data.get('requiere_entidad', False)
        permite_cuotas = data.get('permite_cuotas', False)
        estado = data.get('estado', 'A')

        # Validar estado
        if estado not in ['A', 'I']:
            return jsonify({
                'success': False,
                'error': 'El estado debe ser "A" (Activo) o "I" (Inactivo).'
            }), 400

        forma_cobro_id = forma_cobro_dao.guardarFormaCobro(
            descripcion, codigo, requiere_entidad, permite_cuotas, estado
        )
        if forma_cobro_id:
            return jsonify({
                'success': True,
                'data': {
                    'id': forma_cobro_id,
                    'descripcion': descripcion,
                    'codigo': codigo,
                    'requiere_entidad': requiere_entidad,
                    'permite_cuotas': permite_cuotas,
                    'estado': estado
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la forma de cobro (duplicada o inválida).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar forma de cobro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza una forma de cobro
# ===============================
@forma_cobro_api.route('/formas_cobro/<int:forma_cobro_id>', methods=['PUT'])
def updateFormaCobro(forma_cobro_id):
    data = request.get_json()
    forma_cobro_dao = FormaCobroDao()

    campos_requeridos = ['descripcion', 'estado']

    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
        if campo == 'descripcion' and (data[campo] is None or len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': 'La descripción no puede estar vacía.'
            }), 400

    try:
        descripcion = data['descripcion'].upper()
        codigo = data.get('codigo', '').upper() if data.get('codigo') else None
        requiere_entidad = data.get('requiere_entidad', False)
        permite_cuotas = data.get('permite_cuotas', False)
        estado = data.get('estado', 'A')

        # Validar estado
        if estado not in ['A', 'I']:
            return jsonify({
                'success': False,
                'error': 'El estado debe ser "A" (Activo) o "I" (Inactivo).'
            }), 400

        if forma_cobro_dao.updateFormaCobro(
            forma_cobro_id, descripcion, codigo, requiere_entidad, permite_cuotas, estado
        ):
            return jsonify({
                'success': True,
                'data': {
                    'id': forma_cobro_id,
                    'descripcion': descripcion,
                    'codigo': codigo,
                    'requiere_entidad': requiere_entidad,
                    'permite_cuotas': permite_cuotas,
                    'estado': estado
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la forma de cobro con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar forma de cobro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina una forma de cobro
# ===============================
@forma_cobro_api.route('/formas_cobro/<int:forma_cobro_id>', methods=['DELETE'])
def deleteFormaCobro(forma_cobro_id):
    forma_cobro_dao = FormaCobroDao()

    try:
        resultado = forma_cobro_dao.deleteFormaCobro(forma_cobro_id)
        if resultado is True:
            return jsonify({
                'success': True,
                'mensaje': f'Forma de cobro con ID {forma_cobro_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la forma de cobro porque está siendo usada.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al eliminar forma de cobro: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


















