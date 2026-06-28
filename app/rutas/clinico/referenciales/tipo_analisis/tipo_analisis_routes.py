from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipo_analisismod = Blueprint('tipo_analisis', __name__, template_folder='templates')


@tipo_analisismod.route('/tipo-analisis-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoAnalisisIndex():
    return render_template('tipo_analisis-index.html')
