# Especificación de Caso de Uso: {{Nombre del CU}}

> Verificado contra código el {{fecha}} — archivo(s): `{{ruta/al/Dao.py}}`, `{{ruta/al/api.py}}`

## 1. Resumen
{{1-2 frases: qué hace este CU y para qué módulo/entidad del sistema}}

## 2. Actores relacionados
- {{Rol, ej. Recepcionista / Especialista / Cajero / Administrador}}

## 3. Precondiciones
- El usuario debe poseer el perfil de {{rol}}.
- El caso de uso Autenticar debe haber sido ejecutado con éxito.
- {{otras precondiciones de datos, ej. "debe existir al menos un paciente registrado"}}

## 4. Flujo de eventos

### 4.1 Flujo básico — Alta
1. El usuario selecciona la opción "{{Nombre del CU}}" en el menú.
2. El usuario presiona el botón "Agregar".
3. El sistema muestra el formulario correspondiente.
4. El usuario carga los datos: {{lista de campos reales, tomados del formulario/DAO}}.
5. El usuario confirma presionando "Guardar".
6. El sistema valida los datos ({{reglas de validación reales — únicos, obligatorios, formato}}).
7. El sistema persiste el registro en la base de datos.
8. El sistema muestra mensaje de confirmación.

### 4.2 Flujo básico — Baja (borrado lógico)
1. El usuario selecciona el registro de la lista.
2. El usuario presiona "Eliminar" / "Desactivar".
3. El sistema solicita confirmación.
4. El sistema marca el registro como inactivo (`estado = false` / equivalente) — no elimina físicamente.

### 4.3 Flujo básico — Modificación
1. El usuario selecciona el registro a modificar.
2. El sistema carga los datos actuales en el formulario.
3. El usuario modifica los campos necesarios.
4. El usuario confirma presionando "Guardar".
5. El sistema valida y persiste los cambios.

### 4.4 Flujo alternativo
- Si el usuario presiona "Cancelar", el formulario se limpia sin persistir cambios.
- Si la validación falla, el sistema muestra un mensaje de error y no persiste el registro.
- {{casos alternativos específicos de esta entidad, ej. "si ya existe una cita en ese horario, el sistema rechaza el alta"}}

## 5. Postcondiciones
- Si el caso de uso se ejecuta con éxito, el registro persiste en la base de datos.
- {{postcondiciones específicas, ej. "la agenda del especialista queda actualizada"}}

## 6. Lista de archivos (campos reales del modelo)

| Campo | Columna en BD | Obligatorio | Notas |
|---|---|---|---|
| {{campo}} | {{columna}} | {{sí/no}} | {{validación/observación}} |

## 7. Referencias de código
- DAO: `{{ruta}}`
- Rutas/API: `{{ruta}}`
- Plantilla HTML: `{{ruta}}`
