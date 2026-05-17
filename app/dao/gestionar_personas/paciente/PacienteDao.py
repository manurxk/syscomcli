from flask import current_app as app, session
from app.conexion.Conexion import Conexion
from datetime import date, datetime
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes

class PacienteDao:
    
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
        try:
            # Obtener primera letra del nombre (mayúscula)
            inicial_nombre = nombre.strip()[0].upper() if nombre else 'X'
            
            # Obtener primera letra del apellido (mayúscula)
            inicial_apellido = apellido.strip()[0].upper() if apellido else 'X'
            
            # Obtener año actual
            año_actual = datetime.now().year
            
            # Formato base: Iniciales + Año (sin secuencial aún)
            # El secuencial se agregará en generar_historia_clinica_unica
            historia_base = f"{inicial_nombre}{inicial_apellido}-{año_actual}"
            
            app.logger.info(f"Historia clínica base generada: {historia_base} (de {nombre} {apellido})")
            return historia_base
            
        except Exception as e:
            app.logger.error(f"Error generando historia clínica: {str(e)}")
            # Fallback: usar timestamp
            año_actual = datetime.now().year
            return f"HC-{año_actual}-{int(datetime.now().timestamp()) % 1000}"
        
    def validar_historia_unica(self, historia_clinica, pac_id=None):
        """
        Verifica que la historia clínica no esté duplicada
        pac_id: excluir el propio paciente en UPDATE
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if pac_id:
                # Para UPDATE: excluir el propio paciente
                cur.execute("""
                    SELECT COUNT(*) FROM pacientes 
                    WHERE pac_historia_clinica = %s AND id_paciente != %s
                """, (historia_clinica, pac_id))
            else:
                # Para INSERT: verificar si existe
                cur.execute("""
                    SELECT COUNT(*) FROM pacientes 
                    WHERE pac_historia_clinica = %s
                """, (historia_clinica,))
            
            count = cur.fetchone()[0]
            return count == 0
            
        except Exception as e:
            app.logger.error(f"Error validando unicidad de historia clínica: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
            
    def obtener_siguiente_secuencial_año(self, iniciales, año):
        """
        Obtiene el siguiente número secuencial para las iniciales y año dados
        Formato: AB-2026-001, AB-2026-002, etc.
        
        Args:
            iniciales: Iniciales del paciente (ej: "AB")
            año: Año actual (ej: 2026)
        
        Returns:
            int: Siguiente número secuencial (001, 002, 003, etc.)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Buscar el último secuencial del año para estas iniciales
            # Patrón: AB-2026-001, AB-2026-002, etc.
            patron_busqueda = f"{iniciales}-{año}-%"
            
            cur.execute("""
                SELECT pac_historia_clinica
                FROM pacientes
                WHERE pac_historia_clinica LIKE %s
                ORDER BY pac_historia_clinica DESC
                LIMIT 1
            """, (patron_busqueda,))
            
            resultado = cur.fetchone()
            
            if resultado:
                # Extraer el número secuencial del último registro
                ultima_historia = resultado[0]
                # Formato esperado: AB-2026-001
                partes = ultima_historia.split('-')
                if len(partes) == 3:
                    try:
                        ultimo_secuencial = int(partes[2])
                        siguiente_secuencial = ultimo_secuencial + 1
                        app.logger.info(f"Último secuencial encontrado: {ultimo_secuencial}, siguiente: {siguiente_secuencial}")
                        return siguiente_secuencial
                    except ValueError:
                        app.logger.warning(f"No se pudo extraer secuencial de: {ultima_historia}")
            
            # Si no hay registros previos, empezar desde 1
            app.logger.info(f"No se encontraron registros previos para {iniciales}-{año}, iniciando desde 001")
            return 1
            
        except Exception as e:
            app.logger.error(f"Error obteniendo siguiente secuencial: {str(e)}")
            return 1
        finally:
            cur.close()
            con.close()
    
    def generar_historia_clinica_unica(self, nombre, apellido, cedula=None):
        """
        Genera historia clínica única con formato: Iniciales + Año + Secuencial
        Ejemplo: AB-2026-001, AB-2026-002, etc.
        
        Args:
            nombre: Nombre del paciente
            apellido: Apellido del paciente
            cedula: Cédula (opcional, no se usa en el nuevo formato)
        """
        try:
            # Obtener iniciales y año
            inicial_nombre = nombre.strip()[0].upper() if nombre else 'X'
            inicial_apellido = apellido.strip()[0].upper() if apellido else 'X'
            iniciales = f"{inicial_nombre}{inicial_apellido}"
            año_actual = datetime.now().year
            
            # Obtener siguiente secuencial del año
            siguiente_secuencial = self.obtener_siguiente_secuencial_año(iniciales, año_actual)
            
            # Formato final: AB-2026-001
            historia = f"{iniciales}-{año_actual}-{siguiente_secuencial:03d}"
            
            # Verificar que sea única (por si acaso)
            if not self.validar_historia_unica(historia):
                app.logger.warning(f"Historia {historia} ya existe, incrementando secuencial")
                siguiente_secuencial += 1
                historia = f"{iniciales}-{año_actual}-{siguiente_secuencial:03d}"
            
            app.logger.info(f"Historia clínica única generada: {historia} (de {nombre} {apellido})")
            return historia
            
        except Exception as e:
            app.logger.error(f"Error generando historia clínica única: {str(e)}")
            # Fallback: usar timestamp
            año_actual = datetime.now().year
            timestamp_sufijo = int(datetime.now().timestamp()) % 1000
            return f"HC-{año_actual}-{timestamp_sufijo:03d}"

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
        
        # Verificar si debe filtrar por especialista
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        app.logger.info(f"DEBUG PacienteDao.getPacientes: puede_ver_todos={puede_ver_todos}")
        
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
            app.logger.info(f"DEBUG PacienteDao.getPacientes: id_especialista={id_especialista}")
        
        # Construir query base para contar total
        countSQL = """
            SELECT COUNT(DISTINCT pac.id_paciente)
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        """
        
        # Construir query base para obtener datos
        pacienteSQL = """
            SELECT DISTINCT
                pac.id_paciente,
                pac.pac_historia_clinica,
                CASE WHEN DATE_PART('year', AGE(p.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor,
                p.per_nombre,
                p.per_apellido,
                p.per_cedula,
                p.per_fecha_nacimiento,
                DATE_PART('year', AGE(p.per_fecha_nacimiento)) AS edad,
                p.per_telefono,
                COALESCE(g.des_genero, 'Sin género') AS genero,
                COALESCE(c.des_ciudad, 'Sin ciudad') AS ciudad,
                p.fecha_creacion AS fecha_inscripcion
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
            LEFT JOIN generos g ON p.id_genero = g.id_genero AND g.est_genero = TRUE
            LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        """
        
        # Agregar filtro por especialista si aplica
        if id_especialista:
            countSQL += """
                INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
                WHERE pp.id_especialista = %s AND pp.activo = TRUE
            """
            pacienteSQL += """
                INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
                WHERE pp.id_especialista = %s AND pp.activo = TRUE
            """
        
        pacienteSQL += " ORDER BY pac.id_paciente DESC LIMIT %s OFFSET %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            # Obtener total de registros
            if id_especialista:
                cur.execute(countSQL, (id_especialista,))
            else:
                cur.execute(countSQL)
            total_registros = cur.fetchone()[0]
            
            # Obtener datos paginados
            if id_especialista:
                cur.execute(pacienteSQL, (id_especialista, por_pagina, offset))
            else:
                cur.execute(pacienteSQL, (por_pagina, offset))
            pacientes = cur.fetchall()
            
            resultado = []
            for p in pacientes:
                resultado.append({
                    'id_paciente': p[0],
                    'historia_clinica': p[1] if p[1] else 'Sin historia',
                    'es_menor': p[2] if p[2] is not None else False,
                    'nombre': p[3] if p[3] else 'Sin nombre',
                    'apellido': p[4] if p[4] else 'Sin apellido',
                    'cedula': p[5] if p[5] else 'Sin cédula',
                    'fecha_nacimiento': p[6].strftime('%d/%m/%Y') if p[6] else None,
                    'edad': int(p[7]) if p[7] is not None else None,
                    'telefono': p[8] if p[8] else 'Sin teléfono',
                    'genero': p[9] if p[9] else 'Sin género',
                    'ciudad': p[10] if p[10] else 'Sin ciudad',
                    'fecha_registro': p[11].strftime('%d/%m/%Y') if p[11] else None
                })
            
            total_paginas = (total_registros + por_pagina - 1) // por_pagina  # Redondeo hacia arriba
            
            app.logger.info(f"Se obtuvieron {len(resultado)} pacientes de {total_registros} totales (página {pagina}/{total_paginas})")
            
            return {
                'datos': resultado,
                'total': total_registros,
                'pagina': pagina,
                'por_pagina': por_pagina,
                'total_paginas': total_paginas
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los pacientes: {str(e)}", exc_info=True)
            return {
                'datos': [],
                'total': 0,
                'pagina': pagina,
                'por_pagina': por_pagina,
                'total_paginas': 0
            }
        finally:
            cur.close()
            con.close()

    def getPacienteById(self, pac_id):
        """Obtiene un paciente específico por ID con todos sus datos"""
        pacienteSQL = """
            SELECT
                pac.id_paciente,
                pac.pac_historia_clinica,
                CASE WHEN DATE_PART('year', AGE(p.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor,
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
                p.fecha_creacion AS fecha_inscripcion,
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
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(pacienteSQL, (pac_id,))
            p = cur.fetchone()
            
            if not p:
                app.logger.warning(f"Paciente con ID {pac_id} no encontrado")
                return None
            
            return {
                'id_paciente': p[0],
                'historia_clinica': p[1] if p[1] else None,
                'es_menor': p[2] if p[2] is not None else False,
                'observaciones': p[3] if p[3] else None,
                'nombre': p[4] if p[4] else None,
                'apellido': p[5] if p[5] else None,
                'cedula': p[6] if p[6] else None,
                'fecha_nacimiento': p[7].strftime('%d/%m/%Y') if p[7] else None,
                'edad': int(p[8]) if p[8] is not None else None,
                'telefono': p[9] if p[9] else None,
                'correo': p[10] if p[10] else None,
                'domicilio': p[11] if p[11] else None,
                'genero': p[12] if p[12] else None,
                'estado_civil': p[13] if p[13] else None,
                'ciudad': p[14] if p[14] else None,
                'ciudad_nacimiento': p[15] if p[15] else None,
                'nivel_instruccion': p[16] if p[16] else None,
                'profesion': p[17] if p[17] else None,
                'fecha_registro': p[18].strftime('%d/%m/%Y') if p[18] else None,
                'nom_madre': p[19] if p[19] else None,
                'tel_madre': p[20] if p[20] else None,
                'nom_padre': p[21] if p[21] else None,
                'tel_padre': p[22] if p[22] else None,
                'colegio': p[23] if p[23] else None,
                'tel_colegio': p[24] if p[24] else None
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener paciente por ID: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()

    def getPacienteParaEditar(self, pac_id):
        """Obtiene un paciente con IDs y descripciones para edición"""
        pacienteSQL = """
            SELECT
                pac.id_paciente,
                pac.id_persona,
                pac.pac_historia_clinica,
                CASE WHEN DATE_PART('year', AGE(p.per_fecha_nacimiento)) < 18 THEN TRUE ELSE FALSE END AS es_menor,
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
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(pacienteSQL, (pac_id,))
            p = cur.fetchone()
            
            if not p:
                return None
            
            paciente = {
                'id_paciente': p[0],
                'id_persona': p[1],
                'historia_clinica': p[2],
                'es_menor': p[3],
                'observaciones': p[4],
                'nombre': p[5],
                'apellido': p[6],
                'cedula': p[7],
                'fecha_nacimiento': p[8].strftime('%Y-%m-%d') if p[8] else None,
                'telefono': p[9],
                'correo': p[10],
                'domicilio': p[11],
                'id_genero': p[12],
                'id_estado_civil': p[13],
                'id_ciudad': p[14],
                'id_ciudad_nacimiento': p[15],
                'id_nivel_instruccion': p[16],
                'id_profesion': p[17],
                'genero': p[18],
                'estado_civil': p[19],
                'ciudad': p[20],
                'ciudad_nacimiento': p[21],
                'nivel_instruccion': p[22],
                'profesion': p[23],
                'nom_madre': p[24],
                'tel_madre': p[25],
                'nom_padre': p[26],
                'tel_padre': p[27],
                'educacion': p[28],
                'colegio': p[29],
                'tel_colegio': p[30]
            }
            
            app.logger.info(f"Paciente cargado para editar: {paciente['nombre']} {paciente['apellido']} - Es menor: {paciente['es_menor']}")
            
            return paciente
            
        except Exception as e:
            app.logger.error(f"Error al obtener paciente para editar: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    def guardarPaciente(self, nombre, apellido, cedula, fecha_nacimiento, 
                        telefono=None,  # ← Ahora con valor por defecto
                        id_genero=None, id_estado_civil=None, correo=None, domicilio=None, 
                        id_ciudad=None, id_ciudad_nacimiento=None, id_nivel_instruccion=None, 
                        id_profesion=None, historia_clinica=None, observaciones=None,
                        nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None, 
                        educacion=None, colegio=None, tel_colegio=None):
        """
        Guarda un nuevo paciente completo.
        Campos obligatorios: nombre, apellido, cedula, fecha_nacimiento
        """
        
        # ✅ CORRECCIÓN: Solo validar lo esencial
        if not all([nombre, apellido, cedula, fecha_nacimiento]):
            app.logger.error("Faltan campos obligatorios: nombre, apellido, cedula, fecha_nacimiento")
            return None
        
        
    # ✅ El resto del código sigue igual...
        
        # Validar fecha de nacimiento
        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            app.logger.error(f"Validación de fecha de nacimiento falló: {mensaje}")
            return None
        
        # Generar historia clínica si no viene
        if not historia_clinica or historia_clinica.strip() == "":
            historia_clinica = self.generar_historia_clinica_unica(nombre, apellido, cedula)
            app.logger.info(f"Historia clínica auto-generada: {historia_clinica}")
        else:
            # Si viene manual, validar que sea única
            if not self.validar_historia_unica(historia_clinica):
                app.logger.error(f"Historia clínica duplicada: {historia_clinica}")
                return None
        
        # Calcular automáticamente si es menor
        es_menor = self.calcular_es_menor(fecha_nacimiento)
        app.logger.info(f"Paciente calculado como menor: {es_menor}")
        
        # Validar datos de menor si aplica
        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            app.logger.error(f"Validación de datos de menor falló: {mensaje}")
            return None
        
        insertPersonaSQL = """
            INSERT INTO personas(per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
                            id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                            id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING id_persona
        """
        
        insertPacienteSQL = """
            INSERT INTO pacientes(id_persona, pac_historia_clinica, pac_observaciones)
            VALUES(%s, %s, %s) 
            RETURNING id_paciente
        """
        
        insertMenorSQL = """
            INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre, 
                                        pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # 1. Insertar persona
            app.logger.info(f"Insertando persona: {nombre} {apellido}")
            cur.execute(insertPersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, id_genero, 
                                        id_estado_civil, telefono, correo, domicilio, id_ciudad, 
                                        id_ciudad_nacimiento, id_nivel_instruccion, id_profesion))
            persona_id = cur.fetchone()[0]
            app.logger.info(f"Persona insertada con ID: {persona_id}")

            # 2. Insertar paciente
            app.logger.info(f"Insertando paciente con historia clínica: {historia_clinica}")
            cur.execute(insertPacienteSQL, (persona_id, historia_clinica, observaciones))
            paciente_id = cur.fetchone()[0]
            app.logger.info(f"Paciente insertado con ID: {paciente_id}")

            # 3. Si es menor (calculado automáticamente), insertar datos del menor
            if es_menor and (nom_madre or nom_padre):
                app.logger.info(f"Es menor de edad - Insertando datos de tutor(es)")
                app.logger.info(f"Madre: {nom_madre}, Padre: {nom_padre}, Colegio: {colegio}")
                
                cur.execute(insertMenorSQL, (paciente_id, nom_madre, tel_madre, nom_padre, 
                                            tel_padre, educacion, colegio, tel_colegio))
                app.logger.info("Datos de menor insertados correctamente")

            con.commit()
            app.logger.info(f"Paciente guardado exitosamente con ID: {paciente_id}")
            return paciente_id

        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al insertar paciente completo: {str(e)}", exc_info=True)
            return None

        finally:
            cur.close()
            con.close()

    def updatePaciente(self, pac_id, nombre, apellido, cedula, fecha_nacimiento, id_genero, 
                    id_estado_civil, telefono, correo, domicilio, id_ciudad, id_ciudad_nacimiento,
                    id_nivel_instruccion, id_profesion, historia_clinica, observaciones=None, 
                    nom_madre=None, tel_madre=None, nom_padre=None, tel_padre=None, 
                    educacion=None, colegio=None, tel_colegio=None):
        """
        Actualiza un paciente completo (persona + paciente + datos_menor)
        El campo es_menor se calcula automáticamente basado en la fecha de nacimiento
        """
        
        # Validar fecha de nacimiento
        valido, mensaje = self.validar_fecha_nacimiento(fecha_nacimiento)
        if not valido:
            app.logger.error(f"Validación de fecha de nacimiento falló: {mensaje}")
            return False
        
        # Calcular automáticamente si es menor
        es_menor = self.calcular_es_menor(fecha_nacimiento)
        app.logger.info(f"Paciente calculado como menor: {es_menor} (fecha nacimiento: {fecha_nacimiento})")
        
        # Validar datos de menor si aplica
        valido, mensaje = self.validar_datos_menor(es_menor, nom_madre, nom_padre)
        if not valido:
            app.logger.error(f"Validación de datos de menor falló: {mensaje}")
            return False
        
        updatePersonaSQL = """
            UPDATE personas
            SET per_nombre = %s, per_apellido = %s, per_cedula = %s, per_fecha_nacimiento = %s,
                id_genero = %s, id_estado_civil = %s, per_telefono = %s, per_correo = %s,
                per_domicilio = %s, id_ciudad = %s, id_ciudad_nacimiento = %s,
                id_nivel_instruccion = %s, id_profesion = %s
            WHERE id_persona = (SELECT id_persona FROM pacientes WHERE id_paciente = %s)
        """
        
        updatePacienteSQL = """
            UPDATE pacientes
            SET pac_historia_clinica = %s, pac_observaciones = %s
            WHERE id_paciente = %s
        """
        
        updateMenorSQL = """
            UPDATE pacientes_menores
            SET pam_nom_madre = %s, pam_tel_madre = %s, pam_nom_padre = %s, pam_tel_padre = %s,
                pam_educacion = %s, pam_colegio = %s, pam_tel_colegio = %s
            WHERE id_paciente = %s
        """
        
        insertMenorSQL = """
            INSERT INTO pacientes_menores(id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre,
                                        pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio)
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        deleteMenorSQL = """
            DELETE FROM pacientes_menores WHERE id_paciente = %s
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # 1. Actualizar persona
            app.logger.info(f"Actualizando persona del paciente ID: {pac_id}")
            cur.execute(updatePersonaSQL, (nombre, apellido, cedula, fecha_nacimiento, id_genero,
                                        id_estado_civil, telefono, correo, domicilio, id_ciudad,
                                        id_ciudad_nacimiento, id_nivel_instruccion, 
                                        id_profesion, pac_id))

            # 2. Actualizar paciente
            app.logger.info(f"Actualizando datos del paciente ID: {pac_id}")
            cur.execute(updatePacienteSQL, (historia_clinica, observaciones, pac_id))

            # 3. Manejar datos del menor
            cur.execute("SELECT id_paciente_menor FROM pacientes_menores WHERE id_paciente = %s", (pac_id,))
            existe_menor = cur.fetchone()

            if es_menor:
                # Si es menor (calculado) y tiene datos de tutor
                if nom_madre or nom_padre:
                    if existe_menor:
                        # Actualizar datos existentes
                        app.logger.info(f"Actualizando datos de menor existente para paciente ID: {pac_id}")
                        cur.execute(updateMenorSQL, (nom_madre, tel_madre, nom_padre, tel_padre,
                                                    educacion, colegio, tel_colegio, pac_id))
                    else:
                        # Crear nuevos datos de menor
                        app.logger.info(f"Insertando nuevos datos de menor para paciente ID: {pac_id}")
                        cur.execute(insertMenorSQL, (pac_id, nom_madre, tel_madre, nom_padre,
                                                    tel_padre, educacion, colegio, tel_colegio))
            else:
                # Ya no es menor, eliminar datos si existían
                if existe_menor:
                    app.logger.info(f"Paciente ya no es menor - Eliminando datos de tutor para paciente ID: {pac_id}")
                    cur.execute(deleteMenorSQL, (pac_id,))

            con.commit()
            app.logger.info(f"Paciente {pac_id} actualizado exitosamente")
            return True

        except Exception as e:
            app.logger.error(f"Error al actualizar paciente: {str(e)}", exc_info=True)
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deletePaciente(self, pac_id):
        """
        Elimina un paciente completo (en cascada: pacientes_menores -> pacientes -> personas)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            # Obtener el id_persona antes de eliminar
            cur.execute("SELECT id_persona FROM pacientes WHERE id_paciente = %s", (pac_id,))
            resultado = cur.fetchone()
            
            if not resultado:
                app.logger.error(f"No se encontró el paciente con ID: {pac_id}")
                return False
            
            persona_id = resultado[0]
            app.logger.info(f"Eliminando paciente ID: {pac_id} (persona ID: {persona_id})")

            # 1. Eliminar de pacientes_menores (si existe) - CASCADE lo hace automático
            cur.execute("DELETE FROM pacientes_menores WHERE id_paciente = %s", (pac_id,))
            app.logger.info(f"Datos de menor eliminados (si existían)")
            
            # 2. Eliminar de pacientes
            cur.execute("DELETE FROM pacientes WHERE id_paciente = %s", (pac_id,))
            app.logger.info(f"Paciente eliminado")
            
            # 3. Eliminar de personas
            cur.execute("DELETE FROM personas WHERE id_persona = %s", (persona_id,))
            app.logger.info(f"Persona eliminada")

            con.commit()
            app.logger.info(f"Paciente {pac_id} eliminado exitosamente")
            return True

        except Exception as e:
            app.logger.error(f"Error al eliminar paciente: {str(e)}", exc_info=True)
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def getPacientesMenores(self):
        """
        Obtiene solo los pacientes menores de edad (calculado automáticamente).
        Si el usuario es especialista, solo devuelve sus pacientes asignados.
        """
        # Verificar si debe filtrar por especialista
        id_especialista = None
        if not puede_ver_todos_pacientes():
            id_especialista = obtener_id_especialista_usuario()
        
        # Construir query base
        pacienteSQL = """
            SELECT DISTINCT
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
        """
        
        # Agregar filtro por especialista si aplica
        if id_especialista:
            pacienteSQL += """
                INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
                WHERE DATE_PART('year', AGE(p.per_fecha_nacimiento)) < 18
                    AND pp.id_especialista = %s AND pp.activo = TRUE
            """
        else:
            pacienteSQL += """
                WHERE DATE_PART('year', AGE(p.per_fecha_nacimiento)) < 18
            """
        
        pacienteSQL += " ORDER BY p.per_nombre"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if id_especialista:
                cur.execute(pacienteSQL, (id_especialista,))
            else:
                cur.execute(pacienteSQL)
            resultados = cur.fetchall()
            
            return [{
                'id_paciente': r[0],
                'historia_clinica': r[1],
                'nombre': r[2],
                'apellido': r[3],
                'cedula': r[4],
                'fecha_nacimiento': r[5].strftime('%d/%m/%Y') if r[5] else None,
                'edad': int(r[6]) if r[6] else None,
                'nom_madre': r[7],
                'nom_padre': r[8],
                'colegio': r[9]
            } for r in resultados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener pacientes menores: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()