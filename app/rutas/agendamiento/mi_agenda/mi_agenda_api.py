from flask import Blueprint, jsonify, current_app as app, session
from app.dao.agendamiento.cita.CitaDao import CitaDao
from app.auth.utils.decorators import role_required

miagendaapi = Blueprint('miagendaapi', __name__)


@miagendaapi.route('/mi-agenda/citas-hoy', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "CLINICO")
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
