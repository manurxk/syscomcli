from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

notacreditomod = Blueprint('nota_credito', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notacreditomod.route('/nota-credito-index')
@role_required(*ROLES_VENTAS)
def notaCreditoIndex():
    return render_template('nota-credito-index.html')


@notacreditomod.route('/nota-credito-agregar')
@role_required(*ROLES_VENTAS)
def notaCreditoAgregar():
    return render_template('nota-credito-agregar.html')
