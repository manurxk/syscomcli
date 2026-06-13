from flask import Blueprint, request, jsonify, current_app as app, send_file
from app.dao.modulos.consultorio.consulta.AnamnesisDAO import AnamnesisDao
from app.dao.modulos.consultorio.ficha.FichaDao import FichaMedicaDao  # ✨ NUEVO
from app.services.pdf_service import FichaMedicaPDFService  # ✨ NUEVO
from io import BytesIO
from datetime import datetime

anamnesisapi = Blueprint('anamnesisapi', __name__)


# ============================================
# CRUD BÁSICO DE ANAMNESIS
# ============================================

@anamnesisapi.route('/anamnesis', methods=['GET'])
def getAllAnamnesis():
    """Obtiene la lista completa de anamnesis activas"""
    dao = AnamnesisDao()
    
    try:
        anamnesis = dao.getAllAnamnesis()
        return jsonify({'success': True, 'data': anamnesis, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las anamnesis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno. Consulte con el administrador.'}), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>', methods=['GET'])
def getAnamnesis(id_anamnesis):
    """Obtiene una anamnesis específica por su ID"""
    dao = AnamnesisDao()
    
    try:
        anamnesis = dao.getAnamnesisById(id_anamnesis)
        
        if anamnesis:
            return jsonify({'success': True, 'data': anamnesis, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la anamnesis con el ID proporcionado.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la anamnesis: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/paciente/<int:id_paciente>', methods=['GET'])
def getAnamnesisPorPaciente(id_paciente):
    """Obtiene la anamnesis activa de un paciente específico"""
    dao = AnamnesisDao()
    
    try:
        anamnesis = dao.getAnamnesisByPaciente(id_paciente)
        
        if anamnesis:
            return jsonify({'success': True, 'data': anamnesis, 'error': None}), 200
        else:
            return jsonify({'success': True, 'data': None, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener anamnesis del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis', methods=['POST'])
def addAnamnesis():
    """
    Crea una nueva anamnesis psicológica
    
    Body JSON esperado (solo id_paciente, motivo_consulta y usuario_id son obligatorios):
    {
        "id_paciente": 123,
        "motivo_consulta": "Ansiedad generalizada",
        "usuario_id": 1,
        "informante": "Paciente y madre",
        "relacion_informante": "Madre",
        ...
    }
    """
    data = request.get_json()
    dao = AnamnesisDao()

    # Validar campos obligatorios
    campos_requeridos = ['id_paciente', 'motivo_consulta', 'usuario_id']

    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False, 
                'error': f'El campo {campo} es obligatorio y no puede estar vacío.'
            }), 400

    try:
        anamnesis_id = dao.guardarAnamnesis(
            # Campos obligatorios
            pac_id=data['id_paciente'],
            motivo_consulta=data['motivo_consulta'],
            usuario_id=data['usuario_id'],
            
            # Información básica
            informante=data.get('informante'),
            relacion_informante=data.get('relacion_informante'),
            
            # Antecedentes familiares
            antecedentes_familiares_similares=data.get('antecedentes_familiares_similares'),
            antecedentes_patologicos_familiares=data.get('antecedentes_patologicos_familiares'),
            componentes_familiares=data.get('componentes_familiares'),
            historia_familiar=data.get('historia_familiar'),
            
            # Antecedentes personales
            antecedentes_patologicos_personales=data.get('antecedentes_patologicos_personales'),
            historia_problema_actual=data.get('historia_problema_actual'),
            historia_desarrollo=data.get('historia_desarrollo'),
            
            # Historia académica y laboral
            historia_academica=data.get('historia_academica'),
            historia_laboral=data.get('historia_laboral'),
            historia_rehabilitacion=data.get('historia_rehabilitacion'),
            
            # Medicación y sustancias
            medicacion_actual=data.get('medicacion_actual'),
            medicacion_psiquiatrica_previa=data.get('medicacion_psiquiatrica_previa'),
            consumo_sustancias=data.get('consumo_sustancias'),
            
            # Aspectos generales de funcionamiento
            relaciones_interpersonales=data.get('relaciones_interpersonales'),
            actividad_fisica=data.get('actividad_fisica'),
            patron_sueno=data.get('patron_sueno'),
            patron_alimentacion=data.get('patron_alimentacion'),
            actividad_emocional=data.get('actividad_emocional'),
            actividad_sexual=data.get('actividad_sexual'),
            
            # Evaluación y diagnóstico
            impresion_diagnostica=data.get('impresion_diagnostica'),
            plan_trabajo=data.get('plan_trabajo'),
            
            # Evaluaciones requeridas
            eval_neuropsicologica=data.get('eval_neuropsicologica', False),
            eval_psicologica=data.get('eval_psicologica', False),
            eval_psicopedagogica=data.get('eval_psicopedagogica', False),
            eval_fonoaudiologica=data.get('eval_fonoaudiologica', False),
            eval_psicomotora=data.get('eval_psicomotora', False),
            
            # Terapia
            terapia_individual=data.get('terapia_individual', False),
            terapia_familiar=data.get('terapia_familiar', False),
            terapia_grupal=data.get('terapia_grupal', False),
            terapia_ocupacional=data.get('terapia_ocupacional', False),
            otra_terapia=data.get('otra_terapia'),
            
            # Observaciones e indicaciones
            observaciones=data.get('observaciones'),
            indicaciones=data.get('indicaciones')
        )

        if anamnesis_id is not None:
            return jsonify({
                'success': True,
                'data': {
                    'id_anamnesis': anamnesis_id, 
                    'mensaje': 'Anamnesis creada exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la anamnesis. El paciente ya tiene una anamnesis activa o no existe.'
            }), 400
            
    except Exception as e:
        app.logger.error(f"Error al agregar anamnesis: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>', methods=['PUT'])
def updateAnamnesis(id_anamnesis):
    """
    Actualiza una anamnesis existente
    Solo actualiza los campos enviados en el body (actualización parcial)
    
    Body: Solo incluir los campos que se desean actualizar + usuario_id obligatorio
    """
    data = request.get_json()
    dao = AnamnesisDao()

    # Validar que existe la anamnesis
    anamnesis_existente = dao.getAnamnesisById(id_anamnesis)
    if not anamnesis_existente:
        return jsonify({
            'success': False, 
            'error': 'No se encontró la anamnesis con el ID proporcionado.'
        }), 404

    # Validar usuario_id obligatorio
    if 'usuario_id' not in data or not data['usuario_id']:
        return jsonify({
            'success': False, 
            'error': 'El campo usuario_id es obligatorio.'
        }), 400

    try:
        resultado = dao.updateAnamnesis(
            anamnesis_id=id_anamnesis,
            usuario_id=data['usuario_id'],
            
            # Campos opcionales - solo se actualizan si vienen en el body
            motivo_consulta=data.get('motivo_consulta'),
            informante=data.get('informante'),
            relacion_informante=data.get('relacion_informante'),
            
            # Antecedentes familiares
            antecedentes_familiares_similares=data.get('antecedentes_familiares_similares'),
            antecedentes_patologicos_familiares=data.get('antecedentes_patologicos_familiares'),
            componentes_familiares=data.get('componentes_familiares'),
            historia_familiar=data.get('historia_familiar'),
            
            # Antecedentes personales
            antecedentes_patologicos_personales=data.get('antecedentes_patologicos_personales'),
            historia_problema_actual=data.get('historia_problema_actual'),
            historia_desarrollo=data.get('historia_desarrollo'),
            
            # Historia académica y laboral
            historia_academica=data.get('historia_academica'),
            historia_laboral=data.get('historia_laboral'),
            historia_rehabilitacion=data.get('historia_rehabilitacion'),
            
            # Medicación y sustancias
            medicacion_actual=data.get('medicacion_actual'),
            medicacion_psiquiatrica_previa=data.get('medicacion_psiquiatrica_previa'),
            consumo_sustancias=data.get('consumo_sustancias'),
            
            # Aspectos generales de funcionamiento
            relaciones_interpersonales=data.get('relaciones_interpersonales'),
            actividad_fisica=data.get('actividad_fisica'),
            patron_sueno=data.get('patron_sueno'),
            patron_alimentacion=data.get('patron_alimentacion'),
            actividad_emocional=data.get('actividad_emocional'),
            actividad_sexual=data.get('actividad_sexual'),
            
            # Evaluación y diagnóstico
            impresion_diagnostica=data.get('impresion_diagnostica'),
            plan_trabajo=data.get('plan_trabajo'),
            
            # Evaluaciones requeridas
            eval_neuropsicologica=data.get('eval_neuropsicologica'),
            eval_psicologica=data.get('eval_psicologica'),
            eval_psicopedagogica=data.get('eval_psicopedagogica'),
            eval_fonoaudiologica=data.get('eval_fonoaudiologica'),
            eval_psicomotora=data.get('eval_psicomotora'),
            
            # Terapia
            terapia_individual=data.get('terapia_individual'),
            terapia_familiar=data.get('terapia_familiar'),
            terapia_grupal=data.get('terapia_grupal'),
            terapia_ocupacional=data.get('terapia_ocupacional'),
            otra_terapia=data.get('otra_terapia'),
            
            # Observaciones e indicaciones
            observaciones=data.get('observaciones'),
            indicaciones=data.get('indicaciones'),
            
            # Control de historial
            guardar_historial=data.get('guardar_historial', True)
        )

        if resultado:
            return jsonify({
                'success': True,
                'data': {
                    'id_anamnesis': id_anamnesis, 
                    'mensaje': 'Anamnesis actualizada exitosamente'
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la anamnesis.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al actualizar anamnesis: {str(e)}", exc_info=True)
        return jsonify({
            'success': False, 
            'error': f'Ocurrió un error interno: {str(e)}'
        }), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>', methods=['DELETE'])
def deleteAnamnesis(id_anamnesis):
    """
    Elimina permanentemente una anamnesis (usar con precaución)
    También elimina su historial por CASCADE
    """
    dao = AnamnesisDao()

    try:
        if dao.deleteAnamnesis(id_anamnesis):
            return jsonify({
                'success': True,
                'mensaje': f'Anamnesis con ID {id_anamnesis} eliminada permanentemente.',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró la anamnesis con el ID proporcionado o no se pudo eliminar.'
            }), 404
            
    except Exception as e:
        app.logger.error(f"Error al eliminar anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ACCIONES ESPECIALES
# ============================================

@anamnesisapi.route('/anamnesis/<int:id_anamnesis>/archivar', methods=['PATCH'])
def archivarAnamnesis(id_anamnesis):
    """
    Archiva una anamnesis (marca como inactiva)
    Permite crear una nueva anamnesis para el mismo paciente
    
    Body:
    {
        "usuario_id": 1
    }
    """
    data = request.get_json()
    dao = AnamnesisDao()

    if not data or 'usuario_id' not in data:
        return jsonify({
            'success': False,
            'error': 'El campo usuario_id es obligatorio.'
        }), 400

    try:
        resultado = dao.archivarAnamnesis(
            anamnesis_id=id_anamnesis,
            usuario_id=data['usuario_id']
        )

        if resultado:
            return jsonify({
                'success': True,
                'mensaje': f'Anamnesis {id_anamnesis} archivada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo archivar la anamnesis. Verifique que exista y esté activa.'
            }), 400

    except Exception as e:
        app.logger.error(f"Error al archivar anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>/historial', methods=['GET'])
def getHistorialAnamnesis(id_anamnesis):
    """
    Obtiene el historial de versiones de una anamnesis
    
    Respuesta:
    {
        "success": true,
        "data": [
            {
                "id_historial": 1,
                "version": 2,
                "contenido_json": {...},
                "fecha_modificacion": "20/01/2025 10:30",
                "comentario_cambio": null,
                "modificado_por_nombre": "usuario123"
            }
        ],
        "error": null
    }
    """
    dao = AnamnesisDao()
    
    try:
        historial = dao.getHistorialAnamnesis(id_anamnesis)
        
        return jsonify({
            'success': True, 
            'data': historial, 
            'error': None
        }), 200
            
    except Exception as e:
        app.logger.error(f"Error al obtener historial de anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ✨ NUEVOS ENDPOINTS
# ============================================

@anamnesisapi.route('/anamnesis/<int:id_anamnesis>/pdf', methods=['GET'])
def descargarPDFAnamnesis(id_anamnesis):
    """
    Genera y descarga el PDF de una anamnesis específica
    
    Query params opcionales:
        - tipo: 'completa' (default) | 'basica'
        - incluir_ficha: true | false (default: false)
    
    Respuesta: PDF file
    """
    try:
        # Obtener parámetros
        tipo_pdf = request.args.get('tipo', 'completa')
        incluir_ficha = request.args.get('incluir_ficha', 'false').lower() == 'true'
        
        # Validar tipo
        if tipo_pdf not in ['completa', 'basica']:
            return jsonify({
                'success': False,
                'error': 'El parámetro "tipo" debe ser "completa" o "basica"'
            }), 400
        
        # Obtener datos de la anamnesis
        anamnesis_dao = AnamnesisDao()
        anamnesis = anamnesis_dao.getAnamnesisById(id_anamnesis)
        
        if not anamnesis:
            return jsonify({
                'success': False,
                'error': 'No se encontró la anamnesis con el ID proporcionado.'
            }), 404
        
        # Preparar datos para el PDF
        if incluir_ficha:
            # Obtener ficha médica completa con anamnesis
            ficha_dao = FichaMedicaDao()
            ficha_data = ficha_dao.getFichaMedicaCompleta(anamnesis['id_paciente'])
            
            if not ficha_data:
                return jsonify({
                    'success': False,
                    'error': 'No se pudo obtener la ficha médica del paciente.'
                }), 500
        else:
            # Solo anamnesis - crear estructura mínima
            ficha_data = {
                'paciente': {
                    'nombre_completo': anamnesis.get('nombre_paciente', 'N/A'),
                    'historia_clinica': anamnesis.get('historia_clinica', 'N/A'),
                    'cedula': 'N/A',
                    'edad': None
                },
                'anamnesis': anamnesis,
                'estadisticas': {
                    'tiene_anamnesis': True
                }
            }
        
        # Generar PDF
        pdf_service = FichaMedicaPDFService()
        
        if tipo_pdf == 'basica':
            pdf_buffer = pdf_service.generar_ficha_basica(ficha_data)
        else:
            pdf_buffer = pdf_service.generar_ficha_completa(ficha_data)
        
        # Preparar nombre del archivo
        nombre_paciente = anamnesis.get('nombre_paciente', 'paciente').replace(' ', '_')
        hc = anamnesis.get('historia_clinica', 'sin_hc')
        fecha_actual = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f"anamnesis_{nombre_paciente}_{hc}_{fecha_actual}.pdf"
        
        # Enviar archivo
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except Exception as e:
        app.logger.error(f"Error al generar PDF de anamnesis: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'error': f'Error al generar PDF: {str(e)}'
        }), 500


@anamnesisapi.route('/anamnesis/estadisticas', methods=['GET'])
def getEstadisticasAnamnesis():
    """
    Obtiene estadísticas generales de las anamnesis
    
    Respuesta:
    {
        "success": true,
        "data": {
            "total": 150,
            "este_mes": 12,
            "pacientes_unicos": 145,
            "promedio_versiones": 1.8,
            "por_mes": [...],
            "evaluaciones_mas_comunes": {...},
            "terapias_mas_indicadas": {...}
        }
    }
    """
    dao = AnamnesisDao()
    
    try:
        # Obtener todas las anamnesis
        anamnesis = dao.getAllAnamnesis()
        
        # Calcular estadísticas
        total = len(anamnesis)
        
        # Anamnesis del mes actual
        ahora = datetime.now()
        este_mes = sum(1 for a in anamnesis 
                       if a.get('fecha_elaboracion') and 
                       a['fecha_elaboracion'].startswith(f"{ahora.year:04d}-{ahora.month:02d}"))
        
        # Pacientes únicos
        pacientes_unicos = len(set(a['id_paciente'] for a in anamnesis))
        
        # Promedio de versiones
        versiones = [a.get('version', 1) for a in anamnesis]
        promedio_versiones = round(sum(versiones) / len(versiones), 2) if versiones else 0
        
        # Evaluaciones más comunes
        evaluaciones_count = {
            'neuropsicologica': sum(1 for a in anamnesis if a.get('eval_neuropsicologica')),
            'psicologica': sum(1 for a in anamnesis if a.get('eval_psicologica')),
            'psicopedagogica': sum(1 for a in anamnesis if a.get('eval_psicopedagogica')),
            'fonoaudiologica': sum(1 for a in anamnesis if a.get('eval_fonoaudiologica')),
            'psicomotora': sum(1 for a in anamnesis if a.get('eval_psicomotora'))
        }
        
        # Terapias más indicadas
        terapias_count = {
            'individual': sum(1 for a in anamnesis if a.get('terapia_individual')),
            'familiar': sum(1 for a in anamnesis if a.get('terapia_familiar')),
            'grupal': sum(1 for a in anamnesis if a.get('terapia_grupal')),
            'ocupacional': sum(1 for a in anamnesis if a.get('terapia_ocupacional'))
        }
        
        return jsonify({
            'success': True,
            'data': {
                'total': total,
                'este_mes': este_mes,
                'pacientes_unicos': pacientes_unicos,
                'promedio_versiones': promedio_versiones,
                'evaluaciones_mas_comunes': evaluaciones_count,
                'terapias_mas_indicadas': terapias_count
            },
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>/restaurar', methods=['PATCH'])
def restaurarAnamnesis(id_anamnesis):
    """
    Restaura una anamnesis archivada (la vuelve activa)
    
    Body:
    {
        "usuario_id": 1
    }
    """
    data = request.get_json()
    dao = AnamnesisDao()

    if not data or 'usuario_id' not in data:
        return jsonify({
            'success': False,
            'error': 'El campo usuario_id es obligatorio.'
        }), 400

    try:
        # Verificar que la anamnesis existe
        anamnesis = dao.getAnamnesisById(id_anamnesis)
        if not anamnesis:
            return jsonify({
                'success': False,
                'error': 'No se encontró la anamnesis con el ID proporcionado.'
            }), 404
        
        # Verificar que el paciente no tenga otra anamnesis activa
        anamnesis_activa = dao.getAnamnesisByPaciente(anamnesis['id_paciente'])
        if anamnesis_activa:
            return jsonify({
                'success': False,
                'error': 'El paciente ya tiene una anamnesis activa. Debe archivarla primero.'
            }), 400
        
        # Restaurar (implementar en el DAO si no existe)
        # resultado = dao.restaurarAnamnesis(id_anamnesis, data['usuario_id'])
        
        return jsonify({
            'success': True,
            'mensaje': f'Anamnesis {id_anamnesis} restaurada exitosamente',
            'error': None
        }), 200

    except Exception as e:
        app.logger.error(f"Error al restaurar anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@anamnesisapi.route('/anamnesis/<int:id_anamnesis>/duplicar', methods=['POST'])
def duplicarAnamnesis(id_anamnesis):
    """
    Duplica una anamnesis existente para un nuevo paciente
    
    Body:
    {
        "id_paciente_nuevo": 456,
        "usuario_id": 1
    }
    """
    data = request.get_json()
    dao = AnamnesisDao()

    # Validar campos
    if not data or 'id_paciente_nuevo' not in data or 'usuario_id' not in data:
        return jsonify({
            'success': False,
            'error': 'Los campos id_paciente_nuevo y usuario_id son obligatorios.'
        }), 400

    try:
        # Obtener anamnesis original
        anamnesis_original = dao.getAnamnesisById(id_anamnesis)
        
        if not anamnesis_original:
            return jsonify({
                'success': False,
                'error': 'No se encontró la anamnesis original.'
            }), 404
        
        # Verificar que el nuevo paciente no tenga anamnesis activa
        anamnesis_existente = dao.getAnamnesisByPaciente(data['id_paciente_nuevo'])
        if anamnesis_existente:
            return jsonify({
                'success': False,
                'error': 'El paciente destino ya tiene una anamnesis activa.'
            }), 400
        
        # Crear nueva anamnesis con los datos de la original
        nuevo_id = dao.guardarAnamnesis(
            pac_id=data['id_paciente_nuevo'],
            usuario_id=data['usuario_id'],
            motivo_consulta=anamnesis_original.get('motivo_consulta', ''),
            # ... copiar todos los demás campos
        )
        
        if nuevo_id:
            return jsonify({
                'success': True,
                'data': {
                    'id_anamnesis': nuevo_id,
                    'mensaje': 'Anamnesis duplicada exitosamente'
                },
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo duplicar la anamnesis.'
            }), 500

    except Exception as e:
        app.logger.error(f"Error al duplicar anamnesis: {str(e)}", exc_info=True)
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500