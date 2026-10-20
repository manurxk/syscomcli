from flask import Blueprint, render_template, request, session
from app.auth.utils.decorators import role_required
from app.utils.auditoria_constantes import (alcance_cambios, ROLES_AUDITORIA_COMPLETA,
                                            ROLES_PANTALLA_AUDITORIA)

auditoriamod = Blueprint('auditoria', __name__, template_folder='templates')

PESTANAS = ('cambios', 'eventos', 'accesos', 'sesiones')


@auditoriamod.route('/auditoria-index')
@role_required(*ROLES_PANTALLA_AUDITORIA)
def auditoriaIndex():
    """Pantalla única de Auditoría (PDF 9 + 6, paso 5). Las pestañas y los módulos que se muestran
    dependen de los roles de la sesión; la API vuelve a filtrar en el servidor."""
    roles = {(r or '').strip().upper() for r in session.get('roles', [])}
    alcance = alcance_cambios(roles)
    completa = bool(roles & set(ROLES_AUDITORIA_COMPLETA))
    pestana = request.args.get('tab') if request.args.get('tab') in PESTANAS else 'cambios'
    if not completa:
        pestana = 'cambios'
    return render_template(
        'auditoria-index.html',
        alcance=alcance,
        con_detalle=any(n in ('detalle', 'propios') for n in alcance.values()),
        completa=completa,
        pestana=pestana,
        id_usuario_filtro=request.args.get('usuario', '', type=str) if completa else '',
    )
