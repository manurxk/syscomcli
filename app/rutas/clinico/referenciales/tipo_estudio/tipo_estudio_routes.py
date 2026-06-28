from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipo_estudiomod = Blueprint('tipo_estudio', __name__, template_folder='templates')


@tipo_estudiomod.route('/tipo-estudio-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoEstudioIndex():
    return render_template('tipo_estudio-index.html')
