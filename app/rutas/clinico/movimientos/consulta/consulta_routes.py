from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

consultamod = Blueprint('consulta', __name__, template_folder='templates')

ROLES_CONSULTA = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@consultamod.route('/consulta-index')
@role_required(*ROLES_CONSULTA)
def consultaIndex():
    return render_template('consulta-index.html')


@consultamod.route('/consulta-editar/<int:id_consulta>')
@role_required(*ROLES_CONSULTA)
def consultaAgregar(id_consulta):
    """Página de atención de una consulta (anamnesis + registro clínico). Solo se llega acá
    después de 'Iniciar consulta' desde una cita — no hay alta manual suelta."""
    return render_template('consulta-agregar.html', id_consulta=id_consulta)
