from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

insumomod = Blueprint('insumo', __name__, template_folder='templates')


@insumomod.route('/insumo-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def insumoIndex():
    return render_template('insumo-index.html')
