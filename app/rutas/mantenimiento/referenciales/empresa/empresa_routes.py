from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

empresamod = Blueprint('empresa', __name__, template_folder='templates')


@empresamod.route('/empresa-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def empresaIndex():
    """Página de datos de la empresa."""
    return render_template('empresa-index.html')
