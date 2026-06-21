from flask import Blueprint, render_template

presupuestomod = Blueprint('registrarpresupuesto', __name__, template_folder='templates')

@presupuestomod.route('/presupuesto-index')
def presupuestoIndex():
    return render_template('registrarpresupuesto-index.html')


















