from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class CertificadoMedicoDao:
    """DAO para gestionar certificados médicos"""
    
    def getAllCertificadosMedicos(self):
        """Obtiene todos los certificados médicos con sus datos completos"""
        certificadoSQL = """
            SELECT
                c.id_certificado,
                c.id_consulta,
                c.id_paciente,
                c.id_profesional,
                c.certificado_numero,
                c.certificado_fecha,
                c.id_tipo_certificado,
                tc.des_tipo_certificado AS tipo_certificado_nombre,
                c.certificado_dias_reposo,
                c.certificado_desde_fecha,
                c.certificado_hasta_fecha,
                c.certificado_motivo,
                c.certificado_diagnostico,
                c.certificado_recomendaciones,
                c.certificado_estado,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                c.fecha_creacion
            FROM certificados_medicos c
            JOIN pacientes pac ON c.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN tipos_certificados_medicos tc ON c.id_tipo_certificado = tc.id_tipo_certificado
            WHERE c.est_certificado = 'A'
            ORDER BY c.certificado_fecha DESC, c.id_certificado DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(certificadoSQL)
            certificados = cur.fetchall()
            
            return [{
                'id_certificado': cert[0],
                'id_consulta': cert[1],
                'id_paciente': cert[2],
                'id_profesional': cert[3],
                'certificado_numero': cert[4],
                'certificado_fecha': cert[5].strftime('%d/%m/%Y') if cert[5] else None,
                'id_tipo_certificado': cert[6],
                'certificado_tipo': cert[7] or 'N/A',  # Nombre del tipo para compatibilidad
                'tipo_certificado_nombre': cert[7] or 'N/A',
                'certificado_dias_reposo': cert[8],
                'certificado_desde_fecha': cert[9].strftime('%d/%m/%Y') if cert[9] else None,
                'certificado_hasta_fecha': cert[10].strftime('%d/%m/%Y') if cert[10] else None,
                'certificado_motivo': cert[11],
                'certificado_diagnostico': cert[12],
                'certificado_recomendaciones': cert[13],
                'certificado_estado': cert[14],
                'historia_clinica': cert[15],
                'paciente_nombre': cert[16],
                'paciente_cedula': cert[17],
                'profesional_nombre': cert[18],
                'profesional_matricula': cert[19],
                'fecha_registro': cert[20].strftime('%d/%m/%Y') if cert[20] else None
            } for cert in certificados]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los certificados médicos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCertificadoMedicoById(self, id_certificado):
        """Obtiene un certificado médico específico por ID"""
        certificadoSQL = """
            SELECT
                c.id_certificado,
                c.id_consulta,
                c.id_paciente,
                c.id_profesional,
                c.certificado_numero,
                c.certificado_fecha,
                c.id_tipo_certificado,
                tc.des_tipo_certificado AS tipo_certificado_nombre,
                c.certificado_dias_reposo,
                c.certificado_desde_fecha,
                c.certificado_hasta_fecha,
                c.certificado_motivo,
                c.certificado_diagnostico,
                c.certificado_recomendaciones,
                c.certificado_estado,
                c.est_certificado,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                c.fecha_creacion,
                c.usuario_creacion
            FROM certificados_medicos c
            JOIN pacientes pac ON c.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON c.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            LEFT JOIN tipos_certificados_medicos tc ON c.id_tipo_certificado = tc.id_tipo_certificado
            WHERE c.id_certificado = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(certificadoSQL, (id_certificado,))
            cert = cur.fetchone()
            
            if not cert:
                return None
            
            return {
                'id_certificado': cert[0],
                'id_consulta': cert[1],
                'id_paciente': cert[2],
                'id_profesional': cert[3],
                'certificado_numero': cert[4],
                'certificado_fecha': cert[5].strftime('%Y-%m-%d') if cert[5] else None,
                'id_tipo_certificado': cert[6],
                'certificado_tipo': cert[7] or 'N/A',  # Nombre del tipo para compatibilidad
                'tipo_certificado_nombre': cert[7] or 'N/A',
                'certificado_dias_reposo': cert[8],
                'certificado_desde_fecha': cert[9].strftime('%Y-%m-%d') if cert[9] else None,
                'certificado_hasta_fecha': cert[10].strftime('%Y-%m-%d') if cert[10] else None,
                'certificado_motivo': cert[11],
                'certificado_diagnostico': cert[12],
                'certificado_recomendaciones': cert[13],
                'certificado_estado': cert[14],
                'activo': cert[15] == 'A',
                'historia_clinica': cert[16],
                'paciente_nombre': cert[17],
                'paciente_cedula': cert[18],
                'paciente_telefono': cert[19],
                'profesional_nombre': cert[20],
                'profesional_matricula': cert[21],
                'fecha_registro': cert[22].strftime('%Y-%m-%d') if cert[22] else None,
                'usuario_creacion': cert[23]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener certificado médico por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarCertificadoMedico(self, id_paciente, id_profesional, certificado_fecha,
                                id_tipo_certificado, certificado_motivo,
                                id_consulta=None, certificado_dias_reposo=None,
                                certificado_desde_fecha=None, certificado_hasta_fecha=None,
                                certificado_diagnostico=None, certificado_recomendaciones=None,
                                certificado_estado='VIGENTE', usuario_creacion='ADMIN'):
        """Guarda un nuevo certificado médico"""
        
        if not all([id_paciente, id_profesional, certificado_fecha, id_tipo_certificado, certificado_motivo]):
            app.logger.error("Faltan campos obligatorios para guardar certificado médico")
            return None
        
        # Generar número de certificado si no se proporciona
        certificado_numero = self._generarNumeroCertificado()
        
        insertCertificadoSQL = """
            INSERT INTO certificados_medicos(
                id_consulta, id_paciente, id_profesional, certificado_numero,
                certificado_fecha, id_tipo_certificado, certificado_dias_reposo,
                certificado_desde_fecha, certificado_hasta_fecha, certificado_motivo,
                certificado_diagnostico, certificado_recomendaciones, certificado_estado,
                est_certificado, usuario_creacion
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'A', %s)
            RETURNING id_certificado
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando certificado médico para paciente ID: {id_paciente}")
            
            cur.execute(insertCertificadoSQL, (
                id_consulta,
                id_paciente,
                id_profesional,
                certificado_numero,
                certificado_fecha,
                id_tipo_certificado,
                certificado_dias_reposo,
                certificado_desde_fecha,
                certificado_hasta_fecha,
                certificado_motivo,
                certificado_diagnostico,
                certificado_recomendaciones,
                certificado_estado,
                usuario_creacion
            ))
            
            certificado_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Certificado médico guardado exitosamente con ID: {certificado_id}")
            return certificado_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar certificado médico: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroCertificado(self):
        """Genera un número único de certificado médico"""
        año_actual = date.today().year
        
        selectSQL = """
            SELECT MAX(CAST(SUBSTRING(certificado_numero FROM '[0-9]+$') AS INTEGER))
            FROM certificados_medicos
            WHERE certificado_numero LIKE %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            patron = f'CERT-{año_actual}-%'
            cur.execute(selectSQL, (patron,))
            resultado = cur.fetchone()
            
            siguiente_numero = (resultado[0] or 0) + 1
            return f'CERT-{año_actual}-{str(siguiente_numero).zfill(4)}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de certificado: {str(e)}")
            return f'CERT-{año_actual}-0001'
        finally:
            cur.close()
            con.close()
    
    def updateCertificadoMedico(self, id_certificado, id_tipo_certificado=None,
                               certificado_dias_reposo=None, certificado_desde_fecha=None,
                               certificado_hasta_fecha=None, certificado_motivo=None,
                               certificado_diagnostico=None, certificado_recomendaciones=None,
                               certificado_estado=None, usuario_modificacion='ADMIN'):
        """Actualiza un certificado médico existente"""
        
        updateSQL = """
            UPDATE certificados_medicos
            SET 
                id_tipo_certificado = COALESCE(%s, id_tipo_certificado),
                certificado_dias_reposo = COALESCE(%s, certificado_dias_reposo),
                certificado_desde_fecha = COALESCE(%s, certificado_desde_fecha),
                certificado_hasta_fecha = COALESCE(%s, certificado_hasta_fecha),
                certificado_motivo = COALESCE(%s, certificado_motivo),
                certificado_diagnostico = COALESCE(%s, certificado_diagnostico),
                certificado_recomendaciones = COALESCE(%s, certificado_recomendaciones),
                certificado_estado = COALESCE(%s, certificado_estado),
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_certificado = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (
                id_tipo_certificado,
                certificado_dias_reposo,
                certificado_desde_fecha,
                certificado_hasta_fecha,
                certificado_motivo,
                certificado_diagnostico,
                certificado_recomendaciones,
                certificado_estado,
                usuario_modificacion,
                id_certificado
            ))
            
            con.commit()
            app.logger.info(f"Certificado médico {id_certificado} actualizado exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar certificado médico: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def deleteCertificadoMedico(self, id_certificado):
        """Elimina lógicamente un certificado médico"""
        deleteSQL = """
            UPDATE certificados_medicos
            SET est_certificado = 'I',
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_certificado = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_certificado,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar certificado médico: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

