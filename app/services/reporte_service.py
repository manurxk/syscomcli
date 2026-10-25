from io import BytesIO

from flask import current_app as app

try:
    from weasyprint import HTML
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint no disponible ({type(e).__name__}: {e}). Usando xhtml2pdf como alternativa.")
    from xhtml2pdf import pisa

class ReporteService:
    """
    Servicio de Reportes para procesar info del DAO hacia las vistas y Chart.js.
    Fase 1: Implementado el procesado de ventas para UI.
    """

    def procesar_ventas_para_grafico(self, data):
        """
        Transforma la lista de diccionarios del DAO en el formato JSON
        que Chart.js espera. `data` ya viene agrupado por fecha+moneda desde
        el DAO, asi que cada moneda presente en el rango se grafica como una
        serie (dataset) propia en el mismo eje de fechas — nunca se suman
        montos de monedas distintas en la misma linea.
        """
        try:
            fechas_ordenadas = []
            for fila in data:
                fecha_parts = fila['fecha'].split('-')
                fecha_esf = f"{fecha_parts[2]}/{fecha_parts[1]}/{fecha_parts[0]}" if len(fecha_parts) == 3 else fila['fecha']
                if fecha_esf not in fechas_ordenadas:
                    fechas_ordenadas.append(fecha_esf)

            colores = ["rgba(13, 110, 253, 1)", "rgba(220, 53, 69, 1)", "rgba(25, 135, 84, 1)", "rgba(255, 193, 7, 1)"]
            por_moneda = {}
            for fila in data:
                fecha_parts = fila['fecha'].split('-')
                fecha_esf = f"{fecha_parts[2]}/{fecha_parts[1]}/{fecha_parts[0]}" if len(fecha_parts) == 3 else fila['fecha']
                cod = fila.get('cod_moneda', 'PYG')
                por_moneda.setdefault(cod, {}).setdefault(fecha_esf, 0)
                por_moneda[cod][fecha_esf] += fila['total_general']

            datasets = []
            for i, (cod, valores_por_fecha) in enumerate(por_moneda.items()):
                color = colores[i % len(colores)]
                datasets.append({
                    "label": f"Total Ventas ({cod})",
                    "data": [valores_por_fecha.get(f, 0) for f in fechas_ordenadas],
                    "backgroundColor": color.replace(", 1)", ", 0.5)"),
                    "borderColor": color,
                    "borderWidth": 1
                })

            return {"labels": fechas_ordenadas, "datasets": datasets}
        except Exception as e:
            app.logger.error(f"Error procesando ventas para gráfico: {str(e)}")
            return {"labels": [], "datasets": []}

    def calcular_totales_ventas(self, data):
        """
        Calcula la sumatoria para las KPIs de la UI del reporte, agrupada por
        moneda: sumar Gs. + USD en el mismo total daria un numero sin sentido.
        Devuelve una LISTA (un total por moneda presente en el periodo), no un dict unico.
        """
        por_moneda = {}
        try:
            for fila in data:
                cod = fila.get('cod_moneda', 'PYG')
                if cod not in por_moneda:
                    por_moneda[cod] = {
                        'id_moneda': fila.get('id_moneda'),
                        'cod_moneda': cod,
                        'simbolo_moneda': fila.get('simbolo_moneda', 'Gs.'),
                        'decimales_moneda': fila.get('decimales_moneda', 0),
                        'cantidad_comprobantes': 0,
                        'total_gravado': 0,
                        'total_iva': 0,
                        'total_general': 0,
                    }
                por_moneda[cod]['cantidad_comprobantes'] += fila.get('cantidad_comprobantes', 0)
                por_moneda[cod]['total_gravado'] += fila.get('total_gravado', 0)
                por_moneda[cod]['total_iva'] += fila.get('total_iva', 0)
                por_moneda[cod]['total_general'] += fila.get('total_general', 0)
        except Exception as e:
            app.logger.error(f"Error calculando subtotales de ventas: {str(e)}")

        return list(por_moneda.values())

    def procesar_agendamiento_para_grafico(self, data_diaria):
        labels = []
        atendidas = []
        canceladas = []
        ausencias = []
        
        try:
            for fila in data_diaria:
                fecha_parts = fila['fecha'].split('-')
                if len(fecha_parts) == 3:
                    fecha_esf = f"{fecha_parts[2]}/{fecha_parts[1]}"
                else:
                    fecha_esf = fila['fecha']
                labels.append(fecha_esf)
                atendidas.append(fila['cant_atendidas'])
                canceladas.append(fila['cant_canceladas'])
                ausencias.append(fila['cant_ausencias'])
                
            return {
                "labels": labels,
                "datasets": [
                    {
                        "label": "Atendidas",
                        "data": atendidas,
                        "backgroundColor": "rgba(28, 200, 138, 0.5)",
                        "borderColor": "rgba(28, 200, 138, 1)",
                        "borderWidth": 1
                    },
                    {
                        "label": "Canceladas",
                        "data": canceladas,
                        "backgroundColor": "rgba(231, 74, 59, 0.5)",
                        "borderColor": "rgba(231, 74, 59, 1)",
                        "borderWidth": 1
                    },
                    {
                        "label": "Ausencias",
                        "data": ausencias,
                        "backgroundColor": "rgba(246, 194, 62, 0.5)",
                        "borderColor": "rgba(246, 194, 62, 1)",
                        "borderWidth": 1
                    }
                ]
            }
        except Exception as e:
            app.logger.error(f"Error procesando agendamiento: {str(e)}")
            return {"labels": [], "datasets": []}
            
    def procesar_consultorio_para_grafico(self, dict_especialidades):
        labels = []
        totales = []
        
        try:
            for fila in dict_especialidades:
                labels.append(fila['especialidad'][:15] + '..' if len(fila['especialidad']) > 15 else fila['especialidad'])
                totales.append(fila['cantidad'])
                
            return {
                "labels": labels,
                "datasets": [{
                    "label": "Consultas",
                    "data": totales,
                    "backgroundColor": [
                        "#0d6efd", "#3f3dc4", "#0f766e", "#d63384", "#dc3545",
                        "#fd7e14", "#ffc107", "#198754", "#20c997", "#0dcaf0"
                    ],
                    "borderWidth": 0
                }]
            }
        except Exception as e:
            app.logger.error(f"Error procesando consultorio: {str(e)}")
            return {"labels": [], "datasets": []}

    def _render_pdf(self, html_renderizado):
        """
        Convierte HTML a PDF usando WeasyPrint (preferido) o xhtml2pdf (fallback),
        mismo patrón que FacturaPDFService / FichaHtmlPdfService.
        """
        buffer = BytesIO()

        if WEASYPRINT_AVAILABLE:
            HTML(string=html_renderizado, base_url=app.config.get('SERVER_NAME', '')).write_pdf(buffer)
        else:
            pisa_status = pisa.CreatePDF(html_renderizado, dest=buffer, encoding='utf-8')
            if pisa_status.err:
                raise Exception(f"Error al generar PDF con xhtml2pdf: {pisa_status.err}")

        return buffer.getvalue()

    # ------------------------------------------------------------------
    # PDF de Reportes (PDF 4, paso 5). Las tres plantillas extienden pdf/base-reporte-pdf.html.
    # El servicio recibe los datos ya filtrados por el alcance de la sesión; no consulta ni decide permisos.
    # ------------------------------------------------------------------

    @staticmethod
    def _n(valor):
        return "{:,.0f}".format(float(valor or 0)).replace(',', '.')

    @staticmethod
    def _dec1(valor):
        return "{:,.1f}".format(float(valor or 0)).replace(',', '#').replace('.', ',').replace('#', '.')

    def _pct(self, valor):
        return f"{self._dec1(valor)} %"

    @staticmethod
    def _fecha(valor):
        """'AAAA-MM-DD' (o con hora) → 'dd/mm/aaaa'; '—' si no hay fecha."""
        partes = str(valor or '')[:10].split('-')
        return f"{partes[2]}/{partes[1]}/{partes[0]}" if len(partes) == 3 else '—'

    def _contexto_pdf(self, titulo, fecha_desde, fecha_hasta, alcance):
        """Datos comunes del encabezado y el pie, y los formateadores que usan las plantillas."""
        from datetime import datetime
        from flask import session
        from app.services.documento_clinico_pdf_service import DocumentoClinicoPdfService
        servicio_doc = DocumentoClinicoPdfService()
        return {
            'titulo': titulo, 'fecha_desde': fecha_desde, 'fecha_hasta': fecha_hasta, 'alcance': alcance,
            'empresa': servicio_doc.config_empresa(),
            'logo': servicio_doc._resolver_logo_base64(servicio_doc.BASE_PATH),
            'generado_por': session.get('nombre_persona') or session.get('usu_nick') or '—',
            'generado_en': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'n': self._n, 'dec1': self._dec1, 'pct': self._pct, 'fecha': self._fecha,
        }

    def _pdf(self, plantilla, contexto):
        from flask import render_template
        return self._render_pdf(render_template(plantilla, **contexto))

    def generar_pdf_agendamiento(self, fecha_desde, fecha_hasta, alcance, datos):
        """datos: totales, pacientes, por_especialista, diarios, ausentes, reiteradas, canceladas, detalle."""
        contexto = self._contexto_pdf('Reporte de Agendamiento', fecha_desde, fecha_hasta, alcance)
        contexto.update(datos)
        contexto['limite_detalle'] = 1000
        return self._pdf('pdf/reporte-agendamiento-pdf.html', contexto)

    def generar_pdf_consultorio(self, fecha_desde, fecha_hasta, alcance, datos, con_recibidas):
        """datos: totales, derivaciones, por_especialista, especialidades, top_diagnosticos, por_dia."""
        contexto = self._contexto_pdf('Reporte de Consultorio', fecha_desde, fecha_hasta, alcance)
        contexto.update(datos)
        contexto['con_recibidas'] = con_recibidas
        return self._pdf('pdf/reporte-consultorio-pdf.html', contexto)

    def generar_pdf_ventas(self, fecha_desde, fecha_hasta, condicion, alcance, detalle, por_dia, por_condicion,
                           cobrado, saldos):
        """
        detalle: getVentasDetalle; por_dia: getVentasReport; por_condicion: getVentasPorMetodoPago;
        cobrado: getCobradoPorMoneda; saldos: getSaldoCuentasPorMoneda. Una sección por moneda: nunca se suman
        monedas distintas, y las notas de crédito restan del total.
        """
        fm = self._formatear_moneda
        monedas = {}
        for d in detalle:
            cod, dec = d['cod_moneda'], d.get('decimales_moneda', 0)
            m = monedas.setdefault(cod, {'cod_moneda': cod, 'simbolo_moneda': d['simbolo_moneda'], 'dec': dec,
                                         'id_moneda': d['id_moneda'], 'comprobantes': 0, 'gravado': 0, 'iva': 0,
                                         'total': 0, 'nc_gravado': 0, 'nc_iva': 0, 'nc_total': 0})
            m['comprobantes'] += 1
            prefijo = 'nc_' if d.get('tipo_comprobante') == 'NOTA_CREDITO' else ''
            m[prefijo + 'gravado'] += d['gravado']
            m[prefijo + 'iva'] += d['iva']
            m[prefijo + 'total'] += d['total']
            d['gravado_formateado'] = fm(d['gravado'], dec)
            d['iva_formateado'] = fm(d['iva'], dec)
            d['total_formateado'] = fm(d['total'], dec)

        cobrado_por = {c['cod_moneda']: c['cobrado'] for c in cobrado}
        saldo_por = {s['cod_moneda']: s['monto_pendiente'] for s in saldos}
        lista = []
        for cod, m in sorted(monedas.items(), key=lambda x: x[1]['id_moneda']):
            dec = m['dec']
            condiciones = [dict(c, total_fmt=fm(c['total'], dec)) for c in por_condicion if c['cod_moneda'] == cod]
            total_cond = sum(c['total'] for c in condiciones)
            lista.append({
                'cod_moneda': cod, 'simbolo_moneda': m['simbolo_moneda'], 'comprobantes': m['comprobantes'],
                'gravado': fm(m['gravado'], dec), 'iva': fm(m['iva'], dec),
                'notas_credito': ('- ' + fm(m['nc_total'], dec)) if m['nc_total'] else fm(0, dec),
                'neto': fm(m['total'] - m['nc_total'], dec),
                'gravado_neto': fm(m['gravado'] - m['nc_gravado'], dec), 'iva_neto': fm(m['iva'] - m['nc_iva'], dec),
                'cobrado': fm(cobrado_por.get(cod, 0), dec), 'saldo': fm(saldo_por.get(cod, 0), dec),
                'condiciones': condiciones, 'total_condiciones': total_cond,
                'total_condiciones_fmt': fm(total_cond, dec),
                'dias': [dict(r, gravado_fmt=fm(r['total_gravado'], dec), iva_fmt=fm(r['total_iva'], dec),
                              total_fmt=fm(r['total_general'], dec))
                         for r in por_dia if r['cod_moneda'] == cod],
            })

        saldos_fmt = [dict(s, al_dia_fmt=fm(s['monto_pendiente'] - s['monto_vencido'], s['decimales_moneda']),
                           vencido_fmt=fm(s['monto_vencido'], s['decimales_moneda']),
                           pendiente_fmt=fm(s['monto_pendiente'], s['decimales_moneda'])) for s in saldos]

        contexto = self._contexto_pdf('Reporte de Ventas', fecha_desde, fecha_hasta, alcance)
        contexto.update({'condicion': condicion or 'Todos', 'monedas': lista, 'saldos': saldos_fmt, 'detalle': detalle})
        return self._pdf('pdf/reporte-ventas-pdf.html', contexto)

    def _formatear_moneda(self, valor, decimales=0):
        try:
            val = round(float(valor or 0), decimales)
            return "{:,.{}f}".format(val, decimales).replace(',', '#').replace('.', ',').replace('#', '.')
        except:
            return "0"
