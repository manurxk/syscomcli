# 🔧 Solución: Filtro de Pacientes por Especialista

## Problema Identificado

Aunque se modificó `PacienteDao.getPacientes()`, había **otros endpoints** que también devuelven pacientes y no estaban filtrando:

1. ✅ `app/rutas/gestionar_personas/paciente/paciente_api.py` - `/api/v1/pacientes` (YA CORREGIDO)
2. ❌ `app/rutas/modulos/cita/cita_api.py` - `/api/v1/pacientes` (CORREGIDO AHORA)
3. ❌ `app/dao/modulos/cita/CitaDao.py` - `getPacientes()` (CORREGIDO AHORA)
4. ❌ `app/dao/gestionar_personas/paciente/PacienteDao.py` - `getPacientesMenores()` (CORREGIDO AHORA)

## Cambios Realizados

### 1. CitaDao.getPacientes() ✅
**Archivo:** `app/dao/modulos/cita/CitaDao.py`

**Cambios:**
- ✅ Agregado import de `especialista_helper`
- ✅ Agregado filtro por especialista usando `paciente_profesional`
- ✅ Admin/Recepcionista ven todos los pacientes
- ✅ Especialistas solo ven sus pacientes asignados

### 2. PacienteDao.getPacientesMenores() ✅
**Archivo:** `app/dao/gestionar_personas/paciente/PacienteDao.py`

**Cambios:**
- ✅ Agregado filtro por especialista usando `paciente_profesional`
- ✅ Admin/Recepcionista ven todos los menores
- ✅ Especialistas solo ven sus pacientes menores asignados

## Verificación

### Paso 1: Verificar que la tabla tiene datos

Ejecuta:
```sql
\i app/codigos_sql/VERIFICAR_FASE_1.sql
```

O manualmente:
```sql
SELECT COUNT(*) FROM paciente_profesional WHERE activo = TRUE;
```

**Debe devolver:** Un número mayor a 0 (las relaciones migradas)

### Paso 2: Verificar que los usuarios tienen relaciones

```sql
-- Ver qué pacientes tiene cada especialista
SELECT 
    e.id_especialista,
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) as especialista,
    COUNT(pp.id_paciente) as total_pacientes
FROM especialistas e
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona
LEFT JOIN paciente_profesional pp ON e.id_especialista = pp.id_especialista AND pp.activo = TRUE
GROUP BY e.id_especialista, pe.per_nombre, pe.per_apellido;
```

### Paso 3: Reiniciar la aplicación

```bash
# Reiniciar Flask para cargar los cambios
```

### Paso 4: Probar con diferentes usuarios

1. **Login como Especialista 1:**
   - Ver lista de pacientes → Debe ver SOLO sus pacientes
   - Ver modal de búsqueda de pacientes → Debe ver SOLO sus pacientes
   - Ver pacientes menores → Debe ver SOLO sus pacientes menores

2. **Login como Especialista 2:**
   - Ver lista de pacientes → Debe ver SOLO sus pacientes (diferentes al Especialista 1)
   - Ver modal de búsqueda → Debe ver SOLO sus pacientes

3. **Login como Admin:**
   - Ver lista de pacientes → Debe ver TODOS los pacientes ✅

4. **Login como Recepcionista:**
   - Ver lista de pacientes → Debe ver TODOS los pacientes ✅

## Si Aún No Funciona

### Verificar que el script SQL se ejecutó:

```sql
-- Verificar que la tabla existe
SELECT * FROM paciente_profesional LIMIT 5;

-- Si no existe, ejecutar:
\i app/codigos_sql/FASE_1_PACIENTE_PROFESIONAL.sql
```

### Verificar que los imports están correctos:

```python
# En CitaDao.py y PacienteDao.py debe estar:
from app.utils.especialista_helper import obtener_id_especialista_usuario, puede_ver_todos_pacientes
```

### Verificar logs de la aplicación:

Si hay errores, revisar:
- ¿Se importa correctamente `especialista_helper`?
- ¿La sesión tiene `id_usuario` y `id_grupo`?
- ¿La tabla `paciente_profesional` tiene datos?

### Debug temporal:

Agregar logs temporales en `getPacientes()`:

```python
def getPacientes(self):
    id_especialista = obtener_id_especialista_usuario()
    puede_ver_todos = puede_ver_todos_pacientes()
    
    app.logger.info(f"DEBUG: id_especialista={id_especialista}, puede_ver_todos={puede_ver_todos}")
    # ... resto del código
```

## Archivos Modificados

- ✅ `app/dao/modulos/cita/CitaDao.py` - `getPacientes()` ahora filtra
- ✅ `app/dao/gestionar_personas/paciente/PacienteDao.py` - `getPacientesMenores()` ahora filtra
- ✅ `app/utils/especialista_helper.py` - Helper creado (ya existía)

## Endpoints Afectados

Todos estos endpoints ahora filtran correctamente:

1. `GET /api/v1/pacientes` - Lista principal de pacientes
2. `GET /api/v1/pacientes/menores` - Lista de pacientes menores
3. `GET /api/v1/citas/pacientes` - Pacientes para modal de citas
4. Cualquier template que use DataTables con `/api/v1/pacientes`

---

**¡Ahora debería funcionar correctamente!** 🎉

Si después de reiniciar y verificar aún no funciona, comparte los logs o errores específicos.


