from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime


class SifenXMLService:
    """
    Servicio para generar un XML de prueba del Documento Electrónico (DE) SIFEN.
    Esta versión es simplificada y pensada para pruebas internas, sin validación ante la SET.
    Más adelante se debe ajustar al XSD oficial de SIFEN.
    """

    def generar_xml_factura(self, factura_data, detalle_data, config_empresa):
        """
        Genera un XML representando una factura electrónica (DE) en formato simplificado.

        :param factura_data: dict con datos de la factura (número, fechas, receptor, montos, etc.)
        :param detalle_data: lista de dicts con items de la factura
        :param config_empresa: dict con datos del emisor (ruc, razón social, dirección, etc.)
        :return: bytes (XML en formato UTF-8)
        """
        # Nodo raíz (en SIFEN suele ser <rDE><DE>...</DE></rDE>, aquí simplificado)
        rde = Element("rDE")
        rde.set("xmlns", "http://www.set.gov.py/sifen/xsd")

        de = SubElement(rde, "DE")
        SubElement(de, "dVerFor").text = "150"  # versión ejemplo

        # gTimbre
        g_timbre = SubElement(de, "gTimb")
        SubElement(g_timbre, "iTiDE").text = "1"  # 1 = Factura electrónica (ejemplo)
        SubElement(g_timbre, "dNumTim").text = str(factura_data.get("numero_timbrado", "0"))
        SubElement(g_timbre, "dEst").text = "001"
        SubElement(g_timbre, "dPunExp").text = "001"
        SubElement(g_timbre, "dNumDoc").text = factura_data.get("factura_numero", "")
        SubElement(g_timbre, "dFeIniT").text = factura_data.get("fecha_inicio_vigencia", "")
        SubElement(g_timbre, "dFeFinT").text = factura_data.get("fecha_fin_vigencia", "")

        # gDatGralOpe
        g_dat_gral = SubElement(de, "gDatGralOpe")
        SubElement(g_dat_gral, "dFeEmiDE").text = factura_data.get("fecha_factura", datetime.now().strftime("%Y-%m-%d"))
        SubElement(g_dat_gral, "dMotEmi").text = factura_data.get("tipo_operacion", "VENTA DE MERCADERIA")
        SubElement(g_dat_gral, "iTiOpe").text = "1"  # 1 = Venta mercadería/servicio

        # gEmis (Emisor)
        g_emis = SubElement(de, "gEmis")
        SubElement(g_emis, "dRucEm").text = config_empresa.get("ruc", factura_data.get("ruc_emisor", "0000000"))
        SubElement(g_emis, "dNomEmi").text = config_empresa.get("nombre_empresa", "MI EMPRESA")
        SubElement(g_emis, "dDirEmi").text = config_empresa.get("direccion", "DIRECCION NO ESPECIFICADA")
        SubElement(g_emis, "dNumCas").text = "0"
        SubElement(g_emis, "dCompDir1").text = config_empresa.get("ciudad", "")
        SubElement(g_emis, "dTelEmi").text = config_empresa.get("telefono", "")
        SubElement(g_emis, "dEmailE").text = config_empresa.get("email", "")

        # gDatRec (Receptor)
        g_rec = SubElement(de, "gDatRec")
        SubElement(g_rec, "iNatRec").text = "1"  # 1 = Persona física
        SubElement(g_rec, "dRUCRec").text = factura_data.get("paciente_cedula", "0")
        SubElement(g_rec, "dNomRec").text = factura_data.get("paciente_nombre", "CONSUMIDOR FINAL")
        SubElement(g_rec, "dDirRec").text = factura_data.get("paciente_direccion", "")
        SubElement(g_rec, "dNumCasRec").text = "0"
        SubElement(g_rec, "dTelRec").text = factura_data.get("paciente_telefono", "")
        SubElement(g_rec, "dEmailRec").text = factura_data.get("paciente_email", "")

        # gCamItem - Detalle de items
        g_cam_fe = SubElement(de, "gCamFE")
        for idx, item in enumerate(detalle_data, start=1):
            g_item = SubElement(g_cam_fe, "gCamItem")
            SubElement(g_item, "dSeqItem").text = str(idx)
            SubElement(g_item, "cProd").text = item.get("item_codigo", f"ITEM{idx:03d}")
            SubElement(g_item, "dDesProSer").text = item.get("item_descripcion", "")
            SubElement(g_item, "dCantProSer").text = str(int(item.get("item_cantidad", 0) or 0))
            SubElement(g_item, "cUniMed").text = item.get("unidad_medida", "UNI")
            SubElement(g_item, "dPUniProSer").text = str(item.get("item_precio_unitario", 0))
            SubElement(g_item, "dTotBruOpeItem").text = str(item.get("item_total", 0))
            SubElement(g_item, "iAfecIVA").text = "1"  # 1 = Gravado IVA
            SubElement(g_item, "dTasaIVA").text = str(int(item.get("impuesto_porcentaje", 0) or 0))

        # gTotSub - Totales básicos (simples, para pruebas)
        g_tot = SubElement(de, "gTotSub")
        SubElement(g_tot, "dSubExe").text = str(factura_data.get("sub_exentas", 0))
        SubElement(g_tot, "dSub5").text = str(factura_data.get("sub_iva_5", 0))
        SubElement(g_tot, "dSub10").text = str(factura_data.get("sub_iva_10", 0))
        SubElement(g_tot, "dTotGralOpe").text = str(factura_data.get("factura_total", 0))

        # Convertir a XML string
        xml_bytes = tostring(rde, encoding="utf-8", method="xml")
        return xml_bytes




