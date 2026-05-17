from dataclasses import dataclass
from datetime import datetime


@dataclass
class SifenClientConfig:
    """
    Configuración para el cliente SIFEN.
    En modo 'simulado' no se realizan llamadas HTTP reales.
    """
    modo: str = "simulado"  # 'simulado' | 'real'
    base_url: str | None = None  # URL de SIFEN en modo real


class SifenClient:
    """
    Cliente para interactuar con el servicio SIFEN.
    Esta implementación está en modo SIMULADO: no realiza llamadas externas,
    solo genera un CDC ficticio y devuelve una respuesta de prueba.
    """

    def __init__(self, config: SifenClientConfig):
        self.config = config

    def _generar_cdc_simulado(self, factura_data: dict) -> str:
        """
        Genera un CDC "parecido" al real pero solo para pruebas internas.
        Combina RUC, número de factura, fecha y total, y lo rellena a 44 dígitos.
        """
        ruc = (factura_data.get("ruc_emisor") or "0000000").replace("-", "")
        numero = (factura_data.get("factura_numero") or "").replace("-", "").replace(" ", "")
        fecha = (factura_data.get("fecha_factura") or datetime.now().strftime("%Y%m%d")).replace("-", "").replace("/", "")
        total = str(int(factura_data.get("factura_total", 0)))

        base = f"{ruc}{numero}{fecha}{total}"
        if len(base) < 44:
            base = base.ljust(44, "0")
        return base[:44]

    def enviar_factura(self, xml_firmado: bytes, factura_data: dict) -> dict:
        """
        Envía el XML firmado al SIFEN.
        En modo simulado NO se hace request HTTP, solo se devuelve una respuesta falsa.
        """
        if self.config.modo != "real":
            cdc = self._generar_cdc_simulado(factura_data)
            respuesta = {
                "modo": "simulado",
                "cdc": cdc,
                "estado": "ACEPTADO_SIMULADO",
                "mensaje": "Documento aceptado en modo simulado. No fue enviado a la SET.",
            }
            return respuesta

        # TODO: implementar llamada real a los servicios web de SIFEN
        # utilizando self.config.base_url y la documentación oficial de la SET.
        # Por ahora, para no bloquear el flujo, se devuelve un error controlado.
        return {
            "modo": "real",
            "cdc": None,
            "estado": "NO_IMPLEMENTADO",
            "mensaje": "Cliente SIFEN en modo real aún no implementado.",
        }




