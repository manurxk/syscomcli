from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

aperturacierrecajamod = Blueprint('apertura_cierre_caja', __name__, template_folder='templates')

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@aperturacierrecajamod.route('/caja-estado')
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def cajaEstado():
    """Página con el estado de las cajas y los botones de abrir/cerrar."""
    return render_template('caja-estado.html')


@aperturacierrecajamod.route('/caja-historial')
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def cajaHistorial():
    """Página con el historial de aperturas y cierres de caja."""
    return render_template('caja-historial.html')
