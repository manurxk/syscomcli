from flask import Blueprint, render_template

anamnesismod = Blueprint('anamnesis', __name__, template_folder='templates')

@anamnesismod.route('/anamnesis-index')
def anamnesisIndex():
    return render_template('anamnesis-index.html')