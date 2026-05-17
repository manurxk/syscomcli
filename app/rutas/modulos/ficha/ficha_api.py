# app/routes/ficha_medica_routes.py

from flask import Blueprint, request, jsonify, send_file, current_app as app
from app.dao.modulos.ficha.FichaDao import FichaMedicaDao
from app.services.pdf_service import FichaMedicaPDFService 
from io import BytesIO
from datetime import datetime


fichamedicaapi = Blueprint('fichamedicaapi', __name__)


def limpiar_nombre_archivo(texto):
    """
    Limpia un texto para que sea válido como nombre de archivo
    Elimina espacios, caracteres especiales y normaliza acentos
    """
    if not texto:
        return ''
    # Reemplazar espacios y caracteres problemáticos
    texto = texto.replace(' ', '_')
    texto = texto.replace('/', '_').replace('\\', '_')
    texto = texto.replace(':', '_').replace('*', '_').replace('?', '_')
    texto = texto.replace('"', '_').replace('<', '_').replace('>', '_')
    texto = texto.replace('|', '_')
    # Remover acentos comunes (básico)
    texto = texto.replace('á', 'a').replace('é', 'e').replace('í', 'i')
    texto = texto.replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
    texto = texto.replace('Á', 'A').replace('É', 'E').replace('Í', 'I')
    texto = texto.replace('Ó', 'O').replace('Ú', 'U').replace('Ñ', 'N')
    return texto


# ==========================================
# RUTA PRINCIPAL - FICHA MÉDICA COMPLETA
# ==========================================

@fichamedicaapi.route('/ficha-medica/<int:id_paciente>', methods=['GET'])
def getFichaMedicaCompleta(id_paciente):
    """
    Obtiene la ficha médica completa de un paciente
    Incluye: paciente, anamnesis, consultas, diagnósticos, tratamientos, procedimientos, citas, timeline
    """
    fichadao = FichaMedicaDao()
    
    try:
        ficha_completa = fichadao.getFichaMedicaCompleta(id_paciente)
        
        if ficha_completa and ficha_completa.get('paciente'):
            return jsonify({
                'success': True,
                'data': ficha_completa,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado.'
            }), 404
            
    except Exception as e:
        app.logger.error(f"Error al obtener ficha médica completa: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno. Consulte con el administrador.'
        }), 500


# ==========================================
# RUTAS INDIVIDUALES POR SECCIÓN
# ==========================================

@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/paciente', methods=['GET'])
def getDatosPaciente(id_paciente):
    """Obtiene solo los datos demográficos del paciente"""
    fichadao = FichaMedicaDao()
    
    try:
        paciente = fichadao.getDatosPaciente(id_paciente)
        
        if paciente:
            return jsonify({
                'success': True,
                'data': paciente,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente.'
            }), 404
            
    except Exception as e:
        app.logger.error(f"Error al obtener datos del paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/anamnesis', methods=['GET'])
def getAnamnesisPaciente(id_paciente):
    """Obtiene la anamnesis activa del paciente"""
    fichadao = FichaMedicaDao()
    
    try:
        anamnesis = fichadao.getAnamnesisPaciente(id_paciente)
        
        if anamnesis:
            return jsonify({
                'success': True,
                'data': anamnesis,
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se encontró anamnesis activa para este paciente.'
            }), 404
            
    except Exception as e:
        app.logger.error(f"Error al obtener anamnesis del paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/consultas', methods=['GET'])
def getConsultasRecientes(id_paciente):
    """Obtiene las consultas recientes del paciente"""
    fichadao = FichaMedicaDao()
    
    # Parámetro opcional: límite de resultados
    limite = request.args.get('limite', default=10, type=int)
    
    try:
        consultas = fichadao.getConsultasRecientes(id_paciente, limite)
        
        return jsonify({
            'success': True,
            'data': consultas,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener consultas recientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/diagnosticos', methods=['GET'])
def getDiagnosticosPaciente(id_paciente):
    """Obtiene todos los diagnósticos del paciente"""
    fichadao = FichaMedicaDao()
    
    try:
        diagnosticos = fichadao.getDiagnosticosPaciente(id_paciente)
        
        return jsonify({
            'success': True,
            'data': diagnosticos,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener diagnósticos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/tratamientos', methods=['GET'])
def getTratamientosActivos(id_paciente):
    """Obtiene los tratamientos activos del paciente"""
    fichadao = FichaMedicaDao()
    
    try:
        tratamientos = fichadao.getTratamientosActivos(id_paciente)
        
        return jsonify({
            'success': True,
            'data': tratamientos,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener tratamientos activos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/procedimientos', methods=['GET'])
def getProcedimientosRecientes(id_paciente):
    """Obtiene los procedimientos recientes del paciente"""
    fichadao = FichaMedicaDao()
    
    # Parámetro opcional: límite de resultados
    limite = request.args.get('limite', default=15, type=int)
    
    try:
        procedimientos = fichadao.getProcedimientosRecientes(id_paciente, limite)
        
        return jsonify({
            'success': True,
            'data': procedimientos,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener procedimientos recientes: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/citas', methods=['GET'])
def getProximasCitas(id_paciente):
    """Obtiene las próximas citas del paciente"""
    fichadao = FichaMedicaDao()
    
    # Parámetro opcional: límite de resultados
    limite = request.args.get('limite', default=5, type=int)
    
    try:
        citas = fichadao.getProximasCitas(id_paciente, limite)
        
        return jsonify({
            'success': True,
            'data': citas,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener próximas citas: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/timeline', methods=['GET'])
def getTimelineEventos(id_paciente):
    """Obtiene el timeline de eventos médicos del paciente"""
    fichadao = FichaMedicaDao()
    
    # Parámetro opcional: límite de resultados
    limite = request.args.get('limite', default=30, type=int)
    
    try:
        timeline = fichadao.getTimelineEventos(id_paciente, limite)
        
        return jsonify({
            'success': True,
            'data': timeline,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener timeline de eventos: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ==========================================
# RUTAS PARA EXPORTACIÓN PDF
# ==========================================

@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/pdf', methods=['GET'])
def generarPDFFichaMedica(id_paciente):
    """
    ⭐ RUTA PRINCIPAL PARA GENERAR PDF ⭐
    Genera y descarga el PDF completo de la ficha médica
    
    Query params opcionales:
        - tipo: 'completa' (default) | 'basica'
        - incluir_anamnesis: true (default) | false
    """
    fichadao = FichaMedicaDao()
    
    try:
        # Obtener parámetros
        tipo_pdf = request.args.get('tipo', 'completa')
        incluir_anamnesis = request.args.get('incluir_anamnesis', 'true').lower() == 'true'
        
        # Validar tipo
        if tipo_pdf not in ['completa', 'basica']:
            return jsonify({
                'success': False,
                'error': 'El parámetro "tipo" debe ser "completa" o "basica"'
            }), 400
        
        # Obtener datos completos de la ficha médica
        ficha_completa = fichadao.getFichaMedicaCompleta(id_paciente)
        
        # Validar que exista el paciente
        if not ficha_completa or not ficha_completa.get('paciente'):
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente con el ID proporcionado.'
            }), 404
        
        # Excluir anamnesis si no se solicita
        if not incluir_anamnesis:
            ficha_completa['anamnesis'] = None
        
        # Crear instancia del servicio PDF
        pdf_service = FichaMedicaPDFService()
        
        # Generar el PDF según el tipo
        if tipo_pdf == 'basica':
            pdf_buffer = pdf_service.generar_ficha_basica(ficha_completa)
        else:
            pdf_buffer = pdf_service.generar_ficha_completa(ficha_completa)
        
        # Preparar nombre del archivo con nombre, apellido y cédula
        paciente = ficha_completa['paciente']
        nombre = limpiar_nombre_archivo(paciente.get('nombre', '').strip()) or 'sin_nombre'
        apellido = limpiar_nombre_archivo(paciente.get('apellido', '').strip()) or 'sin_apellido'
        cedula = limpiar_nombre_archivo(paciente.get('cedula', '').strip()) or 'sin_cedula'
        
        nombre_archivo = f"Ficha_Medica_{apellido}_{nombre}_{cedula}.pdf"
        
        # Enviar el archivo PDF al cliente
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=nombre_archivo
        )
        
    except AttributeError as ae:
        app.logger.error(f"Error en servicio PDF: {str(ae)}")
        return jsonify({
            'success': False,
            'error': 'El servicio de generación de PDF no está correctamente configurado.'
        }), 500
        
    except Exception as e:
        app.logger.error(f"Error al generar PDF: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Error al generar el PDF: {str(e)}'
        }), 500


@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/pdf/preview', methods=['GET'])
def previewPDFFichaMedica(id_paciente):
    """
    Genera PDF para visualización en el navegador (sin forzar descarga)
    Útil para vista previa antes de descargar
    """
    fichadao = FichaMedicaDao()
    
    try:
        ficha_completa = fichadao.getFichaMedicaCompleta(id_paciente)
        
        if not ficha_completa or not ficha_completa.get('paciente'):
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente.'
            }), 404
        
        # Generar PDF
        pdf_service = FichaMedicaPDFService()
        pdf_buffer = pdf_service.generar_ficha_completa(ficha_completa)
        
        # Retornar el PDF para visualización inline
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f"ficha_medica_{id_paciente}.pdf"
        )
        
    except Exception as e:
        app.logger.error(f"Error al generar preview PDF: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error al generar el PDF.'
        }), 500


# ==========================================
# RUTA DE RESUMEN EJECUTIVO
# ==========================================

@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/resumen', methods=['GET'])
def getResumenEjecutivo(id_paciente):
    """
    Obtiene un resumen ejecutivo condensado de la ficha médica
    Útil para vistas rápidas o dashboards
    """
    fichadao = FichaMedicaDao()
    
    try:
        paciente = fichadao.getDatosPaciente(id_paciente)
        anamnesis = fichadao.getAnamnesisPaciente(id_paciente)
        proxima_cita = fichadao.getProximasCitas(id_paciente, limite=1)
        tratamientos_activos = fichadao.getTratamientosActivos(id_paciente)
        diagnosticos = fichadao.getDiagnosticosPaciente(id_paciente)
        
        if not paciente:
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente.'
            }), 404
        
        resumen = {
            'paciente': {
                'id': paciente['id_paciente'],
                'nombre_completo': paciente['nombre_completo'],
                'historia_clinica': paciente['historia_clinica'],
                'edad': paciente['edad'],
                'telefono': paciente['telefono']
            },
            'tiene_anamnesis': anamnesis is not None,
            'anamnesis_info': {
                'id_anamnesis': anamnesis['id_anamnesis'] if anamnesis else None,
                'fecha_elaboracion': anamnesis['fecha_elaboracion'] if anamnesis else None,
                'motivo_consulta': anamnesis['motivo_consulta'][:100] + '...' if anamnesis and anamnesis.get('motivo_consulta') and len(anamnesis['motivo_consulta']) > 100 else (anamnesis.get('motivo_consulta') if anamnesis else None)
            } if anamnesis else None,
            'proxima_cita': proxima_cita[0] if proxima_cita else None,
            'tratamientos_activos_count': len(tratamientos_activos),
            'diagnosticos_count': len(diagnosticos),
            'diagnosticos_graves': [d for d in diagnosticos if d.get('gravedad') == 'GRAVE']
        }
        
        return jsonify({
            'success': True,
            'data': resumen,
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener resumen ejecutivo: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ==========================================
# RUTA DE VALIDACIÓN
# ==========================================

@fichamedicaapi.route('/ficha-medica/validar/<int:id_paciente>', methods=['GET'])
def validarPacienteExiste(id_paciente):
    """
    Valida si existe un paciente con el ID proporcionado
    Útil antes de cargar la ficha completa
    """
    fichadao = FichaMedicaDao()
    
    try:
        paciente = fichadao.getDatosPaciente(id_paciente)
        anamnesis = fichadao.getAnamnesisPaciente(id_paciente)
        
        if paciente:
            return jsonify({
                'success': True,
                'data': {
                    'existe': True,
                    'id_paciente': paciente['id_paciente'],
                    'nombre_completo': paciente['nombre_completo'],
                    'historia_clinica': paciente['historia_clinica'],
                    'tiene_anamnesis': anamnesis is not None
                },
                'error': None
            }), 200
        else:
            return jsonify({
                'success': True,
                'data': {'existe': False},
                'error': None
            }), 200
            
    except Exception as e:
        app.logger.error(f"Error al validar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ==========================================
# ESTADÍSTICAS DE FICHA MÉDICA
# ==========================================

@fichamedicaapi.route('/ficha-medica/estadisticas', methods=['GET'])
def getEstadisticasGenerales():
    """
    Obtiene estadísticas generales del sistema de fichas médicas
    """
    fichadao = FichaMedicaDao()
    
    try:
        # Aquí podrías agregar lógica para obtener estadísticas generales
        # Por ahora retornamos un placeholder
        return jsonify({
            'success': True,
            'data': {
                'mensaje': 'Endpoint de estadísticas generales - Pendiente de implementación'
            },
            'error': None
        }), 200
        
    except Exception as e:
        app.logger.error(f"Error al obtener estadísticas generales: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ==========================================
# BÚSQUEDA DE PACIENTES
# ==========================================

@fichamedicaapi.route('/ficha-medica/buscar', methods=['GET'])
def buscarPaciente():
    """
    Busca pacientes por diferentes criterios para acceder a su ficha médica
    
    Query params:
        - historia_clinica: Número de historia clínica
        - cedula: Número de cédula
        - nombre: Nombre o apellido del paciente
    """
    fichadao = FichaMedicaDao()
    
    historia_clinica = request.args.get('historia_clinica')
    cedula = request.args.get('cedula')
    nombre = request.args.get('nombre')
    
    if not any([historia_clinica, cedula, nombre]):
        return jsonify({
            'success': False,
            'error': 'Debe proporcionar al menos un criterio de búsqueda.'
        }), 400
    
    try:
        # TODO: Implementar búsqueda cuando esté disponible en el DAO
        return jsonify({
            'success': False,
            'error': 'Método de búsqueda no implementado aún. Use el ID del paciente.'
        }), 501
        
    except Exception as e:
        app.logger.error(f"Error al buscar paciente: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500


# ==========================================
# EXPORTACIÓN MULTIPROPÓSITO
# ==========================================

@fichamedicaapi.route('/ficha-medica/<int:id_paciente>/exportar', methods=['GET'])
def exportarFichaMedica(id_paciente):
    """
    Ruta genérica de exportación con múltiples formatos
    
    Query params:
        - formato: json (default), pdf
        - tipo: completa (default), basica
        - incluir_anamnesis: true (default), false
    
    Ejemplos:
        /api/v1/ficha-medica/22/exportar?formato=pdf
        /api/v1/ficha-medica/22/exportar?formato=pdf&tipo=basica
        /api/v1/ficha-medica/22/exportar?formato=json
        /api/v1/ficha-medica/22/exportar?formato=pdf&incluir_anamnesis=false
    """
    fichadao = FichaMedicaDao()
    
    formato = request.args.get('formato', default='json', type=str).lower()
    tipo = request.args.get('tipo', default='completa', type=str).lower()
    incluir_anamnesis = request.args.get('incluir_anamnesis', 'true').lower() == 'true'
    
    try:
        ficha_completa = fichadao.getFichaMedicaCompleta(id_paciente)
        
        if not ficha_completa or not ficha_completa.get('paciente'):
            return jsonify({
                'success': False,
                'error': 'No se encontró el paciente.'
            }), 404
        
        # Excluir anamnesis si no se solicita
        if not incluir_anamnesis:
            ficha_completa['anamnesis'] = None
        
        # Formato JSON
        if formato == 'json':
            return jsonify({
                'success': True,
                'data': ficha_completa,
                'error': None
            }), 200
        
        # Formato PDF
        elif formato == 'pdf':
            try:
                pdf_service = FichaMedicaPDFService()
                
                # Generar PDF según el tipo
                if tipo == 'basica':
                    pdf_buffer = pdf_service.generar_ficha_basica(ficha_completa)
                else:
                    pdf_buffer = pdf_service.generar_ficha_completa(ficha_completa)
                
                # Preparar nombre del archivo con nombre, apellido y cédula
                paciente = ficha_completa['paciente']
                nombre = limpiar_nombre_archivo(paciente.get('nombre', '').strip()) or 'sin_nombre'
                apellido = limpiar_nombre_archivo(paciente.get('apellido', '').strip()) or 'sin_apellido'
                cedula = limpiar_nombre_archivo(paciente.get('cedula', '').strip()) or 'sin_cedula'
                
                nombre_archivo = f"Ficha_{tipo.capitalize()}_{apellido}_{nombre}_{cedula}.pdf"
                
                # Retornar el archivo PDF
                return send_file(
                    pdf_buffer,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name=nombre_archivo
                )
                
            except Exception as pe:
                app.logger.error(f"Error al generar PDF: {str(pe)}")
                return jsonify({
                    'success': False,
                    'error': 'Error al generar el archivo PDF.'
                }), 500
        
        else:
            return jsonify({
                'success': False,
                'error': 'Formato no válido. Use: json, pdf'
            }), 400
        
    except Exception as e:
        app.logger.error(f"Error al exportar ficha médica: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500