import psycopg2.errors
from flask import current_app as app
from app.core.base_dao import BaseDAO


class AperturaCierreCajaDao(BaseDAO):
    """Acceso a datos de apertura y cierre de caja (consultas y escrituras en PostgreSQL)."""

    def __init__(self):
        super().__init__(db_name_env="DB_NAME_NUEVA")

    def getAperturasCierres(self):
        """Lista los registros de apertura/cierre de caja."""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.id_caja,
                ac.id_usuario,
                ac.tipo_operacion,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                TO_CHAR(ac.fecha_creacion, 'DD/MM/YYYY') AS fecha_registro,
                caja.des_caja,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario
            FROM aperturas_cierre_caja ac
            JOIN cajas caja ON ac.id_caja = caja.id_caja
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            ORDER BY ac.fecha_operacion DESC, ac.id_apertura_cierre DESC
        """
        return self.execute_query(sql)

    def getAperturaCierreById(self, id_apertura_cierre):
        """Devuelve el registro de apertura/cierre de caja por su id, o None si no existe."""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.id_caja,
                ac.id_usuario,
                ac.tipo_operacion,
                TO_CHAR(ac.fecha_operacion, 'YYYY-MM-DD HH24:MI:SS') AS fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                TO_CHAR(ac.fecha_creacion, 'YYYY-MM-DD') AS fecha_registro,
                ac.usuario_creacion,
                caja.des_caja,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario
            FROM aperturas_cierre_caja ac
            JOIN cajas caja ON ac.id_caja = caja.id_caja
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE ac.id_apertura_cierre = %s
        """
        return self.execute_query_one(sql, (id_apertura_cierre,))

    def getAperturaActivaPorCaja(self, id_caja):
        """Devuelve la apertura vigente de la caja, o None si está cerrada."""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                TO_CHAR(ac.fecha_operacion, 'YYYY-MM-DD HH24:MI:SS') AS fecha_operacion,
                ac.saldo_inicial,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda
            FROM aperturas_cierre_caja ac
            JOIN monedas m ON ac.id_moneda = m.id_moneda
            WHERE ac.id_caja = %s
              AND ac.tipo_operacion = 'APERTURA'
              AND ac.est_apertura_cierre = 'A'
            ORDER BY ac.fecha_operacion DESC
            LIMIT 1
        """
        return self.execute_query_one(sql, (id_caja,))

    def getEstadoCajas(self):
        """Devuelve cada caja con su estado actual (abierta o cerrada)."""
        sql = """
            SELECT
                c.id_caja,
                c.des_caja,
                c.cod_caja,
                c.caja_estado,
                ac.id_apertura_cierre,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_apertura,
                ac.saldo_inicial,
                ac.id_moneda, m.cod_moneda, m.simbolo_moneda, m.decimales_moneda,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario_apertura
            FROM cajas c
            LEFT JOIN LATERAL (
                SELECT ac2.id_apertura_cierre, ac2.fecha_operacion, ac2.saldo_inicial,
                       ac2.id_usuario, ac2.id_moneda
                FROM aperturas_cierre_caja ac2
                WHERE ac2.id_caja = c.id_caja
                  AND ac2.tipo_operacion = 'APERTURA'
                  AND ac2.est_apertura_cierre = 'A'
                ORDER BY ac2.fecha_operacion DESC
                LIMIT 1
            ) ac ON TRUE
            LEFT JOIN monedas m ON ac.id_moneda = m.id_moneda
            LEFT JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE c.est_caja = TRUE
            ORDER BY c.des_caja
        """
        return self.execute_query(sql)

    def calcularSaldoEsperado(self, id_caja):
        """Calcula el saldo esperado de la caja con los movimientos de la apertura vigente."""
        apertura = self.getAperturaActivaPorCaja(id_caja)
        if not apertura:
            return None

        sql = """
            SELECT
                COALESCE(SUM(
                    CASE WHEN fc.cod_forma_cobro = 'EFECTIVO'
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_efectivo,
                COALESCE(SUM(
                    CASE WHEN fc.cod_forma_cobro = 'CHEQUE'
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_cheques,
                COALESCE(SUM(
                    CASE WHEN fc.cod_forma_cobro IN ('TARJETA_CREDITO', 'TARJETA_DEBITO')
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_tarjetas,
                COALESCE(SUM(
                    CASE WHEN fc.cod_forma_cobro = 'TRANSFERENCIA'
                    THEN cd.monto_cobrado ELSE 0 END
                ), 0) AS total_transferencias
            FROM cobranzas c
            JOIN cobranza_detalle cd ON c.id_cobranza = cd.id_cobranza
            JOIN formas_cobro fc ON cd.id_forma_cobro = fc.id_forma_cobro
            WHERE c.id_caja = %s
              AND c.fecha_cobranza >= %s
              AND c.est_cobranza = 'REGISTRADA'
        """
        try:
            row = self.execute_query_one(sql, (id_caja, apertura['fecha_operacion']))
        except Exception:
            row = None

        efectivo = float(row['total_efectivo']) if row else 0
        cheques = float(row['total_cheques']) if row else 0
        tarjetas = float(row['total_tarjetas']) if row else 0
        transferencias = float(row['total_transferencias']) if row else 0
        saldo_inicial = float(apertura['saldo_inicial'] or 0)
        return {
            'saldo_inicial': saldo_inicial,
            'total_efectivo': efectivo,
            'total_cheques': cheques,
            'total_tarjetas': tarjetas,
            'total_transferencias': transferencias,
            'saldo_esperado': saldo_inicial + efectivo + cheques + tarjetas + transferencias,
        }

    def guardarApertura(self, id_caja, id_usuario, saldo_inicial=0,
                        observaciones=None, usuario_creacion=None, id_moneda=1):
        """Registra la apertura de caja con su saldo inicial y moneda; devuelve el id."""
        apertura_activa = self.getAperturaActivaPorCaja(id_caja)
        if apertura_activa:
            raise ValueError(f"La caja ya tiene una apertura activa (ID {apertura_activa['id_apertura_cierre']}).")

        def _fn(cur):
            cur.execute("""
                INSERT INTO aperturas_cierre_caja(
                    id_caja, id_usuario, tipo_operacion, saldo_inicial,
                    monto_efectivo, monto_cheques, monto_tarjetas, monto_transferencias,
                    observaciones, est_apertura_cierre, usuario_creacion, id_moneda
                )
                VALUES (%s, %s, 'APERTURA', %s, %s, 0, 0, 0, %s, 'A', %s, %s)
                RETURNING id_apertura_cierre
            """, (id_caja, id_usuario, saldo_inicial, saldo_inicial,
                  observaciones, usuario_creacion, id_moneda))
            apertura_id = cur.fetchone()[0]
            cur.execute("""
                UPDATE cajas
                SET caja_estado = 'ABIERTA',
                    usuario_modificacion = %s
                WHERE id_caja = %s
            """, (usuario_creacion, id_caja))
            app.logger.info(f"Apertura de caja {id_caja} registrada ID={apertura_id}")
            return apertura_id

        return self.execute_transaction(_fn)

    def guardarCierre(self, id_caja, id_usuario, saldo_final,
                      monto_efectivo=0, monto_cheques=0, monto_tarjetas=0,
                      monto_transferencias=0, observaciones=None,
                      usuario_creacion=None):
        """Registra el cierre de caja con los montos contados por medio de pago."""
        def _fn(cur):
            # sp_cerrar_caja valida, cierra la apertura, registra el CIERRE y deja la caja CERRADA
            try:
                cur.execute("""
                    CALL sp_cerrar_caja(
                        p_id_caja => %s, p_id_usuario => %s, p_saldo_final => %s,
                        o_id_cierre => NULL, o_saldo_esperado => NULL, o_diferencia => NULL,
                        p_monto_efectivo => %s, p_monto_cheques => %s, p_monto_tarjetas => %s,
                        p_monto_transferencias => %s, p_observaciones => %s, p_usuario_creacion => %s)
                """, (id_caja, id_usuario, saldo_final, monto_efectivo, monto_cheques,
                      monto_tarjetas, monto_transferencias, observaciones, usuario_creacion))
            except psycopg2.errors.RaiseException as e:
                raise ValueError(e.diag.message_primary) from e
            cierre_id, saldo_esperado, diferencia = cur.fetchone()
            app.logger.info(f"Cierre de caja {id_caja} registrado ID={cierre_id} "
                            f"(esperado={saldo_esperado}, diferencia={diferencia})")
            return cierre_id

        return self.execute_transaction(_fn)

    def getHistorialPorCaja(self, id_caja, fecha_desde=None, fecha_hasta=None):
        """Devuelve las aperturas y cierres de la caja, con filtro opcional de fechas."""
        sql = """
            SELECT
                ac.id_apertura_cierre,
                ac.tipo_operacion,
                TO_CHAR(ac.fecha_operacion, 'DD/MM/YYYY HH24:MI') AS fecha_operacion,
                ac.saldo_inicial,
                ac.saldo_final,
                ac.monto_efectivo,
                ac.monto_cheques,
                ac.monto_tarjetas,
                ac.monto_transferencias,
                ac.observaciones,
                ac.est_apertura_cierre,
                COALESCE(p.per_nombre || ' ' || p.per_apellido, u.usu_nick) AS usuario
            FROM aperturas_cierre_caja ac
            JOIN usuarios u ON ac.id_usuario = u.id_usuario
            LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
            LEFT JOIN personas p ON f.id_persona = p.id_persona
            WHERE ac.id_caja = %s
        """
        params = [id_caja]
        if fecha_desde:
            sql += " AND DATE(ac.fecha_operacion) >= %s"
            params.append(fecha_desde)
        if fecha_hasta:
            sql += " AND DATE(ac.fecha_operacion) <= %s"
            params.append(fecha_hasta)
        sql += " ORDER BY ac.fecha_operacion DESC"
        return self.execute_query(sql, tuple(params))
