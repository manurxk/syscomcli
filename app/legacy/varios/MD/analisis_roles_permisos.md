# Análisis: Sistema de Roles y Permisos - Jerarquía de Usuarios

## Situación Actual

El sistema actualmente maneja los siguientes roles/grupos:
- **Administrador** (id_grupo = 1)
- **Recepcionista**
- **Especialista**
- **Ventas**

Cada usuario tiene un único `id_grupo` asignado que determina sus permisos en el sistema.

---

## Requerimientos Identificados

### 1. Necesidad de un Superadministrador

**Requerimiento:**
- Crear un nuevo rol **Superadministrador** con acceso total
- Solo el Superadministrador puede:
  - Crear nuevos usuarios en el sistema
  - Asignar el rol de **Administrador** a otros usuarios
- El Administrador (director de la clínica) puede:
  - Asignar roles de: Especialista, Recepcionista y Ventas
  - **NO** puede crear nuevos administradores
  - **NO** puede crear nuevos usuarios (solo el Superadministrador)

### 2. Situación de Roles Múltiples

**Problema identificado:**
- ¿Qué pasa si un Administrador también es Especialista?
- ¿Qué pasa si una Recepcionista también tiene cargo de Ventas?

Esto requiere un sistema que permita **múltiples roles por usuario**.

---

## Propuestas de Solución

### Opción 1: Sistema de Roles Múltiples con Tabla de Relación (RECOMENDADA)

#### Estructura de Base de Datos

**Tabla: `usuarios_roles` (nueva)**
```sql
CREATE TABLE usuarios_roles (
    id_usuario_rol SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario),
    id_grupo INTEGER NOT NULL REFERENCES grupos(id_grupo),
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(id_usuario, id_grupo)
);
```

**Modificaciones a la tabla `usuarios`:**
- Mantener `id_grupo` como **rol principal** (para compatibilidad)
- O eliminar `id_grupo` y usar solo la tabla de relación

#### Jerarquía de Roles

1. **Superadministrador** (id_grupo = 0 o nuevo ID)
   - Acceso total al sistema
   - Único que puede crear usuarios
   - Único que puede asignar rol de Administrador

2. **Administrador** (id_grupo = 1)
   - Puede asignar roles: Especialista, Recepcionista, Ventas
   - NO puede crear usuarios
   - NO puede asignar rol de Administrador

3. **Especialista** (id_grupo = 2)
4. **Recepcionista** (id_grupo = 3)
5. **Ventas** (id_grupo = 4)

#### Ventajas
- ✅ Permite múltiples roles por usuario
- ✅ Flexible y escalable
- ✅ Mantiene compatibilidad con sistema actual
- ✅ Permite auditoría de asignación de roles

#### Desventajas
- ⚠️ Requiere cambios en la lógica de permisos
- ⚠️ Más complejo de implementar

---

### Opción 2: Sistema de Roles Simples con Validación de Jerarquía

#### Estructura
- Mantener un solo `id_grupo` por usuario
- Agregar validaciones en el código para:
  - Solo Superadministrador puede crear usuarios
  - Solo Superadministrador puede asignar Administrador
  - Administrador puede asignar: Especialista, Recepcionista, Ventas

#### Ventajas
- ✅ Más simple de implementar
- ✅ Menos cambios en la base de datos
- ✅ Compatible con sistema actual

#### Desventajas
- ❌ NO resuelve el problema de roles múltiples
- ❌ Un usuario no puede ser Administrador Y Especialista simultáneamente

---

### Opción 3: Sistema Híbrido - Roles Principales + Roles Secundarios

#### Estructura
- Mantener `id_grupo` en `usuarios` como **rol principal**
- Agregar tabla `usuarios_roles_secundarios` para roles adicionales
- Los permisos se calculan como: `permisos_rol_principal OR permisos_roles_secundarios`

#### Ventajas
- ✅ Permite roles múltiples
- ✅ Mantiene compatibilidad
- ✅ Rol principal claro

#### Desventajas
- ⚠️ Puede ser confuso qué rol es "principal"
- ⚠️ Lógica de permisos más compleja

---

## Recomendación: Opción 1 (Sistema de Roles Múltiples)

### Implementación Propuesta

#### 1. Crear nuevo grupo: Superadministrador
```sql
INSERT INTO grupos (des_grupo, est_grupo) 
VALUES ('Superadministrador', TRUE);
-- Asumir que obtiene id_grupo = 0 o el siguiente disponible
```

#### 2. Crear tabla de relación usuarios_roles
```sql
CREATE TABLE usuarios_roles (
    id_usuario_rol SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_grupo INTEGER NOT NULL REFERENCES grupos(id_grupo) ON DELETE CASCADE,
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER REFERENCES usuarios(id_usuario),
    UNIQUE(id_usuario, id_grupo)
);

CREATE INDEX idx_usuarios_roles_usuario ON usuarios_roles(id_usuario);
CREATE INDEX idx_usuarios_roles_grupo ON usuarios_roles(id_grupo);
```

#### 3. Migración de datos existentes
```sql
-- Migrar usuarios existentes a la nueva tabla
INSERT INTO usuarios_roles (id_usuario, id_grupo, es_rol_principal, activo)
SELECT id_usuario, id_grupo, TRUE, usu_estado
FROM usuarios
WHERE id_grupo IS NOT NULL;
```

#### 4. Lógica de Permisos (ACTUALIZADA según decisiones)

**Jerarquía de Roles (orden de prioridad)**:
1. Superadministrador (mayor rango)
2. Administrador
3. Especialista
4. Recepcionista
5. Ventas (menor rango)

**Función: `obtener_permisos_usuario(id_usuario)`**
- Obtiene todos los `id_grupo` activos del usuario desde `usuarios_roles`
- Si tiene Superadministrador → acceso total (bypass de permisos)
- Si tiene múltiples roles → se usa el rol de MAYOR RANGO para permisos críticos
- Para permisos generales → UNION de permisos de todos los roles activos
- El rol principal se usa principalmente para UI/display

**Función: `obtener_rol_mayor_rango(id_usuario)`**
```python
def obtener_rol_mayor_rango(id_usuario):
    """
    Retorna el rol de mayor jerarquía del usuario
    Orden: Superadministrador > Administrador > Especialista > Recepcionista > Ventas
    """
    roles = obtener_roles_usuario(id_usuario)
    jerarquia = {
        'Superadministrador': 5,
        'Administrador': 4,
        'Especialista': 3,
        'Recepcionista': 2,
        'Ventas': 1
    }
    
    rol_mayor = None
    rango_mayor = 0
    
    for rol in roles:
        rango = jerarquia.get(rol['des_grupo'], 0)
        if rango > rango_mayor:
            rango_mayor = rango
            rol_mayor = rol
    
    return rol_mayor
```

**Función: `puede_asignar_rol(usuario_actual, rol_a_asignar)`**
```python
def puede_asignar_rol(id_usuario_actual, id_grupo_a_asignar):
    """
    Determina si un usuario puede asignar un rol específico
    Basado en el rol de MAYOR RANGO del usuario actual
    """
    rol_mayor = obtener_rol_mayor_rango(id_usuario_actual)
    
    if not rol_mayor:
        return False
    
    grupo_nombre = rol_mayor['des_grupo']
    
    # Superadministrador puede asignar cualquier rol
    if grupo_nombre == 'Superadministrador':
        return True
    
    # Administrador solo puede asignar roles menores
    if grupo_nombre == 'Administrador':
        roles_permitidos = ['Especialista', 'Recepcionista', 'Ventas']
        grupo = obtener_grupo_por_id(id_grupo_a_asignar)
        return grupo['des_grupo'] in roles_permitidos
    
    return False
```

**Función: `puede_crear_usuario(id_usuario_actual)`**
```python
def puede_crear_usuario(id_usuario_actual):
    """
    Solo el Superadministrador puede crear usuarios
    El Administrador puede crear funcionarios pero NO usuarios
    """
    rol_mayor = obtener_rol_mayor_rango(id_usuario_actual)
    return rol_mayor and rol_mayor['des_grupo'] == 'Superadministrador'
```

**Función: `validar_roles_usuario(id_usuario, roles)`**
```python
def validar_roles_usuario(id_usuario, roles):
    """
    Valida que el usuario tenga:
    - Máximo 3 roles
    - Mínimo 1 rol activo
    """
    if len(roles) > 3:
        return False, "Un usuario no puede tener más de 3 roles simultáneos"
    
    roles_activos = [r for r in roles if r.get('activo', True)]
    if len(roles_activos) == 0:
        return False, "Un usuario debe tener al menos 1 rol activo"
    
    return True, None
```

#### 5. Modificaciones en el Código

**En `app/auth/dao/user_dao.py`:**
- Agregar método `obtener_roles_usuario(id_usuario)`
- Agregar método `asignar_rol_usuario(id_usuario, id_grupo, es_principal=False)`
- Agregar método `remover_rol_usuario(id_usuario, id_grupo)`
- Modificar `guardarUsuario()` para validar permisos

**En `app/rutas/seguridad/usuario/usuario_api.py`:**
- Agregar validación en `addUsuario()`:
  ```python
  if not puede_crear_usuario(session.get('id_usuario')):
      return jsonify({'error': 'Solo el Superadministrador puede crear usuarios'}), 403
  ```
- Agregar validación al asignar roles:
  ```python
  if not puede_asignar_rol(session.get('id_usuario'), data['id_grupo']):
      return jsonify({'error': 'No tienes permiso para asignar este rol'}), 403
  ```

**En `app/dao/referenciales/usuario/permisos_dao.py`:**
- Modificar `obtener_permisos_grupo()` para aceptar múltiples grupos
- Crear `obtener_permisos_usuario(id_usuario)` que consolida permisos de todos sus roles

**En `app/utils/decorators.py`:**
- Modificar `require_group()` para verificar si el usuario tiene AL MENOS UNO de los roles requeridos
- Crear `require_superadmin()` para rutas exclusivas de Superadministrador

---

## Casos de Uso Resueltos

### Caso 1: Administrador que también es Especialista
```python
# Usuario con ID 5 es Administrador y Especialista
asignar_rol_usuario(id_usuario=5, id_grupo=1, es_rol_principal=True)  # Administrador
asignar_rol_usuario(id_usuario=5, id_grupo=2, es_rol_principal=False)  # Especialista

# Permisos: UNION de permisos de Administrador + Especialista
```

### Caso 2: Recepcionista que también tiene Ventas
```python
# Usuario con ID 10 es Recepcionista y Ventas
asignar_rol_usuario(id_usuario=10, id_grupo=3, es_rol_principal=True)  # Recepcionista
asignar_rol_usuario(id_usuario=10, id_grupo=4, es_rol_principal=False)  # Ventas

# Permisos: UNION de permisos de Recepcionista + Ventas
```

### Caso 3: Creación de Usuario
```python
# Solo Superadministrador puede ejecutar esto
if puede_crear_usuario(usuario_actual):
    nuevo_usuario = guardarUsuario(...)
    # Luego asignar roles según quién lo crea:
    if es_superadmin(usuario_actual):
        # Puede asignar cualquier rol
        asignar_rol_usuario(nuevo_usuario, id_grupo_deseado)
    elif es_administrador(usuario_actual):
        # Solo puede asignar roles menores
        if id_grupo_deseado in [2, 3, 4]:  # Especialista, Recepcionista, Ventas
            asignar_rol_usuario(nuevo_usuario, id_grupo_deseado)
```

---

## Preguntas para Clarificar

1. **¿El Superadministrador debe poder asignarse a sí mismo otros roles?**
   - Por ejemplo, ¿puede un Superadministrador también ser Especialista?
   la idea es que el superadministrador maneje todo los datos tipo yo como pregramador accedo a ese usuario y pudo ver todos lso detalles refefrente a la clinica su funcionamiento y crear el usuario, como tal el adminsitrador  puede crear funcioanrio como especialista y de mas pero solo yo como superadministrador le voy a crear un usurio y contaselña

2. **¿Un Administrador puede tener múltiples roles?**
   - Por ejemplo, ¿puede ser Administrador + Especialista + Ventas?
   podria seer en teoria ela dministrador ya tendria su propio panel entonces si  podria ver todo en este caso me enfoco solo adminsitadrod r y especilista pero si en algun moento debera tener ese acceso 

3. **¿Los permisos se suman (UNION) o se toman del rol más alto?**
   - Si un usuario es Administrador + Especialista, ¿tiene permisos de ambos o solo del más alto?
la idea es que se tome ponele el primer grupo yo como administrador esd m,i primera asigancion y el siguiente es especvilsita  pero solo wsudcedera con la administradora la mayuoria solo tendra un solo rol
4. **¿Qué pasa si se elimina el rol principal de un usuario?**
   - ¿Se debe elegir automáticamente otro rol como principal?
no necesariamiente eliminar pero si deberia de tener solo 1 minimo como un grupo activo, y si no tieen ningun grupo se debera de marcar como desactivado
5. **¿Necesitas auditoría de quién asignó cada rol?**
   - El campo `asignado_por` en la tabla `usuarios_roles` permite esto.
si es lo correcto  ya que solo el superadministrator y administrasor que van a ser los que asigen
6. **¿El Superadministrador puede desactivar/eliminar a otros Superadministradores?**
   - ¿O debe haber al menos uno siempre activo?
solo va a ver un usuario superadministrador la idea es crear el super usuario desde la bd nada mas
7. **¿Los roles tienen prioridad/orden?**
   - Por ejemplo, si hay conflicto de permisos, ¿cuál prevalece?
el de mayor ango seria lo correcto
8. **¿Necesitas un límite de roles por usuario?**
   - Por ejemplo, máximo 3 roles simultáneos.
   el de tres maximo esta bien 
---

## Resumen de Decisiones Tomadas

Basado en tus respuestas, estas son las decisiones clave:

1. **Superadministrador**: 
   - Solo habrá UN usuario Superadministrador (creado manualmente desde BD)
   - Solo él puede crear usuarios y contraseñas
   - El Administrador puede crear funcionarios pero NO usuarios

2. **Roles Múltiples**:
   - Administrador puede tener múltiples roles (principalmente Admin + Especialista)
   - Máximo 3 roles simultáneos por usuario
   - La mayoría de usuarios tendrá solo 1 rol

3. **Permisos**:
   - Se toma el rol principal (primera asignación)
   - Si hay múltiples roles, prevalece el de mayor rango
   - Jerarquía: Superadministrador > Administrador > Especialista > Recepcionista > Ventas

4. **Validaciones**:
   - Mínimo 1 rol activo por usuario
   - Si un usuario no tiene ningún rol activo, se marca como desactivado
   - Auditoría completa con campo `asignado_por`

---

## Plan de Implementación en 3 Fases

### FASE 1: Base de Datos y Estructura (FUNDACIÓN)

**Objetivo**: Preparar la estructura de BD sin romper el sistema actual

#### 1.1 Crear grupo Superadministrador
```sql
-- Verificar si ya existe
SELECT id_grupo FROM grupos WHERE LOWER(des_grupo) = 'superadministrador';

-- Si no existe, crearlo
INSERT INTO grupos (des_grupo, est_grupo) 
VALUES ('Superadministrador', TRUE)
RETURNING id_grupo;
```

#### 1.2 Crear tabla usuarios_roles
```sql
CREATE TABLE IF NOT EXISTS usuarios_roles (
    id_usuario_rol SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL REFERENCES usuarios(id_usuario) ON DELETE CASCADE,
    id_grupo INTEGER NOT NULL REFERENCES grupos(id_grupo) ON DELETE CASCADE,
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER REFERENCES usuarios(id_usuario),
    UNIQUE(id_usuario, id_grupo)
);

-- Índices para optimización
CREATE INDEX idx_usuarios_roles_usuario ON usuarios_roles(id_usuario);
CREATE INDEX idx_usuarios_roles_grupo ON usuarios_roles(id_grupo);
CREATE INDEX idx_usuarios_roles_activo ON usuarios_roles(id_usuario, activo) WHERE activo = TRUE;
```

#### 1.3 Migrar datos existentes
```sql
-- Migrar todos los usuarios actuales a la nueva tabla
INSERT INTO usuarios_roles (id_usuario, id_grupo, es_rol_principal, activo, asignado_por)
SELECT 
    id_usuario, 
    id_grupo, 
    TRUE,  -- Todos los roles actuales son principales
    usu_estado,  -- Estado del usuario
    1  -- Asignado por sistema (o NULL si prefieres)
FROM usuarios
WHERE id_grupo IS NOT NULL
ON CONFLICT (id_usuario, id_grupo) DO NOTHING;
```

#### 1.4 Crear usuario Superadministrador (MANUAL)
```sql
-- PASO 1: Crear funcionario para el superadmin (si no existe)
-- PASO 2: Crear usuario superadministrador
-- PASO 3: Asignar rol de Superadministrador

-- Ejemplo (ajustar según tu estructura):
-- INSERT INTO usuarios (usu_nick, usu_clave, id_funcionario, id_grupo, usu_estado, ...)
-- VALUES ('superadmin', 'hash_de_contraseña', id_funcionario, id_grupo_superadmin, TRUE, ...);

-- Luego asignar en usuarios_roles:
-- INSERT INTO usuarios_roles (id_usuario, id_grupo, es_rol_principal, activo)
-- VALUES (id_usuario_superadmin, id_grupo_superadmin, TRUE, TRUE);
```

**Entregables Fase 1**:
- ✅ Tabla `usuarios_roles` creada
- ✅ Grupo "Superadministrador" creado
- ✅ Datos migrados
- ✅ Usuario Superadministrador creado manualmente

---

### FASE 2: Backend - Lógica y Validaciones (CORE)

**Objetivo**: Implementar toda la lógica de roles múltiples y validaciones

#### 2.1 Crear servicio de roles (`app/services/roles_service.py`)
- `obtener_roles_usuario(id_usuario)` - Obtiene todos los roles activos
- `obtener_rol_principal(id_usuario)` - Obtiene el rol principal
- `obtener_rol_mayor_rango(id_usuario)` - Obtiene el rol de mayor jerarquía
- `puede_asignar_rol(usuario_actual, rol_a_asignar)` - Validación de permisos
- `puede_crear_usuario(usuario_actual)` - Solo Superadministrador
- `validar_roles_usuario(id_usuario, roles)` - Validar máximo 3 roles, mínimo 1
- `asignar_rol_usuario(id_usuario, id_grupo, es_principal, asignado_por)`
- `remover_rol_usuario(id_usuario, id_grupo)`
- `desactivar_usuario_sin_roles(id_usuario)` - Si no tiene roles activos

#### 2.2 Extender UsuarioDao (`app/auth/dao/user_dao.py`)
- Agregar métodos para manejar `usuarios_roles`
- Modificar `guardarUsuario()` para validar permisos
- Agregar validación de máximo 3 roles

#### 2.3 Actualizar PermisosDao (`app/dao/referenciales/usuario/permisos_dao.py`)
- Modificar `obtener_permisos_grupo()` para aceptar múltiples grupos
- Crear `obtener_permisos_usuario(id_usuario)` - Consolida permisos de todos los roles
- Actualizar `es_administrador()` para verificar en `usuarios_roles`
- Crear `es_superadministrador(id_usuario)`
- Crear `obtener_rol_mayor_rango(id_usuario)` - Para resolver conflictos

#### 2.4 Actualizar decoradores (`app/utils/decorators.py`)
- Modificar `require_group()` para verificar múltiples roles
- Crear `require_superadmin()` - Solo Superadministrador
- Crear `require_admin_or_superadmin()` - Administrador o Superadministrador

#### 2.5 Actualizar endpoints (`app/rutas/seguridad/usuario/usuario_api.py`)
- Modificar `addUsuario()` - Validar que solo Superadministrador puede crear
- Modificar `updateUsuario()` - Validar permisos para asignar roles
- Agregar endpoint `POST /usuarios/<id>/roles` - Asignar roles
- Agregar endpoint `DELETE /usuarios/<id>/roles/<id_grupo>` - Remover rol
- Agregar endpoint `GET /usuarios/<id>/roles` - Listar roles del usuario
- Validar máximo 3 roles, mínimo 1 rol activo

**Entregables Fase 2**:
- ✅ Servicio de roles completo
- ✅ Validaciones de permisos funcionando
- ✅ Endpoints actualizados con seguridad
- ✅ Lógica de permisos consolidada

---

### FASE 3: Frontend y UX (INTERFAZ)

**Objetivo**: Adaptar la interfaz para manejar roles múltiples

#### 3.1 Actualizar formulario de creación de usuarios
- Mostrar solo si el usuario es Superadministrador
- Selector de roles múltiples (máximo 3)
- Validación visual de roles permitidos según jerarquía
- Mostrar qué roles puede asignar el usuario actual

#### 3.2 Actualizar formulario de edición de usuarios
- Mostrar todos los roles del usuario
- Permitir agregar/remover roles (con validaciones)
- Indicar rol principal
- Validar que siempre quede al menos 1 rol activo

#### 3.3 Actualizar listado de usuarios
- Mostrar todos los roles de cada usuario
- Indicar rol principal
- Mostrar jerarquía visual (Superadmin > Admin > otros)

#### 3.4 Validaciones en frontend
- Ocultar opciones según permisos del usuario actual
- Mensajes de error claros
- Confirmaciones antes de remover roles

**Entregables Fase 3**:
- ✅ Interfaz actualizada para roles múltiples
- ✅ Validaciones visuales
- ✅ UX mejorada

---

## Testing y Validación

Después de cada fase, probar:

1. **Fase 1**: 
   - Verificar que los datos se migraron correctamente
   - Verificar que el Superadministrador puede iniciar sesión

2. **Fase 2**:
   - Probar creación de usuario (solo Superadmin)
   - Probar asignación de roles según jerarquía
   - Probar roles múltiples (Admin + Especialista)
   - Probar validación de máximo 3 roles
   - Probar desactivación si no tiene roles

3. **Fase 3**:
   - Probar flujo completo desde la interfaz
   - Verificar que las validaciones funcionan
   - Probar casos edge

---

## Consideraciones de Seguridad

1. **Validación en Backend**: Nunca confiar solo en validaciones del frontend
2. **Logs de Auditoría**: Registrar todas las asignaciones/remociones de roles
3. **Protección de Superadministrador**: Prevenir eliminación del último Superadministrador
4. **Validación de Sesión**: Verificar permisos en cada request crítico
5. **Principio de Menor Privilegio**: Los usuarios solo ven/editan lo que su rol permite

---

## Notas Finales

Esta propuesta resuelve ambos problemas:
- ✅ Jerarquía de permisos (Superadministrador > Administrador > otros)
- ✅ Roles múltiples por usuario

La implementación puede ser gradual, manteniendo compatibilidad con el sistema actual mientras se migra a la nueva estructura.

**¿Tienes alguna pregunta o necesitas que aclare algún punto específico?**

