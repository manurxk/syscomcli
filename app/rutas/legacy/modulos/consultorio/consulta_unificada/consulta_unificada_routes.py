from flask import Blueprint, render_template, abort, session
from app.auth.utils.decorators import role_required
from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes

consultaunificada = Blueprint('consultaunificada', __name__, template_folder='templates')


@consultaunificada.route('/consulta/<int:id_cita>')
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def consultaIndex(id_cita):
    """
    Ventana de Consulta Unificada — Fase 2.
    Carga todos los datos de la cita y renderiza la vista con tabs clínicos.
    El cambio de estado a EN_CONSULTA es disparado por botón explícito (no al cargar la página).
    """
    dao = CitaDao()
    cita = dao.getCitaById(id_cita)

    if not cita:
        abort(404)

    # Verificar acceso: el especialista solo puede ver sus propias citas
    if not puede_ver_todos_pacientes():
        id_especialista_logueado = obtener_id_especialista_usuario()
        if id_especialista_logueado and cita['id_especialista'] != id_especialista_logueado:
            abort(403)

    return render_template('consulta.html', cita=cita, id_cita=id_cita)
