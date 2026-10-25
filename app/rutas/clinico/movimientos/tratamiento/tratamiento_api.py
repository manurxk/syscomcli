from datetime import date, datetime, timedelta

from flask import Blueprint, request, jsonify, current_app as app, session

from app.dao.agendamiento.agenda_horarios.AgendaHorariosDao import AgendaHorariosDao
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.dao.clinico.movimientos.tratamiento.TratamientoDao import TratamientoDao
from app.auth.utils.decorators import role_required
from app.utils.mensajes_validacion import msg_obligatorio

tratamientoapi = Blueprint('tratamientoapi', __name__)

ROLES_TRATAMIENTO = ("ADMINISTRADOR", "CLINICO")
MAX_SESIONES_TANDA = 15


@tratamientoapi.route('/consultas/<int:id_consulta>/tratamientos', methods=['GET'])
@role_required(*ROLES_TRATAMIENTO)
def getTratamientos(id_consulta):
    """GET: lista los tratamientos de la consulta."""
    try:
        data = TratamientoDao().getPorConsulta(id_consulta)
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener tratamientos de la consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/consultas/<int:id_consulta>/tratamientos', methods=['POST'])
@role_required(*ROLES_TRATAMIENTO)
def addTratamiento(id_consulta):
    """POST: valida y registra tratamiento en la consulta (201)."""
    data = request.get_json() or {}
    if not data.get('id_tipo_tratamiento'):
        return jsonify({'success': False, 'error': msg_obligatorio('Tipo de tratamiento')}), 400
    if not (data.get('des_tratamiento') or '').strip():
        return jsonify({'success': False, 'error': msg_obligatorio('Descripción del tratamiento')}), 400
    if not data.get('tratamiento_fecha_inicio'):
        return jsonify({'success': False, 'error': msg_obligatorio('Fecha de inicio')}), 400

    try:
        nuevo_id = TratamientoDao().guardar(id_consulta, data, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_tratamiento': nuevo_id}, 'error': None}), 201
    except Exception as e:
        app.logger.error(f"Error al guardar tratamiento de consulta: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>', methods=['DELETE'])
@role_required(*ROLES_TRATAMIENTO)
def deleteTratamiento(id_tratamiento):
    """DELETE: baja lógica de tratamiento; 404 si no existe."""
    try:
        if TratamientoDao().desactivar(id_tratamiento, session.get('id_usuario')):
            return jsonify({'success': True, 'mensaje': 'Registro eliminado correctamente.', 'error': None}), 200
        return jsonify({'success': False, 'error': 'No se encontró el registro con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al eliminar tratamiento de consulta: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ----------------------------------------------------------------------
# Plan de sesiones: el especialista agenda por tandas las citas de Tratamiento de su paciente.
# Solo el especialista que indicó el tratamiento; solo en su propia agenda; solo hasta donde hay turnos generados
# (AgendaHorariosDao.HORIZONTE_DIAS_DEFAULT). Reusa CitaDao.crearCita: mismas reglas y auditoría que una cita de recepción.
# ----------------------------------------------------------------------

def _contextoPlan(id_tratamiento, exigir_activo=True):
    """(contexto, error): el tratamiento es del especialista logueado y, salvo que se indique, está activo."""
    id_funcionario = session.get('id_funcionario')
    id_especialista = CitaDao().getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
    ctx = TratamientoDao().getContextoPlan(id_tratamiento)
    if not ctx or not id_especialista or ctx['id_especialista'] != id_especialista:
        return None, ('No se encontró el tratamiento con el ID proporcionado.', 404)
    if exigir_activo and ctx['tratamiento_estado'] != 'ACTIVO':
        return None, ('El tratamiento no está activo: reactívelo para agendar más sesiones.', 400)
    return ctx, None


def _estadoPlan(ctx, sesiones):
    agendadas = sum(1 for x in sesiones if x['valida'])
    total = ctx['numero_sesiones']
    return {
        'agendadas': agendadas,
        'total': total,
        'restantes': max(total - agendadas, 0) if total else None,
        'max_tanda': MAX_SESIONES_TANDA,
        'horizonte_hasta': (date.today() + timedelta(days=AgendaHorariosDao.HORIZONTE_DIAS_DEFAULT)).isoformat(),
    }


def _validarCantidad(cantidad, estado):
    """(cantidad, error): entre 1 y el tope de la tanda, sin pasar de lo que le falta al plan."""
    try:
        cantidad = int(cantidad)
    except (TypeError, ValueError):
        return None, msg_obligatorio('Cantidad de sesiones')
    if not 1 <= cantidad <= MAX_SESIONES_TANDA:
        return None, f'La tanda debe tener entre 1 y {MAX_SESIONES_TANDA} sesiones.'
    if estado['restantes'] is not None and cantidad > estado['restantes']:
        return None, f"Al plan le faltan {estado['restantes']} sesiones: la tanda no puede tener {cantidad}."
    return cantidad, None


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>/plan', methods=['GET'])
@role_required("CLINICO")
def getPlanTratamiento(id_tratamiento):
    """GET: el plan del tratamiento: sus datos, las sesiones ya agendadas y cuánto falta."""
    try:
        ctx, error = _contextoPlan(id_tratamiento, exigir_activo=False)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        dao = TratamientoDao()
        sesiones = dao.getSesionesPlan(id_tratamiento)
        data = {
            'estado': ctx['tratamiento_estado'], 'futuras': len(dao.getSesionesFuturas(id_tratamiento)),
            'id_tratamiento': id_tratamiento, 'id_especialista': ctx['id_especialista'], 'id_consulta': ctx['id_consulta'],
            'paciente': f"{ctx['paciente_nombre']} {ctx['paciente_apellido']}".strip(),
            'tipo': ctx['des_tipo_tratamiento'], 'descripcion': ctx['des_tratamiento'],
            'frecuencia': ctx['frecuencia_sesiones'],
            'sesiones': sesiones, **_estadoPlan(ctx, sesiones),
        }
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener el plan del tratamiento: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>/plan/proponer', methods=['POST'])
@role_required("CLINICO")
def proponerPlanTratamiento(id_tratamiento):
    """POST: propone la próxima tanda sin guardar nada. Recibe fecha_inicio, cantidad y dias
    ([{dia: 1 a 7 (lunes a domingo), hora: 'HH:MM'}]). Cada sesión sale con `ok` y, si no, el `motivo` y los
    turnos libres de ese día (`alternativas`) para moverla."""
    data = request.get_json() or {}
    try:
        ctx, error = _contextoPlan(id_tratamiento)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        dao = TratamientoDao()
        estado = _estadoPlan(ctx, dao.getSesionesPlan(id_tratamiento))

        cantidad, error = _validarCantidad(data.get('cantidad'), estado)
        if error:
            return jsonify({'success': False, 'error': error}), 400
        try:
            inicio = datetime.strptime(data.get('fecha_inicio') or '', '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'success': False, 'error': msg_obligatorio('Fecha de inicio')}), 400
        dias = []
        for d in data.get('dias') or []:
            try:
                dia, hora = int(d['dia']), datetime.strptime(d['hora'], '%H:%M').strftime('%H:%M')
            except (KeyError, TypeError, ValueError):
                return jsonify({'success': False, 'error': 'Cada día debe indicar el día de la semana y la hora (HH:MM).'}), 400
            if not 1 <= dia <= 7:
                return jsonify({'success': False, 'error': 'El día de la semana debe ser de 1 (lunes) a 7 (domingo).'}), 400
            dias.append((dia, hora))
        if not dias:
            return jsonify({'success': False, 'error': 'Marque al menos un día de la semana.'}), 400

        desde = max(inicio, date.today())
        hasta = date.fromisoformat(estado['horizonte_hasta'])
        slots = dao.getSlotsPlan(ctx['id_especialista'], desde.isoformat(), hasta.isoformat())
        por_inicio = {s['slot_inicio']: s for s in slots}
        libres_por_dia = {}
        for s in slots:
            if s['estado_slot'] == 'DISPONIBLE' and not s['vencido']:
                libres_por_dia.setdefault(s['slot_inicio'][:10], []).append(
                    {'id_slot_agenda': s['id_slot_agenda'], 'hora': s['slot_inicio'][11:]})

        sesiones, dia_actual = [], desde
        while dia_actual <= hasta and len(sesiones) < cantidad:
            for dia, hora in sorted(x for x in dias if x[0] == dia_actual.isoweekday()):
                if len(sesiones) >= cantidad:
                    break
                fecha = dia_actual.isoformat()
                slot = por_inicio.get(f'{fecha} {hora}')
                if slot is None:
                    motivo = 'Fuera de tu horario de atención'
                elif slot['estado_slot'] == 'RESERVADO':
                    motivo = 'Sin cupo: horario ocupado'
                elif slot['estado_slot'] != 'DISPONIBLE':
                    motivo = 'Bloqueado (ausencia o feriado)'
                elif slot['vencido']:
                    motivo = 'El turno ya pasó'
                else:
                    motivo = None
                sesiones.append({
                    'fecha': fecha, 'hora': hora, 'ok': motivo is None, 'motivo': motivo,
                    'id_slot_agenda': slot['id_slot_agenda'] if motivo is None else None,
                    'alternativas': [] if motivo is None else libres_por_dia.get(fecha, []),
                })
            dia_actual += timedelta(days=1)
        for i, x in enumerate(sesiones):
            x['numero'] = estado['agendadas'] + i + 1
        resultado = {'sesiones': sesiones, 'pedidas': cantidad, 'incompleta': len(sesiones) < cantidad,
                     'horizonte_hasta': estado['horizonte_hasta']}
        return jsonify({'success': True, 'data': resultado, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al proponer la tanda del tratamiento: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>/plan/confirmar', methods=['POST'])
@role_required("CLINICO")
def confirmarPlanTratamiento(id_tratamiento):
    """POST: crea las citas de la tanda (201). Recibe sesiones: [{id_slot_agenda}]. Todo o nada: si un turno ya
    no está libre no se crea ninguna cita."""
    data = request.get_json() or {}
    try:
        ctx, error = _contextoPlan(id_tratamiento)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        dao = TratamientoDao()
        estado = _estadoPlan(ctx, dao.getSesionesPlan(id_tratamiento))

        ids = [x.get('id_slot_agenda') for x in data.get('sesiones') or [] if isinstance(x, dict)]
        if not ids or not all(isinstance(i, int) for i in ids):
            return jsonify({'success': False, 'error': 'No hay sesiones para confirmar.'}), 400
        if len(set(ids)) != len(ids):
            return jsonify({'success': False, 'error': 'Hay dos sesiones en el mismo turno.'}), 400
        _, error = _validarCantidad(len(ids), estado)
        if error:
            return jsonify({'success': False, 'error': error}), 400
        propietarios = dao.getEspecialistaDeSlots(ids)
        if any(propietarios.get(i) != ctx['id_especialista'] for i in ids):
            return jsonify({'success': False, 'error': 'Los turnos deben ser de tu propia agenda.'}), 400

        motivo = f"Tratamiento: {ctx['des_tipo_tratamiento']}"
        lista = [{
            'id_paciente': ctx['id_paciente'], 'id_slot_agenda': i, 'modalidad': 'PRESENCIAL',
            'tipo_cita': 'TRATAMIENTO', 'cita_es_primera_vez': False, 'motivo': motivo,
        } for i in ids]
        ids_citas = CitaDao().crearCitasTratamiento(id_tratamiento, lista, usuario_creacion=session.get('id_usuario'))
        return jsonify({'success': True, 'data': {'id_citas': ids_citas}, 'error': None}), 201
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        app.logger.error(f"Error al confirmar la tanda del tratamiento: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# Estados del tratamiento a los que se puede pasar desde cada uno (ACTIVO ya está activo, FINALIZADO se puede reabrir)
TRANSICIONES_TRATAMIENTO = {
    'ACTIVO': ('FINALIZADO', 'SUSPENDIDO'),
    'SUSPENDIDO': ('ACTIVO', 'FINALIZADO'),
    'FINALIZADO': ('ACTIVO',),
}


@tratamientoapi.route('/tratamientos/<int:id_tratamiento>/estado', methods=['PATCH'])
@role_required("CLINICO")
def cambiarEstadoTratamiento(id_tratamiento):
    """PATCH: finaliza, suspende o reactiva el plan de tratamiento. Recibe estado y, al finalizar o suspender,
    cancelar_futuras (true cancela las citas del plan que todavía no ocurrieron; false las deja como están)."""
    data = request.get_json() or {}
    nuevo = data.get('estado')
    try:
        ctx, error = _contextoPlan(id_tratamiento, exigir_activo=False)
        if error:
            return jsonify({'success': False, 'error': error[0]}), error[1]
        if nuevo not in TRANSICIONES_TRATAMIENTO.get(ctx['tratamiento_estado'], ()):
            return jsonify({'success': False, 'error': f"El tratamiento está {ctx['tratamiento_estado'].lower()}: no se puede pasar a {str(nuevo).lower()}."}), 400
        dao = TratamientoDao()
        usuario = session.get('id_usuario')
        canceladas, fallidas = 0, 0
        if nuevo != 'ACTIVO' and data.get('cancelar_futuras'):
            for cita in dao.getSesionesFuturas(id_tratamiento):
                try:
                    CitaDao().cambiarEstadoCita(cita['id_cita'], 'CANCELADA', usuario_modificacion=usuario,
                                                motivo=f"Tratamiento {nuevo.lower()}")
                    canceladas += 1
                except ValueError as e:
                    fallidas += 1
                    app.logger.warning(f"No se pudo cancelar la cita {cita['id_cita']} del plan {id_tratamiento}: {e}")
        dao.cambiarEstado(id_tratamiento, nuevo, usuario)
        return jsonify({'success': True, 'data': {'estado': nuevo, 'canceladas': canceladas, 'fallidas': fallidas}, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al cambiar el estado del tratamiento: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
