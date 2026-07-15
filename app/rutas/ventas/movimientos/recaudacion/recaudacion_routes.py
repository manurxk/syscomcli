from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

recaudacionmod = Blueprint('recaudacion', __name__, template_folder='templates')

ROLES_VENTAS = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@recaudacionmod.route('/recaudacion-index')
@role_required(*ROLES_VENTAS)
def recaudacionIndex():
    return render_template('recaudacion-index.html')


@recaudacionmod.route('/recaudacion-agregar')
@role_required(*ROLES_VENTAS)
def recaudacionAgregar():
    return render_template('recaudacion-agregar.html')
