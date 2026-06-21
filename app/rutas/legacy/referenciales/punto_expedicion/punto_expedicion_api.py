from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.dao.referenciales.punto_expedicion.PuntoExpedicionDao import PuntoExpedicionDao

puntoexpedicionapi = Blueprint('puntoexpedicionapi', __name__)

# ===============================
# Trae todos los puntos de expedición
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion', methods=['GET'])
def getPuntosExpedicion():
    puntoexpediciondao = PuntoExpedicionDao()
    id_establecimiento = request.args.get('id_establecimiento', type=int)
    try:
        puntos = puntoexpediciondao.getPuntosExpedicion(id_establecimiento)
        return jsonify({
            'success': True,
            'data': puntos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los puntos de expedición: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae puntos de expedición por establecimiento
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion/establecimiento/<int:establecimiento_id>', methods=['GET'])
def getPuntosExpedicionPorEstablecimiento(establecimiento_id):
    puntoexpediciondao = PuntoExpedicionDao()
    try:
        puntos = puntoexpediciondao.getPuntosExpedicionPorEstablecimiento(establecimiento_id)
        return jsonify({
            'success': True,
            'data': puntos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener puntos de expedición por establecimiento: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae un punto de expedición por ID
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion/<int:punto_expedicion_id>', methods=['GET'])
def getPuntoExpedicion(punto_expedicion_id):
    puntoexpediciondao = PuntoExpedicionDao()
    try:
        punto = puntoexpediciondao.getPuntoExpedicionById(punto_expedicion_id)
        if punto:
            return jsonify({
                'success': True,
                'data': punto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el punto de expedición con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener punto de expedición: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae próximo número disponible
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion/<int:punto_expedicion_id>/proximo-numero', methods=['GET'])
def getProximoNumero(punto_expedicion_id):
    puntoexpediciondao = PuntoExpedicionDao()
    try:
        siguiente = puntoexpediciondao.getProximoNumero(punto_expedicion_id)
        if siguiente:
            return jsonify({
                'success': True,
                'data': siguiente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el punto de expedición.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener próximo número: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega un nuevo punto de expedición
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion', methods=['POST'])
def addPuntoExpedicion():
    data = request.get_json()
    puntoexpediciondao = PuntoExpedicionDao()

    campos_requeridos = ['id_establecimiento', 'nombre_punto_expedicion']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        punto_id = puntoexpediciondao.guardarPuntoExpedicion(data)
        if punto_id:
            punto = puntoexpediciondao.getPuntoExpedicionById(punto_id)
            return jsonify({
                'success': True,
                'data': punto,
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el punto de expedición (código duplicado, código inválido o datos inválidos).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar punto de expedición: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza un punto de expedición
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion/<int:punto_expedicion_id>', methods=['PUT'])
def updatePuntoExpedicion(punto_expedicion_id):
    data = request.get_json()
    puntoexpediciondao = PuntoExpedicionDao()

    if 'nombre_punto_expedicion' not in data or not data['nombre_punto_expedicion']:
        return jsonify({
            'success': False,
            'error': 'El campo nombre_punto_expedicion es obligatorio.'
        }), 400

    try:
        if puntoexpediciondao.updatePuntoExpedicion(punto_expedicion_id, data):
            punto = puntoexpediciondao.getPuntoExpedicionById(punto_expedicion_id)
            return jsonify({
                'success': True,
                'data': punto,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el punto de expedición con el ID proporcionado o no se pudo actualizar (código inválido).'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar punto de expedición: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina un punto de expedición
# ===============================
@puntoexpedicionapi.route('/puntos-expedicion/<int:punto_expedicion_id>', methods=['DELETE'])
def deletePuntoExpedicion(punto_expedicion_id):
    puntoexpediciondao = PuntoExpedicionDao()
    try:
        resultado = puntoexpediciondao.deletePuntoExpedicion(punto_expedicion_id)
        if resultado == "en_uso":
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar el punto de expedición porque tiene facturas asociadas.'
            }), 400
        elif resultado:
            return jsonify({
                'success': True,
                'mensaje': f'Punto de expedición con ID {punto_expedicion_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el punto de expedición con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar punto de expedición: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
