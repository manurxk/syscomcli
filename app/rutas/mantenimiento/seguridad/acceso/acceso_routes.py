from flask import Blueprint, redirect, url_for
from app.auth.utils.decorators import role_required

accesomod = Blueprint('acceso', __name__, template_folder='templates')


@accesomod.route('/acceso-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def accesoIndex():
    """Accesos pasó a ser la pestaña "Sesiones y usuarios" de Auditoría (PDF 9 + 6, paso 5).
    La ruta se conserva para los enlaces viejos."""
    return redirect(url_for('auditoria.auditoriaIndex', tab='sesiones'))
