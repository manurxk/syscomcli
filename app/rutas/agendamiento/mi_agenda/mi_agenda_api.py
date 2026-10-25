from datetime import datetime

from flask import Blueprint, jsonify, request, current_app as app, session
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.auth.utils.decorators import role_required

miagendaapi = Blueprint('miagendaapi', __name__)


@miagendaapi.route('/mi-agenda/citas-semana', methods=['GET'])
@role_required("ADMINISTRADOR", "CLINICO")
def getCitasSemana():
    """Citas del especialista logueado entre dos fechas (YYYY-MM-DD), para el calendario semanal de Mi Agenda.
    Solo devuelve las suyas; con id_especialista para que la pantalla pida también sus horarios de atención."""
    try:
        desde, hasta = request.args.get('desde', ''), request.args.get('hasta', '')
        try:
            datetime.strptime(desde, '%Y-%m-%d'); datetime.strptime(hasta, '%Y-%m-%d')
        except ValueError:
            return jsonify({'success': False, 'error': 'Indique las fechas desde y hasta (AAAA-MM-DD).'}), 400

        id_funcionario = session.get('id_funcionario')
        dao = CitaDao()
        id_especialista = dao.getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None
        if not id_especialista:
            return jsonify({'success': True, 'data': [], 'id_especialista': None, 'sin_especialista': True, 'error': None}), 200

        data = dao.getCitas(id_especialista, None, desde, f'{hasta} 23:59:59')
        return jsonify({'success': True, 'data': data, 'id_especialista': id_especialista, 'sin_especialista': False, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener la semana de mi agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@miagendaapi.route('/mi-agenda/citas-hoy', methods=['GET'])
@role_required("ADMINISTRADOR", "CLINICO")
def getCitasHoy():
    """Citas de hoy del especialista logueado (resuelto desde session['id_funcionario'])."""
    try:
        id_funcionario = session.get('id_funcionario')
        dao = CitaDao()
        id_especialista = dao.getEspecialistaPorFuncionario(id_funcionario) if id_funcionario else None

        if not id_especialista:
            return jsonify({'success': True, 'data': [], 'sin_especialista': True, 'error': None}), 200

        data = dao.getCitasHoyByEspecialista(id_especialista)
        return jsonify({'success': True, 'data': data, 'sin_especialista': False, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener mi agenda: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
