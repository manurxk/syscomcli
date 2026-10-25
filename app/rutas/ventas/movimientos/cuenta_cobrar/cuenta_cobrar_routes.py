from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

cuentacobrarmod = Blueprint('cuenta_cobrar', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "VENTAS")


@cuentacobrarmod.route('/cuenta-cobrar-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def cuentaCobrarIndex():
    """Página principal de cuenta a cobrar (listado y acciones)."""
    return render_template('cuenta-cobrar-index.html')
