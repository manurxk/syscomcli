from flask import Blueprint, request, jsonify, current_app as app, make_response
import io
import pandas as pd
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors

from app.dao.seguridad.usuario.UsuarioDao import UsuarioDao  # ajusta la ruta según tu estructura

usuarioapi = Blueprint('usuarioapi', __name__)

# --- Funciones para exportar ---

def export_pdf(data, columns, filename='usuarios.pdf'):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))
    table_data = [columns] + data

    table = Table(table_data)
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.gray),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
    ])
    table.setStyle(style)

    elements = [table]
    doc.build(elements)
    pdf = buffer.getvalue()
    buffer.close()

    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

def export_excel(data, columns, filename='usuarios.xlsx'):
    df = pd.DataFrame(data, columns=columns)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Usuarios')
    excel_data = buffer.getvalue()
    buffer.close()

    response = make_response(excel_data)
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

# --- Rutas ---

@usuarioapi.route('/usuarios', methods=['GET'])
def getUsuarios():
    usuariodao = UsuarioDao()
    try:
        usuarios = usuariodao.getUsuarios()
        return jsonify({
            'success': True,
            'data': usuarios,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los usuarios: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@usuarioapi.route('/usuarios/<int:usu_id>', methods=['GET'])
def getUsuario(usu_id):
    usuariodao = UsuarioDao()
    try:
        usuario = usuariodao.getUsuarioById(usu_id)
        if usuario:
            return jsonify({
                'success': True,
                'data': usuario,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@usuarioapi.route('/usuarios', methods=['POST'])
def addUsuario():
    data = request.get_json()
    usuariodao = UsuarioDao()

    campos_requeridos = ['usu_nick', 'usu_clave', 'usu_nro_intentos', 'fun_id', 'gru_id', 'usu_estado']
    valores_estado_permitidos = ['activo', 'inactivo']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or (isinstance(data[campo], str) and len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar valor de usu_estado
    usu_estado = data['usu_estado'].strip().lower()
    if usu_estado not in valores_estado_permitidos:
        return jsonify({
            'success': False,
            'error': f'El campo usu_estado debe ser uno de {valores_estado_permitidos}.'
        }), 400

    try:
        usu_nick = data['usu_nick'].strip()
        usu_clave = data['usu_clave'].strip()
        usu_nro_intentos = int(data['usu_nro_intentos'])
        fun_id = int(data['fun_id'])
        gru_id = int(data['gru_id'])

        usuario_id = usuariodao.guardarUsuario(usu_nick, usu_clave, usu_nro_intentos, fun_id, gru_id, usu_estado)
        if usuario_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'usu_id': usuario_id,
                    'usu_nick': usu_nick,
                    'usu_nro_intentos': usu_nro_intentos,
                    'fun_id': fun_id,
                    'gru_id': gru_id,
                    'usu_estado': usu_estado
                },
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar el usuario. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@usuarioapi.route('/usuarios/<int:usu_id>', methods=['PUT'])
def updateUsuario(usu_id):
    data = request.get_json()
    usuariodao = UsuarioDao()

    campos_requeridos = ['usu_nick', 'usu_clave', 'usu_nro_intentos', 'fun_id', 'gru_id', 'usu_estado']
    valores_estado_permitidos = ['activo', 'inactivo']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or (isinstance(data[campo], str) and len(data[campo].strip()) == 0):
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    # Validar valor de usu_estado
    usu_estado = data['usu_estado'].strip().lower()
    if usu_estado not in valores_estado_permitidos:
        return jsonify({
            'success': False,
            'error': f'El campo usu_estado debe ser uno de {valores_estado_permitidos}.'
        }), 400

    try:
        usu_nick = data['usu_nick'].strip()
        usu_clave = data['usu_clave'].strip()
        usu_nro_intentos = int(data['usu_nro_intentos'])
        fun_id = int(data['fun_id'])
        gru_id = int(data['gru_id'])

        if usuariodao.updateUsuario(usu_id, usu_nick, usu_clave, usu_nro_intentos, fun_id, gru_id, usu_estado):
            return jsonify({
                'success': True,
                'data': {
                    'usu_id': usu_id,
                    'usu_nick': usu_nick,
                    'usu_nro_intentos': usu_nro_intentos,
                    'fun_id': fun_id,
                    'gru_id': gru_id,
                    'usu_estado': usu_estado
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@usuarioapi.route('/usuarios/<int:usu_id>', methods=['DELETE'])
def deleteUsuario(usu_id):
    usuariodao = UsuarioDao()
    try:
        if usuariodao.deleteUsuario(usu_id):
            return jsonify({
                'success': True,
                'mensaje': f'Usuario con ID {usu_id} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el usuario con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar usuario: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# --- Rutas para exportar PDF y Excel (opcional) ---

@usuarioapi.route('/usuarios/export/pdf', methods=['GET'])
def export_usuarios_pdf():
    usuariodao = UsuarioDao()
    try:
        usuarios = usuariodao.getUsuarios()
        if len(usuarios) == 0:
            return jsonify({'success': False, 'error': 'No hay datos para exportar'}), 404

        columns = ['ID', 'Nick', 'Número Intentos', 'ID Funcionario', 'ID Grupo', 'Estado']
        rows = []
        for u in usuarios:
            rows.append([
                u.get('usu_id'),
                u.get('usu_nick'),
                u.get('usu_nro_intentos'),
                u.get('fun_id'),
                u.get('gru_id'),
                u.get('usu_estado'),
            ])

        return export_pdf(rows, columns)
    except Exception as e:
        app.logger.error(f"Error al exportar usuarios a PDF: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno al exportar PDF'}), 500

@usuarioapi.route('/usuarios/export/excel', methods=['GET'])
def export_usuarios_excel():
    usuariodao = UsuarioDao()
    try:
        usuarios = usuariodao.getUsuarios()
        if len(usuarios) == 0:
            return jsonify({'success': False, 'error': 'No hay datos para exportar'}), 404

        columns = ['ID', 'Nick', 'Número Intentos', 'ID Funcionario', 'ID Grupo', 'Estado']
        rows = []
        for u in usuarios:
            rows.append([
                u.get('usu_id'),
                u.get('usu_nick'),
                u.get('usu_nro_intentos'),
                u.get('fun_id'),
                u.get('gru_id'),
                u.get('usu_estado'),
            ])

        return export_excel(rows, columns)
    except Exception as e:
        app.logger.error(f"Error al exportar usuarios a Excel: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno al exportar Excel'}), 500
