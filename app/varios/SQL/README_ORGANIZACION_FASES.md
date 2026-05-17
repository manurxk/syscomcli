# Organización de Scripts SQL por Fases

Este documento explica la organización de todos los scripts SQL del sistema en fases ordenadas (01-14 para estructura, 15 para datos).

## 📋 Estructura de Fases

### Fase 00: Crear Base de Datos
**Archivo:** `00_CREAR_BASE_DATOS.sql`
- Crea la base de datos `cin_db`
- Habilita extensiones necesarias (pg_trgm)
- Configuración inicial

### Fase 01: Referenciales Básicas
**Archivo:** `01_FASE_1_REFERENCIALES_BASICAS.sql`
- Géneros, Estados Civiles, Ciudades
- Niveles de Instrucción, Profesiones, Especialidades
- **Incluye:** Datos iniciales de estas tablas

### Fase 02: Seguridad y Usuarios
**Archivo:** `02_FASE_2_SEGURIDAD_USUARIOS_ACTUALIZADO.sql`
- Grupos (incluye **Superadministrador**)
- Módulos, Cargos
- Personas, Funcionarios, Usuarios
- Páginas, Permisos
- **Tabla usuarios_roles** (roles múltiples)
- Tablas de seguridad avanzada (sesiones, login_attempts, password_reset_tokens, etc.)
- **Incluye:** Datos iniciales de grupos, módulos, cargos

### Fase 03: Personas y Pacientes
**Archivo:** `03_FASE_3_PERSONAS_PACIENTES.sql`
- Pacientes
- Pacientes Menores

### Fase 04: Especialistas y Agendamiento
**Archivo:** `04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql`
- Especialistas, Especialista-Especialidades
- Consultorios, Días de la Semana
- Agenda Horarios, Estados de Citas, Citas, Recordatorios
- **Incluye:** Datos iniciales de días de semana y estados de citas

### Fase 05: Consultorio
**Archivo:** `05_FASE_5_CONSULTORIO.sql`
- Síntomas, Signos, Diagnósticos
- Tipos de Análisis, Tipos de Estudios, Medicamentos
- Tipos de Procedimientos, Tipos de Tratamientos
- Consultas, Registro de Diagnósticos, Procedimientos
- Tratamientos, Registro de Síntomas/Signos, Anamnesis

### Fase 06: Referenciales Ventas
**Archivo:** `06_FASE_6_REFERENCIALES_VENTAS.sql`
- Formas de Cobro, Marcas de Tarjeta
- Entidades Adheridas, Entidades Emisoras
- Depósitos, Cajas, Tipos de Items
- Tipos de Impuestos, Condiciones de Venta
- Tipos de Comprobantes, Estados de Factura, Monedas

### Fase 07: Principales Ventas
**Archivo:** `07_FASE_7_PRINCIPALES_VENTAS.sql`
- Aperturas y Cierres de Caja, Arqueos de Caja
- Recaudaciones, Pedidos, Facturas
- Cuentas a Cobrar, Cobranzas
- Notas de Crédito, Notas de Débito, Libro de Ventas

### Fase 08: Tablas Nuevas
**Archivo:** `08_FASE_8_TABLAS_NUEVAS.sql`
- Presupuestos, Órdenes de Estudios
- Recetas, Certificados Médicos
- Insumos, Informes de Agendamiento y Consultorio

### Fase 09: Triggers y Auditoría
**Archivo:** `09_TRIGGERS_AUDITORIA.sql`
- Triggers de fecha_modificacion automática
- Validación de cupos en citas
- Registro automático de confirmaciones

### Fase 10: Datos Iniciales
**Archivo:** `10_DATOS_INICIALES.sql`
- Monedas, Formas de Cobro, Marcas de Tarjeta
- Tipos de Items, Tipos de Impuestos
- Condiciones de Venta, Tipos de Comprobantes, Estados de Factura

### Fase 11: Migraciones Unificadas
**Archivo:** `11_MIGRACIONES_UNIFICADAS.sql`
- Agregar columna `per_fecha_inscripcion` a personas
- Crear usuario SISTEMA (id_usuario = 1)
- Migrar auditoría de VARCHAR a INTEGER + Foreign Keys

### Fase 12: Crear Usuarios de Ejemplo (Opcional)
**Archivo:** `12_CREAR_USUARIOS_EJEMPLO_UNIFICADO.sql`
- Usuarios de ejemplo: admin, recep1, psico1, psico2, ventas1
- **NOTA:** Requiere generar hashes de contraseñas primero

### Fase 13: Otros (Opcional)
**Archivo:** `13_OTROS.sql`
- Fixes y tablas adicionales opcionales
- Tabla items_servicios

### Fase 14: Empresa, Sede y SIFEN
**Archivo:** `14_FASE_14_EMPRESA_SEDE_SIFEN.sql`
- Empresa (datos SIFEN completos)
- Sedes, Timbrados
- Establecimientos, Puntos de Expedición
- Modificaciones a Consultorios y Facturas

### Fase 15: Inserts de Todos los Datos
**Archivo:** `15_FASE_15_INSERTS_DATOS.sql` ⭐ **NUEVO**
- **TODOS los inserts consolidados**
- Datos referenciales básicos
- Datos de seguridad (incluyendo **Superadministrador**)
- Datos de agendamiento
- Datos de ventas
- Datos de consultorio
- Asignación automática de permisos al Superadministrador

### Fase 16: Paciente-Profesional y Derivaciones
**Archivo:** `16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql` ⭐ **NUEVO**
- **Paciente-Profesional** (vincular pacientes con especialistas M:M)
- **Derivaciones** (derivar pacientes entre especialistas)
- **Notificaciones** (sistema de notificaciones)
- **Soporte para especialistas externos**
- Funciones: crear_derivacion, aceptar_derivacion, rechazar_derivacion
- Migración automática de relaciones desde citas y consultas
- Vistas: v_derivaciones_pendientes, v_pacientes_por_especialista

## 🚀 Cómo Usar

### Opción 1: Script Maestro (Recomendado)

```bash
# 1. Crear base de datos
psql -U postgres -f 00_CREAR_BASE_DATOS.sql

# 2. Conectar a la base de datos
psql -U postgres -d cin_db

# 3. Ejecutar script maestro de estructura (fases 01-14 y 16)
\i 00_SCRIPT_MAESTRO_FASES_01_14.sql

# 4. Ejecutar script de inserts (fase 15)
\i 15_FASE_15_INSERTS_DATOS.sql
```

### Opción 2: Ejecutar Fases Individualmente

```bash
# Conectar a la base de datos
psql -U postgres -d cin_db

# Ejecutar cada fase en orden
\i 01_FASE_1_REFERENCIALES_BASICAS.sql
\i 02_FASE_2_SEGURIDAD_USUARIOS_ACTUALIZADO.sql
\i 03_FASE_3_PERSONAS_PACIENTES.sql
\i 04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql
\i 05_FASE_5_CONSULTORIO.sql
\i 06_FASE_6_REFERENCIALES_VENTAS.sql
\i 07_FASE_7_PRINCIPALES_VENTAS.sql
\i 08_FASE_8_TABLAS_NUEVAS.sql
\i 09_TRIGGERS_AUDITORIA.sql
\i 10_DATOS_INICIALES.sql
\i 11_MIGRACIONES_UNIFICADAS.sql
\i 14_FASE_14_EMPRESA_SEDE_SIFEN.sql

# Fase 16: Paciente-Profesional y Derivaciones
\i 16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql

# Finalmente, ejecutar todos los inserts
\i 15_FASE_15_INSERTS_DATOS.sql
```

## 📝 Notas Importantes

### Sobre el Superadministrador

1. **Grupo creado en Fase 02:** El grupo `SUPERADMINISTRADOR` se crea automáticamente en la Fase 02.

2. **Permisos asignados en Fase 15:** Los permisos se asignan automáticamente en la Fase 15 si ya existen páginas creadas.

3. **Crear usuario Superadministrador:** Después de ejecutar todas las fases, crear el usuario manualmente usando:
   ```bash
   \i crear_superadministrador_completo.sql
   ```
   **IMPORTANTE:** Reemplazar el hash de contraseña en el script antes de ejecutar.

4. **Asignar permisos después de crear páginas:** Si creas nuevas páginas desde la aplicación, ejecutar:
   ```bash
   \i ASIGNAR_PERMISOS_SUPERADMIN.sql
   ```

### Sobre los Datos

- **Fase 15 consolida todos los inserts:** La Fase 15 incluye todos los datos que estaban dispersos en las fases anteriores.
- **No duplica datos:** Usa `ON CONFLICT DO NOTHING` para evitar duplicados.
- **Incluye nuevos roles:** Todos los datos del Superadministrador están incluidos.

### Orden de Ejecución Crítico

1. ✅ **Fase 00:** Crear BD
2. ✅ **Fases 01-14:** Estructura básica (en orden)
3. ✅ **Fase 16:** Funcionalidades avanzadas (Paciente-Profesional, Derivaciones, Notificaciones)
4. ✅ **Fase 15:** Todos los datos
5. ✅ **Crear usuario Superadministrador:** Manualmente
6. ✅ **Crear páginas:** Desde la aplicación
7. ✅ **Asignar permisos:** Ejecutar `ASIGNAR_PERMISOS_SUPERADMIN.sql`

## 🔍 Verificación

Después de ejecutar todas las fases, verificar:

```sql
-- Verificar grupos
SELECT * FROM grupos ORDER BY id_grupo;

-- Verificar que Superadministrador existe
SELECT * FROM grupos WHERE LOWER(des_grupo) = 'superadministrador';

-- Verificar tabla usuarios_roles
SELECT * FROM usuarios_roles LIMIT 5;

-- Verificar datos insertados
SELECT 'Grupos' AS tabla, COUNT(*) AS cantidad FROM grupos
UNION ALL
SELECT 'Módulos', COUNT(*) FROM modulos
UNION ALL
SELECT 'Cargos', COUNT(*) FROM cargos
UNION ALL
SELECT 'Especialidades', COUNT(*) FROM especialidades;
```

## 📚 Archivos Relacionados

- `00_SCRIPT_MAESTRO_FASES_01_14.sql` - Script maestro para estructura (incluye FASE 16)
- `16_FASE_16_PACIENTE_PROFESIONAL_DERIVACIONES.sql` - Funcionalidades avanzadas ⭐ NUEVO
- `15_FASE_15_INSERTS_DATOS.sql` - Todos los inserts consolidados
- `crear_superadministrador_completo.sql` - Crear usuario Superadministrador
- `ASIGNAR_PERMISOS_SUPERADMIN.sql` - Asignar permisos después de crear páginas
- `ANALISIS_FUNCIONALIDADES_COMPLETAS.md` - Análisis detallado de funcionalidades ⭐ NUEVO

## ⚠️ Advertencias

1. **Backup antes de ejecutar:** Siempre hacer backup de la base de datos antes de ejecutar scripts.

2. **Contraseñas:** Los usuarios de ejemplo requieren generar hashes de contraseñas. Ver `generar_hashes_contraseñas.py`.

3. **Páginas:** Los permisos del Superadministrador se asignan automáticamente solo si ya existen páginas creadas.

4. **Producción:** Cambiar todas las contraseñas por defecto en producción.

