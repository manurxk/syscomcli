"""Tarea programada que mantiene el horizonte rodante de turnos (slots_agenda).
Los slots se generan para los próximos HORIZONTE_DIAS_DEFAULT días al crear o
editar un horario (ver AgendaHorariosDao._generarSlots); sin esta tarea, un
horario que nadie vuelve a guardar se queda sin turnos pasado ese horizonte.
Es idempotente (ON CONFLICT DO NOTHING), así que correrla de más no duplica."""
from datetime import datetime

from app import app
from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao


def extender_slots_agendas():
    with app.app_context():
        agenda_dao = AgendaHorariosDao()

        agendas = agenda_dao.getAgendasVigentesActivas()
        estadisticas = {'agendas': len(agendas), 'slots_nuevos': 0, 'fallidas': 0}

        for a in agendas:
            try:
                estadisticas['slots_nuevos'] += agenda_dao.extenderSlotsAgenda(a['id_agenda_horario']) or 0
            except Exception as e:
                estadisticas['fallidas'] += 1
                app.logger.warning(f"Agenda {a['id_agenda_horario']}: no se pudieron extender los turnos: {e}")

        app.logger.info(
            f"Turnos de agenda extendidos: {estadisticas['agendas']} horarios "
            f"(slots nuevos: {estadisticas['slots_nuevos']}, fallidos: {estadisticas['fallidas']})"
        )
        return estadisticas


def configurar_tarea_agenda(scheduler):
    """Uso: scheduler = BackgroundScheduler(); configurar_tarea_agenda(scheduler); scheduler.start()
    Corre al iniciar el servidor y después cada 24 horas: si el servidor estuvo
    apagado, la primera ejecución completa los días que faltaban."""
    with app.app_context():
        scheduler.add_job(
            func=extender_slots_agendas,
            trigger='interval',
            hours=24,
            next_run_time=datetime.now(),
            id='extender_slots_agendas',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
        )
        app.logger.info("Tarea programada de turnos de agenda configurada (al iniciar y cada 24 horas)")
