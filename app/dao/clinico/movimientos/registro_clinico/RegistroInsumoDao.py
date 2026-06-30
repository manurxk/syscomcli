from app.core.base_dao import BaseDAO


class RegistroInsumoDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        sql = """
            SELECT ri.id_registro_insumo, ri.id_consulta, ri.id_insumo,
                   ri.registro_cantidad, ri.registro_observaciones, ri.fecha_creacion,
                   i.des_insumo, i.insumo_unidad_medida
            FROM registro_insumos ri
            JOIN insumos i ON ri.id_insumo = i.id_insumo
            WHERE ri.id_consulta = %s AND ri.est_registro_insumo = TRUE
            ORDER BY ri.id_registro_insumo
        """
        filas = self.execute_query(sql, (id_consulta,))
        for f in filas:
            f['fecha_creacion'] = f['fecha_creacion'].strftime('%d/%m/%Y %H:%M') if f['fecha_creacion'] else None
        return filas

    def getStockDisponible(self, id_insumo):
        sql = "SELECT stock_actual FROM insumos WHERE id_insumo = %s"
        fila = self.execute_query_one(sql, (id_insumo,))
        return fila['stock_actual'] if fila else None

    def guardar(self, id_consulta, datos, usuario_creacion=None):
        """Registra el uso del insumo en la consulta y descuenta el stock, en una sola transacción."""
        id_insumo = datos['id_insumo']
        cantidad = datos['registro_cantidad']
        observaciones = datos.get('registro_observaciones')

        def _guardar(cur):
            cur.execute(
                "UPDATE insumos SET stock_actual = stock_actual - %s WHERE id_insumo = %s AND stock_actual >= %s RETURNING id_insumo",
                (cantidad, id_insumo, cantidad)
            )
            if cur.fetchone() is None:
                raise ValueError("Stock insuficiente para registrar este insumo.")

            cur.execute(
                """
                INSERT INTO registro_insumos (
                    id_consulta, id_insumo, registro_cantidad, registro_observaciones, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING id_registro_insumo
                """,
                (id_consulta, id_insumo, cantidad, observaciones, usuario_creacion)
            )
            return cur.fetchone()[0]

        return self.execute_transaction(_guardar)

    def desactivar(self, id_registro_insumo, usuario_modificacion=None):
        """Desactiva el registro y repone el stock consumido, en una sola transacción."""

        def _desactivar(cur):
            cur.execute(
                """
                UPDATE registro_insumos SET est_registro_insumo = FALSE, usuario_modificacion = %s
                WHERE id_registro_insumo = %s AND est_registro_insumo = TRUE
                RETURNING id_insumo, registro_cantidad
                """,
                (usuario_modificacion, id_registro_insumo)
            )
            fila = cur.fetchone()
            if fila is None:
                return False

            id_insumo, cantidad = fila
            cur.execute(
                "UPDATE insumos SET stock_actual = stock_actual + %s WHERE id_insumo = %s",
                (cantidad, id_insumo)
            )
            return True

        return self.execute_transaction(_desactivar)
