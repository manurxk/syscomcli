from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

arqueocajamod = Blueprint('arqueo_caja', __name__, template_folder='templates')

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@arqueocajamod.route('/arqueo-index')
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "LEER")
def arqueoIndex():
    """Página principal de arqueo de caja (listado y acciones)."""
    return render_template('arqueo-index.html')


@arqueocajamod.route('/arqueo-agregar')
@role_required(*ROLES_CAJA)
@permiso_requerido("VENTAS", "CREAR")
def arqueoAgregar():
    """Página del formulario para registrar arqueo de caja."""
    return render_template('arqueo-agregar.html')
