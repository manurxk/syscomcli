import os
import shutil
from pathlib import Path

BASE_DIR = Path(r"C:\Users\MANUEL RAMIREZ\Documents\clausys\app")

maps_modulos = {
    'agenda_medica': 'agendamiento/agenda_medica',
    'cita': 'agendamiento/cita',
    'recordatorio': 'agendamiento/recordatorio',
    'mi_agenda': 'agendamiento/mi_agenda',

    'consulta': 'consultorio/consulta',
    'consulta_unificada': 'consultorio/consulta_unificada',
    'ficha': 'consultorio/ficha',
    'receta': 'consultorio/receta',
    'certificado_medico': 'consultorio/certificado_medico',
    'orden_estudio': 'consultorio/orden_estudio',
    'derivacion': 'consultorio/derivacion',

    'presupuesto': 'ventas/presupuesto',
    'insumo': 'ventas/insumo',
}

maps_referenciales_dao = {
    'especialidad': 'agendamiento/especialidad',
    'consultorio': 'agendamiento/consultorio',
    'dia': 'agendamiento/dia',
    'feriado': 'agendamiento/feriado',
    
    'diagnostico': 'consultorio/diagnostico',
    'medicamento': 'consultorio/medicamento',
    'signo': 'consultorio/signo',
    'sintoma': 'consultorio/sintoma',
    'tipo_analisis': 'consultorio/tipo_analisis',
    'tipo_estudio': 'consultorio/tipo_estudio',
    'tipo_procedimiento': 'consultorio/tipo_procedimiento',
    'tipo_tratamiento': 'consultorio/tipo_tratamiento',
    'tipo_certificado_medico': 'consultorio/tipo_certificado_medico',
    
    'timbrado': 'ventas/timbrado',
    'establecimiento': 'ventas/establecimiento',
    'punto_expedicion': 'ventas/punto_expedicion',
    'empresa': 'ventas/empresa',
    'sede': 'ventas/sede',
    
    'ciudad': 'generales/ciudad',
    'genero': 'generales/genero',
    'estado_civil': 'generales/estado_civil',
    'nivel_instruccion': 'generales/nivel_instruccion',
    'profesion': 'generales/profesion',
    'cargo': 'generales/cargo',
    'grupo': 'generales/grupo',
    'modulo': 'generales/modulo',
    'usuario': 'generales/usuario',
}

maps_referenciales_rutas = maps_referenciales_dao.copy()
maps_referenciales_rutas.pop('profesion', None)
maps_referenciales_rutas['ocupacion'] = 'generales/ocupacion'

def move_folders(base_path, mapping):
    for src_name, dest_rel_path in mapping.items():
        src_path = base_path / src_name
        dest_path = base_path / dest_rel_path
        if src_path.exists() and src_path.is_dir():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            # Create __init__.py in the parent directory
            init_file = dest_path.parent / '__init__.py'
            if not init_file.exists():
                init_file.touch()
                
            if not dest_path.exists():
                print(f"Moving {src_path} -> {dest_path}")
                shutil.move(str(src_path), str(dest_path))
            else:
                print(f"Target {dest_path} already exists, skipping move.")

print("--- MOVING FOLDERS ---")
move_folders(BASE_DIR / 'dao' / 'modulos', maps_modulos)
move_folders(BASE_DIR / 'rutas' / 'modulos', maps_modulos)
move_folders(BASE_DIR / 'dao' / 'referenciales', maps_referenciales_dao)
move_folders(BASE_DIR / 'rutas' / 'referenciales', maps_referenciales_rutas)

print("--- UPDATING FILES ---")
replacements = []

for k, v in maps_modulos.items():
    v_dot = v.replace('/', '.')
    replacements.append((f"app.dao.modulos.{k}", f"app.dao.modulos.{v_dot}"))
    replacements.append((f"app.rutas.modulos.{k}", f"app.rutas.modulos.{v_dot}"))

for k, v in maps_referenciales_dao.items():
    v_dot = v.replace('/', '.')
    replacements.append((f"app.dao.referenciales.{k}", f"app.dao.referenciales.{v_dot}"))

for k, v in maps_referenciales_rutas.items():
    v_dot = v.replace('/', '.')
    replacements.append((f"app.rutas.referenciales.{k}", f"app.rutas.referenciales.{v_dot}"))

# Additional specific replacements in blueprints.py url_prefixes if needed 
# But let's verify if that's required. The prompt just says refactor folders.
# Let's keep URL prefixes the same by only replacing the python module paths.

print(f"Total replacement string pairs configured: {len(replacements)}")

updated_files = 0
for py_file in BASE_DIR.rglob('*.py'):
    if '__pycache__' in py_file.parts or '.venv' in py_file.parts:
        continue
    
    try:
        content = py_file.read_text(encoding='utf-8')
    except Exception as e:
        continue
        
    new_content = content
    for old_str, new_str in replacements:
        if old_str in new_content:
            new_content = new_content.replace(old_str + '.', new_str + '.')
            new_content = new_content.replace(old_str + ' ', new_str + ' ')
            # for "from app.dao.modulos.cita import"
            new_content = new_content.replace(old_str + '\n', new_str + '\n')

    if new_content != content:
        print(f"Updated imports in {py_file.name}")
        py_file.write_text(new_content, encoding='utf-8')
        updated_files += 1

print(f"Refactoring completed. Updated {updated_files} files.")
