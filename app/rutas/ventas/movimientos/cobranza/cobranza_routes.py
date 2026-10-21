from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

cobranzamod = Blueprint('cobranza', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@cobranzamod.route('/cobranza-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def cobranzaIndex():
    """Página principal de cobranza (listado y acciones)."""
    return render_template('cobranza-index.html')


@cobranzamod.route('/cobranza-agregar')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def cobranzaAgregar():
    """Página del formulario para registrar cobranza."""
    return render_template('cobranza-agregar.html')
