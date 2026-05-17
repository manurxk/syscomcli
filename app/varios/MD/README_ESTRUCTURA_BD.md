# 📋 Documentación de Estructura de Base de Datos - Sistema CIN

## 📁 Archivos SQL Creados

1. **`estructura_bd_y_tablas_faltantes.sql`** - Scripts CREATE TABLE para todas las tablas faltantes
2. **`ejemplos_uso_tablas_faltantes.sql`** - Ejemplos prácticos de uso y consultas útiles

---

## 🏗️ Estructura de Base de Datos - Patrón del Sistema

### Ejemplo de Tabla Referencial Simple: `ciudades`

```sql
CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,           -- ID autoincremental
    des_ciudad VARCHAR(100) NOT NULL UNIQUE, -- Descripción única
    est_ciudad BOOLEAN NOT NULL DEFAULT TRUE -- Estado activo/inactivo
);
```

**Características:**
- ✅ ID con `SERIAL PRIMARY KEY` (autoincremental)
- ✅ Descripción con prefijo `des_`
- ✅ Estado con prefijo `est_` (BOOLEAN o CHAR(1))
- ✅ Campos NOT NULL cuando son obligatorios
- ✅ UNIQUE en campos que no deben repetirse

---

## 📊 Tablas Creadas para Completar Requerimientos

### 1. **PRESUPUESTOS** (`presupuestos` + `presupuesto_detalle`)

**Propósito:** Generar presupuestos/cotizaciones para pacientes

**Tabla Principal:**
- `id_presupuesto` - ID único
- `presupuesto_numero` - Número único del presupuesto (ej: PRES-2024-001)
- `presupuesto_fecha` - Fecha de emisión
- `presupuesto_subtotal`, `presupuesto_descuento`, `presupuesto_total` - Cálculos financieros
- `presupuesto_estado` - PENDIENTE, APROBADO, RECHAZADO, VENCIDO

**Tabla Detalle:**
- `presupuesto_detalle` - Items/servicios incluidos en el presupuesto
- Relación 1:N con la tabla principal

---

### 2. **ÓRDENES DE ESTUDIOS** (`ordenes_estudios` + `orden_estudio_detalle`)

**Propósito:** Generar órdenes de laboratorio/imagenología/estudios complementarios

**Tabla Principal:**
- `id_orden_estudio` - ID único
- `orden_numero` - Número único (ej: ORD-LAB-2024-001)
- `orden_tipo` - LABORATORIO, IMAGENOLOGIA, OTROS
- `orden_estado` - PENDIENTE, REALIZADO, CANCELADO
- `orden_indicaciones` - Instrucciones para el paciente

**Tabla Detalle:**
- `orden_estudio_detalle` - Estudios específicos solicitados
- Relación con `tipos_estudios` y `tipos_analisis`

---

### 3. **RECETAS** (`recetas` + `receta_detalle`)

**Propósito:** Registrar recetas médicas con medicamentos e indicaciones

**Tabla Principal:**
- `id_receta` - ID único
- `receta_numero` - Número único (ej: REC-2024-001)
- `receta_validez_dias` - Días de validez (default: 30)
- `receta_indicaciones_generales` - Instrucciones generales

**Tabla Detalle:**
- `receta_detalle` - Medicamentos prescritos
- Campos: dosis, frecuencia, duración, cantidad, posología, indicaciones específicas

---

### 4. **CERTIFICADOS MÉDICOS** (`certificados_medicos`)

**Propósito:** Generar certificados médicos (reposo, aptitud, asistencia, etc.)

**Campos Principales:**
- `id_certificado` - ID único
- `certificado_numero` - Número único (ej: CERT-2024-001)
- `certificado_tipo` - REPOSO, APTITUD, ASISTENCIA, OTROS
- `certificado_dias_reposo` - Días de reposo (si aplica)
- `certificado_desde_fecha` / `certificado_hasta_fecha` - Período de validez
- `certificado_motivo` - Motivo del certificado
- `certificado_diagnostico` - Diagnóstico relacionado
- `certificado_recomendaciones` - Recomendaciones médicas

---

### 5. **INSUMOS** (`insumos` + `registro_insumos`)

**Propósito:** Gestionar insumos/materiales médicos utilizados en procedimientos

**Tabla Catálogo:**
- `insumos` - Catálogo de insumos disponibles
- Campos: descripción, unidad de medida, stock actual, stock mínimo, precio

**Tabla Registro:**
- `registro_insumos` - Registro de insumos utilizados en procedimientos
- Relación con `registro_procedimientos`
- Campos: cantidad, costo unitario, costo total

---

### 6. **INFORMES DE AGENDAMIENTO** (`informes_agendamiento`)

**Propósito:** Generar informes web de agendamiento (estadísticas, reportes)

**Campos Principales:**
- `informe_tipo` - DIARIO, SEMANAL, MENSUAL, ANUAL, PERSONALIZADO
- `informe_fecha_desde` / `informe_fecha_hasta` - Rango de fechas
- `informe_parametros` - JSONB para parámetros adicionales flexibles
- `informe_generado` - Flag para saber si ya fue generado

---

### 7. **INFORMES DE CONSULTORIO** (`informes_consultorio`)

**Propósito:** Generar informes de consultorio (consultas, diagnósticos, tratamientos, etc.)

**Campos Principales:**
- `informe_tipo` - CONSULTAS, DIAGNOSTICOS, TRATAMIENTOS, PROCEDIMIENTOS, GENERAL
- `informe_fecha_desde` / `informe_fecha_hasta` - Rango de fechas
- `informe_parametros` - JSONB para parámetros adicionales
- Filtros por profesional y especialidad

---

## 🔑 Convenciones de Nomenclatura

### Tablas
- ✅ **Plural** en snake_case: `ciudades`, `presupuestos`, `recetas`
- ✅ Nombres descriptivos y claros

### Campos
- ✅ **IDs**: `id_tabla` (ej: `id_presupuesto`, `id_receta`)
- ✅ **Descripciones**: Prefijo `des_` (ej: `des_ciudad`, `des_insumo`)
- ✅ **Estados**: Prefijo `est_` (ej: `est_presupuesto`, `est_receta`)
- ✅ **Fechas**: Prefijo descriptivo (ej: `presupuesto_fecha`, `receta_fecha`)
- ✅ **Auditoría**: `fecha_creacion`, `usuario_creacion`, `fecha_modificacion`, `usuario_modificacion`

### Tipos de Datos
- ✅ **IDs**: `SERIAL` (autoincremental) o `INTEGER` (FK)
- ✅ **Descripciones**: `VARCHAR(n)` según necesidad
- ✅ **Estados simples**: `CHAR(1)` ('A'=Activo, 'I'=Inactivo)
- ✅ **Estados complejos**: `VARCHAR(20)` (ej: 'PENDIENTE', 'APROBADO')
- ✅ **Fechas**: `DATE` para fechas simples, `TIMESTAMP` para fecha+hora
- ✅ **Montos**: `DECIMAL(10,2)` para valores monetarios
- ✅ **Textos largos**: `TEXT` para observaciones, indicaciones, etc.

---

## 🔗 Relaciones (Foreign Keys)

**Patrón estándar:**
```sql
FOREIGN KEY (id_tabla_referenciada) REFERENCES tabla_referenciada(id_tabla_referenciada)
    ON DELETE RESTRICT ON UPDATE CASCADE
```

**Explicación:**
- `ON DELETE RESTRICT` - No permite eliminar registros referenciados (integridad)
- `ON UPDATE CASCADE` - Actualiza automáticamente las referencias si cambia el ID

**Excepciones:**
- `ON DELETE CASCADE` - Para tablas detalle (ej: `presupuesto_detalle`)
- `ON DELETE SET NULL` - Para campos opcionales (ej: `id_tipo_procedimiento` en detalle)

---

## 📝 Cómo Usar los Scripts

### Paso 1: Crear las Tablas
```bash
# Ejecutar en PostgreSQL
psql -U tu_usuario -d tu_base_datos -f estructura_bd_y_tablas_faltantes.sql
```

### Paso 2: Insertar Datos Iniciales
Los datos iniciales están incluidos en el mismo archivo (ej: insumos básicos)

### Paso 3: Probar con Ejemplos
```bash
# Ejecutar ejemplos de uso
psql -U tu_usuario -d tu_base_datos -f ejemplos_uso_tablas_faltantes.sql
```

---

## ✅ Checklist de Implementación

- [x] Estructura de tablas creada siguiendo el patrón del sistema
- [x] Foreign Keys definidas correctamente
- [x] Índices creados en campos frecuentemente consultados
- [x] Datos iniciales incluidos (insumos básicos)
- [x] Ejemplos de uso proporcionados
- [x] Triggers para automatización (números automáticos, actualización de stock)
- [x] Consultas útiles documentadas

---

## 🚀 Próximos Pasos

1. **Ejecutar los scripts SQL** en tu base de datos PostgreSQL
2. **Verificar** que las tablas se crearon correctamente
3. **Probar** los ejemplos de INSERT y SELECT
4. **Integrar** con el código Python (crear DAOs y APIs)
5. **Crear interfaces** de usuario para cada módulo

---

## 📞 Notas Importantes

- ⚠️ **Ajustar IDs**: Los ejemplos usan IDs de ejemplo (1, 2, etc.). Ajusta según tus datos reales.
- ⚠️ **Validaciones**: Las validaciones de negocio deben implementarse en el código Python
- ⚠️ **Números Únicos**: Los triggers generan números automáticos, pero puedes crear manualmente
- ⚠️ **Stock de Insumos**: El trigger actualiza el stock automáticamente al registrar uso

---

## 📚 Referencias

- Estructura basada en tablas existentes del sistema (`ciudades`, `consultas`, `citas`, etc.)
- Patrón de diseño consistente con el resto del sistema CIN
- Compatible con PostgreSQL 12+









