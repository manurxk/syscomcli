from flask import Blueprint, render_template, abort
from app.auth.utils.decorators import role_required
from app.utils.ficha_acceso import puede_ver_ficha, registrar

fichamod = Blueprint('ficha', __name__, template_folder='templates')

ROLES_FICHA = ("ADMINISTRADOR", "CLINICO")


@fichamod.route('/ficha-index')
@role_required(*ROLES_FICHA)
def fichaIndex():
    """Página de búsqueda de pacientes para abrir su ficha (el clínico ve solo los pacientes con los que tiene vínculo)."""
    return render_template('ficha-index.html')


@fichamod.route('/ficha-paciente/<int:id_paciente>')
@role_required(*ROLES_FICHA)
def fichaPaciente(id_paciente):
    """Página con la ficha clínica del paciente indicado. Solo con vínculo (o Administrador); queda registrado en la
    auditoría quién la abrió, y también los intentos rechazados."""
    if not puede_ver_ficha(id_paciente):
        registrar(id_paciente, 'Intentó abrir sin vínculo la ficha clínica de')
        abort(403)
    registrar(id_paciente, 'Abrió la ficha clínica de')
    return render_template('ficha-paciente.html', id_paciente=id_paciente)
