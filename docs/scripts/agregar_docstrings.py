"""Inserta docstrings en funciones/clases que no los tienen (PDF 7).

Recibe por stdin un JSON {archivo: {"nombre" o "Clase.nombre": "texto"}}.
Solo agrega: nunca cambia una funcion que ya tiene docstring ni toca la logica.
Un texto con saltos de linea se escribe como docstring de varias lineas.

Uso (desde la raiz del repo):
    python -I docs/scripts/agregar_docstrings.py < mapa.json
    python -I docs/scripts/agregar_docstrings.py --probar < mapa.json   # no escribe, solo informa
"""
import ast
import json
import os
import sys

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))


def _nodos(arbol):
    """Mapa 'Clase.metodo' / 'funcion' / 'Clase' -> nodo (solo no anidados)."""
    res = {}
    for n in arbol.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            res.setdefault(n.name, n)
            if isinstance(n, ast.ClassDef):
                for m in n.body:
                    if isinstance(m, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        res[f'{n.name}.{m.name}'] = m
    return res


def _literal(texto, sangria):
    texto = texto.replace('\\', '\\\\').replace('"""', '\\"\\"\\"')
    lineas = texto.strip().split('\n')
    if len(lineas) == 1:
        return [f'{sangria}"""{lineas[0]}"""']
    salida = [f'{sangria}"""{lineas[0]}']
    for l in lineas[1:]:
        salida.append(f'{sangria}{l}'.rstrip() if l.strip() else '')
    salida.append(f'{sangria}"""')
    return salida


def aplicar(mapa, probar=False):
    agregados = omitidos = 0
    for rel, docs in mapa.items():
        ruta = os.path.join(RAIZ, rel)
        with open(ruta, encoding='utf-8', newline='') as fh:
            crudo = fh.read()
        eol = '\r\n' if '\r\n' in crudo else '\n'
        lineas = crudo.split(eol)
        nodos = _nodos(ast.parse(crudo))
        inserciones = []
        for nombre, texto in docs.items():
            nodo = nodos.get(nombre)
            if nodo is None:
                print(f'  NO ENCONTRADO: {rel} {nombre}')
                omitidos += 1
                continue
            if ast.get_docstring(nodo) is not None:
                omitidos += 1
                continue
            primero = nodo.body[0]
            linea_def_fin = primero.lineno - 1
            # el cuerpo puede empezar en la misma linea que el def (una sola linea): no se soporta
            if primero.lineno == nodo.lineno:
                print(f'  UNA LINEA, omitido: {rel} {nombre}')
                omitidos += 1
                continue
            sangria = ' ' * primero.col_offset
            inserciones.append((linea_def_fin, _literal(texto, sangria)))
            agregados += 1
        for pos, bloque in sorted(inserciones, reverse=True):
            lineas[pos:pos] = bloque
        if not probar and inserciones:
            nuevo = eol.join(lineas)
            ast.parse(nuevo)
            with open(ruta, 'w', encoding='utf-8', newline='') as fh:
                fh.write(nuevo)
    return agregados, omitidos


if __name__ == '__main__':
    mapa = json.load(sys.stdin)
    a, o = aplicar(mapa, probar='--probar' in sys.argv)
    print(f'agregados: {a}  omitidos: {o}' + ('  (prueba, sin escribir)' if '--probar' in sys.argv else ''))
