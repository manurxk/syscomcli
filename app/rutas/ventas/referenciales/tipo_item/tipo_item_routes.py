from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

tipoitemmod = Blueprint('tipo_item', __name__, template_folder='templates')


@tipoitemmod.route('/tipo-item-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def tipoItemIndex():
    return render_template('tipo-item-index.html')
