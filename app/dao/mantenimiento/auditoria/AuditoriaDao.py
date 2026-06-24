from app.core.base_dao import BaseDAO


class AuditoriaDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def registrar_evento(self, id_usuario, accion, detalle=None, ip_origen=None):
        sql = """
            INSERT INTO auditoria_sistema (id_usuario, accion, detalle, ip_origen)
            VALUES (%s, %s, %s, %s)
            RETURNING id_auditoria
        """
        fila = self.execute_query_one(sql, (id_usuario or None, accion, detalle, ip_origen), commit=True)
        return fila["id_auditoria"] if fila else None
