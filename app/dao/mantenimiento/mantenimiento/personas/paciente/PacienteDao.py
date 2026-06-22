from datetime import date, datetime

from app.core.base_dao import BaseDAO


class PacienteDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def calcular_es_menor(self, fecha_nacimiento):
        if not fecha_nacimiento:
            return False
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        return edad < 18

    def validar_fecha_nacimiento(self, fecha_nacimiento):
        if not fecha_nacimiento:
            return False, "La fecha de nacimiento es obligatoria"
        if isinstance(fecha_nacimiento, str):
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return False, "Formato de fecha inválido"
        hoy = date.today()
        if fecha_nacimiento > hoy:
            return False, "La fecha de nacimiento no puede ser futura"
        edad = hoy.year - fecha_nacimiento.year
        if edad > 120:
            return False, "La fecha de nacimiento no es válida (mayor a 120 años)"
        return True, ""

    def validar_datos_menor(self, es_menor, nom_madre, nom_padre):
        if es_menor and not nom_madre and not nom_padre:
            return False, "Debe proporcionar al menos el nombre de la madre o del padre para pacientes menores"
        return True, ""

    def generar_historia_clinica_unica(self, nombre, apellido):
        """Formato: Iniciales + Año + Secuencial -> AB-2026-001."""
        inicial_nombre = nombre.strip()[0].upper() if nombre else 'X'
        inicial_apellido = apellido.strip()[0].upper() if apellido else 'X'
        iniciales = f"{inicial_nombre}{inicial_apellido}"
        anio_actual = datetime.now().year

        siguiente = self._obtener_siguiente_secuencial(iniciales, anio_actual)
        historia = f"{iniciales}-{anio_actual}-{siguiente:03d}"

        while not self.validar_historia_unica(historia):
            siguiente += 1
            historia = f"{iniciales}-{anio_actual}-{siguiente:03d}"
        return historia

    def _obtener_siguiente_secuencial(self, iniciales, anio):
        sql = """
            SELECT pac_historia_clinica
            FROM pacientes
            WHERE pac_historia_clinica LIKE %s
            ORDER BY pac_historia_clinica DESC
            LIMIT 1
        """
        fila = self.execute_query_one(sql, (f"{iniciales}-{anio}-%",))
        if not fila:
            return 1
        partes = fila["pac_historia_clinica"].split('-')
        if len(partes) == 3:
            try:
                return int(partes[2]) + 1
            except ValueError:
                pass
        return 1

    def validar_historia_unica(self, historia_clinica, id_paciente=None):
        if id_paciente:
            sql = "SELECT COUNT(*) AS total FROM pacientes WHERE pac_historia_clinica = %s AND id_paciente != %s"
            params = (historia_clinica, id_paciente)
        else:
            sql = "SELECT COUNT(*) AS total FROM pacientes WHERE pac_historia_clinica = %s"
            params = (historia_clinica,)
        fila = self.execute_query_one(sql, params)
        return fila["total"] == 0

    def getPacientes(self, pagina=1, por_pagina=50):
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(100, int(por_pagina)))
        offset = (pagina - 1) * por_pagina

        total = self.execute_query_one("SELECT COUNT(*) AS total FROM pacientes")["total"]

        sql = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                pac.pac_es_menor,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                DATE_PART('year', AGE(p.per_fecha_nacimiento)) AS edad,
                p.per_telefono,
                COALESCE(g.des_genero, 'Sin género') AS genero,
                COALESCE(c.des_ciudad, 'Sin ciudad') AS ciudad,
                pac.fecha_creacion AS fecha_inscripcion
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
            ORDER BY pac.id_paciente DESC
            LIMIT %s OFFSET %s
        """
        datos = self.execute_query(sql, (por_pagina, offset))
        total_paginas = (total + por_pagina - 1) // por_pagina

        return {
            'datos': datos,
            'total': total,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': total_paginas,
        }

    def getPacienteById(self, id_paciente):
        sql = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                pac.pac_es_menor,
                pac.pac_observaciones,
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
                pac.fecha_creacion AS fecha_inscripcion,
                pm.pam_nom_madre,
                pm.pam_tel_madre,
                pm.pam_nom_padre,
                pm.pam_tel_padre,
                pm.pam_colegio,
                pm.pam_tel_colegio
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN estados_civiles ec ON p.id_estado_civil = ec.id_estado_civil AND ec.est_estado_civil = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad AND c.est_ciudad = TRUE
            LEFT JOIN ciudades cn ON p.id_ciudad_nacimiento = cn.id_ciudad AND cn.est_ciudad = TRUE
            LEFT JOIN niveles_instruccion ni ON p.id_nivel_instruccion = ni.id_nivel_instruccion AND ni.est_nivel_instruccion = TRUE
            LEFT JOIN profesiones pr ON p.id_profesion = pr.id_profesion AND pr.est_profesion = TRUE
            LEFT JOIN pacientes_menores pm ON pac.id_paciente = pm.id_paciente
            WHERE pac.id_paciente = %s
        """
        return self.execute_query_one(sql, (id_paciente,))

    def getPacienteParaEditar(self, id_paciente):
        sql = """
            SELECT
                pac.id_paciente,
                pac.id_persona,
                pac.pac_historia_clinica,
                pac.pac_es_menor,
                pac.pac_observaciones,
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
                g.des_genero,
                ec.des_estado_civil,
                c.des_ciudad,
                cn.des_ciudad AS ciudad_nacimiento_desc,
                ni.des_nivel_instruccion,
                pr.des_profesion,
                pm.pam_nom_madre,
                pm.pam_tel_madre,
                pm.pam_nom_padre,
                pm.pam_tel_padre,
                pm.pam_educacion,
                pm.pam_colegio,
                pm.pam_tel_colegio
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN generos g ON p.id_genero = g.id_genero
            LEFT JOIN estados_civiles ec ON p.id_estado_civil = ec.id_estado_civil
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
            LEFT JOIN ciudades cn ON p.id_ciudad_nacimiento = cn.id_ciudad
            LEFT JOIN niveles_instruccion ni ON p.id_nivel_instruccion = ni.id_nivel_instruccion
            LEFT JOIN profesiones pr ON p.id_profesion = pr.id_profesion
            LEFT JOIN pacientes_menores pm ON pac.id_paciente = pm.id_paciente
            WHERE pac.id_paciente = %s
        """
        return self.execute_query_one(sql, (id_paciente,))

    def guardarPaciente(self, nombre, apellido, cedula, fecha_nacimiento, telefono,
                         id_genero=None, id_estado_civil=None, correo=None, domicilio=None,
                         id_ciudad=None, id_ciudad_nacimiento=None, id_nivel_instruccion=None,
                         id_profesion=None, historia_clinica=None, observaciones=None,
                         nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None,
                         educacion=None, colegio=None, tel_colegio=None, usuario_creacion=None):
        """Guarda un nuevo paciente completo (persona + paciente + datos de menor si aplica)."""
        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            raise ValueError(mensaje)

        if not historia_clinica or not historia_clinica.strip():
            historia_clinica = self.generar_historia_clinica_unica(nombre, apellido)
        elif not self.validar_historia_unica(historia_clinica):
            raise ValueError(f"Historia clínica duplicada: {historia_clinica}")

        es_menor = self.calcular_es_menor(fecha_nacimiento)
        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            raise ValueError(mensaje)

        def _crear(cur):
            cur.execute(
                """
                INSERT INTO personas(per_nombre, per_apellido, per_cedula, per_fecha_nacimiento,
                    id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                    id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion, usuario_creacion)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_persona
                """,
                (nombre, apellido, cedula, fecha_nacimiento, id_genero, id_estado_civil,
                 telefono, correo, domicilio, id_ciudad, id_ciudad_nacimiento,
                 id_nivel_instruccion, id_profesion, usuario_creacion),
            )
            persona_id = cur.fetchone()[0]

            cur.execute(
                """
                INSERT INTO pacientes(id_persona, pac_historia_clinica, pac_observaciones, pac_es_menor, usuario_creacion)
                VALUES(%s, %s, %s, %s, %s)
                RETURNING id_paciente
                """,
                (persona_id, historia_clinica, observaciones, es_menor, usuario_creacion),
            )
            paciente_id = cur.fetchone()[0]

            if es_menor and (nom_madre or nom_padre):
                cur.execute(
                    """
                    INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre,
                        pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio, usuario_creacion)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (paciente_id, nom_madre, tel_madre, nom_padre, tel_padre, educacion, colegio, tel_colegio, usuario_creacion),
                )

            return paciente_id

        return self.execute_transaction(_crear)

    def updatePaciente(self, id_paciente, nombre, apellido, cedula, fecha_nacimiento, id_genero,
                        id_estado_civil, telefono, correo, domicilio, id_ciudad, id_ciudad_nacimiento,
                        id_nivel_instruccion, id_profesion, historia_clinica, observaciones=None,
                        nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None,
                        educacion=None, colegio=None, tel_colegio=None, usuario_modificacion=None):
        """Actualiza un paciente completo (persona + paciente + datos de menor)."""
        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            raise ValueError(mensaje)

        es_menor = self.calcular_es_menor(fecha_nacimiento)
        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            raise ValueError(mensaje)

        def _actualizar(cur):
            cur.execute(
                """
                UPDATE personas
                SET per_nombre = %s, per_apellido = %s, per_cedula = %s, per_fecha_nacimiento = %s,
                    id_genero = %s, id_estado_civil = %s, per_telefono = %s, per_correo = %s,
                    per_domicilio = %s, id_ciudad = %s, id_ciudad_nacimiento = %s,
                    id_nivel_instruccion = %s, id_profesion = %s, usuario_modificacion = %s
                WHERE id_persona = (SELECT id_persona FROM pacientes WHERE id_paciente = %s)
                """,
                (nombre, apellido, cedula, fecha_nacimiento, id_genero, id_estado_civil,
                 telefono, correo, domicilio, id_ciudad, id_ciudad_nacimiento,
                 id_nivel_instruccion, id_profesion, usuario_modificacion, id_paciente),
            )

            cur.execute(
                """
                UPDATE pacientes
                SET pac_historia_clinica = %s, pac_observaciones = %s, pac_es_menor = %s, usuario_modificacion = %s
                WHERE id_paciente = %s
                """,
                (historia_clinica, observaciones, es_menor, usuario_modificacion, id_paciente),
            )

            cur.execute("SELECT id_paciente_menor FROM pacientes_menores WHERE id_paciente = %s", (id_paciente,))
            existe_menor = cur.fetchone()

            if es_menor and (nom_madre or nom_padre):
                if existe_menor:
                    cur.execute(
                        """
                        UPDATE pacientes_menores
                        SET pam_nom_madre = %s, pam_tel_madre = %s, pam_nom_padre = %s, pam_tel_padre = %s,
                            pam_educacion = %s, pam_colegio = %s, pam_tel_colegio = %s, usuario_modificacion = %s
                        WHERE id_paciente = %s
                        """,
                        (nom_madre, tel_madre, nom_padre, tel_padre, educacion, colegio, tel_colegio, usuario_modificacion, id_paciente),
                    )
                else:
                    cur.execute(
                        """
                        INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre,
                            pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio, usuario_creacion)
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (id_paciente, nom_madre, tel_madre, nom_padre, tel_padre, educacion, colegio, tel_colegio, usuario_modificacion),
                    )
            elif existe_menor:
                cur.execute("DELETE FROM pacientes_menores WHERE id_paciente = %s", (id_paciente,))

            return True

        return self.execute_transaction(_actualizar)

    def desactivarPaciente(self, id_paciente, usuario_modificacion=None):
        sql = "UPDATE pacientes SET est_paciente = FALSE, usuario_modificacion = %s WHERE id_paciente = %s"
        return self.execute_query(sql, (usuario_modificacion, id_paciente), commit=True) > 0

    def getPacientesMenores(self):
        sql = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                DATE_PART('year', AGE(p.per_fecha_nacimiento)) AS edad,
                pm.pam_nom_madre,
                pm.pam_nom_padre,
                pm.pam_colegio
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN pacientes_menores pm ON pac.id_paciente = pm.id_paciente
            WHERE pac.pac_es_menor = TRUE
            ORDER BY p.per_nombre
        """
        return self.execute_query(sql)
