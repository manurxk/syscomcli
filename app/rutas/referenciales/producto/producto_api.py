from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.producto.ProductoDao import ProductoDao

proapi = Blueprint('proapi', __name__)

def validar_campos_requeridos(data, campos):
    for campo in campos:
        if campo not in data or data[campo] is None or len(str(data[campo]).strip()) == 0:
            return campo
    return None

# Obtener todos los productos
@proapi.route('/productos', methods=['GET'])
def getProductos():
    prodao = ProductoDao()
    try:
        productos = prodao.getProductos()
        return jsonify({
            'success': True,
            'data': productos,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los productos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500

# Obtener producto por ID
@proapi.route('/productos/<int:producto_id>', methods=['GET'])
def getProducto(producto_id):
    prodao = ProductoDao()
    try:
        producto = prodao.getProductoById(producto_id)
        if producto:
            return jsonify({'success': True, 'data': producto, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el producto con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener producto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500

# Agregar nuevo producto
@proapi.route('/productos', methods=['POST'])
def addProducto():
    data = request.get_json()
    prodao = ProductoDao()
    campos_requeridos = ['descripcion', 'cantidad', 'precio_unitario']

    campo_faltante = validar_campos_requeridos(data, campos_requeridos)
    if campo_faltante:
        return jsonify({'success': False, 'error': f'El campo {campo_faltante} es obligatorio y no puede estar vacío.'}), 400

    try:
        descripcion = data['descripcion'].upper()
        cantidad = int(data['cantidad'])
        precio_unitario = float(data['precio_unitario'])

        producto_id = prodao.guardarProducto(descripcion, cantidad, precio_unitario)
        if producto_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': producto_id, 'descripcion': descripcion, 'cantidad': cantidad, 'precio_unitario': precio_unitario},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el producto. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar producto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500

# Actualizar producto
@proapi.route('/productos/<int:producto_id>', methods=['PUT'])
def updateProducto(producto_id):
    data = request.get_json()
    prodao = ProductoDao()
    campos_requeridos = ['descripcion', 'cantidad', 'precio_unitario']

    campo_faltante = validar_campos_requeridos(data, campos_requeridos)
    if campo_faltante:
        return jsonify({'success': False, 'error': f'El campo {campo_faltante} es obligatorio y no puede estar vacío.'}), 400

    try:
        descripcion = data['descripcion'].upper()
        cantidad = int(data['cantidad'])
        precio_unitario = float(data['precio_unitario'])

        if prodao.updateProducto(producto_id, descripcion, cantidad, precio_unitario):
            return jsonify({
                'success': True,
                'data': {'id': producto_id, 'descripcion': descripcion, 'cantidad': cantidad, 'precio_unitario': precio_unitario},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el producto con el ID proporcionado o no se pudo actualizar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar producto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500

# Eliminar producto
@proapi.route('/productos/<int:producto_id>', methods=['DELETE'])
def deleteProducto(producto_id):
    prodao = ProductoDao()
    try:
        if prodao.deleteProducto(producto_id):
            return jsonify({'success': True, 'mensaje': f'Producto con ID {producto_id} eliminado correctamente.', 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el producto con el ID proporcionado o no se pudo eliminar.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar producto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500
