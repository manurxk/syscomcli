import random
from datetime import datetime

class SifenCDCUtils:
    """
    Utilidades puras para el cálculo del CDC de 44 dígitos según el manual técnico del SIFEN.
    """

    @staticmethod
    def calcular_digito_verificador_modulo11(cadena: str) -> str:
        """
        Calcula el dígito verificador usando Módulo 11 (base 2 a 9).
        Similar al cálculo del DV del RUC paraguayo.
        """
        if not cadena.isdigit():
            raise ValueError("La cadena para cálculo de DV debe ser numérica")

        base = 2
        suma = 0
        
        # Iterar la cadena de derecha a izquierda
        for char in reversed(cadena):
            suma += int(char) * base
            base += 1
            if base > 9:
                base = 2

        resto = suma % 11
        if resto > 1:
            dv = 11 - resto
        else:
            dv = 0

        return str(dv)

    @staticmethod
    def generar_cdc(
        ruc_emisor: str,
        tipo_documento: str,
        establecimiento: str,
        punto_expedicion: str,
        numero_documento: str,
        fecha_emision: datetime,
        tipo_emision: str = "1",  # 1: Normal, 2: Contingencia
        codigo_seguridad: str = None
    ) -> str:
        """
        Genera el Código de Control (CDC) de 44 dígitos.
        
        Estructura (44 dígitos):
        - tipo_documento: 2 (ej. 01 para Factura, 04 para Autofactura)
        - ruc_emisor: 8 (sin DV, completado con 0s a la izquierda)
        - digito_verificador_ruc: 1
        - establecimiento: 3 (ej. 001)
        - punto_expedicion: 3 (ej. 001)
        - numero_documento: 7 (ej. 0000001)
        - tipo_contribuyente: 1 (1: PF, 2: PJ) -> asumiremos cálculo en base al RUC o default a PJ si empieza con 8XX
        - fecha_emision: 8 (AAAAMMDD)
        - tipo_emision: 1 (1: Normal)
        - codigo_seguridad: 9 (aleatorio si no se provee)
        - DV_CDC: 1 (Módulo 11 de los 43 caracteres anteriores)
        
        *Nota: La estructura XSD real del CDC (DE Id) es:
        Id = "01" (tipo_documento) + RUC (8) + DV (1) + Estab (3) + Punto (3) + NumDoc (7) + TipoCont (1) + Fecha (8) + TipoEmi (1) + CodSeg (9) + DV (1) = 44 dígitos
        """
        # Limpieza de RUC
        ruc_emisor = ruc_emisor.replace("-", "")
        # Extraer DV del RUC asumiendo que es el último caracter si longitud es 9+
        if len(ruc_emisor) >= 6:
            # Simplificación: si se pasa solo ruc_emisor, asumimos que NO trae DV o si ya trae lo cortamos
            pass
        
        # SIFEN pide RUC a 8 posiciones.
        # Si el RUC enviado ya tiene DV, debemos separarlo. Asumimos RUC enviado *sin* DV pero con 0s a izq
        ruc_8 = str(ruc_emisor).zfill(8)

        # Truncar o asegurar longitud
        tipo_doc_2 = str(tipo_documento).zfill(2)
        estab_3 = str(establecimiento).zfill(3)
        punto_3 = str(punto_expedicion).zfill(3)
        num_doc_7 = str(numero_documento).zfill(7)
        
        # Tipo de contribuyente: 1 = PF, 2 = PJ
        # Heurística simple para Paraguay: RUC persona jurídica empieza con 8, o tiene ciertas logitudes
        tipo_cont_1 = "2" if str(ruc_emisor).startswith("8") else "1"

        fecha_8 = fecha_emision.strftime("%Y%m%d")
        tipo_emi_1 = str(tipo_emision)

        if not codigo_seguridad:
            # Generar código aleatorio de 9 dígitos numéricos
            codigo_seguridad = "".join([str(random.randint(0, 9)) for _ in range(9)])
        cod_seg_9 = str(codigo_seguridad).zfill(9)[:9]

        # Concatenar los 43 dígitos
        # Requerimiento exacto manual Módulo 11 (V150):
        # 1-2: Tipo Documento
        # 3-10: RUC Emisor
        # 11: DV RUC Emisor  -> ASUMIMOS que ruc_emisor debe ser calculado? NO, SIFEN asume que la estructura trae DVs.
        # En vez de adivinar el RUC DV, requeriremos que llegue por separado o que la cadena de arriba esté correcta.
        
        # Mejoramos la firma de la funcion para aceptar DV explicito, o calcularlo.
        # En la implementación real de get_config, obtenemos: ruc, dv
        pass

    @staticmethod
    def generar_cdc_real(
        tipo_documento: str,
        ruc_emisor: str,
        dv_ruc_emisor: str,
        establecimiento: str,
        punto_expedicion: str,
        numero_documento: str,
        tipo_contribuyente: str,
        fecha_emision_yyyymmdd: str,
        tipo_emision: str = "1",
        codigo_seguridad: str = None
    ) -> str:
        """
        Genera CDC con los componentes explícitos.
        """
        tipo_doc_2 = str(tipo_documento).zfill(2)[:2]
        ruc_8 = str(ruc_emisor).zfill(8)[:8]
        dv_1 = str(dv_ruc_emisor)[:1]
        estab_3 = str(establecimiento).zfill(3)[:3]
        punto_3 = str(punto_expedicion).zfill(3)[:3]
        num_doc_7 = str(numero_documento).zfill(7)[:7]
        tipo_cont_1 = str(tipo_contribuyente)[:1]
        fecha_8 = str(fecha_emision_yyyymmdd)[:8]
        tipo_emi_1 = str(tipo_emision)[:1]

        if not codigo_seguridad:
            codigo_seguridad = "".join([str(random.randint(0, 9)) for _ in range(9)])
        cod_seg_9 = str(codigo_seguridad).zfill(9)[:9]

        cadena_43 = f"{tipo_doc_2}{ruc_8}{dv_1}{estab_3}{punto_3}{num_doc_7}{tipo_cont_1}{fecha_8}{tipo_emi_1}{cod_seg_9}"
        
        dv_cdc = SifenCDCUtils.calcular_digito_verificador_modulo11(cadena_43)

        return f"{cadena_43}{dv_cdc}"
