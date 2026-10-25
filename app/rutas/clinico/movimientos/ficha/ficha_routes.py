from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

fichamod = Blueprint('ficha', __name__, template_folder='templates')

ROLES_FICHA = ("ADMINISTRADOR", "CLINICO")


@fichamod.route('/ficha-index')
@role_required(*ROLES_FICHA)
def fichaIndex():
    """Página de búsqueda de pacientes para abrir su ficha."""
    return render_template('ficha-index.html')


@fichamod.route('/ficha-paciente/<int:id_paciente>')
@role_required(*ROLES_FICHA)
def fichaPaciente(id_paciente):
    """Página con la ficha clínica del paciente indicado."""
    return render_template('ficha-paciente.html', id_paciente=id_paciente)
