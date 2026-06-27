from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

listaesperamod = Blueprint('lista_espera', __name__, template_folder='templates')


@listaesperamod.route('/lista-espera-index')
@role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCIONISTA")
def listaEsperaIndex():
    return render_template('lista_espera-index.html')
