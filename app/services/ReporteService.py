from flask import current_app as app

class ReporteService:
    """
    Servicio de Reportes para procesar info del DAO hacia las vistas y Chart.js.
    Fase 1: Implementado el procesado de ventas para UI.
    """

    def procesar_ventas_para_grafico(self, data):
        """
        Transforma la lista de diccionarios del DAO en el formato JSON 
        que Chart.js espera.
        """
        labels = []
        totales = []
        
        try:
            for fila in data:
                # Se asume que date_str viene en formato 'YYYY-MM-DD' desde el DAO
                # Se podría formatear aquí a 'DD/MM/YYYY' para Chart.js
                fecha_parts = fila['fecha'].split('-')
                if len(fecha_parts) == 3:
                    fecha_esf = f"{fecha_parts[2]}/{fecha_parts[1]}/{fecha_parts[0]}"
                else:
                    fecha_esf = fila['fecha']
                    
                labels.append(fecha_esf)
                totales.append(fila['total_general'])
                
            return {
                "labels": labels,
                "datasets": [{
                    "label": "Total Ventas (₲)",
                    "data": totales,
                    "backgroundColor": "rgba(13, 110, 253, 0.5)",
                    "borderColor": "rgba(13, 110, 253, 1)",
                    "borderWidth": 1
                }]
            }
        except Exception as e:
            app.logger.error(f"Error procesando ventas para gráfico: {str(e)}")
            return {"labels": [], "datasets": []}

    def calcular_totales_ventas(self, data):
        """
        Calcula la sumatoria general para las KPIs de la UI del reporte.
        """
        totales = {
            'cantidad_comprobantes': 0,
            'total_gravado': 0,
            'total_iva': 0,
            'total_general': 0
        }
        
        try:
            for fila in data:
                totales['cantidad_comprobantes'] += fila.get('cantidad_comprobantes', 0)
                totales['total_gravado'] += fila.get('total_gravado', 0)
                totales['total_iva'] += fila.get('total_iva', 0)
                totales['total_general'] += fila.get('total_general', 0)
        except Exception as e:
            app.logger.error(f"Error calculando subtotales de ventas: {str(e)}")
            
        return totales

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

    def generar_pdf_ventas(self, fecha_desde, fecha_hasta, metodo_pago, datos, totales):
        """
        Genera el PDF del reporte de ventas usando WeasyPrint.
        """
        from flask import render_template
        from weasyprint import HTML
        
        # Format the numbers for the template
        totales_formateados = {k: self._formatear_moneda(v) for k, v in totales.items()}
        
        for d in datos:
            d['gravado_formateado'] = self._formatear_moneda(d.get('gravado', 0))
            d['iva_formateado'] = self._formatear_moneda(d.get('iva', 0))
            d['total_formateado'] = self._formatear_moneda(d.get('total', 0))
        
        html_renderizado = render_template(
            'pdf/reporte-ventas-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            metodo_pago=metodo_pago or 'Todos',
            datos=datos,
            totales=totales_formateados
        )
        
        # Generar PDF en memoria
        pdf_bytes = HTML(string=html_renderizado, base_url=app.config.get('SERVER_NAME', '')).write_pdf()
        return pdf_bytes

    def generar_pdf_agendamiento(self, fecha_desde, fecha_hasta, datos_diarios, totales):
        """
        Genera el PDF del reporte de agendamiento.
        """
        from flask import render_template
        from weasyprint import HTML
        
        html_renderizado = render_template(
            'pdf/reporte-agendamiento-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            datos=datos_diarios,
            totales=totales
        )
        
        pdf_bytes = HTML(string=html_renderizado).write_pdf()
        return pdf_bytes

    def generar_pdf_consultorio(self, fecha_desde, fecha_hasta, especialidades, totales):
        """
        Genera el PDF del reporte de consultorio.
        """
        from flask import render_template
        from weasyprint import HTML
        
        html_renderizado = render_template(
            'pdf/reporte-consultorio-pdf.html',
            fecha_desde=fecha_desde,
            fecha_hasta=fecha_hasta,
            especialidades=especialidades,
            totales=totales
        )
        
        pdf_bytes = HTML(string=html_renderizado).write_pdf()
        return pdf_bytes
    
    def _formatear_moneda(self, valor):
        try:
            val = int(valor or 0)
            return "{:,.0f}".format(val).replace(',', '.')
        except:
            return "0"
