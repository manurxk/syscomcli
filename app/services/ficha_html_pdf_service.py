# app/services/ficha_html_pdf_service.py

import os
import base64
from io import BytesIO
from datetime import datetime

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint no disponible ({type(e).__name__}: {e}). Usando xhtml2pdf como alternativa.")
    from xhtml2pdf import pisa


class FichaHtmlPdfService:
    """
    Genera el PDF de la ficha médica usando la plantilla HTML `FICHA.html`
    (mismo patrón que FacturaPDFService/FE.html para el KuDE de facturas).
    """

    def _get_image_base64(self, image_path):
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error al leer imagen {image_path}: {str(e)}")
        return None

    def _resolver_logo_base64(self, base_path):
        posibles_logos = [
            os.path.join(base_path, 'app', 'static', 'img', 'logo_clinica.png'),
            os.path.join(base_path, 'app', 'static', 'img', 'iconoazul.png'),
            os.path.join(base_path, 'app', 'static', 'img', 'logo.png'),
        ]
        for p in posibles_logos:
            if os.path.exists(p):
                b64 = self._get_image_base64(p)
                if b64:
                    return b64
        return None

    def _fv(self, valor, defecto='—'):
        return str(valor) if valor not in (None, '') else defecto

    def _bloque_tutor(self, paciente):
        if not paciente.get('es_menor'):
            return ''
        return f"""
        <table class="tabla-datos" style="margin-top:4px;">
          <tr>
            <td style="width:25%;"><span class="lbl">Nombre madre</span>{self._fv(paciente.get('madre_nombre'))}</td>
            <td style="width:25%;"><span class="lbl">Tel. madre</span>{self._fv(paciente.get('madre_telefono'))}</td>
            <td style="width:25%;"><span class="lbl">Nombre padre</span>{self._fv(paciente.get('padre_nombre'))}</td>
            <td style="width:25%;"><span class="lbl">Tel. padre</span>{self._fv(paciente.get('padre_telefono'))}</td>
          </tr>
          <tr>
            <td colspan="4"><span class="lbl">Colegio</span>{self._fv(paciente.get('colegio'))}</td>
          </tr>
        </table>"""

    def _diagnosticos_html(self, diagnosticos):
        if not diagnosticos:
            return '<tr><td colspan="2" class="celda-contenido">Sin diagnósticos registrados.</td></tr>'
        filas = []
        for d in diagnosticos:
            filas.append(
                f'<tr><td>{self._fv(d.get("cod_cie10"))}</td>'
                f'<td>{self._fv(d.get("diagnostico"))}</td></tr>'
            )
        return "".join(filas)

    def _tratamientos_html(self, tratamientos):
        if not tratamientos:
            return '<tr><td colspan="4" class="celda-contenido">Sin tratamientos activos.</td></tr>'
        filas = []
        for t in tratamientos:
            filas.append(
                f'<tr><td>{self._fv(t.get("tipo_tratamiento"))}</td>'
                f'<td>{self._fv(t.get("descripcion"))}</td>'
                f'<td>{self._fv(t.get("fecha_inicio"))}</td>'
                f'<td>{self._fv(t.get("profesional"))}</td></tr>'
            )
        return "".join(filas)

    def generar_ficha_html_pdf(self, ficha_data, config_empresa=None, generado_por=None):
        """
        Args:
            ficha_data (dict): salida de FichaDao.getFichaCompleta()
            config_empresa (dict, optional): nombre, direccion, telefono, ruc, sitio_web
            generado_por (dict, optional): nombre_completo, matricula (de FichaDao.getDatosGenerador)

        Returns:
            BytesIO: buffer con el PDF generado
        """
        empresa = config_empresa or {}
        generador = generado_por or {}
        paciente = ficha_data.get('paciente') or {}
        anamnesis = ficha_data.get('anamnesis') or {}

        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(base_path, 'FICHA.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        logo_base64 = self._resolver_logo_base64(base_path)
        proximas_citas = ficha_data.get('proximas_citas') or []

        fecha_nac_edad = ''
        if paciente.get('fecha_nacimiento'):
            fecha_nac_edad = paciente['fecha_nacimiento']
            if paciente.get('edad') is not None:
                fecha_nac_edad += f" · {paciente['edad']} años"

        reemplazos = {
            '#!#pathLogo#!#': f'<img src="data:image/png;base64,{logo_base64}" alt="Logo">' if logo_base64 else '',
            '#!#EMPRESA_NOMBRE#!#': self._fv(empresa.get('nombre'), 'SYSCLIN'),
            '#!#EMPRESA_DIRECCION#!#': self._fv(empresa.get('direccion'), ''),
            '#!#EMPRESA_TELEFONO#!#': self._fv(empresa.get('telefono'), ''),
            '#!#EMPRESA_RUC#!#': self._fv(empresa.get('ruc'), ''),
            '#!#EMPRESA_WEB#!#': self._fv(empresa.get('sitio_web'), ''),

            '#!#HISTORIA_CLINICA#!#': self._fv(paciente.get('historia_clinica')),
            '#!#FECHA_GENERACION#!#': datetime.now().strftime('%d/%m/%Y %H:%M'),

            '#!#PAC_NOMBRE#!#': self._fv(paciente.get('nombre_completo')),
            '#!#PAC_FECHA_NAC_EDAD#!#': self._fv(fecha_nac_edad),
            '#!#PAC_GENERO#!#': self._fv(paciente.get('genero')),
            '#!#PAC_CEDULA#!#': self._fv(paciente.get('cedula')),
            '#!#PAC_ESTADO_CIVIL#!#': self._fv(paciente.get('estado_civil')),
            '#!#PAC_TELEFONO#!#': self._fv(paciente.get('telefono')),
            '#!#PAC_CORREO#!#': self._fv(paciente.get('correo')),
            '#!#PAC_DOMICILIO#!#': self._fv(paciente.get('domicilio')),
            '#!#PAC_CIUDAD#!#': self._fv(paciente.get('ciudad')),
            '#!#BLOQUE_TUTOR#!#': self._bloque_tutor(paciente),

            '#!#TOTAL_CONSULTAS#!#': str(len(ficha_data.get('consultas_recientes') or [])),
            '#!#TOTAL_DIAGNOSTICOS#!#': str(len(ficha_data.get('diagnosticos') or [])),
            '#!#TOTAL_TRATAMIENTOS#!#': str(len(ficha_data.get('tratamientos_activos') or [])),
            '#!#PROXIMA_CITA#!#': proximas_citas[0]['fecha'] if proximas_citas else 'Sin citas próximas',

            '#!#MOTIVO_CONSULTA#!#': self._fv(anamnesis.get('motivo_consulta'), 'Sin anamnesis registrada.'),
            '#!#ANTEC_PERSONALES#!#': self._fv(anamnesis.get('antecedentes_patologicos_personales')),
            '#!#ANTEC_FAMILIARES#!#': self._fv(anamnesis.get('antecedentes_patologicos_familiares')),
            '#!#MEDICACION_ACTUAL#!#': self._fv(anamnesis.get('medicacion_actual')),
            '#!#MEDICACION_PSIQUIATRICA#!#': self._fv(anamnesis.get('medicacion_psiquiatrica_previa')),

            '#!#DIAGNOSTICOS_HTML#!#': self._diagnosticos_html(ficha_data.get('diagnosticos')),
            '#!#TRATAMIENTOS_HTML#!#': self._tratamientos_html(ficha_data.get('tratamientos_activos')),

            '#!#GENERADOR_NOMBRE#!#': self._fv(generador.get('nombre_completo'), 'No especificado'),
            '#!#GENERADOR_MATRICULA#!#': self._fv(generador.get('matricula')),

            '#!#ANIO_ACTUAL#!#': str(datetime.now().year),
        }

        for marcador, valor in reemplazos.items():
            html = html.replace(marcador, str(valor) if valor is not None else '')

        buffer = BytesIO()
        if WEASYPRINT_AVAILABLE:
            try:
                HTML(string=html, base_url=base_path).write_pdf(buffer)
            except Exception as e:
                raise Exception(f"Error al generar PDF con WeasyPrint: {str(e)}")
        else:
            pisa_status = pisa.CreatePDF(html, dest=buffer, encoding='utf-8')
            if pisa_status.err:
                raise Exception("Error al generar PDF con xhtml2pdf.")

        buffer.seek(0)
        return buffer
