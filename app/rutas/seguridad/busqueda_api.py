from flask import Blueprint, jsonify, request, current_app as app
from app.dao.BusquedaDao import BusquedaDao

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



