from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

remisionmod = Blueprint('remision', __name__, template_folder='templates')


@remisionmod.route('/remision-index')
@role_required("ADMINISTRADOR", "VENTAS")
@permiso_requerido("VENTAS", "LEER")
def remisionIndex():
    """Página principal de remisión (listado y acciones)."""
    return render_template('remision-index.html')


@remisionmod.route('/remision-agregar')
@role_required("ADMINISTRADOR", "VENTAS")
@permiso_requerido("VENTAS", "CREAR")
def remisionAgregar():
    """Página del formulario para registrar remisión."""
    return render_template('remision-agregar.html')
