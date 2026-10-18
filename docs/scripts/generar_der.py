"""
Regenera el DER (docs/base_de_datos/DER_completo.puml, PlantUML) a partir de la base real.

Lee del catálogo de PostgreSQL las tablas, columnas, tipos, claves primarias y foráneas de
sysclin_bd y escribe el DER con el mismo formato que ya tenía:
  - una entidad por tabla: "* pk : TIPO <<PK>>", "--", columnas con <<FK>> si son clave foránea;
  - relaciones "padre ||--o{ hija : "columna"" para todas las claves foráneas, salvo las de
    auditoría (usuario_creacion / usuario_modificacion -> usuarios), que llenarían el diagrama.
Respeta el orden de las tablas y relaciones del DER anterior; las nuevas van junto a las
parecidas. Antes de escribir guarda una copia del DER anterior (DER_completo_anterior_<fecha>.puml).

Uso (desde la raíz del repositorio, con el contenedor syscomcli_bd corriendo):
    python docs/scripts/generar_der.py              # regenera el DER
    python docs/scripts/generar_der.py --verificar  # solo compara el DER con la base (0 diferencias = al día)
"""
import os
import re
import shutil
import subprocess
import sys
from datetime import date

DER = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'base_de_datos', 'DER_completo.puml'))
AUDITORIA = ('usuario_creacion', 'usuario_modificacion')
ENCABEZADO = [
    '@startuml DER_SYSCOMCLI_COMPLETO',
    '!define PK(x) <b><color:#b8861b><&key></color> x</b>',
    '!define FK(x) <color:#6c8ebf><&link-intact></color> x',
    'hide circle',
    'skinparam linetype ortho',
]


def consultar(sql):
    salida = subprocess.run(
        ['docker', 'exec', 'syscomcli_bd', 'psql', '-U', 'postgres', '-d', 'sysclin_bd', '-At', '-F', '\t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', check=True).stdout
    return [linea.split('\t') for linea in salida.splitlines() if linea]


def tipo_der(data_type, largo, precision, escala, defecto, es_pk):
    if data_type == 'integer':
        return 'SERIAL' if es_pk and defecto.startswith('nextval') else 'INTEGER'
    if data_type == 'bigint':
        return 'BIGSERIAL' if es_pk and defecto.startswith('nextval') else 'BIGINT'
    if data_type == 'character varying':
        return f'VARCHAR({largo})' if largo else 'VARCHAR'
    if data_type == 'character':
        return f'CHAR({largo})' if largo else 'CHAR'
    if data_type == 'numeric':
        return f'NUMERIC({precision},{escala})' if precision else 'NUMERIC'
    return {
        'smallint': 'SMALLINT', 'text': 'TEXT', 'boolean': 'BOOLEAN', 'date': 'DATE',
        'timestamp without time zone': 'TIMESTAMP', 'timestamp with time zone': 'TIMESTAMPTZ',
        'time without time zone': 'TIME', 'inet': 'INET', 'uuid': 'UUID', 'jsonb': 'JSONB',
    }.get(data_type, data_type.upper())


def leer_base():
    """{tabla: [(columna, tipo, es_pk, es_fk)]} y relaciones [(padre, hija, columna)]."""
    pks = {(t, c) for t, c in consultar("""
        SELECT tc.table_name, kcu.column_name FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
          ON kcu.constraint_name = tc.constraint_name AND kcu.table_schema = tc.table_schema
        WHERE tc.table_schema = 'public' AND tc.constraint_type = 'PRIMARY KEY'""")}
    fks = consultar("""
        SELECT confrelid::regclass::text, conrelid::regclass::text, a.attname
        FROM pg_constraint k JOIN pg_attribute a ON a.attrelid = k.conrelid AND a.attnum = k.conkey[1]
        JOIN pg_namespace n ON n.oid = k.connamespace
        WHERE k.contype = 'f' AND n.nspname = 'public'""")
    columnas_fk = {(hija, col) for _, hija, col in fks}
    tablas = {}
    for t, c, tipo, largo, prec, esc, defecto in consultar("""
            SELECT table_name, column_name, data_type, COALESCE(character_maximum_length::text, ''),
                   COALESCE(numeric_precision::text, ''), COALESCE(numeric_scale::text, ''), COALESCE(column_default, '')
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
            ORDER BY table_name, ordinal_position"""):
        es_pk = (t, c) in pks
        tablas.setdefault(t, []).append((c, tipo_der(tipo, largo, prec, esc, defecto, es_pk), es_pk, (t, c) in columnas_fk))
    relaciones = [tuple(r) for r in fks if r[2] not in AUDITORIA]
    return tablas, relaciones


def leer_der(texto):
    """Tablas (en orden), columnas por tabla y relaciones (en orden) del DER existente."""
    tablas, actual = {}, None
    for linea in texto.splitlines():
        m = re.match(r'entity "(\w+)"', linea)
        if m:
            actual = m.group(1)
            tablas[actual] = []
            continue
        if actual and linea.strip() == '}':
            actual = None
            continue
        m = re.match(r'\s+\*?\s*(\w+) : (\S+)( <<(PK|FK)>>)?$', linea)
        if actual and m:
            tablas[actual].append((m.group(1), m.group(2), m.group(4) == 'PK', m.group(4) == 'FK'))
    relaciones = [tuple(r) for r in re.findall(r'^(\w+) \|\|--o\{ (\w+) : "(\w+)"', texto, re.M)]
    return tablas, relaciones


def ordenar(previas, nuevas_todas, afinidad):
    """Mantiene el orden previo y ubica cada elemento nuevo después de su afín (o al final)."""
    orden = [x for x in previas if x in nuevas_todas]
    for x in nuevas_todas:
        if x in orden:
            continue
        ancla = next((y for y in reversed(orden) if afinidad(x, y)), None)
        orden.insert(orden.index(ancla) + 1 if ancla else len(orden), x)
    return orden


def generar(tablas, relaciones, texto_anterior):
    tablas_previas, rel_previas = leer_der(texto_anterior)
    padre_de = {}
    for p, h, _ in relaciones:
        padre_de.setdefault(h, p)
    orden_tablas = ordenar(list(tablas_previas), sorted(tablas),
                           lambda nueva, vieja: padre_de.get(nueva) and padre_de.get(vieja) == padre_de.get(nueva))
    orden_rel = ordenar(rel_previas, sorted(relaciones), lambda nueva, vieja: vieja[1] == nueva[1] or vieja[0] == nueva[0])

    salida = ENCABEZADO + [
        f"' Generado desde sysclin_bd con docs/scripts/generar_der.py el {date.today():%d/%m/%Y}.",
        "' Relaciones: todas las claves foráneas, salvo las de auditoría (usuario_creacion/usuario_modificacion -> usuarios).",
        "' Datos clínicos con ON DELETE RESTRICT (migración 107): borrar una consulta o cita no borra su historia.",
        '',
    ]
    for t in orden_tablas:
        cols = tablas[t]
        salida.append(f'entity "{t}" as {t} {{')
        for c, tipo, es_pk, _ in cols:
            if es_pk:
                salida.append(f'  * {c} : {tipo} <<PK>>')
        salida.append('  --')
        for c, tipo, es_pk, es_fk in cols:
            if not es_pk:
                salida.append(f'  {c} : {tipo}' + (' <<FK>>' if es_fk else ''))
        salida += ['}', '']
    salida += [f'{p} ||--o{{ {h} : "{c}"' for p, h, c in orden_rel]
    salida.append('@enduml')
    return '\n'.join(salida) + '\n'


def diferencias(texto, tablas, relaciones):
    der_tablas, der_rel = leer_der(texto)
    dif = []
    for t in sorted(set(tablas) | set(der_tablas)):
        if t not in der_tablas:
            dif.append(f'tabla en la base, no en el DER: {t}')
        elif t not in tablas:
            dif.append(f'tabla en el DER, no en la base: {t}')
        elif sorted(der_tablas[t]) != sorted(tablas[t]):
            a, b = set(tablas[t]), set(der_tablas[t])
            dif += [f'{t}: falta en el DER {x[0]} {x[1]}' for x in sorted(a - b)]
            dif += [f'{t}: sobra en el DER {x[0]} {x[1]}' for x in sorted(b - a)]
    dif += [f'relación faltante: {r}' for r in sorted(set(relaciones) - set(der_rel))]
    dif += [f'relación que sobra: {r}' for r in sorted(set(der_rel) - set(relaciones))]
    return dif


def main():
    tablas, relaciones = leer_base()
    texto = open(DER, encoding='utf-8').read() if os.path.exists(DER) else ''
    if '--verificar' in sys.argv:
        dif = diferencias(texto, tablas, relaciones)
        print('\n'.join(dif) if dif else 'DER al día: 0 diferencias con la base')
        print(f'{len(tablas)} tablas, {sum(len(c) for c in tablas.values())} columnas, {len(relaciones)} relaciones en la base')
        sys.exit(1 if dif else 0)

    if texto:
        copia = DER.replace('.puml', f'_anterior_{date.today():%Y%m%d}.puml')
        if not os.path.exists(copia):
            shutil.copyfile(DER, copia)
            print('copia del DER anterior:', copia)
    nuevo = generar(tablas, relaciones, texto)
    with open(DER, 'w', encoding='utf-8', newline='\n') as f:
        f.write(nuevo)
    print(f'DER regenerado: {len(tablas)} tablas, {len(relaciones)} relaciones -> {DER}')


if __name__ == '__main__':
    main()
