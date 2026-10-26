from flask import current_app as app
from app.core.base_dao import BaseDAO
from app.core.moneda import get_moneda, redondear
from app.dao.ventas.movimientos.apertura_cierre_caja.AperturaCierreCajaDao import AperturaCierreCajaDao


class ArqueoCajaDao(BaseDAO):
    """Acceso a datos de arqueo de caja (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def _generarNumeroArqueo(self, cur):
        """Genera el siguiente número correlativo de arqueo de caja dentro de la transacción en curso (cursor `cur`)."""
        patron = "ARQ-" + "' || TO_CHAR(NOW(), 'YYYY-MM') || '-%"
        cur.execute("""
            SELECT TO_CHAR(NOW(), 'YYYY') AS anio,
                   TO_CHAR(NOW(), 'MM') AS mes,
                   COALESCE(
                       MAX(CAST(SPLIT_PART(arqueo_numero, '-', 4) AS INTEGER)), 0
                   ) + 1 AS siguiente
            FROM arqueos_caja
            WHERE arqueo_numero LIKE 'ARQ-' || TO_CHAR(NOW(), 'YYYY') || '-' || TO_CHAR(NOW(), 'MM') || '-%'
        """)
        row = cur.fetchone()
        anio, mes, siguiente = row
        return f"ARQ-{anio}-{mes}-{str(siguiente).zfill(4)}"

    def getArqueos(self):
        """Lista los registros de arqueo de caja."""
        sql = """
            SELECT
                a.id_arqueo,
                a.arqueo_numero,
                a.id_caja,
                a.id_apertura_cierre,
                TO_CHAR(a.fecha_arqueo, 'DD/MM/YYYY HH24:MI') AS fecha_arqueo,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.observaciones,
                a.est_arqueo,
                c.des_caja AS caja,
                ac.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_apertura
            FROM arqueos_caja a
            JOIN cajas c ON a.id_caja = c.id_caja
            JOIN aperturas_cierre_caja ac ON a.id_apertura_cierre = ac.id_apertura_cierre
            JOIN monedas m ON ac.id_moneda = m.id_moneda
            ORDER BY a.fecha_arqueo DESC, a.id_arqueo DESC
        """
        return self.execute_query(sql)

    def getArqueoById(self, id_arqueo):
        """Devuelve el registro de arqueo de caja por su id, o None si no existe."""
        sql = """
            SELECT
                a.id_arqueo,
                a.arqueo_numero,
                a.id_caja,
                a.id_apertura_cierre,
                TO_CHAR(a.fecha_arqueo, 'DD/MM/YYYY HH24:MI') AS fecha_arqueo,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.observaciones,
                a.est_arqueo,
                c.des_caja AS caja,
                ac.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_apertura
            FROM arqueos_caja a
            JOIN cajas c ON a.id_caja = c.id_caja
            JOIN aperturas_cierre_caja ac ON a.id_apertura_cierre = ac.id_apertura_cierre
            JOIN monedas m ON ac.id_moneda = m.id_moneda
            WHERE a.id_arqueo = %s
        """
        return self.execute_query_one(sql, (id_arqueo,))

    def getArqueosPorCaja(self, id_caja):
        """Lista los arqueos de la caja indicada."""
        sql = """
            SELECT
                a.id_arqueo,
                a.arqueo_numero,
                TO_CHAR(a.fecha_arqueo, 'DD/MM/YYYY HH24:MI') AS fecha_arqueo,
                a.monto_esperado,
                a.monto_real,
                a.diferencia,
                a.est_arqueo,
                ac.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_apertura
            FROM arqueos_caja a
            JOIN aperturas_cierre_caja ac ON a.id_apertura_cierre = ac.id_apertura_cierre
            JOIN monedas m ON ac.id_moneda = m.id_moneda
            WHERE a.id_caja = %s
            ORDER BY a.fecha_arqueo DESC
        """
        return self.execute_query(sql, (id_caja,))

    def calcularMontoEsperado(self, id_apertura_cierre, id_caja):
        """Dinero físico que debería haber en la caja ahora (efectivo + cheques): lo que se cuenta con las manos en un
        arqueo. Incluye el saldo inicial y descuenta las recaudaciones depositadas; no incluye tarjetas ni transferencias,
        que no están en el cajón. Solo existe para la apertura activa (None si la apertura no existe o ya se cerró)."""
        apertura = self.execute_query_one("""
            SELECT id_caja, est_apertura_cierre FROM aperturas_cierre_caja
            WHERE id_apertura_cierre = %s AND tipo_operacion = 'APERTURA'
        """, (id_apertura_cierre,))
        if not apertura or apertura['est_apertura_cierre'] != 'A' or apertura['id_caja'] != id_caja:
            return None
        esperado = AperturaCierreCajaDao().calcularSaldoEsperado(id_caja)
        return esperado['esperado_fisico'] if esperado else None

    def guardarArqueo(self, id_apertura_cierre, id_caja, monto_real,
                      observaciones=None, usuario_creacion=None):
        """Registra el arqueo: compara el dinero físico contado (efectivo + cheques) con el esperado y guarda la diferencia."""
        apertura = self.execute_query_one(
            "SELECT id_moneda FROM aperturas_cierre_caja WHERE id_apertura_cierre = %s",
            (id_apertura_cierre,)
        )
        if not apertura:
            raise ValueError("No se encontró la apertura de caja especificada.")
        moneda = get_moneda(apertura['id_moneda'])
        decimales = int(moneda['decimales_moneda'])

        monto_esperado = self.calcularMontoEsperado(id_apertura_cierre, id_caja)
        if monto_esperado is None:
            raise ValueError("El arqueo se hace sobre la apertura activa de la caja: esa apertura no existe o ya se cerró.")
        monto_esperado = redondear(monto_esperado, decimales)
        monto_real = redondear(monto_real, decimales)

        diferencia = monto_real - monto_esperado
        # Tolerancia: 1000 Gs. para la moneda local (sin decimales), 1 unidad para el resto (ej. 1 USD)
        tolerancia = 1000 if decimales == 0 else 1
        est_arqueo = 'CONCILIADO' if abs(diferencia) <= tolerancia else 'CON_DIFERENCIA'

        def _fn(cur):
            numero = self._generarNumeroArqueo(cur)
            cur.execute("""
                INSERT INTO arqueos_caja(
                    id_apertura_cierre, id_caja, arqueo_numero,
                    monto_esperado, monto_real, diferencia,
                    observaciones, est_arqueo, usuario_creacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id_arqueo
            """, (id_apertura_cierre, id_caja, numero,
                  monto_esperado, monto_real, diferencia,
                  observaciones, est_arqueo, usuario_creacion))
            id_arqueo = cur.fetchone()[0]
            app.logger.info(f"Arqueo {numero} registrado ID={id_arqueo}")
            return id_arqueo

        return self.execute_transaction(_fn)
