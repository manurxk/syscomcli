from xml.etree.ElementTree import Element, SubElement, tostring
from datetime import datetime

class SifenXMLService:
    """
    Servicio para generar el XML del Documento Electrónico (DE) SIFEN
    conforme al esquema XSD v150 oficial.
    """

    def generar_xml_v150(self, factura_data: dict, detalle_data: list, config_emis: object, cdc: str) -> bytes:
        """
        Genera el XML v150 válido.
        :param factura_data: Datos de la factura
        :param detalle_data: Lista de items
        :param config_emis: Instancia de SifenEmisionConfig con los datos de emisión.
        :param cdc: Código de Control generado previamente por sifen_cdc_utils.
        """
        # Namespace oficial
        rde = Element("rDE", {"xmlns": "http://ekuatia.set.gov.py/sifen/xsd"})
        
        # Nodo DE principal
        de = SubElement(rde, "DE", {"Id": cdc})
        SubElement(de, "dVerFor").text = "150"
        
        # ---------------------------------------------
        # gTimb (Timbrado)
        # ---------------------------------------------
        g_timb = SubElement(de, "gTimb")
        SubElement(g_timb, "iTiDE").text = "1"  # 1 = Factura Electrónica
        SubElement(g_timb, "dNumTim").text = str(config_emis.timbrado_numero)
        SubElement(g_timb, "dEst").text = str(config_emis.establecimiento_codigo)
        SubElement(g_timb, "dPunExp").text = str(config_emis.punto_expedicion_codigo)
        # numero de factura format: 0000001
        num_doc = str(factura_data.get("factura_numero", config_emis.siguiente_numero))
        if "-" in num_doc:
            num_doc = num_doc.split("-")[-1]
        SubElement(g_timb, "dNumDoc").text = num_doc.zfill(7)
        # TODO: SIFEN_REAL — dSerieNum si aplica a la empresa
        SubElement(g_timb, "dFeIniT").text = config_emis.timbrado_fecha_inicio
        
        # ---------------------------------------------
        # gDatGralOpe (Datos Generales Operación)
        # ---------------------------------------------
        g_dat_gral = SubElement(de, "gDatGralOpe")
        # Fecha de Emision (Formato ISO)
        fecha_emision = factura_data.get("fecha_factura")
        if not fecha_emision:
            fecha_emision = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        elif len(fecha_emision) == 10:  # yyyy-mm-dd
            fecha_emision = f"{fecha_emision}T12:00:00"
        
        SubElement(g_dat_gral, "dFeEmiDE").text = fecha_emision
        
        # Operación comercial
        g_ope_com = SubElement(g_dat_gral, "gOpeCom")
        SubElement(g_ope_com, "iTipTra").text = "1"     # 1 = Venta de mercaderia
        SubElement(g_ope_com, "iTImp").text = "1"       # 1 = IVA
        moneda = factura_data.get("moneda", "PYG")
        SubElement(g_ope_com, "cMoneOpe").text = moneda
        SubElement(g_ope_com, "dDesMoneOpe").text = "Guarani" if moneda == "PYG" else "Dolar"
        
        if moneda != "PYG":
            # TODO: SIFEN_REAL — Obtener tipo de cambio BCP del día real
            SubElement(g_ope_com, "dCondTiCam").text = "1" # Global
            SubElement(g_ope_com, "dTiCam").text = str(factura_data.get("tipo_cambio", "7500"))
        
        # ---------------------------------------------
        # gEmis (Emisor)
        # ---------------------------------------------
        g_emis = SubElement(de, "gEmis")
        SubElement(g_emis, "dRucEm").text = str(config_emis.ruc_emisor)
        SubElement(g_emis, "dDVEmi").text = str(config_emis.digito_verificador)
        # Tipo de contribuyente: 1 Física, 2 Jurídica
        tipo_cont_emi = "2" if str(config_emis.ruc_emisor).startswith("8") else "1"
        SubElement(g_emis, "iTipCont").text = tipo_cont_emi
        SubElement(g_emis, "cTipReg").text = "1" # Regimen General
        SubElement(g_emis, "dNomEmi").text = str(config_emis.razon_social)
        SubElement(g_emis, "dDirEmi").text = str(config_emis.direccion)
        SubElement(g_emis, "dNumCas").text = str(config_emis.numero_casa)
        SubElement(g_emis, "dCompDir1").text = str(config_emis.ciudad)
        if config_emis.telefono:
            SubElement(g_emis, "dTelEmi").text = str(config_emis.telefono)
        if config_emis.email:
            SubElement(g_emis, "dEmailE").text = str(config_emis.email)

        # Actividad económica
        g_act_eco = SubElement(g_emis, "gActEco")
        SubElement(g_act_eco, "cActEco").text = "86200" # Ejemplo de código de actividad médica
        SubElement(g_act_eco, "dDesActEco").text = str(config_emis.actividad_economica)

        # ---------------------------------------------
        # gDatRec (Receptor)
        # ---------------------------------------------
        g_rec = SubElement(de, "gDatRec")
        ruc_rec = str(factura_data.get("paciente_cedula", "0"))
        tipo_cont_rec = "2" if "-" in ruc_rec else "1" # Simple heurisitica
        
        SubElement(g_rec, "iNatRec").text = tipo_cont_rec  # 1 Física, 2 Jurídica
        SubElement(g_rec, "iTiOpe").text = "1"             # 1 B2B / B2C
        SubElement(g_rec, "cPaisRec").text = "PRY"
        SubElement(g_rec, "dDesPaisRe").text = "Paraguay"
        
        if tipo_cont_rec == "2" and "-" in ruc_rec:
            # Es un RUC con DV
            partes = ruc_rec.split("-")
            SubElement(g_rec, "dRUCRec").text = partes[0]
            SubElement(g_rec, "dDVRec").text = partes[1]
        else:
            SubElement(g_rec, "dNumIDRec").text = ruc_rec
            
        SubElement(g_rec, "dNomRec").text = factura_data.get("paciente_nombre", "CONSUMIDOR FINAL")
        SubElement(g_rec, "dDirRec").text = factura_data.get("paciente_direccion", "Ciudad")
        SubElement(g_rec, "dNumCasRec").text = "0"
        if str(factura_data.get("paciente_telefono", "")):
            SubElement(g_rec, "dTelRec").text = str(factura_data.get("paciente_telefono", ""))
        if str(factura_data.get("paciente_email", "")):
            SubElement(g_rec, "dEmailRec").text = str(factura_data.get("paciente_email", ""))

        # ---------------------------------------------
        # gDtipDE (Específico: gCamFE Factura Electrónica)
        # ---------------------------------------------
        g_dtip = SubElement(de, "gDtipDE")
        g_cam_fe = SubElement(g_dtip, "gCamFE")
        # TODO: SIFEN_REAL — Configurar condición de venta al contado/crédito según gOpePro
        SubElement(g_cam_fe, "iIndPres").text = "1" # Operacion presencial

        # ---------------------------------------------
        # gCamItem (Detalle de Items)
        # ---------------------------------------------
        # Variables acumuladoras para Totales y Bases Imponibles
        sub_exe = 0
        sub_5 = 0
        sub_10 = 0
        base_5 = 0
        base_10 = 0
        iva_5 = 0
        iva_10 = 0
        
        for idx, item in enumerate(detalle_data, start=1):
            g_item = SubElement(de, "gCamItem")
            # En la estructura real XSD, gCamItem va como hijo directo de DE ? 
            # Corrección: según XSD, gCamItem va dentro de gDtipDE? 
            # No, gCamItem va como hijo de DE, justo antes de gTotSub.
            SubElement(g_item, "dPcodExt").text = item.get("item_codigo", f"P{idx:03d}")
            SubElement(g_item, "dDesProSer").text = str(item.get("item_descripcion"))
            c_uni = SubElement(g_item, "gValorItem")
            
            precio_uni = int(item.get("item_precio_unitario", 0))
            cant = int(item.get("item_cantidad", 1) or 1)
            desc = int(item.get("item_descuento", 0) or 0)
            
            tot_bruto = precio_uni * cant
            tot_neto = tot_bruto - desc
            
            SubElement(c_uni, "dPUniProSer").text = str(precio_uni)
            SubElement(c_uni, "dTotBruOpeItem").text = str(tot_bruto)
            # Todo tipo de variaciones si hay descuentos...
            
            g_cam_iva = SubElement(g_item, "gCamIVA")
            tasa_iva = float(item.get("impuesto_porcentaje", 10.0) or 0.0)
            if tasa_iva == 0:
                SubElement(g_cam_iva, "iAfecIVA").text = "3" # Exento
                SubElement(g_cam_iva, "dPropIVA").text = "0"
                SubElement(g_cam_iva, "dTasaIVA").text = "0"
                sub_exe += tot_neto
            elif tasa_iva == 5:
                SubElement(g_cam_iva, "iAfecIVA").text = "1" # Gravado
                SubElement(g_cam_iva, "dPropIVA").text = "100"
                SubElement(g_cam_iva, "dTasaIVA").text = "5"
                base_imp = round(tot_neto / 1.05)
                monto_iva = tot_neto - base_imp
                SubElement(g_cam_iva, "dBasGravIVA").text = str(base_imp)
                SubElement(g_cam_iva, "dLiqIVAItem").text = str(monto_iva)
                
                # En SIFEN, dSub5/dSub10 acumulan el total de la operacion (con IVA)
                sub_5 += tot_neto
                base_5 += base_imp
                iva_5 += monto_iva
            else: # 10%
                SubElement(g_cam_iva, "iAfecIVA").text = "1" # Gravado
                SubElement(g_cam_iva, "dPropIVA").text = "100"
                SubElement(g_cam_iva, "dTasaIVA").text = "10"
                base_imp = round(tot_neto / 1.10)
                monto_iva = tot_neto - base_imp
                SubElement(g_cam_iva, "dBasGravIVA").text = str(base_imp)
                SubElement(g_cam_iva, "dLiqIVAItem").text = str(monto_iva)
                
                # En SIFEN, dSub5/dSub10 acumulan el total de la operacion (con IVA)
                sub_10 += tot_neto
                base_10 += base_imp
                iva_10 += monto_iva

        # ---------------------------------------------
        # gTotSub (Totales)
        # ---------------------------------------------
        g_tot_sub = SubElement(de, "gTotSub")
        # Base Totals
        SubElement(g_tot_sub, "dSubExe").text = str(sub_exe)
        SubElement(g_tot_sub, "dSubExo").text = "0"
        SubElement(g_tot_sub, "dSub5").text = str(sub_5)
        SubElement(g_tot_sub, "dSub10").text = str(sub_10)
        
        # SIFEN E014: dTotOpe = dSubExe + dSubExo + dSub5 + dSub10
        tot_ope = sub_exe + sub_5 + sub_10
        SubElement(g_tot_sub, "dTotOpe").text = str(tot_ope)
        SubElement(g_tot_sub, "dTotDesc").text = "0"
        SubElement(g_tot_sub, "dTotDescGlotem").text = "0"
        SubElement(g_tot_sub, "dTotAntItem").text = "0"
        SubElement(g_tot_sub, "dTotAnt").text = "0"
        SubElement(g_tot_sub, "dPorcDescTotal").text = "0"
        SubElement(g_tot_sub, "dTotOpeGs").text = str(tot_ope)

        if sub_5 > 0 or sub_10 > 0:
            SubElement(g_tot_sub, "dIVA5").text = str(iva_5)
            SubElement(g_tot_sub, "dIVA10").text = str(iva_10)
            SubElement(g_tot_sub, "dIVAcomi").text = "0"
            SubElement(g_tot_sub, "dTotIVA").text = str(iva_5 + iva_10)
            SubElement(g_tot_sub, "dBaseGrav5").text = str(base_5)
            SubElement(g_tot_sub, "dBaseGrav10").text = str(base_10)
            SubElement(g_tot_sub, "dTBasGraIVA").text = str(base_5 + base_10)

        # Convertir a bytes de XML
        xml_bytes = tostring(rde, encoding="utf-8", xml_declaration=True)
        return xml_bytes

    def generar_xml_factura(self, factura_data: dict, detalle_data: list, config_empresa: dict) -> bytes:
        """
        [DEPRECATED] Mantenido por compatibilidad temporal hacia atrás.
        Usar generar_xml_v150() pasandole SifenEmisionConfig y CDC en lo posible.
        """
        # Crearemos un config y CDC dummy para no romper codigo viejo hasta ser eliminado
        from .sifen_config_service import SifenEmisionConfig
        from app.utils.sifen_cdc_utils import SifenCDCUtils
        
        config_dummy = SifenEmisionConfig(
            ruc_emisor=config_empresa.get("ruc", "0000000"),
            digito_verificador="0",
            razon_social=config_empresa.get("nombre_empresa", "EMPRESA DUMMY"),
            actividad_economica="ACTIVIDAD",
            direccion=config_empresa.get("direccion", "DIR"),
            numero_casa="0",
            ciudad=config_empresa.get("ciudad", "CIU"),
            telefono=config_empresa.get("telefono", ""),
            email=config_empresa.get("email", ""),
            timbrado_numero=factura_data.get("numero_timbrado", "12345678"),
            timbrado_fecha_inicio="2024-01-01",
            timbrado_fecha_fin="2025-01-01",
            establecimiento_codigo="001",
            punto_expedicion_codigo="001",
            siguiente_numero=1,
            id_punto_expedicion=1
        )
        cdc_dummy = SifenCDCUtils.generar_cdc_real(
            tipo_documento="01",
            ruc_emisor=config_dummy.ruc_emisor,
            dv_ruc_emisor=config_dummy.digito_verificador,
            establecimiento=config_dummy.establecimiento_codigo,
            punto_expedicion=config_dummy.punto_expedicion_codigo,
            numero_documento="0000001",
            tipo_contribuyente="2",
            fecha_emision_yyyymmdd=datetime.now().strftime("%Y%m%d")
        )
        return self.generar_xml_v150(factura_data, detalle_data, config_dummy, cdc_dummy)
