from flask import Blueprint, render_template

tipo_item_mod = Blueprint('tipo_item', __name__, template_folder='templates')

@tipo_item_mod.route('/tipo-item-index')
def tipoItemIndex():
    return render_template('tipo-item-index.html')


















