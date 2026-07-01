from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

arqueocajamod = Blueprint('arqueo_caja', __name__, template_folder='templates')

ROLES_CAJA = ("ADMINISTRADOR", "SUPERADMIN", "VENTAS")


@arqueocajamod.route('/arqueo-index')
@role_required(*ROLES_CAJA)
def arqueoIndex():
    return render_template('arqueo-index.html')


@arqueocajamod.route('/arqueo-agregar')
@role_required(*ROLES_CAJA)
def arqueoAgregar():
    return render_template('arqueo-agregar.html')
