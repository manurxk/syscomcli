"""
Sincroniza el DER de SQL Power Architect (docs/base_de_datos/sysconcli.architect) con la base real.

Lee del catálogo de PostgreSQL las columnas (en su orden), tipos, nulos, claves primarias y foráneas
de sysclin_bd y corrige el .architect:
  - columnas: agrega las que faltan, quita las que sobran y corrige tipo, largo/precisión y nulo;
    respeta la convención del archivo (text, inet, uuid y char se guardan como VARCHAR; smallint y
    bigint como INTEGER);
  - relaciones: agrega las claves foráneas que faltan, quita las que sobran y pone la regla de
    borrado/actualización real (CASCADE, RESTRICT, NO ACTION...).
No toca la posición ni el color de las tablas (la organización del diagrama queda igual). Las tablas
nuevas o borradas no las maneja: se agregan o quitan aparte. Antes de escribir guarda una copia
del archivo (sysconcli.architect.bak_<fecha_hora>).

Uso (desde la raíz del repositorio, con el contenedor syscomcli_bd corriendo):
    python docs/scripts/sincronizar_architect.py              # sincroniza el DER
    python docs/scripts/sincronizar_architect.py --verificar  # solo lista las diferencias (0 = al día)
"""
import collections
import os
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime

ARCHITECT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', 'base_de_datos', 'sysconcli.architect'))
NL = '\r\n'
# Regla JDBC que usa Power Architect: 0 CASCADE, 1 RESTRICT, 2 SET NULL, 3 NO ACTION, 4 SET DEFAULT
REGLA = {'c': '0', 'r': '1', 'n': '2', 'a': '3', 'd': '4'}
ENTERO = ('4', '63b011c7-c81f-4c75-8271-632b3c87f727')
TEXTO = ('12', '831ac2d4-0e65-47ec-a0b7-62b7f6b8760a')
TIPOS = {
    'integer': ENTERO, 'smallint': ENTERO, 'bigint': ENTERO,
    'numeric': ('2', '115245ce-612c-4d6a-b559-6dd903dd959a'),
    'boolean': ('16', 'a26374aa-3026-4bb8-b564-eb2e186dfa5d'),
    'date': ('91', 'ee349be3-6af2-46e1-b305-975f5354b009'),
    'time without time zone': ('92', '10d6960f-169d-47c2-860a-37341342b1d5'),
    'timestamp without time zone': ('93', '6497d8de-0e00-40d6-a42e-e2adca83be64'),
}


def consultar(sql):
    salida = subprocess.run(
        ['docker', 'exec', 'syscomcli_bd', 'psql', '-U', 'postgres', '-d', 'sysclin_bd', '-At', '-F', '\t', '-c', sql],
        capture_output=True, text=True, encoding='utf-8', check=True).stdout
    return [linea.split('\t') for linea in salida.splitlines() if linea]


def leer_base():
    """Columnas por tabla [(col, tipo, nulo, largo, precision, escala)], PK por tabla y FKs."""
    columnas = collections.defaultdict(list)
    for tabla, col, tipo, nulo, largo, prec, esc in consultar("""
            SELECT c.table_name, c.column_name, c.data_type, c.is_nullable,
                   COALESCE(c.character_maximum_length, 0), COALESCE(c.numeric_precision, 0), COALESCE(c.numeric_scale, 0)
            FROM information_schema.columns c
            JOIN information_schema.tables t USING (table_schema, table_name)
            WHERE c.table_schema = 'public' AND t.table_type = 'BASE TABLE'
            ORDER BY c.table_name, c.ordinal_position"""):
        columnas[tabla].append((col, tipo, '1' if nulo == 'YES' else '0', int(largo), int(prec), int(esc)))
    pks = dict(consultar("""
            SELECT tc.table_name, k.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage k USING (constraint_schema, constraint_name, table_name)
            WHERE tc.constraint_type = 'PRIMARY KEY' AND tc.table_schema = 'public'"""))
    fks = {}
    for hija, col, padre, col_padre, borrar, actualizar in consultar("""
            SELECT conrelid::regclass::text,
                   (SELECT attname FROM pg_attribute WHERE attrelid = conrelid AND attnum = conkey[1]),
                   confrelid::regclass::text,
                   (SELECT attname FROM pg_attribute WHERE attrelid = confrelid AND attnum = confkey[1]),
                   confdeltype, confupdtype
            FROM pg_constraint
            WHERE contype = 'f' AND connamespace = 'public'::regnamespace AND array_length(conkey, 1) = 1"""):
        fks[(hija, col, padre)] = (col_padre, REGLA[borrar], REGLA[actualizar])
    return columnas, pks, fks


def tipo_architect(tipo, largo, prec, esc):
    codigo, uuid_tipo = TIPOS.get(tipo, TEXTO)
    if tipo == 'numeric':
        return codigo, uuid_tipo, prec, esc
    return codigo, uuid_tipo, (largo if codigo == TEXTO[0] else 0), 0


def poner(etiqueta, atributo, valor):
    return re.sub(r' %s="[^"]*"' % atributo, f' {atributo}="{valor}"', etiqueta)


def sincronizar(texto, columnas, pks, fks):
    cambios = []
    ultimo = [max(int(n) for n in re.findall(r'id="[A-Z]+(\d+)"', texto)) + 1000]

    def nuevo_id(prefijo):
        ultimo[0] += 1
        return f'{prefijo}{ultimo[0]}'

    id_tabla, id_columna, quitadas = {}, {}, set()

    def tabla(m):
        bloque, tid, nombre = m.group(0), m.group(1), m.group(2)
        id_tabla[nombre] = tid
        carpeta = re.search(r'<folder id="[^"]*" populated="true" name="Columns"[^>]*>\r?\n(.*?)\s*</folder>', bloque, re.S)
        actuales = {re.search(r' name="([^"]+)"', c).group(1): c
                    for c in re.findall(r'[ \t]*<column .*?</column>', carpeta.group(1), re.S)}
        salida = []
        for col, tipo, nulo, largo, prec, esc in columnas[nombre]:
            codigo, uuid_tipo, prec, esc = tipo_architect(tipo, largo, prec, esc)
            if col in actuales:
                xml = actuales.pop(col)
                cabeza = re.match(r'[ \t]*<column [^>]*>', xml).group(0)
                nueva = cabeza
                for atributo, valor in (('type', codigo), ('userDefinedTypeUUID', uuid_tipo), ('precision', prec),
                                        ('scale', esc), ('nullable', nulo)):
                    nueva = poner(nueva, atributo, valor)
                if nueva != cabeza:
                    cambios.append(f'columna modificada: {nombre}.{col}')
                    xml = xml.replace(cabeza, nueva, 1)
            else:
                pk = ' primaryKeySeq="0"' if pks.get(nombre) == col else ''
                xml = (f'    <column id="{nuevo_id("COL")}" populated="true" UUID="{uuid.uuid4()}" autoIncrement="false" '
                       f'autoIncrementSequenceName="{nombre}_{col}_seq" defaultValue="" name="{col}" nullable="{nulo}" '
                       f'physicalName="{col}" precision="{prec}"{pk} referenceCount="1" scale="{esc}" '
                       f'sourceDataTypeName="UserDefinedSQLType" type="{codigo}" userDefinedTypeUUID="{uuid_tipo}" >'
                       f'{NL}     <remarks></remarks>{NL}    </column>')
                cambios.append(f'columna agregada: {nombre}.{col}')
            id_columna[re.search(r'<column id="([^"]+)"', xml).group(1)] = (nombre, col)
            salida.append(xml)
        for col, xml in actuales.items():
            cambios.append(f'columna quitada: {nombre}.{col}')
            quitadas.add(re.search(r'<column id="([^"]+)"', xml).group(1))
        return bloque[:carpeta.start(1)] + NL.join(salida) + bloque[carpeta.end(1):]

    texto = re.sub(r'<table id="(TAB\d+)"[^>]*? name="([^"]+)".*?</table>', tabla, texto, flags=re.S)
    if any(f' column-ref="{c}"' in texto for c in quitadas):
        sys.exit('Una columna a quitar es parte de un índice: revisar a mano.')
    tabla_de = {v: k for k, v in id_tabla.items()}
    columna_de = {(t, c): i for i, (t, c) in id_columna.items()}

    presentes, links_quitar = set(), []

    def relacion(m):
        xml = m.group(0)
        cabeza = re.match(r'[ \t]*<relationship [^>]*>', xml).group(0)
        hija = tabla_de[re.search(r'fk-table-ref="([^"]+)"', cabeza).group(1)]
        padre = tabla_de[re.search(r'pk-table-ref="([^"]+)"', cabeza).group(1)]
        refs = re.findall(r'fk-column-ref="([^"]+)"', xml)
        col = id_columna[refs[0]][1] if refs and refs[0] in id_columna else None
        clave = (hija, col, padre)
        if clave not in fks or clave in presentes:
            cambios.append(f'relación quitada: {padre} -> {hija}.{col}')
            links_quitar.append(re.search(r'id="([^"]+)"', cabeza).group(1))
            return ''
        presentes.add(clave)
        _, borrar, actualizar = fks[clave]
        nueva = poner(poner(cabeza, 'deleteRule', borrar), 'updateRule', actualizar)
        if nueva != cabeza:
            cambios.append(f'regla de relación: {padre} -> {hija}.{col}')
        return xml.replace(cabeza, nueva, 1)

    texto = re.sub(r'[ \t]*<relationship id="REL\d+".*?</relationship>\r?\n', relacion, texto, flags=re.S)
    for rid in links_quitar:
        texto = re.sub(r'[ \t]*<table-link relationship-ref="%s"[^>]*/>\r?\n' % rid, '', texto)

    relaciones, links = [], []
    for (hija, col, padre), (col_padre, borrar, actualizar) in sorted(fks.items()):
        if (hija, col, padre) in presentes:
            continue
        rid, nombre = nuevo_id('REL'), f'{padre}_{hija}_{col}_fk'
        relaciones.append(
            f'   <relationship id="{rid}" populated="true" UUID="{uuid.uuid4()}" deferrability="7" deleteRule="{borrar}" '
            f'fk-table-ref="{id_tabla[hija]}" fkCardinality="7" identifying="false" name="{nombre}" physicalName="{nombre}" '
            f'pk-table-ref="{id_tabla[padre]}" pkCardinality="2" updateRule="{actualizar}" >{NL}'
            f'    <column-mapping id="{nuevo_id("CMP")}" populated="true" UUID="{uuid.uuid4()}" '
            f'fk-column-ref="{columna_de[(hija, col)]}" name="Column Mapping" physicalName="Column Mapping" '
            f'pk-column-ref="{columna_de[(padre, col_padre)]}" />{NL}   </relationship>{NL}')
        links.append(f'  <table-link relationship-ref="{rid}" pkConnection="0.5" fkConnection="0.5" rLineColor="0x000000" '
                     f'pkLabelText="" fkLabelText="" orientation="132"/>{NL}')
        cambios.append(f'relación agregada: {padre} -> {hija}.{col}')
    for marca, bloque in (('</relationships>', relaciones), ('<table-link ', links)):
        i = texto.rfind('\n', 0, texto.index(marca)) + 1
        texto = texto[:i] + ''.join(bloque) + texto[i:]
    return texto, cambios


def main():
    verificar = '--verificar' in sys.argv
    texto = open(ARCHITECT, encoding='utf-8', newline='').read()
    columnas, pks, fks = leer_base()
    faltan = set(columnas) ^ set(re.findall(r'<table id="TAB\d+"[^>]*? name="([^"]+)"', texto))
    if faltan:
        sys.exit(f'Las tablas no coinciden con la base ({", ".join(sorted(faltan))}): agregarlas o quitarlas aparte.')
    nuevo, cambios = sincronizar(texto, columnas, pks, fks)
    for c in cambios:
        print(c)
    print(f'{len(cambios)} diferencias · {len(columnas)} tablas, '
          f'{sum(map(len, columnas.values()))} columnas, {len(fks)} relaciones en la base')
    if verificar or not cambios:
        sys.exit(1 if cambios else 0)
    copia = f'{ARCHITECT}.bak_{datetime.now():%Y%m%d_%H%M%S}'
    shutil.copy2(ARCHITECT, copia)
    with open(ARCHITECT, 'w', encoding='utf-8', newline='') as f:
        f.write(nuevo)
    print(f'DER sincronizado. Copia del anterior: {os.path.basename(copia)}')


if __name__ == '__main__':
    main()
