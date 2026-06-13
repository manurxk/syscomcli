from flask import Blueprint, jsonify, request, current_app as app
from app.dao.BusquedaDao import BusquedaDao
from app.utils.especialista_helper import obtener_id_especialista_usuario
from app.conexion.Conexion import Conexion

# Crear blueprint para búsqueda
busquedaapi = Blueprint('busquedaapi', __name__)

# ==========================================
# BÚSQUEDA GLOBAL
# ==========================================

@busquedaapi.route('/busqueda', methods=['GET'])
def buscarGlobal():
    """
    Endpoint de búsqueda global que busca en pacientes, especialistas y referenciales.
    
    Query params:
        - q: Término de búsqueda (requerido)
        - limite: Número máximo de resultados por categoría (opcional, default: 20)
    """
    try:
        termino = request.args.get('q', '').strip()
        limite = request.args.get('limite', 20, type=int)
        
        if not termino or len(termino) < 2:
            return jsonify({
                'success': True,
                'data': {
                    'pacientes': [],
                    'especialistas': [],
                    'referenciales': []
                },
                'error': None
            }), 200
        
        busquedadao = BusquedaDao()
        resultados = busquedadao.buscarGlobal(termino, limite)
        
        return jsonify({
            'success': True,
            'data': resultados,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error en búsqueda global: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'data': None,
            'error': 'Ocurrió un error al realizar la búsqueda'
        }), 500

@busquedaapi.route('/especialista-actual', methods=['GET'])
def getEspecialistaActual():
    """Obtiene datos del especialista logueado para auto-completar formularios"""
    try:
        id_especialista = obtener_id_especialista_usuario()
        if not id_especialista:
            return jsonify({'success': False, 'error': 'No es especialista'}), 404
        
        # Obtener nombre completo
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        cur.execute("""
            SELECT CONCAT(p.per_nombre, ' ', p.per_apellido) 
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            WHERE e.id_especialista = %s
        """, (id_especialista,))
        nombre = cur.fetchone()
        cur.close()
        con.close()

        return jsonify({
            'success': True,
            'data': {
                'id_especialista': id_especialista,
                'nombre_completo': nombre[0] if nombre else 'Especialista'
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500



