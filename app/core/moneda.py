from decimal import Decimal, ROUND_HALF_UP

from app.core.base_dao import BaseDAO

MONEDA_LOCAL_ID = 1


def redondear(monto, decimales):
    """Redondea un monto a los decimales de su moneda (PYG=0, USD=2)."""
    exp = Decimal(1).scaleb(-int(decimales))
    return Decimal(str(monto or 0)).quantize(exp, rounding=ROUND_HALF_UP)


def get_moneda(id_moneda=None, cur=None):
    """Devuelve dict con los datos de la moneda; ValueError si no existe o esta inactiva."""
    id_moneda = id_moneda or MONEDA_LOCAL_ID
    sql = ("SELECT id_moneda, des_moneda, cod_moneda, simbolo_moneda, decimales_moneda, "
           "es_moneda_local, est_moneda FROM monedas WHERE id_moneda = %s")
    if cur is not None:
        cur.execute(sql, (id_moneda,))
        fila = cur.fetchone()
        fila = dict(zip([c[0] for c in cur.description], fila)) if fila else None
    else:
        fila = BaseDAO(db_name_env="DB_NAME_NUEVA").execute_query_one(sql, (id_moneda,))
    if not fila:
        raise ValueError('La moneda indicada no existe.')
    if not fila['est_moneda']:
        raise ValueError('La moneda indicada está inactiva.')
    return fila


def formatear(monto, moneda):
    """Ej.: 1500000 PYG -> 'Gs. 1.500.000'; 1234.5 USD -> 'US$ 1,234.50' (separadores según moneda)."""
    dec = int(moneda['decimales_moneda'])
    valor = redondear(monto, dec)
    texto = f"{valor:,.{dec}f}"
    if moneda.get('es_moneda_local'):
        texto = texto.replace(',', '#').replace('.', ',').replace('#', '.')
    simbolo = moneda.get('simbolo_moneda') or moneda.get('cod_moneda')
    return f"{simbolo} {texto}"
