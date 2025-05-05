from flask import Blueprint, request, jsonify, current_app as app
from datetime import datetime
from app.dao.referenciales.cliente.ClienteDao import ClienteDao

cliapi = Blueprint('cliapi', __name__)

def response_json(success, data=None, error=None, status_code=200):
    """Función para crear respuestas JSON estándar."""
    return jsonify({
        'success': success,
        'data': data,
        'error': error
    }), status_code

@cliapi.route('/clientes', methods=['GET'])
def getClientes():
    clientedao = ClienteDao()

    try:
        clientes = clientedao.getClientes()
        return response_json(True, clientes)
    except Exception as e:
        app.logger.error(f"Error al obtener todos los clientes: {str(e)}")
        return response_json(False, error='Ocurrió un error interno. Consulte con el administrador.', status_code=500)

@cliapi.route('/clientes/<int:id_cliente>', methods=['GET'])
def getCliente(id_cliente):
    clientedao = ClienteDao()

    try:
        cliente = clientedao.getClienteById(id_cliente)

        if cliente:
            return response_json(True, cliente)
        else:
            return response_json(False, error='No se encontró el cliente con el ID proporcionado.', status_code=404)
    except Exception as e:
        app.logger.error(f"Error al obtener cliente: {str(e)}")
        return response_json(False, error='Ocurrió un error interno. Consulte con el administrador.', status_code=500)

@cliapi.route('/clientes', methods=['POST'])
def addCliente():
    data = request.get_json()
    clientedao = ClienteDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula', 'direccion', 'telefono', 'fecha_registro']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return response_json(False, error=f'El campo {campo} es obligatorio y no puede estar vacío.', status_code=400)

    # Validar el formato de fecha_registro
    try:
        fecha_registro = datetime.strptime(data['fecha_registro'], "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return response_json(False, error='El formato de fecha_registro es inválido. Debe ser YYYY-MM-DDTHH:MM:SS.', status_code=400)

    try:
        id_cliente = clientedao.guardarCliente(
            data['nombre'].strip().upper(),
            data['apellido'].strip().upper(),
            data['cedula'],
            data['direccion'].strip().upper(),
            data['telefono'],
            fecha_registro
        )

        return response_json(True, {
            'id_cliente': id_cliente,
            'nombre': data['nombre'].upper(),
            'apellido': data['apellido'].upper(),
            'cedula': data['cedula'],
            'direccion': data['direccion'].upper(),
            'telefono': data['telefono'],
            'fecha_registro': fecha_registro
        }, status_code=201)

    except Exception as e:
        app.logger.error(f"Error al agregar cliente: {str(e)}")
        return response_json(False, error='Ocurrió un error interno. Consulte con el administrador.', status_code=500)

@cliapi.route('/clientes/<int:id_cliente>', methods=['PUT'])
def updateCliente(id_cliente):
    data = request.get_json()

    # Imprime el contenido de data para depuración
    print("Cliente data:", data)  # Esta línea imprime el contenido de data

    clientedao = ClienteDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula', 'direccion', 'telefono', 'fecha_registro']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return response_json(False, error=f'El campo {campo} es obligatorio y no puede estar vacío.', status_code=400)

    try:
        cliente_existente = clientedao.getClienteById(id_cliente)
        if not cliente_existente:
            return response_json(False, error='No se encontró el cliente con el ID proporcionado.', status_code=404)

        # Validar y convertir la fecha
        try:
            fecha_registro = datetime.strptime(data['fecha_registro'], "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return response_json(False, error='El formato de fecha_registro es inválido. Debe ser YYYY-MM-DDTHH:MM:SS.', status_code=400)

        if clientedao.updateCliente(
            id_cliente,
            data['nombre'].strip().upper(),
            data['apellido'].strip().upper(),
            data['cedula'],
            data['direccion'].strip().upper(),
            data['telefono'],
            fecha_registro
        ):
            return response_json(True, {
                'id_cliente': id_cliente,
                'nombre': data['nombre'].upper(),
                'apellido': data['apellido'].upper(),
                'cedula': data['cedula'],
                'direccion': data['direccion'].upper(),
                'telefono': data['telefono'],
                'fecha_registro': fecha_registro
            })
        else:
            return response_json(False, error='No se pudo actualizar el cliente.', status_code=404)

    except Exception as e:
        app.logger.error(f"Error al actualizar cliente: {str(e)}")
        return response_json(False, error='Ocurrió un error interno. Consulte con el administrador.', status_code=500)

@cliapi.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def deleteCliente(id_cliente):
    clientedao = ClienteDao()

    try:
        cliente_existente = clientedao.getClienteById(id_cliente)
        if not cliente_existente:
            return response_json(False, error='No se encontró el cliente con el ID proporcionado.', status_code=404)

        if clientedao.deleteCliente(id_cliente):
            return response_json(True, {
                'mensaje': f'Cliente con ID {id_cliente} eliminado correctamente.'
            })
        else:
            return response_json(False, error='No se pudo eliminar el cliente.', status_code=404)

    except Exception as e:
        app.logger.error(f"Error al eliminar cliente: {str(e)}")
        return response_json(False, error='Ocurrió un error interno. Consulte con el administrador.', status_code=500)
