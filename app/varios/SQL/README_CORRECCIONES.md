# Scripts SQL de Corrección

## 📋 Scripts Disponibles

### `FIX_CORRECCIONES_SEGURIDAD.sql`
**Script unificado con todas las correcciones de seguridad**

Incluye:
- ✅ Corrección de vista `v_usuarios_seguridad` (incluye `usu_clave`)
- ✅ Configuración de contraseñas sin expiración para todos los usuarios
- ✅ Verificaciones

**Cuándo ejecutar:**
- Después de crear la BD si la vista no funciona correctamente
- Si necesitas desactivar expiración de contraseñas para todos los usuarios
- Si obtienes error "no existe la columna usu_clave" en login

**Ejecutar:**
```sql
\i app/varios/SQL/FIX_CORRECCIONES_SEGURIDAD.sql
```

## 📝 Notas

- El script principal `02_FASE_2_SEGURIDAD_USUARIOS.sql` ya incluye la vista correcta
- Este script de corrección es solo para aplicar después si es necesario
- Es seguro ejecutarlo múltiples veces (usa `DROP VIEW IF EXISTS` y `UPDATE` condicional)









