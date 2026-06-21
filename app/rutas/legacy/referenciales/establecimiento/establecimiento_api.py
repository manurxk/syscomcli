from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.dao.referenciales.establecimiento.EstablecimientoDao import EstablecimientoDao

establecimientoapi = Blueprint('establecimientoapi', __name__)

# ===============================
# Trae todos los establecimientos
# ===============================
@establecimientoapi.route('/establecimientos', methods=['GET'])
def getEstablecimientos():
    establecimientodao = EstablecimientoDao()
    id_sede = request.args.get('id_sede', type=int)
    try:
        establecimientos = establecimientodao.getEstablecimientos(id_sede)
        return jsonify({
            'success': True,
            'data': establecimientos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los establecimientos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae establecimientos por sede
# ===============================
@establecimientoapi.route('/establecimientos/sede/<int:sede_id>', methods=['GET'])
def getEstablecimientosPorSede(sede_id):
    establecimientodao = EstablecimientoDao()
    try:
        establecimientos = establecimientodao.getEstablecimientosPorSede(sede_id)
        return jsonify({
            'success': True,
            'data': establecimientos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener establecimientos por sede: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae un establecimiento por ID
# ===============================
@establecimientoapi.route('/establecimientos/<int:establecimiento_id>', methods=['GET'])
def getEstablecimiento(establecimiento_id):
    establecimientodao = EstablecimientoDao()
    try:
        establecimiento = establecimientodao.getEstablecimientoById(establecimiento_id)
        if establecimiento:
            return jsonify({
                'success': True,
                'data': establecimiento,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el establecimiento con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener establecimiento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega un nuevo establecimiento
# ===============================
@establecimientoapi.route('/establecimientos', methods=['POST'])
def addEstablecimiento():
    data = request.get_json()
    establecimientodao = EstablecimientoDao()

    campos_requeridos = ['id_sede', 'nombre_establecimiento']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        establecimiento_id = establecimientodao.guardarEstablecimiento(data)
        if establecimiento_id:
            establecimiento = establecimientodao.getEstablecimientoById(establecimiento_id)
            return jsonify({
                'success': True,
                'data': establecimiento,
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el establecimiento (código duplicado, código inválido o datos inválidos).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar establecimiento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza un establecimiento
# ===============================
@establecimientoapi.route('/establecimientos/<int:establecimiento_id>', methods=['PUT'])
def updateEstablecimiento(establecimiento_id):
    data = request.get_json()
    establecimientodao = EstablecimientoDao()

    if 'nombre_establecimiento' not in data or not data['nombre_establecimiento']:
        return jsonify({
            'success': False,
            'error': 'El campo nombre_establecimiento es obligatorio.'
        }), 400

    try:
        if establecimientodao.updateEstablecimiento(establecimiento_id, data):
            establecimiento = establecimientodao.getEstablecimientoById(establecimiento_id)
            return jsonify({
                'success': True,
                'data': establecimiento,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el establecimiento con el ID proporcionado o no se pudo actualizar (código inválido).'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar establecimiento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina un establecimiento
# ===============================
@establecimientoapi.route('/establecimientos/<int:establecimiento_id>', methods=['DELETE'])
def deleteEstablecimiento(establecimiento_id):
    establecimientodao = EstablecimientoDao()
    try:
        resultado = establecimientodao.deleteEstablecimiento(establecimiento_id)
        if resultado == "en_uso":
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar el establecimiento porque tiene puntos de expedición asociados.'
            }), 400
        elif resultado:
            return jsonify({
                'success': True,
                'mensaje': f'Establecimiento con ID {establecimiento_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el establecimiento con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar establecimiento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
