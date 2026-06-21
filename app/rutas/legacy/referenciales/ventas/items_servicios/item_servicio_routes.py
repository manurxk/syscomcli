from flask import Blueprint, render_template

item_servicio = Blueprint('item_servicio', __name__, template_folder='templates')


@item_servicio.route('/item-servicio-index')
def itemServicioIndex():
    """Pantalla principal del catálogo de Items/Servicios de ventas."""
    return render_template('item-servicio-index.html')




