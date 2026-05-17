from flask import Blueprint, render_template, request
from app.dao.modulos.ventas.cuenta_cobrar.CuentaCobrarDao import CuentaCobrarDao

cobranza_mod = Blueprint('cobranza', __name__, template_folder='templates')

@cobranza_mod.route('/cobranza-index')
def cobranzaIndex():
    """Página principal de gestión de cobranzas"""
    return render_template('registrar-cobranza-index.html')

@cobranza_mod.route('/cobranza-agregar')
def cobranzaAgregar():
    """Página para agregar nueva cobranza"""
    cuenta_id = request.args.get('cuenta', None)
    return render_template('registrar-cobranza-agregar.html', cuenta_id=cuenta_id)


















