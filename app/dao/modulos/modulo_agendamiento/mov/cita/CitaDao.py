# Data access object - DAO
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CitaDao:

    def getCitas(self):
        citaSQL = """
            SELECT 
                    c.id_cita, 
                    pm.nombre, 
                    pm.apellido, 
                    e.descripcion, 
                    t.descripcion, 
                    p.nombre, 
                    p.apellido, 
                    p.cedula, 
                    c.fecha_cita,
                    h.descripcion,            -- id de la tabla horas
                    c.observacion, 
                    es.descripcion
                FROM 
                    citas c, 
                    agenda_medicas a, 
                    personas pm, 
                    medicos m, 
                    especialidades e, 
                    turnos t, 
                    personas p, 
                    pacientes pa, 
                    horas h,                 -- cambio de disponibilidad_horaria a horas
                    estado_citas es
                WHERE 
                    c.id_agenda_medica = a.id_agenda_medica 
                    AND a.id_medico = m.id_medico 
                    AND m.id_persona = pm.id_persona 
                    AND a.id_especialidad = e.id_especialidad 
                    AND a.id_turno = t.id_turno 
                    AND c.id_paciente = pa.id_paciente 
                    AND pa.id_persona = p.id_persona 
                    AND c.id_estado_cita = es.id_estado_cita 
                    AND c.id = h.id; 

            """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(citaSQL)
            citas = cur.fetchall()
            return [{
                'id_cita':  cita[0], 'nombrem':  cita[1], 'apellidom': cita[2], 'especialidad':  cita[3], 'turno':  cita[4], 'nombrep':  cita[5],  'apellidop':  cita[6],'cedula':  cita[7], 'fecha_cita': cita[8].strftime('%d/%m/%Y'), 'hora': cita[9], 'observacion': cita[10], 'estado': cita[11]} for cita in citas]
        
        except Exception as e:
            app.logger.error(f"Error al obtener todas las citas: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()

    def getCitaById(self, id_cita):
        citaSQL = """
        SELECT 
              c.id_cita, pm.nombre, pm.apellido,e.descripcion,  t.descripcion, p.nombre, p.apellido, p.cedula, fecha_cita, h.dis_horas, c.observacion, es.descripcion, c.id_agenda_medica, pm.id_persona, m.id_medico, a.id_especialidad, a.id_turno, p.id_persona, pa.id_paciente, h.id_disponibilidad_horaria, c.id_estado_cita
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
                    "fecha_cita": citaEncontrada[8],
                    "hora":citaEncontrada[9],
                    "observacion": citaEncontrada[10],
                    "estado": citaEncontrada[11],
                    "id_agenda_medica": citaEncontrada[12],
                    "id_persona": citaEncontrada[13],
                    "id_medico": citaEncontrada[14],
                    "id_especialidad": citaEncontrada[15],
                    "id_turno": citaEncontrada[16],
                    "id_persona": citaEncontrada[17],
                    "id_paciente": citaEncontrada[18],
                    "id_disponibilidad_horaria": citaEncontrada[19],
                    "id_estado_cita": citaEncontrada[20]
                }
            else:
                return None
        except Exception as e:
            app.logger.error(f"Error al obtener cita: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def guardarCita(self, id_agenda_medica, id_paciente, fecha_cita, id_hora, observacion, id_estado_cita, ):
        insertCitaSQL = """
        INSERT INTO citas(id_agenda_medica, id_paciente, fecha_cita,  id_hora, observacion, id_estado_cita) VALUES(%s, %s, %s, %s, %s,%s) RETURNING id_cita
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(insertCitaSQL, (id_agenda_medica, id_paciente, fecha_cita, id_hora, observacion, id_estado_cita))
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

    def updateCita(self, id_cita, id_agenda_medica, id_paciente, fecha_cita, id_hora, observacion, id_estado_cita):
        updateCitaSQL = """
        UPDATE citas
        SET id_agenda_medica=%s, id_paciente=%s, fecha_cita = %s,  id_hora=%s, observacion=%s, id_estado_cita=%s
        WHERE id_cita=%s
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(updateCitaSQL, ( id_agenda_medica, id_paciente, fecha_cita, id_hora, observacion, id_estado_cita,  id_cita))
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
