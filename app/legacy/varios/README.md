# Documentación del Sistema

## 📚 Documentación Principal

### Seguridad y Autenticación
- **`MD/RESUMEN_MEJORAS_SEGURIDAD_AUTENTICACION.md`** - Resumen completo de cambios de seguridad
- **`MD/README_CAMBIOS_SEGURIDAD.md`** - Guía rápida de cambios

### Base de Datos
- **`MD/README_ESTRUCTURA_BD.md`** - Estructura de la base de datos
- **`MD/README_FASES.md`** - Documentación de fases de creación de BD
- **`SQL/README_CORRECCIONES.md`** - Scripts SQL de corrección

## 🔧 Scripts SQL Principales

### Creación de Base de Datos (Ejecutar en orden)
1. `00_CREAR_BASE_DATOS.sql`
2. `01_FASE_1_REFERENCIALES_BASICAS.sql`
3. `02_FASE_2_SEGURIDAD_USUARIOS.sql` ✅ (Incluye todas las mejoras)
4. `03_FASE_3_PERSONAS_PACIENTES.sql`
5. `11_MIGRACIONES_UNIFICADAS.sql`
6. `12_CREAR_USUARIOS_EJEMPLO_UNIFICADO.sql`

### Correcciones
- `FIX_CORRECCIONES_SEGURIDAD.sql` - Correcciones unificadas (solo si es necesario)

## 📝 Notas Importantes

- Los scripts principales ya incluyen todas las correcciones
- Los scripts FIX son solo para aplicar después si es necesario
- Ver `MD/RESUMEN_MEJORAS_SEGURIDAD_AUTENTICACION.md` para detalles completos









