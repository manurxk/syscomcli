# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class PerfilDao:
    def getPerfilCompleto(self, id_usuario):
        """
        Obtiene todos los datos del perfil de un usuario
        Como todos los usuarios son funcionarios, usamos INNER JOIN
        """
        sql = """
        SELECT 
            u.id_usuario,
            u.usu_nick,
            u.usu_estado,
            u.creacion_fecha,
            p.per_telefono,
            p.per_correo,
            p.per_domicilio,
            p.per_nombre,
            p.per_apellido,
            p.per_cedula,
            p.per_fecha_nacimiento,
            g.des_grupo as rol,
            c.des_ciudad as ciudad,
            gen.des_genero as genero,
            ec.des_estado_civil as estado_civil,
            f.id_funcionario,
            f.fun_estado,
            car.des_cargo as cargo
        FROM usuarios u
        INNER JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
        INNER JOIN personas p ON f.id_persona = p.id_persona
        INNER JOIN grupos g ON u.id_grupo = g.id_grupo
        LEFT JOIN ciudades c ON p.id_ciudad = c.id_ciudad
        LEFT JOIN generos gen ON p.id_genero = gen.id_genero
        LEFT JOIN estados_civiles ec ON p.id_estado_civil = ec.id_estado_civil
        LEFT JOIN cargos car ON f.id_cargo = car.id_cargo
        WHERE u.id_usuario = %s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (id_usuario,))
            perfil = cur.fetchone()
            
            if perfil:
                return {
                    # Datos del Usuario
                    'nom_usuario': perfil[1],  # username para el frontend
                    'est_usuario': perfil[2],  # estado booleano
                    'foto_usuario': 'img/undraw_profile.svg',
                    
                    # Datos de la Persona
                    'nombre_completo': f"{perfil[7]} {perfil[8]}",
                    'ruc_persona': perfil[9],  # cédula/RUC
                    'fech_nac': perfil[10],  # fecha de nacimiento
                    'tel_persona': perfil[4],  # teléfono
                    'email_persona': perfil[5],  # email/correo
                    'dir_persona': perfil[6],  # dirección
                    
                    # Datos del Sistema
                    'rol': perfil[11],
                    'ciudad': perfil[12] or 'No especificada',
                    'genero': perfil[13] or 'No especificado',
                    'estado_civil': perfil[14] or 'No especificado',
                    
                    # Datos del Funcionario
                    'es_funcionario': True,
                    'cargo': perfil[17] or 'No asignado',
                    'especialidad': None,  # No existe la relación
                    'mat_funcionario': None,  # matrícula - no existe en BD
                }
            return None
        except Exception as e:
            app.logger.error(f"Error al obtener perfil completo: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()