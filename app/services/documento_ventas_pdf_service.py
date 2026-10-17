# app/services/documento_ventas_pdf_service.py

from app.core.moneda import formatear, get_moneda
from app.dao.ventas.movimientos.factura.FacturaDao import numero_a_letras
from app.services.documento_clinico_pdf_service import DocumentoClinicoPdfService


class DocumentoVentasPdfService(DocumentoClinicoPdfService):
    """
    PDF de los documentos de Ventas sin valor fiscal: nota de remisión (REMISION.html) y
    presupuesto (PRESUPUESTO.html). Las NC/ND son KuDE y salen de FacturaPDFService.

    Mismo patrón que los documentos clínicos: plantilla en la carpeta templates del módulo,
    marcadores #!#...#!# con datos ya escapados; reutiliza el encabezado, el bloque del paciente,
    el logo y el motor de PDF de DocumentoClinicoPdfService.
    """

    MODULO = 'ventas'
    PLANTILLAS = {
        'remision': ('remision', 'REMISION.html'),
        'presupuesto': ('presupuesto', 'PRESUPUESTO.html'),
    }

    @staticmethod
    def _monto(valor, moneda):
        """Monto sin símbolo, con los separadores de la moneda (150.000 / 1,234.50)."""
        return formatear(valor or 0, moneda).split(' ', 1)[1]

    def generar_remision_pdf(self, remision, detalle, paciente, empresa):
        """remision: RemisionDao.getRemisionById; detalle: getRemisionDetalle; paciente: FichaDao.getDatosPaciente."""
        asociados = []
        if remision.get('factura_numero'):
            asociados.append(f"Factura {self._fv(remision['factura_numero'])}")
        if remision.get('pedido_numero'):
            asociados.append(f"Pedido {self._fv(remision['pedido_numero'])}")
        items = ''
        for i, d in enumerate(detalle or [], 1):
            cantidad = d.get('item_cantidad')
            cantidad = f"{float(cantidad):g}" if cantidad is not None else ''
            if d.get('item_unidad'):
                cantidad += f" {d['item_unidad']}"
            items += (f'<tr><td style="text-align: center; width: 6%;">{i}</td>'
                      f'<td>{self._fv(d.get("item_descripcion") or d.get("des_item_servicio"))}</td>'
                      f'<td style="text-align: center; width: 12%;">{self._fv(cantidad)}</td>'
                      f'<td style="width: 22%;">{self._fv(d.get("observaciones"), "")}</td></tr>')
        reemplazos = self._reemplazos_comunes(remision.get('remision_numero'),
                                              self._fecha(remision.get('fecha_remision')), empresa, paciente, {})
        reemplazos.update({
            '#!#DOC_ASOCIADO#!#': ' · '.join(asociados) or '—',
            '#!#FECHA_ENTREGA#!#': self._corta(self._fecha(remision.get('fecha_entrega'))),
            '#!#ESTADO#!#': self._fv(remision.get('est_remision')),
            '#!#ITEMS#!#': items,
            '#!#OBSERVACIONES#!#': self._fv(remision.get('observaciones')),
        })
        return self._render('remision', reemplazos)

    def generar_presupuesto_pdf(self, presupuesto, paciente, firmante, empresa):
        """
        presupuesto: PresupuestoDao.getPresupuestoById (con 'detalles').
        firmante: FichaDao.getDatosGenerador del especialista (el del PEI si es plan de tratamiento,
        si no el profesional del presupuesto cuando es especialista) o {} si no hay.
        Con id_pei sale como presupuesto de plan de tratamiento, solo con la referencia del PEI.
        """
        moneda = get_moneda(presupuesto.get('id_moneda'))
        es_plan = bool(presupuesto.get('id_pei'))
        profesional = (presupuesto.get('profesional_nombre') or '').strip()  # CONCAT de NULL da ' '
        detalles = presupuesto.get('detalles') or []
        con_descuento = any(float(d.get('item_descuento') or 0) for d in detalles)

        filas = ('<tr><th>Nº</th><th>Servicio</th><th>Cant.</th><th>Precio unit.</th>'
                 + ('<th>Desc.</th>' if con_descuento else '') + '<th>Subtotal</th></tr>')
        for i, d in enumerate(detalles, 1):
            filas += (f'<tr><td style="text-align: center; width: 6%;">{i}</td>'
                      f'<td>{self._fv(d.get("item_descripcion"))}</td>'
                      f'<td style="text-align: center; width: 9%;">{float(d.get("item_cantidad") or 0):g}</td>'
                      f'<td class="num" style="width: 15%;">{self._monto(d.get("item_precio_unitario"), moneda)}</td>'
                      + (f'<td class="num" style="width: 12%;">{self._monto(d.get("item_descuento"), moneda)}</td>'
                         if con_descuento else '')
                      + f'<td class="num" style="width: 15%;">{self._monto(d.get("item_subtotal"), moneda)}</td></tr>')

        total = presupuesto.get('presupuesto_total') or 0
        try:
            letras = numero_a_letras(total, moneda)
        except ValueError:
            letras = formatear(total, moneda)
        fecha = self._fecha(presupuesto.get('fecha_presupuesto'))
        validez = self._fecha(presupuesto.get('fecha_validez'))

        bloque_plan = bloque_pago = ''
        if es_plan:
            bloque_plan = f"""
  <div class="seccion">Plan de tratamiento</div>
  <table class="tabla-datos">
    <tr>
      <td style="width: 34%;"><span class="lbl">Plan individual (PEI)</span>Versión {self._fv(presupuesto.get('pei_nro_version'))} · {self._fv(presupuesto.get('pei_estado'))}</td>
      <td style="width: 66%;"><span class="lbl">Especialista a cargo</span>{self._fv(firmante.get('nombre_completo'))}</td>
    </tr>
    <tr><td colspan="2"><span class="lbl">Cronograma de seguimiento</span><span class="texto-largo">{self._fv(presupuesto.get('pei_cronograma_seguimiento'))}</span></td></tr>
  </table>"""
            bloque_pago = f"""
  <div class="seccion no-cortar" style="margin-top: 8px;">Formas de pago</div>
  <table class="tabla-datos">
    <tr>
      <td style="width: 33%;"><span class="lbl">Contado (plan completo)</span>{formatear(total, moneda)}</td>
      <td style="width: 34%;"><span class="lbl">Crédito</span>En cuotas, según las condiciones de caja</td>
      <td style="width: 33%;"><span class="lbl">Por sesión</span>Según precio vigente de cada servicio</td>
    </tr>
  </table>
  <table class="tabla-datos" style="margin-top: 6px;">
    <tr><td><span class="lbl">Condiciones</span>La cantidad de sesiones es estimada: si el plan cambia se emite una nueva versión del PEI y un nuevo presupuesto. Las sesiones no realizadas sin aviso con 24 h de anticipación se consideran realizadas.{f' Válido hasta el {self._corta(validez)}.' if validez else ''}</td></tr>
  </table>"""

        observaciones = ''
        if presupuesto.get('observaciones'):
            observaciones = (f'<table class="tabla-datos" style="margin-top: 6px;"><tr><td><span class="lbl">Observaciones</span>'
                             f'<span class="texto-largo">{self._fv(presupuesto["observaciones"])}</span></td></tr></table>')

        if firmante:
            firma_nombre = self._fv(firmante.get('nombre_completo'))
            firma_detalle = f"Matrícula Nº {self._fv(firmante.get('matricula'))}"
        elif profesional:
            firma_nombre, firma_detalle = self._fv(profesional), 'Profesional'
        else:
            firma_nombre, firma_detalle = self._fv(empresa.get('nombre'), 'SYSCLIN'), 'Por la clínica'

        dias = (validez - fecha).days if validez and fecha else None
        reemplazos = self._reemplazos_comunes(presupuesto.get('presupuesto_numero'), fecha, empresa, paciente, {})
        reemplazos.update({
            '#!#PIE#!#': 'Presupuesto de plan de tratamiento' if es_plan else 'Presupuesto',
            '#!#SUBTITULO#!#': ('Presupuesto de tratamiento · Documento confidencial' if es_plan
                                else 'Presupuesto · Documento sin valor fiscal'),
            '#!#TITULO#!#': 'PRESUPUESTO DE<br>PLAN DE TRATAMIENTO' if es_plan else 'PRESUPUESTO',
            '#!#PROFESIONAL#!#': self._fv(profesional),
            '#!#MONEDA#!#': self._fv(f"{moneda.get('des_moneda', '').title()} ({moneda.get('cod_moneda')})"),
            '#!#VALIDO_HASTA#!#': self._corta(validez),
            '#!#ESTADO#!#': self._fv(presupuesto.get('presupuesto_estado')),
            '#!#BLOQUE_PLAN#!#': bloque_plan,
            '#!#TITULO_DETALLE#!#': 'Servicios presupuestados' if es_plan else 'Detalle',
            '#!#ITEMS#!#': filas,
            '#!#SUBTOTAL#!#': self._monto(presupuesto.get('presupuesto_subtotal'), moneda),
            '#!#DESCUENTO#!#': self._monto(presupuesto.get('presupuesto_descuento'), moneda),
            '#!#SIMBOLO#!#': self._fv(moneda.get('simbolo_moneda') or moneda.get('cod_moneda')),
            '#!#TOTAL#!#': self._monto(total, moneda),
            '#!#TOTAL_LETRAS#!#': self._fv(letras),
            '#!#BLOQUE_PAGO#!#': bloque_pago,
            '#!#FILA_OBSERVACIONES#!#': observaciones,
            '#!#FIRMA_NOMBRE#!#': firma_nombre,
            '#!#FIRMA_DETALLE#!#': firma_detalle,
            '#!#FIRMA_ACEPTA#!#': ('Conformidad del paciente o responsable' if es_plan
                                   else 'Aceptación del paciente o responsable'),
            '#!#CONFIDENCIAL#!#': ('Documento con datos de salud del paciente. Prohibida su reproducción o '
                                   'divulgación sin autorización.' if es_plan else
                                   (f'Presupuesto válido por {dias} días. ' if dias else '')
                                   + 'No constituye comprobante de venta.'),
        })
        return self._render('presupuesto', reemplazos)
