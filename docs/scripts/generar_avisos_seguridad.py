"""Genera el capítulo "Avisos de validación" del manual de seguridad (HTML fijo, lo lee manual_word_service).

Usa los mismos datos y tipos que el anexo de la guía de uso (ayuda_routes._mensajes_validacion) con el
rol ADMINISTRADOR, que ve todas las pantallas. Regenerar cuando cambien los mensajes:
    python -X utf8 docs/scripts/extraer_mensajes_validacion.py --escribir
    docker exec -w /app syscomcli_app python -X utf8 docs/scripts/generar_avisos_seguridad.py
"""
import os
import sys
from html import escape

sys.path.insert(0, os.getcwd())
from app.rutas.ayuda import ayuda_routes as r  # noqa: E402

DESTINO = os.path.join('app', 'rutas', 'ayuda', 'templates', 'ayuda-seguridad-secciones', 'avisos_validacion.html')

secciones, _ = r._armar_manual('ADMINISTRADOR')
tipos = r._mensajes_validacion(secciones, ['ADMINISTRADOR', 'SUPERADMIN'])

html = ['<p>Cuando un dato no cumple una regla, el sistema no lo guarda y muestra un aviso en rojo en la misma pantalla. '
        'Los avisos son de pocos tipos y dicen lo mismo en todas las pantallas. Este capítulo sirve para reconocer un '
        'aviso que le informa un usuario y saber en qué pantallas puede ocurrir. Las capturas de cada aviso están en '
        'la guía de uso (anexo <em>Avisos de validación del sistema</em>).</p>']
for t in tipos:
    html.append(f'<h4>{escape(t["titulo"])}</h4>')
    html.append(f'<p>{escape(t["significa"])}</p>')
    html.append(f'<p><strong>Ejemplo:</strong> {escape(t["ejemplo"])}</p>')
    html.append(f'<p><strong>Qué indicar al usuario:</strong> {escape(t["hacer"])}</p>')
    html.append('<p><strong>Pantallas donde puede ocurrir:</strong></p>')
    html.append('<ul>' + ''.join(f'<li>{escape(i)}</li>' for i in t['lista']) + '</ul>')
html.append('<p>Un aviso que no encaja en ninguno de estos tipos es una regla propia de la pantalla (por ejemplo, una '
            'cita sin turno libre o una caja que no está abierta). Pida al usuario el texto exacto del aviso: '
            'siempre dice qué falta.</p>')
with open(DESTINO, 'w', encoding='utf-8') as f:
    f.write('\n'.join(html) + '\n')
print(f'{len(tipos)} tipos, {len(secciones)} pantallas -> {DESTINO}')
