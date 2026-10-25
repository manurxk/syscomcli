from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

recaudacionmod = Blueprint('recaudacion', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "VENTAS")


@recaudacionmod.route('/recaudacion-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def recaudacionIndex():
    """Página principal de recaudación (listado y acciones)."""
    return render_template('recaudacion-index.html')


@recaudacionmod.route('/recaudacion-agregar')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def recaudacionAgregar():
    """Página del formulario para registrar recaudación."""
    return render_template('recaudacion-agregar.html')
