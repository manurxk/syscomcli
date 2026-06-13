import os
import base64
from datetime import datetime
from io import BytesIO
import qrcode
from flask import current_app as app

from app.services.factura_pdf_service import FacturaPDFService
from app.dao.modulos.ventas.factura.FacturaDao import FacturaDao

class SifenKudeService:
    """
    Servicio encargado de la Representación Gráfica (KUDE) de las facturas electrónicas.
    Genera el QR normativo, orquesta la creación del PDF y define políticas de almacenamiento.
    """
    
    @staticmethod
    def generar_url_qr(factura_data: dict, modo: str = 'simulado') -> str:
        """
        Genera la URL SIFEN codificada en el QR.
        """
        cdc = factura_data.get('codigo_sifen')
        if not cdc:
            raise ValueError("No se puede generar QR sin CDC (codigo_sifen).")

        if modo == 'simulado':
            return f"DOCUMENTO SIMULADO SIFEN - Prueba de integracion (CDC: {cdc})"
            
        # Para entorno REAL
        # Forma típica URL e-kuatia: https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id={cdc}
        qr_url = f"https://ekuatia.set.gov.py/consultas/qr?nVersion=150&Id={cdc}"
        # A futuro se pueden agregar hash &dFeEmiDi etc.
        return qr_url

    @staticmethod
    def generar_imagen_qr_base64(qr_data_string: str) -> str:
        """Genera imagen PNG de QR y la retorna en Base64."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=2,
        )
        qr.add_data(qr_data_string)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')

    @staticmethod
    def generar_y_guardar_kude(id_factura: int, factura_data: dict, detalle: list, config_empresa: dict) -> str:
        """
        1. Genera el PDF con el comprobante y el QR inyectado.
        2. Guarda el PDF en el servidor `static/kude/YYYY/MM/factura_ID.pdf`.
        3. Actualiza `factura_kude_path` en la base de datos.
        """
        modo = app.config.get('SIFEN_MODO', 'simulado')
        
        # Inyectar QR Base64 a los datos
        qr_url = SifenKudeService.generar_url_qr(factura_data, modo)
        qr_b64 = SifenKudeService.generar_imagen_qr_base64(qr_url)
        factura_data['qr_base64'] = qr_b64
        
        pdf_service = FacturaPDFService()
        pdf_buffer = pdf_service.generar_factura_pdf(factura_data, detalle, config_empresa)
        
        # Definir política de almacenamiento
        now = datetime.now()
        anio = str(now.year)
        mes = str(now.month).zfill(2)
        
        # path estático donde Flask sirve los archivos
        static_dir = os.path.join(app.root_path, 'static', 'kude', anio, mes)
        os.makedirs(static_dir, exist_ok=True)
        
        file_name = f"factura_{id_factura}_{factura_data.get('codigo_sifen', 'KUDE')}.pdf"
        file_path = os.path.join(static_dir, file_name)
        
        # Escribir el buffer al archivo
        with open(file_path, 'wb') as f:
            f.write(pdf_buffer.getvalue())
            
        # Guardar path relativo en BD
        db_path = f"kude/{anio}/{mes}/{file_name}"
        
        # Actualizar base de datos de manera atómica
        SifenKudeService._actualizar_path_bd(id_factura, db_path)
        
        return db_path
        
    @staticmethod
    def _actualizar_path_bd(id_factura: int, path: str):
        from app.conexion.Conexion import Conexion
        con = Conexion().getConexion()
        cur = con.cursor()
        try:
            cur.execute("UPDATE facturas SET factura_kude_path = %s WHERE id_factura = %s", (path, id_factura))
            con.commit()
        except BaseException:
            con.rollback()
            raise
        finally:
            cur.close()
            con.close()

    @staticmethod
    def _actualizar_estado_sifen(id_factura: int, nuevo_estado: str):
        """Actualiza el campo factura_estado_sifen en la BD."""
        from app.conexion.Conexion import Conexion
        con = Conexion().getConexion()
        cur = con.cursor()
        try:
            cur.execute(
                "UPDATE facturas SET factura_estado_sifen = %s WHERE id_factura = %s",
                (nuevo_estado, id_factura)
            )
            con.commit()
        except BaseException:
            con.rollback()
            raise
        finally:
            cur.close()
            con.close()

    @staticmethod
    def reenviar_factura(id_factura: int) -> dict:
        """
        P5 — Reenvía una factura electrónica rechazada.

        Flujo válido: RECHAZADO → PENDIENTE → (se procesa fuera de este método)

        :param id_factura: ID de la factura a reenviar.
        :returns: dict con 'success', 'mensaje', y op. 'cdc'.
        :raises ValueError: si la factura está APROBADA o no existe.
        """
        from app.dao.modulos.ventas.factura.FacturaDao import FacturaDao
        from app.conexion.Conexion import Conexion

        # 1. Verificar el estado actual
        dao = FacturaDao()
        factura_data = dao.getFacturaById(id_factura)
        if not factura_data:
            raise ValueError(f"Factura con ID {id_factura} no encontrada.")

        estado_sifen = factura_data.get('factura_estado_sifen') or ''

        if estado_sifen.upper() == 'APROBADO':
            return {
                'success': False,
                'mensaje': 'No se puede reenviar una factura ya APROBADA por SIFEN.',
                'estado_actual': estado_sifen
            }

        if estado_sifen.upper() not in ('RECHAZADO', 'PENDIENTE', 'NO_IMPLEMENTADO',
                                        'ERROR', 'ACEPTADO_SIMULADO', ''):
            app.logger.warning(
                f"Factura {id_factura} con estado inesperado '{estado_sifen}' — se permite reenvío igualmente."
            )

        # 2. Obtener detalle y empresa para regenerar KUDE
        detalle = dao.getFacturaDetalle(id_factura)
        config_empresa = {
            'nombre_empresa': factura_data.get('empresa_razon_social', ''),
            'ruc': factura_data.get('empresa_ruc', ''),
        }

        # 3. Regenerar KUDE (QR + PDF) y actualizar path en BD
        try:
            db_path = SifenKudeService.generar_y_guardar_kude(
                id_factura, factura_data, detalle, config_empresa
            )
        except Exception as e:
            app.logger.error(f"Error al regenerar KUDE en reenvío de factura {id_factura}: {e}")
            return {'success': False, 'mensaje': f'Error al regenerar KUDE: {str(e)}'}

        # 4. Resetear estado SIFEN a PENDIENTE para que el worker lo procese
        SifenKudeService._actualizar_estado_sifen(id_factura, 'PENDIENTE')

        app.logger.info(f"Factura {id_factura} marcada como PENDIENTE para reenvío. KUDE: {db_path}")
        return {
            'success': True,
            'mensaje': 'Factura marcada como PENDIENTE. Será reenviada a SIFEN en el próximo ciclo.',
            'kude_path': db_path
        }

