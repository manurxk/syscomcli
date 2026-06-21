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
                    'foto_usuario': PerfilDao._obtenerFoto(id_usuario),
                    
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

    @staticmethod
    def _obtenerFoto(id_usuario):
        import os
        import glob
        from flask import current_app as app
        try:
            upload_folder = os.path.join(app.root_path, 'static', 'uploads', 'perfiles')
            pattern = os.path.join(upload_folder, f"perfil_{id_usuario}.*")
            matches = glob.glob(pattern)
            if matches:
                filename = os.path.basename(matches[0])
                return f"uploads/perfiles/{filename}"
        except Exception as e:
            app.logger.warning(f"Error al buscar foto: {str(e)}")
        return 'img/undraw_profile.svg'

    def updatePerfil(self, id_usuario, data):
        """ C Actualiza los datos personales del usuario """
        sql = """
        UPDATE personas
        SET per_telefono = %s,
            per_correo = %s,
            per_domicilio = %s
        WHERE id_persona = (
            SELECT f.id_persona 
            FROM funcionarios f 
            JOIN usuarios u ON f.id_funcionario = u.id_funcionario 
            WHERE u.id_usuario = %s
        )
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql, (data.get('telefono'), data.get('email'), data.get('direccion'), id_usuario))
            con.commit()
            return True
        except Exception as e:
            app.logger.error(f"Error al actualizar perfil: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateFoto(self, id_usuario, ruta_foto):
        """ La foto se guarda localmente y se lee dinámicamente en _obtenerFoto """
        return True

    def getEstadisticasUsuario(self, id_usuario, id_grupo):
        """ Retorna estadísticas básicas """
        return {
            "Accesos Recientes": 24,
            "Tareas Completadas": 12,
            "Días Activos": 45
        }

    def getActividadReciente(self, id_usuario, limite):
        """ Retorna la actividad reciente simulada """
        from datetime import datetime, timedelta
        hoy = datetime.now()
        actividad = [
            {
                "accion": "Inicio de sesión",
                "detalle": "Acceso exitoso al sistema",
                "fecha": hoy.strftime("%Y-%m-%dT%H:%M:%S"),
                "icono": "fas fa-sign-in-alt text-success"
            },
            {
                "accion": "Actualización de perfil",
                "detalle": "Modificó sus datos personales",
                "fecha": (hoy - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S"),
                "icono": "fas fa-user-edit text-primary"
            }
        ]
        return actividad