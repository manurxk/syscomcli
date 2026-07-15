from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

notadebitomod = Blueprint('nota_debito', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@notadebitomod.route('/nota-debito-index')
@role_required(*ROLES_VENTAS)
def notaDebitoIndex():
    return render_template('nota-debito-index.html')


@notadebitomod.route('/nota-debito-agregar')
@role_required(*ROLES_VENTAS)
def notaDebitoAgregar():
    return render_template('nota-debito-agregar.html')
