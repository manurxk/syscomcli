"""
BudgetAutomationService — Automatización del ciclo de vida de presupuestos.

Responsabilidades:
  1. Marcar como VENCIDO los presupuestos PENDIENTES cuya fecha_vencimiento
     haya pasado (tarea programada diaria a las 07:00 AM).
  2. Notificar al área de ventas cuando hay presupuestos vencidos (stub
     preparado para integración con email o notificación interna).
  3. Exponer iniciar_scheduler() para ser llamado desde el __init__ de Flask.

Dependencias externas:
  - APScheduler (pip install apscheduler)
  - Las DAOs existentes del proyecto (PresupuestoDao)

Uso típico (en app/__init__.py o create_app):
    from app.services.budget_automation_service import iniciar_scheduler
    iniciar_scheduler(app)
"""
import logging
from datetime import datetime
from typing import List

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask


logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Alerta al área de ventas
# ---------------------------------------------------------------------------

def enviar_alerta_ventas(ids_presupuestos: List[int]) -> None:
    """
    Stub: notifica al área de ventas sobre presupuestos recién vencidos.

    Preparado para integración futura con:
      - Email (Flask-Mail / smtplib)
      - Notificación interna (tabla notificaciones + WebSocket)
      - Webhook externo (Slack, Teams, etc.)

    Args:
        ids_presupuestos: Lista de IDs de presupuestos que acaban de vencerse.
    """
    if not ids_presupuestos:
        return

    # TODO: Reemplazar este stub con el mecanismo de notificación real.
    logger.info(
        f"[BudgetAutomation] ALERTA VENTAS — {len(ids_presupuestos)} presupuesto(s) "
        f"vencido(s): {ids_presupuestos}"
    )

    # Ejemplo de integración futura con email:
    # from flask_mail import Message, mail
    # msg = Message(
    #     subject="Presupuestos vencidos hoy",
    #     recipients=["ventas@sysclin.com"],
    #     body=f"{len(ids_presupuestos)} presupuesto(s) vencieron hoy: {ids_presupuestos}"
    # )
    # mail.send(msg)


# ---------------------------------------------------------------------------
# Tarea programada
# ---------------------------------------------------------------------------

def _tarea_vencimiento_presupuestos() -> None:
    """
    Tarea diaria: consulta presupuestos PENDIENTES vencidos y los marca como
    VENCIDO en batch.

    Llamada automáticamente por APScheduler a las 07:00 AM hora local.
    No debe llamarse directamente en producción.
    """
    logger.info(
        f"[BudgetAutomation] Iniciando tarea de vencimiento — "
        f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    )

    try:
        from app.dao.modulos.ventas.presupuesto.PresupuestoDao import PresupuestoDao
        dao = PresupuestoDao()

        # Obtener IDs de presupuestos que van a vencer (para la alerta)
        # Hacemos esto ANTES de actualizar el estado para tener los IDs
        presupuestos_a_vencer = dao.getPresupuestosProximosAVencer(dias_alerta=0)
        ids_a_vencer = [p['id_presupuesto'] for p in presupuestos_a_vencer]

        # Actualizar estado a VENCIDO en batch
        cantidad = dao.vencerPresupuestosExpirados(usuario_modificacion='SISTEMA')

        if cantidad > 0:
            logger.info(
                f"[BudgetAutomation] {cantidad} presupuesto(s) marcado(s) como VENCIDO."
            )
            # Notificar al área de ventas
            enviar_alerta_ventas(ids_a_vencer)
        else:
            logger.info("[BudgetAutomation] No hay presupuestos vencidos para procesar.")

    except Exception as e:
        logger.error(
            f"[BudgetAutomation] Error en tarea de vencimiento: {str(e)}",
            exc_info=True
        )


# ---------------------------------------------------------------------------
# Inicialización del scheduler
# ---------------------------------------------------------------------------

_scheduler: BackgroundScheduler = None


def iniciar_scheduler(app: Flask) -> None:
    """
    Inicializa y arranca el BackgroundScheduler de APScheduler.

    Configura la tarea de vencimiento de presupuestos para ejecutarse
    cada día a las 07:00 AM hora local.

    Args:
        app: Instancia de la aplicación Flask. Se usa para ejecutar las
             tareas dentro del contexto de la app (acceso a config, DAOs, etc.)

    Ejemplo de uso (app/__init__.py):
        from app.services.budget_automation_service import iniciar_scheduler
        iniciar_scheduler(app)
    """
    global _scheduler

    if _scheduler and _scheduler.running:
        logger.warning("[BudgetAutomation] El scheduler ya está en ejecución.")
        return

    _scheduler = BackgroundScheduler(timezone='America/Asuncion')

    def tarea_con_contexto():
        """Envuelve la tarea en el contexto de la app Flask."""
        with app.app_context():
            _tarea_vencimiento_presupuestos()

    _scheduler.add_job(
        func=tarea_con_contexto,
        trigger=CronTrigger(hour=7, minute=0),
        id='vencimiento_presupuestos',
        name='Vencimiento automático de presupuestos',
        replace_existing=True,
        max_instances=1,        # Evitar ejecuciones paralelas
        coalesce=True           # Si se acumularon disparos perdidos, ejecutar una sola vez
    )

    _scheduler.start()
    logger.info(
        "[BudgetAutomation] Scheduler iniciado. "
        "Tarea de vencimiento programada para las 07:00 AM diariamente."
    )


def detener_scheduler() -> None:
    """
    Detiene el scheduler de forma limpia.

    Llamar en el teardown de la aplicación para liberar recursos.

    Ejemplo (app/__init__.py):
        import atexit
        from app.services.budget_automation_service import detener_scheduler
        atexit.register(detener_scheduler)
    """
    global _scheduler
    if _scheduler and _scheduler.running:
        _scheduler.shutdown(wait=False)
        logger.info("[BudgetAutomation] Scheduler detenido correctamente.")
