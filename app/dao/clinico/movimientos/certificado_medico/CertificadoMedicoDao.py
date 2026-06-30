from app.core.base_dao import BaseDAO
from datetime import date


class CertificadoMedicoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT c.id_certificado, c.id_consulta, c.id_tipo_certificado_medico,
                   c.certificado_numero, c.certificado_fecha, c.certificado_dias_reposo,
                   c.certificado_desde_fecha, c.certificado_hasta_fecha, c.certificado_motivo,
                   c.certificado_diagnostico, c.certificado_recomendaciones, c.certificado_estado,
                   c.fecha_creacion, tc.des_tipo_certificado_medico
            FROM certificados_medicos c
            JOIN tipos_certificados_medicos tc ON c.id_tipo_certificado_medico = tc.id_tipo_certificado_medico
            WHERE c.id_consulta = %s AND c.est_certificado = TRUE
            ORDER BY c.id_certificado
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['certificado_fecha'] = f['certificado_fecha'].strftime('%Y-%m-%d') if f['certificado_fecha'] else None
            f['certificado_desde_fecha'] = f['certificado_desde_fecha'].strftime('%Y-%m-%d') if f['certificado_desde_fecha'] else None
            f['certificado_hasta_fecha'] = f['certificado_hasta_fecha'].strftime('%Y-%m-%d') if f['certificado_hasta_fecha'] else None
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def guardar(self, id_consulta, id_paciente, id_especialista, datos, usuario_creacion=None):
        def _crear(cur):
            anio = date.today().year
            cur.execute(
                "SELECT MAX(CAST(SUBSTRING(certificado_numero FROM '[0-9]+$') AS INTEGER)) FROM certificados_medicos WHERE certificado_numero LIKE %s",
                (f'CERT-{anio}-%',)
            )
            siguiente = (cur.fetchone()[0] or 0) + 1
            numero = f'CERT-{anio}-{siguiente:04d}'

            cur.execute(
                """
                INSERT INTO certificados_medicos(
                    id_consulta, id_paciente, id_especialista, id_tipo_certificado_medico,
                    certificado_numero, certificado_fecha, certificado_dias_reposo,
                    certificado_desde_fecha, certificado_hasta_fecha, certificado_motivo,
                    certificado_diagnostico, certificado_recomendaciones, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_certificado
                """,
                (id_consulta, id_paciente, id_especialista, datos['id_tipo_certificado_medico'],
                 numero, datos['certificado_fecha'], datos.get('certificado_dias_reposo'),
                 datos.get('certificado_desde_fecha'), datos.get('certificado_hasta_fecha'),
                 datos['certificado_motivo'], datos.get('certificado_diagnostico'),
                 datos.get('certificado_recomendaciones'), usuario_creacion)
            )
            return cur.fetchone()[0]

        return self.execute_transaction(_crear)

    def desactivar(self, id_certificado, usuario_modificacion=None):
        sql = "UPDATE certificados_medicos SET est_certificado = FALSE, usuario_modificacion = %s WHERE id_certificado = %s"
        return self.execute_query(sql, (usuario_modificacion, id_certificado), commit=True) > 0
