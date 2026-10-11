-- 100_multimoneda.sql
-- Prepara el sistema para varias monedas. La cantidad de decimales de cada
-- monto la define monedas.decimales_moneda (PYG = 0, USD = 2); la base guarda
-- siempre NUMERIC(18,2) y la aplicacion redondea segun la moneda del documento.

BEGIN;

UPDATE monedas SET est_moneda = TRUE WHERE es_moneda_local;

DO $$
DECLARE
    t text;
BEGIN
    FOREACH t IN ARRAY ARRAY['cajas','cuentas_cobrar','cobranzas','notas_credito',
                             'notas_debito','recaudaciones','libro_ventas',
                             'pedidos','presupuestos']
    LOOP
        EXECUTE format(
            'ALTER TABLE %I ADD COLUMN IF NOT EXISTS id_moneda INTEGER NOT NULL
             DEFAULT 1 REFERENCES monedas(id_moneda)', t);
    END LOOP;
END $$;

UPDATE cuentas_cobrar cc SET id_moneda = f.id_moneda FROM facturas f WHERE f.id_factura = cc.id_factura;
UPDATE cobranzas c      SET id_moneda = cc.id_moneda FROM cuentas_cobrar cc WHERE cc.id_cuenta_cobrar = c.id_cuenta_cobrar;

DO $$
DECLARE
    r record;
BEGIN
    FOR r IN
        SELECT table_name, column_name FROM information_schema.columns
        WHERE table_schema = 'public' AND data_type = 'numeric'
          AND (table_name, column_name) IN (
            ('cuentas_cobrar','monto_pagado'),('cuentas_cobrar','monto_pendiente'),('cuentas_cobrar','monto_total'),
            ('factura_detalle','impuesto_monto'),('factura_detalle','item_descuento'),('factura_detalle','item_precio_con_iva'),
            ('factura_detalle','item_precio_unitario'),('factura_detalle','item_subtotal'),('factura_detalle','item_total'),
            ('facturas','factura_descuento'),('facturas','factura_impuestos'),('facturas','factura_subtotal'),('facturas','factura_total'),
            ('libro_ventas','monto_exento'),('libro_ventas','monto_gravado'),('libro_ventas','monto_iva'),('libro_ventas','monto_total'),
            ('nota_credito_detalle','item_precio_unitario'),('nota_credito_detalle','monto_total'),
            ('nota_debito_detalle','item_precio_unitario'),('nota_debito_detalle','monto_total'),
            ('notas_credito','monto_total'),('notas_debito','monto_total'),
            ('recaudaciones','monto_cheques'),('recaudaciones','monto_efectivo'),('recaudaciones','monto_tarjetas'),('recaudaciones','monto_total'),
            ('cobranzas','monto_cobrado'),('cobranza_detalle','monto_cobrado'))
    LOOP
        EXECUTE format('ALTER TABLE %I ALTER COLUMN %I TYPE NUMERIC(18,2)', r.table_name, r.column_name);
    END LOOP;
END $$;

COMMIT;
