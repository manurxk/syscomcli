from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

libroventasmod = Blueprint('libro_ventas', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "VENTAS")


@libroventasmod.route('/libro-ventas-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def libroVentasIndex():
    """Página principal de libro de ventas (listado y acciones)."""
    return render_template('libro-ventas-index.html')
