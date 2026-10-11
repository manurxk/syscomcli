// Formato de dinero según la moneda del documento (decimales y símbolo vienen de la tabla monedas).
// Uso: formatMoney(150000, {decimales_moneda: 0, simbolo_moneda: 'Gs.'}) -> "Gs. 150.000"
window.formatMoney = function (valor, moneda) {
  const dec = moneda && moneda.decimales_moneda != null ? Number(moneda.decimales_moneda) : 0;
  const simbolo = moneda ? (moneda.simbolo_moneda || moneda.cod_moneda || '') : 'Gs.';
  const num = Number(valor);
  if (valor === null || valor === undefined || valor === '' || isNaN(num)) return '—';
  return `${simbolo} ${num.toLocaleString('es-PY', { minimumFractionDigits: dec, maximumFractionDigits: dec })}`.trim();
};
