# Estructura del Módulo de Autenticación

## 📁 Módulo Centralizado: `app/auth/`

Se ha creado un módulo centralizado `app/auth/` que actúa como punto de entrada único para todas las funcionalidades de autenticación y seguridad.

## ✅ Ventajas

1. **Importaciones simplificadas:**
   ```python
   # ANTES (disperso):
   from app.rutas.seguridad.login_routes import logmod
   from app.services.auth_service import AuthService
   from app.dao.seguridad.auth_dao import AuthDao
   from app.middleware.auth_middleware import verificar_sesion_mejorada
   
   # AHORA (centralizado):
   from app.auth import login_blueprint, AuthService, AuthDao, verificar_sesion_mejorada
   ```

2. **Organización clara:** Todo lo relacionado con auth en un solo lugar conceptual
3. **Sin romper código:** Los archivos físicos se mantienen donde están
4. **Fácil migración:** Puedes migrar gradualmente los imports

## 📋 Ubicaciones Físicas (Se Mantienen)

Los archivos físicos **NO se mueven**, solo se centralizan las importaciones:

- `app/rutas/seguridad/login_routes.py` → `app.auth.login_blueprint`
- `app/rutas/seguridad/auth_api.py` → `app.auth.auth_api_blueprint`
- `app/rutas/seguridad/admin_auth_api.py` → `app.auth.admin_auth_api_blueprint`
- `app/services/auth_service.py` → `app.auth.AuthService`
- `app/dao/seguridad/auth_dao.py` → `app.auth.AuthDao`
- `app/dao/seguridad/usuario/UsuarioDao.py` → `app.auth.UsuarioDao`
- `app/middleware/auth_middleware.py` → `app.auth.verificar_sesion_mejorada`
- `app/tasks/auth_tasks.py` → `app.auth.limpiar_sesiones_expiradas`
- `app/utils/auth.py` → `app.auth.role_required`
- `app/utils/password_validator.py` → `app.auth.validar_politica_password`

## 🔄 Uso

### Opción 1: Usar el módulo centralizado (Recomendado para código nuevo)
```python
from app.auth import AuthService, AuthDao, role_required
```

### Opción 2: Usar imports directos (Sigue funcionando)
```python
from app.services.auth_service import AuthService
from app.dao.seguridad.auth_dao import AuthDao
```

## 📝 Nota

Este módulo es un **wrapper/fachada** que no mueve archivos físicos, solo centraliza las importaciones. Esto permite:
- ✅ Mantener compatibilidad con código existente
- ✅ Facilitar futuras migraciones
- ✅ Organizar conceptualmente el código
- ✅ No romper nada existente









