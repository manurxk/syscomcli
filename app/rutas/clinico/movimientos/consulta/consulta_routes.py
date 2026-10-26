from flask import Blueprint, render_template, abort, session, url_for
from app.auth.utils.decorators import role_required
from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.clinico.movimientos.derivacion.DerivacionDao import DerivacionDao
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
    return render_template('proximo-control.html', paciente=f"{consulta['paciente_nombre']} {consulta['paciente_apellido']}".strip(),
                           titulo='Próximo control', motivo_defecto='Control', volver_agenda=False,
                           subtitulo='Elegí un turno libre de tu agenda: se crea la cita de Seguimiento del paciente y recepción la ve en su calendario',
                           api_turnos=f'/api/v1/consultas/{id_consulta}/proximo-control/turnos',
                           api_agendar=f'/api/v1/consultas/{id_consulta}/proximo-control',
                           url_volver_consulta=url_for('consulta.consultaAgregar', id_consulta=id_consulta))


@consultamod.route('/derivacion-cita/<int:id_derivacion>')
@role_required("CLINICO")
def derivacionCita(id_derivacion):
    """Cita del paciente derivado: el especialista que aceptó la derivación elige un turno libre de su agenda
    (cita de Primera vez con él). Se llega desde la tarjeta «Derivaciones» de Mi Agenda."""
    id_funcionario = session.get('id_funcionario')
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    d = DerivacionDao().getById(id_derivacion)
    if not d or not id_especialista or d['id_especialista_destino'] != id_especialista or d['estado_derivacion'] != 'ACEPTADA':
        abort(404)
    consulta = TratamientoDao().getContextoConsulta(d['id_consulta'])
    return render_template('proximo-control.html', paciente=f"{consulta['paciente_nombre']} {consulta['paciente_apellido']}".strip(),
                           titulo='Cita del paciente derivado', motivo_defecto='Derivación', volver_agenda=True,
                           subtitulo='Elegí un turno libre de tu agenda: se crea la cita de Primera vez del paciente que te derivaron',
                           api_turnos=f'/api/v1/derivaciones/{id_derivacion}/cita/turnos',
                           api_agendar=f'/api/v1/derivaciones/{id_derivacion}/cita',
                           url_volver_consulta=None)
