"""Candado para que las tareas programadas corran en UN solo proceso.

APScheduler corre dentro de cada proceso que importa run.py. Si hay más de un
proceso (recarga automática de Flask en desarrollo, varios workers de gunicorn
o dos contenedores de la app contra la misma base), cada uno tendría su propio
scheduler y los recordatorios por WhatsApp se mandarían repetidos.

Usa un advisory lock de PostgreSQL tomado en una conexión propia que queda
abierta mientras viva el proceso: si el proceso termina, la conexión se cierra
y el candado se libera solo, sin intervención.
"""
import time

from app.core.base_dao import BaseDAO

# Identificador fijo del candado (cualquier bigint; debe ser único en el sistema)
SCHEDULER_LOCK_ID = 7420001

# Conexión que sostiene el candado: no se cierra mientras viva el proceso
_conexion_lock = None


def adquirir_lock_scheduler(intentos=10, espera_segundos=1):
    """True si este proceso queda como el único que ejecuta las tareas programadas.

    Reintenta unos segundos: en una recarga de desarrollo, el proceso anterior
    puede tardar un instante en soltar el candado al terminar.
    """
    global _conexion_lock
    if _conexion_lock is not None:
        return True

    con = BaseDAO(db_name_env="DB_NAME_NUEVA")._get_conexion()
    con.autocommit = True
    cur = con.cursor()
    for _ in range(intentos):
        cur.execute("SELECT pg_try_advisory_lock(%s)", (SCHEDULER_LOCK_ID,))
        if cur.fetchone()[0]:
            _conexion_lock = con
            return True
        time.sleep(espera_segundos)

    con.close()
    return False
