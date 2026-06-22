from app.core.base_dao import BaseDAO

# IDs de cargos que requieren datos de especialista
CARGOS_ESPECIALISTAS = [3]


class FuncionarioDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def es_cargo_especialista(self, id_cargo):
        return id_cargo in CARGOS_ESPECIALISTAS

    def getFuncionarios(self):
        sql = """
            SELECT
                f.id_funcionario,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                DATE_PART('year', AGE(p.per_fecha_nacimiento)) AS edad,
                p.per_telefono,
                COALESCE(g.des_genero, 'Sin género') AS genero,
                COALESCE(c.des_ciudad, 'Sin ciudad') AS ciudad,
                COALESCE(car.des_cargo, 'Sin cargo') AS cargo,
                f.est_funcionario,
                e.esp_matricula,
                COALESCE(STRING_AGG(DISTINCT esp.des_especialidad, ', '), 'Sin especialidades') AS especialidades,
                CASE WHEN e.id_especialista IS NOT NULL THEN TRUE ELSE FALSE END AS es_especialista,
                p.fecha_creacion AS fecha_inscripcion
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN cargos car ON f.id_cargo = car.id_cargo
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            GROUP BY f.id_funcionario, p.per_nombre, p.per_apellido, p.per_cedula,
                     p.per_fecha_nacimiento, p.per_telefono, g.des_genero, c.des_ciudad,
                     car.des_cargo, f.est_funcionario, e.esp_matricula, e.id_especialista,
                     p.fecha_creacion
            ORDER BY f.id_funcionario DESC
        """
        return self.execute_query(sql)

    def getFuncionarioById(self, id_funcionario):
        sql = """
            SELECT
                f.id_funcionario,
                f.est_funcionario,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                DATE_PART('year', AGE(p.per_fecha_nacimiento)) AS edad,
                p.per_telefono,
                p.per_correo,
                p.per_domicilio,
                COALESCE(g.des_genero, 'Sin género') AS genero,
                COALESCE(ec.des_estado_civil, 'Sin estado civil') AS estado_civil,
                COALESCE(c.des_ciudad, 'Sin ciudad') AS ciudad,
                COALESCE(cn.des_ciudad, 'Sin ciudad nacimiento') AS ciudad_nacimiento,
                COALESCE(ni.des_nivel_instruccion, 'Sin nivel') AS nivel_instruccion,
                COALESCE(pr.des_profesion, 'Sin profesión') AS profesion,
                COALESCE(car.des_cargo, 'Sin cargo') AS cargo,
                p.fecha_creacion AS fecha_inscripcion,
                e.esp_matricula,
                e.esp_color_agenda,
                COALESCE(STRING_AGG(esp.des_especialidad, ', '), 'Sin especialidades') AS especialidades
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN cargos car ON f.id_cargo = car.id_cargo
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN estados_civiles ec ON p.id_estado_civil = ec.id_estado_civil AND ec.est_estado_civil = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad AND c.est_ciudad = TRUE
            LEFT JOIN ciudades cn ON p.id_ciudad_nacimiento = cn.id_ciudad AND cn.est_ciudad = TRUE
            LEFT JOIN niveles_instruccion ni ON p.id_nivel_instruccion = ni.id_nivel_instruccion AND ni.est_nivel_instruccion = TRUE
            LEFT JOIN profesiones pr ON p.id_profesion = pr.id_profesion AND pr.est_profesion = TRUE
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            WHERE f.id_funcionario = %s
            GROUP BY f.id_funcionario, f.est_funcionario, p.per_nombre, p.per_apellido, p.per_cedula,
                     p.per_fecha_nacimiento, p.per_telefono, p.per_correo, p.per_domicilio,
                     g.des_genero, ec.des_estado_civil, c.des_ciudad, cn.des_ciudad,
                     ni.des_nivel_instruccion, pr.des_profesion, car.des_cargo,
                     p.fecha_creacion, e.esp_matricula, e.esp_color_agenda
        """
        return self.execute_query_one(sql, (id_funcionario,))

    def getFuncionarioParaEditar(self, id_funcionario):
        sql = """
            SELECT
                f.id_funcionario,
                f.id_persona,
                f.id_cargo,
                f.est_funcionario,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                p.per_telefono,
                p.per_correo,
                p.per_domicilio,
                p.id_genero,
                p.id_estado_civil,
                p.id_ciudad,
                p.id_ciudad_nacimiento,
                p.id_nivel_instruccion,
                p.id_profesion,
                e.id_especialista,
                e.esp_matricula,
                e.esp_color_agenda,
                g.des_genero,
                ec.des_estado_civil,
                c.des_ciudad,
                cn.des_ciudad AS ciudad_nacimiento_desc,
                ni.des_nivel_instruccion,
                pr.des_profesion,
                car.des_cargo
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN cargos car ON f.id_cargo = car.id_cargo
            LEFT JOIN generos g ON p.id_genero = g.id_genero
            LEFT JOIN estados_civiles ec ON p.id_estado_civil = ec.id_estado_civil
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
            LEFT JOIN ciudades cn ON p.id_ciudad_nacimiento = cn.id_ciudad
            LEFT JOIN niveles_instruccion ni ON p.id_nivel_instruccion = ni.id_nivel_instruccion
            LEFT JOIN profesiones pr ON p.id_profesion = pr.id_profesion
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            WHERE f.id_funcionario = %s
        """
        funcionario = self.execute_query_one(sql, (id_funcionario,))
        if not funcionario:
            return None

        especialidades_sql = """
            SELECT ee.id_especialidad
            FROM especialista_especialidades ee
            JOIN especialistas e ON ee.id_especialista = e.id_especialista
            WHERE e.id_funcionario = %s AND ee.est_especialista_especialidad = TRUE
        """
        filas = self.execute_query(especialidades_sql, (id_funcionario,))
        funcionario["especialidades"] = [f["id_especialidad"] for f in filas]
        return funcionario

    def getFuncionariosSinUsuario(self):
        sql = """
            SELECT
                f.id_funcionario,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                p.per_cedula AS cedula,
                car.des_cargo AS cargo
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN cargos car ON f.id_cargo = car.id_cargo
            LEFT JOIN usuarios u ON u.id_funcionario = f.id_funcionario
            WHERE f.est_funcionario = TRUE
              AND u.id_usuario IS NULL
            ORDER BY p.per_nombre, p.per_apellido
        """
        return self.execute_query(sql)

    def guardarFuncionario(self, nombre, apellido, cedula, fecha_nacimiento, genero_id, estado_civil_id,
                            telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id, nivel_instruccion_id,
                            profesion_id, id_cargo, est_funcionario=True, usuario_creacion=None,
                            esp_matricula=None, especialidades=None, esp_color_agenda='#3498db'):
        """Guarda un nuevo funcionario completo (persona + funcionario + especialista si aplica)."""
        if self.es_cargo_especialista(id_cargo):
            if not esp_matricula:
                raise ValueError("Matrícula es obligatoria para especialistas")
            if not especialidades:
                raise ValueError("Debe seleccionar al menos una especialidad")

        def _crear(cur):
            cur.execute(
                """
                INSERT INTO personas(per_nombre, per_apellido, per_cedula, per_fecha_nacimiento,
                    id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                    id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion, usuario_creacion)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_persona
                """,
                (nombre, apellido, cedula, fecha_nacimiento, genero_id, estado_civil_id,
                 telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id,
                 nivel_instruccion_id, profesion_id, usuario_creacion),
            )
            persona_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO funcionarios(id_persona, id_cargo, est_funcionario, usuario_creacion)
                VALUES(%s, %s, %s, %s)
                RETURNING id_funcionario
                """,
                (persona_id, id_cargo, est_funcionario, usuario_creacion),
            )
            funcionario_id = cur.fetchone()[0]

            if self.es_cargo_especialista(id_cargo):
                cur.execute(
                    """
                    INSERT INTO especialistas(id_funcionario, esp_matricula, esp_color_agenda, usuario_creacion)
                    VALUES(%s, %s, %s, %s)
                    RETURNING id_especialista
                    """,
                    (funcionario_id, esp_matricula, esp_color_agenda, usuario_creacion),
                )
                especialista_id = cur.fetchone()[0]
                for id_especialidad in especialidades:
                    cur.execute(
                        """
                        INSERT INTO especialista_especialidades(id_especialista, id_especialidad, usuario_creacion)
                        VALUES(%s, %s, %s)
                        """,
                        (especialista_id, id_especialidad, usuario_creacion),
                    )

            return funcionario_id

        return self.execute_transaction(_crear)

    def updateFuncionario(self, id_funcionario, nombre, apellido, cedula, fecha_nacimiento, genero_id,
                           estado_civil_id, telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id,
                           nivel_instruccion_id, profesion_id, id_cargo, est_funcionario, usuario_modificacion=None,
                           esp_matricula=None, especialidades=None, esp_color_agenda='#3498db'):
        """Actualiza un funcionario completo (persona + funcionario + especialista + especialidades)."""
        if self.es_cargo_especialista(id_cargo):
            if not esp_matricula:
                raise ValueError("Matrícula es obligatoria para especialistas")
            if not especialidades:
                raise ValueError("Debe seleccionar al menos una especialidad")

        def _actualizar(cur):
            cur.execute(
                """
                UPDATE personas
                SET per_nombre = %s, per_apellido = %s, per_cedula = %s, per_fecha_nacimiento = %s,
                    id_genero = %s, id_estado_civil = %s, per_telefono = %s, per_correo = %s,
                    per_domicilio = %s, id_ciudad = %s, id_ciudad_nacimiento = %s,
                    id_nivel_instruccion = %s, id_profesion = %s, usuario_modificacion = %s
                WHERE id_persona = (SELECT id_persona FROM funcionarios WHERE id_funcionario = %s)
                """,
                (nombre, apellido, cedula, fecha_nacimiento, genero_id, estado_civil_id,
                 telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id,
                 nivel_instruccion_id, profesion_id, usuario_modificacion, id_funcionario),
            )

            cur.execute(
                """
                UPDATE funcionarios
                SET id_cargo = %s, est_funcionario = %s, usuario_modificacion = %s
                WHERE id_funcionario = %s
                """,
                (id_cargo, est_funcionario, usuario_modificacion, id_funcionario),
            )

            cur.execute("SELECT id_especialista FROM especialistas WHERE id_funcionario = %s", (id_funcionario,))
            existe_especialista = cur.fetchone()

            if self.es_cargo_especialista(id_cargo):
                if existe_especialista:
                    cur.execute(
                        "UPDATE especialistas SET esp_matricula = %s, esp_color_agenda = %s, usuario_modificacion = %s WHERE id_funcionario = %s",
                        (esp_matricula, esp_color_agenda, usuario_modificacion, id_funcionario),
                    )
                    especialista_id = existe_especialista[0]
                else:
                    cur.execute(
                        """
                        INSERT INTO especialistas(id_funcionario, esp_matricula, esp_color_agenda, usuario_creacion)
                        VALUES(%s, %s, %s, %s) RETURNING id_especialista
                        """,
                        (id_funcionario, esp_matricula, esp_color_agenda, usuario_modificacion),
                    )
                    especialista_id = cur.fetchone()[0]

                cur.execute(
                    "DELETE FROM especialista_especialidades WHERE id_especialista = %s",
                    (especialista_id,),
                )
                for id_especialidad in especialidades:
                    cur.execute(
                        """
                        INSERT INTO especialista_especialidades(id_especialista, id_especialidad, usuario_creacion)
                        VALUES(%s, %s, %s)
                        """,
                        (especialista_id, id_especialidad, usuario_modificacion),
                    )
            elif existe_especialista:
                especialista_id = existe_especialista[0]
                cur.execute("DELETE FROM especialista_especialidades WHERE id_especialista = %s", (especialista_id,))
                cur.execute("DELETE FROM especialistas WHERE id_funcionario = %s", (id_funcionario,))

            return True

        return self.execute_transaction(_actualizar)

    def desactivarFuncionario(self, id_funcionario, usuario_modificacion=None):
        sql = "UPDATE funcionarios SET est_funcionario = FALSE, usuario_modificacion = %s WHERE id_funcionario = %s"
        return self.execute_query(sql, (usuario_modificacion, id_funcionario), commit=True) > 0

    def getFuncionariosEspecialistas(self):
        sql = """
            SELECT
                e.id_especialista,
                f.id_funcionario,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                COALESCE(e.esp_matricula, '') AS matricula,
                p.per_cedula AS cedula,
                COALESCE(e.esp_color_agenda, '#3498db') AS color_agenda,
                STRING_AGG(esp.des_especialidad, ', ') AS especialidades
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            WHERE f.est_funcionario = TRUE AND e.est_especialista = TRUE
            GROUP BY e.id_especialista, f.id_funcionario, p.per_nombre, p.per_apellido,
                     p.per_cedula, e.esp_matricula, e.esp_color_agenda
            ORDER BY p.per_nombre, p.per_apellido
        """
        return self.execute_query(sql)

    def getEspecialidadesByEspecialista(self, id_especialista):
        sql = """
            SELECT esp.id_especialidad, esp.des_especialidad
            FROM especialista_especialidades ee
            JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad
            WHERE ee.id_especialista = %s AND ee.est_especialista_especialidad = TRUE AND esp.est_especialidad = TRUE
            ORDER BY esp.des_especialidad
        """
        return self.execute_query(sql, (id_especialista,))
