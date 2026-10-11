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
                        "#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545",
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

    def generar_pdf_ventas(self, fecha_desde, fecha_hasta, metodo_pago, datos, totales):
        """
        Genera el PDF del reporte de ventas.
        """
        from flask import render_template

        # `totales` es una lista (un total por moneda presente en el periodo)
        totales_formateados = []
        for t in totales:
            dec = t.get('decimales_moneda', 0)
            tf = dict(t)
            tf['total_gravado_formateado'] = self._formatear_moneda(t.get('total_gravado', 0), dec)
            tf['total_iva_formateado'] = self._formatear_moneda(t.get('total_iva', 0), dec)
            tf['total_general_formateado'] = self._formatear_moneda(t.get('total_general', 0), dec)
            totales_formateados.append(tf)

        for d in datos:
            dec = d.get('decimales_moneda', 0)
            d['gravado_formateado'] = self._formatear_moneda(d.get('gravado', 0), dec)
            d['iva_formateado'] = self._formatear_moneda(d.get('iva', 0), dec)
            d['total_formateado'] = self._formatear_moneda(d.get('total', 0), dec)

        html_renderizado = render_template(
            'pdf/reporte-ventas-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            metodo_pago=metodo_pago or 'Todos',
            datos=datos,
            totales=totales_formateados
        )

        return self._render_pdf(html_renderizado)

    def generar_pdf_agendamiento(self, fecha_desde, fecha_hasta, datos_diarios, totales):
        """
        Genera el PDF del reporte de agendamiento.
        """
        from flask import render_template

        html_renderizado = render_template(
            'pdf/reporte-agendamiento-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            datos=datos_diarios,
            totales=totales
        )

        return self._render_pdf(html_renderizado)

    def generar_pdf_consultorio(self, fecha_desde, fecha_hasta, especialidades, totales):
        """
        Genera el PDF del reporte de consultorio.
        """
        from flask import render_template

        html_renderizado = render_template(
            'pdf/reporte-consultorio-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            especialidades=especialidades,
            totales=totales
        )

        return self._render_pdf(html_renderizado)

    def _formatear_moneda(self, valor, decimales=0):
        try:
            val = round(float(valor or 0), decimales)
            return "{:,.{}f}".format(val, decimales).replace(',', '#').replace('.', ',').replace('#', '.')
        except:
            return "0"
