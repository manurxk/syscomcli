"""Extrae los mensajes de validación de datos (HTTP 400/409/422) de app/rutas.

Recorre con ast cada función con @<blueprint>.route y busca
`return jsonify({... 'error'|'mensaje'|'message': <texto>}), 400`.
Devuelve una lista de dicts; con --json la imprime, con --resumen cuenta por módulo.

Uso: python -X utf8 docs/scripts/extraer_mensajes_validacion.py [--escribir | --json]
--escribir regenera app/rutas/ayuda/mensajes_validacion.json (lo lee el anexo del manual).
"""
import ast
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
import importlib.util  # noqa: E402

# Se carga el archivo directo: importar el paquete app arrastra Flask y el resto de la aplicación
_spec = importlib.util.spec_from_file_location("mensajes_validacion", RAIZ / "app" / "utils" / "mensajes_validacion.py")
estandar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(estandar)

COMUNES = {n: getattr(estandar, n) for n in dir(estandar) if n.startswith("msg_")}
RUTAS = RAIZ / "app" / "rutas"
CODIGOS = {400, 409, 422}
CLAVES = {"error", "mensaje", "message"}
ACCION = {"GET": "Consultar", "POST": "Crear", "PUT": "Editar", "PATCH": "Editar", "DELETE": "Eliminar / dar de baja"}


def texto(nodo):
    """Texto de una constante o f-string; las partes dinámicas quedan como {…}."""
    if isinstance(nodo, ast.Constant) and isinstance(nodo.value, str):
        return nodo.value
    if isinstance(nodo, ast.JoinedStr):
        return "".join(p.value if isinstance(p, ast.Constant) else "{…}" for p in nodo.values)
    if isinstance(nodo, ast.Call) and getattr(nodo.func, "id", "") in COMUNES:
        # Los argumentos que no son constantes (el dato ingresado) quedan como {…}
        args = [a.value if isinstance(a, ast.Constant) else "{…}" for a in nodo.args]
        return COMUNES[nodo.func.id](*args)
    if isinstance(nodo, ast.BinOp) and isinstance(nodo.op, ast.Add):
        a, b = texto(nodo.left), texto(nodo.right)
        return None if a is None or b is None else a + b
    return None


def ruta_y_metodos(func):
    """(ruta, métodos) del decorador .route de la función, o None."""
    for d in func.decorator_list:
        if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr == "route":
            ruta = texto(d.args[0]) if d.args else ""
            metodos = ["GET"]
            for kw in d.keywords:
                if kw.arg == "methods" and isinstance(kw.value, (ast.List, ast.Tuple)):
                    metodos = [e.value for e in kw.value.elts if isinstance(e, ast.Constant)]
            return ruta, metodos
    return None


def constantes_de_roles(arbol):
    """Tuplas de strings definidas a nivel de módulo (p. ej. ROLES_VENTAS = (...))."""
    res = {}
    for n in arbol.body:
        if isinstance(n, ast.Assign) and isinstance(n.value, (ast.Tuple, ast.List)) and len(n.targets) == 1                 and isinstance(n.targets[0], ast.Name):
            vals = [e.value for e in n.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
            if vals:
                res[n.targets[0].id] = vals
    return res


def roles(func, consts):
    """Roles del @role_required de la función; vacío si no lo tiene o no se puede resolver."""
    for d in func.decorator_list:
        if isinstance(d, ast.Call) and getattr(d.func, "id", "") == "role_required":
            out = []
            for a in d.args:
                if isinstance(a, ast.Constant):
                    out.append(a.value)
                elif isinstance(a, ast.Starred) and isinstance(a.value, ast.Name):
                    out += consts.get(a.value.id, [])
            return out
    return []


def blueprint_de(carpeta):
    """Nombre del Blueprint de pantallas (*_routes.py) de la carpeta."""
    for f in sorted(carpeta.glob("*_routes.py")):
        m = re.search(r"Blueprint\(\s*['\"]([\w]+)['\"]", f.read_text(encoding="utf-8"))
        if m:
            return m.group(1)
    # Órdenes, recetas, certificados, etc. se usan dentro de la pantalla de Consulta
    return "consulta" if carpeta.parent.name == "movimientos" and carpeta.parent.parent.name == "clinico" else ""


def mensajes_de(func):
    """Mensajes de los `return jsonify(...), <código de validación>` de la función."""
    out = []
    for n in ast.walk(func):
        if not (isinstance(n, ast.Return) and isinstance(n.value, ast.Tuple) and len(n.value.elts) == 2):
            continue
        cuerpo, cod = n.value.elts
        if not (isinstance(cod, ast.Constant) and cod.value in CODIGOS):
            continue
        if not (isinstance(cuerpo, ast.Call) and getattr(cuerpo.func, "id", "") == "jsonify" and cuerpo.args):
            continue
        arg = cuerpo.args[0]
        if not isinstance(arg, ast.Dict):
            continue
        for k, v in zip(arg.keys, arg.values):
            if isinstance(k, ast.Constant) and k.value in CLAVES:
                if isinstance(v, ast.Name):
                    if v.id in ("e", "ex", "ve", "err"):
                        out.append((cod.value, None))  # str(e): viene del DAO
                    else:
                        for t in asignados(func, v.id):
                            out.append((cod.value, t))
                    break
                if isinstance(v, ast.Call) and getattr(v.func, "id", "") in COMUNES and len(v.args) == 1                         and isinstance(v.args[0], ast.Name):
                    # msg_obligatorio(campo) dentro de un `for campo in (...)`: un mensaje por cada campo
                    for valor in valores_del_bucle(func, v.args[0].id):
                        out.append((cod.value, COMUNES[v.func.id](valor)))
                    break
                if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "str":
                    out.append((cod.value, None))
                    break
                t = texto(v)
                if t:
                    out.append((cod.value, re.sub(r"\s+", " ", t).strip()))
                    break
    return out


def valores_del_bucle(func, nombre):
    """Constantes que recorre `for <nombre> in (...)` o `in <lista asignada en la función>`."""
    res = []
    for n in ast.walk(func):
        if isinstance(n, ast.For) and isinstance(n.target, ast.Name) and n.target.id == nombre:
            it = n.iter
            if isinstance(it, ast.Name):
                lista = it.id
                for a in ast.walk(func):
                    if isinstance(a, ast.Assign) and any(isinstance(t, ast.Name) and t.id == lista for t in a.targets):
                        it = a.value
            if isinstance(it, (ast.Tuple, ast.List)):
                res += [e.value for e in it.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return res


def asignados(func, nombre):
    """Textos constantes asignados a la variable `nombre` dentro de la función."""
    res = []
    for n in ast.walk(func):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == nombre for t in n.targets):
            t = texto(n.value)
            if t:
                res.append(re.sub(r"\s+", " ", t).strip())
    return res


def reglas_de_negocio(arbol):
    """Mensajes de `raise ValueError(...)` de los módulos dao/services que importa la ruta."""
    res = []
    for n in ast.walk(arbol):
        if isinstance(n, ast.ImportFrom) and n.module and n.module.startswith(("app.dao", "app.services")):
            f = RAIZ / (n.module.replace(".", "/") + ".py")
            if not f.exists():
                continue
            try:
                sub = ast.parse(f.read_text(encoding="utf-8"))
            except SyntaxError:
                continue
            for r in ast.walk(sub):
                if isinstance(r, ast.Raise) and isinstance(r.exc, ast.Call) and getattr(r.exc.func, "id", "") == "ValueError" and r.exc.args:
                    t = texto(r.exc.args[0])
                    if t:
                        res.append((str(f.relative_to(RAIZ)).replace("\\", "/"), re.sub(r"\s+", " ", t).strip()))
    return res


def extraer():
    res = []
    for py in sorted(RUTAS.rglob("*.py")):
        if py.name.endswith("_routes.py") or py.name == "__init__.py":
            continue
        try:
            arbol = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        partes = py.relative_to(RUTAS).parts[:-1]
        negocio = reglas_de_negocio(arbol)
        consts = constantes_de_roles(arbol)
        bp = blueprint_de(py.parent)
        for f in ast.walk(arbol):
            if not isinstance(f, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            rm = ruta_y_metodos(f)
            if not rm:
                continue
            ruta, metodos = rm
            vistos = set()
            for cod, msg in mensajes_de(f):
                lista = [(None, msg)] if msg else [(a, m) for a, m in negocio]
                for origen, m in lista:
                    if (cod, m) in vistos:
                        continue
                    vistos.add((cod, m))
                    res.append({
                        "modulo": partes[0] if partes else "",
                        "ventana": "/".join(partes[1:]) if len(partes) > 1 else partes[0] if partes else "",
                        "archivo": str(py.relative_to(RAIZ)).replace("\\", "/"),
                        "funcion": f.name,
                        "ruta": ruta,
                        "accion": ACCION.get(metodos[0], metodos[0]),
                        "roles": roles(f, consts),
                        "blueprint": bp,
                        "codigo": cod,
                        "mensaje": m,
                        "origen": "regla de negocio" if origen else "campo",
                    })
    return res


def agrupar(datos):
    """Una fila por (blueprint, acción, mensaje); los roles se unen (vacío = sin restricción)."""
    filas = {}
    for d in datos:
        acc = d["accion"] if d["origen"] == "campo" else ""
        k = (d["blueprint"], acc, d["mensaje"])
        f = filas.setdefault(k, {"blueprint": d["blueprint"], "accion": acc, "mensaje": d["mensaje"],
                                 "origen": d["origen"], "roles": set(), "libre": False})
        if d["roles"]:
            f["roles"] |= set(d["roles"])
        else:
            f["libre"] = True
    out = []
    for f in filas.values():
        out.append({"blueprint": f["blueprint"], "accion": f["accion"], "mensaje": f["mensaje"],
                    "origen": f["origen"], "roles": [] if f["libre"] else sorted(f["roles"])})
    return sorted(out, key=lambda x: (x["blueprint"], x["accion"], x["mensaje"]))


if __name__ == "__main__":
    datos = extraer()
    if "--escribir" in sys.argv:
        destino = RAIZ / "app" / "rutas" / "ayuda" / "mensajes_validacion.json"
        filas = agrupar(datos)
        destino.write_text(json.dumps(filas, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{len(filas)} mensajes escritos en {destino.relative_to(RAIZ)}")
    elif "--json" in sys.argv:
        print(json.dumps(datos, ensure_ascii=False, indent=1))
    else:
        from collections import Counter
        print(f"{len(datos)} mensajes · {len({d['mensaje'] for d in datos})} distintos · {len({d['archivo'] for d in datos})} archivos")
        for m, c in sorted(Counter(d["modulo"] for d in datos).items()):
            print(f"  {m:15} {c}")
        print("--- más repetidos:")
        for t, c in Counter(d["mensaje"] for d in datos).most_common(10):
            print(f"  {c:3}  {t}")
