from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

auditoriamod = Blueprint('auditoria', __name__, template_folder='templates')


@auditoriamod.route('/auditoria-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def auditoriaIndex():
    return render_template('auditoria-index.html')
