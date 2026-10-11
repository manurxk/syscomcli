-- 101_simbolo_pyg.sql
-- El simbolo de PYG estaba guardado como '?' (problema de codificacion).
UPDATE monedas SET simbolo_moneda = 'Gs.' WHERE cod_moneda = 'PYG' AND simbolo_moneda = '?';
