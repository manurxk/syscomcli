from flask import Blueprint, render_template
from app.auth.utils.decorators import role_required

menumod = Blueprint('menu', __name__, template_folder='templates')


@menumod.route('/menu-index')
@role_required("ADMINISTRADOR", "SUPERADMIN")
def menuIndex():
    return render_template('menu-index.html')
