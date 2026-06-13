-- ============================================================================
-- FASE 7: TABLAS PRINCIPALES DE VENTAS
-- ============================================================================
-- Este script crea las tablas principales (transaccionales) del módulo de Ventas
-- Ejecutar después de: 06_FASE_6_REFERENCIALES_VENTAS.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Estas tablas almacenan las transacciones y operaciones del módulo
-- 2. Todas las cantidades monetarias están en INTEGER (Guaraníes - sin decimales)
-- 3. El usuario de sesión se captura desde Flask (session['id_usuario'])
-- ============================================================================

-- ============================================================================
-- 1. APERTURAS Y CIERRES DE CAJA
-- ============================================================================
CREATE TABLE IF NOT EXISTS aperturas_cierre_caja (
    id_apertura_cierre SERIAL PRIMARY KEY,
    id_caja INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    tipo_operacion VARCHAR(20) NOT NULL,
    fecha_operacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    saldo_inicial INTEGER DEFAULT 0,
    saldo_final INTEGER,
    monto_efectivo INTEGER DEFAULT 0,
    monto_cheques INTEGER DEFAULT 0,
    monto_tarjetas INTEGER DEFAULT 0,
    monto_transferencias INTEGER DEFAULT 0,
    observaciones TEXT,
    est_apertura_cierre CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_caja) REFERENCES cajas(id_caja) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 2. ARQUEOS DE CAJA
-- ============================================================================
CREATE TABLE IF NOT EXISTS arqueos_caja (
    id_arqueo SERIAL PRIMARY KEY,
    id_apertura_cierre INTEGER NOT NULL,
    id_caja INTEGER NOT NULL,
    fecha_arqueo TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    arqueo_numero VARCHAR(50) UNIQUE,
    monto_esperado INTEGER NOT NULL,
    monto_real INTEGER NOT NULL,
    diferencia INTEGER DEFAULT 0,
    observaciones TEXT,
    est_arqueo VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_apertura_cierre) REFERENCES aperturas_cierre_caja(id_apertura_cierre) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_caja) REFERENCES cajas(id_caja) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 3. RECAUDACIONES A DEPOSITAR
-- ============================================================================
CREATE TABLE IF NOT EXISTS recaudaciones (
    id_recaudacion SERIAL PRIMARY KEY,
    id_caja INTEGER NOT NULL,
    id_deposito INTEGER NOT NULL,
    id_usuario INTEGER NOT NULL,
    recaudacion_numero VARCHAR(50) UNIQUE,
    fecha_recaudacion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_deposito DATE,
    monto_total INTEGER NOT NULL,
    monto_efectivo INTEGER DEFAULT 0,
    monto_cheques INTEGER DEFAULT 0,
    monto_tarjetas INTEGER DEFAULT 0,
    observaciones TEXT,
    est_recaudacion VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_caja) REFERENCES cajas(id_caja) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_deposito) REFERENCES depositos(id_deposito) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 4. PEDIDOS DEL CLIENTE
-- ============================================================================
CREATE TABLE IF NOT EXISTS pedidos (
    id_pedido SERIAL PRIMARY KEY,
    pedido_numero VARCHAR(50) UNIQUE NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER,
    fecha_pedido TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_entrega DATE,
    pedido_subtotal INTEGER DEFAULT 0,
    pedido_descuento INTEGER DEFAULT 0,
    pedido_total INTEGER DEFAULT 0,
    observaciones TEXT,
    est_pedido VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de Pedidos
CREATE TABLE IF NOT EXISTS pedido_detalle (
    id_pedido_detalle SERIAL PRIMARY KEY,
    id_pedido INTEGER NOT NULL,
    id_tipo_item INTEGER,
    id_consulta INTEGER,
    item_descripcion VARCHAR(255) NOT NULL,
    item_cantidad INTEGER DEFAULT 1,
    item_precio_unitario INTEGER NOT NULL,
    item_descuento INTEGER DEFAULT 0,
    item_subtotal INTEGER NOT NULL,
    observaciones TEXT,
    
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_item) REFERENCES tipos_items(id_tipo_item) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 5. FACTURAS (Facturación Electrónica)
-- ============================================================================
CREATE TABLE IF NOT EXISTS facturas (
    id_factura SERIAL PRIMARY KEY,
    factura_numero VARCHAR(50) UNIQUE NOT NULL,
    id_tipo_comprobante INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_pedido INTEGER,
    id_condicion_venta INTEGER NOT NULL,
    id_moneda INTEGER NOT NULL DEFAULT 1,
    fecha_factura TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE,
    factura_subtotal INTEGER DEFAULT 0,
    factura_descuento INTEGER DEFAULT 0,
    factura_impuestos INTEGER DEFAULT 0,
    factura_total INTEGER NOT NULL,
    factura_total_letras TEXT,
    codigo_sifen VARCHAR(50),
    numero_timbrado VARCHAR(50),
    observaciones TEXT,
    est_factura INTEGER NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_tipo_comprobante) REFERENCES tipos_comprobantes(id_tipo_comprobante) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_pedido) REFERENCES pedidos(id_pedido) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_condicion_venta) REFERENCES condiciones_venta(id_condicion_venta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_moneda) REFERENCES monedas(id_moneda) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (est_factura) REFERENCES estados_factura(id_estado_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de Facturas
CREATE TABLE IF NOT EXISTS factura_detalle (
    id_factura_detalle SERIAL PRIMARY KEY,
    id_factura INTEGER NOT NULL,
    id_tipo_item INTEGER,
    id_consulta INTEGER,
    item_descripcion VARCHAR(255) NOT NULL,
    item_cantidad INTEGER DEFAULT 1,
    item_precio_unitario INTEGER NOT NULL,
    item_descuento INTEGER DEFAULT 0,
    item_subtotal INTEGER NOT NULL,
    id_tipo_impuesto INTEGER,
    impuesto_porcentaje NUMERIC(5,2) DEFAULT 0,
    impuesto_monto INTEGER DEFAULT 0,
    item_total INTEGER NOT NULL,
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_item) REFERENCES tipos_items(id_tipo_item) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_impuesto) REFERENCES tipos_impuestos(id_tipo_impuesto) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 6. CUENTAS A COBRAR
-- ============================================================================
CREATE TABLE IF NOT EXISTS cuentas_cobrar (
    id_cuenta_cobrar SERIAL PRIMARY KEY,
    id_factura INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    cuenta_numero VARCHAR(50) UNIQUE,
    fecha_emision TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fecha_vencimiento DATE NOT NULL,
    monto_total INTEGER NOT NULL,
    monto_pagado INTEGER DEFAULT 0,
    monto_pendiente INTEGER NOT NULL,
    numero_cuotas INTEGER DEFAULT 1,
    cuota_actual INTEGER DEFAULT 1,
    observaciones TEXT,
    est_cuenta_cobrar VARCHAR(20) DEFAULT 'PENDIENTE',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 7. COBRANZAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS cobranzas (
    id_cobranza SERIAL PRIMARY KEY,
    cobranza_numero VARCHAR(50) UNIQUE NOT NULL,
    id_cuenta_cobrar INTEGER NOT NULL,
    id_factura INTEGER NOT NULL,
    id_caja INTEGER NOT NULL,
    id_forma_cobro INTEGER NOT NULL,
    fecha_cobranza TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    monto_cobrado INTEGER NOT NULL,
    observaciones TEXT,
    est_cobranza VARCHAR(20) DEFAULT 'REGISTRADA',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_cuenta_cobrar) REFERENCES cuentas_cobrar(id_cuenta_cobrar) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_caja) REFERENCES cajas(id_caja) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_forma_cobro) REFERENCES formas_cobro(id_forma_cobro) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de Cobranzas
CREATE TABLE IF NOT EXISTS cobranza_detalle (
    id_cobranza_detalle SERIAL PRIMARY KEY,
    id_cobranza INTEGER NOT NULL,
    id_forma_cobro INTEGER NOT NULL,
    id_marca_tarjeta INTEGER,
    id_entidad_adherida INTEGER,
    id_entidad_emisora INTEGER,
    numero_cheque VARCHAR(50),
    numero_tarjeta VARCHAR(50),
    numero_cuotas INTEGER DEFAULT 1,
    monto_cobrado INTEGER NOT NULL,
    observaciones TEXT,
    
    FOREIGN KEY (id_cobranza) REFERENCES cobranzas(id_cobranza) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_forma_cobro) REFERENCES formas_cobro(id_forma_cobro) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_marca_tarjeta) REFERENCES marcas_tarjeta(id_marca_tarjeta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_entidad_adherida) REFERENCES entidades_adheridas(id_entidad_adherida) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_entidad_emisora) REFERENCES entidades_emisoras(id_entidad_emisora) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 8. NOTAS DE CRÉDITO
-- ============================================================================
CREATE TABLE IF NOT EXISTS notas_credito (
    id_nota_credito SERIAL PRIMARY KEY,
    nota_credito_numero VARCHAR(50) UNIQUE NOT NULL,
    id_factura INTEGER NOT NULL,
    id_tipo_comprobante INTEGER NOT NULL,
    fecha_nota_credito TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo_nota_credito TEXT NOT NULL,
    monto_total INTEGER NOT NULL,
    codigo_sifen VARCHAR(50),
    numero_timbrado VARCHAR(50),
    observaciones TEXT,
    est_nota_credito VARCHAR(20) DEFAULT 'REGISTRADA',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_comprobante) REFERENCES tipos_comprobantes(id_tipo_comprobante) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de Notas de Crédito
CREATE TABLE IF NOT EXISTS nota_credito_detalle (
    id_nota_credito_detalle SERIAL PRIMARY KEY,
    id_nota_credito INTEGER NOT NULL,
    id_factura_detalle INTEGER,
    item_descripcion VARCHAR(255) NOT NULL,
    item_cantidad INTEGER DEFAULT 1,
    item_precio_unitario INTEGER NOT NULL,
    monto_total INTEGER NOT NULL,
    
    FOREIGN KEY (id_nota_credito) REFERENCES notas_credito(id_nota_credito) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_factura_detalle) REFERENCES factura_detalle(id_factura_detalle) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 9. NOTAS DE DÉBITO
-- ============================================================================
CREATE TABLE IF NOT EXISTS notas_debito (
    id_nota_debito SERIAL PRIMARY KEY,
    nota_debito_numero VARCHAR(50) UNIQUE NOT NULL,
    id_factura INTEGER NOT NULL,
    id_tipo_comprobante INTEGER NOT NULL,
    fecha_nota_debito TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    motivo_nota_debito TEXT NOT NULL,
    monto_total INTEGER NOT NULL,
    codigo_sifen VARCHAR(50),
    numero_timbrado VARCHAR(50),
    observaciones TEXT,
    est_nota_debito VARCHAR(20) DEFAULT 'REGISTRADA',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_comprobante) REFERENCES tipos_comprobantes(id_tipo_comprobante) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de Notas de Débito
CREATE TABLE IF NOT EXISTS nota_debito_detalle (
    id_nota_debito_detalle SERIAL PRIMARY KEY,
    id_nota_debito INTEGER NOT NULL,
    id_factura_detalle INTEGER,
    item_descripcion VARCHAR(255) NOT NULL,
    item_cantidad INTEGER DEFAULT 1,
    item_precio_unitario INTEGER NOT NULL,
    monto_total INTEGER NOT NULL,
    
    FOREIGN KEY (id_nota_debito) REFERENCES notas_debito(id_nota_debito) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_factura_detalle) REFERENCES factura_detalle(id_factura_detalle) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 10. LIBRO DE VENTAS
-- ============================================================================
CREATE TABLE IF NOT EXISTS libro_ventas (
    id_libro_venta SERIAL PRIMARY KEY,
    libro_fecha DATE NOT NULL,
    id_factura INTEGER,
    id_nota_credito INTEGER,
    id_nota_debito INTEGER,
    tipo_comprobante VARCHAR(50) NOT NULL,
    numero_comprobante VARCHAR(50) NOT NULL,
    id_paciente INTEGER NOT NULL,
    monto_gravado INTEGER DEFAULT 0,
    monto_exento INTEGER DEFAULT 0,
    monto_iva INTEGER DEFAULT 0,
    monto_total INTEGER NOT NULL,
    codigo_sifen VARCHAR(50),
    numero_timbrado VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    
    FOREIGN KEY (id_factura) REFERENCES facturas(id_factura) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_nota_credito) REFERENCES notas_credito(id_nota_credito) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_nota_debito) REFERENCES notas_debito(id_nota_debito) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_apertura_caja ON aperturas_cierre_caja(id_caja);
CREATE INDEX IF NOT EXISTS idx_apertura_usuario ON aperturas_cierre_caja(id_usuario);
CREATE INDEX IF NOT EXISTS idx_apertura_fecha ON aperturas_cierre_caja(fecha_operacion);
CREATE INDEX IF NOT EXISTS idx_arqueo_caja ON arqueos_caja(id_caja);
CREATE INDEX IF NOT EXISTS idx_recaudacion_caja ON recaudaciones(id_caja);
CREATE INDEX IF NOT EXISTS idx_recaudacion_deposito ON recaudaciones(id_deposito);
CREATE INDEX IF NOT EXISTS idx_pedido_paciente ON pedidos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_pedido_fecha ON pedidos(fecha_pedido);
CREATE INDEX IF NOT EXISTS idx_factura_paciente ON facturas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_factura_fecha ON facturas(fecha_factura);
CREATE INDEX IF NOT EXISTS idx_factura_numero ON facturas(factura_numero);
CREATE INDEX IF NOT EXISTS idx_cuenta_cobrar_factura ON cuentas_cobrar(id_factura);
CREATE INDEX IF NOT EXISTS idx_cuenta_cobrar_paciente ON cuentas_cobrar(id_paciente);
CREATE INDEX IF NOT EXISTS idx_cobranza_factura ON cobranzas(id_factura);
CREATE INDEX IF NOT EXISTS idx_cobranza_caja ON cobranzas(id_caja);
CREATE INDEX IF NOT EXISTS idx_nota_credito_factura ON notas_credito(id_factura);
CREATE INDEX IF NOT EXISTS idx_nota_debito_factura ON notas_debito(id_factura);
CREATE INDEX IF NOT EXISTS idx_libro_venta_fecha ON libro_ventas(libro_fecha);
CREATE INDEX IF NOT EXISTS idx_libro_venta_paciente ON libro_ventas(id_paciente);

-- ============================================================================
-- FUNCIÓN: Actualizar totales de facturas (FIX INTEGRADO)
-- ============================================================================
-- Esta función actualiza los totales de facturas basándose en su detalle
-- ============================================================================

CREATE OR REPLACE FUNCTION actualizar_totales_facturas()
RETURNS VOID AS $$
BEGIN
    -- Actualizar totales de todas las facturas que tienen detalle
    UPDATE facturas f
    SET 
        factura_subtotal = (
            SELECT COALESCE(SUM(item_subtotal), 0)
            FROM factura_detalle fd
            WHERE fd.id_factura = f.id_factura
        ),
        factura_impuestos = (
            SELECT COALESCE(SUM(impuesto_monto), 0)
            FROM factura_detalle fd
            WHERE fd.id_factura = f.id_factura
        ),
        factura_total = (
            SELECT COALESCE(SUM(item_total), 0)
            FROM factura_detalle fd
            WHERE fd.id_factura = f.id_factura
        ) - COALESCE(f.factura_descuento, 0),
        fecha_modificacion = CURRENT_TIMESTAMP,
        usuario_modificacion = 1
    WHERE EXISTS (
        SELECT 1 FROM factura_detalle fd WHERE fd.id_factura = f.id_factura
    );
    
    -- Actualizar también las facturas sin detalle para que tengan valores en 0 explícitos
    UPDATE facturas f
    SET 
        factura_subtotal = 0,
        factura_impuestos = 0,
        factura_total = 0 - COALESCE(f.factura_descuento, 0),
        fecha_modificacion = CURRENT_TIMESTAMP,
        usuario_modificacion = 1
    WHERE NOT EXISTS (
        SELECT 1 FROM factura_detalle fd WHERE fd.id_factura = f.id_factura
    )
    AND (factura_subtotal != 0 OR factura_impuestos != 0 OR factura_total != 0);
    
    -- Actualizar cuentas a cobrar asociadas
    UPDATE cuentas_cobrar cc
    SET 
        monto_total = (
            SELECT factura_total 
            FROM facturas f 
            WHERE f.id_factura = cc.id_factura
        ),
        monto_pendiente = (
            SELECT factura_total 
            FROM facturas f 
            WHERE f.id_factura = cc.id_factura
        ) - cc.monto_pagado,
        fecha_modificacion = CURRENT_TIMESTAMP,
        usuario_modificacion = 1
    WHERE EXISTS (
        SELECT 1 FROM facturas f WHERE f.id_factura = cc.id_factura
    );
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION actualizar_totales_facturas() IS 
'Actualiza los totales de todas las facturas basándose en su detalle y actualiza cuentas a cobrar asociadas';

-- ============================================================================
-- FIN FASE 7
-- ============================================================================








