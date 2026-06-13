import os
import re

def migrate_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Cambiar bg-primary de card-header a transparente/limpio
    content = content.replace('card-header bg-primary text-white', 'card-header')
    
    # 2. Estandarizar botón "Agregar" en el header
    # Busca <button ... id="btnAgregar" ...>Agregar</button>
    content = re.sub(
        r'<button type="button" class="btn btn-primary" id="btnAgregar">Agregar</button>',
        r'<button class="btn btn-sm btn-primary shadow-sm" type="button" id="btnAgregar"><i class="fas fa-plus fa-sm text-white-50"></i> Agregar</button>',
        content
    )

    # 3. Mapeo de Badges a versión "soft" de SB Admin Pro
    content = content.replace('badge badge-success', 'badge bg-success-soft text-success')
    content = content.replace('badge badge-secondary', 'badge bg-secondary-soft text-secondary')
    content = content.replace('badge badge-danger', 'badge bg-danger-soft text-danger')
    content = content.replace('badge badge-info', 'badge bg-info-soft text-info')
    content = content.replace('badge badge-warning', 'badge bg-warning-soft text-warning')

    # 4. Botones de Acción en Tablas (DataTables)
    def clean_and_format_button(match):
        attrs = match.group(1)
        text = match.group(2)
        
        # Mapeo de iconos por name
        icons = {
            'btn_editar': 'fa-edit',
            'btn_eliminar': 'fa-trash-alt',
            'btn_ver': 'fa-eye',
            'btn_pdf': 'fa-file-pdf',
            'btn_imprimir': 'fa-print',
            'btn_resetear': 'fa-redo',
            'btn_desactivar': 'fa-ban',
            'btn_consultar': 'fa-search'
        }
        
        btn_name = re.search(r'name="(btn_[a-z_]+)"', attrs)
        btn_key = btn_name.group(1) if btn_name else ""
        icon = icons.get(btn_key, 'fa-external-link-alt')
        
        # Limpiar clases previas
        attrs = re.sub(r'class="[^"]+"', '', attrs).strip()
        # Limpiar espacios extra
        attrs = re.sub(r'\s+', ' ', attrs)
        
        margin = "me-2" if btn_key != list(icons.keys())[-1] else "" # Simplificación
        
        return f'<button class="btn btn-datatable btn-icon btn-transparent-dark {margin}" {attrs}><i class="fas {icon}"></i></button>'

    # Reemplazo potente para botones de acción conocidos (manejando saltos de línea)
    content = re.sub(
        r'<button\s+([^>]*name="btn_(?:editar|eliminar|ver|pdf|imprimir|resetear|desactivar|consultar)"[^>]*)>(.*?)</button>',
        clean_and_format_button,
        content,
        flags=re.DOTALL
    )






    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    base_path = '/home/armando/Documentos/PERSONAL/GIT/Angasys/app/rutas'
    files_migrated = 0
    
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('-index.html'):
                filepath = os.path.join(root, file)
                print(f"Migrando: {filepath}")
                migrate_file(filepath)
                files_migrated += 1
                
    print(f"\nFinalizado. Se migraron {files_migrated} archivos.")

if __name__ == "__main__":
    main()
