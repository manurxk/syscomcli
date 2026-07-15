from flask import Blueprint, request, jsonify, current_app as app

from app.dao.ventas.movimientos.libro_ventas.LibroVentasDao import LibroVentasDao
from app.auth.utils.decorators import role_required

libroventasapi = Blueprint('libroventasapi', __name__)

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@libroventasapi.route('/libro-ventas', methods=['GET'])
@role_required(*ROLES_VENTAS)
def getLibroVentas():
    fecha_desde = request.args.get('fecha_desde') or None
    fecha_hasta = request.args.get('fecha_hasta') or None
    try:
        dao     = LibroVentasDao()
        datos   = dao.getLibroVentas(fecha_desde, fecha_hasta)
        resumen = dao.getResumenLibroVentas(fecha_desde, fecha_hasta)
        totales = dao.getTotalesLibroVentas(fecha_desde, fecha_hasta)
        return jsonify({
            'success': True,
            'data':    datos,
            'resumen': resumen,
            'totales': totales,
            'error':   None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener libro de ventas: {e}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
