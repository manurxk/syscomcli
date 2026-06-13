from flask import Blueprint, request, jsonify
from flask import current_app as app
import os
import uuid
from werkzeug.utils import secure_filename
from app.dao.referenciales.ventas.empresa.EmpresaDao import EmpresaDao

empresaapi = Blueprint('empresaapi', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'svg', 'webp'}
MAX_LOGO_SIZE_MB = 5

def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ===============================
# Trae todas las empresas
# ===============================
@empresaapi.route('/empresas', methods=['GET'])
def getEmpresas():
    empresadao = EmpresaDao()
    try:
        empresas = empresadao.getEmpresas()
        return jsonify({
            'success': True,
            'data': empresas,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las empresas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae una empresa por ID
# ===============================
@empresaapi.route('/empresas/<int:empresa_id>', methods=['GET'])
def getEmpresa(empresa_id):
    empresadao = EmpresaDao()
    try:
        empresa = empresadao.getEmpresaById(empresa_id)
        if empresa:
            return jsonify({
                'success': True,
                'data': empresa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la empresa con el ID proporcionado.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae la empresa principal
# ===============================
@empresaapi.route('/empresas/principal', methods=['GET'])
def getEmpresaPrincipal():
    empresadao = EmpresaDao()
    try:
        empresa = empresadao.getEmpresaPrincipal()
        if empresa:
            return jsonify({
                'success': True,
                'data': empresa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró una empresa principal.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener empresa principal: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Trae datos de empresa para SIFEN
# ===============================
@empresaapi.route('/empresas/<int:empresa_id>/datos-sifen', methods=['GET'])
def getDatosSifen(empresa_id):
    empresadao = EmpresaDao()
    try:
        datos = empresadao.getDatosEmpresaParaSIFEN(empresa_id)
        if datos:
            return jsonify({
                'success': True,
                'data': datos,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontraron datos SIFEN para la empresa.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al obtener datos SIFEN: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Agrega una nueva empresa
# ===============================
@empresaapi.route('/empresas', methods=['POST'])
def addEmpresa():
    data = request.get_json()
    empresadao = EmpresaDao()

    campos_requeridos = ['ruc_nit', 'razon_social', 'departamento', 'distrito', 'ciudad', 'direccion', 'telefono', 'celular', 'email']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        if not empresadao.validarRUC(data['ruc_nit']):
            return jsonify({
                'success': False,
                'error': 'El RUC tiene un formato inválido.'
            }), 400

        if not empresadao.validarEmail(data['email']):
            return jsonify({
                'success': False,
                'error': 'El email tiene un formato inválido.'
            }), 400

        empresa_id = empresadao.guardarEmpresa(data)
        if empresa_id:
            empresa = empresadao.getEmpresaById(empresa_id)
            return jsonify({
                'success': True,
                'data': empresa,
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la empresa (RUC duplicado o datos inválidos).'
            }), 400
    except Exception as e:
        app.logger.error(f"Error al agregar empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza una empresa
# ===============================
@empresaapi.route('/empresas/<int:empresa_id>', methods=['PUT'])
def updateEmpresa(empresa_id):
    data = request.get_json()
    empresadao = EmpresaDao()

    campos_requeridos = ['razon_social', 'departamento', 'distrito', 'ciudad', 'direccion', 'telefono', 'celular', 'email']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400

    try:
        if not empresadao.validarEmail(data['email']):
            return jsonify({
                'success': False,
                'error': 'El email tiene un formato inválido.'
            }), 400

        if empresadao.updateEmpresa(empresa_id, data):
            empresa = empresadao.getEmpresaById(empresa_id)
            return jsonify({
                'success': True,
                'data': empresa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la empresa con el ID proporcionado o no se pudo actualizar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al actualizar empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Elimina una empresa
# ===============================
@empresaapi.route('/empresas/<int:empresa_id>', methods=['DELETE'])
def deleteEmpresa(empresa_id):
    empresadao = EmpresaDao()

    try:
        resultado = empresadao.deleteEmpresa(empresa_id)
        if resultado is True:
            return jsonify({
                'success': True,
                'mensaje': f'Empresa con ID {empresa_id} eliminada correctamente.',
                'error': None
            }), 200
        elif resultado == "en_uso":
            return jsonify({
                'success': False,
                'error': 'No se puede eliminar esta empresa porque tiene sedes asociadas.'
            }), 400
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la empresa.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar empresa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Subir / Actualizar Logo
# ===============================
@empresaapi.route('/empresas/<int:empresa_id>/logo', methods=['POST'])
def uploadLogo(empresa_id):
    """Recibe un archivo de imagen y lo guarda como logo de la empresa"""
    if 'logo' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió ningún archivo.'}), 400

    file = request.files['logo']

    if file.filename == '':
        return jsonify({'success': False, 'error': 'Nombre de archivo vacío.'}), 400

    if not _allowed_file(file.filename):
        return jsonify({'success': False, 'error': f'Formato no permitido. Use: {", ".join(ALLOWED_EXTENSIONS)}'}), 400

    # Verificar tamaño (máx 5 MB)
    file.seek(0, 2)  # Mover al final
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)  # Resetear
    if size_mb > MAX_LOGO_SIZE_MB:
        return jsonify({'success': False, 'error': f'El archivo supera el límite de {MAX_LOGO_SIZE_MB} MB.'}), 400

    try:
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"logo_{empresa_id}_{uuid.uuid4().hex[:8]}.{ext}"
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'logos')
        os.makedirs(upload_folder, exist_ok=True)
        filepath = os.path.join(upload_folder, filename)

        # Eliminar logo anterior si existe
        empresadao = EmpresaDao()
        empresa = empresadao.getEmpresaById(empresa_id)
        if empresa and empresa.get('logo_path'):
            old_path = os.path.join(app.root_path, 'static', empresa['logo_path'].lstrip('/'))
            if os.path.exists(old_path):
                os.remove(old_path)

        file.save(filepath)
        # Guardar ruta relativa para que sea accesible desde el navegador
        logo_url = f"uploads/logos/{filename}"

        if empresadao.updateLogo(empresa_id, logo_url):
            return jsonify({
                'success': True,
                'data': {'logo_url': f"/static/{logo_url}"},
                'error': None
            }), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el logo en la base de datos.'}), 500

    except Exception as e:
        app.logger.error(f"Error al subir logo: {str(e)}")
        return jsonify({'success': False, 'error': f'Error interno: {str(e)}'}), 500
