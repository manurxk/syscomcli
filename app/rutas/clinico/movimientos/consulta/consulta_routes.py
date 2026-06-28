from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

consultamod = Blueprint('consulta', __name__, template_folder='templates')

ROLES_CONSULTA = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@consultamod.route('/consulta-index')
@role_required(*ROLES_CONSULTA)
def consultaIndex():
    return render_template('consulta-index.html')


@consultamod.route('/consulta-agregar')
@consultamod.route('/consulta-editar/<int:id_consulta>')
@role_required(*ROLES_CONSULTA)
def consultaAgregar(id_consulta=None):
    """Página para registrar/editar una consulta, con sección de anamnesis del paciente."""
    return render_template('consulta-agregar.html', id_consulta=id_consulta)
