from flask import Blueprint, render_template

cuenta_cobrar_mod = Blueprint('cuenta_cobrar', __name__, template_folder='templates')

@cuenta_cobrar_mod.route('/cuenta-cobrar-index')
def cuentaCobrarIndex():
    """Página principal de gestión de cuentas a cobrar"""
    return render_template('registrar-cuenta-cobrar-index.html')


















