from flask import Blueprint, request, jsonify, current_app as app, make_response
import io
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from app.dao.gestionar_personas.persona.PersonaDao import PersonaDao

personaapi = Blueprint('personaapi', __name__)

# --- Funciones para exportar ---

def export_pdf(data, columns, filename='personas.pdf'):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
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

def export_excel(data, columns, filename='personas.xlsx'):
    df = pd.DataFrame(data, columns=columns)
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Personas')
    excel_data = buffer.getvalue()
    buffer.close()

    response = make_response(excel_data)
    response.headers['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response.headers['Content-Disposition'] = f'attachment; filename={filename}'
    return response

# --- Rutas existentes ---

@personaapi.route('/personas', methods=['GET'])
def getPersonas():
    personadao = PersonaDao()
    try:
        personas = personadao.getPersonas()
        return jsonify({
            'success': True,
            'data': personas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las personas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@personaapi.route('/personas/<int:persona_id>', methods=['GET'])
def getPersona(persona_id):
    personadao = PersonaDao()
    try:
        persona = personadao.getPersonasById(persona_id)
        if persona:
            return jsonify({
                'success': True,
                'data': persona,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@personaapi.route('/personas', methods=['POST'])
def addPersona():
    data = request.get_json()
    personadao = PersonaDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula','fecha_nacimiento','id_genero', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad']

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        fecha_nacimiento = data['fecha_nacimiento']
        id_genero = data['id_genero']
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']

        persona_id = personadao.guardarPersona(nombre, apellido, cedula, fecha_nacimiento, id_genero, id_estado_civil, telefono_emergencia, id_ciudad)
        if persona_id is not None:
            return jsonify({
                'success': True,
                'data': {'id': persona_id, 'nombre': nombre, 'apellido': apellido, 'cedula': cedula, 'fecha_nacimiento': fecha_nacimiento, 'id_genero': id_genero, 'id_estado_civil': id_estado_civil, 'telefono_emergencia': telefono_emergencia, 'id_ciudad':id_ciudad},
                'error': None
            }), 201
        else:
            return jsonify({'success': False, 'error': 'No se pudo guardar la persona. Consulte con el administrador.'}), 500
    except Exception as e:
        app.logger.error(f"Error al agregar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@personaapi.route('/personas/<int:persona_id>', methods=['PUT'])
def updatePersona(persona_id):
    data = request.get_json()
    personadao = PersonaDao()

    campos_requeridos = ['nombre', 'apellido', 'cedula', 'fecha_nacimiento', 'id_genero', 'id_estado_civil', 'telefono_emergencia', 'id_ciudad' ]

    for campo in campos_requeridos:
        if campo not in data or data[campo] is None or len(data[campo].strip()) == 0:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        nombre = data['nombre'].upper()
        apellido = data['apellido'].upper()
        cedula = data['cedula'].strip()
        fecha_nacimiento = data['fecha_nacimiento']
        id_genero = data['id_genero']
        id_estado_civil = data['id_estado_civil']
        telefono_emergencia = data['telefono_emergencia'].strip()
        id_ciudad = data['id_ciudad']

        if personadao.updatePersona(persona_id, nombre, apellido, cedula, fecha_nacimiento, id_genero, id_estado_civil, telefono_emergencia, id_ciudad):
            return jsonify({
                'success': True,
                'data': {'id': persona_id, 'nombre': nombre, 'apellido': apellido, 'cedula': cedula, 'fecha_nacimiento': fecha_nacimiento, 'id_genero': id_genero, 'id_estado_civil': id_estado_civil, 'telefono_emergencia': telefono_emergencia, 'id_ciudad':id_ciudad},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

@personaapi.route('/personas/<int:persona_id>', methods=['DELETE'])
def deletePersona(persona_id):
    personadao = PersonaDao()
    try:
        if personadao.deletePersona(persona_id):
            return jsonify({
                'success': True,
                'mensaje': f'Persona con ID {persona_id} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la persona con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar persona: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# --- NUEVAS RUTAS PARA EXPORTACIÓN ---

@personaapi.route('/personas/export/pdf', methods=['GET'])
def export_personas_pdf():
    personadao = PersonaDao()
    try:
        personas = personadao.getPersonas()
        if len(personas) == 0:
            return jsonify({'success': False, 'error': 'No hay datos para exportar'}), 404

        columns = ['ID', 'Nombre', 'Apellido', 'Cédula', 'Fecha de Nacimiento', 'Género', 'Estado Civil', 'Teléfono Emergencia', 'Ciudad']
        rows = []
        for p in personas:
            rows.append([
                p.get('id'),
                p.get('nombre'),
                p.get('apellido'),
                p.get('cedula'),
                p.get('fecha_nacimiento'),
                p.get('genero'),
                p.get('estado_civil'),
                p.get('telefono_emergencia'),
                p.get('ciudad')
            ])

        return export_pdf(rows, columns)
    except Exception as e:
        app.logger.error(f"Error al exportar personas a PDF: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno al exportar PDF'}), 500

@personaapi.route('/personas/export/excel', methods=['GET'])
def export_personas_excel():
    personadao = PersonaDao()
    try:
        personas = personadao.getPersonas()
        if len(personas) == 0:
            return jsonify({'success': False, 'error': 'No hay datos para exportar'}), 404

        columns = ['ID', 'Nombre', 'Apellido', 'Cédula', 'Fecha de Nacimiento', 'Género', 'Estado Civil', 'Teléfono Emergencia', 'Ciudad']
        rows = []
        for p in personas:
            rows.append([
                p.get('id'),
                p.get('nombre'),
                p.get('apellido'),
                p.get('cedula'),
                p.get('fecha_nacimiento'),
                p.get('genero'),
                p.get('estado_civil'),
                p.get('telefono_emergencia'),
                p.get('ciudad')
            ])

        return export_excel(rows, columns)
    except Exception as e:
        app.logger.error(f"Error al exportar personas a Excel: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno al exportar Excel'}), 500
