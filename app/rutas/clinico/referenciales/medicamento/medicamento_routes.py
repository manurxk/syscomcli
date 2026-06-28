from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

medicamentomod = Blueprint('medicamento', __name__, template_folder='templates')


@medicamentomod.route('/medicamento-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def medicamentoIndex():
    return render_template('medicamento-index.html')
