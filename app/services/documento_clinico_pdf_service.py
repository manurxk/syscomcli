# app/services/documento_clinico_pdf_service.py

import os
from io import BytesIO
from datetime import datetime, timedelta

from app.services.ficha_html_pdf_service import FichaHtmlPdfService, WEASYPRINT_AVAILABLE
from app.dao.mantenimiento.referenciales.empresa.EmpresaDao import EmpresaDao

if WEASYPRINT_AVAILABLE:
    from weasyprint import HTML
else:
    from xhtml2pdf import pisa

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto',
         'septiembre', 'octubre', 'noviembre', 'diciembre']


class DocumentoClinicoPdfService(FichaHtmlPdfService):
    """
    PDF de los documentos que emite el especialista desde la consulta: orden de estudios y
    análisis (ORDEN.html), receta (RECETA.html) y certificado (CERTIFICADO.html).

    Mismo patrón que la ficha (FICHA.html): cada plantilla vive en la carpeta templates de su
    módulo y sus marcadores #!#...#!# se reemplazan por datos ya escapados (_fv). Reutiliza de
    FichaHtmlPdfService el escape, el logo y el motor de PDF.
    """

    BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    MODULO = 'clinico'  # carpeta de app/rutas donde están los módulos de PLANTILLAS
    PLANTILLAS = {
        'orden': ('orden', 'ORDEN.html'),
        'receta': ('receta', 'RECETA.html'),
        'certificado': ('certificado_medico', 'CERTIFICADO.html'),
    }

    # ---------- comunes ----------

    @staticmethod
    def _fecha(valor):
        """'AAAA-MM-DD' -> date (los DAO devuelven las fechas ya formateadas así)."""
        return datetime.strptime(valor, '%Y-%m-%d').date() if valor else None

    @staticmethod
    def _corta(d):
        return d.strftime('%d/%m/%Y') if d else '—'

    @staticmethod
    def _larga(d):
        return f"{d.day} de {MESES[d.month - 1]} de {d.year}" if d else ''

    @staticmethod
    def config_empresa():
        """Datos de la empresa para el encabezado (mismo criterio que el PDF de la ficha)."""
        emp = EmpresaDao().getEmpresaPrincipal() or {}
        ruc = f"{emp.get('ruc_nit', '')}-{emp.get('digito_verificador', '')}" if emp.get('ruc_nit') else ''
        return {
            'nombre': emp.get('nombre_comercial') or emp.get('razon_social', ''),
            'direccion': emp.get('direccion', ''),
            'telefono': emp.get('telefono') or emp.get('celular', ''),
            'ruc': ruc,
        }

    def _reemplazos_comunes(self, numero, fecha, empresa, paciente, generador):
        logo = self._resolver_logo_base64(self.BASE_PATH)
        nacimiento = paciente.get('fecha_nacimiento') or ''
        if nacimiento and paciente.get('edad') is not None:
            nacimiento += f" · {paciente['edad']} años"
        responsable = ''
        if paciente.get('es_menor'):
            nombre = paciente.get('madre_nombre') or paciente.get('padre_nombre')
            responsable = (f'<tr><td colspan="4"><span class="lbl">Responsable (paciente menor de edad)</span>'
                           f'{self._fv(nombre)}</td></tr>')
        return {
            '#!#pathLogo#!#': f'<img src="data:image/png;base64,{logo}" alt="Logo">' if logo else '',
            '#!#EMPRESA_NOMBRE#!#': self._fv(empresa.get('nombre'), 'SYSCLIN'),
            '#!#EMPRESA_DIRECCION#!#': self._fv(empresa.get('direccion'), ''),
            '#!#EMPRESA_TELEFONO#!#': self._fv(empresa.get('telefono'), ''),
            '#!#EMPRESA_RUC#!#': self._fv(empresa.get('ruc'), ''),
            '#!#NUMERO#!#': self._fv(numero),
            '#!#FECHA#!#': self._corta(fecha),
            '#!#PAC_NOMBRE#!#': self._fv(paciente.get('nombre_completo')),
            '#!#PAC_CEDULA#!#': self._fv(paciente.get('cedula')),
            '#!#PAC_NAC_EDAD#!#': self._fv(nacimiento),
            '#!#PAC_HISTORIA#!#': self._fv(paciente.get('historia_clinica')),
            '#!#FILA_RESPONSABLE#!#': responsable,
            '#!#FIRMA_NOMBRE#!#': self._fv(generador.get('nombre_completo')),
            '#!#FIRMA_MATRICULA#!#': self._fv(generador.get('matricula')),
            '#!#FIRMA_ESPECIALIDAD#!#': self._fv(generador.get('especialidades'), ''),
        }

    def _render(self, tipo, reemplazos):
        carpeta, archivo = self.PLANTILLAS[tipo]
        ruta = os.path.join(self.BASE_PATH, 'app', 'rutas', self.MODULO, 'movimientos', carpeta, 'templates', archivo)
        with open(ruta, 'r', encoding='utf-8') as f:
            html = f.read()
        for marcador, valor in reemplazos.items():
            html = html.replace(marcador, str(valor) if valor is not None else '')

        buffer = BytesIO()
        if WEASYPRINT_AVAILABLE:
            HTML(string=html, base_url=self.BASE_PATH).write_pdf(buffer)
        else:
            pisa_status = pisa.CreatePDF(html, dest=buffer, encoding='utf-8')
            if pisa_status.err:
                raise Exception("Error al generar PDF con xhtml2pdf.")
        buffer.seek(0)
        return buffer

    # ---------- documentos ----------

    def generar_orden_pdf(self, orden, paciente, generador, empresa):
        """orden: OrdenDao.getParaImprimir; paciente: FichaDao.getDatosPaciente; generador: FichaDao.getDatosGenerador."""
        diagnosticos = ''.join(
            f"<div>{self._fv(d.get('cod_cie10'))} — {self._fv(d.get('des_diagnostico'))}</div>"
            for d in orden.get('diagnosticos') or []) or 'Sin diagnóstico registrado en la consulta.'
        items = ''.join(
            f'<tr><td style="text-align: center; width: 6%;">{i}</td>'
            f'<td style="width: 18%;">{"ANÁLISIS" if d.get("tipo_orden") == "ANALISIS" else "ESTUDIO"}</td>'
            f'<td>{self._fv(d.get("descripcion"))}</td></tr>'
            for i, d in enumerate(orden.get('detalles') or [], 1))
        reemplazos = self._reemplazos_comunes(orden.get('orden_numero'), self._fecha(orden.get('orden_fecha')),
                                              empresa, paciente, generador)
        reemplazos.update({
            '#!#DIAGNOSTICOS#!#': diagnosticos,
            '#!#ITEMS#!#': items,
            '#!#INDICACIONES#!#': self._fv(orden.get('orden_indicaciones')),
            '#!#OBSERVACIONES#!#': self._fv(orden.get('orden_observaciones')),
        })
        return self._render('orden', reemplazos)

    def generar_receta_pdf(self, receta, paciente, generador, empresa):
        """receta: RecetaDao.getParaImprimir."""
        filas = ''
        for d in receta.get('detalles') or []:
            filas += (f'<tr><td><b>{self._fv(d.get("des_medicamento"))}</b></td>'
                      f'<td>{self._fv(d.get("medicamento_dosis"))}</td>'
                      f'<td>{self._fv(d.get("medicamento_frecuencia"))}</td>'
                      f'<td style="text-align: center;">{self._fv(d.get("medicamento_duracion"))}</td>'
                      f'<td style="text-align: center;">{self._fv(d.get("medicamento_cantidad"))}</td></tr>')
            if d.get('medicamento_indicaciones'):
                filas += f'<tr><td colspan="5" class="indic">Indicación: {self._fv(d["medicamento_indicaciones"])}</td></tr>'
        fecha = self._fecha(receta.get('receta_fecha'))
        dias = receta.get('receta_validez_dias')
        validez = f"{dias} días (hasta el {self._corta(fecha + timedelta(days=dias))})" if dias and fecha else '—'
        observaciones = ''
        if receta.get('receta_observaciones'):
            observaciones = (f'<tr><td><span class="lbl">Observaciones</span><span class="texto-largo">'
                             f'{self._fv(receta["receta_observaciones"])}</span></td></tr>')
        reemplazos = self._reemplazos_comunes(receta.get('receta_numero'), fecha, empresa, paciente, generador)
        reemplazos.update({
            '#!#ITEMS#!#': filas,
            '#!#INDICACIONES#!#': self._fv(receta.get('receta_indicaciones_generales')),
            '#!#FILA_OBSERVACIONES#!#': observaciones,
            '#!#VALIDEZ#!#': validez,
        })
        return self._render('receta', reemplazos)

    def generar_certificado_pdf(self, cert, paciente, generador, empresa):
        """cert: CertificadoMedicoDao.getParaImprimir. El diagnóstico solo aparece si se cargó."""
        fecha = self._fecha(cert.get('certificado_fecha'))
        especialidad = cert.get('des_especialidad') or generador.get('especialidades') or 'la especialidad'
        texto = (f"Por la presente certifico que <b>{self._fv(paciente.get('nombre_completo'))}</b>, con cédula de "
                 f"identidad Nº <b>{self._fv(paciente.get('cedula'))}</b>, asistió a consulta de "
                 f"<b>{self._fv(especialidad)}</b> el día <b>{self._larga(fecha)}</b>")
        if cert.get('hora_inicio') and cert.get('hora_fin'):
            texto += f", en el horario de {cert['hora_inicio']} a {cert['hora_fin']}"
        texto += '.'
        dias = cert.get('certificado_dias_reposo')
        if dias:
            desde, hasta = self._fecha(cert.get('certificado_desde_fecha')), self._fecha(cert.get('certificado_hasta_fecha'))
            texto += f" Se indica reposo de <b>{dias} día{'s' if dias != 1 else ''}</b>"
            if desde and hasta:
                texto += f", desde el {self._corta(desde)} hasta el {self._corta(hasta)}"
            texto += '.'

        filas = ''
        for etiqueta, campo in (('Motivo', 'certificado_motivo'), ('Diagnóstico', 'certificado_diagnostico'),
                                ('Recomendaciones', 'certificado_recomendaciones')):
            if cert.get(campo):
                filas += (f'<tr><td><span class="lbl">{etiqueta}</span><span class="texto-largo">'
                          f'{self._fv(cert[campo])}</span></td></tr>')

        tipo = self._fv(cert.get('des_tipo_certificado_medico'), 'Certificado').upper()
        titulo = tipo.replace('CERTIFICADO ', 'CERTIFICADO<br>', 1) if tipo.startswith('CERTIFICADO ') else tipo
        reemplazos = self._reemplazos_comunes(cert.get('certificado_numero'), fecha, empresa, paciente, generador)
        reemplazos.update({
            '#!#TITULO#!#': titulo,
            '#!#TEXTO#!#': texto,
            '#!#FILAS_DATOS#!#': filas,
            '#!#FECHA_LARGA#!#': self._larga(fecha),
        })
        return self._render('certificado', reemplazos)
