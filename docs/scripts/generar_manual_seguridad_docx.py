"""Genera un manual técnico en Word, igual al que descarga el sistema (/ayuda/seguridad/docx e /infraestructura/docx).

El formato y el armado están en app/services/manual_word_service.py y los capítulos, en
app/rutas/ayuda/ayuda_routes.py (PARTES_SEGURIDAD, SECCIONES_INFRAESTRUCTURA). Se corre dentro del contenedor,
porque los capítulos son plantillas de Flask y la Parte C del manual de seguridad se genera de los avisos:
    docker exec -w /app syscomcli_app python -X utf8 docs/scripts/generar_manual_seguridad_docx.py [seguridad|infraestructura] [salida.docx]

Salida por defecto: docs/estandar/manual_<manual>.docx (se sobrescribe). Sin argumentos genera el de seguridad.

El índice es un campo de Word: al abrir el archivo, seleccionar todo (Ctrl+A) y presionar F9.
"""
import importlib.util
import os
import sys
from datetime import date

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
LOGO = os.path.join(RAIZ, 'app', 'static', 'img', 'sys_logo.png')
MANUALES = ('seguridad', 'infraestructura')


def cargar_servicio():
    """Carga manual_word_service.py por ruta: importar el paquete app arrancaría Flask."""
    spec = importlib.util.spec_from_file_location(
        'manual_word_service', os.path.join(RAIZ, 'app', 'services', 'manual_word_service.py'))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main():
    manual = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] in MANUALES else 'seguridad'
    resto = [a for a in sys.argv[1:] if a not in MANUALES]
    salida = os.path.abspath(resto[0]) if resto else os.path.join(RAIZ, 'docs', 'estandar', f'manual_{manual}.docx')

    sys.path.insert(0, os.getcwd())
    from app import app
    from app.rutas.ayuda import ayuda_routes as r
    from app.services.ayuda_service import AyudaService

    with app.test_request_context():
        partes, anexos, scripts, datos = r._manual_tecnico(manual, r._figura(True))
        docx = AyudaService().manual_tecnico_docx(partes, anexos, scripts, date.today().strftime('%d/%m/%Y'), datos)
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, 'wb') as f:
        f.write(docx)
    for p in partes:
        print(f"{p['titulo'] or 'Sin parte'}: {len(p['capitulos'])} capítulos")
    print(f'Manual generado: {salida}')


if __name__ == '__main__':
    main()
