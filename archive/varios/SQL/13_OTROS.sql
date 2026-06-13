-- ============================================================================
-- FIX: Actualizar totales de facturas basándose en su detalle (VERSIÓN MEJORADA)
-- ============================================================================
-- Este script actualiza los totales de todas las facturas basándose en
-- los items de su detalle. Ejecutar después de recrear la base de datos
-- o cuando se detecten facturas con totales en cero.
-- ============================================================================

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
    usuario_modificacion = 'SISTEMA'
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
    usuario_modificacion = 'SISTEMA'
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
    usuario_modificacion = 'SISTEMA'
WHERE EXISTS (
    SELECT 1 FROM facturas f WHERE f.id_factura = cc.id_factura
);

-- Mostrar resumen de facturas actualizadas
SELECT 
    'Facturas con detalle' AS tipo,
    COUNT(*) AS cantidad,
    SUM(factura_subtotal) AS total_subtotal,
    SUM(factura_impuestos) AS total_impuestos,
    SUM(factura_total) AS total_general
FROM facturas
WHERE EXISTS (
    SELECT 1 FROM factura_detalle fd WHERE fd.id_factura = facturas.id_factura
)
UNION ALL
SELECT 
    'Facturas sin detalle' AS tipo,
    COUNT(*) AS cantidad,
    SUM(factura_subtotal) AS total_subtotal,
    SUM(factura_impuestos) AS total_impuestos,
    SUM(factura_total) AS total_general
FROM facturas
WHERE NOT EXISTS (
    SELECT 1 FROM factura_detalle fd WHERE fd.id_factura = facturas.id_factura
);

-- Mostrar facturas que aún tienen problemas (opcional, para diagnóstico)
SELECT 
    f.id_factura,
    f.factura_numero,
    f.factura_subtotal,
    f.factura_impuestos,
    f.factura_total,
    COUNT(fd.id_factura_detalle) AS cantidad_items,
    COALESCE(SUM(fd.item_subtotal), 0) AS subtotal_calculado,
    COALESCE(SUM(fd.impuesto_monto), 0) AS impuestos_calculados,
    COALESCE(SUM(fd.item_total), 0) AS total_calculado
FROM facturas f
LEFT JOIN factura_detalle fd ON f.id_factura = fd.id_factura
GROUP BY f.id_factura, f.factura_numero, f.factura_subtotal, f.factura_impuestos, f.factura_total
HAVING 
    f.factura_subtotal != COALESCE(SUM(fd.item_subtotal), 0) OR
    f.factura_impuestos != COALESCE(SUM(fd.impuesto_monto), 0) OR
    f.factura_total != (COALESCE(SUM(fd.item_total), 0) - COALESCE(f.factura_descuento, 0))
ORDER BY f.id_factura;











CREATE TABLE items_servicios (
    id_item             SERIAL PRIMARY KEY,
    cod_item            VARCHAR(30),
    des_item            VARCHAR(150) NOT NULL,
    id_tipo_item        INTEGER NULL REFERENCES tipos_items(id_tipo_item),
    unidad_medida       VARCHAR(20) NOT NULL DEFAULT 'SERVICIO',
    precio_referencial  INTEGER NOT NULL DEFAULT 0,
    id_tipo_impuesto    INTEGER NULL REFERENCES tipos_impuestos(id_tipo_impuesto),
    porcentaje_impuesto NUMERIC(5,2) DEFAULT 0,
    est_item            CHAR(1) NOT NULL DEFAULT 'A',
    usuario_creacion    VARCHAR(50),
    fecha_creacion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion   TIMESTAMP
);

CREATE UNIQUE INDEX ux_items_servicios_des_item ON items_servicios (LOWER(des_item));