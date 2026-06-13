# Sistema CIN - Sistema de Gestión Clínica

## 📚 Documentación Principal

### Sistema de Roles y Superadministrador

**`README_IMPLEMENTACION_ROLES_SUPERADMIN.md`** - Documentación completa del sistema de roles múltiples y Superadministrador.

Incluye:
- ✅ Guía de instalación y configuración
- ✅ Arquitectura del sistema
- ✅ Funcionalidades implementadas
- ✅ Reglas de negocio
- ✅ Solución de problemas

### Scripts SQL

**`app/varios/SQL/README.md`** - Guía de scripts SQL y fases de instalación.

---

## 🚀 Inicio Rápido

### Instalación de Base de Datos

```bash
# Ejecutar script maestro unificado (recomendado)
psql -U postgres -f app/varios/SQL/00_SCRIPT_MAESTRO_UNIFICADO.sql
```

### Ejecutar Aplicación

```bash
python run.py
```

---

## 📁 Estructura del Proyecto

```
clausys/
├── app/                    # Aplicación principal
│   ├── auth/              # Autenticación y autorización
│   ├── dao/               # Data Access Objects
│   ├── rutas/             # Rutas y controladores
│   ├── services/          # Servicios de negocio
│   ├── templates/         # Plantillas HTML
│   └── utils/             # Utilidades
├── app/varios/
│   ├── SQL/               # Scripts SQL
│   └── MD/                # Documentación adicional
└── README_IMPLEMENTACION_ROLES_SUPERADMIN.md  # Documentación principal
```

---

## 🔐 Roles del Sistema

- **Superadministrador**: Acceso total, único que puede crear usuarios
- **Administrador**: Acceso completo excepto creación de usuarios
- **Recepcionista**: Agendamiento y ventas básicas
- **Especialista**: Consultas médicas y agendamiento
- **Ventas**: Módulo de ventas completo

---

## 📝 Notas

- Consulta `README_IMPLEMENTACION_ROLES_SUPERADMIN.md` para documentación detallada
- Los scripts SQL están en `app/varios/SQL/`
- La documentación adicional está en `app/varios/MD/`

---

**Última actualización:** Enero 2025

