from flask import Blueprint, render_template
from datetime import datetime

informacionmod = Blueprint('informacion', __name__, template_folder='templates')

@informacionmod.route('/privacidad')
def privacidad():
    """Página de política de privacidad"""
    return render_template('privacidad.html', 
                         current_year=datetime.now().year)

@informacionmod.route('/soporte')
def soporte():
    """Página de información de soporte"""
    return render_template('soporte.html',
                         current_year=datetime.now().year)

@informacionmod.route('/contacto')
def contacto():
    """Página de contacto"""
    return render_template('contacto.html',
                         current_year=datetime.now().year)

















