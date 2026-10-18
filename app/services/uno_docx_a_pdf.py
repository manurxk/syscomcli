"""Convierte un .docx a PDF con LibreOffice, actualizando antes los índices (tabla de contenido).

Corre con el Python del sistema (/usr/bin/python3 + python3-uno), no con el de la aplicación:
lo llama manual_word_service.docx_a_pdf().

Uso: /usr/bin/python3 uno_docx_a_pdf.py entrada.docx salida.pdf carpeta_perfil
"""
import os
import subprocess
import sys
import time

import uno
from com.sun.star.beans import PropertyValue


def _propiedad(nombre, valor):
    p = PropertyValue()
    p.Name = nombre
    p.Value = valor
    return p


def main():
    entrada, salida, perfil = (os.path.abspath(a) for a in sys.argv[1:4])
    tuberia = f'sysclin_{os.getpid()}'
    oficina = subprocess.Popen([
        'soffice', '--headless', '--invisible', '--nologo', '--norestore', '--nodefault', '--nolockcheck',
        f'-env:UserInstallation={uno.systemPathToFileUrl(perfil)}',
        f'--accept=pipe,name={tuberia};urp;StarOffice.ComponentContext',
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        local = uno.getComponentContext()
        resolvedor = local.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', local)
        contexto = None
        for _ in range(150):  # hasta ~30 s mientras LibreOffice arranca
            try:
                contexto = resolvedor.resolve(f'uno:pipe,name={tuberia};urp;StarOffice.ComponentContext')
                break
            except Exception:
                time.sleep(0.2)
        if contexto is None:
            raise RuntimeError('LibreOffice no respondió')
        escritorio = contexto.ServiceManager.createInstanceWithContext('com.sun.star.frame.Desktop', contexto)
        documento = escritorio.loadComponentFromURL(uno.systemPathToFileUrl(entrada), '_blank', 0,
                                                    (_propiedad('Hidden', True),))
        # Dos pasadas: al llenarse el índice cambian las páginas de los capítulos
        for _ in range(2):
            indices = documento.getDocumentIndexes()
            for i in range(indices.getCount()):
                indices.getByIndex(i).update()
            documento.getTextFields().refresh()
        documento.storeToURL(uno.systemPathToFileUrl(salida), (_propiedad('FilterName', 'writer_pdf_Export'),))
        documento.close(True)
        try:
            escritorio.terminate()
        except Exception:
            pass  # LibreOffice corta la conexión al cerrarse
    finally:
        try:
            oficina.wait(timeout=20)
        except subprocess.TimeoutExpired:
            oficina.kill()


if __name__ == '__main__':
    main()
