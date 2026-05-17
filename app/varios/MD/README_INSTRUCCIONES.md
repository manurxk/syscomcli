# 📋 INSTRUCCIONES PARA CREAR LA BASE DE DATOS DESDE CERO

## 🎯 Objetivo

Este conjunto de scripts SQL permite crear la base de datos completa del Sistema CIN desde cero, organizada por módulos y fases.

## 📁 Archivos SQL Creados

Los scripts están organizados en el siguiente orden de ejecución:

1. **00_CREAR_BASE_DATOS.sql** - Crea la base de datos y extensiones
2. **01_FASE_1_REFERENCIALES_BASICAS.sql** - Tablas referenciales básicas
3. **02_FASE_2_SEGURIDAD_USUARIOS.sql** - Sistema de seguridad y usuarios
4. **03_FASE_3_PERSONAS_PACIENTES.sql** - Tablas de pacientes
5. **04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql** - Especialistas y agendamiento
6. **05_FASE_5_CONSULTORIO.sql** - Módulo de consultorio
7. **06_FASE_6_REFERENCIALES_VENTAS.sql** - Referenciales de ventas
8. **07_FASE_7_PRINCIPALES_VENTAS.sql** - Tablas principales de ventas
9. **08_FASE_8_TABLAS_NUEVAS.sql** - Tablas nuevas (presupuestos, recetas, etc.)
10. **09_TRIGGERS_AUDITORIA.sql** - Triggers y funciones de auditoría
11. **10_DATOS_INICIALES.sql** - Datos iniciales del sistema

## 🚀 Pasos para Ejecutar

### Opción 1: Ejecutar Script por Script

```bash
# 1. Conectar a PostgreSQL
psql -U postgres

# 2. Ejecutar cada script en orden
\i 00_CREAR_BASE_DATOS.sql
\c cin_db
\i 01_FASE_1_REFERENCIALES_BASICAS.sql
\i 02_FASE_2_SEGURIDAD_USUARIOS.sql
\i 03_FASE_3_PERSONAS_PACIENTES.sql
\i 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
\i 05_FASE_5_CONSULTORIO.sql
\i 06_FASE_6_REFERENCIALES_VENTAS.sql
\i 07_FASE_7_PRINCIPALES_VENTAS.sql
\i 08_FASE_8_TABLAS_NUEVAS.sql
\i 09_TRIGGERS_AUDITORIA.sql
\i 10_DATOS_INICIALES.sql
```

### Opción 2: Ejecutar desde Línea de Comandos

```bash
# Crear base de datos
psql -U postgres -f 00_CREAR_BASE_DATOS.sql

# Ejecutar todas las fases
psql -U postgres -d cin_db -f 01_FASE_1_REFERENCIALES_BASICAS.sql
psql -U postgres -d cin_db -f 02_FASE_2_SEGURIDAD_USUARIOS.sql
psql -U postgres -d cin_db -f 03_FASE_3_PERSONAS_PACIENTES.sql
psql -U postgres -d cin_db -f 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
psql -U postgres -d cin_db -f 05_FASE_5_CONSULTORIO.sql
psql -U postgres -d cin_db -f 06_FASE_6_REFERENCIALES_VENTAS.sql
psql -U postgres -d cin_db -f 07_FASE_7_PRINCIPALES_VENTAS.sql
psql -U postgres -d cin_db -f 08_FASE_8_TABLAS_NUEVAS.sql
psql -U postgres -d cin_db -f 09_TRIGGERS_AUDITORIA.sql
psql -U postgres -d cin_db -f 10_DATOS_INICIALES.sql
```

## 📊 Estructura de la Base de Datos

### Convenciones de Nomenclatura

- **IDs**: `id_tabla` (SERIAL PRIMARY KEY)
- **Descripciones**: `des_tabla` (VARCHAR)
- **Estados**: `est_tabla` (CHAR(1) 'A'/'I' o BOOLEAN)
- **Auditoría**: 
  - Patrón nuevo: `fecha_creacion`, `usuario_creacion`, `fecha_modificacion`, `usuario_modificacion`
  - Patrón antiguo: `creacion_fecha`, `creacion_hora`, `creacion_usuario`, `modificacion_fecha`, `modificacion_hora`, `modificacion_usuario`

### Manejo de Usuarios y Sesiones

1. **Sesión de Usuario**: Cuando un usuario inicia sesión, se guarda en Flask:
   ```python
   session['id_usuario'] = usuario_encontrado['id_usuario']
   session['usu_nick'] = usuario_encontrado['usu_nick']
   ```

2. **Auditoría en INSERT**: Pasar el usuario desde la sesión:
   ```python
   usuario_creacion = session.get('usu_nick', 'SISTEMA')
   # O usar id_usuario si la tabla lo requiere
   usuario_creacion_id = session.get('id_usuario', 1)
   ```

3. **Auditoría en UPDATE**: Pasar el usuario desde la sesión:
   ```python
   usuario_modificacion = session.get('usu_nick', 'SISTEMA')
   # O usar id_usuario si la tabla lo requiere
   usuario_modificacion_id = session.get('id_usuario', 1)
   ```

### Valores Monetarios

- Todos los montos están en **Guaraníes (PYG)** como **INTEGER** (sin decimales)
- Ejemplo: 150000 (ciento cincuenta mil guaraníes), no 150000.00

## 🔐 Seguridad

### Crear Usuario Administrador

Después de ejecutar todos los scripts, crear un usuario administrador:

1. Crear persona
2. Crear funcionario vinculado a la persona
3. Crear usuario con contraseña hasheada

```python
from werkzeug.security import generate_password_hash

# Hashear contraseña
password_hash = generate_password_hash('tu_contraseña_segura', method='pbkdf2:sha256')

# Insertar en base de datos
```

## ⚠️ Importante

1. **Orden de Ejecución**: Los scripts deben ejecutarse en el orden indicado debido a las dependencias de Foreign Keys
2. **Datos Iniciales**: Los datos iniciales básicos ya están incluidos en los scripts
3. **Producción**: Cambiar todas las contraseñas por defecto antes de usar en producción
4. **Backup**: Hacer backup antes de ejecutar en producción

## 📝 Notas Adicionales

- Los triggers automáticos actualizan `fecha_modificacion` en UPDATE
- El usuario de sesión se captura desde Flask (`session['id_usuario']` o `session['usu_nick']`)
- Las tablas referenciales pueden gestionarse desde las interfaces administrativas
- Los valores monetarios están en Guaraníes (PYG) sin decimales

## 🆘 Solución de Problemas

### Error: "relation already exists"
- Eliminar la base de datos y volver a crearla: `DROP DATABASE IF EXISTS cin_db;`

### Error: "foreign key constraint"
- Verificar que las tablas referenciales se crearon antes que las tablas que las referencian

### Error: "permission denied"
- Verificar que el usuario tiene permisos para crear bases de datos y tablas

## 📞 Soporte

Para más información, consultar la documentación del sistema o contactar al equipo de desarrollo.








