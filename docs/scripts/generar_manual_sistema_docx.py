"""Genera el Manual del sistema en Word (guías de uso + seguridad en un solo documento, por partes).

El armado está en ayuda_routes._sistema_partes y el formato en app/services/manual_word_service.py. Se corre
dentro del contenedor, porque las secciones de la guía son plantillas de Flask:
    docker exec -w /app syscomcli_app python -X utf8 docs/scripts/generar_manual_sistema_docx.py [salida.docx]
Salida por defecto: docs/estandar/manual_sistema.docx (se sobrescribe).

El índice es un campo de Word: al abrir el archivo, seleccionar todo (Ctrl+A) y presionar F9.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.getcwd())
from app import app  # noqa: E402
from app.rutas.ayuda import ayuda_routes as r  # noqa: E402
from app.services.ayuda_service import AyudaService  # noqa: E402

SALIDA = os.path.join('docs', 'estandar', 'manual_sistema.docx')


def main():
    salida = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.abspath(SALIDA)
    with app.test_request_context():
        partes = r._sistema_partes(r._figura(True))
        docx = AyudaService().manual_sistema_docx(partes, r.SCRIPTS_INFRAESTRUCTURA, date.today().strftime('%d/%m/%Y'))
    os.makedirs(os.path.dirname(salida), exist_ok=True)
    with open(salida, 'wb') as f:
        f.write(docx)
    for p in partes:
        print(f"{p['titulo']}: {len(p['capitulos'])} capítulos")
    print(f'Manual generado: {salida}')


if __name__ == '__main__':
    main()
