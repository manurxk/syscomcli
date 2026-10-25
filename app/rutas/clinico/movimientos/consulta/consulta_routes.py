from flask import Blueprint, render_template, abort, session
from app.auth.utils.decorators import role_required
from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.clinico.movimientos.tratamiento.TratamientoDao import TratamientoDao

consultamod = Blueprint('consulta', __name__, template_folder='templates')

ROLES_CONSULTA = ("ADMINISTRADOR", "CLINICO")


@consultamod.route('/consulta-index')
@role_required(*ROLES_CONSULTA)
def consultaIndex():
    """Página principal de Consulta (workspace de la consulta clínica)."""
    return render_template('consulta-index.html')


@consultamod.route('/consulta-editar/<int:id_consulta>')
@role_required(*ROLES_CONSULTA)
def consultaAgregar(id_consulta):
    """Página de atención de una consulta (anamnesis + registro clínico). Solo se llega acá
    después de 'Iniciar consulta' desde una cita — no hay alta manual suelta."""
    return render_template('consulta-agregar.html', id_consulta=id_consulta)


@consultamod.route('/tratamiento-plan/<int:id_tratamiento>')
@role_required("CLINICO")
def tratamientoPlan(id_tratamiento):
    """Plan de sesiones de un tratamiento: el especialista agenda por tandas las citas de Tratamiento de su paciente."""
    return render_template('tratamiento-plan.html', id_tratamiento=id_tratamiento)


@consultamod.route('/tratamiento-plan/nuevo/<int:id_consulta>')
@role_required("CLINICO")
def tratamientoPlanNuevo(id_consulta):
    """Plan de un tratamiento nuevo de la consulta: se indica el tratamiento y se agendan sus sesiones por tandas.
    Solo el especialista de la consulta; el tratamiento se crea al guardar el plan o al generar la primera tanda."""
    id_funcionario = session.get('id_funcionario')
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    consulta = TratamientoDao().getContextoConsulta(id_consulta)
    if not consulta or not id_especialista or consulta['id_especialista'] != id_especialista:
        abort(404)
    return render_template('tratamiento-plan.html', id_tratamiento=None, id_consulta=id_consulta,
                           id_especialista=id_especialista,
                           paciente=f"{consulta['paciente_nombre']} {consulta['paciente_apellido']}".strip(),
                           horizonte_dias=AgendaHorariosDao.HORIZONTE_DIAS_DEFAULT)


@consultamod.route('/proximo-control/<int:id_consulta>')
@role_required("CLINICO")
def proximoControl(id_consulta):
    """Próximo control: el especialista elige un turno libre de su agenda y se crea la cita de Seguimiento del paciente.
    `volver=agenda` (al finalizar la consulta) vuelve a Mi Agenda; sin eso, vuelve a la consulta."""
    id_funcionario = session.get('id_funcionario')
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    consulta = TratamientoDao().getContextoConsulta(id_consulta)
    if not consulta or not id_especialista or consulta['id_especialista'] != id_especialista:
        abort(404)
    return render_template('proximo-control.html', id_consulta=id_consulta,
                           paciente=f"{consulta['paciente_nombre']} {consulta['paciente_apellido']}".strip())
