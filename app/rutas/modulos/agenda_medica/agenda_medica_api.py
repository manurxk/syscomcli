from flask import Blueprint, request, jsonify, session, current_app as app
from app.dao.modulos.agenda_medica.Agenda_MedicaDao import AgendaDao
from app.auth.utils.decorators import role_required
import traceback

agendaapi = Blueprint('agendaapi', __name__)


@agendaapi.route('/agenda', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getAllAgendas():
    """Obtiene la lista completa de agendas configuradas"""
    agendadao = AgendaDao()
    
    try:
        agendas = agendadao.getAllAgendas()
        return jsonify({'success': True, 'data': agendas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las agendas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


@agendaapi.route('/agenda/<int:id_agenda_horario>', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getAgenda(id_agenda_horario):
    """Obtiene una configuración de agenda específica por su ID"""
    agendadao = AgendaDao()
    
    try:
        agenda = agendadao.getAgendaById(id_agenda_horario)
        
        if agenda:
            return jsonify({'success': True, 'data': agenda, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la agenda con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


@agendaapi.route('/agenda/<int:id_agenda_horario>/editar', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getAgendaParaEditar(id_agenda_horario):
    """Obtiene agenda con IDs originales para formulario de edición"""
    agendadao = AgendaDao()

    try:
        agenda = agendadao.getAgendaParaEditar(id_agenda_horario)

        if agenda:
            return jsonify({'success': True, 'data': agenda, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la agenda.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener agenda para editar: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/agenda', methods=['POST'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def addAgenda():
    """Crea una nueva configuración de agenda"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    agendadao = AgendaDao()

    # A partir del nuevo diseño, la agenda solo define disponibilidad
    # del especialista; la especialidad se elige al crear la cita.
    campos_requeridos = [
        'id_especialista', 'id_consultorio', 
        'id_dia_semana', 'hora_inicio', 'hora_fin', 'duracion_turno'
    ]

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    # Validaciones adicionales
    if data['hora_inicio'] >= data['hora_fin']:
        return jsonify({'success': False, 'error': 'La hora de inicio debe ser menor que la hora de fin.'}), 400
    
    if data.get('fecha_hasta') and data.get('fecha_desde'):
        if data['fecha_hasta'] < data['fecha_desde']:
            return jsonify({'success': False, 'error': 'La fecha hasta debe ser mayor o igual que la fecha desde.'}), 400

    try:
        # Normalizar turno: convertir 'MAÑANA'/'TARDE' a 'Mañana'/'Tarde'
        turno_raw = data.get('turno', 'MAÑANA').upper()
        if 'MANANA' in turno_raw or 'MAÑANA' in turno_raw:
            turno = 'Mañana'
        elif 'TARDE' in turno_raw:
            turno = 'Tarde'
        else:
            # Determinar por hora si no está especificado
            hora_num = int(data['hora_inicio'].split(':')[0])
            turno = 'Mañana' if hora_num < 13 else 'Tarde'
        
        # Calcular cupos si no se proporciona
        cupos_totales = data.get('cupos_totales')
        if not cupos_totales:
            hora_inicio = data['hora_inicio']
            hora_fin = data['hora_fin']
            duracion = data['duracion_turno']
            h1, m1 = map(int, hora_inicio.split(':'))
            h2, m2 = map(int, hora_fin.split(':'))
            minutos_totales = (h2 * 60 + m2) - (h1 * 60 + m1)
            cupos_totales = max(1, minutos_totales // duracion)
        
        agenda_id = agendadao.guardarAgenda(
            id_especialista=data['id_especialista'],
            id_consultorio=data['id_consultorio'],
            id_dia_semana=data['id_dia_semana'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            duracion_turno=data['duracion_turno'],
            turno=turno,
            cupos_totales=cupos_totales,
            fecha_desde=data.get('fecha_desde'),
            fecha_hasta=data.get('fecha_hasta'),
            creacion_usuario=id_usuario  # Usar usuario de sesión
        )

        if agenda_id is not None:
            return jsonify({
                'success': True,
                'data': {'id_agenda_horario': agenda_id, 'mensaje': 'Agenda creada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la agenda. El consultorio puede estar ocupado en ese horario.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar agenda: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@agendaapi.route('/agenda/<int:id_agenda_horario>', methods=['PUT'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def updateAgenda(id_agenda_horario):
    """Actualiza una configuración de agenda existente"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    data = request.get_json()
    agendadao = AgendaDao()

    agenda_existente = agendadao.getAgendaById(id_agenda_horario)
    if not agenda_existente:
        return jsonify({'success': False, 'error': 'No se encontró la agenda con el ID proporcionado.'}), 404

    # En edición también dejamos de exigir especialidad en la agenda.
    campos_requeridos = [
        'id_consultorio', 'id_dia_semana',
        'hora_inicio', 'hora_fin', 'duracion_turno'
    ]

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({'success': False, 'error': f'El campo {campo} es obligatorio y no puede estar vacío.'}), 400

    # Validaciones adicionales
    if data['hora_inicio'] >= data['hora_fin']:
        return jsonify({'success': False, 'error': 'La hora de inicio debe ser menor que la hora de fin.'}), 400
    
    if data.get('fecha_hasta') and data.get('fecha_desde'):
        if data['fecha_hasta'] < data['fecha_desde']:
            return jsonify({'success': False, 'error': 'La fecha hasta debe ser mayor o igual que la fecha desde.'}), 400

    try:
        # Normalizar turno igual que en POST
        turno_raw = data.get('turno', 'MAÑANA').upper()
        if 'MANANA' in turno_raw or 'MAÑANA' in turno_raw:
            turno = 'Mañana'
        elif 'TARDE' in turno_raw:
            turno = 'Tarde'
        else:
            hora_num = int(data['hora_inicio'].split(':')[0])
            turno = 'Mañana' if hora_num < 13 else 'Tarde'
        
        # Calcular cupos si no se proporciona
        cupos_totales = data.get('cupos_totales')
        if not cupos_totales:
            hora_inicio = data['hora_inicio']
            hora_fin = data['hora_fin']
            duracion = data['duracion_turno']
            h1, m1 = map(int, hora_inicio.split(':'))
            h2, m2 = map(int, hora_fin.split(':'))
            minutos_totales = (h2 * 60 + m2) - (h1 * 60 + m1)
            cupos_totales = max(1, minutos_totales // duracion)
        
        resultado = agendadao.updateAgenda(
            id_agenda_horario=id_agenda_horario,
            id_consultorio=data['id_consultorio'],
            id_dia_semana=data['id_dia_semana'],
            hora_inicio=data['hora_inicio'],
            hora_fin=data['hora_fin'],
            duracion_turno=data['duracion_turno'],
            turno=turno,
            cupos_totales=cupos_totales,
            fecha_desde=data.get('fecha_desde'),
            fecha_hasta=data.get('fecha_hasta'),
            activo=data.get('activo', True),
            modificacion_usuario=id_usuario  # Usar usuario de sesión
        )

        if resultado:
            return jsonify({
                'success': True,
                'data': {'id_agenda_horario': id_agenda_horario, 'mensaje': 'Agenda actualizada exitosamente'},
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la agenda. El consultorio puede estar ocupado en ese horario.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar agenda: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@agendaapi.route('/agenda/<int:id_agenda_horario>', methods=['DELETE'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def deleteAgenda(id_agenda_horario):
    """Elimina lógicamente una configuración de agenda"""
    agendadao = AgendaDao()

    try:
        if agendadao.deleteAgenda(id_agenda_horario):
            return jsonify({
                'success': True,
                'mensaje': f'Agenda con ID {id_agenda_horario} eliminada correctamente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la agenda con el ID proporcionado o no se pudo eliminar.'
            }), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


# ==========================================
# ⭐ NUEVO ENDPOINT: TOGGLE ESTADO
# ==========================================
@agendaapi.route('/agenda/<int:id_agenda_horario>/estado', methods=['PATCH'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def toggleEstadoAgenda(id_agenda_horario):
    """Activa o desactiva una configuración de agenda (toggle de estado)"""
    # Obtener usuario de sesión
    id_usuario = session.get('id_usuario')
    if not id_usuario:
        return jsonify({'success': False, 'error': 'No autenticado'}), 401
    
    agendadao = AgendaDao()
    data = request.get_json()

    # Validar que se envió el campo requerido
    if 'est_agenda_horario' not in data:
        return jsonify({
            'success': False, 
            'error': 'El campo est_agenda_horario es requerido.'
        }), 400

    # Validar que el valor sea booleano
    nuevo_estado = data.get('est_agenda_horario')
    if not isinstance(nuevo_estado, bool):
        return jsonify({
            'success': False, 
            'error': 'El campo est_agenda_horario debe ser un valor booleano (true/false).'
        }), 400

    try:
        # Verificar que la agenda existe
        agenda_existente = agendadao.getAgendaById(id_agenda_horario)
        if not agenda_existente:
            return jsonify({
                'success': False, 
                'error': 'No se encontró la agenda con el ID proporcionado.'
            }), 404

        # Actualizar el estado
        resultado = agendadao.updateEstadoAgenda(
            id_agenda_horario=id_agenda_horario,
            est_agenda_horario=nuevo_estado,
            modificacion_usuario=id_usuario  # Usar usuario de sesión
        )

        if resultado:
            accion = 'activada' if nuevo_estado else 'desactivada'
            return jsonify({
                'success': True,
                'message': f'Agenda {accion} correctamente.',
                'data': {
                    'id_agenda_horario': id_agenda_horario,
                    'est_agenda_horario': nuevo_estado
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el estado de la agenda.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al cambiar estado de agenda: {str(e)}")
        return jsonify({
            'success': False, 
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# NOTA: El endpoint /especialistas está definido en cita_api.py
# Como citaapi se registra después de agendaapi, Flask usa el endpoint de citas
# Ambos DAOs (CitaDao y AgendaDao) ahora tienen la misma estructura para mantener consistencia


@agendaapi.route('/agenda/especialistas/<int:id_especialista>/especialidades', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getEspecialidadesByEspecialista(id_especialista):
    """Obtiene las especialidades de un especialista específico"""
    agendadao = AgendaDao()
    
    try:
        especialidades = agendadao.getEspecialidadesByEspecialista(id_especialista)
        return jsonify({'success': True, 'data': especialidades, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialidades del especialista: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/dias-semana', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getDiasSemana():
    """Obtiene lista de días de la semana"""
    agendadao = AgendaDao()
    
    try:
        dias = agendadao.getDiasSemana()
        return jsonify({'success': True, 'data': dias, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener días de la semana: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/consultorios', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getConsultorios():
    """Obtiene lista de consultorios"""
    agendadao = AgendaDao()
    
    try:
        consultorios = agendadao.getConsultorios()
        return jsonify({'success': True, 'data': consultorios, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener consultorios: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/agenda/especialista/<int:id_especialista>', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getAgendasByEspecialista(id_especialista):
    """Obtiene todas las agendas de un especialista específico"""
    agendadao = AgendaDao()
    
    try:
        agendas = agendadao.getAgendasByEspecialista(id_especialista)
        return jsonify({'success': True, 'data': agendas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener agendas del especialista: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/agenda/matriz-consultorios', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA")
def getAgendaSemanalConsultorio():
    """Obtiene matriz semanal de uso de consultorios"""
    agendadao = AgendaDao()
    id_consultorio = request.args.get('id_consultorio', type=int)
    
    try:
        matriz = agendadao.getAgendaSemanalConsultorio(id_consultorio)
        return jsonify({'success': True, 'data': matriz, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener matriz semanal: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@agendaapi.route('/especialistas/con-agenda', methods=['GET'])
@role_required("ADMINISTRADOR", "RECEPCIONISTA", "ESPECIALISTA")
def getEspecialistasConAgenda():
    """Obtiene lista de especialistas que tienen agenda configurada"""
    agendadao = AgendaDao()
    
    try:
        especialistas = agendadao.getEspecialistasConAgenda()
        return jsonify({'success': True, 'data': especialistas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialistas con agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500