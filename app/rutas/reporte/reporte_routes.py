from flask import Blueprint, render_template, session, request
from datetime import date
from app.auth.utils.decorators import role_required
from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.utils.auditoria_constantes import AuditAccion
from app.utils.reportes_alcance import (PESTANAS, ROLES_PANTALLA_REPORTES, alcance_de_sesion,
                                        pestanas_permitidas)

reportemod = Blueprint('reporte', __name__, template_folder='templates')


@reportemod.route('/index')
@role_required(*ROLES_PANTALLA_REPORTES)
def reporteIndex():
    """Pantalla única de Reportes (PDF 4, paso 4). Las pestañas, el filtro de especialista y el alcance
    (todos los especialistas o solo lo propio) los fija el servidor según los roles de la sesión;
    la API vuelve a aplicarlos en cada consulta."""
    roles = session.get('roles', [])
    permitidas = pestanas_permitidas(roles)
    pestana = request.args.get('tab') if request.args.get('tab') in permitidas else permitidas[0]
    alcances = {p: alcance_de_sesion(p) for p in permitidas}

    especialistas = []
    if any(a['puede_filtrar'] for a in alcances.values()):
        especialistas = FuncionarioDao().getEspecialistasActivos()

    hoy = date.today()
    AuditoriaDao().registrar_evento(
        id_usuario=session.get('id_usuario'),
        accion=AuditAccion.REPORT_VIEW,
        detalle=f'Visita a Reportes ({pestana})',
        ip_origen=request.remote_addr
    )

    return render_template('reportes-index.html',
                           pestanas=[p for p in PESTANAS if p in permitidas],
                           pestana=pestana,
                           alcances=alcances,
                           especialistas=especialistas,
                           fecha_desde=hoy.replace(day=1).strftime('%Y-%m-%d'),
                           fecha_hasta=hoy.strftime('%Y-%m-%d'))
