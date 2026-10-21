from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

diagnosticomod = Blueprint('diagnostico', __name__, template_folder='templates')


@diagnosticomod.route('/diagnostico-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def diagnosticoIndex():
    """Página del ABM de diagnóstico (tabla y ventana modal)."""
    return render_template('diagnostico-index.html')
