import os
import psycopg2
from flask import current_app as app


class BaseDAO:
    def __init__(self, db_name_env="DB_NAME"):
        self._db_name_env = db_name_env

    def _get_conexion(self):
        return psycopg2.connect(
            dbname=os.getenv(self._db_name_env, "clinicain"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            host=os.getenv("DB_HOST", "127.0.0.1"),
            port=os.getenv("DB_PORT", "5432"),
        )

    def execute_query(self, sql, params=None, commit=False):
        con = self._get_conexion()
        cur = con.cursor()
        try:
            cur.execute(sql, params or ())
            if commit:
                con.commit()
                return cur.rowcount
            columnas = [c[0] for c in cur.description] if cur.description else []
            filas = cur.fetchall()
            return [dict(zip(columnas, f)) for f in filas]
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error de BD en {self.__class__.__name__}: {e}")
            raise
        finally:
            cur.close()
            con.close()

    def execute_query_one(self, sql, params=None, commit=False):
        con = self._get_conexion()
        cur = con.cursor()
        try:
            cur.execute(sql, params or ())
            if commit:
                fila = cur.fetchone()
                con.commit()
            else:
                columnas = [c[0] for c in cur.description] if cur.description else []
                f = cur.fetchone()
                fila = dict(zip(columnas, f)) if f else None
            return fila
        except Exception as e:
            con.rollback()
            app.logger.error(f"Error de BD en {self.__class__.__name__}: {e}")
            raise
        finally:
            cur.close()
            con.close()
