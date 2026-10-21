from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required, permiso_requerido

notadebitomod = Blueprint('nota_debito', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notadebitomod.route('/nota-debito-index')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "LEER")
def notaDebitoIndex():
    """Página principal de nota de débito (listado y acciones)."""
    return render_template('nota-debito-index.html')


@notadebitomod.route('/nota-debito-agregar')
@role_required(*ROLES_VENTAS)
@permiso_requerido("VENTAS", "CREAR")
def notaDebitoAgregar():
    """Página del formulario para registrar nota de débito."""
    return render_template('nota-debito-agregar.html')
