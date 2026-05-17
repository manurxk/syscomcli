from flask import Blueprint, render_template

ordenestudiomod = Blueprint('registrarordenestudio', __name__, template_folder='templates')


@ordenestudiomod.route('/orden-estudio-index')
def ordenEstudioIndex():
    """Página principal de gestión de órdenes de estudios"""
    return render_template('registrarordenestudio-index.html')

