from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipo_tratamientomod = Blueprint('tipo_tratamiento', __name__, template_folder='templates')


@tipo_tratamientomod.route('/tipo-tratamiento-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoTratamientoIndex():
    return render_template('tipo_tratamiento-index.html')
