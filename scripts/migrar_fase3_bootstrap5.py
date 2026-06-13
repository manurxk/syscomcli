#!/usr/bin/env python3
"""
Script para migrar componentes de Bootstrap 4 a Bootstrap 5 (Fase 3)
Migra modals, atributos data-* y JavaScript
"""

import os
import re
from pathlib import Path

# Directorio base del proyecto
PROJECT_ROOT = Path(__file__).parent
RUTAS_DIR = PROJECT_ROOT / 'app' / 'rutas'
TEMPLATES_DIR = PROJECT_ROOT / 'app' / 'templates'

# Patrones de reemplazo
REPLACEMENTS = [
    # Modals - Botón de cierre
    (r'<button\s+type="button"\s+class="close"\s+data-dismiss="modal">\s*&times;\s*</button>',
     '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'),
    
    # Modals - Botón de cierre (variante sin espacios)
    (r'<button\s+type="button"\s+class="close"\s+data-dismiss="modal">&times;</button>',
     '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'),
    
    # Modals - Botón de cierre (variante con comillas simples)
    (r"<button\s+type='button'\s+class='close'\s+data-dismiss='modal'>\s*&times;\s*</button>",
     "<button type='button' class='btn-close' data-bs-dismiss='modal' aria-label='Close'></button>"),
    
    # Atributos data-* en modals
    (r'data-dismiss="modal"', 'data-bs-dismiss="modal"'),
    (r"data-dismiss='modal'", "data-bs-dismiss='modal'"),
    
    # Atributos data-toggle
    (r'data-toggle="', 'data-bs-toggle="'),
    (r"data-toggle='", "data-bs-toggle='"),
    
    # Atributos data-target
    (r'data-target="', 'data-bs-target="'),
    (r"data-target='", "data-bs-target='"),
    
    # Atributos data-backdrop
    (r'data-backdrop="', 'data-bs-backdrop="'),
    (r"data-backdrop='", "data-bs-backdrop='"),
    
    # Atributos data-parent
    (r'data-parent="', 'data-bs-parent="'),
    (r"data-parent='", "data-bs-parent='"),
    
    # JavaScript - API de modals Bootstrap 4 a Bootstrap 5
    # Nota: Estos requieren revisión manual, pero los marcamos
    (r'\$\(["\']#(\w+)["\']\)\.modal\(["\']show["\']\)',
     r'new bootstrap.Modal(document.getElementById("\1")).show()'),
    (r'\$\(["\']#(\w+)["\']\)\.modal\(["\']hide["\']\)',
     r'new bootstrap.Modal(document.getElementById("\1")).hide()'),
    (r'\$\(["\']#(\w+)["\']\)\.modal\(["\']toggle["\']\)',
     r'new bootstrap.Modal(document.getElementById("\1")).toggle()'),
]

def find_html_files(directory):
    """Encuentra todos los archivos HTML en el directorio"""
    html_files = []
    for root, dirs, files in os.walk(directory):
        # Ignorar directorios comunes
        dirs[:] = [d for d in dirs if d not in ['__pycache__', 'node_modules', '.git']]
        for file in files:
            if file.endswith('.html'):
                html_files.append(Path(root) / file)
    return html_files

def migrate_file(file_path):
    """Migra un archivo HTML de Bootstrap 4 a Bootstrap 5"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        changes_made = []
        
        # Aplicar todos los reemplazos
        for pattern, replacement in REPLACEMENTS:
            new_content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
            if new_content != content:
                changes_made.append(f"  - {pattern[:50]}...")
                content = new_content
        
        # Solo escribir si hubo cambios
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, changes_made
        else:
            return False, []
    
    except Exception as e:
        print(f"❌ Error procesando {file_path}: {e}")
        return False, []

def main():
    """Función principal"""
    print("=" * 80)
    print("MIGRACIÓN FASE 3: Bootstrap 4 → Bootstrap 5")
    print("=" * 80)
    print()
    
    # Encontrar todos los archivos HTML
    html_files = []
    if RUTAS_DIR.exists():
        html_files.extend(find_html_files(RUTAS_DIR))
    if TEMPLATES_DIR.exists():
        html_files.extend(find_html_files(TEMPLATES_DIR))
    
    # Excluir base.html e inicio.html (ya migrados)
    html_files = [f for f in html_files if f.name not in ['base.html', 'inicio.html', 'login.html']]
    
    print(f"📁 Encontrados {len(html_files)} archivos HTML para migrar\n")
    
    # Procesar cada archivo
    migrated_count = 0
    total_changes = 0
    
    for file_path in html_files:
        rel_path = file_path.relative_to(PROJECT_ROOT)
        changed, changes = migrate_file(file_path)
        
        if changed:
            migrated_count += 1
            total_changes += len(changes)
            print(f"✅ Migrado: {rel_path}")
            if changes:
                for change in changes[:3]:  # Mostrar solo los primeros 3 cambios
                    print(change)
                if len(changes) > 3:
                    print(f"  ... y {len(changes) - 3} cambios más")
    
    print()
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"📊 Archivos procesados: {len(html_files)}")
    print(f"✅ Archivos migrados: {migrated_count}")
    print(f"📝 Total de cambios: {total_changes}")
    print(f"⚪ Archivos sin cambios: {len(html_files) - migrated_count}")
    print()
    print("⚠️  IMPORTANTE: Revisar manualmente los cambios en JavaScript")
    print("   especialmente los que usan la API de modals de Bootstrap")
    print("=" * 80)

if __name__ == '__main__':
    main()



