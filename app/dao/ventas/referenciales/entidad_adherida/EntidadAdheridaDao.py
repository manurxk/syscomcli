import re
from app.core.base_dao import BaseDAO


class EntidadAdheridaDao(BaseDAO):
    """Acceso a datos de entidad adherida (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getEntidadesAdheridas(self):
        """Lista los registros de entidad adherida."""
        sql = """
            SELECT id_entidad_adherida, des_entidad_adherida, cod_entidad_adherida,
                   ruc_entidad, telefono_entidad, email_entidad, est_entidad_adherida
            FROM entidades_adheridas
            ORDER BY des_entidad_adherida ASC
        """
        return self.execute_query(sql)

    def getEntidadAdheridaById(self, id_entidad_adherida):
        """Devuelve el registro de entidad adherida por su id, o None si no existe."""
        sql = """
            SELECT id_entidad_adherida, des_entidad_adherida, cod_entidad_adherida,
                   ruc_entidad, telefono_entidad, email_entidad, est_entidad_adherida
            FROM entidades_adheridas WHERE id_entidad_adherida = %s
        """
        return self.execute_query_one(sql, (id_entidad_adherida,))

    def validarDescripcion(self, descripcion):
        """Indica si la descripción solo contiene caracteres permitidos."""
        return bool(re.match(r"^[A-Za-zÁÉÍÓÚáéíóúÑñ0-9 .\-]+$", descripcion))

    def entidadAdheridaExiste(self, descripcion, excluir_id=None):
        """Indica si ya existe un registro de entidad adherida con ese valor; `excluir_id` omite el propio registro al editar."""
        sql = "SELECT 1 FROM entidades_adheridas WHERE LOWER(des_entidad_adherida)=LOWER(%s)"
        params = [descripcion]
        if excluir_id:
            sql += " AND id_entidad_adherida != %s"
            params.append(excluir_id)
        return self.execute_query_one(sql, tuple(params)) is not None

    def guardarEntidadAdherida(self, descripcion, codigo=None, ruc=None, telefono=None,
                                email=None, estado=True, usuario_creacion=None):
        """Inserta un registro de entidad adherida y devuelve el id generado."""
        sql = """
            INSERT INTO entidades_adheridas (des_entidad_adherida, cod_entidad_adherida,
                                             ruc_entidad, telefono_entidad, email_entidad,
                                             est_entidad_adherida, usuario_creacion)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_entidad_adherida
        """
        fila = self.execute_query_one(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             ruc, telefono, email, estado, usuario_creacion),
            commit=True
        )
        return fila["id_entidad_adherida"] if fila else None

    def updateEntidadAdherida(self, id_entidad_adherida, descripcion, codigo=None,
                               ruc=None, telefono=None, email=None,
                               estado=True, usuario_modificacion=None):
        """Actualiza los datos de entidad adherida; devuelve True si modificó una fila."""
        sql = """
            UPDATE entidades_adheridas
            SET des_entidad_adherida=%s, cod_entidad_adherida=%s, ruc_entidad=%s,
                telefono_entidad=%s, email_entidad=%s, est_entidad_adherida=%s,
                usuario_modificacion=%s
            WHERE id_entidad_adherida=%s
        """
        return self.execute_query(
            sql,
            (descripcion, codigo.upper() if codigo else None,
             ruc, telefono, email, estado, usuario_modificacion, id_entidad_adherida),
            commit=True
        ) > 0

    def desactivarEntidadAdherida(self, id_entidad_adherida, usuario_modificacion=None):
        """Da de baja (lógica) el registro de entidad adherida; devuelve True si modificó una fila."""
        sql = "UPDATE entidades_adheridas SET est_entidad_adherida=FALSE, usuario_modificacion=%s WHERE id_entidad_adherida=%s"
        return self.execute_query(sql, (usuario_modificacion, id_entidad_adherida), commit=True) > 0
