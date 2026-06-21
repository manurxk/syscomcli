from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class PresupuestoDao:
    """DAO para gestionar presupuestos/cotizaciones médicas"""
    
    def getPresupuestos(self):
        """Obtiene todos los presupuestos con sus datos completos"""
        presupuestoSQL = """
            SELECT
                p.id_presupuesto,
                p.id_consulta,
                p.id_paciente,
                p.id_profesional,
                p.presupuesto_numero,
                p.presupuesto_fecha,
                p.presupuesto_validez_dias,
                p.presupuesto_estado,
                p.presupuesto_subtotal,
                p.presupuesto_descuento,
                p.presupuesto_total,
                p.presupuesto_observaciones,
                p.frecuencia_sugerida,
                p.id_plan_tratamiento,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                p.fecha_creacion,
                p.fecha_vencimiento
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON p.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.est_presupuesto = 'A'
            ORDER BY p.presupuesto_fecha DESC, p.id_presupuesto DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(presupuestoSQL)
            presupuestos = cur.fetchall()
            
            return [{
                'id_presupuesto': pr[0],
                'id_consulta': pr[1],
                'id_paciente': pr[2],
                'id_profesional': pr[3],
                'presupuesto_numero': pr[4],
                'presupuesto_fecha': pr[5].strftime('%d/%m/%Y') if pr[5] else None,
                'presupuesto_validez_dias': pr[6],
                'presupuesto_estado': pr[7],
                'presupuesto_subtotal': pr[8],
                'presupuesto_descuento': pr[9],
                'presupuesto_total': pr[10],
                'presupuesto_observaciones': pr[11],
                'frecuencia_sugerida': pr[12],
                'id_plan_tratamiento': pr[13],
                'historia_clinica': pr[14],
                'paciente_nombre': pr[15],
                'paciente_cedula': pr[16],
                'profesional_nombre': pr[17],
                'profesional_matricula': pr[18],
                'fecha_registro': pr[19].strftime('%d/%m/%Y') if pr[19] else None,
                'fecha_vencimiento': pr[20].strftime('%d/%m/%Y') if pr[20] else None
            } for pr in presupuestos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener todos los presupuestos: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getPresupuestoById(self, id_presupuesto):
        """Obtiene un presupuesto específico por ID con su detalle"""
        presupuestoSQL = """
            SELECT
                p.id_presupuesto,
                p.id_consulta,
                p.id_paciente,
                p.id_profesional,
                p.presupuesto_numero,
                p.presupuesto_fecha,
                p.presupuesto_validez_dias,
                p.presupuesto_estado,
                p.presupuesto_subtotal,
                p.presupuesto_descuento,
                p.presupuesto_total,
                p.presupuesto_observaciones,
                p.est_presupuesto,
                p.frecuencia_sugerida,
                p.id_plan_tratamiento,
                p.fecha_vencimiento,
                p.motivo_rechazo,
                -- Datos del paciente
                pac.pac_historia_clinica,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                pp.per_cedula AS paciente_cedula,
                pp.per_telefono AS paciente_telefono,
                -- Datos del profesional
                CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS profesional_nombre,
                e.esp_matricula,
                p.fecha_creacion,
                p.usuario_creacion
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            JOIN especialistas e ON p.id_profesional = e.id_especialista
            JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
            JOIN personas pe ON f.id_persona = pe.id_persona
            WHERE p.id_presupuesto = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(presupuestoSQL, (id_presupuesto,))
            pr = cur.fetchone()
            
            if not pr:
                return None
            
            # Índices de columnas (orden del SELECT después de las adiciones)
            # 0:id, 1:id_consulta, 2:id_paciente, 3:id_profesional, 4:numero,
            # 5:fecha, 6:validez_dias, 7:estado, 8:subtotal, 9:descuento, 10:total,
            # 11:observaciones, 12:est_presupuesto, 13:frecuencia, 14:id_plan,
            # 15:fecha_vencimiento, 16:motivo_rechazo, 17:historia_clinica,
            # 18:paciente_nombre, 19:cedula, 20:telefono, 21:profesional_nombre,
            # 22:matricula, 23:fecha_creacion, 24:usuario_creacion
            return {
                'id_presupuesto': pr[0],
                'id_consulta': pr[1],
                'id_paciente': pr[2],
                'id_profesional': pr[3],
                'presupuesto_numero': pr[4],
                'presupuesto_fecha': pr[5].strftime('%Y-%m-%d') if pr[5] else None,
                'presupuesto_validez_dias': pr[6],
                'presupuesto_estado': pr[7],
                'presupuesto_subtotal': pr[8],
                'presupuesto_descuento': pr[9],
                'presupuesto_total': pr[10],
                'presupuesto_observaciones': pr[11],
                'activo': pr[12] == 'A',
                'frecuencia_sugerida': pr[13],
                'id_plan_tratamiento': pr[14],
                'fecha_vencimiento': pr[15].strftime('%Y-%m-%d') if pr[15] else None,
                'motivo_rechazo': pr[16],
                'historia_clinica': pr[17],
                'paciente_nombre': pr[18],
                'paciente_cedula': pr[19],
                'paciente_telefono': pr[20],
                'profesional_nombre': pr[21],
                'profesional_matricula': pr[22],
                'fecha_registro': pr[23].strftime('%Y-%m-%d') if pr[23] else None,
                'usuario_creacion': pr[24]
            }
            
        except Exception as e:
            app.logger.error(f"Error al obtener presupuesto por ID: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def getPresupuestoDetalle(self, id_presupuesto):
        """Obtiene el detalle completo de un presupuesto"""
        detalleSQL = """
            SELECT
                pd.id_presupuesto_detalle,
                pd.id_presupuesto,
                pd.id_tipo_procedimiento,
                pd.des_item,
                pd.cantidad,
                pd.precio_unitario,
                pd.subtotal,
                pd.observaciones,
                tp.des_tipo_procedimiento
            FROM presupuesto_detalle pd
            LEFT JOIN tipos_procedimientos tp ON pd.id_tipo_procedimiento = tp.id_tipo_procedimiento
            WHERE pd.id_presupuesto = %s
            ORDER BY pd.id_presupuesto_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(detalleSQL, (id_presupuesto,))
            detalles = cur.fetchall()
            
            return [{
                'id_presupuesto_detalle': d[0],
                'id_presupuesto': d[1],
                'id_tipo_procedimiento': d[2],
                'des_item': d[3],
                'cantidad': d[4],
                'precio_unitario': d[5],
                'subtotal': d[6],
                'observaciones': d[7],
                'tipo_procedimiento': d[8]
            } for d in detalles]
            
        except Exception as e:
            app.logger.error(f"Error al obtener detalle del presupuesto: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def guardarPresupuesto(self, id_paciente, id_profesional, presupuesto_fecha,
                          presupuesto_validez_dias=30, presupuesto_estado='PENDIENTE',
                          id_consulta=None, presupuesto_observaciones=None,
                          frecuencia_sugerida=None, id_plan_tratamiento=None,
                          usuario_creacion='ADMIN'):
        """Guarda un nuevo presupuesto.
        
        La fecha_vencimiento se calcula automáticamente como:
            presupuesto_fecha + presupuesto_validez_dias días.
        """
        
        if not all([id_paciente, id_profesional, presupuesto_fecha]):
            app.logger.error("Faltan campos obligatorios para guardar presupuesto")
            return None
        
        # Generar número de presupuesto
        presupuesto_numero = self._generarNumeroPresupuesto()
        
        insertPresupuestoSQL = """
            INSERT INTO presupuestos(
                id_consulta, id_paciente, id_profesional, presupuesto_numero,
                presupuesto_fecha, presupuesto_validez_dias, presupuesto_estado,
                presupuesto_observaciones, est_presupuesto, frecuencia_sugerida,
                id_plan_tratamiento, usuario_creacion,
                fecha_vencimiento
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, 'A', %s, %s, %s,
                   %s::DATE + (%s || ' days')::INTERVAL)
            RETURNING id_presupuesto
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            app.logger.info(f"Insertando presupuesto para paciente ID: {id_paciente}")
            
            cur.execute(insertPresupuestoSQL, (
                id_consulta,
                id_paciente,
                id_profesional,
                presupuesto_numero,
                presupuesto_fecha,
                presupuesto_validez_dias,
                presupuesto_estado,
                presupuesto_observaciones,
                frecuencia_sugerida,
                id_plan_tratamiento,
                usuario_creacion,
                presupuesto_fecha,      # Para calcular fecha_vencimiento
                presupuesto_validez_dias
            ))
            
            presupuesto_id = cur.fetchone()[0]
            con.commit()
            
            app.logger.info(f"Presupuesto guardado exitosamente con ID: {presupuesto_id}")
            return presupuesto_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar presupuesto: {str(e)}", exc_info=True)
            return None
        finally:
            cur.close()
            con.close()
    
    def guardarPresupuestoDetalle(self, id_presupuesto, des_item, precio_unitario,
                                  cantidad=1, id_tipo_procedimiento=None,
                                  observaciones=None):
        """Guarda un item en el detalle del presupuesto"""
        
        subtotal = precio_unitario * cantidad
        
        insertDetalleSQL = """
            INSERT INTO presupuesto_detalle(
                id_presupuesto, id_tipo_procedimiento, des_item,
                cantidad, precio_unitario, subtotal, observaciones
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            RETURNING id_presupuesto_detalle
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(insertDetalleSQL, (
                id_presupuesto,
                id_tipo_procedimiento,
                des_item,
                cantidad,
                precio_unitario,
                subtotal,
                observaciones
            ))
            
            detalle_id = cur.fetchone()[0]
            con.commit()
            
            # Actualizar totales del presupuesto
            self._actualizarTotalesPresupuesto(id_presupuesto)
            
            return detalle_id
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al guardar detalle de presupuesto: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()
    
    def _actualizarTotalesPresupuesto(self, id_presupuesto):
        """Actualiza los totales del presupuesto basado en su detalle"""
        updateTotalesSQL = """
            UPDATE presupuestos
            SET 
                presupuesto_subtotal = (
                    SELECT COALESCE(SUM(subtotal), 0)
                    FROM presupuesto_detalle
                    WHERE id_presupuesto = %s
                ),
                presupuesto_total = (
                    SELECT COALESCE(SUM(subtotal), 0)
                    FROM presupuesto_detalle
                    WHERE id_presupuesto = %s
                ) - presupuesto_descuento,
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_presupuesto = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateTotalesSQL, (id_presupuesto, id_presupuesto, id_presupuesto))
            con.commit()
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar totales del presupuesto: {str(e)}")
        finally:
            cur.close()
            con.close()
    
    def _generarNumeroPresupuesto(self):
        """Genera un número único de presupuesto"""
        año_actual = date.today().year
        
        selectSQL = """
            SELECT MAX(CAST(SUBSTRING(presupuesto_numero FROM '[0-9]+$') AS INTEGER))
            FROM presupuestos
            WHERE presupuesto_numero LIKE %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            patron = f'PRES-{año_actual}-%'
            cur.execute(selectSQL, (patron,))
            resultado = cur.fetchone()
            
            siguiente_numero = (resultado[0] or 0) + 1
            return f'PRES-{año_actual}-{str(siguiente_numero).zfill(4)}'
            
        except Exception as e:
            app.logger.error(f"Error al generar número de presupuesto: {str(e)}")
            return f'PRES-{año_actual}-0001'
        finally:
            cur.close()
            con.close()
    
    def updatePresupuesto(self, id_presupuesto, presupuesto_estado=None,
                         presupuesto_descuento=None, presupuesto_observaciones=None,
                         frecuencia_sugerida=None, id_plan_tratamiento=None,
                         usuario_modificacion='ADMIN'):
        """Actualiza un presupuesto existente.
        
        Estados válidos: PENDIENTE, APROBADO, RECHAZADO, VENCIDO,
                         FACTURADO_PARCIAL, FACTURADO.
        """
        
        updateSQL = """
            UPDATE presupuestos
            SET 
                presupuesto_estado = COALESCE(%s, presupuesto_estado),
                presupuesto_descuento = COALESCE(%s, presupuesto_descuento),
                presupuesto_observaciones = COALESCE(%s, presupuesto_observaciones),
                frecuencia_sugerida = COALESCE(%s, frecuencia_sugerida),
                id_plan_tratamiento = COALESCE(%s, id_plan_tratamiento),
                presupuesto_total = presupuesto_subtotal - COALESCE(%s, presupuesto_descuento),
                fecha_modificacion = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_presupuesto = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(updateSQL, (
                presupuesto_estado,
                presupuesto_descuento,
                presupuesto_observaciones,
                frecuencia_sugerida,
                id_plan_tratamiento,
                presupuesto_descuento,
                usuario_modificacion,
                id_presupuesto
            ))
            
            con.commit()
            app.logger.info(f"Presupuesto {id_presupuesto} actualizado exitosamente")
            return True
            
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al actualizar presupuesto: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def rechazarPresupuesto(self, id_presupuesto, motivo_rechazo=None, usuario_modificacion='ADMIN'):
        """Rechaza un presupuesto registrando el motivo.

        Solo se puede rechazar un presupuesto en estado PENDIENTE.
        Este es un estado terminal: no puede volver a PENDIENTE.
        """
        rechazarSQL = """
            UPDATE presupuestos
            SET presupuesto_estado   = 'RECHAZADO',
                motivo_rechazo       = %s,
                fecha_modificacion   = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE id_presupuesto  = %s
              AND presupuesto_estado = 'PENDIENTE'
              AND est_presupuesto  = 'A'
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(rechazarSQL, (motivo_rechazo, usuario_modificacion, id_presupuesto))
            filas = cur.rowcount
            con.commit()

            if filas == 0:
                app.logger.warning(
                    f"No se pudo rechazar el presupuesto {id_presupuesto}. "
                    "Puede que no esté en estado PENDIENTE o no exista."
                )
                return False

            app.logger.info(f"Presupuesto {id_presupuesto} rechazado. Motivo: {motivo_rechazo}")
            return True

        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al rechazar presupuesto: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()

    def vencerPresupuestosExpirados(self, usuario_modificacion='SISTEMA'):
        """Cambia a estado VENCIDO todos los presupuestos PENDIENTES cuya
        fecha_vencimiento ya haya pasado.

        Diseñado para ser llamado por un scheduler nocturno (APScheduler).
        Retorna la cantidad de registros actualizados.
        """
        vencerSQL = """
            UPDATE presupuestos
            SET presupuesto_estado   = 'VENCIDO',
                fecha_modificacion   = CURRENT_TIMESTAMP,
                usuario_modificacion = %s
            WHERE presupuesto_estado = 'PENDIENTE'
              AND est_presupuesto    = 'A'
              AND fecha_vencimiento  < CURRENT_DATE
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(vencerSQL, (usuario_modificacion,))
            cantidad = cur.rowcount
            con.commit()
            app.logger.info(f"Tarea de vencimiento: {cantidad} presupuesto(s) marcado(s) como VENCIDO.")
            return cantidad

        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al vencer presupuestos expirados: {str(e)}")
            return 0
        finally:
            cur.close()
            con.close()

    def getPresupuestosProximosAVencer(self, dias_alerta=7):
        """Obtiene presupuestos PENDIENTES cuya fecha_vencimiento
        cae dentro de los próximos `dias_alerta` días.

        Útil para mostrar alertas en el dashboard administrativo.
        """
        alertaSQL = """
            SELECT
                p.id_presupuesto,
                p.presupuesto_numero,
                p.fecha_vencimiento,
                p.presupuesto_total,
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
                (p.fecha_vencimiento - CURRENT_DATE) AS dias_restantes
            FROM presupuestos p
            JOIN pacientes pac ON p.id_paciente = pac.id_paciente
            JOIN personas pp ON pac.id_persona = pp.id_persona
            WHERE p.presupuesto_estado = 'PENDIENTE'
              AND p.est_presupuesto = 'A'
              AND p.fecha_vencimiento BETWEEN CURRENT_DATE
                                          AND (CURRENT_DATE + (%s || ' days')::INTERVAL)
            ORDER BY p.fecha_vencimiento ASC
        """

        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()

        try:
            cur.execute(alertaSQL, (dias_alerta,))
            rows = cur.fetchall()
            return [{
                'id_presupuesto':    r[0],
                'presupuesto_numero': r[1],
                'fecha_vencimiento': r[2].strftime('%d/%m/%Y') if r[2] else None,
                'presupuesto_total': r[3],
                'paciente_nombre':   r[4],
                'dias_restantes':    r[5]
            } for r in rows]

        except Exception as e:
            app.logger.error(f"Error al obtener presupuestos próximos a vencer: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def deletePresupuesto(self, id_presupuesto):
        """Elimina lógicamente un presupuesto"""
        deleteSQL = """
            UPDATE presupuestos
            SET est_presupuesto = 'I',
                fecha_modificacion = CURRENT_TIMESTAMP
            WHERE id_presupuesto = %s
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_presupuesto,))
            con.commit()
            return cur.rowcount > 0
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar presupuesto: {str(e)}")
            return False
        finally:
            cur.close()
            con.close()
    
    def getPresupuestosPorPaciente(self, id_paciente):
        """Obtiene todos los presupuestos de un paciente"""
        presupuestoSQL = """
            SELECT
                p.id_presupuesto,
                p.presupuesto_numero,
                p.presupuesto_fecha,
                p.presupuesto_total,
                p.presupuesto_estado
            FROM presupuestos p
            WHERE p.id_paciente = %s AND p.est_presupuesto = 'A'
            ORDER BY p.presupuesto_fecha DESC
        """
        
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(presupuestoSQL, (id_paciente,))
            presupuestos = cur.fetchall()
            
            return [{
                'id_presupuesto': pr[0],
                'presupuesto_numero': pr[1],
                'presupuesto_fecha': pr[2].strftime('%d/%m/%Y') if pr[2] else None,
                'presupuesto_total': pr[3],
                'presupuesto_estado': pr[4]
            } for pr in presupuestos]
            
        except Exception as e:
            app.logger.error(f"Error al obtener presupuestos del paciente: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()


















