from flask import Blueprint, jsonify, session
from app.auth.utils.decorators import role_required
from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
from app.utils.especialista_helper import obtener_id_especialista_usuario

miagendaapi = Blueprint('miagendaapi', __name__)


@miagendaapi.route('/mi-agenda/citas-hoy', methods=['GET'])
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def getCitasHoy():
    """
    Devuelve las citas del día actual para el especialista logueado.
    Si el usuario no tiene especialista asociado, devuelve lista vacía.
    """
    id_especialista = obtener_id_especialista_usuario()

    if not id_especialista:
        return jsonify({
            'success': True,
            'citas': [],
            'total': 0,
            'mensaje': 'El usuario no tiene un especialista asociado.',
            'sin_especialista': True
        })

    dao = CitaDao()
    citas = dao.getCitasHoyByEspecialista(id_especialista)

    return jsonify({
        'success': True,
        'citas': citas,
        'total': len(citas),
        'id_especialista': id_especialista,
        'sin_especialista': False
    })
