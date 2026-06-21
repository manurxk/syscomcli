# Análisis de Estructura - Sistema CIN (Sysclin)

Este documento detalla la arquitectura, tecnologías y el estado actual del **Sistema CIN**, un ecosistema de gestión clínica integral.

## 🌟 Resumen del Proyecto
**Sistema CIN** es una plataforma diseñada para digitalizar y optimizar la operativa de centros médicos. Cubre desde el agendamiento inicial hasta la facturación, pasando por la consulta médica y el historial clínico digital.

## 🛠️ Stack Tecnológico
- **Backend**: Python 3.x con **Flask**.
- **Base de Datos**: PostgreSQL (conectividad vía `psycopg2`).
- **Frontend**: Plantillas **Jinja2** con **Bootstrap 5** (Migración Fase 3 en curso).
- **Tareas Programadas**: **APScheduler** (recordatorios de citas, limpieza de tokens).
- **Documentación**: ReportLab / WeasyPrint / xhtml2pdf (Recetas, Informes, Presupuestos).
- **Notificaciones**: Integración con **WhatsApp** (Ultramsg / pywhatkit).
- **Despliegue**: Soporte para **Docker** (Docker Compose + PostgreSQL).

## 🏗️ Arquitectura del Software
El proyecto implementa un patrón modular y escalable para separar responsabilidades:

### 📂 Estructura de Directorios
- **`app/`**: Núcleo de la aplicación.
  - **`auth/`**: Gestión de seguridad y sesiones.
  - **`dao/` (Data Access Objects)**: Capa de persistencia (Consultas SQL directas).
  - **`rutas/`**: Controladores que gestionan las peticiones HTTP (Blueprints).
    - `referenciales/`: Módulos maestros (Ciudades, Especialidades, Formas de Cobro).
    - `modulos/`: Procesos de negocio (Agenda, Cita, Consulta, Ventas, Facturación).
    - `gestionar_personas/`: Gestión de Pacientes y Funcionarios.
  - **`services/`**: Lógica de negocio pura que coordina DAOs y rutas.
  - **`templates/`**: Vistas HTML organizadas por funcionalidad.
  - **`static/`**: Recursos estáticos (CSS personalizado, JS, imágenes).
- **`dock/`**: Configuración de contenedores para entornos de desarrollo/producción.
- **`scripts/`**: Automatizaciones para mantenimiento y migración visual.

## 🚀 Lo que estás haciendo (Contexto Actual)
Basado en los archivos analizados (`migrar_fase3_bootstrap5.py`, `original_presupuesto.html`), he identificado que te encuentras en una etapa crítica de:

1.  **Modernización Visual**: Migrando formularios complejos de Bootstrap antiguo a **Bootstrap 5**, con un enfoque en diseño "Premium" y "Clean".
2.  **Unificación de Experiencia**: Rediseñando la **Ficha Médica** para que funcione como un expediente digital moderno con navegación por pestañas (Anamnesis, Evolución, Diagnóstico).
3.  **Refactorización de Formularios**: Implementando layouts de doble columna para manejar la extensa carga de datos clínicos de forma ergonómica.
4.  **Automatización de Procesos**: Refinando el flujo de Ventas (Facturación, Cobros, Arqueo de Caja) e integrando recordatorios automáticos para reducir el ausentismo de pacientes.

## 🔐 Seguridad y Control
El sistema posee un robusto control de acceso basado en roles:
- **Superadministrador**: Gestión total de usuarios y sistema.
- **Administrador**: Gestión operativa completa.
- **Recepcionista**: Foco en flujo de pacientes y agenda.
- **Especialista**: Gestión clínica y fichas médicas.
- **Ventas**: Gestión comercial y tesorería.

---
*Este análisis refleja una estructura madura, orientada a la mantenibilidad mediante la separación de lógica de datos (DAO) y lógica de presentación (Templates/Rutas).*
