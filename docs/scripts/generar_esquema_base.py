"""
Genera los scripts de creación de la base (migrations/00 a 16) a partir de la base real.

Toma el esquema completo de sysclin_bd (pg_dump --schema-only, sin dueños ni permisos) y lo reparte por
módulo, con los mismos 15 módulos de los scripts originales de la base:
  - 00_funciones.sql: las funciones (las usan los triggers de todos los módulos);
  - 01 a 15: cada tabla con su secuencia, valores por defecto, claves, índices, triggers y comentarios.
    Una clave foránea va en el módulo de su tabla, salvo que apunte a una tabla de un módulo posterior:
    entonces va en el módulo de esa tabla, para que el orden de ejecución nunca falle. Una vista va en el
    último módulo de las tablas que usa;
  - 16_datos_referenciales.sql: los catálogos (decisión D1 del plan del PDF 3), con usuario_creacion y
    usuario_modificacion vacíos (en una base nueva no hay usuarios) y el valor de cada secuencia.
17_rol_sysclin_app.sql y 18_superadmin_inicial.sql no se generan: se escriben a mano (llevan contraseña).

Regla para cambiar la base (manual del administrador, §3.2): el cambio va primero en una migración temporal
migrations/NN_temp_<descripcion>.sql; se aplica en sysclin_bd y se valida; después se corre este script (y
--probar) para fusionarlo en los scripts por módulo, y se borra la migración temporal. Los archivos *_temp_*
nunca forman parte de la creación de una base nueva.

Uso (desde la raíz del repositorio, con el contenedor syscomcli_bd corriendo):
    python docs/scripts/generar_esquema_base.py           # escribe migrations/00 a 16
    python docs/scripts/generar_esquema_base.py --probar  # crea una base temporal con 00 a 17, la compara
                                                         # con sysclin_bd y la borra (no toca la base real)
"""
import collections
import os
import re
import subprocess
import sys
from datetime import date

RAIZ = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..'))
CARPETA = os.path.join(RAIZ, 'migrations')
BASE = 'sysclin_bd'
BASE_PRUEBA = 'sysclin_esquema_test'

MODULOS = [
    ('01_infraestructura_auth', 'Infraestructura y autenticación',
     'usuarios sesiones password_reset_tokens mfa_codigos mfa_dispositivos_confiables'),
    ('02_referenciales_generales', 'Referenciales generales',
     'generos estados_civiles paises departamentos ciudades profesiones niveles_instruccion cargos modulos paginas'),
    ('03_personas', 'Personas, funcionarios, pacientes y especialistas',
     'personas funcionarios pacientes pacientes_menores especialidades especialistas especialista_especialidades'),
    ('04_roles_auditoria', 'Roles, permisos, accesos y auditoría',
     'roles usuarios_roles acciones roles_permisos roles_paginas accesos_sistema auditoria_sistema'),
    ('05_sedes_clinica', 'Empresa, sedes y consultorios', 'empresa sedes consultorios'),
    ('06_referenciales_agendamiento_clinico', 'Referenciales de agendamiento y clínicos',
     'dias_semana estados_citas signos sintomas diagnosticos medicamentos tipos_analisis tipos_estudios '
     'tipos_procedimientos tipos_tratamientos tipos_certificados_medicos instrumentos'),
    ('07_agenda_citas', 'Agenda y citas',
     'agenda_horarios slots_agenda citas citas_log_estados lista_espera recordatorios'),
    ('08_consulta_anamnesis', 'Consulta, anamnesis, PEI, notas clínicas y derivaciones',
     'consultas anamnesis pei notas_clinicas derivaciones'),
    ('09_registro_clinico', 'Registro clínico',
     'insumos registro_diagnosticos registro_signos registro_sintomas registro_procedimientos registro_insumos tratamientos'),
    ('10_ordenes_recetas_certificados', 'Órdenes, recetas y certificados',
     'ordenes orden_detalle recetas receta_detalle certificados_medicos'),
    ('11_referenciales_ventas', 'Referenciales de ventas',
     'monedas condiciones_venta formas_cobro tipos_comprobantes tipos_impuestos tipos_items marcas_tarjeta '
     'entidades_adheridas entidades_emisoras estados_factura'),
    ('12_pedido_presupuesto', 'Ítems de servicio, pedidos y presupuestos',
     'items_servicios pedidos pedido_detalle presupuestos presupuesto_detalle'),
    ('13_facturacion_remisiones', 'Facturación, notas de crédito/débito y remisiones',
     'timbrados puntos_expedicion facturas factura_detalle notas_credito nota_credito_detalle notas_debito '
     'nota_debito_detalle remisiones remision_detalle'),
    ('14_caja', 'Caja, depósitos y recaudaciones',
     'cajas depositos aperturas_cierre_caja arqueos_caja recaudaciones'),
    ('15_cobranza_cxc', 'Cuentas a cobrar, cobranzas y libro de ventas',
     'cuentas_cobrar libro_ventas cobranzas cobranza_detalle'),
]
CATALOGOS = ('roles modulos paginas acciones roles_paginas roles_permisos generos estados_civiles paises '
             'departamentos ciudades profesiones niveles_instruccion cargos especialidades dias_semana estados_citas '
             'signos sintomas diagnosticos medicamentos insumos instrumentos tipos_analisis tipos_estudios '
             'tipos_procedimientos tipos_tratamientos tipos_certificados_medicos monedas condiciones_venta '
             'formas_cobro tipos_comprobantes tipos_impuestos tipos_items estados_factura marcas_tarjeta '
             'entidades_adheridas entidades_emisoras').split()
AUDITORIA = ('usuario_creacion', 'usuario_modificacion')
APLICAR = 'docker exec syscomcli_bd psql -U postgres -d <base_nueva> -q -v ON_ERROR_STOP=1 -f /tmp/{archivo}'


def docker(*args, entrada=None):
    # En bytes: en modo texto, Windows convierte \n en \r\n al enviar y eso cambia el cuerpo de las funciones
    salida = subprocess.run(['docker', 'exec', '-i', 'syscomcli_bd', *args],
                            input=entrada.encode('utf-8') if entrada is not None else None,
                            capture_output=True, check=True).stdout
    return salida.decode('utf-8')


def consultar(sql, base=BASE):
    salida = docker('psql', '-U', 'postgres', '-d', base, '-At', '-F', '\t', '-c', sql)
    return [linea.split('\t') for linea in salida.splitlines() if linea]


def cabecera(archivo, titulo, detalle):
    return (f'-- {archivo}.sql — {titulo}\n'
            f'-- Generado el {date.today():%Y-%m-%d} desde {BASE} con docs/scripts/generar_esquema_base.py, con todos los\n'
            f'-- cambios de la base hasta esa fecha ya fusionados. No se edita a mano: un cambio va primero en una\n'
            f'-- migración temporal NN_temp_<descripcion>.sql; validado, se regenera este archivo y se borra la temporal\n'
            f'-- (manual del administrador, §3.2).\n'
            f'{detalle}'
            f'-- Orden: 00 a 18, uno por uno (manual del administrador, "Crear la base desde cero"):\n'
            f'--   {APLICAR.format(archivo=archivo + ".sql")}\n\n')


def repartir():
    """{archivo: [bloques]} con el esquema de la base repartido por módulo."""
    dump = docker('pg_dump', '-U', 'postgres', '-d', BASE, '--schema-only', '--no-owner', '--no-privileges')
    dump = re.sub(r'^\\(un)?restrict .*\n', '', dump, flags=re.M)
    partes = re.split(r'\n(?=--\n-- Name: )', dump)
    preambulo = re.sub(r'\A(--.*\n|\n)+', '', partes[0]).strip() + '\n'
    modulo_de = {t: i + 1 for i, (_, _, tablas) in enumerate(MODULOS) for t in tablas.split()}
    tablas_base = {t for (t,) in consultar("SELECT relname FROM pg_class WHERE relkind = 'r' AND relnamespace = 'public'::regnamespace")}
    if tablas_base != set(modulo_de):
        sys.exit(f'Tablas sin módulo o que ya no existen: {sorted(tablas_base ^ set(modulo_de))}. Actualizar MODULOS.')
    secuencia_de = dict(consultar("""
        SELECT s.relname, t.relname FROM pg_class s
        JOIN pg_depend d ON d.objid = s.oid AND d.deptype IN ('a', 'i')
        JOIN pg_class t ON t.oid = d.refobjid
        WHERE s.relkind = 'S' AND s.relnamespace = 'public'::regnamespace"""))
    indice_de = {i: t for i, t in consultar("SELECT indexname, tablename FROM pg_indexes WHERE schemaname = 'public'")}
    vista_de = {}
    archivos = collections.defaultdict(list)
    for parte in partes[1:]:
        m = re.match(r'--\n-- Name: (.*?); Type: (.*?); Schema: .*?; Owner: .*\n', parte)
        nombre, tipo = m.group(1), m.group(2)
        primera = nombre.split()[0]
        if tipo in ('FUNCTION', 'PROCEDURE') or (tipo == 'COMMENT' and primera in ('FUNCTION', 'PROCEDURE')):
            n = 0
        elif tipo == 'TABLE':
            n = modulo_de[nombre]
        elif tipo in ('SEQUENCE', 'SEQUENCE OWNED BY'):
            n = modulo_de[secuencia_de[nombre]]
        elif tipo in ('DEFAULT', 'CONSTRAINT', 'TRIGGER'):
            n = modulo_de[primera]
        elif tipo == 'FK CONSTRAINT':
            padre = re.search(r'REFERENCES public\.(\w+)', parte).group(1)
            n = max(modulo_de[primera], modulo_de[padre])
        elif tipo == 'INDEX':
            n = modulo_de[re.search(r' ON (?:ONLY )?public\.(\w+)', parte).group(1)]
        elif tipo == 'VIEW':
            usadas = {t for t in re.findall(r'public\.(\w+)', parte) if t in modulo_de}
            n = vista_de[nombre] = max(modulo_de[t] for t in usadas)
        elif tipo == 'COMMENT':
            objeto = nombre.split()
            if objeto[0] == 'TABLE':
                n = modulo_de[objeto[1]]
            elif objeto[0] == 'COLUMN':
                tabla = objeto[1].split('.')[0]
                n = modulo_de[tabla] if tabla in modulo_de else vista_de[tabla]
            elif objeto[0] in ('CONSTRAINT', 'TRIGGER'):
                n = modulo_de[objeto[3]]
            elif objeto[0] == 'INDEX':
                n = modulo_de[indice_de[objeto[1]]]
            elif objeto[0] == 'VIEW':
                n = vista_de[objeto[1]]
            else:
                sys.exit(f'Comentario sin ubicar: {nombre}')
        else:
            sys.exit(f'Tipo de objeto sin ubicar: {tipo} ({nombre})')
        archivos[n].append(parte.rstrip() + '\n')
    return preambulo, archivos


def datos_referenciales():
    """COPY de cada catálogo (padres antes que hijos) y el valor de sus secuencias."""
    padres = collections.defaultdict(set)
    for hija, padre in consultar("""
            SELECT conrelid::regclass::text, confrelid::regclass::text FROM pg_constraint
            WHERE contype = 'f' AND connamespace = 'public'::regnamespace AND conrelid <> confrelid"""):
        if hija in CATALOGOS and padre in CATALOGOS:
            padres[hija].add(padre)
    orden, pendientes = [], list(CATALOGOS)
    while pendientes:
        lista = [t for t in pendientes if padres[t] <= set(orden)]
        if not lista:
            sys.exit(f'Dependencia circular entre catálogos: {pendientes}')
        orden += lista
        pendientes = [t for t in pendientes if t not in lista]
    salida = []
    for tabla in orden:
        columnas = [c for (c,) in consultar(
            f"SELECT column_name FROM information_schema.columns WHERE table_schema = 'public' AND table_name = '{tabla}' ORDER BY ordinal_position")]
        expresiones = ', '.join(f'NULL::integer AS {c}' if c in AUDITORIA else f'"{c}"' for c in columnas)
        pk = consultar(f"SELECT a.attname FROM pg_index i JOIN pg_attribute a ON a.attrelid = i.indrelid AND a.attnum = ANY (i.indkey) WHERE i.indrelid = '{tabla}'::regclass AND i.indisprimary")
        filas = docker('psql', '-U', 'postgres', '-d', BASE, '-Atq', '-c',
                       f'COPY (SELECT {expresiones} FROM public.{tabla} ORDER BY {", ".join(c for (c,) in pk)}) TO STDOUT')
        salida.append(f'COPY public.{tabla} ({", ".join(columnas)}) FROM stdin;\n{filas}\\.\n')
    for (secuencia,) in consultar(f"""
            SELECT s.relname FROM pg_class s
            JOIN pg_depend d ON d.objid = s.oid AND d.deptype IN ('a', 'i')
            JOIN pg_class t ON t.oid = d.refobjid
            WHERE s.relkind = 'S' AND t.relname IN ({", ".join(f"'{t}'" for t in CATALOGOS)}) ORDER BY 1"""):
        valor, llamado = consultar(f'SELECT last_value, is_called FROM public.{secuencia}')[0]
        salida.append(f"SELECT pg_catalog.setval('public.{secuencia}', {valor}, {'true' if llamado == 't' else 'false'});\n")
    return orden, '\n'.join(salida)


def escribir():
    preambulo, archivos = repartir()
    nombres = [('00_funciones', 'Funciones generales')] + [(a, t) for a, t, _ in MODULOS]
    for n, (archivo, titulo) in enumerate(nombres):
        if n == 0:
            detalle = ('-- Las 6 funciones de la base. Van primero porque los triggers de todos los módulos usan\n'
                       '-- fn_set_fecha_modificacion(). Antes: crear la base vacía (CREATE DATABASE).\n')
        else:
            detalle = (f'-- Tablas: {", ".join(MODULOS[n - 1][2].split())}.\n'
                       '-- Incluye también las claves foráneas de módulos anteriores que apuntan a estas tablas.\n')
        ruta = os.path.join(CARPETA, archivo + '.sql')
        with open(ruta, 'w', encoding='utf-8', newline='\n') as f:
            f.write(cabecera(archivo, titulo, detalle) + preambulo + '\n' + '\n'.join(archivos[n]))
        print(f'{archivo}.sql: {sum(b.count(chr(10)) for b in archivos[n])} líneas, {len(archivos[n])} objetos')
    orden, datos = datos_referenciales()
    detalle = (f'-- Catálogos y configuración del sistema ({len(orden)} tablas): {", ".join(orden)}.\n'
               '-- No incluye personas, pacientes, funcionarios, usuarios, datos clínicos ni movimientos, ni los datos\n'
               '-- propios de cada instalación (empresa, sedes, consultorios, cajas, timbrados, puntos de expedición,\n'
               '-- depósitos, ítems de servicio): se cargan desde las pantallas del sistema.\n'
               '-- usuario_creacion / usuario_modificacion van vacíos: en una base nueva todavía no hay usuarios.\n'
               '-- La moneda USD (id 99) trae una tasa de cambio de prueba: corregirla desde el ABM de monedas.\n')
    with open(os.path.join(CARPETA, '16_datos_referenciales.sql'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(cabecera('16_datos_referenciales', 'Datos referenciales', detalle) + preambulo + '\n' + datos)
    print(f'16_datos_referenciales.sql: {len(orden)} catálogos')


CONSULTA_OBJETOS = """
SELECT 'tabla', relname FROM pg_class WHERE relkind = 'r' AND relnamespace = 'public'::regnamespace
UNION ALL SELECT 'columna', table_name || '.' || column_name || ' ' || data_type || COALESCE('(' || character_maximum_length || ')', '')
       || COALESCE(' ' || numeric_precision || ',' || numeric_scale, '') || ' null=' || is_nullable || ' def=' || COALESCE(column_default, '')
       FROM information_schema.columns WHERE table_schema = 'public'
UNION ALL SELECT 'restriccion', conrelid::regclass || ' ' || conname || ' ' || contype::text || ' ' || md5(pg_get_constraintdef(oid))
       FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype <> 'c'
UNION ALL SELECT 'check', conrelid::regclass || ' ' || conname || ' '
       -- PostgreSQL reescribe los casts de "IN (...)" al cargarlos: se comparan sin casts ni paréntesis
       || regexp_replace(pg_get_constraintdef(oid), '::[a-z ]+(\\[\\])?|[() ]', '', 'g')
       FROM pg_constraint WHERE connamespace = 'public'::regnamespace AND contype = 'c'
UNION ALL SELECT 'indice', indexdef FROM pg_indexes WHERE schemaname = 'public'
UNION ALL SELECT 'funcion', proname || '(' || pg_get_function_identity_arguments(oid) || ') ' || md5(pg_get_functiondef(oid))
       FROM pg_proc WHERE pronamespace = 'public'::regnamespace
UNION ALL SELECT 'trigger', pg_get_triggerdef(oid) FROM pg_trigger WHERE NOT tgisinternal
UNION ALL SELECT 'vista', viewname || ' ' || md5(definition) FROM pg_views WHERE schemaname = 'public'
UNION ALL SELECT 'secuencia', sequencename FROM pg_sequences WHERE schemaname = 'public'
UNION ALL SELECT 'comentario', COALESCE(c.relname, '') || ' ' || d.objsubid || ' ' || md5(d.description) FROM pg_description d
       LEFT JOIN pg_class c ON c.oid = d.objoid
       WHERE d.objoid IN (SELECT oid FROM pg_class WHERE relnamespace = 'public'::regnamespace
                          UNION SELECT oid FROM pg_constraint WHERE connamespace = 'public'::regnamespace
                          UNION SELECT oid FROM pg_proc WHERE pronamespace = 'public'::regnamespace)
UNION ALL SELECT 'permiso_app', table_name || ' ' || privilege_type FROM information_schema.role_table_grants WHERE grantee = 'sysclin_app'
"""


def probar():
    """Crea BASE_PRUEBA con 00 a 17 (la 17 sin cambiar la contraseña del rol), la compara y la borra."""
    psql = ['psql', '-U', 'postgres', '-q', '-v', 'ON_ERROR_STOP=1']
    docker(*psql, '-d', 'postgres', '-c', f'DROP DATABASE IF EXISTS {BASE_PRUEBA}')
    docker(*psql, '-d', 'postgres', '-c', f'CREATE DATABASE {BASE_PRUEBA}')
    try:
        scripts = [f for f in os.listdir(CARPETA) if re.match(r'(0\d|1[0-7])_.*\.sql$', f) and '_temp_' not in f]
        for archivo in sorted(scripts):
            texto = open(os.path.join(CARPETA, archivo), encoding='utf-8').read()
            if archivo.startswith('17_'):
                # el rol es de todo el servidor: sin esta línea no cambia la contraseña real de la app
                texto = re.sub(r'^ALTER ROLE sysclin_app PASSWORD .*$', '', texto, flags=re.M)
            docker(*psql, '-d', BASE_PRUEBA, '-v', 'app_password=x', entrada=texto)
            print(f'aplicado: {archivo}')
        real, nueva = (sorted(map(tuple, consultar(CONSULTA_OBJETOS, b))) for b in (BASE, BASE_PRUEBA))
        conteo = lambda filas: collections.Counter(tipo for tipo, _ in filas)
        print(f'{"objeto":<12} {BASE:>11} {"base nueva":>11}')
        for tipo in conteo(real) | conteo(nueva):
            print(f'{tipo:<12} {conteo(real)[tipo]:>11} {conteo(nueva)[tipo]:>11}')
        diferencias = sorted(set(real) ^ set(nueva))
        for d in diferencias[:20]:
            print('DIFERENCIA', ('solo en la real:' if d in set(real) else 'solo en la nueva:'), *d)
        catalogos_mal = []
        for tabla in CATALOGOS:
            sql = (f"SELECT count(*) || ' ' || COALESCE(md5(string_agg((to_jsonb(x) - 'usuario_creacion' - 'usuario_modificacion')::text,"
                   f" '|' ORDER BY (to_jsonb(x) - 'usuario_creacion' - 'usuario_modificacion')::text)), '-') FROM public.{tabla} x")
            if consultar(sql, BASE) != consultar(sql, BASE_PRUEBA):
                catalogos_mal.append(tabla)
        print(f'catálogos iguales: {len(CATALOGOS) - len(catalogos_mal)} de {len(CATALOGOS)}', catalogos_mal or '')
        sin_datos = consultar('SELECT (SELECT count(*) FROM personas) + (SELECT count(*) FROM usuarios) + (SELECT count(*) FROM consultas) + (SELECT count(*) FROM facturas)', BASE_PRUEBA)[0][0]
        print(f'filas en personas+usuarios+consultas+facturas de la base nueva: {sin_datos}')
        ok = not diferencias and not catalogos_mal and sin_datos == '0'
        print('PRUEBA OK' if ok else 'PRUEBA CON DIFERENCIAS')
        return ok
    finally:
        docker(*psql, '-d', 'postgres', '-c', f'DROP DATABASE IF EXISTS {BASE_PRUEBA}')
        print(f'base temporal {BASE_PRUEBA} borrada')


if __name__ == '__main__':
    if '--probar' in sys.argv:
        sys.exit(0 if probar() else 1)
    escribir()
