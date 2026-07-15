from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

libroventasmod = Blueprint('libro_ventas', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@libroventasmod.route('/libro-ventas-index')
@role_required(*ROLES_VENTAS)
def libroVentasIndex():
    return render_template('libro-ventas-index.html')
