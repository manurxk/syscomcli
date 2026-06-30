from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

presupuestomod = Blueprint('presupuesto', __name__, template_folder='templates')


@presupuestomod.route('/presupuesto-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def presupuestoIndex():
    return render_template('presupuesto-index.html')


@presupuestomod.route('/presupuesto-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def presupuestoAgregar():
    return render_template('presupuesto-agregar.html')
