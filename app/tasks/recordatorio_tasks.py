"""Tarea programada que envía los recordatorios pendientes (regla EMAIL
1440min/120min creada al confirmar una cita, ver CitaDao.cambiarEstadoCita)
por correo. El envío por WhatsApp (UltraMsg) queda como canal manual/relegado,
disponible vía el botón de reenvío en la cita."""
from app import app
from app.dao.agendamiento.recordatorio.RecordatorioDao import RecordatorioDao
from app.services.EmailService import EmailService


def procesar_recordatorios_pendientes():
    with app.app_context():
        recordatorio_dao = RecordatorioDao()
        email_service = EmailService()

        pendientes = recordatorio_dao.getPendientesEnVentana(limite=100)
        estadisticas = {'total': len(pendientes), 'enviados': 0, 'fallidos': 0}

        for r in pendientes:
            if not r['paciente_correo']:
                estadisticas['fallidos'] += 1
                app.logger.warning(
                    f"Recordatorio {r['id_recordatorio']} (cita {r['id_cita']}): "
                    "paciente sin correo registrado."
                )
                continue

            success, error, _tipo_error = email_service.enviar_recordatorio_cita(
                correo_destino=r['paciente_correo'],
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
