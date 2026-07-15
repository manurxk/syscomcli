from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

cuentacobrarmod = Blueprint('cuenta_cobrar', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@cuentacobrarmod.route('/cuenta-cobrar-index')
@role_required(*ROLES_VENTAS)
def cuentaCobrarIndex():
    return render_template('cuenta-cobrar-index.html')
