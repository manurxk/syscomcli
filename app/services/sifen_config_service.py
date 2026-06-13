from dataclasses import dataclass
from typing import Optional
from datetime import date
from flask import current_app as app
from app.conexion.Conexion import Conexion

class SifenConfigException(Exception):
    """Excepción lanzada cuando hay un error en la configuración SIFEN (ej. Timbrado vencido o no encontrado)"""
    pass

@dataclass
class SifenEmisionConfig:
    ruc_emisor: str
    digito_verificador: str
    razon_social: str
    actividad_economica: str
    direccion: str
    numero_casa: str
    ciudad: str
    telefono: str
    email: str
    timbrado_numero: str
    timbrado_fecha_inicio: str
    timbrado_fecha_fin: str
    establecimiento_codigo: str
    punto_expedicion_codigo: str
    siguiente_numero: int
    id_punto_expedicion: int

class SifenConfigService:
    """
    Servicio para recuperar y centralizar la configuración de emisión SIFEN
    desde la base de datos (Empresa, Timbrado, Establecimiento, Punto de Expedición).
    """

    @staticmethod
    def get_config_emision(id_empresa: Optional[int] = None, id_punto_expedicion: Optional[int] = None) -> SifenEmisionConfig:
        """
        Recupera la configuración de emisión vigente.
        Si no hay timbrado vigente, lanza SifenConfigException.
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # 1. Obtener datos de la empresa
            if id_empresa:
                sql_empresa = """
                SELECT ruc_nit, digito_verificador, razon_social, actividad_economica_principal,
                       direccion, numero_casa, ciudad, telefono, email
                FROM empresa
                WHERE id_empresa = %s AND est_empresa = TRUE
                """
                cur.execute(sql_empresa, (id_empresa,))
            else:
                sql_empresa = """
                SELECT ruc_nit, digito_verificador, razon_social, actividad_economica_principal,
                       direccion, numero_casa, ciudad, telefono, email
                FROM empresa
                WHERE es_principal = TRUE AND est_empresa = TRUE
                LIMIT 1
                """
                cur.execute(sql_empresa)

            empresa_row = cur.fetchone()
            if not empresa_row:
                raise SifenConfigException("No se encontraron datos de la empresa emisora")

            (ruc, dv, razon_social, actividad_econ, direccion, num_casa, ciudad, telefono, email) = empresa_row

            # Limpiar RUC de guiones si los hay
            ruc = ruc.replace('-', '') if ruc else ruc
            
            # Default values para evitar None in XML
            actividad_econ = actividad_econ or "ACTIVIDAD NO ESPECIFICADA"
            direccion = direccion or "DIRECCION NO ESPECIFICADA"
            num_casa = num_casa or "0"
            ciudad = ciudad or ""
            telefono = telefono or ""
            email = email or ""
            dv = dv or "0"

            # 2. Obtener punto de expedición, establecimiento y timbrado activo de la empresa
            if id_punto_expedicion:
                sql_punto = """
                SELECT p.id_punto_expedicion, p.codigo_punto_expedicion, p.ultimo_numero_usado,
                       e.codigo_establecimiento,
                       t.numero_timbrado, t.fecha_inicio, t.fecha_vencimiento
                FROM puntos_expedicion p
                JOIN establecimientos e ON p.id_establecimiento = e.id_establecimiento
                LEFT JOIN timbrados t ON t.id_empresa = e.id_empresa AND t.est_timbrado = TRUE
                WHERE p.id_punto_expedicion = %s
                ORDER BY t.fecha_inicio DESC
                LIMIT 1
                """
                cur.execute(sql_punto, (id_punto_expedicion,))
            else:
                # Buscar el primer punto de expedición activo del establecimiento principal o primer establecimiento
                sql_punto = """
                SELECT p.id_punto_expedicion, p.codigo_punto_expedicion, p.ultimo_numero_usado,
                       e.codigo_establecimiento,
                       t.numero_timbrado, t.fecha_inicio, t.fecha_vencimiento
                FROM establecimientos e
                JOIN puntos_expedicion p ON p.id_establecimiento = e.id_establecimiento
                LEFT JOIN timbrados t ON t.id_empresa = e.id_empresa AND t.est_timbrado = TRUE
                WHERE e.id_empresa = %s AND e.est_establecimiento = TRUE AND p.est_punto_expedicion = TRUE
                ORDER BY e.es_principal DESC, e.id_establecimiento ASC, p.id_punto_expedicion ASC
                LIMIT 1
                """
                id_emp_para_busqueda = id_empresa
                if not id_empresa:
                    # Si no pasaron id_empresa, necesitamos obtener el id del es_principal para buscar el punto
                    cur.execute("SELECT id_empresa FROM empresa WHERE es_principal = TRUE AND est_empresa = TRUE LIMIT 1")
                    res_emp = cur.fetchone()
                    id_emp_para_busqueda = res_emp[0] if res_emp else -1
                    
                cur.execute(sql_punto, (id_emp_para_busqueda,))

            punto_row = cur.fetchone()
            if not punto_row:
                raise SifenConfigException("No se encontró punto de expedición o timbrado activo")

            (id_punto, cod_punto, ultimo_numero, cod_estab, num_timbrado, fec_ini, fec_fin) = punto_row

            ultimo_numero = ultimo_numero or 0
            siguiente_numero = ultimo_numero + 1

            # 3. Validar vigencia del timbrado
            hoy = date.today()
            if hoy < fec_ini or hoy > fec_fin:
                raise SifenConfigException(f"Timbrado {num_timbrado} fuera de fecha de vigencia. (Vigencia: {fec_ini} al {fec_fin})")

            return SifenEmisionConfig(
                ruc_emisor=ruc,
                digito_verificador=dv,
                razon_social=razon_social,
                actividad_economica=actividad_econ,
                direccion=direccion,
                numero_casa=num_casa,
                ciudad=ciudad,
                telefono=telefono,
                email=email,
                timbrado_numero=str(num_timbrado),
                timbrado_fecha_inicio=fec_ini.strftime("%Y-%m-%d") if hasattr(fec_ini, 'strftime') else str(fec_ini),
                timbrado_fecha_fin=fec_fin.strftime("%Y-%m-%d") if hasattr(fec_fin, 'strftime') else str(fec_fin),
                establecimiento_codigo=str(cod_estab).zfill(3),
                punto_expedicion_codigo=str(cod_punto).zfill(3),
                siguiente_numero=siguiente_numero,
                id_punto_expedicion=id_punto
            )

        except SifenConfigException:
            raise
        except Exception as e:
            app.logger.error(f"Error al obtener config SIFEN: {str(e)}")
            raise SifenConfigException(f"Error al consultar configuración SIFEN: {str(e)}")
        finally:
            cur.close()
            con.close()
