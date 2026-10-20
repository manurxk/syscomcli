import json
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from app.core.base_dao import BaseDAO

DIAS_SEMANA = {1: 'Lunes', 2: 'Martes', 3: 'Miércoles', 4: 'Jueves', 5: 'Viernes', 6: 'Sábado', 7: 'Domingo'}
PATRON_HORA = re.compile(r"^([01][0-9]|2[0-3]):[0-5][0-9]$")


class EmpresaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEmpresaPrincipal(self):
        sql = """
            SELECT e.id_empresa, e.ruc_nit, e.digito_verificador, e.razon_social, e.nombre_comercial,
                   e.tipo_contribuyente, e.id_ciudad, c.des_ciudad, e.direccion, e.numero_casa, e.codigo_postal,
                   e.telefono, e.celular, e.email, e.sitio_web, e.actividad_economica_principal,
                   e.horario_atencion, e.horario_atencion_tramos, e.es_principal, e.est_empresa
            FROM empresa e
            LEFT JOIN ciudades c ON c.id_ciudad = e.id_ciudad
            ORDER BY e.id_empresa
            LIMIT 1
        """
        return self.execute_query_one(sql)

    def validarRuc(self, ruc_nit):
        """Misma regla que el check constraint chk_empresa_ruc_len: solo dígitos, 6 a 20 caracteres."""
        return bool(re.match(r"^[0-9]{6,20}$", ruc_nit or ""))

    def validarEmail(self, email):
        """Misma regla que el check constraint chk_empresa_email."""
        patron = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        return bool(re.match(patron, email or "", re.IGNORECASE))

    def rucExiste(self, ruc_nit, excluir_id=None):
        sql = "SELECT 1 FROM empresa WHERE ruc_nit = %s"
        params = [ruc_nit]
        if excluir_id:
            sql += " AND id_empresa != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEmpresa(self, ruc_nit, digito_verificador, razon_social, tipo_contribuyente,
                        direccion, telefono, celular, email, nombre_comercial=None, id_ciudad=None,
                        numero_casa=None, codigo_postal=None, sitio_web=None,
                        actividad_economica_principal=None, horario_atencion=None, horario_atencion_tramos=None,
                        usuario_creacion=None):
        """Solo permitido si todavía no existe ninguna empresa (single-tenant)."""
        if self.getEmpresaPrincipal() is not None:
            raise ValueError("Ya existe una empresa configurada")

        sql = """
            INSERT INTO empresa (ruc_nit, digito_verificador, razon_social, nombre_comercial,
                                  tipo_contribuyente, id_ciudad, direccion, numero_casa, codigo_postal,
                                  telefono, celular, email, sitio_web, actividad_economica_principal,
                                  horario_atencion, horario_atencion_tramos, es_principal, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s::jsonb, TRUE, %s)
            RETURNING id_empresa
        """
        fila = self.execute_query_one(sql, (
            ruc_nit, digito_verificador, razon_social, nombre_comercial, tipo_contribuyente,
            id_ciudad, direccion, numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            actividad_economica_principal, horario_atencion, self._tramosJson(horario_atencion_tramos),
            usuario_creacion
        ), commit=True)
        return fila["id_empresa"] if fila else None

    def updateEmpresa(self, id_empresa, ruc_nit, digito_verificador, razon_social, tipo_contribuyente,
                       direccion, telefono, celular, email, nombre_comercial=None, id_ciudad=None,
                       numero_casa=None, codigo_postal=None, sitio_web=None,
                       actividad_economica_principal=None, horario_atencion=None, horario_atencion_tramos=None,
                       usuario_modificacion=None):
        sql = """
            UPDATE empresa
            SET ruc_nit = %s, digito_verificador = %s, razon_social = %s, nombre_comercial = %s,
                tipo_contribuyente = %s, id_ciudad = %s, direccion = %s, numero_casa = %s,
                codigo_postal = %s, telefono = %s, celular = %s, email = %s, sitio_web = %s,
                actividad_economica_principal = %s, horario_atencion = %s,
                horario_atencion_tramos = %s::jsonb, usuario_modificacion = %s
            WHERE id_empresa = %s
        """
        return self.execute_query(sql, (
            ruc_nit, digito_verificador, razon_social, nombre_comercial, tipo_contribuyente,
            id_ciudad, direccion, numero_casa, codigo_postal, telefono, celular, email, sitio_web,
            actividad_economica_principal, horario_atencion, self._tramosJson(horario_atencion_tramos),
            usuario_modificacion, id_empresa
        ), commit=True) > 0


    def _tramosJson(self, tramos):
        return json.dumps(tramos) if tramos else None

    def validarTramos(self, tramos):
        """Valida el horario de atención en tramos ({"<id_dia_semana>": [["HH:MM","HH:MM"], ...]}).

        Devuelve (tramos_normalizados, errores): días 1 a 7, horas HH:MM, desde menor que hasta y tramos
        del mismo día sin superponerse. Los tramos de cada día quedan ordenados por hora; un día sin
        tramos se quita (= cerrado). Un horario vacío es válido (None)."""
        if not tramos:
            return None, []
        if not isinstance(tramos, dict):
            return None, ['El horario de atención no tiene un formato válido.']

        errores = []
        normalizado = {}
        for clave, lista in tramos.items():
            try:
                dia = int(clave)
            except (TypeError, ValueError):
                dia = None
            if dia not in DIAS_SEMANA:
                errores.append(f'El día "{clave}" del horario no es válido.')
                continue
            nombre = DIAS_SEMANA[dia]
            if not isinstance(lista, list):
                errores.append(f'{nombre}: los tramos no tienen un formato válido.')
                continue
            validos = []
            for tramo in lista:
                if not (isinstance(tramo, (list, tuple)) and len(tramo) == 2
                        and all(isinstance(h, str) and PATRON_HORA.match(h) for h in tramo)):
                    errores.append(f'{nombre}: cada tramo necesita hora de inicio y de fin (HH:MM).')
                    continue
                desde, hasta = tramo
                if desde >= hasta:
                    errores.append(f'{nombre}: el tramo {desde}-{hasta} debe empezar antes de terminar.')
                    continue
                validos.append([desde, hasta])
            validos.sort()
            for anterior, siguiente in zip(validos, validos[1:]):
                if siguiente[0] < anterior[1]:
                    errores.append(f'{nombre}: los tramos {anterior[0]}-{anterior[1]} y '
                                   f'{siguiente[0]}-{siguiente[1]} se superponen.')
            if validos:
                normalizado[str(dia)] = validos

        return (normalizado or None), errores

    def getTramosHorario(self):
        """Tramos del horario de atención de la empresa ({"<id_dia_semana>": [["HH:MM","HH:MM"], ...]}) o None."""
        return (self.getEmpresaPrincipal() or {}).get('horario_atencion_tramos')

    def estaEnHorario(self, fecha_hora=None, tramos=None):
        """True si fecha_hora (por defecto, ahora en hora de Asunción) cae dentro de algún tramo del
        horario de atención de la empresa. Sin horario cargado devuelve True: no hay con qué comparar,
        así que nada cuenta como "fuera de horario". Para revisar muchas fechas, pasar los tramos ya
        leídos (getTramosHorario) y no se consulta la base en cada llamada."""
        if tramos is None:
            tramos = self.getTramosHorario()
        if not tramos:
            return True
        if fecha_hora is None:
            fecha_hora = datetime.now(ZoneInfo('America/Asuncion'))
        hora = fecha_hora.strftime('%H:%M')
        return any(desde <= hora < hasta for desde, hasta in tramos.get(str(fecha_hora.isoweekday()), []))
