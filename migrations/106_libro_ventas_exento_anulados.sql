-- 106_libro_ventas_exento_anulados.sql
-- Prueba integral 2026-10-12: corrige los datos que ya están en libro_ventas por dos errores
-- del código (corregidos en FacturaDao, NotaCreditoDao y NotaDebitoDao el 2026-10-13):
--
--   1. monto_exento nunca se llenaba: una factura exenta figuraba como "gravado con IVA 0".
--      Se recalcula gravado/exento de cada factura a partir de su detalle.
--   2. Al anular una factura o una nota, su fila del libro quedaba con el monto completo
--      y seguía sumando en el libro y en "Ventas del mes". El comprobante anulado sigue
--      figurando en el libro, pero con montos en 0.
--
-- No se tocan las facturas ya emitidas con descuento (el IVA se calculaba antes del
-- descuento): son comprobantes emitidos; el error queda documentado en el plan.
--
-- Antes de aplicarla se hizo un backup: sysclin_bd_20261013_132329.dump.gpg
--   Get-Content migrations\106_libro_ventas_exento_anulados.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

-- 1. Gravado y exento de cada factura, según el IVA de sus ítems
UPDATE libro_ventas lv
SET monto_gravado = s.gravado,
    monto_exento  = s.exento
FROM (
    SELECT id_factura,
           COALESCE(SUM(item_subtotal) FILTER (WHERE impuesto_porcentaje > 0), 0)  AS gravado,
           COALESCE(SUM(item_subtotal) FILTER (WHERE COALESCE(impuesto_porcentaje, 0) = 0), 0) AS exento
    FROM factura_detalle
    GROUP BY id_factura
) s
WHERE lv.id_factura = s.id_factura
  AND lv.tipo_comprobante = 'FACTURA';

-- 2. Comprobantes anulados: figuran en el libro, pero en 0
UPDATE libro_ventas lv
SET monto_gravado = 0, monto_exento = 0, monto_iva = 0, monto_total = 0
FROM facturas f
WHERE lv.id_factura = f.id_factura
  AND lv.tipo_comprobante = 'FACTURA'
  AND f.fecha_anulacion IS NOT NULL;

UPDATE libro_ventas lv
SET monto_gravado = 0, monto_exento = 0, monto_iva = 0, monto_total = 0
FROM notas_credito nc
WHERE lv.id_nota_credito = nc.id_nota_credito
  AND nc.est_nota_credito = 'ANULADA';

UPDATE libro_ventas lv
SET monto_gravado = 0, monto_exento = 0, monto_iva = 0, monto_total = 0
FROM notas_debito nd
WHERE lv.id_nota_debito = nd.id_nota_debito
  AND nd.est_nota_debito = 'ANULADA';

COMMIT;
