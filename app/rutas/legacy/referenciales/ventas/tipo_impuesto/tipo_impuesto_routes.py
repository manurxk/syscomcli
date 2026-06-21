from flask import Blueprint, render_template

tipo_impuesto_mod = Blueprint('tipo_impuesto', __name__, template_folder='templates')

@tipo_impuesto_mod.route('/tipo-impuesto-index')
def tipoImpuestoIndex():
    return render_template('tipo-impuesto-index.html')


















