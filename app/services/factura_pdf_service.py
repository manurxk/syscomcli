# app/services/factura_pdf_service.py

from io import BytesIO
from datetime import datetime
import qrcode
import os
import tempfile
import re
import base64
try:
    from weasyprint import HTML, CSS
    WEASYPRINT_AVAILABLE = True
except (ImportError, OSError) as e:
    # Captura tanto ImportError como OSError (error al cargar DLLs de GTK)
    WEASYPRINT_AVAILABLE = False
    print(f"WeasyPrint no disponible ({type(e).__name__}: {e}). Usando xhtml2pdf como alternativa.")
    from xhtml2pdf import pisa

class FacturaPDFService:
    """
    Servicio para generar PDFs de facturas con código QR.
    Ahora utiliza la plantilla HTML `FE.html` como base del KuDE
    y la convierte a PDF con xhtml2pdf.
    """
    
    def __init__(self):
        # Mantengo la firma del constructor por compatibilidad,
        # aunque ya no usamos los estilos de ReportLab.
        pass
    
    def _formatear_fecha(self, fecha_str):
        """Formatea fecha a DD/MM/YYYY"""
        try:
            if fecha_str and fecha_str != 'N/A':
                if 'T' in fecha_str:
                    fecha_obj = datetime.strptime(fecha_str.split('T')[0], '%Y-%m-%d')
                    return fecha_obj.strftime('%d/%m/%Y')
                elif '-' in fecha_str:
                    partes = fecha_str.split('-')
                    if len(partes[0]) == 4:  # YYYY-MM-DD
                        fecha_obj = datetime.strptime(fecha_str.split(' ')[0], '%Y-%m-%d')
                        return fecha_obj.strftime('%d/%m/%Y')
                    else:  # DD-MM-YYYY
                        return fecha_str.replace('-', '/')
                return fecha_str
        except:
            pass
        return fecha_str or 'N/A'
    
    def _generar_codigo_qr(self, datos_factura):
        """Genera el código QR para la factura según normativa SIFEN Paraguay"""
        cdc = datos_factura.get('codigo_sifen', '')
        
        if not cdc:
            ruc = datos_factura.get('ruc_emisor', '0000000-0').replace('-', '')
            numero = datos_factura.get('factura_numero', '').replace('-', '').replace(' ', '')
            fecha = datos_factura.get('fecha_factura', '').replace('-', '').replace('/', '')
            total = str(int(datos_factura.get('factura_total', 0)))
            cdc = f"{ruc}{numero}{fecha}{total}".ljust(44, '0')[:44]
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(cdc)
        qr.make(fit=True)
        
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_buffer = BytesIO()
        qr_img.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        return qr_buffer, cdc
    
    def _formatear_moneda(self, valor):
        """Formatea un valor numérico como moneda paraguaya"""
        try:
            if valor is None:
                return "0"
            valor_float = float(valor)
            return f"{int(valor_float):,}".replace(',', '.')
        except (ValueError, TypeError):
            return "0"
    
    def _get_image_base64(self, image_path):
        """Convierte una imagen a base64 para usar en PDF"""
        try:
            if image_path and os.path.exists(image_path):
                with open(image_path, 'rb') as img_file:
                    return base64.b64encode(img_file.read()).decode('utf-8')
        except Exception as e:
            # Usar print si no hay logger disponible
            print(f"Error al leer imagen {image_path}: {str(e)}")
        return None
    
    def _calcular_valor_venta_por_tasa(self, detalle_data):
        """
        Suma el VALOR DE VENTA (monto con IVA incluido) por tasa:
        - exentas
        - gravadas al 5%
        - gravadas al 10%

        Usamos item_total (monto con IVA). Si no existe, caemos a item_subtotal.
        """
        total_exentas = 0
        total_5 = 0
        total_10 = 0

        # Validar que detalle_data sea iterable
        if not detalle_data or not isinstance(detalle_data, (list, tuple)):
            return total_exentas, total_5, total_10

        for item in detalle_data:
            # Validar que item sea un diccionario
            if not isinstance(item, dict):
                continue
            try:
                porcentaje = float(item.get('impuesto_porcentaje', 0) or 0)
                total_item = item.get('item_total')
                if total_item is None:
                    # fallback: si no hay total, usar subtotal
                    total_item = item.get('item_subtotal', 0) or 0
                total_item = float(total_item or 0)

                if porcentaje == 5:
                    total_5 += total_item
                elif porcentaje == 10:
                    total_10 += total_item
                else:
                    total_exentas += total_item
            except (ValueError, TypeError):
                continue

        return total_exentas, total_5, total_10
    
    def generar_factura_pdf(self, factura_data, detalle_data=None, config_empresa=None):
        """
        Genera un PDF de la factura usando la plantilla HTML FE.html
        """
        # Normalizar estructuras
        factura_data = factura_data or {}
        # Asegurar que detalle_data sea una lista válida
        try:
            if detalle_data is None:
                detalle_data = []
            elif not isinstance(detalle_data, (list, tuple)):
                # Intentar convertir a lista si es iterable
                try:
                    iter(detalle_data)  # Verificar si es iterable
                    detalle_data = list(detalle_data)
                except (TypeError, ValueError):
                    detalle_data = []
        except (TypeError, AttributeError):
            detalle_data = []
        empresa = config_empresa or {}

        # --------------------------------------------
        # 1) Cargar plantilla FE.html
        # --------------------------------------------
        base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        template_path = os.path.join(base_path, 'FE.html')

        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()

        # --------------------------------------------
        # 2) Preparar datos de emisor y factura
        # --------------------------------------------
        direccion_emisor = empresa.get('direccion', 'Dirección no especificada')
        ciudad_emisor = empresa.get('ciudad', 'Ciudad no especificada')
        telefono_emisor = empresa.get('telefono', '')
        email_emisor = empresa.get('email', '')
        actividad_economica = empresa.get('actividad_economica', '')
        ruc_emisor = empresa.get('ruc', factura_data.get('ruc_emisor', '0000000-0'))

        # Logo - usar primero el logo guardado en BD, luego fallback a estáticos
        path_logo = ''
        logo_base64 = ''

        # 1) Logo desde config_empresa (subido por el Superadmin)
        if empresa.get('logo_path'):
            logo_rel = empresa['logo_path']  # Ej: "uploads/logos/logo_1_abc.png"
            logo_abs = os.path.join(base_path, 'app', 'static', logo_rel)
            if os.path.exists(logo_abs):
                path_logo = logo_abs
                logo_base64 = self._get_image_base64(logo_abs)

        # 2) Fallback a logos estáticos del proyecto
        if not logo_base64:
            posibles_logos = [
                os.path.join(base_path, 'app', 'static', 'img', 'logo_clinica.png'),
                os.path.join(base_path, 'app', 'static', 'img', 'iconoazul.png'),
                os.path.join(base_path, 'app', 'static', 'img', 'logo.png'),
                os.path.join(base_path, 'static', 'img', 'logo_clinica.png'),
            ]
            for p in posibles_logos:
                if os.path.exists(p):
                    path_logo = p
                    logo_base64 = self._get_image_base64(p)
                    break

        # Fechas
        fecha_emision = self._formatear_fecha(factura_data.get('fecha_factura', ''))
        try:
            fecha_completa = str(factura_data.get('fecha_factura', ''))
            if 'T' in fecha_completa:
                hora_emision = fecha_completa.split('T')[1].split('.')[0]
            else:
                hora_emision = datetime.now().strftime('%H:%M:%S')
        except Exception:
            hora_emision = datetime.now().strftime('%H:%M:%S')

        # Condición de venta
        condicion_venta = str(factura_data.get('condicion_venta', 'Contado')).lower()
        marcado_contado = 'X' if 'contado' in condicion_venta else ''
        marcado_credito = 'X' if 'credito' in condicion_venta or 'crédito' in condicion_venta else ''

        moneda = factura_data.get('moneda', 'PYG')
        # Estos totales se recalcularán desde el detalle para asegurar consistencia
        subtotal = 0
        total = 0

        # Calcular valor de venta por tasa (con IVA incluido) y extraer IVA contenido
        if detalle_data:
            exentas_total, vta_5_total, vta_10_total = self._calcular_valor_venta_por_tasa(detalle_data)
            
            # Asegurar que los valores sean numéricos, no None
            exentas_total = float(exentas_total or 0)
            vta_5_total = float(vta_5_total or 0)
            vta_10_total = float(vta_10_total or 0)

            # IVA incluido en el precio:
            #   - Para 10%: IVA = total / 11
            #   - Para 5% : IVA = total / 21
            iva_5_monto = int(vta_5_total / 21) if vta_5_total > 0 else 0
            iva_10_monto = int(vta_10_total / 11) if vta_10_total > 0 else 0
            total_iva = iva_5_monto + iva_10_monto

            subtotal = exentas_total + vta_5_total + vta_10_total
            total = subtotal  # total operación = suma de valores de venta (precio con IVA)
        else:
            exentas_total = 0
            vta_5_total = 0
            vta_10_total = 0
            iva_5_monto = 0
            iva_10_monto = 0
            total_iva = 0
            subtotal = 0
            total = 0

        # --------------------------------------------
        # 3) Construir filas HTML del detalle - CORREGIDO
        # --------------------------------------------
        filas_html = []
        # Validar que detalle_data sea iterable antes de iterar
        if detalle_data and isinstance(detalle_data, (list, tuple)):
            for idx, item in enumerate(detalle_data):
                # Validar que item sea un diccionario
                if not isinstance(item, dict):
                    continue
                    
                codigo = item.get('item_codigo', f'ITEM{idx+1:03d}') or ''
                descripcion = item.get('item_descripcion', '') or ''
                unidad = item.get('unidad_medida', 'UNI') or 'UNI'
                cantidad = int(item.get('item_cantidad', 0) or 0)
                
                # Precio unitario mostrado debe ser CON IVA (total / cantidad)
                total_item = float(item.get('item_total', 0) or 0)
                precio_unit_num = 0.0
                if cantidad > 0 and total_item > 0:
                    precio_unit_num = total_item / cantidad
                precio_unit = self._formatear_moneda(precio_unit_num)
                
                descuento_val = float(item.get('item_descuento', 0) or 0)
                descuento = self._formatear_moneda(descuento_val)
                subtotal_item = total_item  # valor de venta (con IVA) para mostrar en columnas
                porcentaje_iva = float(item.get('impuesto_porcentaje', 0) or 0)

                valor_exentas = ''
                valor_5 = ''
                valor_10 = ''
                if porcentaje_iva == 5:
                    valor_5 = self._formatear_moneda(subtotal_item)
                elif porcentaje_iva == 10:
                    valor_10 = self._formatear_moneda(subtotal_item)
                else:
                    valor_exentas = self._formatear_moneda(subtotal_item)

                # Asegurar que NUNCA haya valores None o vacíos - todos deben ser strings válidos
                codigo = str(codigo) if codigo else ''
                descripcion = str(descripcion) if descripcion else ''
                unidad = str(unidad) if unidad else 'UNI'
                cantidad_str = str(int(cantidad)) if cantidad is not None and cantidad >= 0 else '0'
                precio_unit = str(precio_unit) if precio_unit else '0'
                descuento = str(descuento) if descuento else '0'
                valor_exentas = str(valor_exentas) if valor_exentas else ''
                valor_5 = str(valor_5) if valor_5 else ''
                valor_10 = str(valor_10) if valor_10 else ''
                
                # Escapar HTML para evitar problemas
                codigo = codigo.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                descripcion = descripcion.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                unidad = unidad.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
                
                # IMPORTANTE: Asegurar que todas las celdas tengan contenido (al menos un espacio)
                # xhtml2pdf tiene problemas con celdas completamente vacías
                codigo_final = codigo if codigo else ' '
                descripcion_final = descripcion if descripcion else ' '
                unidad_final = unidad if unidad else 'UNI'
                
                # IMPORTANTE: Usar estilos inline mínimos y asegurar padding
                filas_html.append(
                    f'<tr style="font-size: 7pt;">'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: center;">{codigo_final}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px;">{descripcion_final}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: center;">{unidad_final}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{cantidad_str}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{precio_unit}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{descuento}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{valor_exentas if valor_exentas else " "}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{valor_5 if valor_5 else " "}</td>'
                    f'<td style="border: 1px solid #040303; padding: 4px; text-align: right;">{valor_10 if valor_10 else " "}</td>'
                    f'</tr>'
                )

        # Agregar filas vacías para llenar la página (mínimo 5 filas)
        filas_actuales = len(filas_html)
        filas_minimas = 5

        if filas_actuales < filas_minimas:
            for _ in range(filas_minimas - filas_actuales):
                filas_html.append(
                    '<tr style="font-size: 7pt;">'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                    '</tr>'
                )

        # Si no hay items, mostrar mensaje
        if not filas_html:
            filas_html = [
                '<tr style="font-size: 7pt;">'
                '<td style="border: 1px solid #040303; padding: 4px;"> </td>'
                '<td colspan="8" style="border: 1px solid #040303; padding: 10px; text-align: center;">No hay items en esta factura</td>'
                '</tr>'
            ]

        detalle_html = "\n".join(filas_html)

        # --------------------------------------------
        # 4) QR - Espacio reservado (no se genera, se usará el CDC de SIFEN más adelante)
        # --------------------------------------------
        # El QR se generará más adelante con el CDC de SIFEN
        # Por ahora dejamos un espacio reservado vacío
        cdc = factura_data.get('codigo_sifen', '')

        # --------------------------------------------
        # 5) Reemplazos de marcadores de FE.html
        # --------------------------------------------
        reemplazos = {
            '#!#pathLogo#!#': f"data:image/png;base64,{logo_base64}" if logo_base64 else '',
            '#!#dDirEmi#!#': direccion_emisor,
            '#!#dDesCiuEmi#!#': ciudad_emisor,
            '#!#dTelEmi#!#': telefono_emisor,
            '#!#dMailEmi#!#': email_emisor,
            '#!#dDesActEco#!#': actividad_economica,
            '#!#dRucEm#!#': ruc_emisor,
            '#!#dNumTim#!#': factura_data.get('numero_timbrado', 'N/A'),
            '#!#dFeIniT#!#': self._formatear_fecha(factura_data.get('fecha_inicio_vigencia', '')),
            '#!#dNumDoc#!#': factura_data.get('factura_numero', ''),
            '#!#dSerieDoc#!#': '',
            '#!#fEmiDE#!#': f"{fecha_emision} {hora_emision}",
            '#!#dRucRec#!#': factura_data.get('paciente_cedula', ''),
            '#!#contado#!#': marcado_contado,
            '#!#credito#!#': marcado_credito,
            '#!#dNomRec#!#': factura_data.get('paciente_nombre', ''),
            '#!#dNcuotas#!#': '',
            '#!#dDirRec#!#': factura_data.get('paciente_direccion', ''),
            '#!#dDmonOpe#!#': moneda,
            '#!#dTelRec#!#': factura_data.get('paciente_telefono', ''),
            '#!#dCambio#!#': '',
            '#!#dEmailRec#!#': factura_data.get('paciente_email', ''),
            '#!#dNroDocAsoc#!#': '',
            '#!#dDesTiTran#!#': factura_data.get('tipo_operacion', 'Venta de Mercadería'),
            '#!#dDocAsociados#!#': '',
            '#!#DetailTablePapel#!#': detalle_html,
            '#!#dSubExe#!#': self._formatear_moneda(exentas_total),
            '#!#dSubVta5#!#': self._formatear_moneda(vta_5_total),
            '#!#dSubVta10#!#': self._formatear_moneda(vta_10_total),
            '#!#dMontoLetras#!#': factura_data.get('factura_total_letras', ''),
            '#!#dTotOpe#!#': self._formatear_moneda(total),
            '#!#dLIva5#!#': self._formatear_moneda(iva_5_monto),
            '#!#dLiva10#!#': self._formatear_moneda(iva_10_monto),
            '#!#dLtotIva#!#': self._formatear_moneda(total_iva),
            '#!#qrPath#!#': f"data:image/png;base64,{factura_data.get('qr_base64')}" if factura_data.get('qr_base64') else '',
            '#!#CDC#!#': cdc or factura_data.get('codigo_sifen', ''),
        }

        for marcador, valor in reemplazos.items():
            html = html.replace(marcador, str(valor) if valor is not None else '')
        
        # Workaround para bug de xhtml2pdf con tablas complejas - CORREGIDO
        # Remover estilos problemáticos del tbody
        html = re.sub(r'<tbody[^>]*style="[^"]*min-height[^"]*"[^>]*>', '<tbody style="font-size: 7pt;">', html)
        html = re.sub(r'<tbody[^>]*style="[^"]*height:[^"]*"[^>]*>', '<tbody style="font-size: 7pt;">', html)

        # CRÍTICO: Remover el atributo style problemático del tbody en el HTML
        # que causa el error de NoneType
        html = html.replace(
            '<tbody style="font-size: 11pt; min-height: 9.5cm;height:16px;">',
            '<tbody style="font-size: 7pt;">'
        )
        
        # Si estamos usando xhtml2pdf, simplificar estilos
        if not WEASYPRINT_AVAILABLE:
            # Asegurar que imágenes base64 esten contenidas para xhtml2pdf si es necesario
            # Simplificar alturas fijas en la tabla y otras celdas de la tabla del QR
            html = re.sub(
                r'style="[^"]*height:\s*5cm[^"]*"',
                'style="vertical-align: top;"',
                html,
                flags=re.IGNORECASE
            )
            # Simplificar altura fija en la tabla completa
            html = re.sub(
                r'<table\s+style="[^"]*height:\s*5cm[^"]*"',
                '<table style="border: 1px solid #040303; width: 100%; font-size: 8pt;"',
                html,
                flags=re.IGNORECASE
            )
            html = re.sub(
                r'<table\s+style="[^"]*max-height:\s*5cm[^"]*"',
                '<table style="border: 1px solid #040303; width: 100%; font-size: 8pt;"',
                html,
                flags=re.IGNORECASE
            )

        # --------------------------------------------
        # 6) HTML → PDF usando WeasyPrint (preferido) o xhtml2pdf (fallback)
        # --------------------------------------------
        buffer = BytesIO()
        
        if WEASYPRINT_AVAILABLE:
            # Usar WeasyPrint - mejor soporte para HTML/CSS y tablas complejas
            try:
                html_doc = HTML(string=html, base_url=base_path)
                html_doc.write_pdf(buffer)
            except Exception as e:
                error_msg = f"Error al generar PDF con WeasyPrint: {str(e)}"
                print(f"Error detallado: {error_msg}")
                raise Exception(error_msg)
        else:
            # Fallback a xhtml2pdf si WeasyPrint no está disponible
            try:
                pisa_status = pisa.CreatePDF(
                    html,
                    dest=buffer,
                    encoding='utf-8',
                    link_callback=None
                )
                
                if pisa_status.err:
                    error_msg = f"Error en generación PDF: {pisa_status.err}"
                    print(f"Error detallado: {error_msg}")
                    raise Exception(error_msg)
            except Exception as e:
                error_msg = f"Error al generar PDF: {str(e)}"
                print(f"Error detallado: {error_msg}")
                raise Exception(error_msg)
        
        buffer.seek(0)
        return buffer
    
    def generar_preview_factura(self, datos_formulario, items, config_empresa=None):
        """Genera un PDF de preview de la factura antes de guardarla"""
        factura_preview = {
            'factura_numero': datos_formulario.get('factura_numero', 'PREVIEW'),
            'fecha_factura': datos_formulario.get('fecha_factura', datetime.now().strftime('%Y-%m-%d')),
            'codigo_sifen': datos_formulario.get('codigo_sifen', ''),
            'numero_timbrado': datos_formulario.get('numero_timbrado', ''),
            'fecha_inicio_vigencia': datos_formulario.get('fecha_inicio_vigencia', '01/01/2024'),
            'fecha_fin_vigencia': datos_formulario.get('fecha_fin_vigencia', '31/12/2024'),
            'paciente_nombre': datos_formulario.get('paciente_nombre', ''),
            'paciente_cedula': datos_formulario.get('paciente_cedula', ''),
            'paciente_direccion': datos_formulario.get('paciente_direccion', ''),
            'paciente_telefono': datos_formulario.get('paciente_telefono', ''),
            'paciente_email': datos_formulario.get('paciente_email', ''),
            'condicion_venta': datos_formulario.get('condicion_venta', 'Contado'),
            'moneda': datos_formulario.get('moneda', 'PYG'),
            'tipo_operacion': datos_formulario.get('tipo_operacion', 'Venta de Mercadería'),
            'factura_subtotal': datos_formulario.get('factura_subtotal', 0),
            'factura_impuestos': datos_formulario.get('factura_impuestos', 0),
            'factura_descuento': datos_formulario.get('factura_descuento', 0),
            'factura_total': datos_formulario.get('factura_total', 0),
            'ruc_emisor': datos_formulario.get('ruc_emisor', '0000000-0')
        }
        
        return self.generar_factura_pdf(factura_preview, items, config_empresa)