from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

instrumentomod = Blueprint('instrumento', __name__, template_folder='templates')


@instrumentomod.route('/instrumento-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def instrumentoIndex():
    return render_template('instrumento-index.html')
