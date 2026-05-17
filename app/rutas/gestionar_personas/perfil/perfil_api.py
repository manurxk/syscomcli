from flask import Blueprint, request, jsonify, session, current_app as app
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

    perfildao = PerfilDao()
    id_usuario = session.get('id_usuario')
    limite = request.args.get('limite', 5, type=int)

    try:
        actividad = perfildao.getActividadReciente(id_usuario, limite)

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