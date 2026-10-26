"""Tarea programada que pasa a «Pendiente de observación» (EN_OBSERVACION) las consultas que el especialista inició y no
cerró en el día. Corre todos los días a las 23:00 (hora de Asunción); al iniciar el servidor completa las de días
anteriores si estuvo apagado. La cita de origen queda como está (EN_CONSULTA): se completa cuando el especialista cierra
la consulta. Es idempotente: solo toca consultas PENDIENTE o EN_ATENCION."""
from datetime import datetime

from app import app
from app.core.base_dao import BaseDAO


def pasar_consultas_a_observacion(incluir_hoy=True):
    """Pasa a EN_OBSERVACION las consultas abiertas de días anteriores y, con `incluir_hoy`, también las de hoy.
    Devuelve cuántas pasó. No toca la cita ni el contenido clínico; la auditoría de `consultas` deja el cambio."""
    with app.app_context():
        comparador = '<=' if incluir_hoy else '<'
        cantidad = BaseDAO(db_name_env="DB_NAME_NUEVA").execute_query(
            f"""UPDATE consultas SET consulta_estado = 'EN_OBSERVACION'
                WHERE est_consulta = TRUE AND consulta_estado IN ('PENDIENTE', 'EN_ATENCION')
                  AND consulta_fecha::date {comparador} (now() AT TIME ZONE 'America/Asuncion')::date""",
            commit=True)
        app.logger.info(f"Consultas pasadas a «Pendiente de observación»: {cantidad}")
        return cantidad


def configurar_tarea_consultas(scheduler):
    """Uso: scheduler = BackgroundScheduler(); configurar_tarea_consultas(scheduler); scheduler.start()
    Corre cada día a las 23:00 y una vez al iniciar (solo con las consultas de días anteriores)."""
    with app.app_context():
        scheduler.add_job(
            func=pasar_consultas_a_observacion,
            trigger='cron', hour=23, minute=0, timezone='America/Asuncion',
            id='consultas_a_observacion',
            replace_existing=True,
            max_instances=1,
            coalesce=True,
            misfire_grace_time=3600,
        )
        scheduler.add_job(
            func=pasar_consultas_a_observacion, kwargs={'incluir_hoy': False},
            trigger='date', run_date=datetime.now(),
            id='consultas_a_observacion_inicio',
            replace_existing=True,
        )
        app.logger.info("Tarea programada de consultas sin cerrar configurada (todos los días a las 23:00)")
