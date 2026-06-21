from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

recordatoriomod = Blueprint('recordatorio', __name__, template_folder='templates')

@recordatoriomod.route('/recordatorio-index')
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def recordatorioIndex():
    """Vista principal de gestión de recordatorios"""
    return render_template('recordatorio-index.html')

