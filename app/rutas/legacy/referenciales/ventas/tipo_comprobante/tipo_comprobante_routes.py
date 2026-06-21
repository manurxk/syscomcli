from flask import Blueprint, render_template

tipo_comprobante_mod = Blueprint('tipo_comprobante', __name__, template_folder='templates')

@tipo_comprobante_mod.route('/tipo-comprobante-index')
def tipoComprobanteIndex():
    return render_template('tipo-comprobante-index.html')


















