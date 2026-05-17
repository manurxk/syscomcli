from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.libro_ventas.LibroVentasDao import LibroVentasDao

libro_ventas_api = Blueprint('libro_ventas_api', __name__)

@libro_ventas_api.route('/libro_ventas', methods=['GET'])
def getAllLibroVentas():
    """Obtiene todas las entradas del libro de ventas"""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    dao = LibroVentasDao()
    
    try:
        entradas = dao.getLibroVentas(fecha_desde, fecha_hasta)
        return jsonify({'success': True, 'data': entradas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener libro de ventas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@libro_ventas_api.route('/libro_ventas/<int:id_libro_venta>', methods=['GET'])
def getLibroVenta(id_libro_venta):
    """Obtiene una entrada específica del libro de ventas por su ID"""
    dao = LibroVentasDao()
    
    try:
        entrada = dao.getLibroVentasById(id_libro_venta)
        
        if entrada:
            return jsonify({'success': True, 'data': entrada, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la entrada del libro de ventas.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener entrada del libro de ventas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@libro_ventas_api.route('/libro_ventas/resumen', methods=['GET'])
def getResumenLibroVentas():
    """Obtiene un resumen del libro de ventas por tipo de comprobante"""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    dao = LibroVentasDao()
    
    try:
        resumen = dao.getResumenLibroVentas(fecha_desde, fecha_hasta)
        return jsonify({'success': True, 'data': resumen, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener resumen del libro de ventas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@libro_ventas_api.route('/libro_ventas/totales', methods=['GET'])
def getTotalesLibroVentas():
    """Obtiene los totales generales del libro de ventas"""
    fecha_desde = request.args.get('fecha_desde')
    fecha_hasta = request.args.get('fecha_hasta')
    
    dao = LibroVentasDao()
    
    try:
        totales = dao.getTotalesLibroVentas(fecha_desde, fecha_hasta)
        
        if totales:
            return jsonify({'success': True, 'data': totales, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se pudieron calcular los totales.'}), 500
    except Exception as e:
        app.logger.error(f"Error al obtener totales del libro de ventas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


















