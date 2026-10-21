from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

puntoexpedicionmod = Blueprint('punto_expedicion', __name__, template_folder='templates')


@puntoexpedicionmod.route('/punto-expedicion-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def puntoExpedicionIndex():
    """Página principal de punto de expedición (listado y acciones)."""
    return render_template('punto-expedicion-index.html')
