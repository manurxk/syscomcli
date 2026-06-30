from flask import Blueprint, jsonify, current_app as app

from app.dao.mantenimiento.referenciales.ciudad.CiudadDao import CiudadDao
from app.dao.mantenimiento.referenciales.departamento.DepartamentoDao import DepartamentoDao
from app.dao.mantenimiento.referenciales.pais.PaisDao import PaisDao
from app.dao.mantenimiento.referenciales.genero.GeneroDao import GeneroDao
from app.dao.mantenimiento.referenciales.estado_civil.EstadoCivilDao import EstadoCivilDao
from app.dao.mantenimiento.referenciales.nivel_instruccion.NivelInstruccionDao import NivelInstruccionDao
from app.dao.mantenimiento.referenciales.profesion.ProfesionDao import ProfesionDao
from app.dao.mantenimiento.referenciales.cargo.CargoDao import CargoDao
from app.dao.agendamiento.referenciales.especialidad.EspecialidadDao import EspecialidadDao
from app.auth.utils.decorators import role_required


referencialesapi = Blueprint('referencialesapi', __name__)


def _listar(dao_fn, campo_id, campo_desc):
    """Adapta filas de BaseDAO (id_x, des_x) al formato {id, descripcion} que espera el frontend."""
    filas = dao_fn()
    return [{'id': f[campo_id], 'descripcion': f[campo_desc]} for f in filas]


# ============================================
# CIUDADES
# ============================================
@referencialesapi.route('/ciudades', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getCiudades():
    try:
        ciudades = CiudadDao().getCiudades()
        data = [{'id': c['id_ciudad'], 'descripcion': c['des_ciudad'], 'id_departamento': c['id_departamento']} for c in ciudades]
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener ciudades: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@referencialesapi.route('/ciudades/<int:id_ciudad>', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getCiudad(id_ciudad):
    try:
        ciudad = CiudadDao().getCiudadById(id_ciudad)
        if not ciudad:
            return jsonify({'success': False, 'error': 'Ciudad no encontrada.'}), 404

        departamento = DepartamentoDao().getDepartamentoById(ciudad['id_departamento'])
        pais = PaisDao().getPaisById(departamento['id_pais']) if departamento else None

        data = {
            'id_ciudad': ciudad['id_ciudad'],
            'desc_ciudad': ciudad['des_ciudad'],
            'id_departamento': departamento['id_departamento'] if departamento else None,
            'desc_departamento': departamento['des_departamento'] if departamento else None,
            'id_pais': pais['id_pais'] if pais else None,
            'desc_pais': pais['des_pais'] if pais else None,
        }
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener ciudad: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# DEPARTAMENTOS Y PAÍSES
# ============================================
@referencialesapi.route('/departamentos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getDepartamentos():
    try:
        data = _listar(DepartamentoDao().getDepartamentos, 'id_departamento', 'des_departamento')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener departamentos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@referencialesapi.route('/paises', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getPaises():
    try:
        data = _listar(PaisDao().getPaises, 'id_pais', 'des_pais')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener países: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# GÉNEROS Y ESTADOS CIVILES
# ============================================
@referencialesapi.route('/generos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getGeneros():
    try:
        data = _listar(GeneroDao().getGeneros, 'id_genero', 'des_genero')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener géneros: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@referencialesapi.route('/estados-civiles', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getEstadosCiviles():
    try:
        data = _listar(EstadoCivilDao().getEstadosCiviles, 'id_estado_civil', 'des_estado_civil')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener estados civiles: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# NIVELES DE INSTRUCCIÓN Y PROFESIONES
# ============================================
@referencialesapi.route('/niveles-instruccion', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getNivelesInstruccion():
    try:
        data = _listar(NivelInstruccionDao().getNivelesInstruccion, 'id_nivel_instruccion', 'des_nivel_instruccion')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener niveles de instrucción: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@referencialesapi.route('/profesiones', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getProfesiones():
    try:
        data = _listar(ProfesionDao().getProfesiones, 'id_profesion', 'des_profesion')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener profesiones: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# CARGOS
# ============================================
@referencialesapi.route('/cargos-permitidos', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN")
def getCargosPermitidos():
    try:
        cargos = CargoDao().getCargos()
        data = [
            {'id': c['id_cargo'], 'descripcion': c['des_cargo'], 'es_clinico': c['es_clinico']}
            for c in cargos
        ]
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener cargos: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ESPECIALIDADES
# ============================================
@referencialesapi.route('/especialidades-permitidas', methods=['GET'])
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")
def getEspecialidades():
    try:
        data = _listar(EspecialidadDao().getEspecialidades, 'id_especialidad', 'des_especialidad')
        return jsonify({'success': True, 'data': data, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener especialidades: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500
