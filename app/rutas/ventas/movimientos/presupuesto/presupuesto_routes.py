from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

presupuestomod = Blueprint('presupuesto', __name__, template_folder='templates')


@presupuestomod.route('/presupuesto-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
@permiso_requerido("VENTAS", "LEER")
def presupuestoIndex():
    """Página principal de presupuesto (listado y acciones)."""
    return render_template('presupuesto-index.html')


@presupuestomod.route('/presupuesto-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
@permiso_requerido("VENTAS", "CREAR")
def presupuestoAgregar():
    """Página del formulario para registrar presupuesto."""
    return render_template('presupuesto-agregar.html')
