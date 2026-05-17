from flask import Blueprint, request, jsonify
from flask import current_app as app
from app.dao.referenciales.sede.SedeDao import SedeDao

sedeapi = Blueprint('sedeapi', __name__)

# ===============================
# Trae todas las sedes
# ===============================
@sedeapi.route('/sedes', methods=['GET'])
def getSedes():
    sededao = SedeDao()
    id_empresa = request.args.get('id_empresa', type=int)
    try:
        sedes = sededao.getSedes(id_empresa)
        return jsonify({
            'success': True,
            'data': sedes,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las sedes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae sedes por empresa
# ===============================
@sedeapi.route('/sedes/empresa/<int:empresa_id>', methods=['GET'])
def getSedesPorEmpresa(empresa_id):
    sededao = SedeDao()
    try:
        sedes = sededao.getSedesPorEmpresa(empresa_id)
        return jsonify({
            'success': True,
            'data': sedes,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener sedes por empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae una sede por ID
# ===============================
@sedeapi.route('/sedes/<int:sede_id>', methods=['GET'])
def getSede(sede_id):
    sededao = SedeDao()
    try:
        sede = sededao.getSedeById(sede_id)
        if sede:
            return jsonify({
                'success': True,
                'data': sede,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la sede con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener sede: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega una nueva sede
# ===============================
@sedeapi.route('/sedes', methods=['POST'])
def addSede():
    data = request.get_json()
    sededao = SedeDao()

    campos_requeridos = ['id_empresa', 'des_sede']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        sede_id = sededao.guardarSede(data)
        if sede_id:
            sede = sededao.getSedeById(sede_id)
            return jsonify({
                'success': True,
                'data': sede,
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la sede (código duplicado o datos inválidos).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar sede: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza una sede
# ===============================
@sedeapi.route('/sedes/<int:sede_id>', methods=['PUT'])
def updateSede(sede_id):
    data = request.get_json()
    sededao = SedeDao()

    if 'des_sede' not in data or not data['des_sede']:
        return jsonify({
            'success': False,
            'error': 'El campo des_sede es obligatorio.'
        }), 400

    try:
        if sededao.updateSede(sede_id, data):
            sede = sededao.getSedeById(sede_id)
            return jsonify({
                'success': True,
                'data': sede,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la sede con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar sede: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina una sede
# ===============================
@sedeapi.route('/sedes/<int:sede_id>', methods=['DELETE'])
def deleteSede(sede_id):
    sededao = SedeDao()

    try:
        resultado = sededao.deleteSede(sede_id)
        if resultado is True:
            return jsonify({
                'success': True,
                'mensaje': f'Sede con ID {sede_id} eliminada correctamente.',
                'error': None
            }), 200
        elif resultado == "en_uso":
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar esta sede porque tiene consultorios asociados.'
            }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la sede.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar sede: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500
