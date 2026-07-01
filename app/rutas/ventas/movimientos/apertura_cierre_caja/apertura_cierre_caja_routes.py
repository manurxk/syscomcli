from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

aperturacierrecajamod = Blueprint('apertura_cierre_caja', __name__, template_folder='templates')

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@aperturacierrecajamod.route('/caja-estado')
@role_required(*ROLES_CAJA)
def cajaEstado():
    return render_template('caja-estado.html')


@aperturacierrecajamod.route('/caja-historial')
@role_required(*ROLES_CAJA)
def cajaHistorial():
    return render_template('caja-historial.html')
