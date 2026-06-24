from datetime import date, datetime

from app.core.base_dao import BaseDAO

class PacienteDao(BaseDAO):

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def calcular_es_menor(self, fecha_nacimiento):
        """Calcula automáticamente si es menor de edad basado en la fecha de nacimiento"""
        if not fecha_nacimiento:
            return False
        
        # Si es string, convertir a date
        if isinstance(fecha_nacimiento, str):
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
        
        hoy = date.today()
        edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
        
        return edad < 18
    
    def validar_fecha_nacimiento(self, fecha_nacimiento):
        """Valida que la fecha de nacimiento sea razonable"""
        if not fecha_nacimiento:
            return False, "La fecha de nacimiento es obligatoria"
        
        # Si es string, convertir a date
        if isinstance(fecha_nacimiento, str):
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return False, "Formato de fecha inválido"
        
        hoy = date.today()
        
        # No puede ser fecha futura
        if fecha_nacimiento > hoy:
            return False, "La fecha de nacimiento no puede ser futura"
        
        # No puede ser mayor a 120 años
        edad = hoy.year - fecha_nacimiento.year
        if edad > 120:
            return False, "La fecha de nacimiento no es válida (mayor a 120 años)"
        
        return True, ""
    
    def validar_datos_menor(self, es_menor, nom_madre, nom_padre):
        """Valida que si es menor tenga al menos un tutor"""
        if es_menor:
            if not nom_madre and not nom_padre:
                return False, "Debe proporcionar al menos el nombre de la madre o del padre para pacientes menores"
        return True, ""
    def generar_historia_clinica(self, nombre, apellido, cedula=None):
        """
        Genera historia clínica con formato: InicialNombre + InicialApellido + Año + Secuencial
        Ejemplos: AB-2026-001, MG-2026-002
        
        Args:
            nombre: Nombre del paciente
            apellido: Apellido del paciente
            cedula: Cédula (opcional, no se usa en el nuevo formato)
        """
        inicial_nombre = nombre.strip()[0].upper() if nombre else 'X'
        inicial_apellido = apellido.strip()[0].upper() if apellido else 'X'
        año_actual = datetime.now().year
        # Formato base: Iniciales + Año (sin secuencial aún, se agrega en generar_historia_clinica_unica)
        return f"{inicial_nombre}{inicial_apellido}-{año_actual}"

    def cedulaExiste(self, cedula, excluir_id_persona=None):
        """Verifica si la cédula ya está registrada en personas (paciente o funcionario)."""
        sql = "SELECT 1 FROM personas WHERE per_cedula = %s"
        params = [cedula]
        if excluir_id_persona:
            sql += " AND id_persona != %s"
            params.append(excluir_id_persona)
        return self.execute_query_one(sql, tuple(params)) is not None

    def validar_historia_unica(self, historia_clinica, pac_id=None):
        """
        Verifica que la historia clínica no esté duplicada
        pac_id: excluir el propio paciente en UPDATE
        """
        if pac_id:
            sql = "SELECT COUNT(*) AS total FROM pacientes WHERE pac_historia_clinica = %s AND id_paciente != %s"
            params = (historia_clinica, pac_id)
        else:
            sql = "SELECT COUNT(*) AS total FROM pacientes WHERE pac_historia_clinica = %s"
            params = (historia_clinica,)

        fila = self.execute_query_one(sql, params)
        return fila["total"] == 0

    def obtener_siguiente_secuencial_año(self, iniciales, año):
        """
        Obtiene el siguiente número secuencial para las iniciales y año dados
        Formato: AB-2026-001, AB-2026-002, etc.
        """
        sql = """
            SELECT pac_historia_clinica
            FROM pacientes
            WHERE pac_historia_clinica LIKE %s
            ORDER BY pac_historia_clinica DESC
            LIMIT 1
        """
        fila = self.execute_query_one(sql, (f"{iniciales}-{año}-%",))

        if not fila:
            return 1

        # Formato esperado: AB-2026-001
        partes = fila["pac_historia_clinica"].split('-')
        if len(partes) == 3:
            try:
                return int(partes[2]) + 1
            except ValueError:
                pass
        return 1
    
    def generar_historia_clinica_unica(self, nombre, apellido, cedula=None):
        """
        Genera historia clínica única con formato: Iniciales + Año + Secuencial
        Ejemplo: AB-2026-001, AB-2026-002, etc.
        
        Args:
            nombre: Nombre del paciente
            apellido: Apellido del paciente
            cedula: Cédula (opcional, no se usa en el nuevo formato)
        """
        inicial_nombre = nombre.strip()[0].upper() if nombre else 'X'
        inicial_apellido = apellido.strip()[0].upper() if apellido else 'X'
        iniciales = f"{inicial_nombre}{inicial_apellido}"
        año_actual = datetime.now().year

        siguiente_secuencial = self.obtener_siguiente_secuencial_año(iniciales, año_actual)
        historia = f"{iniciales}-{año_actual}-{siguiente_secuencial:03d}"

        # Verificar que sea única (por si acaso)
        while not self.validar_historia_unica(historia):
            siguiente_secuencial += 1
            historia = f"{iniciales}-{año_actual}-{siguiente_secuencial:03d}"

        return historia

    def getPacientes(self, pagina=1, por_pagina=50):
        """
        Obtiene todos los pacientes con sus datos completos con paginación.
        Si el usuario es especialista, solo devuelve sus pacientes asignados.
        Si es Admin o Recepcionista, devuelve todos los pacientes.
        
        Args:
            pagina: Número de página (por defecto 1)
            por_pagina: Cantidad de registros por página (por defecto 50)
        
        Returns:
            Diccionario con:
                - datos: Lista de pacientes
                - total: Total de registros
                - pagina: Página actual
                - por_pagina: Registros por página
                - total_paginas: Total de páginas
        """
        # Validar parámetros
        pagina = max(1, int(pagina))
        por_pagina = max(1, min(100, int(por_pagina)))  # Máximo 100 por página
        offset = (pagina - 1) * por_pagina

        total_registros = self.execute_query_one("SELECT COUNT(*) AS total FROM pacientes")["total"]

        pacienteSQL = """
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

        pacientes = self.execute_query(pacienteSQL, (por_pagina, offset))

        resultado = []
        for p in pacientes:
            resultado.append({
                'id_paciente': p['id_paciente'],
                'historia_clinica': p['pac_historia_clinica'] if p['pac_historia_clinica'] else 'Sin historia',
                'es_menor': p['pac_es_menor'] if p['pac_es_menor'] is not None else False,
                'nombre': p['per_nombre'] if p['per_nombre'] else 'Sin nombre',
                'apellido': p['per_apellido'] if p['per_apellido'] else 'Sin apellido',
                'cedula': p['per_cedula'] if p['per_cedula'] else 'Sin cédula',
                'fecha_nacimiento': p['per_fecha_nacimiento'].strftime('%d/%m/%Y') if p['per_fecha_nacimiento'] else None,
                'edad': int(p['edad']) if p['edad'] is not None else None,
                'telefono': p['per_telefono'] if p['per_telefono'] else 'Sin teléfono',
                'genero': p['genero'] if p['genero'] else 'Sin género',
                'ciudad': p['ciudad'] if p['ciudad'] else 'Sin ciudad',
                'fecha_registro': p['fecha_inscripcion'].strftime('%d/%m/%Y') if p['fecha_inscripcion'] else None
            })

        total_paginas = (total_registros + por_pagina - 1) // por_pagina  # Redondeo hacia arriba

        return {
            'datos': resultado,
            'total': total_registros,
            'pagina': pagina,
            'por_pagina': por_pagina,
            'total_paginas': total_paginas
        }

    def getPacienteById(self, pac_id):
        """Obtiene un paciente específico por ID con todos sus datos"""
        pacienteSQL = """
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

        p = self.execute_query_one(pacienteSQL, (pac_id,))

        if not p:
            return None

        return {
            'id_paciente': p['id_paciente'],
            'historia_clinica': p['pac_historia_clinica'] if p['pac_historia_clinica'] else None,
            'es_menor': p['pac_es_menor'] if p['pac_es_menor'] is not None else False,
            'observaciones': p['pac_observaciones'] if p['pac_observaciones'] else None,
            'nombre': p['per_nombre'] if p['per_nombre'] else None,
            'apellido': p['per_apellido'] if p['per_apellido'] else None,
            'cedula': p['per_cedula'] if p['per_cedula'] else None,
            'fecha_nacimiento': p['per_fecha_nacimiento'].strftime('%d/%m/%Y') if p['per_fecha_nacimiento'] else None,
            'edad': int(p['edad']) if p['edad'] is not None else None,
            'telefono': p['per_telefono'] if p['per_telefono'] else None,
            'correo': p['per_correo'] if p['per_correo'] else None,
            'domicilio': p['per_domicilio'] if p['per_domicilio'] else None,
            'genero': p['genero'] if p['genero'] else None,
            'estado_civil': p['estado_civil'] if p['estado_civil'] else None,
            'ciudad': p['ciudad'] if p['ciudad'] else None,
            'ciudad_nacimiento': p['ciudad_nacimiento'] if p['ciudad_nacimiento'] else None,
            'nivel_instruccion': p['nivel_instruccion'] if p['nivel_instruccion'] else None,
            'profesion': p['profesion'] if p['profesion'] else None,
            'fecha_registro': p['fecha_inscripcion'].strftime('%d/%m/%Y') if p['fecha_inscripcion'] else None,
            'nom_madre': p['pam_nom_madre'] if p['pam_nom_madre'] else None,
            'tel_madre': p['pam_tel_madre'] if p['pam_tel_madre'] else None,
            'nom_padre': p['pam_nom_padre'] if p['pam_nom_padre'] else None,
            'tel_padre': p['pam_tel_padre'] if p['pam_tel_padre'] else None,
            'colegio': p['pam_colegio'] if p['pam_colegio'] else None,
            'tel_colegio': p['pam_tel_colegio'] if p['pam_tel_colegio'] else None
        }

    def getPacienteParaEditar(self, pac_id):
        """Obtiene un paciente con IDs y descripciones para edición"""
        pacienteSQL = """
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

        p = self.execute_query_one(pacienteSQL, (pac_id,))

        if not p:
            return None

        return {
            'id_paciente': p['id_paciente'],
            'id_persona': p['id_persona'],
            'historia_clinica': p['pac_historia_clinica'],
            'es_menor': p['pac_es_menor'],
            'observaciones': p['pac_observaciones'],
            'nombre': p['per_nombre'],
            'apellido': p['per_apellido'],
            'cedula': p['per_cedula'],
            'fecha_nacimiento': p['per_fecha_nacimiento'].strftime('%Y-%m-%d') if p['per_fecha_nacimiento'] else None,
            'telefono': p['per_telefono'],
            'correo': p['per_correo'],
            'domicilio': p['per_domicilio'],
            'id_genero': p['id_genero'],
            'id_estado_civil': p['id_estado_civil'],
            'id_ciudad': p['id_ciudad'],
            'id_ciudad_nacimiento': p['id_ciudad_nacimiento'],
            'id_nivel_instruccion': p['id_nivel_instruccion'],
            'id_profesion': p['id_profesion'],
            'genero': p['des_genero'],
            'estado_civil': p['des_estado_civil'],
            'ciudad': p['des_ciudad'],
            'ciudad_nacimiento': p['ciudad_nacimiento_desc'],
            'nivel_instruccion': p['des_nivel_instruccion'],
            'profesion': p['des_profesion'],
            'nom_madre': p['pam_nom_madre'],
            'tel_madre': p['pam_tel_madre'],
            'nom_padre': p['pam_nom_padre'],
            'tel_padre': p['pam_tel_padre'],
            'educacion': p['pam_educacion'],
            'colegio': p['pam_colegio'],
            'tel_colegio': p['pam_tel_colegio']
        }
    def guardarPaciente(self, nombre, apellido, cedula, fecha_nacimiento,
                        telefono=None,
                        id_genero=None, id_estado_civil=None, correo=None, domicilio=None,
                        id_ciudad=None, id_ciudad_nacimiento=None, id_nivel_instruccion=None,
                        id_profesion=None, historia_clinica=None, observaciones=None,
                        nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None,
                        educacion=None, colegio=None, tel_colegio=None, usuario_creacion=None):
        """
        Guarda un nuevo paciente completo.
        Campos obligatorios: nombre, apellido, cedula, fecha_nacimiento
        """
        if not all([nombre, apellido, cedula, fecha_nacimiento]):
            raise ValueError("Faltan campos obligatorios: nombre, apellido, cedula, fecha_nacimiento")

        if self.cedulaExiste(cedula):
            raise ValueError(f'Ya existe una persona registrada con la cédula "{cedula}".')

        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            raise ValueError(mensaje)

        if not historia_clinica or historia_clinica.strip() == "":
            historia_clinica = self.generar_historia_clinica_unica(nombre, apellido)
        elif not self.validar_historia_unica(historia_clinica):
            raise ValueError(f"Historia clínica duplicada: {historia_clinica}")

        es_menor = self.calcular_es_menor(fecha_nacimiento)

        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            raise ValueError(mensaje)

        insertPersonaSQL = """
            INSERT INTO personas(per_nombre, per_apellido, per_cedula, per_fecha_nacimiento,
                            id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                            id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion, usuario_creacion)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id_persona
        """

        insertPacienteSQL = """
            INSERT INTO pacientes(id_persona, pac_historia_clinica, pac_observaciones, pac_es_menor, usuario_creacion)
            VALUES(%s, %s, %s, %s, %s)
            RETURNING id_paciente
        """

        insertMenorSQL = """
            INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre,
                                        pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio, usuario_creacion)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        def _guardar(cur):
            # 1. Insertar persona
            cur.execute(insertPersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, id_genero,
                                        id_estado_civil, telefono, correo, domicilio, id_ciudad,
                                        id_ciudad_nacimiento, id_nivel_instruccion, id_profesion, usuario_creacion))
            persona_id = cur.fetchone()[0]

            # 2. Insertar paciente
            cur.execute(insertPacienteSQL, (persona_id, historia_clinica, observaciones, es_menor, usuario_creacion))
            paciente_id = cur.fetchone()[0]

            # 3. Si es menor (calculado automáticamente), insertar datos del menor
            if es_menor and (nom_madre or nom_padre):
                cur.execute(insertMenorSQL, (paciente_id, nom_madre, tel_madre, nom_padre,
                                            tel_padre, educacion, colegio, tel_colegio, usuario_creacion))

            return paciente_id

        return self.execute_transaction(_guardar)

    def updatePaciente(self, pac_id, nombre, apellido, cedula, fecha_nacimiento, id_genero,
                    id_estado_civil, telefono, correo, domicilio, id_ciudad, id_ciudad_nacimiento,
                    id_nivel_instruccion, id_profesion, historia_clinica, observaciones=None,
                    nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None,
                    educacion=None, colegio=None, tel_colegio=None, usuario_modificacion=None):
        """
        Actualiza un paciente completo (persona + paciente + datos_menor)
        El campo es_menor se calcula automáticamente basado en la fecha de nacimiento
        """
        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            raise ValueError(mensaje)

        fila_persona = self.execute_query_one(
            "SELECT id_persona FROM pacientes WHERE id_paciente = %s", (pac_id,)
        )
        id_persona_actual = fila_persona["id_persona"] if fila_persona else None
        if self.cedulaExiste(cedula, excluir_id_persona=id_persona_actual):
            raise ValueError(f'Ya existe una persona registrada con la cédula "{cedula}".')

        es_menor = self.calcular_es_menor(fecha_nacimiento)

        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            raise ValueError(mensaje)

        updatePersonaSQL = """
            UPDATE personas
            SET per_nombre = %s, per_apellido = %s, per_cedula = %s, per_fecha_nacimiento = %s,
                id_genero = %s, id_estado_civil = %s, per_telefono = %s, per_correo = %s,
                per_domicilio = %s, id_ciudad = %s, id_ciudad_nacimiento = %s,
                id_nivel_instruccion = %s, id_profesion = %s, usuario_modificacion = %s
            WHERE id_persona = (SELECT id_persona FROM pacientes WHERE id_paciente = %s)
        """

        updatePacienteSQL = """
            UPDATE pacientes
            SET pac_historia_clinica = %s, pac_observaciones = %s, pac_es_menor = %s, usuario_modificacion = %s
            WHERE id_paciente = %s
        """

        updateMenorSQL = """
            UPDATE pacientes_menores
            SET pam_nom_madre = %s, pam_tel_madre = %s, pam_nom_padre = %s, pam_tel_padre = %s,
                pam_educacion = %s, pam_colegio = %s, pam_tel_colegio = %s, usuario_modificacion = %s
            WHERE id_paciente = %s
        """

        insertMenorSQL = """
            INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre,
                                        pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio, usuario_creacion)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        deleteMenorSQL = """
            DELETE FROM pacientes_menores WHERE id_paciente = %s
        """

        def _actualizar(cur):
            # 1. Actualizar persona
            cur.execute(updatePersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, id_genero,
                                        id_estado_civil, telefono, correo, domicilio, id_ciudad,
                                        id_ciudad_nacimiento, id_nivel_instruccion,
                                        id_profesion, usuario_modificacion, pac_id))

            # 2. Actualizar paciente
            cur.execute(updatePacienteSQL, (historia_clinica, observaciones, es_menor, usuario_modificacion, pac_id))

            # 3. Manejar datos del menor
            cur.execute("SELECT id_paciente_menor FROM pacientes_menores WHERE id_paciente = %s", (pac_id,))
            existe_menor = cur.fetchone()

            if es_menor and (nom_madre or nom_padre):
                if existe_menor:
                    cur.execute(updateMenorSQL, (nom_madre, tel_madre, nom_padre, tel_padre,
                                                educacion, colegio, tel_colegio, usuario_modificacion, pac_id))
                else:
                    cur.execute(insertMenorSQL, (pac_id, nom_madre, tel_madre, nom_padre,
                                                tel_padre, educacion, colegio, tel_colegio, usuario_modificacion))
            elif existe_menor:
                cur.execute(deleteMenorSQL, (pac_id,))

            return True

        return self.execute_transaction(_actualizar)

    def desactivarPaciente(self, pac_id, usuario_modificacion=None):
        """Desactiva un paciente (soft-delete, est_paciente = FALSE)."""
        sql = "UPDATE pacientes SET est_paciente = FALSE, usuario_modificacion = %s WHERE id_paciente = %s"
        return self.execute_query(sql, (usuario_modificacion, pac_id), commit=True) > 0

    def getPacientesMenores(self):
        """Obtiene solo los pacientes menores de edad (pac_es_menor = TRUE)."""
        pacienteSQL = """
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

        resultados = self.execute_query(pacienteSQL)

        return [{
            'id_paciente': r['id_paciente'],
            'historia_clinica': r['pac_historia_clinica'],
            'nombre': r['per_nombre'],
            'apellido': r['per_apellido'],
            'cedula': r['per_cedula'],
            'fecha_nacimiento': r['per_fecha_nacimiento'].strftime('%d/%m/%Y') if r['per_fecha_nacimiento'] else None,
            'edad': int(r['edad']) if r['edad'] else None,
            'nom_madre': r['pam_nom_madre'],
            'nom_padre': r['pam_nom_padre'],
            'colegio': r['pam_colegio']
        } for r in resultados]