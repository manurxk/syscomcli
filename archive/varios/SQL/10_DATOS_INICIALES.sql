-- ============================================================================
-- DATOS INICIALES DEL SISTEMA
-- ============================================================================
-- Este script inserta datos iniciales necesarios para el funcionamiento del sistema
-- Ejecutar después de: 09_TRIGGERS_AUDITORIA.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Estos son datos básicos necesarios para el funcionamiento inicial
-- 2. Puedes modificar estos datos según tus necesidades
-- 3. Los usuarios se crean con contraseña por defecto (cambiar en producción)
-- ============================================================================

-- ============================================================================
-- DATOS INICIALES YA INSERTADOS EN FASES ANTERIORES
-- ============================================================================
-- Los siguientes datos ya fueron insertados en las fases anteriores:
-- - Géneros (FASE 1)
-- - Estados civiles (FASE 1)
-- - Ciudades (FASE 1)
-- - Niveles de instrucción (FASE 1)
-- - Profesiones (FASE 1)
-- - Especialidades (FASE 1)
-- - Grupos (FASE 2)
-- - Módulos (FASE 2)
-- - Cargos (FASE 2)
-- - Días de la semana (FASE 4)
-- - Estados de citas (FASE 4)
-- ============================================================================

-- ============================================================================
-- DATOS ADICIONALES PARA VENTAS
-- ============================================================================

-- Monedas (Solo Guaraní Paraguayo)
INSERT INTO monedas (des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, es_moneda_local, tasa_cambio, est_moneda, usuario_creacion) VALUES
    ('Guaraní Paraguayo', 'PYG', 'Gs.', 0, TRUE, 1, 'A', 'SISTEMA')
ON CONFLICT (cod_moneda) DO NOTHING;

-- Formas de cobro
INSERT INTO formas_cobro (des_forma_cobro, cod_forma_cobro, requiere_entidad, permite_cuotas, est_forma_cobro, usuario_creacion) VALUES
    ('Efectivo', 'EFECTIVO', FALSE, FALSE, 'A', 'SISTEMA'),
    ('Cheque', 'CHEQUE', TRUE, FALSE, 'A', 'SISTEMA'),
    ('Tarjeta de Crédito', 'TARJ_CRED', TRUE, TRUE, 'A', 'SISTEMA'),
    ('Tarjeta de Débito', 'TARJ_DEB', TRUE, FALSE, 'A', 'SISTEMA'),
    ('Transferencia Bancaria', 'TRANSF', TRUE, FALSE, 'A', 'SISTEMA')
ON CONFLICT (des_forma_cobro) DO NOTHING;

-- Marcas de tarjeta
INSERT INTO marcas_tarjeta (des_marca_tarjeta, cod_marca_tarjeta, est_marca_tarjeta, usuario_creacion) VALUES
    ('Visa', 'VISA', 'A', 'SISTEMA'),
    ('Mastercard', 'MASTERCARD', 'A', 'SISTEMA'),
    ('American Express', 'AMEX', 'A', 'SISTEMA')
ON CONFLICT (des_marca_tarjeta) DO NOTHING;

-- Tipos de items
INSERT INTO tipos_items (des_tipo_item, cod_tipo_item, tipo_item_categoria, requiere_stock, est_tipo_item, usuario_creacion) VALUES
    ('Consulta Médica', 'CONSULTA', 'SERVICIO', FALSE, 'A', 'SISTEMA'),
    ('Producto', 'PRODUCTO', 'PRODUCTO', TRUE, 'A', 'SISTEMA'),
    ('Servicio', 'SERVICIO', 'SERVICIO', FALSE, 'A', 'SISTEMA')
ON CONFLICT (des_tipo_item) DO NOTHING;

-- Tipos de impuestos
INSERT INTO tipos_impuestos (des_tipo_impuesto, cod_tipo_impuesto, porcentaje_impuesto, tipo_calculo, est_tipo_impuesto, usuario_creacion) VALUES
    ('IVA 10%', 'IVA10', 10.00, 'PORCENTAJE', 'A', 'SISTEMA'),
    ('IVA 5%', 'IVA5', 5.00, 'PORCENTAJE', 'A', 'SISTEMA'),
    ('Exento', 'EXENTO', 0.00, 'PORCENTAJE', 'A', 'SISTEMA')
ON CONFLICT (des_tipo_impuesto) DO NOTHING;

-- Condiciones de venta
INSERT INTO condiciones_venta (des_condicion_venta, cod_condicion_venta, dias_credito, permite_cuotas, numero_cuotas_max, est_condicion_venta, usuario_creacion) VALUES
    ('Contado', 'CONTADO', 0, FALSE, 1, 'A', 'SISTEMA'),
    ('Crédito 30 días', 'CRED_30', 30, FALSE, 1, 'A', 'SISTEMA'),
    ('Crédito 60 días', 'CRED_60', 60, FALSE, 1, 'A', 'SISTEMA')
ON CONFLICT (des_condicion_venta) DO NOTHING;

-- Tipos de comprobantes
INSERT INTO tipos_comprobantes (des_tipo_comprobante, cod_tipo_comprobante, codigo_sifen, requiere_timbrado, tipo_documento, est_tipo_comprobante, usuario_creacion) VALUES
    ('Factura', 'FACTURA', '001', TRUE, 'FACTURA', 'A', 'SISTEMA'),
    ('Recibo', 'RECIBO', '002', TRUE, 'RECIBO', 'A', 'SISTEMA'),
    ('Nota de Crédito', 'NOTA_CRED', '003', TRUE, 'NOTA_CREDITO', 'A', 'SISTEMA'),
    ('Nota de Débito', 'NOTA_DEB', '004', TRUE, 'NOTA_DEBITO', 'A', 'SISTEMA')
ON CONFLICT (des_tipo_comprobante) DO NOTHING;

-- Estados de factura
INSERT INTO estados_factura (des_estado_factura, cod_estado_factura, permite_modificacion, permite_anulacion, color_estado, est_estado_factura, usuario_creacion) VALUES
    ('Pendiente', 'PENDIENTE', TRUE, TRUE, 'warning', 'A', 'SISTEMA'),
    ('Pagada', 'PAGADA', FALSE, FALSE, 'success', 'A', 'SISTEMA'),
    ('Anulada', 'ANULADA', FALSE, FALSE, 'danger', 'A', 'SISTEMA'),
    ('Vencida', 'VENCIDA', FALSE, TRUE, 'danger', 'A', 'SISTEMA')
ON CONFLICT (des_estado_factura) DO NOTHING;

-- ============================================================================
-- CREAR USUARIO ADMINISTRADOR INICIAL
-- ============================================================================
-- NOTA: Este usuario debe crearse manualmente después de tener funcionarios
-- La contraseña debe ser cambiada en producción
-- ============================================================================

-- Ejemplo de creación de usuario administrador (descomentar y ajustar):
/*
-- IMPORTANTE: Estos INSERT siguen exactamente la estructura de los DAOs

-- 1. Crear persona administrador
-- Estructura según FuncionarioDao.guardarFuncionario() y PacienteDao.guardarPaciente()
INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_fecha_nacimiento, 
                     id_genero, id_estado_civil, per_telefono, per_correo, per_domicilio,
                     id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion) VALUES
    ('Administrador', 'Sistema', '0000000', '1980-01-01', 
     NULL, NULL, '0980000000', NULL, NULL,
     NULL, NULL, NULL, NULL)
RETURNING id_persona;

-- 2. Crear funcionario (asumiendo id_persona = 1, id_cargo = 1)
-- Estructura según FuncionarioDao.guardarFuncionario()
INSERT INTO funcionarios (id_persona, id_cargo, fun_estado, creacion_usuario) VALUES
    (1, 1, TRUE, 1)
RETURNING id_funcionario;

-- 3. Crear usuario (asumiendo id_funcionario = 1, id_grupo = 1)
-- Contraseña: admin123 (debe ser hasheada con werkzeug.security.generate_password_hash)
-- Estructura según UsuarioDao.guardarUsuario()
INSERT INTO usuarios (usu_nick, usu_clave, id_funcionario, id_grupo, 
                     usu_estado, creacion_usuario, creacion_fecha, creacion_hora) VALUES
    ('admin', 'scrypt:32768:8:1$...', 1, 1, TRUE, 1, CURRENT_DATE, CURRENT_TIME);
*/

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- 1. Los datos iniciales de referenciales ya están insertados en las fases anteriores
-- 2. Los usuarios deben crearse manualmente desde la aplicación o con scripts específicos
-- 3. Las contraseñas deben ser hasheadas usando werkzeug.security.generate_password_hash
-- 4. Los datos de ejemplo pueden ser modificados según las necesidades del negocio
-- 5. Para producción, cambiar todas las contraseñas por defecto
-- 
-- ============================================================================

-- ============================================================================
-- FIN DATOS INICIALES
-- ============================================================================

