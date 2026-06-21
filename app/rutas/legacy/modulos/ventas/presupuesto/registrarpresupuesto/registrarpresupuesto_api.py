from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.ventas.presupuesto.PresupuestoDao import PresupuestoDao
from app.conexion.Conexion import Conexion

presupuestoapi = Blueprint('presupuestoapi', __name__)


# ============================================
# CRUD BÁSICO DE PRESUPUESTOS
# ============================================

@presupuestoapi.route('/presupuestos', methods=['GET'])
def getAllPresupuestos():
    """Obtiene la lista completa de presupuestos activos"""
    dao = PresupuestoDao()
    
    try:
        presupuestos = dao.getPresupuestos()
        return jsonify({'success': True, 'data': presupuestos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todos los presupuestos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/frecuencias', methods=['GET'])
def getFrecuencias():
    """Obtiene la lista de frecuencias de agendamiento permitidas"""
    try:
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        cur.execute("SELECT des_frecuencia, dias_intervalo FROM frecuencias_agendamiento WHERE est_frecuencia = TRUE ORDER BY dias_intervalo")
        filas = cur.fetchall()
        frecuencias = [{'descripcion': f[0], 'dias': f[1]} for f in filas]
        cur.close()
        con.close()
        return jsonify({'success': True, 'data': frecuencias, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener frecuencias: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['GET'])
def getPresupuesto(id_presupuesto):
    """Obtiene un presupuesto específico por su ID con su detalle"""
    dao = PresupuestoDao()
    
    try:
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        
        if presupuesto:
            # Obtener detalle
            detalle = dao.getPresupuestoDetalle(id_presupuesto)
            presupuesto['detalle'] = detalle
            
            return jsonify({'success': True, 'data': presupuesto, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener el presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos', methods=['POST'])
def addPresupuesto():
    """Crea un nuevo presupuesto"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    # Validar campos obligatorios
    campos_requeridos = ['id_paciente', 'id_profesional', 'presupuesto_fecha']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400
    
    try:
        presupuesto_id = dao.guardarPresupuesto(
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            presupuesto_fecha=data['presupuesto_fecha'],
            presupuesto_validez_dias=data.get('presupuesto_validez_dias', 30),
            presupuesto_estado=data.get('presupuesto_estado', 'PENDIENTE'),
            id_consulta=data.get('id_consulta'),
            presupuesto_observaciones=data.get('presupuesto_observaciones'),
            frecuencia_sugerida=data.get('frecuencia_sugerida'),
            id_plan_tratamiento=data.get('id_plan_tratamiento'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if presupuesto_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_presupuesto': presupuesto_id,
                    'mensaje': 'Presupuesto creado exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar el presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/detalle', methods=['POST'])
def addPresupuestoDetalle(id_presupuesto):
    """Agrega un item al detalle de un presupuesto"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    campos_requeridos = ['des_item', 'precio_unitario']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarPresupuestoDetalle(
            id_presupuesto=id_presupuesto,
            des_item=data['des_item'],
            precio_unitario=int(data['precio_unitario']),  # Convertir a entero (guaraníes)
            cantidad=data.get('cantidad', 1),
            id_tipo_procedimiento=data.get('id_tipo_procedimiento'),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_presupuesto_detalle': detalle_id, 'mensaje': 'Item agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el item al presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/detalle/<int:id_detalle>', methods=['DELETE'])
def deletePresupuestoDetalle(id_presupuesto, id_detalle):
    """Elimina un item del detalle de un presupuesto"""
    dao = PresupuestoDao()
    
    try:
        # Verificar que el detalle existe y pertenece al presupuesto
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        if not presupuesto:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
        
        detalle = dao.getPresupuestoDetalle(id_presupuesto)
        item_existe = any(d['id_presupuesto_detalle'] == id_detalle for d in detalle)
        
        if not item_existe:
            return jsonify({'success': False, 'error': 'No se encontró el item.'}), 404
        
        # Eliminar el item (DELETE físico ya que es detalle)
        deleteSQL = "DELETE FROM presupuesto_detalle WHERE id_presupuesto_detalle = %s"
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        try:
            cur.execute(deleteSQL, (id_detalle,))
            con.commit()
            
            # Actualizar totales del presupuesto
            dao._actualizarTotalesPresupuesto(id_presupuesto)
            
            return jsonify({
                'success': True,
                'mensaje': 'Item eliminado correctamente.',
                'error': None
            }), 200
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error al eliminar item: {str(e)}")
            return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
        finally:
            cur.close()
            con.close()
            
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['PUT'])
def updatePresupuesto(id_presupuesto):
    """Actualiza un presupuesto existente"""
    data = request.get_json()
    dao = PresupuestoDao()
    
    # Validar que existe el presupuesto
    presupuesto_existente = dao.getPresupuestoById(id_presupuesto)
    if not presupuesto_existente:
        return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
    
    try:
        resultado = dao.updatePresupuesto(
            id_presupuesto=id_presupuesto,
            presupuesto_estado=data.get('presupuesto_estado'),
            presupuesto_descuento=int(data.get('presupuesto_descuento', 0)) if data.get('presupuesto_descuento') else None,
            presupuesto_observaciones=data.get('presupuesto_observaciones'),
            frecuencia_sugerida=data.get('frecuencia_sugerida'),
            id_plan_tratamiento=data.get('id_plan_tratamiento'),
            usuario_modificacion=data.get('usuario_modificacion', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_presupuesto': id_presupuesto, 'mensaje': 'Presupuesto actualizado exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el presupuesto.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>', methods=['DELETE'])
def deletePresupuesto(id_presupuesto):
    """Elimina lógicamente un presupuesto"""
    dao = PresupuestoDao()
    
    try:
        if dao.deletePresupuesto(id_presupuesto):
            return jsonify({
                'success': True,
                'mensaje': f'Presupuesto con ID {id_presupuesto} eliminado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el presupuesto o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar presupuesto: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS DE FILTRADO
# ============================================

@presupuestoapi.route('/presupuestos/paciente/<int:id_paciente>', methods=['GET'])
def getPresupuestosPorPaciente(id_paciente):
    """Obtiene todos los presupuestos de un paciente"""
    dao = PresupuestoDao()
    
    try:
        presupuestos = dao.getPresupuestosPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': presupuestos, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener presupuestos del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500

# ============================================
# PLAN DE TRATAMIENTO AUTOMATIZADO
# ============================================

@presupuestoapi.route('/presupuestos/simular-plan', methods=['POST'])
@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/simular-plan', methods=['POST'])
def simularPlanTratamiento(id_presupuesto=None):
    """Simula las fechas para un plan de tratamiento automatizado"""
    data = request.get_json()
    
    campos_requeridos = [
        'id_especialista', 'id_paciente', 'fecha_inicio', 
        'hora_inicio', 'hora_fin', 'cantidad_sesiones', 'frecuencia'
    ]
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio para simular el plan.'
            }), 400
            
    try:
        from app.services.recurrence_service import RecurrenceService
        recurrence_service = RecurrenceService()
        
        resultado = recurrence_service.simular_plan(
            id_especialista=data['id_especialista'],
            id_paciente=data['id_paciente'],
            fecha_inicio=data['fecha_inicio'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            cantidad_sesiones=int(data['cantidad_sesiones']),
            frecuencia=data['frecuencia'],
            dias_intervalo=int(data.get('dias_intervalo', 1))
        )
        
        if resultado['success']:
            return jsonify(resultado), 200
        else:
            return jsonify(resultado), 400
            
    except Exception as e:
        app.logger.error(f"Error al simular plan de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno al simular el plan.'}), 500

@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/confirmar-plan', methods=['POST'])
def confirmarPlanTratamiento(id_presupuesto):
    """Guarda en BD un plan de tratamiento automatizado (lote de citas)"""
    data = request.get_json()
    from flask import session
    from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
    
    id_usuario = session.get('id_usuario', 1) # Default 1 para casos sin sesión activa
    
    if 'sesiones' not in data or not data['sesiones']:
        return jsonify({'success': False, 'error': 'No se enviaron sesiones para agendar.'}), 400
        
    if 'id_especialista' not in data or 'id_paciente' not in data or 'id_especialidad' not in data:
        return jsonify({'success': False, 'error': 'Faltan datos básicos (especialista, paciente, especialidad).'}), 400
        
    cita_dao = CitaDao()
    dao = PresupuestoDao()
    nuevas_citas = []
    errores = []
    
    # 1. Obtener datos del presupuesto para observaciones/motivo
    presupuesto = dao.getPresupuestoById(id_presupuesto)
    motivo = f"Plan de Tratamiento - Presupuesto #{id_presupuesto}" if not presupuesto else f"Plan de Tratamiento: {presupuesto.get('presupuesto_observaciones', f'Presupuesto #{id_presupuesto}')}"
    
    # 2. Iterar y guardar
    try:
        from app.conexion.Conexion import Conexion
        # Para forzar un commit general manual o usamos la gestión de CitaDao individual
        # Usaremos CitaDao individual, pero si alguna falla podemos continuar o hacer rollback.
        # Mejor agendar todas las posibles y reportar si alguna falló.
        for sesion in data['sesiones']:
            # Verificar si era válida en la simulación
            if sesion.get('conflicto', False):
                errores.append(f"Sesión {sesion.get('numero_sesion')}: ignorada por conflicto.")
                continue
                
            cita_id = cita_dao.guardarCita(
                id_paciente=data['id_paciente'],
                id_agenda_horario=sesion.get('id_agenda_horario'),
                id_especialista=data['id_especialista'],
                id_especialidad=data['id_especialidad'],
                cita_fecha=sesion['fecha'],
                cita_hora_inicio=sesion['hora_inicio'],
                cita_hora_fin=sesion['hora_fin'],
                cita_tipo='SEGUIMIENTO' if sesion.get('numero_sesion', 1) > 1 else 'PRIMERA_VEZ',
                cita_motivo=motivo,
                cita_creacion_usuario=id_usuario,
                id_estado_cita=1, # 1=AGENDADA
                cita_observaciones=f"Generado automáticamente. Sesión {sesion.get('numero_sesion')} de plan.",
                cita_numero_sesion=sesion.get('numero_sesion')
            )
            
            if cita_id:
                nuevas_citas.append(cita_id)
            else:
                errores.append(f"Sesión {sesion.get('numero_sesion')}: error al guardar en base de datos.")
                
        # 3. Marcar presupuesto como agendado (Podríamos actualizar su estado a APROBADO_AGENDADO)
        # Opcional, pero para mantener historia:
        dao.updatePresupuesto(
            id_presupuesto=id_presupuesto,
            presupuesto_estado='APROBADO', # Si estaba pendiente y lo agendan, asumimos aprobado
            usuario_modificacion=id_usuario
        )
        
        return jsonify({
            'success': True,
            'mensaje': f'Se agendaron {len(nuevas_citas)} sesiones correctamente. Errores: {len(errores)}',
            'citas_generadas': nuevas_citas,
            'errores': errores
        }), 201
        
    except Exception as e:
        app.logger.error(f"Error al confirmar plan de tratamiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno al guardar las citas.'}), 500

@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/contrato-pdf', methods=['GET'])
def generarContratoPDF(id_presupuesto):
    """Genera y descarga el PDF del contrato de tratamiento para el presupuesto"""
    dao = PresupuestoDao()
    from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
    cita_dao = CitaDao()
    
    try:
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        if not presupuesto:
            return jsonify({'success': False, 'error': 'No se encontró el presupuesto.'}), 404
            
        # Intentar obtener las citas que haya generado para este presupuesto
        # Se asume que en "cita_motivo" o "cita_observaciones" está "Presupuesto #ID"
        from app.conexion.Conexion import Conexion
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        
        cur.execute("""
            SELECT 
                cita_fecha, 
                cita_hora_inicio, 
                cita_hora_fin, 
                cita_numero_sesion 
            FROM citas 
            WHERE id_paciente = %s 
              AND id_especialista = %s
              AND cita_motivo LIKE %s
              AND cita_activo = TRUE
            ORDER BY cita_fecha, cita_hora_inicio
        """, (
            presupuesto['id_paciente'], 
            presupuesto['id_profesional'], 
            f"%Presupuesto #{id_presupuesto}%"
        ))
        
        citas_db = cur.fetchall()
        citas = []
        for c in citas_db:
            citas.append({
                'fecha': c[0].strftime('%d/%m/%Y'),
                'hora_inicio': c[1].strftime('%H:%M') if c[1] else '',
                'hora_fin': c[2].strftime('%H:%M') if c[2] else '',
                'numero_sesion': c[3]
            })
            
        cur.close()
        con.close()
        
        # Preparar datos para el template
        from datetime import datetime
        # Obtener detalle del presupuesto para el contrato
        detalles = dao.getPresupuestoDetalle(id_presupuesto)
        
        datos_contrato = {
            'empresa_nombre': app.config.get('NOMBRE_CLINICA', 'Clínica Sysclin'),
            'empresa_ruc': app.config.get('RUC_CLINICA', '80000000-1'),
            'empresa_telefono': app.config.get('TELEFONO_CLINICA', '0999 999 999'),
            'empresa_direccion': app.config.get('DIRECCION_CLINICA', 'Asunción, Paraguay'),
            
            'fecha_actual': datetime.now().strftime('%d/%m/%Y'),
            
            'presupuesto': presupuesto,
            'paciente_nombre': presupuesto.get('paciente_nombre', 'Paciente'),
            'paciente_cedula': presupuesto.get('paciente_cedula', ''),
            'especialista_nombre': presupuesto.get('profesional_nombre', 'Profesional'),
            
            'cantidad_sesiones': len(citas) if citas else presupuesto.get('presupuesto_observaciones', '').split(' ')[0] if presupuesto.get('presupuesto_observaciones') else 'A definir',
            'frecuencia_sugerida': presupuesto.get('frecuencia_sugerida', 'Semanal'),
            
            'citas': citas,
            'detalles': detalles,
            'total_presupuesto': presupuesto.get('presupuesto_total', 0),
            
            # Variables de políticas
            'multa_ausencia_porcentaje': '100%',
            'horas_aviso_cancelacion': '24'
        }
            
        from app.services.contrato_pdf_service import ContratoPDFService
        pdf_service = ContratoPDFService()
        pdf_buffer = pdf_service.generar_contrato_pdf(datos_contrato)
        
        if not pdf_buffer:
            return jsonify({'success': False, 'error': 'No se pudo generar el documento PDF.'}), 500
            
        from flask import send_file
        return send_file(
            pdf_buffer,
            download_name=f"Contrato_Presupuesto_{id_presupuesto}.pdf",
            as_attachment=True,
            mimetype='application/pdf'
        )
        
    except Exception as e:
        app.logger.error(f"Error al generar contrato PDF: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno al generar el PDF.'}), 500


@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/registrar-citas', methods=['POST'])
def registrarCitasMasivasPresupuesto(id_presupuesto):
    """Simula y registra las citas masivas para un presupuesto"""
    data = request.get_json()
    from flask import session
    id_usuario = session.get('id_usuario', 1)
    
    campos_requeridos = [
        'id_especialista', 'id_paciente', 'fecha_inicio', 
        'hora_inicio', 'hora_fin', 'cantidad_sesiones', 'frecuencia'
    ]
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio.'}), 400
            
    try:
        from app.services.recurrence_service import RecurrenceService
        recurrence_service = RecurrenceService()
        
        # 1. Simular para obtener el plan de fechas y horarios
        simulacion = recurrence_service.simular_plan(
            id_especialista=data['id_especialista'],
            id_paciente=data['id_paciente'],
            fecha_inicio=data['fecha_inicio'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            cantidad_sesiones=int(data['cantidad_sesiones']),
            frecuencia=data['frecuencia'],
            dias_intervalo=int(data.get('dias_intervalo', 1))
        )
        
        if not simulacion['success']:
            return jsonify({'success': False, 'error': simulacion['error']}), 400
            
        # 2. Registrar el plan obtenido
        resultado = recurrence_service.registrar_plan(
            id_especialista=data['id_especialista'],
            id_paciente=data['id_paciente'],
            id_presupuesto=id_presupuesto,
            plan_sesiones=simulacion['sesiones'],
            id_especialidad=data.get('id_especialidad'),
            id_usuario=id_usuario
        )
        
        if resultado['success']:
            # FASE 3: El cambio de estado a APROBADO ahora es manejado de manera 
            # atómica y transaccional dentro de recurrence_service.confirmar_citas
            
            return jsonify({
                'success': True, 
                'mensaje': resultado['mensaje'],
                'citas_ids': resultado['citas_ids'],
                'errores': resultado['errores']
            }), 201
        else:
            return jsonify({
                'success': False, 
                'error': 'No se pudieron registrar las citas.', 
                'detalles': resultado['errores']
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al registrar citas masivas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno al registrar las citas.'}), 500


# ============================================
# FASE 1: NUEVOS ENDPOINTS DE GESTIÓN DE CICLO DE VIDA
# ============================================

@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/rechazar', methods=['POST'])
def rechazarPresupuesto(id_presupuesto):
    """Rechaza un presupuesto en estado PENDIENTE.

    Body JSON (opcional):
        {
            "motivo_rechazo": "Precio demasiado alto"
        }

    Solo funciona si el presupuesto está en estado PENDIENTE.
    RECHAZADO es un estado terminal: no revierte a PENDIENTE.
    """
    dao = PresupuestoDao()
    data = request.get_json(silent=True) or {}

    motivo = data.get('motivo_rechazo', None)
    usuario = app.config.get('USUARIO_ACTUAL', 'ADMIN')

    try:
        resultado = dao.rechazarPresupuesto(
            id_presupuesto=id_presupuesto,
            motivo_rechazo=motivo,
            usuario_modificacion=usuario
        )

        if resultado:
            return jsonify({
                'success': True,
                'mensaje': f'Presupuesto {id_presupuesto} rechazado correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo rechazar el presupuesto. '
                         'Verificá que exista y esté en estado PENDIENTE.'
            }), 400

    except Exception as e:
        app.logger.error(f"Error al rechazar presupuesto {id_presupuesto}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@presupuestoapi.route('/presupuestos/alertas/proximos-a-vencer', methods=['GET'])
def getPresupuestosProximosAVencer():
    """Retorna presupuestos PENDIENTES que vencen en los próximos N días.

    Query param:
        dias_alerta (int, default=7): Horizonte de días para la alerta.

    Usado por el dashboard administrativo para mostrar el widget de alertas.
    """
    dao = PresupuestoDao()
    dias_alerta = request.args.get('dias_alerta', 7, type=int)

    try:
        alertas = dao.getPresupuestosProximosAVencer(dias_alerta=dias_alerta)
        return jsonify({
            'success': True,
            'data': alertas,
            'total': len(alertas),
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error al obtener alertas de vencimiento: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# FASE 3 — TAREA 4: Duplicar y Actualizar presupuesto
# ============================================

@presupuestoapi.route('/presupuestos/<int:id_presupuesto>/duplicar', methods=['GET'])
def duplicarPresupuesto(id_presupuesto):
    """Retorna los datos de un presupuesto para pre-cargar el formulario de nuevo presupuesto.

    NO crea ningún registro en la BD. Solo devuelve los datos del presupuesto
    original (ítems, paciente, profesional, moneda) para que el frontend
    los inyecte en el formulario antes de que el usuario guarde.

    Solo está disponible para presupuestos en estado VENCIDO o RECHAZADO.

    Returns:
        {
            "success": True,
            "data": {
                "id_paciente": int,
                "id_profesional": int,
                "id_moneda": int,
                "fecha_vencimiento_sugerida": "YYYY-MM-DD",   # hoy + 30 días
                "detalle": [...],                              # ítems a copiar
                "presupuesto_observaciones": str | None
            }
        }
    """
    dao = PresupuestoDao()

    try:
        presupuesto = dao.getPresupuestoById(id_presupuesto)
        if not presupuesto:
            return jsonify({'success': False, 'error': 'Presupuesto no encontrado.'}), 404

        # Solo se puede duplicar desde estados terminales (VENCIDO o RECHAZADO)
        estados_duplicables = ('VENCIDO', 'RECHAZADO')
        if presupuesto.get('presupuesto_estado') not in estados_duplicables:
            return jsonify({
                'success': False,
                'error': f'Solo se pueden duplicar presupuestos en estado '
                         f'{" o ".join(estados_duplicables)}. '
                         f'Estado actual: {presupuesto.get("presupuesto_estado")}'
            }), 400

        # Calcular nueva fecha de vencimiento sugerida: hoy + 30 días
        from datetime import date, timedelta
        nueva_vencimiento = (date.today() + timedelta(days=30)).strftime('%Y-%m-%d')

        datos_base = {
            'id_paciente':               presupuesto.get('id_paciente'),
            'id_profesional':            presupuesto.get('id_profesional'),
            'id_moneda':                 presupuesto.get('id_moneda'),
            'fecha_vencimiento_sugerida': nueva_vencimiento,
            'presupuesto_observaciones': presupuesto.get('presupuesto_observaciones'),
            'detalle':                   presupuesto.get('detalle', []),
            # Metadatos de referencia para el formulario
            'presupuesto_numero_base':   presupuesto.get('presupuesto_numero'),
            'paciente_nombre':           presupuesto.get('paciente_nombre'),
            'profesional_nombre':        presupuesto.get('profesional_nombre'),
        }

        return jsonify({'success': True, 'data': datos_base, 'error': None}), 200

    except Exception as e:
        app.logger.error(f"Error al duplicar presupuesto {id_presupuesto}: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
