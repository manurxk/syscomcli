from datetime import datetime

from flask import current_app as app
from app.core.base_dao import BaseDAO


class RecaudacionDao(BaseDAO):
    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    # ── Consultas ─────────────────────────────────────────────────────────

    def getRecaudaciones(self):
        sql = """
            SELECT
                r.id_recaudacion,
                r.recaudacion_numero,
                r.id_caja,
                r.id_deposito,
                r.id_usuario,
                r.monto_total,
                r.monto_efectivo,
                r.monto_cheques,
                r.monto_tarjetas,
                r.observaciones,
                r.est_recaudacion,
                caja.des_caja,
                dep.des_deposito,
                TO_CHAR(r.fecha_recaudacion, 'DD/MM/YYYY HH24:MI') AS fecha_recaudacion_fmt,
                TO_CHAR(r.fecha_deposito,    'DD/MM/YYYY')          AS fecha_deposito_fmt,
                TO_CHAR(r.fecha_creacion,    'DD/MM/YYYY')          AS fecha_registro
            FROM recaudaciones r
            JOIN cajas     caja ON r.id_caja      = caja.id_caja
            JOIN depositos dep  ON r.id_deposito  = dep.id_deposito
            ORDER BY r.fecha_recaudacion DESC, r.id_recaudacion DESC
        """
        return self.execute_query(sql)

    def getRecaudacionById(self, id_recaudacion):
        sql = """
            SELECT
                r.id_recaudacion,
                r.recaudacion_numero,
                r.id_caja,
                r.id_deposito,
                r.id_usuario,
                r.monto_total,
                r.monto_efectivo,
                r.monto_cheques,
                r.monto_tarjetas,
                r.observaciones,
                r.est_recaudacion,
                r.usuario_creacion,
                caja.des_caja,
                dep.des_deposito,
                TO_CHAR(r.fecha_recaudacion, 'YYYY-MM-DD HH24:MI:SS') AS fecha_recaudacion_fmt,
                TO_CHAR(r.fecha_deposito,    'YYYY-MM-DD')             AS fecha_deposito_fmt,
                TO_CHAR(r.fecha_creacion,    'DD/MM/YYYY')             AS fecha_registro
            FROM recaudaciones r
            JOIN cajas     caja ON r.id_caja      = caja.id_caja
            JOIN depositos dep  ON r.id_deposito  = dep.id_deposito
            WHERE r.id_recaudacion = %s
        """
        return self.execute_query_one(sql, (id_recaudacion,))

    def getRecaudacionesPendientes(self):
        sql = """
            SELECT
                r.id_recaudacion,
                r.recaudacion_numero,
                r.monto_total,
                caja.des_caja,
                dep.des_deposito,
                TO_CHAR(r.fecha_recaudacion, 'DD/MM/YYYY HH24:MI') AS fecha_recaudacion_fmt
            FROM recaudaciones r
            JOIN cajas     caja ON r.id_caja     = caja.id_caja
            JOIN depositos dep  ON r.id_deposito = dep.id_deposito
            WHERE r.est_recaudacion = 'PENDIENTE'
            ORDER BY r.fecha_recaudacion ASC
        """
        return self.execute_query(sql)

    # ── Helpers internos ─────────────────────────────────────────────────

    def _generarNumero(self, cur):
        año    = datetime.now().year
        mes    = datetime.now().strftime('%m')
        patron = f'REC-{año}-{mes}-%'
        cur.execute(
            "SELECT recaudacion_numero FROM recaudaciones "
            "WHERE recaudacion_numero LIKE %s ORDER BY recaudacion_numero DESC LIMIT 1",
            (patron,)
        )
        row       = cur.fetchone()
        siguiente = 1
        if row and row[0]:
            partes = row[0].split('-')
            if len(partes) == 4:
                try:
                    siguiente = int(partes[3]) + 1
                except ValueError:
                    pass
        return f'REC-{año}-{mes}-{siguiente:04d}'

    def _verificarCajaAbierta(self, cur, id_caja):
        cur.execute("""
            SELECT id_apertura_cierre
            FROM aperturas_cierre_caja
            WHERE id_caja = %s
              AND tipo_operacion = 'APERTURA'
              AND est_apertura_cierre = 'A'
            LIMIT 1
        """, (id_caja,))
        if not cur.fetchone():
            raise ValueError("No hay caja abierta. Debe abrir la caja antes de registrar una recaudación.")

    # ── Escritura ─────────────────────────────────────────────────────────

    def guardar(self, data: dict, usuario_creacion=None):
        """
        Registra una recaudación en una transacción única.
        Pasos: verificar caja abierta → generar número → INSERT recaudaciones
        """
        id_caja     = data.get('id_caja')
        id_deposito = data.get('id_deposito')

        if not all([id_caja, id_deposito]):
            raise ValueError('id_caja e id_deposito son obligatorios.')

        monto_efectivo = int(data.get('monto_efectivo') or 0)
        monto_cheques  = int(data.get('monto_cheques')  or 0)
        monto_tarjetas = int(data.get('monto_tarjetas') or 0)
        monto_total    = monto_efectivo + monto_cheques + monto_tarjetas

        if monto_total <= 0:
            raise ValueError('El monto total de la recaudación debe ser mayor a cero.')

        fecha_deposito = data.get('fecha_deposito') or None

        def _fn(cur):
            self._verificarCajaAbierta(cur, id_caja)

            numero = self._generarNumero(cur)

            cur.execute("""
                INSERT INTO recaudaciones(
                    recaudacion_numero, id_caja, id_deposito, id_usuario,
                    fecha_deposito, monto_total, monto_efectivo,
                    monto_cheques, monto_tarjetas,
                    observaciones, est_recaudacion, usuario_creacion
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'PENDIENTE', %s)
                RETURNING id_recaudacion
            """, (
                numero,
                id_caja,
                id_deposito,
                usuario_creacion,
                fecha_deposito,
                monto_total,
                monto_efectivo,
                monto_cheques,
                monto_tarjetas,
                data.get('observaciones') or None,
                usuario_creacion,
            ))
            id_rec = cur.fetchone()[0]
            app.logger.info(f"Recaudación creada: {numero} (ID={id_rec})")
            return id_rec

        return self.execute_transaction(_fn)

    def marcarDepositada(self, id_recaudacion, fecha_deposito, usuario=None):
        """Cambia est_recaudacion a DEPOSITADA y registra la fecha de depósito."""
        rec = self.getRecaudacionById(id_recaudacion)
        if not rec:
            raise ValueError('Recaudación no encontrada.')
        if rec['est_recaudacion'] != 'PENDIENTE':
            raise ValueError('Solo se pueden depositar recaudaciones en estado PENDIENTE.')

        def _fn(cur):
            cur.execute("""
                UPDATE recaudaciones
                SET est_recaudacion      = 'DEPOSITADA',
                    fecha_deposito       = %s,
                    fecha_modificacion   = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_recaudacion = %s
            """, (fecha_deposito, usuario, id_recaudacion))
            return cur.rowcount > 0

        return self.execute_transaction(_fn)

    def anular(self, id_recaudacion, usuario=None):
        """Anula una recaudación PENDIENTE o DEPOSITADA."""
        rec = self.getRecaudacionById(id_recaudacion)
        if not rec:
            raise ValueError('Recaudación no encontrada.')
        if rec['est_recaudacion'] == 'ANULADA':
            return False

        def _fn(cur):
            cur.execute("""
                UPDATE recaudaciones
                SET est_recaudacion      = 'ANULADA',
                    fecha_modificacion   = CURRENT_TIMESTAMP,
                    usuario_modificacion = %s
                WHERE id_recaudacion = %s AND est_recaudacion != 'ANULADA'
            """, (usuario, id_recaudacion))
            return cur.rowcount > 0

        return self.execute_transaction(_fn)
