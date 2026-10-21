from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

sedemod = Blueprint('sede', __name__, template_folder='templates')


@sedemod.route('/sede-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def sedeIndex():
    """Página del ABM de sede (tabla y ventana modal)."""
    return render_template('sede-index.html')
