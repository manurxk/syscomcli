from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

formacobromod = Blueprint('forma_cobro', __name__, template_folder='templates')


@formacobromod.route('/forma-cobro-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def formaCobroIndex():
    """Página principal de forma de cobro (listado y acciones)."""
    return render_template('forma-cobro-index.html')
