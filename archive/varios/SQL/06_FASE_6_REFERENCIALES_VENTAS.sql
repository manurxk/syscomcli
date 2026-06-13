-- ============================================================================
-- FASE 6: TABLAS REFERENCIALES DE VENTAS
-- ============================================================================
-- Este script crea las tablas referenciales del módulo de Ventas
-- Ejecutar después de: 05_FASE_5_CONSULTORIO.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Estas tablas se gestionan desde las interfaces administrativas
-- 2. Consideraciones para Paraguay: Facturación Electrónica (SIFEN)
-- 3. Todos los montos monetarios están en INTEGER (Guaraníes - sin decimales)
-- ============================================================================

-- ============================================================================
-- 1. FORMA DE COBRO
-- ============================================================================
CREATE TABLE IF NOT EXISTS formas_cobro (
    id_forma_cobro SERIAL PRIMARY KEY,
    des_forma_cobro VARCHAR(100) NOT NULL UNIQUE,
    cod_forma_cobro VARCHAR(10),
    requiere_entidad BOOLEAN DEFAULT FALSE,
    permite_cuotas BOOLEAN DEFAULT FALSE,
    est_forma_cobro CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 2. MARCA TARJETA
-- ============================================================================
CREATE TABLE IF NOT EXISTS marcas_tarjeta (
    id_marca_tarjeta SERIAL PRIMARY KEY,
    des_marca_tarjeta VARCHAR(100) NOT NULL UNIQUE,
    cod_marca_tarjeta VARCHAR(10),
    est_marca_tarjeta CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 3. ENTIDAD ADHERIDA
-- ============================================================================
CREATE TABLE IF NOT EXISTS entidades_adheridas (
    id_entidad_adherida SERIAL PRIMARY KEY,
    des_entidad_adherida VARCHAR(255) NOT NULL UNIQUE,
    cod_entidad_adherida VARCHAR(20),
    ruc_entidad VARCHAR(20),
    telefono_entidad VARCHAR(20),
    email_entidad VARCHAR(100),
    est_entidad_adherida CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 4. ENTIDAD EMISORA
-- ============================================================================
CREATE TABLE IF NOT EXISTS entidades_emisoras (
    id_entidad_emisora SERIAL PRIMARY KEY,
    des_entidad_emisora VARCHAR(255) NOT NULL UNIQUE,
    cod_entidad_emisora VARCHAR(20),
    ruc_entidad VARCHAR(20),
    telefono_entidad VARCHAR(20),
    email_entidad VARCHAR(100),
    tipo_entidad VARCHAR(50),
    est_entidad_emisora CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 5. DEPÓSITO
-- ============================================================================
CREATE TABLE IF NOT EXISTS depositos (
    id_deposito SERIAL PRIMARY KEY,
    des_deposito VARCHAR(255) NOT NULL UNIQUE,
    cod_deposito VARCHAR(20),
    tipo_deposito VARCHAR(50) NOT NULL,
    numero_cuenta VARCHAR(50),
    banco_deposito VARCHAR(100),
    ruc_banco VARCHAR(20),
    moneda_deposito VARCHAR(3) DEFAULT 'PYG',
    est_deposito CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 6. CAJA
-- ============================================================================
CREATE TABLE IF NOT EXISTS cajas (
    id_caja SERIAL PRIMARY KEY,
    des_caja VARCHAR(100) NOT NULL UNIQUE,
    cod_caja VARCHAR(20),
    caja_saldo_inicial INTEGER DEFAULT 0,
    caja_saldo_actual INTEGER DEFAULT 0,
    caja_estado VARCHAR(20) DEFAULT 'CERRADA',
    id_deposito INTEGER,
    est_caja CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_deposito) REFERENCES depositos(id_deposito) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 7. TIPO DE ITEMS
-- ============================================================================
CREATE TABLE IF NOT EXISTS tipos_items (
    id_tipo_item SERIAL PRIMARY KEY,
    des_tipo_item VARCHAR(100) NOT NULL UNIQUE,
    cod_tipo_item VARCHAR(10),
    tipo_item_categoria VARCHAR(50),
    requiere_stock BOOLEAN DEFAULT FALSE,
    est_tipo_item CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 8. TIPO DE IMPUESTOS
-- ============================================================================
CREATE TABLE IF NOT EXISTS tipos_impuestos (
    id_tipo_impuesto SERIAL PRIMARY KEY,
    des_tipo_impuesto VARCHAR(100) NOT NULL UNIQUE,
    cod_tipo_impuesto VARCHAR(10),
    porcentaje_impuesto DECIMAL(5,2) DEFAULT 0,
    tipo_calculo VARCHAR(20) DEFAULT 'PORCENTAJE',
    est_tipo_impuesto CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 9. CONDICIÓN DE VENTA
-- ============================================================================
CREATE TABLE IF NOT EXISTS condiciones_venta (
    id_condicion_venta SERIAL PRIMARY KEY,
    des_condicion_venta VARCHAR(100) NOT NULL UNIQUE,
    cod_condicion_venta VARCHAR(10),
    dias_credito INTEGER DEFAULT 0,
    permite_cuotas BOOLEAN DEFAULT FALSE,
    numero_cuotas_max INTEGER DEFAULT 1,
    est_condicion_venta CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 10. TIPO DE COMPROBANTE (Facturación Electrónica - Paraguay)
-- ============================================================================
CREATE TABLE IF NOT EXISTS tipos_comprobantes (
    id_tipo_comprobante SERIAL PRIMARY KEY,
    des_tipo_comprobante VARCHAR(100) NOT NULL UNIQUE,
    cod_tipo_comprobante VARCHAR(10),
    codigo_sifen VARCHAR(10),
    requiere_timbrado BOOLEAN DEFAULT TRUE,
    tipo_documento VARCHAR(50),
    est_tipo_comprobante CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 11. ESTADO DE FACTURA
-- ============================================================================
CREATE TABLE IF NOT EXISTS estados_factura (
    id_estado_factura SERIAL PRIMARY KEY,
    des_estado_factura VARCHAR(100) NOT NULL UNIQUE,
    cod_estado_factura VARCHAR(10),
    permite_modificacion BOOLEAN DEFAULT TRUE,
    permite_anulacion BOOLEAN DEFAULT TRUE,
    color_estado VARCHAR(20),
    est_estado_factura CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 12. MONEDA
-- ============================================================================
CREATE TABLE IF NOT EXISTS monedas (
    id_moneda SERIAL PRIMARY KEY,
    des_moneda VARCHAR(100) NOT NULL UNIQUE,
    cod_moneda VARCHAR(3) NOT NULL UNIQUE,
    simbolo_moneda VARCHAR(10),
    decimales_moneda INTEGER DEFAULT 0,
    es_moneda_local BOOLEAN DEFAULT FALSE,
    tasa_cambio DECIMAL(10,4) DEFAULT 1,
    est_moneda CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_forma_cobro_codigo ON formas_cobro(cod_forma_cobro);
CREATE INDEX IF NOT EXISTS idx_marca_tarjeta_codigo ON marcas_tarjeta(cod_marca_tarjeta);
CREATE INDEX IF NOT EXISTS idx_entidad_adherida_codigo ON entidades_adheridas(cod_entidad_adherida);
CREATE INDEX IF NOT EXISTS idx_entidad_adherida_ruc ON entidades_adheridas(ruc_entidad);
CREATE INDEX IF NOT EXISTS idx_entidad_emisora_codigo ON entidades_emisoras(cod_entidad_emisora);
CREATE INDEX IF NOT EXISTS idx_entidad_emisora_ruc ON entidades_emisoras(ruc_entidad);
CREATE INDEX IF NOT EXISTS idx_caja_codigo ON cajas(cod_caja);
CREATE INDEX IF NOT EXISTS idx_caja_estado ON cajas(caja_estado);
CREATE INDEX IF NOT EXISTS idx_caja_deposito ON cajas(id_deposito);
CREATE INDEX IF NOT EXISTS idx_tipo_item_codigo ON tipos_items(cod_tipo_item);
CREATE INDEX IF NOT EXISTS idx_tipo_item_categoria ON tipos_items(tipo_item_categoria);
CREATE INDEX IF NOT EXISTS idx_deposito_codigo ON depositos(cod_deposito);
CREATE INDEX IF NOT EXISTS idx_tipo_impuesto_codigo ON tipos_impuestos(cod_tipo_impuesto);
CREATE INDEX IF NOT EXISTS idx_condicion_venta_codigo ON condiciones_venta(cod_condicion_venta);
CREATE INDEX IF NOT EXISTS idx_tipo_comprobante_codigo ON tipos_comprobantes(cod_tipo_comprobante);
CREATE INDEX IF NOT EXISTS idx_tipo_comprobante_sifen ON tipos_comprobantes(codigo_sifen);
CREATE INDEX IF NOT EXISTS idx_estado_factura_codigo ON estados_factura(cod_estado_factura);
CREATE INDEX IF NOT EXISTS idx_moneda_codigo ON monedas(cod_moneda);
CREATE INDEX IF NOT EXISTS idx_moneda_local ON monedas(es_moneda_local);

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE formas_cobro IS 'Formas de pago disponibles (Efectivo, Cheque, Tarjeta, etc.)';
COMMENT ON TABLE marcas_tarjeta IS 'Marcas de tarjetas de crédito/débito (Visa, Mastercard, etc.)';
COMMENT ON TABLE entidades_adheridas IS 'Entidades que aceptan pagos (comercios, proveedores)';
COMMENT ON TABLE entidades_emisoras IS 'Entidades que emiten tarjetas/métodos de pago (bancos, financieras)';
COMMENT ON TABLE depositos IS 'Depósitos bancarios y cuentas para recaudaciones';
COMMENT ON TABLE cajas IS 'Puntos de caja y control de saldos';
COMMENT ON TABLE tipos_items IS 'Tipos de items vendibles (Consultas, Productos, Servicios, etc.)';
COMMENT ON TABLE tipos_impuestos IS 'Tipos de impuestos aplicables (IVA, IT, etc.)';
COMMENT ON TABLE condiciones_venta IS 'Condiciones de venta (Contado, Crédito 30 días, etc.)';
COMMENT ON TABLE tipos_comprobantes IS 'Tipos de comprobantes según facturación electrónica (SIFEN)';
COMMENT ON TABLE estados_factura IS 'Estados de las facturas (Pendiente, Pagada, Anulada, etc.)';
COMMENT ON TABLE monedas IS 'Monedas disponibles en el sistema (PYG, USD, EUR, etc.)';

-- ============================================================================
-- DATOS INICIALES
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

-- NOTA: Las siguientes tablas se gestionan desde la aplicación (no requieren datos iniciales):
-- - entidades_adheridas (se agregan dinámicamente)
-- - entidades_emisoras (se agregan dinámicamente)
-- - depositos (se agregan dinámicamente)
-- - cajas (se agregan dinámicamente)

-- ============================================================================
-- FIN FASE 6
-- ============================================================================








