# Sistema de Roles Múltiples y Superadministrador - Documentación Completa

**Fecha de última actualización:** Enero 2025  
**Estado:** ✅ Implementación Completa

---

## 📋 Tabla de Contenidos

1. [Resumen Ejecutivo](#resumen-ejecutivo)
2. [Instalación y Configuración](#instalación-y-configuración)
3. [Arquitectura del Sistema](#arquitectura-del-sistema)
4. [Funcionalidades Implementadas](#funcionalidades-implementadas)
5. [Reglas de Negocio](#reglas-de-negocio)
6. [Guía de Uso](#guía-de-uso)
7. [Archivos Modificados](#archivos-modificados)
8. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Resumen Ejecutivo

Este documento describe la implementación completa del sistema de **roles múltiples** y **Superadministrador** en el sistema CIN. La implementación incluye:

- ✅ Rol de Superadministrador con permisos totales
- ✅ Sistema de roles múltiples (hasta 3 roles por usuario)
- ✅ Restricciones de creación de usuarios (solo Superadmin)
- ✅ Restricciones de asignación de roles según nivel de acceso
- ✅ Filtrado de cargos y grupos según permisos
- ✅ Panel exclusivo para Superadministrador
- ✅ Validaciones en backend y frontend

---

## 🚀 Instalación y Configuración

### Para Base de Datos Nueva

#### Opción 1: Script Maestro Unificado (Recomendado)

```bash
# Desde psql
psql -U postgres -f app/varios/SQL/00_SCRIPT_MAESTRO_UNIFICADO.sql
```

**Ventajas:**
- ✅ Ejecuta todas las fases (00-14) en orden correcto
- ✅ Incluye el grupo Superadministrador desde el inicio
- ✅ Crea la tabla `usuarios_roles` automáticamente
- ✅ Asigna permisos al Superadministrador después de crear páginas

#### Opción 2: Ejecutar Fases Manualmente

```bash
# 1. Crear base de datos
psql -U postgres -f 00_CREAR_BASE_DATOS.sql

# 2. Referenciales básicas
psql -U postgres -d cin_db -f 01_FASE_1_REFERENCIALES_BASICAS.sql

# 3. Seguridad y usuarios (INCLUYE Superadministrador)
psql -U postgres -d cin_db -f 02_FASE_2_SEGURIDAD_USUARIOS.sql

# 4-14. Resto de fases...
# ... (continuar con fases 03-14)

# IMPORTANTE: Después de crear todas las páginas, asignar permisos
psql -U postgres -d cin_db -f ASIGNAR_PERMISOS_SUPERADMIN.sql
```

### Para Base de Datos Existente

Si ya tienes una base de datos en funcionamiento, ejecuta el script de migración:

```bash
psql -U postgres -d cin_db -f crear_superadministrador_completo.sql
```

**Este script:**
1. ✅ Crea el grupo Superadministrador
2. ✅ Crea la tabla `usuarios_roles`
3. ✅ Migra los datos existentes de `usuarios.id_grupo` a `usuarios_roles`
4. ✅ Copia todos los permisos del Administrador al Superadministrador
5. ✅ Crea el usuario `superadmin` (requiere hash de contraseña)

### Generar Hash de Contraseña

Antes de ejecutar el script de migración, genera el hash de la contraseña:

```python
from werkzeug.security import generate_password_hash

password = "tu_contraseña_segura"
hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
print(f"Hash: {hashed_password}")
```

Luego reemplaza `<HASH_CONTRASEÑA>` en el script SQL con el hash generado.

---

## 🏗️ Arquitectura del Sistema

### Estructura de Base de Datos

#### Tabla `grupos`

Ahora incluye 5 grupos (en orden de creación):

1. **SUPERADMINISTRADOR** (ID: 5)
2. **ADMINISTRADOR** (ID: 1)
3. **RECEPCIONISTA** (ID: 2)
4. **ESPECIALISTA** (ID: 3)
5. **VENTAS** (ID: 4)

#### Tabla `usuarios_roles` (NUEVA)

Permite que un usuario tenga múltiples roles:

```sql
CREATE TABLE usuarios_roles (
    id_usuario_rol SERIAL PRIMARY KEY,
    id_usuario INTEGER NOT NULL,
    id_grupo INTEGER NOT NULL,
    es_rol_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER,
    CONSTRAINT unique_usuario_grupo UNIQUE(id_usuario, id_grupo)
);
```

#### Tabla `funcionario_grupos` (NUEVA)

Permite asignar grupos/roles a funcionarios:

```sql
CREATE TABLE funcionario_grupos (
    id_funcionario_grupo SERIAL PRIMARY KEY,
    id_funcionario INTEGER NOT NULL,
    id_grupo INTEGER NOT NULL,
    es_grupo_principal BOOLEAN DEFAULT FALSE,
    activo BOOLEAN DEFAULT TRUE,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    asignado_por INTEGER,
    CONSTRAINT unique_funcionario_grupo UNIQUE(id_funcionario, id_grupo)
);
```

### Servicios y Componentes

#### `RolesService` (`app/services/roles_service.py`)

Servicio centralizado para gestión de roles y permisos:

- `puede_crear_usuario()`: Verifica si el usuario puede crear nuevos usuarios
- `puede_asignar_rol()`: Verifica si puede asignar un rol específico
- `obtener_roles_permitidos()`: Obtiene lista de roles que puede asignar
- `es_superadmin()`: Verifica si un grupo es Superadministrador
- `es_admin()`: Verifica si un grupo es Administrador
- `obtener_grupos_operativos()`: Obtiene grupos operativos (Recepcionista, Especialista, Ventas)

---

## ✅ Funcionalidades Implementadas

### 1. Panel de Superadministrador

- ✅ Sección "Usuarios" visible solo para Superadministrador
- ✅ Dashboard con módulos específicos para Superadmin
- ✅ Acceso completo a todos los módulos

### 2. Creación de Usuarios

- ✅ Solo Superadministrador puede crear usuarios nuevos
- ✅ Validación en backend y frontend
- ✅ Campos de contraseña ocultos para no-Superadmin

### 3. Asignación de Roles

**Superadministrador:**
- ✅ Puede asignar cualquier rol (incluyendo Administrador y Superadministrador)

**Administrador:**
- ✅ Solo puede asignar roles operativos (Recepcionista, Especialista, Ventas)
- ❌ No puede asignar Administrador ni Superadministrador

### 4. Roles Múltiples

- ✅ Un usuario puede tener hasta 3 roles activos simultáneos
- ✅ Un rol debe ser marcado como "principal"
- ✅ Validación en backend y frontend del límite de 3 roles

### 5. Grupos por Funcionario

- ✅ Un funcionario puede tener hasta 3 grupos asignados
- ✅ El primer grupo seleccionado es el grupo principal
- ✅ Filtrado de grupos según permisos del usuario actual

### 6. Filtrado de Cargos

- ✅ Superadministrador ve todos los cargos
- ✅ Administrador NO ve el cargo "ADMINISTRADOR"
- ✅ Endpoint `/api/v1/cargos-permitidos` filtra según rol

### 7. Filtrado de Grupos

- ✅ Superadministrador ve todos los grupos
- ✅ Administrador solo ve grupos operativos
- ✅ Validación adicional en frontend

---

## 📋 Reglas de Negocio

### Matriz de Permisos

| Acción | Superadministrador | Administrador | Otros Roles |
|--------|-------------------|---------------|-------------|
| **Crear usuarios** | ✅ SÍ | ❌ NO | ❌ NO |
| **Asignar rol Administrador** | ✅ SÍ | ❌ NO | ❌ NO |
| **Asignar rol Superadministrador** | ✅ SÍ | ❌ NO | ❌ NO |
| **Asignar roles operativos** | ✅ SÍ | ✅ SÍ | ❌ NO |
| **Ver usuarios Admin/Superadmin** | ✅ SÍ | ❌ NO | ❌ NO |
| **Editar usuarios Admin/Superadmin** | ✅ SÍ | ❌ NO | ❌ NO |
| **Cambiar contraseñas** | ✅ SÍ | ❌ NO | ❌ NO |
| **Ver cargo ADMINISTRADOR** | ✅ SÍ | ❌ NO | ❌ NO |

### Límites y Validaciones

- **Máximo 3 roles por usuario**: Validado en backend y frontend
- **Máximo 3 grupos por funcionario**: Validado en backend y frontend
- **Un rol principal obligatorio**: Siempre debe haber exactamente un rol principal
- **No remover último rol**: No se puede remover el único rol activo de un usuario

---

## 📖 Guía de Uso

### Crear un Usuario Nuevo (Solo Superadmin)

1. Iniciar sesión como Superadministrador
2. Ir a "Registrar" → "Usuarios"
3. Hacer clic en "Agregar Nuevo Usuario"
4. Seleccionar funcionario (sin usuario asignado)
5. Ingresar username y contraseña
6. Seleccionar rol principal
7. Guardar

### Asignar Roles Adicionales

1. Editar un usuario existente
2. En la sección "Roles Adicionales", hacer clic en "Agregar Rol"
3. Seleccionar el rol a agregar (según permisos)
4. El sistema validará que no exceda 3 roles
5. Guardar

### Asignar Grupos a Funcionario

1. Crear o editar un funcionario
2. En la sección "Grupos/Roles Asignados", seleccionar los grupos
3. El primer grupo seleccionado será el principal
4. Máximo 3 grupos por funcionario
5. Guardar

---

## 📁 Archivos Modificados

### Backend

**Servicios:**
- `app/services/roles_service.py` - Servicio centralizado de roles

**DAOs:**
- `app/auth/dao/user_dao.py` - Gestión de roles de usuarios
- `app/dao/gestionar_personas/funcionario/FuncionarioDao.py` - Gestión de grupos de funcionarios
- `app/dao/referenciales/cargo/CargoDao.py` - Filtrado de cargos

**APIs:**
- `app/rutas/seguridad/usuario/usuario_api.py` - Endpoints con validaciones
- `app/rutas/gestionar_personas/funcionario/funcionario_api.py` - Endpoints con validaciones
- `app/rutas/referenciales/cargo/cargo_api.py` - Endpoint de cargos permitidos

**Helpers:**
- `app/utils/template_helpers.py` - Funciones helper para templates
- `app/utils/decorators.py` - Decoradores de seguridad

### Frontend

**Templates:**
- `app/templates/base.html` - Menú lateral con restricciones
- `app/rutas/seguridad/templates/inicio.html` - Dashboard con módulos
- `app/rutas/seguridad/usuario/templates/usuario-index.html` - Gestión de usuarios
- `app/rutas/gestionar_personas/funcionario/templates/funcionario-index.html` - Gestión de funcionarios
- `app/rutas/gestionar_personas/funcionario/templates/funcionario-agregar.html` - Formulario de funcionarios

### SQL

- `app/varios/SQL/00_SCRIPT_MAESTRO_UNIFICADO.sql` - Script maestro
- `app/varios/SQL/02_FASE_2_SEGURIDAD_USUARIOS.sql` - Fase 2 actualizada
- `app/varios/SQL/ASIGNAR_PERMISOS_SUPERADMIN.sql` - Asignación de permisos

---

## 🔧 Solución de Problemas

### Error: "No se encontró el grupo Superadministrador"

**Solución**: Ejecuta primero `02_FASE_2_SEGURIDAD_USUARIOS.sql` o verifica que el INSERT de grupos incluya Superadministrador.

### Error: "No se encontró la tabla usuarios_roles"

**Solución**: Ejecuta `02_FASE_2_SEGURIDAD_USUARIOS.sql` (versión actualizada) que incluye la creación de esta tabla.

### El Superadministrador no tiene permisos

**Solución**: Ejecuta `ASIGNAR_PERMISOS_SUPERADMIN.sql` después de crear todas las páginas.

### Error: "llave duplicada viola restricción de unicidad usuarios_id_funcionario_key"

**Solución**: El script `crear_superadministrador_completo.sql` maneja este caso automáticamente. Si persiste, verifica que no exista otro usuario con el mismo `id_funcionario`.

### El Administrador ve el cargo "ADMINISTRADOR"

**Solución**: Verifica que el frontend esté usando el endpoint `/api/v1/cargos-permitidos` en lugar de `/api/v1/cargos`.

### El Administrador puede asignar el rol "Administrador"

**Solución**: Verifica que `RolesService.puede_asignar_rol()` esté validando correctamente y que el frontend esté usando `/api/v1/funcionarios/grupos-permitidos`.

---

## ✅ Verificación

### Verificar que el Superadministrador existe

```sql
SELECT id_grupo, des_grupo, est_grupo
FROM grupos
WHERE LOWER(des_grupo) = 'superadministrador';
```

### Verificar permisos del Superadministrador

```sql
SELECT 
    m.des_modulo AS "Módulo",
    COUNT(*) AS "Total Páginas",
    SUM(CASE WHEN p.leer THEN 1 ELSE 0 END) AS "Ver",
    SUM(CASE WHEN p.insertar THEN 1 ELSE 0 END) AS "Crear",
    SUM(CASE WHEN p.editar THEN 1 ELSE 0 END) AS "Editar",
    SUM(CASE WHEN p.borrar THEN 1 ELSE 0 END) AS "Eliminar"
FROM permisos p
INNER JOIN grupos g ON p.id_grupo = g.id_grupo
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE LOWER(g.des_grupo) = 'superadministrador'
  AND pg.est_pagina = TRUE
GROUP BY m.des_modulo
ORDER BY m.des_modulo;
```

### Verificar tabla usuarios_roles

```sql
SELECT COUNT(*) AS "Total roles asignados"
FROM usuarios_roles
WHERE activo = TRUE;
```

---

## 📝 Notas Importantes

1. **Orden de Ejecución**: El grupo Superadministrador debe crearse ANTES que el Administrador para que tenga el ID más bajo (opcional, pero recomendado).

2. **Permisos Automáticos**: La función `asignar_permisos_superadministrador()` se ejecuta automáticamente después de crear páginas, pero puedes ejecutarla manualmente cuando sea necesario.

3. **Compatibilidad**: Los cambios son **compatibles hacia atrás**. El código Python existente seguirá funcionando porque:
   - La tabla `usuarios.id_grupo` sigue existiendo (rol principal)
   - La tabla `usuarios_roles` es adicional (roles múltiples)
   - Los permisos se siguen consultando desde `permisos` usando `id_grupo`

4. **Migración de Datos**: Si actualizas una BD existente, el script `crear_superadministrador_completo.sql` migra automáticamente los datos de `usuarios.id_grupo` a `usuarios_roles`.

5. **Seguridad**: Todas las validaciones críticas están en el backend. El frontend solo oculta opciones para mejor UX, pero no es seguro por sí solo.

---

## 🎯 Estado de Implementación

### ✅ Completado (100%)

- [x] Panel de Superadministrador
- [x] Restricción de creación de usuarios
- [x] Restricción de asignación de roles
- [x] Roles múltiples por usuario
- [x] Grupos por funcionario
- [x] Filtrado de cargos según permisos
- [x] Filtrado de grupos según permisos
- [x] Validaciones en backend
- [x] Validaciones en frontend
- [x] Documentación completa

---

**Última actualización:** Enero 2025  
**Versión:** 1.0.0  
**Autor:** Sistema CIN

