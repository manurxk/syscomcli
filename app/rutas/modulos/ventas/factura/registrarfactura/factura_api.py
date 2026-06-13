from flask import Blueprint, request, jsonify, current_app as app, send_file
from app.dao.modulos.ventas.factura.FacturaDao import FacturaDao
from app.dao.referenciales.ventas.empresa.EmpresaDao import EmpresaDao
from app.dao.referenciales.ventas.timbrado.TimbradoDao import TimbradoDao
from app.services.factura_pdf_service import FacturaPDFService
from app.services.sifen_xml_service import SifenXMLService
from app.services.sifen_firma_service import SifenFirmaService, SifenFirmaConfig
from app.services.sifen_client import SifenClient, SifenClientConfig
from datetime import datetime

facturaapi = Blueprint('facturaapi', __name__)


def _obtenerDatosEmpresaParaSIFEN(id_empresa=None):
    """
    Obtiene los datos de empresa necesarios para generar PDF y XML SIFEN.
    Si no se proporciona id_empresa, obtiene la empresa principal.
    """
    empresa_dao = EmpresaDao()
    
    if id_empresa:
        empresa = empresa_dao.getEmpresaById(id_empresa)
    else:
        empresa_principal = empresa_dao.getEmpresaPrincipal()
        if empresa_principal:
            empresa = empresa_dao.getEmpresaById(empresa_principal['id'])
        else:
            empresa = None
    
    if not empresa:
        # Fallback a configuración si no hay empresa en BD
        return {
            'nombre_empresa': app.config.get('NOMBRE_EMPRESA', 'Nombre de la Empresa'),
            'razon_social': app.config.get('NOMBRE_EMPRESA', 'Nombre de la Empresa'),
            'ruc': app.config.get('RUC_EMISOR', '0000000-0'),
            'direccion': app.config.get('DIRECCION_EMISOR', 'Dirección no especificada'),
            'ciudad': app.config.get('CIUDAD_EMISOR', 'Ciudad no especificada'),
            'telefono': app.config.get('TELEFONO_EMISOR', ''),
            'email': app.config.get('EMAIL_EMISOR', ''),
            'website': app.config.get('WEBSITE_EMISOR', ''),
            'actividad_economica': app.config.get('ACTIVIDAD_ECONOMICA', '')
        }
    
    # Construir RUC completo
    ruc_completo = empresa.get('ruc_nit', '')
    if empresa.get('digito_verificador'):
        ruc_completo = f"{ruc_completo}-{empresa.get('digito_verificador')}"
    
    return {
        'nombre_empresa': empresa.get('razon_social', empresa.get('nombre_comercial', '')),
        'razon_social': empresa.get('razon_social', ''),
        'ruc': ruc_completo,
        'direccion': empresa.get('direccion', ''),
        'ciudad': empresa.get('ciudad', ''),
        'departamento': empresa.get('departamento', ''),
        'telefono': empresa.get('telefono', ''),
        'email': empresa.get('email', ''),
        'website': empresa.get('sitio_web', ''),
        'actividad_economica': empresa.get('actividad_economica_principal', ''),
        'logo_path': empresa.get('logo_path', '')  # Para PDF automático
    }

@facturaapi.route('/facturas', methods=['GET'])
def getAllFacturas():
    """Obtiene todas las facturas"""
    dao = FacturaDao()
    
    try:
        facturas = dao.getFacturas()
        return jsonify({'success': True, 'data': facturas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener todas las facturas: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>', methods=['GET'])
def getFactura(id_factura):
    """Obtiene una factura específica por su ID con su detalle"""
    dao = FacturaDao()
    
    try:
        factura = dao.getFacturaById(id_factura)
        
        if factura:
            # Obtener detalle
            detalle = dao.getFacturaDetalle(id_factura)
            factura['detalle'] = detalle
            
            return jsonify({'success': True, 'data': factura, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
    except Exception as e:
        app.logger.error(f"Error al obtener la factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas', methods=['POST'])
def addFactura():
    """Crea una nueva factura"""
    data = request.get_json()
    dao = FacturaDao()
    
    campos_requeridos = ['id_paciente', 'id_tipo_comprobante', 'id_condicion_venta', 'fecha_factura']
    
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        factura_id = dao.guardarFactura(
            id_paciente=data['id_paciente'],
            id_tipo_comprobante=data['id_tipo_comprobante'],
            id_condicion_venta=data['id_condicion_venta'],
            fecha_factura=data['fecha_factura'],
            id_moneda=data.get('id_moneda', 1),
            id_pedido=data.get('id_pedido'),
            fecha_vencimiento=data.get('fecha_vencimiento'),
            factura_subtotal=data.get('factura_subtotal', 0),
            factura_descuento=data.get('factura_descuento', 0),
            factura_impuestos=data.get('factura_impuestos', 0),
            factura_total=data.get('factura_total', 0),
            codigo_sifen=data.get('codigo_sifen'),
            numero_timbrado=data.get('numero_timbrado'),
            observaciones=data.get('observaciones'),
            est_factura=data.get('est_factura', 1),
            usuario_creacion=app.config.get('USUARIO_ACTUAL', 'ADMIN'),
            id_empresa=data.get('id_empresa'),
            id_timbrado=data.get('id_timbrado'),
            id_punto_expedicion=data.get('id_punto_expedicion')
        )
        
        if factura_id:
            return jsonify({
                'success': True,
                'data': {'id_factura': factura_id, 'mensaje': 'Factura creada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo crear la factura.'
            }), 500
            
    except Exception as e:
        app.logger.error(f"Error al crear factura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>/detalle', methods=['POST'])
def addFacturaDetalle(id_factura):
    """Agrega un item al detalle de una factura"""
    data = request.get_json()
    dao = FacturaDao()
    
    campos_requeridos = ['item_descripcion', 'item_precio_unitario']
    
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        detalle_id = dao.guardarFacturaDetalle(
            id_factura=id_factura,
            item_descripcion=data['item_descripcion'],
            item_precio_unitario=int(data['item_precio_unitario']),
            item_cantidad=data.get('item_cantidad', 1),
            item_descuento=int(data.get('item_descuento', 0)),
            id_tipo_item=data.get('id_tipo_item'),
            id_consulta=data.get('id_consulta'),
            id_tipo_impuesto=data.get('id_tipo_impuesto'),
            impuesto_porcentaje=float(data.get('impuesto_porcentaje', 0)),
            observaciones=data.get('observaciones')
        )
        
        if detalle_id:
            return jsonify({
                'success': True,
                'data': {'id_factura_detalle': detalle_id, 'mensaje': 'Item agregado exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo agregar el item a la factura.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al agregar detalle de factura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>/detalle/<int:id_detalle>', methods=['PUT'])
def updateFacturaDetalle(id_factura, id_detalle):
    """Actualiza un item del detalle de factura"""
    data = request.get_json()
    dao = FacturaDao()
    
    try:
        resultado = dao.updateFacturaDetalle(
            id_factura_detalle=id_detalle,
            item_descripcion=data.get('item_descripcion'),
            item_cantidad=data.get('item_cantidad'),
            item_precio_unitario=int(data['item_precio_unitario']) if data.get('item_precio_unitario') else None,
            item_descuento=int(data.get('item_descuento', 0)) if data.get('item_descuento') is not None else None,
            id_tipo_item=data.get('id_tipo_item'),
            id_consulta=data.get('id_consulta'),
            id_tipo_impuesto=data.get('id_tipo_impuesto'),
            impuesto_porcentaje=float(data.get('impuesto_porcentaje', 0)) if data.get('impuesto_porcentaje') is not None else None
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Item actualizado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar el item.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar detalle de factura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>/detalle/<int:id_detalle>', methods=['DELETE'])
def deleteFacturaDetalle(id_factura, id_detalle):
    """Elimina un item del detalle de factura"""
    dao = FacturaDao()
    
    try:
        resultado = dao.deleteFacturaDetalle(id_detalle)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Item eliminado exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar el item.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al eliminar detalle de factura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>', methods=['PUT'])
def updateFactura(id_factura):
    """Actualiza una factura existente"""
    data = request.get_json()
    dao = FacturaDao()
    
    try:
        resultado = dao.updateFactura(
            id_factura=id_factura,
            fecha_factura=data.get('fecha_factura'),
            fecha_vencimiento=data.get('fecha_vencimiento'),
            factura_descuento=int(data.get('factura_descuento', 0)) if data.get('factura_descuento') is not None else None,
            codigo_sifen=data.get('codigo_sifen'),
            numero_timbrado=data.get('numero_timbrado'),
            observaciones=data.get('observaciones'),
            est_factura=data.get('est_factura'),
            usuario_modificacion=app.config.get('USUARIO_ACTUAL', 'ADMIN')
        )
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Factura actualizada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo actualizar la factura.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al actualizar factura: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>', methods=['DELETE'])
def deleteFactura(id_factura):
    """Elimina una factura y su detalle"""
    dao = FacturaDao()
    
    try:
        resultado = dao.deleteFactura(id_factura)
        
        if resultado:
            return jsonify({
                'success': True,
                'mensaje': 'Factura eliminada exitosamente',
                'error': None
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo eliminar la factura.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error al eliminar factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS DE FILTRADO
# ============================================

@facturaapi.route('/facturas/paciente/<int:id_paciente>', methods=['GET'])
def getFacturasPorPaciente(id_paciente):
    """Obtiene todas las facturas de un paciente"""
    dao = FacturaDao()
    
    try:
        facturas = dao.getFacturasPorPaciente(id_paciente)
        return jsonify({'success': True, 'data': facturas, 'error': None}), 200
    except Exception as e:
        app.logger.error(f"Error al obtener facturas del paciente: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


# ============================================
# ENDPOINTS PARA PDF Y PREVIEW
# ============================================

@facturaapi.route('/facturas/preview', methods=['POST'])
def previewFactura():
    """Genera un PDF de preview de la factura antes de guardarla"""
    data = request.get_json()
    pdf_service = FacturaPDFService()
    
    try:
        # Validar datos mínimos
        if not data.get('codigo_sifen'):
            return jsonify({
                'success': False,
                'error': 'El código SIFEN es requerido para generar el preview.'
            }), 400
        
        # Obtener datos de empresa desde BD
        id_empresa = data.get('id_empresa')
        config_empresa = _obtenerDatosEmpresaParaSIFEN(id_empresa)
        
        # Generar PDF de preview
        # Asegurar que items sea una lista válida
        items = data.get('items', [])
        # Validación más robusta: verificar si es iterable y convertir a lista
        try:
            if items is None:
                items = []
            elif not isinstance(items, (list, tuple)):
                # Intentar convertir a lista si es iterable
                try:
                    iter(items)  # Verificar si es iterable
                    items = list(items)
                except (TypeError, ValueError):
                    items = []
        except (TypeError, AttributeError):
            items = []
        
        pdf_buffer = pdf_service.generar_preview_factura(
            datos_formulario=data,
            items=items,
            config_empresa=config_empresa
        )
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f"preview_factura_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        import traceback
        app.logger.error(f"Error al generar preview de factura: {str(e)}")
        app.logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error al generar el preview: {str(e)}'
        }), 500


@facturaapi.route('/facturas/<int:id_factura>/pdf', methods=['GET'])
def generarPDFFactura(id_factura):
    """Genera un PDF de la factura guardada con código QR"""
    dao = FacturaDao()
    pdf_service = FacturaPDFService()
    
    try:
        # Obtener factura completa
        factura = dao.getFacturaById(id_factura)
        
        if not factura:
            return jsonify({
                'success': False,
                'error': 'No se encontró la factura.'
            }), 404
        
        # Obtener detalle
        detalle = dao.getFacturaDetalle(id_factura)
        
        # Preparar datos para el PDF
        factura_data = {
            'factura_numero': factura.get('factura_numero', ''),
            'fecha_factura': str(factura.get('fecha_factura', '')),
            'codigo_sifen': factura.get('codigo_sifen', ''),
            'numero_timbrado': factura.get('numero_timbrado', ''),
            'fecha_inicio_vigencia': factura.get('fecha_inicio_vigencia', '01/01/2024'),
            'fecha_fin_vigencia': factura.get('fecha_fin_vigencia', '31/12/2024'),
            'paciente_nombre': factura.get('paciente_nombre', ''),
            'paciente_cedula': factura.get('paciente_cedula', ''),
            'paciente_telefono': factura.get('paciente_telefono', ''),
            'paciente_direccion': factura.get('paciente_direccion', ''),
            'paciente_email': factura.get('paciente_email', ''),
            'condicion_venta': factura.get('condicion_venta', 'Contado'),
            'moneda': factura.get('moneda', 'PYG'),
            'tipo_operacion': 'Venta de Mercadería',
            'factura_subtotal': factura.get('factura_subtotal', 0),
            'factura_impuestos': factura.get('factura_impuestos', 0),
            'factura_descuento': factura.get('factura_descuento', 0),
            'factura_total': factura.get('factura_total', 0),
            'factura_total_letras': factura.get('factura_total_letras', ''),
            'observaciones': factura.get('observaciones', ''),
            'ruc_emisor': app.config.get('RUC_EMISOR', '0000000-0')
        }
        
        # Obtener datos de empresa desde BD
        id_empresa = factura.get('id_empresa')
        config_empresa = _obtenerDatosEmpresaParaSIFEN(id_empresa)
        
        # Generar PDF
        pdf_buffer = pdf_service.generar_factura_pdf(factura_data, detalle, config_empresa)
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"factura_{factura_data['factura_numero']}.pdf"
        )
        
    except Exception as e:
        app.logger.error(f"Error al generar PDF de factura: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error al generar el PDF: {str(e)}'
        }), 500


@facturaapi.route('/facturas/<int:id_factura>/kude', methods=['GET'])
def descargarKude(id_factura):
    """Descarga el Representante Gráfico KUDE de la Factura, validando y guardando según política SIFEN."""
    dao = FacturaDao()
    from app.services.sifen_kude_service import SifenKudeService
    import os
    
    try:
        factura = dao.getFacturaById(id_factura)
        if not factura:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
            
        cdc = factura.get('codigo_sifen')
        
        # Validar que sea un DE SIFEN y tenga CDC
        if not cdc:
            # Si no tiene CDC, es una factura tradicional o no autorizada todavía
            return jsonify({
                'success': False, 
                'error': 'Factura no posee CDC (No es válida o no ha sido sincronizada a SIFEN).'
            }), 400
            
        # Si ya existe path en base de datos, lo retornamos (cache)
        kude_path = factura.get('factura_kude_path')
        if kude_path:
            abs_path = os.path.join(app.root_path, 'static', *kude_path.split('/'))
            if os.path.exists(abs_path):
                return send_file(abs_path, as_attachment=True)

        # Si no existe, lo generamos
        detalle = dao.getFacturaDetalle(id_factura)
        
        # Preparar data estructurada como espera _generar_factura_pdf
        factura_data = {
            'factura_numero': factura.get('factura_numero', ''),
            'fecha_factura': str(factura.get('fecha_factura', '')),
            'codigo_sifen': cdc,
            'numero_timbrado': factura.get('numero_timbrado', ''),
            'fecha_inicio_vigencia': factura.get('fecha_inicio_vigencia', '01/01/2024'),
            'fecha_fin_vigencia': factura.get('fecha_fin_vigencia', '31/12/2024'),
            'paciente_nombre': factura.get('paciente_nombre', ''),
            'paciente_cedula': factura.get('paciente_cedula', ''),
            'paciente_telefono': factura.get('paciente_telefono', ''),
            'paciente_direccion': factura.get('paciente_direccion', ''),
            'condicion_venta': factura.get('condicion_venta', 'Contado'),
            'moneda': factura.get('moneda', 'PYG'),
            'tipo_operacion': 'Venta de Mercadería',
            'factura_total': factura.get('factura_total', 0),
            'factura_total_letras': factura.get('factura_total_letras', ''),
            'ruc_emisor': app.config.get('RUC_EMISOR', '0000000-0')
        }
        
        config_empresa = _obtenerDatosEmpresaParaSIFEN(factura.get('id_empresa'))
        
        # Generamos, guardamos politícamente y actualizamos bd
        db_path = SifenKudeService.generar_y_guardar_kude(id_factura, factura_data, detalle, config_empresa)
        
        abs_path = os.path.join(app.root_path, 'static', *db_path.split('/'))
        return send_file(abs_path, as_attachment=True)
            
    except Exception as e:
        app.logger.error(f"Error en descarga de KUDE: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Ocurrió un error al generar el PDF KUDE: {str(e)}'}), 500
@facturaapi.route('/facturas/<int:id_factura>/sifen-simulado', methods=['GET'])
def simularEnvioSifen(id_factura):
    """
    Genera el XML SIFEN, lo "firma" y simula el envío al SIFEN.
    NO realiza ninguna llamada real a la SET.
    
    Devuelve:
      - CDC simulado
      - XML firmado (para inspección)
    """
    dao = FacturaDao()
    pdf_service = FacturaPDFService()
    xml_service = SifenXMLService()

    try:
        factura = dao.getFacturaById(id_factura)
        if not factura:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404

        detalle = dao.getFacturaDetalle(id_factura)

        factura_data = {
            'factura_numero': factura.get('factura_numero', ''),
            'fecha_factura': str(factura.get('fecha_factura', '')),
            'codigo_sifen': factura.get('codigo_sifen', ''),  # podría estar vacío en simulación
            'numero_timbrado': factura.get('numero_timbrado', ''),
            'fecha_inicio_vigencia': factura.get('fecha_inicio_vigencia', '01/01/2024'),
            'fecha_fin_vigencia': factura.get('fecha_fin_vigencia', '31/12/2024'),
            'paciente_nombre': factura.get('paciente_nombre', ''),
            'paciente_cedula': factura.get('paciente_cedula', ''),
            'paciente_telefono': factura.get('paciente_telefono', ''),
            'paciente_direccion': factura.get('paciente_direccion', ''),
            'paciente_email': factura.get('paciente_email', ''),
            'condicion_venta': factura.get('condicion_venta', 'Contado'),
            'moneda': factura.get('moneda', 'PYG'),
            'tipo_operacion': 'Venta de Mercadería',
            'factura_subtotal': factura.get('factura_subtotal', 0),
            'factura_impuestos': factura.get('factura_impuestos', 0),
            'factura_descuento': factura.get('factura_descuento', 0),
            'factura_total': factura.get('factura_total', 0),
            'observaciones': factura.get('observaciones', ''),
            'ruc_emisor': factura.get('empresa_ruc', '0000000-0')
        }

        # Obtener datos de empresa desde BD
        id_empresa = factura.get('id_empresa')
        config_empresa = _obtenerDatosEmpresaParaSIFEN(id_empresa)

        # 1) Generar XML simplificado
        xml_bytes = xml_service.generar_xml_factura(factura_data, detalle, config_empresa)

        # 2) "Firmar" XML en modo simulado
        firma_cfg = SifenFirmaConfig(modo=app.config.get('SIFEN_MODO', 'simulado'))
        firma_service = SifenFirmaService(firma_cfg)
        xml_firmado = firma_service.firmar_xml(xml_bytes)

        # 3) Simular envío a SIFEN
        client_cfg = SifenClientConfig(modo=app.config.get('SIFEN_MODO', 'simulado'))
        sifen_client = SifenClient(client_cfg)
        resultado = sifen_client.enviar_factura(xml_firmado, factura_data)

        # 4) Generar KUDE en modo simulado usando el CDC generado
        factura_data_sim = dict(factura_data)
        factura_data_sim['codigo_sifen'] = resultado.get('cdc', factura_data.get('codigo_sifen', ''))
        pdf_buffer = pdf_service.generar_factura_pdf(factura_data_sim, detalle, config_empresa)

        # Devolvemos JSON con info y el PDF como adjunto opcional
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=False,
            download_name=f"factura_sifen_sim_{factura_data['factura_numero']}.pdf"
        )

    except Exception as e:
        app.logger.error(f"Error en simulación SIFEN: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Ocurrió un error en la simulación SIFEN: {str(e)}'
        }), 500


@facturaapi.route('/facturas/<int:id_factura>/xml', methods=['GET'])
def getFacturaXml(id_factura):
    """Genera y retorna el XML SIFEN (v150) de una factura guardada"""
    dao = FacturaDao()
    xml_service = SifenXMLService()
    
    try:
        factura = dao.getFacturaById(id_factura)
        if not factura:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
            
        detalle = dao.getFacturaDetalle(id_factura)
        
        # Obtener configuración
        from app.services.sifen_config_service import SifenConfigService, SifenConfigException
        try:
            config_emis = SifenConfigService.get_config_emision(id_empresa=factura.get('id_empresa'))
        except SifenConfigException as e:
            # Generar config dummy si falla para evitar que el endpoint caiga en facturas viejas
            from app.services.sifen_config_service import SifenEmisionConfig
            config_emis = SifenEmisionConfig(
                ruc_emisor="80000000", digito_verificador="1", razon_social="EMPRESA PREDETERMINADA",
                actividad_economica="ACTIVIDAD ECONOMICA", direccion="DIRECCION", numero_casa="0", ciudad="ASUNCION",
                telefono="000000", email="test@test.com", timbrado_numero="12345678", timbrado_fecha_inicio="2024-01-01",
                timbrado_fecha_fin="2025-01-01", establecimiento_codigo="001", punto_expedicion_codigo="001", siguiente_numero=1, id_punto_expedicion=1
            )
            
        cdc = factura.get('codigo_sifen')
        if not cdc:
            from app.utils.sifen_cdc_utils import SifenCDCUtils
            # Extraer num doc secuencial
            num_str = str(factura.get('factura_numero', '0'))
            num_sec = num_str.split('-')[-1].lstrip('0') or '0'
            fecha_str = str(factura.get('fecha_factura', ''))[:10].replace('-', '') or '20240101'
            cdc = SifenCDCUtils.generar_cdc_real(
                tipo_documento="01", ruc_emisor=config_emis.ruc_emisor, dv_ruc_emisor=config_emis.digito_verificador,
                establecimiento=config_emis.establecimiento_codigo, punto_expedicion=config_emis.punto_expedicion_codigo,
                numero_documento=num_sec, tipo_contribuyente="2" if config_emis.ruc_emisor.startswith("8") else "1",
                fecha_emision_yyyymmdd=fecha_str
            )
            
        xml_bytes = xml_service.generar_xml_v150(factura, detalle, config_emis, cdc)
        
        from flask import Response
        return Response(xml_bytes, mimetype='application/xml')
        
    except Exception as e:
        app.logger.error(f"Error al generar XML de factura: {str(e)}")
        import traceback
        app.logger.error(traceback.format_exc())
        return jsonify({'success': False, 'error': f'Ocurrió un error: {str(e)}'}), 500


@facturaapi.route('/facturas/<int:id_factura>/json', methods=['GET'])
def getFacturaJson(id_factura):
    """Retorna la representación JSON de la factura"""
    dao = FacturaDao()
    try:
        factura = dao.getFacturaById(id_factura)
        if not factura:
            return jsonify({'success': False, 'error': 'No se encontró la factura.'}), 404
        detalle = dao.getFacturaDetalle(id_factura)
        factura['detalle'] = detalle
        return jsonify(factura), 200
    except Exception as e:
        app.logger.error(f"Error al obtener JSON de factura: {str(e)}")
        return jsonify({'success': False, 'error': 'Ocurrió un error interno.'}), 500


@facturaapi.route('/facturas/<int:id_factura>/reenviar', methods=['POST'])
def reenviarFactura(id_factura):
    """
    P5 — Reenvío de factura electrónica rechazada.
    Permite reenviar una factura en estado RECHAZADO a SIFEN.
    """
    from app.services.sifen_kude_service import SifenKudeService
    try:
        resultado = SifenKudeService.reenviar_factura(id_factura)
        if resultado.get('success'):
            return jsonify({'success': True, 'data': resultado, 'error': None}), 200
        else:
            return jsonify({'success': False, 'error': resultado.get('mensaje', 'No se pudo reenviar.')}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        app.logger.error(f"Error al reenviar factura {id_factura}: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500


