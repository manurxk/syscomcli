"""Genera el manual de seguridad y operación en Word, igual al que descarga el sistema (/ayuda/seguridad/pdf).

El formato y el armado están en app/services/manual_word_service.py; este script solo lo llama fuera de
Flask, con el contenido de app/rutas/ayuda/templates/ayuda-seguridad-secciones/*.html en el orden de
SECCIONES_SEGURIDAD y los scripts de SCRIPTS_SEGURIDAD (ayuda_routes.py).

Uso: python docs/scripts/generar_manual_seguridad_docx.py [salida.docx]
Salida por defecto: docs/estandar/manual_seguridad.docx (se sobrescribe).

El índice es un campo de Word: al abrir el archivo, seleccionar todo (Ctrl+A) y presionar F9.
"""
import ast
import importlib.util
import os
import sys
from datetime import date

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RUTAS_AYUDA = os.path.join(RAIZ, 'app', 'rutas', 'ayuda', 'ayuda_routes.py')
SECCIONES_DIR = os.path.join(RAIZ, 'app', 'rutas', 'ayuda', 'templates')
LOGO = os.path.join(RAIZ, 'app', 'static', 'img', 'sys_logo.png')
SALIDA = os.path.join(RAIZ, 'docs', 'estandar', 'manual_seguridad.docx')


def cargar_servicio():
    """Carga manual_word_service.py por ruta: importar el paquete app arrancaría Flask."""
    spec = importlib.util.spec_from_file_location(
        'manual_word_service', os.path.join(RAIZ, 'app', 'services', 'manual_word_service.py'))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def _constantes_rutas():
    """Lee SECCIONES_SEGURIDAD y SCRIPTS_SEGURIDAD de ayuda_routes.py sin importar Flask."""
    with open(RUTAS_AYUDA, encoding='utf-8') as f:
        arbol = ast.parse(f.read())
    valores = {}
    for nodo in arbol.body:
        if isinstance(nodo, ast.Assign) and isinstance(nodo.targets[0], ast.Name):
            if nodo.targets[0].id in ('SECCIONES_SEGURIDAD', 'SCRIPTS_SEGURIDAD'):
                valores[nodo.targets[0].id] = ast.literal_eval(nodo.value)
    return valores['SECCIONES_SEGURIDAD'], valores['SCRIPTS_SEGURIDAD']


def main():
    salida = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else SALIDA
    secciones, scripts = _constantes_rutas()
    docx = cargar_servicio().manual_seguridad(RAIZ, SECCIONES_DIR, secciones, scripts, LOGO,
                                              date.today().strftime('%d/%m/%Y'))
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, 'wb') as f:
        f.write(docx)
    print(f'Manual generado: {salida}')


if __name__ == '__main__':
    main()
