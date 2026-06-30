from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

peimod = Blueprint('pei', __name__, template_folder='templates')

ROLES_PEI = ("ADMINISTRADOR", "SUPERADMIN", "CLINICO")


@peimod.route('/pei-index')
@role_required(*ROLES_PEI)
def peiIndex():
    return render_template('pei-index.html')


@peimod.route('/pei-agregar')
@role_required(*ROLES_PEI)
def peiAgregarNuevo():
    """Nueva PEI — requiere buscar paciente en la pantalla."""
    return render_template('pei-agregar.html', id_paciente=None)


@peimod.route('/pei-agregar/<int:id_paciente>')
@role_required(*ROLES_PEI)
def peiAgregar(id_paciente):
    """Nueva versión de PEI para un paciente específico."""
    return render_template('pei-agregar.html', id_paciente=id_paciente)
