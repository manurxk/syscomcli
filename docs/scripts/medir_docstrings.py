"""Mide la cobertura de docstrings de app/dao y app/rutas (PDF 7).

Uso (desde la raiz del repo):
    python docs/scripts/medir_docstrings.py            # resumen por carpeta
    python docs/scripts/medir_docstrings.py --faltan   # ademas, lista lo que no tiene docstring
    python docs/scripts/medir_docstrings.py --faltan ventas   # filtra por texto en la ruta

Cuenta funciones, metodos y clases. Excluye metodos magicos (__x__) y las
funciones anidadas dentro de otras funciones.
"""
import ast
import os
import sys

RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
ZONAS = ['app/dao', 'app/rutas']
META = 80


def items(arbol):
    """Devuelve (nombre, linea, tiene_docstring) de clases y funciones no anidadas."""
    def recorrer(nodo, dentro_de_funcion):
        for hijo in ast.iter_child_nodes(nodo):
            es_func = isinstance(hijo, (ast.FunctionDef, ast.AsyncFunctionDef))
            if es_func or isinstance(hijo, ast.ClassDef):
                magico = es_func and hijo.name.startswith('__') and hijo.name.endswith('__')
                if not dentro_de_funcion and not magico:
                    yield hijo.name, hijo.lineno, ast.get_docstring(hijo) is not None
                yield from recorrer(hijo, dentro_de_funcion or es_func)
            else:
                yield from recorrer(hijo, dentro_de_funcion)
    return recorrer(arbol, False)


def main():
    args = [a for a in sys.argv[1:] if a != '--faltan']
    listar = '--faltan' in sys.argv
    filtro = args[0].lower() if args else ''
    for zona in ZONAS:
        base = os.path.normpath(os.path.join(RAIZ, zona))
        total = con = 0
        por_sub = {}
        faltan = []
        for d, _, fs in os.walk(base):
            for f in sorted(fs):
                if not f.endswith('.py'):
                    continue
                ruta = os.path.join(d, f)
                rel = os.path.relpath(ruta, RAIZ).replace(os.sep, '/')
                with open(ruta, encoding='utf-8') as fh:
                    try:
                        arbol = ast.parse(fh.read())
                    except SyntaxError:
                        print('  (no se pudo leer)', rel)
                        continue
                sub = os.path.relpath(d, base).replace(os.sep, '/').split('/')[0]
                for nombre, linea, tiene in items(arbol):
                    total += 1
                    con += tiene
                    a = por_sub.setdefault(sub, [0, 0])
                    a[0] += 1
                    a[1] += tiene
                    if not tiene:
                        faltan.append(f'{rel}:{linea} {nombre}')
        pct = round(100 * con / total, 1) if total else 0
        marca = 'OK' if pct >= META else f'falta {META - pct:.1f} pts'
        print(f'{zona}: {con}/{total} = {pct}%  [{marca}]')
        for sub, (t, c) in sorted(por_sub.items()):
            print(f'    {sub:<16} {c:>4}/{t:<4} {round(100 * c / t):>3}%')
        if listar:
            for linea in faltan:
                if filtro in linea.lower():
                    print('      sin docstring:', linea)


if __name__ == '__main__':
    main()
