from flask import Blueprint, render_template, request

presupuestomod = Blueprint('registrarpresupuesto', __name__, template_folder='templates')

@presupuestomod.route('/presupuesto-index')
def presupuestoIndex():
    return render_template('registrarpresupuesto-index.html')

@presupuestomod.route('/presupuesto-agregar')
@presupuestomod.route('/presupuesto-editar/<int:id_presupuesto>')
def presupuestoAgregar(id_presupuesto=None):
    embedded   = request.args.get('embedded', '0') == '1'
    id_paciente = request.args.get('id_paciente', type=int)
    # FASE 3 — TAREA 4: id del presupuesto base para duplicar y actualizar
    id_base    = request.args.get('base', type=int)
    return render_template(
        'registrarpresupuesto-agregar.html',
        embedded=embedded,
        id_presupuesto=id_presupuesto,
        id_paciente=id_paciente,
        id_base=id_base          # Disponible en el template como {{ id_base }}
    )
















