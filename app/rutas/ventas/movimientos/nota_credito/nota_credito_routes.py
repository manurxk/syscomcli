from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

notacreditomod = Blueprint('nota_credito', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notacreditomod.route('/nota-credito-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def notaCreditoIndex():
    """Página principal de nota de crédito (listado y acciones)."""
    return render_template('nota-credito-index.html')


@notacreditomod.route('/nota-credito-agregar')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def notaCreditoAgregar():
    """Página del formulario para registrar nota de crédito."""
    return render_template('nota-credito-agregar.html')
