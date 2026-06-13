# app/dao/AnamnesisDao.py
from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime
import json

class AnamnesisDao:
    
    def validar_paciente_existe(self, pac_id):
        """Valida que el paciente exista antes de crear/actualizar anamnesis"""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("SELECT id_paciente FROM pacientes WHERE id_paciente = %s", (pac_id,))
            existe = cur.fetchone() is not None
            
            if not existe:
                app.logger.error(f"Paciente con ID {pac_id} no existe")
            
            return existe
            
        except Exception as e:
            app.logger.error(f"Error validando existencia de paciente: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def tiene_anamnesis_activa(self, pac_id):
        """Verifica si el paciente ya tiene una anamnesis activa"""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("""
                SELECT id_anamnesis FROM anamnesis 
                WHERE id_paciente = %s
                ORDER BY id_anamnesis DESC
                LIMIT 1
            """, (pac_id,))
            
            resultado = cur.fetchone()
            return resultado[0] if resultado else None
            
        except Exception as e:
            app.logger.error(f"Error verificando anamnesis activa: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getAnamnesisByPaciente(self, pac_id):
        """Obtiene la anamnesis más reciente de un paciente con datos completos"""
        anamnesisSQL = """
            SELECT
                a.id_anamnesis,
                a.id_paciente,
                a.informante,
                a.relacion_informante,
                a.motivo_consulta,
                a.fecha_creacion,
                a.fecha_modificacion,
                a.antecedentes_familiares_similares,
                a.antecedentes_patologicos_familiares,
                a.componentes_familiares,
                a.historia_familiar,
                a.antecedentes_patologicos_personales,
                a.historia_problema_actual,
                a.historia_desarrollo,
                a.historia_academica,
                a.historia_laboral,
                a.historia_rehabilitacion,
                a.medicacion_actual,
                a.medicacion_psiquiatrica_previa,
                a.consumo_sustancias,
                a.relaciones_interpersonales,
                a.actividad_fisica,
                a.patron_sueno,
                a.patron_alimentacion,
                a.actividad_emocional,
                a.actividad_sexual,
                a.impresion_diagnostica,
                a.plan_trabajo,
                a.eval_neuropsicologica,
                a.eval_psicologica,
                a.eval_psicopedagogica,
                a.eval_fonoaudiologica,
                a.eval_psicomotora,
                a.terapia_individual,
                a.terapia_familiar,
                a.terapia_grupal,
                a.terapia_ocupacional,
                a.otra_terapia,
                a.observaciones,
                a.indicaciones,
                a.usuario_modificacion,
                a.version,
                p.per_nombre || ' ' || p.per_apellido AS nombre_paciente,
                pac.pac_historia_clinica
            FROM anamnesis a
            JOIN pacientes pac ON a.id_paciente = pac.id_paciente
            JOIN personas p ON pac.id_persona = p.id_persona
            WHERE a.id_paciente = %s
            ORDER BY a.id_anamnesis DESC
            LIMIT 1
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(anamnesisSQL, (pac_id,))
            a = cur.fetchone()
            
            if not a:
                app.logger.info(f"No existe anamnesis para paciente ID: {pac_id}")
                return None
            
            return {
                'id_anamnesis': a[0],
                'id_paciente': a[1],
                'informante': a[2],
                'relacion_informante': a[3],
                'motivo_consulta': a[4],
                'fecha_elaboracion': a[5].strftime('%d/%m/%Y %H:%M') if a[5] else None,
                'fecha_ultima_modificacion': a[6].strftime('%d/%m/%Y %H:%M') if a[6] else None,
                'antecedentes_familiares_similares': a[7],
                'antecedentes_patologicos_familiares': a[8],
                'componentes_familiares': a[9],
                'historia_familiar': a[10],
                'antecedentes_patologicos_personales': a[11],
                'historia_problema_actual': a[12],
                'historia_desarrollo': a[13],
                'historia_academica': a[14],
                'historia_laboral': a[15],
                'historia_rehabilitacion': a[16],
                'medicacion_actual': a[17],
                'medicacion_psiquiatrica_previa': a[18],
                'consumo_sustancias': a[19],
                'relaciones_interpersonales': a[20],
                'actividad_fisica': a[21],
                'patron_sueno': a[22],
                'patron_alimentacion': a[23],
                'actividad_emocional': a[24],
                'actividad_sexual': a[25],
                'impresion_diagnostica': a[26],
                'plan_trabajo': a[27],
                'eval_neuropsicologica': a[28],
                'eval_psicologica': a[29],
                'eval_psicopedagogica': a[30],
                'eval_fonoaudiologica': a[31],
                'eval_psicomotora': a[32],
                'terapia_individual': a[33],
                'terapia_familiar': a[34],
                'terapia_grupal': a[35],
                'terapia_ocupacional': a[36],
                'otra_terapia': a[37],
                'observaciones': a[38],
                'indicaciones': a[39],
                'usuario_modificacion': a[40],
                'version': a[41],
                'nombre_paciente': a[42],
                'historia_clinica': a[43]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener anamnesis por paciente: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getAnamnesisById(self, anamnesis_id):
        """Obtiene una anamnesis específica por su ID"""
        anamnesisSQL = """
            SELECT
                a.*,
                p.per_nombre || ' ' || p.per_apellido AS nombre_paciente,
                pac.pac_historia_clinica
            FROM anamnesis a
            JOIN pacientes pac ON a.id_paciente = pac.id_paciente
            JOIN personas p ON pac.id_persona = p.id_persona
            WHERE a.id_anamnesis = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(anamnesisSQL, (anamnesis_id,))
            resultado = cur.fetchone()
            
            if not resultado:
                return None
            
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, resultado))
            
        except Exception as e:
            app.logger.error(f"Error al obtener anamnesis por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarAnamnesis(self, pac_id, motivo_consulta, usuario_id, 
                        informante=None, relacion_informante=None,
                        antecedentes_familiares_similares=None,
                        antecedentes_patologicos_familiares=None,
                        componentes_familiares=None,
                        historia_familiar=None,
                        antecedentes_patologicos_personales=None,
                        historia_problema_actual=None,
                        historia_desarrollo=None,
                        historia_academica=None,
                        historia_laboral=None,
                        historia_rehabilitacion=None,
                        medicacion_actual=None,
                        medicacion_psiquiatrica_previa=None,
                        consumo_sustancias=None,
                        relaciones_interpersonales=None,
                        actividad_fisica=None,
                        patron_sueno=None,
                        patron_alimentacion=None,
                        actividad_emocional=None,
                        actividad_sexual=None,
                        impresion_diagnostica=None,
                        plan_trabajo=None,
                        eval_neuropsicologica=False,
                        eval_psicologica=False,
                        eval_psicopedagogica=False,
                        eval_fonoaudiologica=False,
                        eval_psicomotora=False,
                        terapia_individual=False,
                        terapia_familiar=False,
                        terapia_grupal=False,
                        terapia_ocupacional=False,
                        otra_terapia=None,
                        observaciones=None,
                        indicaciones=None):
        """
        Guarda una nueva anamnesis para un paciente.
        Campos obligatorios: pac_id, motivo_consulta, usuario_id
        """
        
        if not all([pac_id, motivo_consulta, usuario_id]):
            app.logger.error("Faltan campos obligatorios: pac_id, motivo_consulta, usuario_id")
            return None
        
        if not self.validar_paciente_existe(pac_id):
            return None
        
        anamnesis_existente = self.tiene_anamnesis_activa(pac_id)
        if anamnesis_existente:
            app.logger.warning(f"Paciente {pac_id} ya tiene anamnesis activa (ID: {anamnesis_existente})")
            return None
        
        insertAnamnesisSQL = """
            INSERT INTO anamnesis(
                id_paciente, informante, relacion_informante, motivo_consulta,
                antecedentes_familiares_similares, antecedentes_patologicos_familiares,
                componentes_familiares, historia_familiar,
                antecedentes_patologicos_personales, historia_problema_actual, historia_desarrollo,
                historia_academica, historia_laboral, historia_rehabilitacion,
                medicacion_actual, medicacion_psiquiatrica_previa, consumo_sustancias,
                relaciones_interpersonales, actividad_fisica, patron_sueno, patron_alimentacion,
                actividad_emocional, actividad_sexual,
                impresion_diagnostica, plan_trabajo,
                eval_neuropsicologica, eval_psicologica, eval_psicopedagogica,
                eval_fonoaudiologica, eval_psicomotora,
                terapia_individual, terapia_familiar, terapia_grupal,
                terapia_ocupacional, otra_terapia,
                observaciones, indicaciones,
                elaborado_por, version, activo
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, TRUE
            ) RETURNING id_anamnesis
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando nueva anamnesis para paciente ID: {pac_id}")
            
            cur.execute(insertAnamnesisSQL, (
                pac_id, informante, relacion_informante, motivo_consulta,
                antecedentes_familiares_similares, antecedentes_patologicos_familiares,
                componentes_familiares, historia_familiar,
                antecedentes_patologicos_personales, historia_problema_actual, historia_desarrollo,
                historia_academica, historia_laboral, historia_rehabilitacion,
                medicacion_actual, medicacion_psiquiatrica_previa, consumo_sustancias,
                relaciones_interpersonales, actividad_fisica, patron_sueno, patron_alimentacion,
                actividad_emocional, actividad_sexual,
                impresion_diagnostica, plan_trabajo,
                eval_neuropsicologica, eval_psicologica, eval_psicopedagogica,
                eval_fonoaudiologica, eval_psicomotora,
                terapia_individual, terapia_familiar, terapia_grupal,
                terapia_ocupacional, otra_terapia,
                observaciones, indicaciones,
                usuario_id, 1
            ))
            
            anamnesis_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Anamnesis creada exitosamente con ID: {anamnesis_id}")
            return anamnesis_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al insertar anamnesis: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def updateAnamnesis(self, anamnesis_id, usuario_id, motivo_consulta=None,
                       informante=None, relacion_informante=None,
                       antecedentes_familiares_similares=None,
                       antecedentes_patologicos_familiares=None,
                       componentes_familiares=None,
                       historia_familiar=None,
                       antecedentes_patologicos_personales=None,
                       historia_problema_actual=None,
                       historia_desarrollo=None,
                       historia_academica=None,
                       historia_laboral=None,
                       historia_rehabilitacion=None,
                       medicacion_actual=None,
                       medicacion_psiquiatrica_previa=None,
                       consumo_sustancias=None,
                       relaciones_interpersonales=None,
                       actividad_fisica=None,
                       patron_sueno=None,
                       patron_alimentacion=None,
                       actividad_emocional=None,
                       actividad_sexual=None,
                       impresion_diagnostica=None,
                       plan_trabajo=None,
                       eval_neuropsicologica=False,
                       eval_psicologica=False,
                       eval_psicopedagogica=False,
                       eval_fonoaudiologica=False,
                       eval_psicomotora=False,
                       terapia_individual=False,
                       terapia_familiar=False,
                       terapia_grupal=False,
                       terapia_ocupacional=False,
                       otra_terapia=None,
                       observaciones=None,
                       indicaciones=None,
                       guardar_historial=True):
        """
        Actualiza una anamnesis existente.
        Si guardar_historial=True, guarda la versión anterior en anamnesis_historial
        """
        
        if not all([anamnesis_id, usuario_id]):
            app.logger.error("Faltan campos obligatorios: anamnesis_id, usuario_id")
            return False
        
        if guardar_historial:
            self._guardar_en_historial(anamnesis_id, usuario_id)
        
        updateAnamnesisSQL = """
            UPDATE anamnesis SET
                informante = %s,
                relacion_informante = %s,
                motivo_consulta = COALESCE(%s, motivo_consulta),
                fecha_ultima_modificacion = CURRENT_TIMESTAMP,
                antecedentes_familiares_similares = %s,
                antecedentes_patologicos_familiares = %s,
                componentes_familiares = %s,
                historia_familiar = %s,
                antecedentes_patologicos_personales = %s,
                historia_problema_actual = %s,
                historia_desarrollo = %s,
                historia_academica = %s,
                historia_laboral = %s,
                historia_rehabilitacion = %s,
                medicacion_actual = %s,
                medicacion_psiquiatrica_previa = %s,
                consumo_sustancias = %s,
                relaciones_interpersonales = %s,
                actividad_fisica = %s,
                patron_sueno = %s,
                patron_alimentacion = %s,
                actividad_emocional = %s,
                actividad_sexual = %s,
                impresion_diagnostica = %s,
                plan_trabajo = %s,
                eval_neuropsicologica = %s,
                eval_psicologica = %s,
                eval_psicopedagogica = %s,
                eval_fonoaudiologica = %s,
                eval_psicomotora = %s,
                terapia_individual = %s,
                terapia_familiar = %s,
                terapia_grupal = %s,
                terapia_ocupacional = %s,
                otra_terapia = %s,
                observaciones = %s,
                indicaciones = %s,
                usuario_modificacion = %s,
                fecha_modificacion = CURRENT_TIMESTAMP,
                version = version + 1
            WHERE id_anamnesis = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Actualizando anamnesis ID: {anamnesis_id}")
            
            cur.execute(updateAnamnesisSQL, (
                informante, relacion_informante, motivo_consulta,
                antecedentes_familiares_similares, antecedentes_patologicos_familiares,
                componentes_familiares, historia_familiar,
                antecedentes_patologicos_personales, historia_problema_actual, historia_desarrollo,
                historia_academica, historia_laboral, historia_rehabilitacion,
                medicacion_actual, medicacion_psiquiatrica_previa, consumo_sustancias,
                relaciones_interpersonales, actividad_fisica, patron_sueno, patron_alimentacion,
                actividad_emocional, actividad_sexual,
                impresion_diagnostica, plan_trabajo,
                eval_neuropsicologica, eval_psicologica, eval_psicopedagogica,
                eval_fonoaudiologica, eval_psicomotora,
                terapia_individual, terapia_familiar, terapia_grupal,
                terapia_ocupacional, otra_terapia,
                observaciones, indicaciones,
                usuario_id, anamnesis_id
            ))
            
            con.commit()
            app.logger.info(f"Anamnesis {anamnesis_id} actualizada exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar anamnesis: {str(e)}", exc_info=True)
            return False
        finally:
            cur.close()
            con.close()
    
    def _guardar_en_historial(self, anamnesis_id, usuario_id):
        """
        Guarda una copia de la anamnesis actual en la tabla de historial (privado)
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute("SELECT * FROM anamnesis WHERE id_anamnesis = %s", (anamnesis_id,))
            columnas = [desc[0] for desc in cur.description]
            datos = cur.fetchone()
            
            if not datos:
                return False
            
            datos_dict = dict(zip(columnas, datos))
            
            for key, value in datos_dict.items():
                if isinstance(value, datetime):
                    datos_dict[key] = value.isoformat()
            
            contenido_json = json.dumps(datos_dict)
            
            insertHistorialSQL = """
                INSERT INTO anamnesis_historial(
                    id_anamnesis, version, contenido_json, usuario_modificacion
                ) VALUES (%s, %s, %s, %s)
            """
            
            cur.execute(insertHistorialSQL, (
                anamnesis_id,
                datos_dict.get('version', 1),
                contenido_json,
                usuario_id
            ))
            
            con.commit()
            app.logger.info(f"Versión guardada en historial para anamnesis ID: {anamnesis_id}")
            return True
            
        except Exception as e:
            app.logger.error(f"Error al guardar en historial: {str(e)}")
            con.rollback()
            return False
        finally:
            cur.close()
            con.close()
    
    def getHistorialAnamnesis(self, anamnesis_id):
        """Obtiene todas las versiones históricas de una anamnesis"""
        historialSQL = """
            SELECT
                h.id_historial,
                h.version,
                h.contenido_json,
                h.fecha_modificacion,
                h.comentario_cambio,
                pf.per_nombre || ' ' || pf.per_apellido AS modificado_por_nombre
            FROM anamnesis_historial h
            LEFT JOIN usuarios u ON h.modificado_por = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas pf ON f.id_persona = pf.id_persona
            WHERE h.id_anamnesis = %s
            ORDER BY h.version DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(historialSQL, (anamnesis_id,))
            resultados = cur.fetchall()
            
            return [{
                'id_historial': r[0],
                'version': r[1],
                'contenido_json': r[2],
                'fecha_modificacion': r[3].strftime('%d/%m/%Y %H:%M') if r[3] else None,
                'comentario_cambio': r[4],
                'modificado_por_nombre': r[5]
            } for r in resultados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener historial de anamnesis: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def archivarAnamnesis(self, anamnesis_id, usuario_id):
        """
        Marca una anamnesis como inactiva (archivada)
        Permite crear una nueva anamnesis para el mismo paciente
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Archivando anamnesis ID: {anamnesis_id}")
            
            self._guardar_en_historial(anamnesis_id, usuario_id)
            
            cur.execute("""
                UPDATE anamnesis 
                SET usuario_modificacion = %s,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_anamnesis = %s
            """, (usuario_id, anamnesis_id))
            
            con.commit()
            app.logger.info(f"Anamnesis {anamnesis_id} archivada exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al archivar anamnesis: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteAnamnesis(self, anamnesis_id):
        """
        Elimina permanentemente una anamnesis (usar con precaución)
        Elimina también su historial por CASCADE
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.warning(f"ELIMINACIÓN PERMANENTE de anamnesis ID: {anamnesis_id}")
            
            cur.execute("DELETE FROM anamnesis WHERE id_anamnesis = %s", (anamnesis_id,))
            
            con.commit()
            app.logger.info(f"Anamnesis {anamnesis_id} eliminada permanentemente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar anamnesis: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def getAllAnamnesis(self):
        """Obtiene todas las anamnesis (para listados)"""
        anamnesisSQL = """
            SELECT
                a.id_anamnesis,
                a.id_paciente,
                p.per_nombre || ' ' || p.per_apellido AS nombre_paciente,
                pac.pac_historia_clinica,
                a.motivo_consulta,
                a.fecha_creacion,
                a.fecha_modificacion,
                a.version,
                a.usuario_creacion
            FROM anamnesis a
            JOIN pacientes pac ON a.id_paciente = pac.id_paciente
            JOIN personas p ON pac.id_persona = p.id_persona
            ORDER BY a.fecha_creacion DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(anamnesisSQL)
            resultados = cur.fetchall()
            
            return [{
                'id_anamnesis': r[0],
                'id_paciente': r[1],
                'nombre_paciente': r[2],
                'historia_clinica': r[3],
                'motivo_consulta': r[4][:100] + '...' if r[4] and len(r[4]) > 100 else r[4],
                'fecha_elaboracion': r[5].strftime('%d/%m/%Y') if r[5] else None,
                'fecha_ultima_modificacion': r[6].strftime('%d/%m/%Y') if r[6] else None,
                'version': r[7],
                'elaborado_por_nombre': r[8]
            } for r in resultados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todas las anamnesis: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()