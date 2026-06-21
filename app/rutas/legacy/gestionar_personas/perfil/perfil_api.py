from flask import Blueprint, request, jsonify, session, current_app as app
import os
from werkzeug.utils import secure_filename
from app.dao.gestionar_personas.perfil.PerfilDao import PerfilDao

perfilapi = Blueprint('perfilapi', __name__)

# ===============================
# Obtiene el perfil del usuario logueado
# ===============================
@perfilapi.route('/perfil', methods=['GET'])
def getPerfil():
    # Verificar que el usuario esté logueado
    # CORREGIDO: Usar 'id_usuario' en lugar de 'id'
    if 'id_usuario' not in session:
        return jsonify({
            'success': False,
            'error': 'Usuario no autenticado'
        }), 401

    perfildao = PerfilDao()
    id_usuario = session.get('id_usuario')

    try:
        perfil = perfildao.getPerfilCompleto(id_usuario)

        if perfil:
            return jsonify({
                'success': True,
                'data': perfil,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el perfil del usuario.'
            }), 404

    except Exception as e:
        app.logger.error(f"Error al obtener perfil: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Obtiene estadísticas del usuario
# ===============================
@perfilapi.route('/perfil/estadisticas', methods=['GET'])
def getEstadisticas():
    if 'id_usuario' not in session:
        return jsonify({
            'success': False,
            'error': 'Usuario no autenticado'
        }), 401

    perfildao = PerfilDao()
    id_usuario = session.get('id_usuario')
    id_grupo = session.get('id_grupo')

    try:
        estadisticas = perfildao.getEstadisticasUsuario(id_usuario, id_grupo)

        return jsonify({
            'success': True,
            'data': estadisticas,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Obtiene actividad reciente del usuario
# ===============================
@perfilapi.route('/perfil/actividad-reciente', methods=['GET'])
def getActividadReciente():
    if 'id_usuario' not in session:
        return jsonify({
            'success': False,
            'error': 'Usuario no autenticado'
        }), 401

    id_usuario = session.get('id_usuario')
    limite = request.args.get('limite', 10, type=int)

    try:
        from app.dao.AuditoriaDao import AuditoriaDao
        actividad = AuditoriaDao().obtener_actividad_reciente(id_usuario=id_usuario, limite=limite)

        return jsonify({
            'success': True,
            'data': actividad,
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al obtener actividad reciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500

# ===============================
# Actualiza los datos personales del usuario
# ===============================
@perfilapi.route('/perfil/update', methods=['POST'])
def updatePerfil():
    if 'id_usuario' not in session:
        return jsonify({'success': False, 'error': 'Usuario no autenticado'}), 401

    data = request.json
    id_usuario = session.get('id_usuario')
    perfildao = PerfilDao()

    try:
        success = perfildao.updatePerfil(id_usuario, data)
        if success:
            from app.dao.AuditoriaDao import AuditoriaDao
            from app.utils.auditoria_constantes import AuditAccion
            
            campos_mod = [k for k in data.keys() if 'password' not in k.lower() and 'clave' not in k.lower()]
            detalle_update = f"Perfil actualizado. Campos: {', '.join(campos_mod)}"
            
            AuditoriaDao().registrar_evento(
                id_usuario=id_usuario,
                accion=AuditAccion.PROFILE_UPDATE,
                detalle=detalle_update,
                ip_origen=request.remote_addr
            )
            
            return jsonify({'success': True}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudo actualizar el perfil'}), 400
    except Exception as e:
        app.logger.error(f"Error al actualizar perfil: {str(e)}")
        return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

# ===============================
# Actualiza la foto de perfil
# ===============================
@perfilapi.route('/perfil/update-photo', methods=['POST'])
def updateFotoPerfil():
    if 'id_usuario' not in session:
        return jsonify({'success': False, 'error': 'Usuario no autenticado'}), 401
        
    if 'foto' not in request.files:
        return jsonify({'success': False, 'error': 'No se envió ninguna foto'}), 400
        
    foto = request.files['foto']
    if foto.filename == '':
        return jsonify({'success': False, 'error': 'Nombre de archivo vacío'}), 400

    if foto:
        filename = secure_filename(foto.filename)
        # Asegurar un nombre único
        id_usuario = session.get('id_usuario')
        extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else 'jpg'
        nuevo_nombre = f"perfil_{id_usuario}.{extension}"
        
        # Guardar archivo
        upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'perfiles')
        os.makedirs(upload_folder, exist_ok=True)
        ruta_guardado = os.path.join(upload_folder, nuevo_nombre)
        
        try:
            foto.save(ruta_guardado)
            
            # Actualizar en BD
            perfildao = PerfilDao()
            ruta_bd = f"uploads/perfiles/{nuevo_nombre}"
            success = perfildao.updateFoto(id_usuario, ruta_bd)
            
            if success:
                # Actualizar info en session
                session['foto'] = ruta_bd
                return jsonify({
                    'success': True, 
                    'ruta_foto': f"/static/{ruta_bd}"
                }), 200
            else:
                return jsonify({'success': False, 'error': 'Error al actualizar base de datos'}), 500
        except Exception as e:
            app.logger.error(f"Error al subir foto: {str(e)}")
            return jsonify({'success': False, 'error': 'Error al guardar la imagen'}), 500