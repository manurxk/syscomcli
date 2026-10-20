"""
Prueba de carga de los triggers (PDF 6, tarea 4; plan 09_plan_auditoria_triggers.md, paso 4).

Mide cuánto cuestan los triggers al insertar y modificar muchas filas. No toca la base real: crea una base
temporal con los scripts de creación (migrations/00 a 16, los mismos de generar_esquema_base.py), mide y la
borra. La tabla de prueba es `personas`, que tiene los dos tipos de trigger del sistema:
  - trg_personas_fecha_mod (BEFORE UPDATE, fn_set_fecha_modificacion): pone la fecha de modificación;
  - trg_personas_auditoria (AFTER INSERT/UPDATE/DELETE, fn_auditar_cambios): guarda antes/después.

Tres configuraciones (ALTER TABLE ... DISABLE/ENABLE TRIGGER):
  sin triggers · solo fecha de modificación · fecha + auditoría (como funciona el sistema)
En cada una: INSERT de N filas en una sola sentencia y UPDATE de esas N filas, medidos con
EXPLAIN (ANALYZE, FORMAT JSON), que también informa el tiempo de cada trigger. Cada medición se repite
REPETICIONES veces y se toma la mediana.

Uso (desde la raíz del repositorio, con el contenedor syscomcli_bd corriendo):
    python docs/scripts/prueba_carga_triggers.py            # 10.000 filas
    python docs/scripts/prueba_carga_triggers.py 50000      # otra cantidad
"""
import json
import os
import re
import statistics
import subprocess
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
CARPETA = os.path.join(RAIZ, 'migrations')
BASE_CARGA = 'sysclin_carga_test'
REPETICIONES = 3
PSQL = ['psql', '-U', 'postgres', '-q', '-v', 'ON_ERROR_STOP=1']

CONFIGURACIONES = [
    ('sin triggers', 'DISABLE TRIGGER trg_personas_fecha_mod', 'DISABLE TRIGGER trg_personas_auditoria'),
    ('solo fecha de modificación', 'ENABLE TRIGGER trg_personas_fecha_mod', 'DISABLE TRIGGER trg_personas_auditoria'),
    ('fecha + auditoría', 'ENABLE TRIGGER trg_personas_fecha_mod', 'ENABLE TRIGGER trg_personas_auditoria'),
]


def docker(*args, entrada=None):
    # En bytes: en modo texto, Windows convierte \n en \r\n al enviar (mismo criterio que generar_esquema_base.py)
    salida = subprocess.run(['docker', 'exec', '-i', 'syscomcli_bd', *args],
                            input=entrada.encode('utf-8') if entrada is not None else None,
                            capture_output=True, check=True).stdout
    return salida.decode('utf-8')


def sql(texto):
    return docker('psql', '-U', 'postgres', '-d', BASE_CARGA, '-At', '-c', texto).strip()


def medir(sentencia):
    """Ejecuta la sentencia con EXPLAIN ANALYZE; devuelve (ms totales, {trigger: ms})."""
    plan = json.loads(sql(f'EXPLAIN (ANALYZE, FORMAT JSON) {sentencia}'))[0]
    # Solo los triggers del sistema (trg_*); los RI_ConstraintTrigger internos son los chequeos de claves foráneas
    triggers = {t['Trigger Name']: t['Time'] for t in plan.get('Triggers', []) if t['Trigger Name'].startswith('trg_')}
    return plan['Execution Time'], triggers


def preparar_base():
    docker(*PSQL, '-d', 'postgres', '-c', f'DROP DATABASE IF EXISTS {BASE_CARGA}')
    docker(*PSQL, '-d', 'postgres', '-c', f'CREATE DATABASE {BASE_CARGA}')
    scripts = sorted(f for f in os.listdir(CARPETA) if re.match(r'(0\d|1[0-6])_.*\.sql$', f) and '_temp_' not in f)
    for archivo in scripts:
        docker(*PSQL, '-d', BASE_CARGA, entrada=open(os.path.join(CARPETA, archivo), encoding='utf-8').read())
    print(f'base temporal {BASE_CARGA} creada con {len(scripts)} scripts (00 a 16)')


def vaciar():
    sql('TRUNCATE personas, auditoria_transacciones RESTART IDENTITY CASCADE')


def miles(n):
    return f'{n:,}'.replace(',', '.')


def main():
    filas = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 10000
    insertar = (f"INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono) "
                f"SELECT 'Nombre ' || g, 'Apellido ' || g, 'PC' || g, '0981' || g FROM generate_series(1, {filas}) g")
    modificar = "UPDATE personas SET per_telefono = per_telefono || '9'"
    preparar_base()
    resultados = []
    try:
        for nombre, fecha, auditoria in CONFIGURACIONES:
            sql(f'ALTER TABLE personas {fecha}, {auditoria}')
            ins, upd, trg, auditadas = [], [], {}, 0
            for _ in range(REPETICIONES):
                vaciar()
                t, tr_i = medir(insertar)
                ins.append(t)
                sql('VACUUM ANALYZE personas')
                t, tr_u = medir(modificar)
                upd.append(t)
                for k, v in (tr_i | {f'{k} (update)': v for k, v in tr_u.items()}).items():
                    trg.setdefault(k, []).append(v)
                auditadas = int(sql('SELECT count(*) FROM auditoria_transacciones'))
            tamano = int(sql("SELECT pg_total_relation_size('auditoria_transacciones')"))
            resultados.append((nombre, statistics.median(ins), statistics.median(upd), auditadas, tamano,
                               {k: statistics.median(v) for k, v in trg.items()}))
            print(f'medido: {nombre}')
    finally:
        docker(*PSQL, '-d', 'postgres', '-c', f'DROP DATABASE IF EXISTS {BASE_CARGA}')
        print(f'base temporal {BASE_CARGA} borrada')

    base_ins, base_upd = resultados[0][1], resultados[0][2]
    print(f'\nPrueba de carga: {miles(filas)} filas en personas, mediana de {REPETICIONES} repeticiones (ms)\n')
    print(f'{"configuración":<28}{"INSERT":>10}{"ms/fila":>9}{"vs sin":>9}{"UPDATE":>10}{"ms/fila":>9}{"vs sin":>9}{"auditadas":>11}')
    for nombre, ins, upd, auditadas, _, _ in resultados:
        print(f'{nombre:<28}{ins:>10.0f}{ins / filas:>9.3f}{ins / base_ins:>8.1f}x{upd:>10.0f}{upd / filas:>9.3f}{upd / base_upd:>8.1f}x{auditadas:>11}')
    print('\nTiempo dentro de cada trigger (ms, mediana):')
    for nombre, *_, triggers in resultados:
        for trigger, ms in sorted(triggers.items()):
            print(f'  {nombre:<28}{trigger:<38}{ms:>9.0f}')
    _, _, _, auditadas, tamano, _ = resultados[-1]
    if auditadas:
        print(f'\nEspacio de la auditoría: {tamano / 1024 / 1024:.1f} MB para {miles(auditadas)} registros '
              f'(~{tamano / auditadas:.0f} bytes por cambio, con índices)')


if __name__ == '__main__':
    main()
