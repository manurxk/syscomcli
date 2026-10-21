import re

from app.core.base_dao import BaseDAO

class FuncionarioDao(BaseDAO):
    """Acceso a datos de funcionarios."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def es_cargo_especialista(self, id_cargo):
        """Un cargo requiere datos de especialista si está marcado como clínico
        (cargos.es_clinico), el mismo criterio que usa la pantalla de funcionarios."""
        fila = self.execute_query_one("SELECT es_clinico FROM cargos WHERE id_cargo = %s", (id_cargo,))
        return bool(fila and fila['es_clinico'])

    def validarNombreApellido(self, texto):
        """Regla más permisiva que los referenciales de catálogo: letras, espacios, guion y apóstrofe (nombres reales)."""
        patron = r"^[A-Za-zÁÉÍÓÚÜáéíóúüÑñ '\-]+$"
        return bool(re.match(patron, texto))

    def matriculaExiste(self, esp_matricula, excluir_id_funcionario=None):
        """Verifica si la matrícula profesional ya está registrada en otro especialista."""
        sql = "SELECT 1 FROM especialistas WHERE esp_matricula = %s"
        params = [esp_matricula]
        if excluir_id_funcionario:
            sql += " AND id_funcionario != %s"
            params.append(excluir_id_funcionario)
        return self.execute_query_one(sql, tuple(params)) is not None

    def validarSinCitasPendientes(self, id_funcionario):
        """Impide dar de baja a un especialista con citas futuras sin cerrar (estado no final).
        Las citas no cambian de especialista (COMMENT ON TABLE citas): primero se cancelan
        o se reagendan con otro especialista."""
        sql = """
            SELECT p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                   COUNT(*) AS pendientes,
                   TO_CHAR(MIN(c.cita_inicio), 'DD/MM/YYYY HH24:MI') AS proxima
            FROM citas c
            JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
            JOIN especialistas e ON c.id_especialista = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            WHERE e.id_funcionario = %s
              AND e.est_especialista = TRUE
              AND ec.es_final = FALSE
              AND c.cita_inicio >= (now() AT TIME ZONE 'America/Asuncion')
            GROUP BY p.per_nombre, p.per_apellido
        """
        fila = self.execute_query_one(sql, (id_funcionario,))
        if fila and fila['pendientes'] > 0:
            raise ValueError(
                f"{fila['nombre_completo']} tiene {fila['pendientes']} cita(s) pendiente(s) "
                f"(próxima: {fila['proxima']}). Cancélelas o reagéndelas con otro especialista "
                f"antes de darlo de baja."
            )

    def cedulaExiste(self, cedula, excluir_id_persona=None):
        """Verifica si la cédula ya está registrada en personas (paciente o funcionario)."""
        sql = "SELECT 1 FROM personas WHERE per_cedula = %s"
        params = [cedula]
        if excluir_id_persona:
            sql += " AND id_persona != %s"
            params.append(excluir_id_persona)
        return self.execute_query_one(sql, tuple(params)) is not None

    def getEspecialistasActivos(self):
        """Especialistas activos para combos (agenda médica, etc.)."""
        sql = """
            SELECT
                e.id_especialista,
                e.esp_matricula,
                e.esp_color_agenda,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                COALESCE(STRING_AGG(DISTINCT esp.des_especialidad, ', '), 'Sin especialidades') AS especialidades
            FROM especialistas e
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            WHERE f.est_funcionario = TRUE AND e.est_especialista = TRUE
            GROUP BY e.id_especialista, e.esp_matricula, e.esp_color_agenda, p.per_nombre, p.per_apellido
            ORDER BY p.per_apellido, p.per_nombre
        """
        return self.execute_query(sql)

    def getFuncionarios(self):
        """Obtiene todos los funcionarios con sus datos completos"""
        funcionarioSQL = """
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
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario AND e.est_especialista = TRUE
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            GROUP BY f.id_funcionario, p.per_nombre, p.per_apellido, p.per_cedula,
                     p.per_fecha_nacimiento, p.per_telefono, g.des_genero, c.des_ciudad,
                     car.des_cargo, f.est_funcionario, e.esp_matricula, e.id_especialista,
                     p.fecha_creacion
            ORDER BY f.id_funcionario DESC
        """

        funcionarios = self.execute_query(funcionarioSQL)

        resultado = []
        for f in funcionarios:
            resultado.append({
                'id_funcionario': f['id_funcionario'],
                'nombre': f['per_nombre'] if f['per_nombre'] else 'Sin nombre',
                'apellido': f['per_apellido'] if f['per_apellido'] else 'Sin apellido',
                'cedula': f['per_cedula'] if f['per_cedula'] else 'Sin cédula',
                'fecha_nacimiento': f['per_fecha_nacimiento'].strftime('%d/%m/%Y') if f['per_fecha_nacimiento'] else None,
                'edad': int(f['edad']) if f['edad'] is not None else None,
                'telefono': f['per_telefono'] if f['per_telefono'] else 'Sin teléfono',
                'genero': f['genero'] if f['genero'] else 'Sin género',
                'ciudad': f['ciudad'] if f['ciudad'] else 'Sin ciudad',
                'cargo': f['cargo'] if f['cargo'] else 'Sin cargo',
                'activo': f['est_funcionario'] if f['est_funcionario'] is not None else False,
                'matricula': f['esp_matricula'] if f['esp_matricula'] else None,
                'especialidades': f['especialidades'] if f['especialidades'] else 'Sin especialidades',
                'es_especialista': f['es_especialista'] if f['es_especialista'] is not None else False,
                'fecha_registro': f['fecha_inscripcion'].strftime('%d/%m/%Y') if f['fecha_inscripcion'] else None
            })

        return resultado

    def getFuncionarioById(self, id_funcionario):
        """Obtiene un funcionario específico por ID con todos sus datos"""
        funcionarioSQL = """
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
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario AND e.est_especialista = TRUE
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista AND ee.est_especialista_especialidad = TRUE
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            WHERE f.id_funcionario = %s
            GROUP BY f.id_funcionario, f.est_funcionario, p.per_nombre, p.per_apellido, p.per_cedula,
                     p.per_fecha_nacimiento, p.per_telefono, p.per_correo, p.per_domicilio,
                     g.des_genero, ec.des_estado_civil, c.des_ciudad, cn.des_ciudad,
                     ni.des_nivel_instruccion, pr.des_profesion, car.des_cargo,
                     p.fecha_creacion, e.esp_matricula, e.esp_color_agenda
        """

        f = self.execute_query_one(funcionarioSQL, (id_funcionario,))

        if not f:
            return None

        return {
            'id_funcionario': f['id_funcionario'],
            'activo': f['est_funcionario'] if f['est_funcionario'] is not None else False,
            'nombre': f['per_nombre'] if f['per_nombre'] else 'Sin nombre',
            'apellido': f['per_apellido'] if f['per_apellido'] else 'Sin apellido',
            'cedula': f['per_cedula'] if f['per_cedula'] else 'Sin cédula',
            'fecha_nacimiento': f['per_fecha_nacimiento'].strftime('%d/%m/%Y') if f['per_fecha_nacimiento'] else None,
            'edad': int(f['edad']) if f['edad'] is not None else None,
            'telefono': f['per_telefono'] if f['per_telefono'] else None,
            'correo': f['per_correo'] if f['per_correo'] else None,
            'domicilio': f['per_domicilio'] if f['per_domicilio'] else None,
            'genero': f['genero'] if f['genero'] else None,
            'estado_civil': f['estado_civil'] if f['estado_civil'] else None,
            'ciudad': f['ciudad'] if f['ciudad'] else None,
            'ciudad_nacimiento': f['ciudad_nacimiento'] if f['ciudad_nacimiento'] else None,
            'nivel_instruccion': f['nivel_instruccion'] if f['nivel_instruccion'] else None,
            'profesion': f['profesion'] if f['profesion'] else None,
            'cargo': f['cargo'] if f['cargo'] else None,
            'fecha_registro': f['fecha_inscripcion'].strftime('%d/%m/%Y') if f['fecha_inscripcion'] else None,
            'matricula': f['esp_matricula'] if f['esp_matricula'] else None,
            'color_agenda': f['esp_color_agenda'] if f['esp_color_agenda'] else None,
            'especialidades': f['especialidades'] if f['especialidades'] else None
        }

    def getFuncionarioParaEditar(self, id_funcionario):
        """Obtiene un funcionario con IDs y descripciones para edición"""
        funcionarioSQL = """
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
                cn.des_ciudad AS des_ciudad_nacimiento,
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
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario AND e.est_especialista = TRUE
            WHERE f.id_funcionario = %s
        """

        especialidadesSQL = """
            SELECT ee.id_especialidad
            FROM especialista_especialidades ee
            JOIN especialistas e ON ee.id_especialista = e.id_especialista
            WHERE e.id_funcionario = %s AND ee.est_especialista_especialidad = TRUE
        """

        f = self.execute_query_one(funcionarioSQL, (id_funcionario,))

        if not f:
            return None

        funcionario = {
            'id_funcionario': f['id_funcionario'],
            'id_persona': f['id_persona'],
            'id_cargo': f['id_cargo'],
            'activo': f['est_funcionario'],
            'nombre': f['per_nombre'],
            'apellido': f['per_apellido'],
            'cedula': f['per_cedula'],
            'fecha_nacimiento': f['per_fecha_nacimiento'].strftime('%Y-%m-%d') if f['per_fecha_nacimiento'] else None,
            'telefono': f['per_telefono'],
            'correo': f['per_correo'],
            'domicilio': f['per_domicilio'],
            'id_genero': f['id_genero'],
            'id_estado_civil': f['id_estado_civil'],
            'id_ciudad': f['id_ciudad'],
            'id_ciudad_nacimiento': f['id_ciudad_nacimiento'],
            'id_nivel_instruccion': f['id_nivel_instruccion'],
            'id_profesion': f['id_profesion'],
            'id_especialista': f['id_especialista'],
            'matricula': f['esp_matricula'],
            'color_agenda': f['esp_color_agenda'],
            # Descripciones para mostrar en el formulario
            'genero': f['des_genero'],
            'estado_civil': f['des_estado_civil'],
            'ciudad': f['des_ciudad'],
            'ciudad_nacimiento': f['des_ciudad_nacimiento'],
            'nivel_instruccion': f['des_nivel_instruccion'],
            'profesion': f['des_profesion'],
            'cargo': f['des_cargo'],
            'especialidades': []
        }

        especialidades = self.execute_query(especialidadesSQL, (id_funcionario,))
        funcionario['especialidades'] = [e['id_especialidad'] for e in especialidades]

        return funcionario

    def guardarFuncionario(self, nombre, apellido, cedula, fecha_nacimiento, genero_id, estado_civil_id,
                      telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id, nivel_instruccion_id,
                      profesion_id, id_cargo, est_funcionario=True, usuario_creacion=None,
                      esp_matricula=None, especialidades=None, esp_color_agenda='#3498db'):
        """
        Guarda un nuevo funcionario completo (persona + funcionario + especialista si aplica)

        Args:
            especialidades: lista de IDs de especialidades [1, 2, 8]
        """

        # Validar si es especialista
        if self.es_cargo_especialista(id_cargo):
            if not esp_matricula:
                raise ValueError("Matrícula es obligatoria para especialistas")
            if not especialidades or len(especialidades) == 0:
                raise ValueError("Debe seleccionar al menos una especialidad")
            if self.matriculaExiste(esp_matricula):
                raise ValueError(f'Ya existe un especialista registrado con la matrícula "{esp_matricula}".')

        if self.cedulaExiste(cedula):
            raise ValueError(f'Ya existe una persona registrada con la cédula "{cedula}".')

        insertPersonaSQL = """
            INSERT INTO personas(per_nombre, per_apellido, per_cedula, per_fecha_nacimiento,
                            id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                            id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion, usuario_creacion)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_persona
        """

        insertFuncionarioSQL = """
            INSERT INTO funcionarios(id_persona, id_cargo, est_funcionario, usuario_creacion)
            VALUES(%s, %s, %s, %s)
            RETURNING id_funcionario
        """

        insertEspecialistaSQL = """
            INSERT INTO especialistas(id_funcionario, esp_matricula, esp_color_agenda, usuario_creacion)
            VALUES(%s, %s, %s, %s)
            RETURNING id_especialista
        """

        insertEspecialidadSQL = """
            INSERT INTO especialista_especialidades(id_especialista, id_especialidad, usuario_creacion)
            VALUES(%s, %s, %s)
        """

        def _guardar(cur):
            # 1. Insertar persona
            cur.execute(insertPersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, genero_id,
                                        estado_civil_id, telefono, correo, domicilio, ciudad_id,
                                        ciudad_nacimiento_id, nivel_instruccion_id, profesion_id, usuario_creacion))
            persona_id = cur.fetchone()[0]

            # 2. Insertar funcionario
            cur.execute(insertFuncionarioSQL, (persona_id, id_cargo, est_funcionario, usuario_creacion))
            funcionario_id = cur.fetchone()[0]

            # 3. Si es especialista, insertar en especialistas
            if self.es_cargo_especialista(id_cargo) and esp_matricula:
                cur.execute(insertEspecialistaSQL, (funcionario_id, esp_matricula, esp_color_agenda, usuario_creacion))
                especialista_id = cur.fetchone()[0]

                # 4. Insertar especialidades (múltiples)
                if especialidades:
                    for id_especialidad in especialidades:
                        cur.execute(insertEspecialidadSQL, (especialista_id, id_especialidad, usuario_creacion))

            return funcionario_id

        return self.execute_transaction(_guardar)

    def updateFuncionario(self, id_funcionario, nombre, apellido, cedula, fecha_nacimiento, genero_id,
                        estado_civil_id, telefono, correo, domicilio, ciudad_id, ciudad_nacimiento_id,
                        nivel_instruccion_id, profesion_id, id_cargo, est_funcionario, usuario_modificacion=None,
                        esp_matricula=None, especialidades=None, esp_color_agenda='#3498db'):
        """Actualiza un funcionario completo (persona + funcionario + especialista + especialidades)"""

        # Validar si es especialista
        if self.es_cargo_especialista(id_cargo):
            if not esp_matricula:
                raise ValueError("Matrícula es obligatoria para especialistas")
            if not especialidades or len(especialidades) == 0:
                raise ValueError("Debe seleccionar al menos una especialidad")
            if self.matriculaExiste(esp_matricula, excluir_id_funcionario=id_funcionario):
                raise ValueError(f'Ya existe un especialista registrado con la matrícula "{esp_matricula}".')

        # Baja como especialista (cargo no clínico) o del funcionario desde el formulario
        if not self.es_cargo_especialista(id_cargo) or not est_funcionario:
            self.validarSinCitasPendientes(id_funcionario)

        fila_persona = self.execute_query_one(
            "SELECT id_persona FROM funcionarios WHERE id_funcionario = %s", (id_funcionario,)
        )
        id_persona_actual = fila_persona["id_persona"] if fila_persona else None
        if self.cedulaExiste(cedula, excluir_id_persona=id_persona_actual):
            raise ValueError(f'Ya existe una persona registrada con la cédula "{cedula}".')

        updatePersonaSQL = """
            UPDATE personas
            SET per_nombre = %s, per_apellido = %s, per_cedula = %s, per_fecha_nacimiento = %s,
                id_genero = %s, id_estado_civil = %s, per_telefono = %s, per_correo = %s,
                per_domicilio = %s, id_ciudad = %s, id_ciudad_nacimiento = %s,
                id_nivel_instruccion = %s, id_profesion = %s, usuario_modificacion = %s
            WHERE id_persona = (SELECT id_persona FROM funcionarios WHERE id_funcionario = %s)
        """

        updateFuncionarioSQL = """
            UPDATE funcionarios
            SET id_cargo = %s, est_funcionario = %s, usuario_modificacion = %s
            WHERE id_funcionario = %s
        """

        # Reactiva la fila si estaba dada de baja: UNIQUE(id_funcionario) impide un segundo INSERT
        updateEspecialistaSQL = """
            UPDATE especialistas
            SET esp_matricula = %s, esp_color_agenda = %s, est_especialista = TRUE, usuario_modificacion = %s
            WHERE id_funcionario = %s
        """

        insertEspecialistaSQL = """
            INSERT INTO especialistas(id_funcionario, esp_matricula, esp_color_agenda, usuario_creacion)
            VALUES(%s, %s, %s, %s)
            RETURNING id_especialista
        """

        # Borrado lógico: citas, consultas y demás historia clínica referencian al especialista
        desactivarEspecialidadesSQL = """
            UPDATE especialista_especialidades
            SET est_especialista_especialidad = FALSE, usuario_modificacion = %s
            WHERE id_especialista = %s AND est_especialista_especialidad = TRUE
        """

        # Mismo patrón "buscar y reactivar" que ListaEsperaDao.agregarOReactivar
        activarEspecialidadSQL = """
            INSERT INTO especialista_especialidades(id_especialista, id_especialidad, usuario_creacion)
            VALUES(%s, %s, %s)
            ON CONFLICT (id_especialista, id_especialidad) DO UPDATE
            SET est_especialista_especialidad = TRUE, usuario_modificacion = EXCLUDED.usuario_creacion
        """

        desactivarEspecialistaSQL = """
            UPDATE especialistas
            SET est_especialista = FALSE, usuario_modificacion = %s
            WHERE id_funcionario = %s
        """

        # Mismo criterio que AgendaHorariosDao al editar un horario: solo turnos libres a futuro
        quitarSlotsLibresSQL = """
            DELETE FROM slots_agenda
            WHERE id_especialista = %s
              AND estado_slot = 'DISPONIBLE'
              AND slot_inicio >= (now() AT TIME ZONE 'America/Asuncion')
        """

        def _actualizar(cur):
            # 1. Actualizar persona
            cur.execute(updatePersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, genero_id,
                                        estado_civil_id, telefono, correo, domicilio, ciudad_id,
                                        ciudad_nacimiento_id, nivel_instruccion_id,
                                        profesion_id, usuario_modificacion, id_funcionario))

            # 2. Actualizar funcionario
            cur.execute(updateFuncionarioSQL, (id_cargo, est_funcionario, usuario_modificacion, id_funcionario))

            # 3. Manejar datos de especialista
            cur.execute("SELECT id_especialista FROM especialistas WHERE id_funcionario = %s", (id_funcionario,))
            existe_especialista = cur.fetchone()

            if self.es_cargo_especialista(id_cargo):
                # Si debe ser especialista
                if esp_matricula:
                    if existe_especialista:
                        # Actualizar especialista existente
                        cur.execute(updateEspecialistaSQL, (esp_matricula, esp_color_agenda, usuario_modificacion, id_funcionario))
                        id_especialista = existe_especialista[0]
                    else:
                        # Crear nuevo especialista
                        cur.execute(insertEspecialistaSQL, (id_funcionario, esp_matricula, esp_color_agenda, usuario_modificacion))
                        id_especialista = cur.fetchone()[0]

                    # Actualizar especialidades: desactivar todas y reactivar/insertar las elegidas
                    cur.execute(desactivarEspecialidadesSQL, (usuario_modificacion, id_especialista))

                    if especialidades:
                        for id_especialidad in especialidades:
                            cur.execute(activarEspecialidadSQL, (id_especialista, id_especialidad, usuario_modificacion))
            else:
                # Si ya no es especialista, darlo de baja (se conserva para su historia clínica)
                if existe_especialista:
                    cur.execute(desactivarEspecialidadesSQL, (usuario_modificacion, existe_especialista[0]))
                    cur.execute(desactivarEspecialistaSQL, (usuario_modificacion, id_funcionario))
                    cur.execute(quitarSlotsLibresSQL, (existe_especialista[0],))

            return True

        return self.execute_transaction(_actualizar)

    def desactivarFuncionario(self, id_funcionario, usuario_modificacion=None):
        """Desactiva un funcionario (soft-delete, est_funcionario = FALSE)."""
        self.validarSinCitasPendientes(id_funcionario)
        sql = "UPDATE funcionarios SET est_funcionario = FALSE, usuario_modificacion = %s WHERE id_funcionario = %s"
        return self.execute_query(sql, (usuario_modificacion, id_funcionario), commit=True) > 0

    def getFuncionariosEspecialistas(self):
        """Obtiene solo los funcionarios que son especialistas
        Estructura similar a getFuncionariosSinUsuario para mantener consistencia"""
        funcionarioSQL = """
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

        resultados = self.execute_query(funcionarioSQL)
        # Estructura similar a getFuncionariosSinUsuario: id, nombre_completo, matricula (equivalente a cargo), cedula
        return [{
            'id_especialista': r['id_especialista'],
            'id_funcionario': r['id_funcionario'],
            'nombre_completo': r['nombre_completo'],
            'matricula': r['matricula'],
            'cedula': r['cedula'],
            'color_agenda': r['color_agenda'],
            'especialidades': r['especialidades'] if r['especialidades'] else ''
        } for r in resultados]
    
    def getEspecialidadesByEspecialista(self, id_especialista):
        """Obtiene las especialidades de un especialista"""
        sql = """
            SELECT esp.id_especialidad, esp.des_especialidad
            FROM especialista_especialidades ee
            JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad
            WHERE ee.id_especialista = %s AND ee.est_especialista_especialidad = TRUE AND esp.est_especialidad = TRUE
            ORDER BY esp.des_especialidad
        """
        return self.execute_query(sql, (id_especialista,))