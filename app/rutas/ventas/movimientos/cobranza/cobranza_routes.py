from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

cobranzamod = Blueprint('cobranza', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@cobranzamod.route('/cobranza-index')
@role_required(*ROLES_VENTAS)
def cobranzaIndex():
    return render_template('cobranza-index.html')


@cobranzamod.route('/cobranza-agregar')
@role_required(*ROLES_VENTAS)
def cobranzaAgregar():
    return render_template('cobranza-agregar.html')
