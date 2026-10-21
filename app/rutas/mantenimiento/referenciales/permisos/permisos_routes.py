from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

permisosmod = Blueprint('permisos', __name__, template_folder='templates')


@permisosmod.route('/permisos-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def permisosIndex():
    """Página de la matriz de permisos por rol."""
    return render_template('permisos-index.html')
