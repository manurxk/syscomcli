from flask import Blueprint, render_template

certificadomedicomod = Blueprint('registrarcertificadomedico', __name__, template_folder='templates')


@certificadomedicomod.route('/certificado-medico-index')
def certificadoMedicoIndex():
    """Página principal de gestión de certificados médicos"""
    return render_template('registrarcertificadomedico-index.html')

