from app.core.base_dao import BaseDAO


class RegistroInsumoDao(BaseDAO):
    """Acceso a datos de los insumos utilizados en una consulta (descuenta stock)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getPorConsulta(self, id_consulta):
        """Lista los insumos utilizados de la consulta."""
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
        """Devuelve el stock actual del insumo."""
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
                """UPDATE insumos SET stock_actual = stock_actual - %s WHERE id_insumo = %s AND stock_actual >= %s
                   RETURNING des_insumo, insumo_unidad_medida, stock_actual, stock_minimo""",
                (cantidad, id_insumo, cantidad)
            )
            insumo = cur.fetchone()
            if insumo is None:
                cur.execute("SELECT des_insumo, insumo_unidad_medida, stock_actual FROM insumos WHERE id_insumo = %s", (id_insumo,))
                actual = cur.fetchone()
                if actual is None:
                    raise ValueError("El insumo no existe.")
                raise ValueError(f"Stock insuficiente de {actual[0]}: quedan {actual[2]:g} {actual[1].lower()}.")

            cur.execute(
                """
                INSERT INTO registro_insumos (
                    id_consulta, id_insumo, registro_cantidad, registro_observaciones, usuario_creacion
                ) VALUES (%s, %s, %s, %s, %s)
                RETURNING id_registro_insumo
                """,
                (id_consulta, id_insumo, cantidad, observaciones, usuario_creacion)
            )
            nombre, unidad, stock, minimo = insumo
            aviso = (f"El stock de {nombre} quedó en {stock:g} {unidad.lower()} (mínimo {minimo:g}): hay que reponerlo."
                     if stock <= minimo else None)
            return {'id_registro_insumo': cur.fetchone()[0], 'aviso': aviso}

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
