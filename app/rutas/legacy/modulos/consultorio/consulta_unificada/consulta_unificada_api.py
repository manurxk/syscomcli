from flask import Blueprint, jsonify, abort, current_app as app
from app.auth.utils.decorators import role_required
from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
from app.dao.modulos.consultorio.consulta.ReConsultaDao import ConsultaDao
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes

consultaunificadaapi = Blueprint('consultaunificadaapi', __name__)


def _verificar_acceso_cita(cita):
    """Verifica que el especialista logueado puede operar esta cita. Abort 403 si no."""
    if not puede_ver_todos_pacientes():
        id_esp = obtener_id_especialista_usuario()
        if id_esp and cita['id_especialista'] != id_esp:
            abort(403)


@consultaunificadaapi.route('/consulta/<int:id_cita>/detalle', methods=['GET'])
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def getDetalleCita(id_cita):
    """Retorna el detalle completo de la cita para el panel lateral."""
    dao = CitaDao()
    cita = dao.getCitaById(id_cita)

    if not cita:
        return jsonify({'success': False, 'mensaje': 'Cita no encontrada'}), 404

    _verificar_acceso_cita(cita)

    return jsonify({'success': True, 'cita': cita})


@consultaunificadaapi.route('/consulta/<int:id_cita>/iniciar', methods=['POST'])
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def iniciarConsulta(id_cita):
    """Inicia la consulta: crea registro en consultas y retorna id_consulta."""
    try:
        dao_cita = CitaDao()
        cita = dao_cita.getCitaById(id_cita)

        if not cita:
            return jsonify({'success': False, 'mensaje': 'Cita no encontrada'}), 404

        _verificar_acceso_cita(cita)

        estado_actual = (cita.get('estado_nombre') or '').upper().strip()
        app.logger.info(f"iniciarConsulta: cita={id_cita}, estado='{estado_actual}', pac={cita.get('id_paciente')}, esp={cita.get('id_especialista')}")

        if 'COMPLET' in estado_actual or 'CANCEL' in estado_actual:
            return jsonify({
                'success': False,
                'mensaje': f"No se puede iniciar la consulta con estado {estado_actual}."
            }), 400

        # Obtener o crear el registro en tabla consultas
        dao_consulta = ConsultaDao()
        consulta = dao_consulta.getConsultaDesdeCita(id_cita)
        app.logger.info(f"iniciarConsulta: consulta_existente={'si' if consulta else 'no'}")

        if not consulta:
            from flask import session
            usuario = session.get('usu_nick', 'ADMIN')
            fecha_consulta = f"{cita.get('cita_fecha', '')} {cita.get('cita_hora_inicio', '00:00')}"
            motivo = cita.get('cita_motivo') or 'Consulta iniciada desde agenda'
            app.logger.info(f"iniciarConsulta: guardando consulta fecha={fecha_consulta}")
            id_consulta = dao_consulta.guardarConsulta(
                id_paciente=cita['id_paciente'],
                id_profesional=cita['id_especialista'],
                consulta_fecha=fecha_consulta,
                consulta_motivo=motivo,
                consulta_estado='EN_ATENCION',
                id_cita=id_cita,
                usuario_creacion=usuario
            )
            app.logger.info(f"iniciarConsulta: id_consulta={id_consulta}")
            if not id_consulta:
                return jsonify({'success': False, 'mensaje': 'No se pudo crear el registro de consulta.'}), 500
        else:
            id_consulta = consulta['id_consulta']
            app.logger.info(f"iniciarConsulta: usando consulta existente id={id_consulta}")

        # Cambiar estado de la cita (no bloqueante)
        if estado_actual != 'EN_CONSULTA':
            ok = dao_cita.cambiarEstadoCita(id_cita, 'EN_CONSULTA')
            app.logger.info(f"iniciarConsulta: cambiarEstado={ok}")

        return jsonify({
            'success': True,
            'mensaje': 'Consulta iniciada. Tabs habilitados.',
            'id_consulta': id_consulta
        })

    except Exception as e:
        app.logger.error(f"ERROR CRITICO iniciarConsulta cita={id_cita}: {e}", exc_info=True)
        return jsonify({'success': False, 'mensaje': f'Error interno: {str(e)}'}), 500


@consultaunificadaapi.route('/consulta/<int:id_cita>/cerrar', methods=['POST'])
@role_required("ADMINISTRADOR", "ESPECIALISTA")
def cerrarConsulta(id_cita):
    """
    Cambia el estado de la cita a COMPLETADA y marca la consulta como FINALIZADA.
    """
    dao_cita = CitaDao()
    cita = dao_cita.getCitaById(id_cita)

    if not cita:
        return jsonify({'success': False, 'mensaje': 'Cita no encontrada'}), 404

    _verificar_acceso_cita(cita)

    estado_actual = (cita.get('estado_nombre') or '').upper()
    if estado_actual == 'COMPLETADA':
        return jsonify({'success': True, 'mensaje': 'La consulta ya estaba completada.'})

    # Marcar la consulta clínica como FINALIZADA
    dao_consulta = ConsultaDao()
    consulta = dao_consulta.getConsultaDesdeCita(id_cita)
    if consulta:
        from flask import session
        usuario = session.get('usu_nick', 'ADMIN')
        dao_consulta.updateConsulta(
            id_consulta=consulta['id_consulta'],
            consulta_fecha=consulta.get('consulta_fecha', ''),
            consulta_motivo=consulta.get('consulta_motivo', ''),
            consulta_estado='FINALIZADA',
            usuario_modificacion=usuario
        )

    # Cambiar estado de la cita
    ok = dao_cita.cambiarEstadoCita(id_cita, 'COMPLETADA')
    if ok:
        return jsonify({'success': True, 'mensaje': 'Consulta cerrada exitosamente.'})
    else:
        return jsonify({'success': False, 'mensaje': 'Error al cerrar la consulta.'}), 500
