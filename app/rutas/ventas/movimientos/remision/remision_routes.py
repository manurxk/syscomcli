from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

remisionmod = Blueprint('remision', __name__, template_folder='templates')


@remisionmod.route('/remision-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def remisionIndex():
    return render_template('remision-index.html')


@remisionmod.route('/remision-agregar')
@role_required("ADMINISTRADOR", "SUPERADMIN", "VENTAS")
def remisionAgregar():
    return render_template('remision-agregar.html')
