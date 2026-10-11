-- 102_moneda_apertura_caja.sql
-- La moneda del turno de caja la fija la apertura, no la caja fisica
-- (100_multimoneda.sql olvido esta tabla). Default PYG.
ALTER TABLE aperturas_cierre_caja ADD COLUMN IF NOT EXISTS id_moneda INTEGER NOT NULL
    DEFAULT 1 REFERENCES monedas(id_moneda);
