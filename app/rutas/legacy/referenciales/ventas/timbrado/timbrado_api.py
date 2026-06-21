from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.dao.referenciales.ventas.timbrado.TimbradoDao import TimbradoDao

timbradoapi = Blueprint('timbradoapi', __name__)

# ===============================
# Trae todos los timbrados
# ===============================
@timbradoapi.route('/timbrados', methods=['GET'])
def getTimbrados():
    timbradodao = TimbradoDao()
    id_empresa = request.args.get('id_empresa', type=int)
    try:
        timbrados = timbradodao.getTimbrados(id_empresa)
        return jsonify({
            'success': True,
            'data': timbrados,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los timbrados: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae timbrados por empresa
# ===============================
@timbradoapi.route('/timbrados/empresa/<int:empresa_id>', methods=['GET'])
def getTimbradosPorEmpresa(empresa_id):
    timbradodao = TimbradoDao()
    try:
        timbrados = timbradodao.getTimbrados(empresa_id)
        return jsonify({
            'success': True,
            'data': timbrados,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados por empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae un timbrado por ID
# ===============================
@timbradoapi.route('/timbrados/<int:timbrado_id>', methods=['GET'])
def getTimbrado(timbrado_id):
    timbradodao = TimbradoDao()
    try:
        timbrado = timbradodao.getTimbradoById(timbrado_id)
        if timbrado:
            return jsonify({
                'success': True,
                'data': timbrado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el timbrado con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener timbrado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae timbrado vigente
# ===============================
@timbradoapi.route('/timbrados/vigente/<int:empresa_id>', methods=['GET'])
def getTimbradoVigente(empresa_id):
    timbradodao = TimbradoDao()
    tipo_documento = request.args.get('tipo_documento', 'factura')
    try:
        timbrado = timbradodao.getTimbradoVigente(empresa_id, tipo_documento)
        if timbrado:
            return jsonify({
                'success': True,
                'data': timbrado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró un timbrado vigente para esta empresa y tipo de documento.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener timbrado vigente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae timbrados por vencer
# ===============================
@timbradoapi.route('/timbrados/por-vencer', methods=['GET'])
def getTimbradosPorVencer():
    timbradodao = TimbradoDao()
    dias_antes = request.args.get('dias', 30, type=int)
    try:
        timbrados = timbradodao.getTimbradosPorVencer(dias_antes)
        return jsonify({
            'success': True,
            'data': timbrados,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener timbrados por vencer: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega un nuevo timbrado
# ===============================
@timbradoapi.route('/timbrados', methods=['POST'])
def addTimbrado():
    data = request.get_json()
    timbradodao = TimbradoDao()

    campos_requeridos = ['id_empresa', 'numero_timbrado', 'fecha_inicio', 'fecha_vencimiento']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        timbrado_id = timbradodao.guardarTimbrado(data)
        if timbrado_id:
            timbrado = timbradodao.getTimbradoById(timbrado_id)
            return jsonify({
                'success': True,
                'data': timbrado,
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el timbrado (número duplicado, fechas inválidas o datos incorrectos).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar timbrado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza un timbrado
# ===============================
@timbradoapi.route('/timbrados/<int:timbrado_id>', methods=['PUT'])
def updateTimbrado(timbrado_id):
    data = request.get_json()
    timbradodao = TimbradoDao()

    campos_requeridos = ['numero_timbrado', 'fecha_inicio', 'fecha_vencimiento']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        if timbradodao.updateTimbrado(timbrado_id, data):
            timbrado = timbradodao.getTimbradoById(timbrado_id)
            return jsonify({
                'success': True,
                'data': timbrado,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el timbrado con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar timbrado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina un timbrado
# ===============================
@timbradoapi.route('/timbrados/<int:timbrado_id>', methods=['DELETE'])
def deleteTimbrado(timbrado_id):
    timbradodao = TimbradoDao()

    try:
        resultado = timbradodao.deleteTimbrado(timbrado_id)
        if resultado is True:
            return jsonify({
                'success': True,
                'mensaje': f'Timbrado con ID {timbrado_id} eliminado correctamente.',
                'error': None
            }), 200
        elif resultado == "en_uso":
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar este timbrado porque tiene facturas asociadas.'
            }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el timbrado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar timbrado: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
