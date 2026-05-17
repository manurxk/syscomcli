from flask import current_app as app
from app.conexion.Conexion import Conexion
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes

class BusquedaDao:
    """
    DAO para búsqueda global en el sistema.
    Busca en pacientes, especialistas/funcionarios y referenciales.
    """
    
    def buscarGlobal(self, termino_busqueda, limite=20):
        """
        Realiza una búsqueda global en múltiples entidades del sistema.
        
        Args:
            termino_busqueda: Término a buscar
            limite: Número máximo de resultados por categoría (default: 20)
        
        Returns:
            dict con resultados agrupados por categoría
        """
        if not termino_busqueda or len(termino_busqueda.strip()) < 2:
            return {
                'pacientes': [],
                'especialistas': [],
                'referenciales': []
            }
        
        termino = f"%{termino_busqueda.strip().upper()}%"
        
        resultados = {
            'pacientes': self._buscarPacientes(termino, limite),
            'especialistas': self._buscarEspecialistas(termino, limite),
            'referenciales': self._buscarReferenciales(termino, limite)
        }
        
        return resultados
    
    def _buscarPacientes(self, termino, limite):
        """Busca pacientes por nombre, apellido, cédula o historia clínica"""
        # Verificar si debe filtrar por especialista
        id_especialista = None
        puede_ver_todos = puede_ver_todos_pacientes()
        
        if not puede_ver_todos:
            id_especialista = obtener_id_especialista_usuario()
        
        pacientesSQL = """
            SELECT DISTINCT
                pac.id_paciente,
                pac.pac_historia_clinica,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                p.per_cedula,
                p.per_telefono
            FROM pacientes pac
            JOIN personas p ON pac.id_persona = p.id_persona
        """
        
        if id_especialista:
            pacientesSQL += """
                INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
                WHERE (UPPER(p.per_nombre) LIKE %s 
                    OR UPPER(p.per_apellido) LIKE %s
                    OR UPPER(p.per_cedula) LIKE %s
                    OR UPPER(pac.pac_historia_clinica) LIKE %s)
                    AND pp.id_especialista = %s AND pp.activo = TRUE
            """
        else:
            pacientesSQL += """
                WHERE UPPER(p.per_nombre) LIKE %s 
                    OR UPPER(p.per_apellido) LIKE %s
                    OR UPPER(p.per_cedula) LIKE %s
                    OR UPPER(pac.pac_historia_clinica) LIKE %s
            """
        
        pacientesSQL += " ORDER BY p.per_nombre, p.per_apellido LIMIT %s"
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            if id_especialista:
                cur.execute(pacientesSQL, (termino, termino, termino, termino, id_especialista, limite))
            else:
                cur.execute(pacientesSQL, (termino, termino, termino, termino, limite))
            
            pacientes = cur.fetchall()
            
            return [{
                'id': p[0],
                'historia_clinica': p[1] if p[1] else 'Sin historia',
                'nombre_completo': p[2] if p[2] else 'Sin nombre',
                'cedula': p[3] if p[3] else 'Sin cédula',
                'telefono': p[4] if p[4] else 'Sin teléfono',
                'tipo': 'paciente',
                'url': f'/modulos/paciente/{p[0]}'
            } for p in pacientes]
            
        except Exception as e:
            app.logger.error(f"Error al buscar pacientes: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def _buscarEspecialistas(self, termino, limite):
        """Busca especialistas/funcionarios por nombre, apellido, cédula o matrícula"""
        especialistasSQL = """
            SELECT DISTINCT
                e.id_especialista,
                f.id_funcionario,
                p.per_nombre || ' ' || p.per_apellido AS nombre_completo,
                p.per_cedula,
                COALESCE(e.esp_matricula, '') AS matricula,
                STRING_AGG(DISTINCT esp.des_especialidad, ', ') AS especialidades
            FROM funcionarios f
            JOIN personas p ON f.id_persona = p.id_persona
            LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
            LEFT JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista
            LEFT JOIN especialidades esp ON ee.id_especialidad = esp.id_especialidad AND esp.est_especialidad = TRUE
            WHERE f.fun_estado = TRUE
                AND (UPPER(p.per_nombre) LIKE %s 
                    OR UPPER(p.per_apellido) LIKE %s
                    OR UPPER(p.per_cedula) LIKE %s
                    OR UPPER(COALESCE(e.esp_matricula, '')) LIKE %s)
            GROUP BY e.id_especialista, f.id_funcionario, p.per_nombre, p.per_apellido, 
                     p.per_cedula, e.esp_matricula
            ORDER BY p.per_nombre, p.per_apellido
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(especialistasSQL, (termino, termino, termino, termino, limite))
            especialistas = cur.fetchall()
            
            return [{
                'id': e[0] if e[0] else e[1],  # id_especialista o id_funcionario
                'id_funcionario': e[1],
                'nombre_completo': e[2] if e[2] else 'Sin nombre',
                'cedula': e[3] if e[3] else 'Sin cédula',
                'matricula': e[4] if e[4] else '',
                'especialidades': e[5] if e[5] else 'Sin especialidades',
                'tipo': 'especialista',
                'url': f'/modulos/funcionario/{e[1]}'
            } for e in especialistas]
            
        except Exception as e:
            app.logger.error(f"Error al buscar especialistas: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()
    
    def _buscarReferenciales(self, termino, limite):
        """Busca en referenciales: ciudades, especialidades, consultorios"""
        referencialesSQL = """
            (
                SELECT 'ciudad' AS tipo, id_ciudad AS id, des_ciudad AS nombre, NULL AS descripcion_extra
                FROM ciudades
                WHERE est_ciudad = TRUE AND UPPER(des_ciudad) LIKE %s
                LIMIT %s
            )
            UNION ALL
            (
                SELECT 'especialidad' AS tipo, id_especialidad AS id, des_especialidad AS nombre, NULL AS descripcion_extra
                FROM especialidades
                WHERE est_especialidad = TRUE AND UPPER(des_especialidad) LIKE %s
                LIMIT %s
            )
            UNION ALL
            (
                SELECT 'consultorio' AS tipo, id_consultorio AS id, des_consultorio AS nombre, NULL AS descripcion_extra
                FROM consultorios
                WHERE est_consultorio = TRUE AND UPPER(des_consultorio) LIKE %s
                LIMIT %s
            )
            ORDER BY tipo, nombre
            LIMIT %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            limite_por_tipo = limite // 3  # Dividir el límite entre los tipos
            cur.execute(referencialesSQL, (
                termino, limite_por_tipo,
                termino, limite_por_tipo,
                termino, limite_por_tipo,
                limite
            ))
            
            referenciales = cur.fetchall()
            
            resultados = []
            for r in referenciales:
                tipo = r[0]
                id_ref = r[1]
                nombre = r[2] if r[2] else 'Sin nombre'
                
                # Construir URL según el tipo
                if tipo == 'ciudad':
                    url = f'/referenciales/ciudad/{id_ref}'
                elif tipo == 'especialidad':
                    url = f'/referenciales/especialidad/{id_ref}'
                elif tipo == 'consultorio':
                    url = f'/referenciales/consultorio/{id_ref}'
                else:
                    url = '#'
                
                resultados.append({
                    'id': id_ref,
                    'nombre': nombre,
                    'tipo': tipo,
                    'tipo_display': tipo.capitalize(),
                    'url': url
                })
            
            return resultados
            
        except Exception as e:
            app.logger.error(f"Error al buscar referenciales: {str(e)}", exc_info=True)
            return []
        finally:
            cur.close()
            con.close()



