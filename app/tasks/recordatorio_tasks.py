"""Tarea programada que envía los recordatorios pendientes (reglas 1440min/120min
creadas al confirmar una cita, ver CitaDao.cambiarEstadoCita) por WhatsApp (UltraMsg).
Requiere ULTRAMSG_INSTANCE_ID y ULTRAMSG_TOKEN en el .env."""
from app import app
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.services.UltraMsgService import UltraMsgService


def procesar_recordatorios_pendientes():
    with app.app_context():
        recordatorio_dao = RecordatorioDao()
        ultramsg_service = UltraMsgService()

        if not ultramsg_service.client_available:
            app.logger.error("Recordatorios no procesados: UltraMsg no está configurado.")
            return {'total': 0, 'enviados': 0, 'fallidos': 0}

        pendientes = recordatorio_dao.getPendientesEnVentana(limite=100)
        estadisticas = {'total': len(pendientes), 'enviados': 0, 'fallidos': 0}

        for r in pendientes:
            if not r['paciente_telefono']:
                estadisticas['fallidos'] += 1
                app.logger.warning(
                    f"Recordatorio {r['id_recordatorio']} (cita {r['id_cita']}): "
                    "paciente sin teléfono registrado."
                )
                continue

            success, _message_id, error, _tipo_error = ultramsg_service.enviar_recordatorio_cita(
                telefono=r['paciente_telefono'],
                nombre_paciente=r['paciente_nombre'],
                cita_fecha=r['cita_fecha'],
                cita_hora=r['cita_hora'],
                especialista=r['especialista_nombre'],
                especialidad=r['des_especialidad'] or 'Consulta',
                motivo=r['cita_motivo'],
            )

            if success:
                recordatorio_dao.marcarEnviado(r['id_recordatorio'])
                estadisticas['enviados'] += 1
            else:
                estadisticas['fallidos'] += 1
                app.logger.warning(
                    f"Recordatorio {r['id_recordatorio']} (cita {r['id_cita']}) falló: {error}"
                )

        app.logger.info(
            f"Recordatorios procesados: {estadisticas['total']} "
            f"(enviados: {estadisticas['enviados']}, fallidos: {estadisticas['fallidos']})"
        )
        return estadisticas


def configurar_tarea_recordatorios(scheduler):
    """Uso: scheduler = BackgroundScheduler(); configurar_tarea_recordatorios(scheduler); scheduler.start()"""
    with app.app_context():
        scheduler.add_job(
            func=procesar_recordatorios_pendientes,
            trigger='interval',
            minutes=10,
            id='procesar_recordatorios',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=300,
        )
        app.logger.info("Tarea programada de recordatorios configurada (cada 10 minutos)")
