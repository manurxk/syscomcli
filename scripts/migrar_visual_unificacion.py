import os
import re

def migrate_buttons(directory):
    # Regex para encontrar botones con clase close
    # Busca <button ... class="...close..." ...>...</button>
    button_re = re.compile(r'(<button[^>]*class="([^"]*)\bclose\b([^"]*)"[^>]*>)(.*?)(</button>)', re.DOTALL)
    
    # Regex para limpiar &times; y contenido similar
    times_re = re.compile(r'(&times;|<span>\s*&times;\s*</span>)', re.IGNORECASE)

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = content
                
                def replace_button(match):
                    full_open_tag = match.group(1)
                    class_before = match.group(2)
                    class_after = match.group(3)
                    inner_content = match.group(4)
                    close_tag = match.group(5)
                    
                    # Determinar si necesita btn-close-white
                    is_white = 'text-white' in class_before or 'text-white' in class_after
                    
                    new_classes = class_before + 'btn-close' + class_after
                    if is_white:
                        new_classes = new_classes.replace('text-white', 'btn-close-white')
                    else:
                        # Si no era white, nos aseguramos que no quede text-white residual
                        pass
                    
                    # Limpiar espacios dobles
                    new_classes = ' '.join(new_classes.split())
                    
                    # Construir el nuevo tag de apertura
                    # Reemplazamos la clase vieja por la nueva en el tag original
                    new_open_tag = full_open_tag.replace(match.group(2) + 'close' + match.group(3), new_classes)
                    
                    # Agregar aria-label si no existe
                    if 'aria-label' not in new_open_tag:
                        new_open_tag = new_open_tag.replace('>', ' aria-label="Close">')
                    
                    # El contenido interno debe ser vaciado si era solo &times;
                    if times_re.search(inner_content) or not inner_content.strip():
                        return f'{new_open_tag}{close_tag}'
                    else:
                        # Si tiene otro contenido, lo dejamos (podría ser un texto "Cerrar")
                        # Pero removemos el &times; si existe
                        cleaned_inner = times_re.sub('', inner_content)
                        return f'{new_open_tag}{cleaned_inner}{close_tag}'

                new_content = button_re.sub(replace_button, content)
                
                if new_content != content:
                    print(f"Migrando: {path}")
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

if __name__ == "__main__":
    migrate_buttons('app/rutas')
    migrate_buttons('app/templates')
