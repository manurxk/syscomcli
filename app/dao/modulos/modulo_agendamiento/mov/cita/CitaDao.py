# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CitaDao:

    def getCitas(self):
        citaSQL = """
       SELECT 
            c.id_cita, pm.nombre, pm.apellido, e.descripcion, t.descripcion, p.nombre, p.apellido, p.cedula, h.dis_horas, c.observacion, es.descripcion
                FROM  citas c, agenda_medicas a, personas pm, medicos m, especialidades e, turnos t, personas p, pacientes pa, disponibilidad_horaria h, estado_citas es
                where c.id_agenda_medica=a.id_agenda_medica and a.id_medico=m.id_medico and m.id_persona=pm.id_persona 
				and a.id_especialidad=e.id_especialidad and a.id_turno=t.id_turno and c.id_paciente=pa.id_paciente and pa.id_persona=p.id_persona 
				and c.id_estado_cita=es.id_estado_cita and c.id_hora=h.id_disponibilidad_horaria
            """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL)
            citas = cur.fetchall()
            return [{
                'id_cita':  cita[0], 'nombrem':  cita[1], 'apellidom': cita[2], 'especialidad':  cita[3], 'turno':  cita[4], 'nombrep':  cita[5],  'apellidop':  cita[6],'cedula':  cita[7], 'hora': cita[8], 'observacion': cita[9], 'estado': cita[10]} for cita in citas]
        
        except Exception as e:
            app.logger.error(f"Error al obtener todas las citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCitaById(self, id_cita):
        citaSQL = """
        SELECT 
              c.id_cita, pm.nombre, pm.apellido,e.descripcion,  t.descripcion, p.nombre, p.apellido, p.cedula, h.dis_horas, c.observacion, es.descripcion, c.id_agenda_medica, pm.id_persona, m.id_medico, a.id_especialidad, a.id_turno, p.id_persona, pa.id_paciente, h.id_disponibilidad_horaria, c.id_estado_cita
                FROM  citas c, agenda_medicas a, personas pm, medicos m, especialidades e, turnos t, personas p, pacientes pa, disponibilidad_horaria h, estado_citas es
                where c.id_agenda_medica=a.id_agenda_medica and a.id_medico=m.id_medico and m.id_persona=pm.id_persona 
				and a.id_especialidad=e.id_especialidad and a.id_turno=t.id_turno and c.id_paciente=pa.id_paciente and pa.id_persona=p.id_persona 
				and c.id_estado_cita=es.id_estado_cita and c.id_hora=h.id_disponibilidad_horaria and c.id_cita=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL, (id_cita,))
            citaEncontrada = cur.fetchone()
            if citaEncontrada:
                return {
                    "id_cita": citaEncontrada[0],
                    "nombrem": citaEncontrada[1],
                    "apellidom": citaEncontrada[2],
                    "especialidad": citaEncontrada[3],
                    "turno": citaEncontrada[4],
                    "nombrep": citaEncontrada[5],
                    "apellidop": citaEncontrada[6],
                    "cedula": citaEncontrada[7],
                    "hora":citaEncontrada[8],
                    "observacion": citaEncontrada[9],
                    "estado": citaEncontrada[10],
                    "id_agenda_medica": citaEncontrada[11],
                    "id_persona": citaEncontrada[12],
                    "id_medico": citaEncontrada[13],
                    "id_especialidad": citaEncontrada[14],
                    "id_turno": citaEncontrada[15],
                    "id_persona": citaEncontrada[16],
                    "id_paciente": citaEncontrada[17],
                    "id_disponibilidad_horaria": citaEncontrada[18],
                    "id_estado_cita": citaEncontrada[19]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener cita: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarCita(self, id_agenda_medica, id_paciente, observacion, id_estado_cita, id_hora,):
        insertCitaSQL = """
        INSERT INTO citas(id_agenda_medica, id_paciente, observacion, id_estado_cita, id_hora) VALUES(%s, %s, %s, %s,%s) RETURNING id_cita
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertCitaSQL, (id_agenda_medica, id_paciente, observacion, id_estado_cita, id_hora))
            cita_id = cur.fetchone()[0]
            con.commit()
            return cita_id
        except Exception as e:
            app.logger.error(f"Error al insertar cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def updateCita(self, id_cita, id_agenda_medica, id_paciente, observacion, id_estado_cita, id_hora):
        updateCitaSQL = """
        UPDATE citas
        SET id_agenda_medica=%s, id_paciente=%s, observacion=%s, id_estado_cita=%s, id_hora=%s
        WHERE id_cita=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateCitaSQL, ( id_agenda_medica, id_paciente, observacion, id_estado_cita, id_hora, id_cita))
            filas_afectadas = cur.rowcount
            con.commit()
            return filas_afectadas > 0
        except Exception as e:
            app.logger.error(f"Error al actualizar cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()

    def deleteCita(self, id_cita):
        deleteCitaSQL = """
        DELETE FROM citas
        WHERE id_cita=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(deleteCitaSQL, (id_cita,))
            rows_affected = cur.rowcount
            con.commit()
            return rows_affected > 0
        except Exception as e:
            app.logger.error(f"Error al eliminar  cita: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
