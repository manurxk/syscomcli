# Scripts SQL - Sistema CIN

## 📋 Scripts Principales

### Script Maestro Unificado

**`00_SCRIPT_MAESTRO_UNIFICADO.sql`** - Ejecuta todas las fases (00-14) en orden e incluye el Superadministrador automáticamente.

```bash
psql -U postgres -f 00_SCRIPT_MAESTRO_UNIFICADO.sql
```

### Scripts por Fase

- `00_CREAR_BASE_DATOS.sql` - Crear base de datos
- `01_FASE_1_REFERENCIALES_BASICAS.sql` - Referenciales básicas
- `02_FASE_2_SEGURIDAD_USUARIOS.sql` - Seguridad y usuarios (incluye Superadministrador)
- `03_FASE_3_PERSONAS_PACIENTES.sql` - Personas y pacientes
- `04_FASE_4_ESPECIALISTAS_AGENDAMIENTO.sql` - Especialistas y agendamiento
- `05_FASE_5_CONSULTORIO.sql` - Consultorios
- `06_FASE_6_REFERENCIALES_VENTAS.sql` - Referenciales de ventas
- `07_FASE_7_PRINCIPALES_VENTAS.sql` - Tablas principales de ventas
- `08_FASE_8_TABLAS_NUEVAS.sql` - Tablas nuevas
- `09_TRIGGERS_AUDITORIA.sql` - Triggers de auditoría
- `10_DATOS_INICIALES.sql` - Datos iniciales
- `11_MIGRACIONES_UNIFICADAS.sql` - Migraciones unificadas
- `12_CREAR_USUARIOS_EJEMPLO.sql` - Usuarios de ejemplo
- `13_OTROS.sql` - Otros scripts
- `14_FASE_14_EMPRESA_SEDE_SIFEN.sql` - Empresa, sede y SIFEN

### Scripts de Utilidad

- `ASIGNAR_PERMISOS_SUPERADMIN.sql` - Asigna permisos al Superadministrador después de crear páginas

## 📚 Documentación Completa

Para documentación completa sobre el sistema de roles y Superadministrador, consulta:

**`README_IMPLEMENTACION_ROLES_SUPERADMIN.md`** (en la raíz del proyecto)

Este documento incluye:
- Guía de instalación
- Arquitectura del sistema
- Funcionalidades implementadas
- Reglas de negocio
- Solución de problemas

## ⚠️ Notas Importantes

1. **Orden de Ejecución**: Ejecuta las fases en orden (00, 01, 02, ...)
2. **Superadministrador**: Se crea automáticamente en la fase 2
3. **Permisos**: Ejecuta `ASIGNAR_PERMISOS_SUPERADMIN.sql` después de crear todas las páginas

