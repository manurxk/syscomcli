from dataclasses import dataclass


@dataclass
class SifenFirmaConfig:
    """
    Configuración para la firma SIFEN.
    En modo 'simulado' no se realiza firma criptográfica real.
    """
    modo: str = "simulado"  # 'simulado' | 'real'
    cert_path: str | None = None
    cert_password: str | None = None


class SifenFirmaService:
    """
    Servicio responsable de firmar el XML del DE.
    En modo 'simulado' simplemente agrega un comentario indicando que es una firma de prueba.
    Más adelante se puede implementar la firma XMLDSig real usando el certificado de la SET.
    """

    def __init__(self, config: SifenFirmaConfig):
        self.config = config

    def firmar_xml(self, xml_bytes: bytes) -> bytes:
        """
        Recibe el XML (bytes) y devuelve el XML "firmado".
        En modo simulado, solo envuelve el XML con un comentario.
        """
        if self.config.modo != "real":
            # Firma simulada: dejamos el XML tal cual y añadimos un comentario
            return b"<!-- Firma SIFEN SIMULADA - NO VALIDA PARA PRODUCCION -->\n" + xml_bytes

        # TODO: implementar firma XMLDSig real cuando se disponga de certificado y especificaciones
        # Por ahora retornamos el mismo XML para no bloquear el flujo.
        return xml_bytes




