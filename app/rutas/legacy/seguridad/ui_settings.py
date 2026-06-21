from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, session
from app.services.ui_settings_service import UISettingsService
from app.rutas.seguridad.dashboard import es_superadmin

ui_settings_bp = Blueprint('ui_settings', __name__, url_prefix='/configuracion-ui')

@ui_settings_bp.route('/')
def index():
    if not es_superadmin():
        return redirect(url_for('dashboard.index'))
    
    preferencias = UISettingsService.obtener_preferencias()
    return render_template('configuracion-ui-index.html', preferencias=preferencias)

@ui_settings_bp.route('/actualizar', methods=['POST'])
def actualizar():
    if not es_superadmin():
        return jsonify({'success': False, 'error': 'No autorizado'}), 403
    
    data = request.json
    componente = data.get('componente')
    color_clase = data.get('color_clase')
    
    if not componente or not color_clase:
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400
    
    exito = UISettingsService.actualizar_preferencia(componente, color_clase)
    
    if exito:
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Error al actualizar en base de datos'}), 500
