# 🔍 Debug: Filtro de Pacientes

## Pasos para Debuggear

### 1. Verificar Logs de la Aplicación

Después de reiniciar la aplicación, cuando un especialista acceda a la lista de pacientes, deberías ver en los logs algo como:

```
DEBUG especialista_helper: grupo_id=3, usuario_id=X
DEBUG puede_ver_todos_pacientes: grupo_id=3, puede_ver=False
DEBUG especialista_helper: id_especialista encontrado=Y
DEBUG PacienteDao.getPacientes: puede_ver_todos=False
DEBUG PacienteDao.getPacientes: id_especialista=Y
```

### 2. Verificar Sesión del Usuario

Agrega temporalmente en cualquier ruta que devuelva pacientes:

```python
@app.route('/debug-sesion')
def debug_sesion():
    return jsonify({
        'id_usuario': session.get('id_usuario'),
        'id_grupo': session.get('id_grupo'),
        'grupo': session.get('grupo'),
        'sesion_completa': dict(session)
    })
```

Luego accede a `/debug-sesion` cuando estés logueado como especialista.

### 3. Verificar Query SQL Generada

Agrega temporalmente en `PacienteDao.getPacientes()`:

```python
app.logger.info(f"DEBUG SQL generada: {pacienteSQL}")
if id_especialista:
    app.logger.info(f"DEBUG Parámetros: id_especialista={id_especialista}")
```

### 4. Verificar Datos en Base de Datos

Ejecuta estas consultas:

```sql
-- Ver qué especialistas existen
SELECT 
    e.id_especialista,
    f.id_usuario,
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) as nombre_especialista
FROM especialistas e
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona;

-- Ver relaciones paciente_profesional
SELECT 
    pp.id_paciente_profesional,
    pp.id_paciente,
    pp.id_especialista,
    pp.activo,
    CONCAT(per.per_nombre, ' ', per.per_apellido) as nombre_paciente,
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) as nombre_especialista
FROM paciente_profesional pp
JOIN pacientes p ON pp.id_paciente = p.id_paciente
JOIN personas per ON p.id_persona = per.id_persona
JOIN especialistas e ON pp.id_especialista = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona
WHERE pp.activo = TRUE;
```

### 5. Probar Query Manualmente

Ejecuta esta query reemplazando `X` con el `id_especialista` del usuario:

```sql
SELECT DISTINCT
    pac.id_paciente,
    pac.pac_historia_clinica,
    p.per_nombre,
    p.per_apellido
FROM pacientes pac
JOIN personas p ON pac.id_persona = p.id_persona
INNER JOIN paciente_profesional pp ON pac.id_paciente = pp.id_paciente
WHERE pp.id_especialista = X AND pp.activo = TRUE
ORDER BY pac.id_paciente DESC;
```

**Si esta query devuelve los pacientes correctos, el problema está en el código Python.**
**Si no devuelve nada, el problema está en los datos de `paciente_profesional`.**

## Posibles Problemas y Soluciones

### Problema 1: La sesión no tiene `id_usuario` o `id_grupo`

**Solución:** Verificar que el login guarda correctamente estos valores.

### Problema 2: El usuario no tiene `id_especialista` asociado

**Solución:** Verificar que el usuario tiene un funcionario y ese funcionario tiene un especialista:

```sql
SELECT 
    u.id_usuario,
    u.usu_nick,
    f.id_funcionario,
    e.id_especialista
FROM usuarios u
LEFT JOIN funcionarios f ON u.id_funcionario = f.id_funcionario
LEFT JOIN especialistas e ON f.id_funcionario = e.id_funcionario
WHERE u.id_usuario = X;  -- Reemplazar X con el id_usuario
```

### Problema 3: Los pacientes no están asignados al especialista

**Solución:** Verificar que existen relaciones en `paciente_profesional`:

```sql
SELECT COUNT(*) 
FROM paciente_profesional 
WHERE id_especialista = X AND activo = TRUE;
```

Si devuelve 0, ejecutar nuevamente el script de migración.

### Problema 4: La aplicación no se reinició

**Solución:** Reiniciar completamente la aplicación Flask.

---

**Comparte los logs y resultados de estas verificaciones para identificar el problema exacto.**


