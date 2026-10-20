"""Tareas programadas de la auditoría de cambios en datos (PDF 9 + 6, paso 6).

- Alertas (cada 5 minutos): revisa los cambios nuevos de auditoria_transacciones y, si hay anulaciones o cambios
  fuera del horario de atención, manda un correo a cada Administrador / Superadministrador activo con correo,
  con solo lo que su rol puede ver. Al enviar registra ALERTA_ENVIADA en auditoria_sistema con el último cambio
  revisado ("hasta el cambio #N"), así tras un reinicio no repite alertas.
- Informe semanal (lunes 07:00, hora de Paraguay): PDF de la semana anterior a los mismos destinatarios;
  registra INFORME_SEMANAL.
Los correos salen por EmailService (sin SMTP configurado, solo se escriben en el log)."""
from app import app
from app.dao.mantenimiento.auditoria.AuditoriaDao import AuditoriaDao
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao
from app.services.EmailService import EmailService
from app.services.informe_auditoria_service import (armar_informe, correo_alerta, generar_pdf_informe,
                                                    modulos_destinatario, motivos_alerta, semana_anterior)
from app.utils.auditoria_constantes import AuditAccion

# Último cambio revisado por este proceso. Arranca en el de la última alerta enviada (o en el último cambio
# existente, si nunca se envió una: no se avisa de lo anterior a la puesta en marcha).
_ultimo_revisado = None


def procesar_alertas_auditoria():
    global _ultimo_revisado
    with app.app_context():
        dao = AuditoriaDao()
        if _ultimo_revisado is None:
            _ultimo_revisado = dao.getUltimoIdAlertado()
            if _ultimo_revisado is None:
                _ultimo_revisado = dao.getMaxIdCambio()
                app.logger.info(f"Alertas de auditoría: se empieza a revisar después del cambio #{_ultimo_revisado}")
                return {'revisados': 0, 'alertas': 0}

        cambios = dao.getCambiosDesde(_ultimo_revisado)
        if not cambios:
            return {'revisados': 0, 'alertas': 0}
        empresadao = EmpresaDao()
        tramos = empresadao.getTramosHorario()
        alertas = []
        for c in cambios:
            c['motivos'] = motivos_alerta(c, tramos, empresadao)
            if c['motivos']:
                alertas.append(c)
        hasta = cambios[-1]['id_auditoria_transaccion']

        if alertas:
            email = EmailService()
            enviados = []
            for d in dao.getDestinatariosAuditoria():
                modulos = modulos_destinatario(d['roles'])
                suyas = [a for a in alertas if a['modulo'] in modulos]
                if not suyas:
                    continue
                asunto, texto, html = correo_alerta(suyas)
                ok, error, _ = email.enviar_correo(d['correo'], asunto, texto, cuerpo_html=html)
                enviados.append(f"{d['usu_nick']} ({len(suyas)}{'' if ok else ', ERROR: ' + str(error)})")
            anulaciones = sum('Anulación' in a['motivos'] for a in alertas)
            fuera = sum('Fuera de horario' in a['motivos'] for a in alertas)
            dao.registrar_evento(
                None, AuditAccion.ALERTA_ENVIADA,
                f"Alertas de auditoría hasta el cambio #{hasta}: {anulaciones} anulación(es), {fuera} fuera de horario. "
                f"Destinatarios: {', '.join(enviados) or 'ninguno con correo cargado'}")
            app.logger.info(f"Alertas de auditoría: {len(alertas)} cambio(s) alertado(s) hasta el #{hasta}")

        _ultimo_revisado = hasta
        return {'revisados': len(cambios), 'alertas': len(alertas)}


def enviar_informe_semanal(hoy=None):
    with app.app_context():
        dao = AuditoriaDao()
        desde, hasta = semana_anterior(hoy)
        email = EmailService()
        enviados = []
        for d in dao.getDestinatariosAuditoria():
            modulos = modulos_destinatario(d['roles'])
            if not modulos:
                continue
            pdf = generar_pdf_informe(armar_informe(modulos, desde, hasta))
            ok, error, _ = email.enviar_correo(
                d['correo'], f"Sysclin · Informe de auditoría del {desde:%d/%m} al {hasta:%d/%m/%Y}",
                f"Adjunto el informe de auditoría de la semana del {desde:%d/%m/%Y} al {hasta:%d/%m/%Y}.",
                adjuntos=[{'nombre': f'Informe_auditoria_{desde}_al_{hasta}.pdf', 'contenido': pdf,
                           'mime': ('application', 'pdf')}])
            enviados.append(f"{d['usu_nick']}{'' if ok else ' (ERROR: ' + str(error) + ')'}")
        dao.registrar_evento(None, AuditAccion.INFORME_SEMANAL,
                             f"Informe de auditoría del {desde} al {hasta}. Destinatarios: "
                             f"{', '.join(enviados) or 'ninguno con correo cargado'}")
        app.logger.info(f"Informe semanal de auditoría ({desde} al {hasta}) enviado a: {', '.join(enviados) or 'nadie'}")
        return enviados


def configurar_tarea_auditoria(scheduler):
    """Uso: scheduler = BackgroundScheduler(); configurar_tarea_auditoria(scheduler); scheduler.start()"""
    with app.app_context():
        scheduler.add_job(func=procesar_alertas_auditoria, trigger='interval', minutes=5,
                          id='alertas_auditoria', replace_existing=True, max_instances=1, coalesce=True,
                          misfire_grace_time=300)
        scheduler.add_job(func=enviar_informe_semanal, trigger='cron', day_of_week='mon', hour=7, minute=0,
                          id='informe_semanal_auditoria', replace_existing=True, max_instances=1, coalesce=True,
                          misfire_grace_time=3600)
        app.logger.info("Tareas programadas de auditoría configuradas (alertas cada 5 min; informe los lunes 07:00)")
