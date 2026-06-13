from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.agendamiento.feriado.FeriadoDao import FeriadoDao

feriadoapi = Blueprint('feriadoapi', __name__)

# ===============================
# Trae todos los feriados
# ===============================
@feriadoapi.route('/feriados', methods=['GET'])
def getFeriados():
    dao = FeriadoDao()
    try:
        feriados = dao.getFeriados()
        return jsonify({
            'success': True,
            'data': feriados,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los feriados: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae un feriado por ID
# ===============================
@feriadoapi.route('/feriados/<int:feriado_id>', methods=['GET'])
def getFeriado(feriado_id):
    dao = FeriadoDao()
    try:
        f = dao.getFeriadoById(feriado_id)
        if f:
            return jsonify({
                'success': True,
                'data': f,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el feriado con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener feriado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega un nuevo feriado
# ===============================
@feriadoapi.route('/feriados', methods=['POST'])
def addFeriado():
    data = request.get_json()
    dao = FeriadoDao()

    campos_requeridos = ['fecha', 'descripcion', 'estado']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio.'}), 400
        if campo == 'descripcion' and (not data[campo] or len(str(data[campo]).strip()) == 0):
            return jsonify({'success': False, 'error': 'La descripción no puede estar vacía.'}), 400

    try:
        fecha = data['fecha']
        descripcion = str(data['descripcion']).strip()
        estado = str(data['estado']).upper() in ['A', 'TRUE', '1', 'ACTIVO']

        feriado_id = dao.guardarFeriado(fecha, descripcion, estado)
        if feriado_id:
            return jsonify({
                'success': True,
                'data': {'id': feriado_id, 'fecha': fecha, 'descripcion': descripcion, 'estado': estado},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el feriado. Verifique si la fecha ya existe.'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar feriado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

# ===============================
# Actualiza un feriado
# ===============================
@feriadoapi.route('/feriados/<int:feriado_id>', methods=['PUT'])
def updateFeriado(feriado_id):
    data = request.get_json()
    dao = FeriadoDao()

    campos_requeridos = ['fecha', 'descripcion', 'estado']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio.'}), 400

    try:
        fecha = data['fecha']
        descripcion = str(data['descripcion']).strip()
        estado = str(data['estado']).upper() in ['A', 'TRUE', '1', 'ACTIVO']

        if dao.updateFeriado(feriado_id, fecha, descripcion, estado):
            return jsonify({
                'success': True,
                'data': {'id': feriado_id, 'fecha': fecha, 'descripcion': descripcion, 'estado': estado},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar. Verifique si existe o si la nueva fecha entra en conflicto.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar feriado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

# ===============================
# Elimina un feriado
# ===============================
@feriadoapi.route('/feriados/<int:feriado_id>', methods=['DELETE'])
def deleteFeriado(feriado_id):
    dao = FeriadoDao()
    try:
        if dao.deleteFeriado(feriado_id):
            return jsonify({
                'success': True,
                'mensaje': f'Feriado eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el feriado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar feriado: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
