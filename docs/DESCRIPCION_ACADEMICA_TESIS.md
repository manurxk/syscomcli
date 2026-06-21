# Sistema de Gestión Clínica Integral (SYSCOMcli)
## Descripción Académica — Tesis de Grado Universitaria

---

## 1. Presentación del Proyecto

**SYSCOMcli** (Sistema de Gestión Clínica Integral) es una aplicación web desarrollada como trabajo de tesis de grado universitaria, orientada a resolver una problemática real en el sector de la salud: la ausencia de herramientas digitales accesibles para la gestión administrativa y clínica en centros médicos de pequeña y mediana escala.

El sistema fue concebido, diseñado e implementado íntegramente por el autor, aplicando principios y metodologías adquiridos a lo largo de la carrera universitaria. Abarca desde el agendamiento de pacientes hasta la emisión de documentos clínicos y la gestión comercial, constituyendo un sistema ERP (Enterprise Resource Planning) orientado al sector salud.

---

## 2. Planteamiento del Problema

Los centros médicos, consultorios y clínicas privadas de pequeña escala frecuentemente operan con procesos manuales o con herramientas tecnológicas fragmentadas (planillas, agendas físicas, software desconectados entre sí). Esta situación genera:

- **Pérdida de información clínica** por ausencia de registros digitales centralizados.
- **Ineficiencia operativa** en el agendamiento y seguimiento de citas.
- **Errores administrativos** en la facturación y control de cajas.
- **Falta de trazabilidad** en el historial médico de los pacientes.
- **Comunicación deficiente** entre médicos y personal administrativo.

SYSCOMcli propone una solución integral, modular y escalable que digitaliza y unifica estos procesos en una única plataforma web.

---

## 3. Objetivos

### 3.1 Objetivo General

Desarrollar un sistema web de gestión clínica integral que permita administrar de forma eficiente los procesos administrativos, clínicos y comerciales de un centro médico, aplicando principios de arquitectura de software y buenas prácticas de ingeniería.

### 3.2 Objetivos Específicos

1. Diseñar e implementar una arquitectura de software en capas que separe responsabilidades entre acceso a datos, lógica de negocio y presentación.
2. Desarrollar un módulo de agendamiento médico con control de disponibilidad y notificaciones automáticas.
3. Implementar un sistema de fichas clínicas digitales que registre el historial completo del paciente.
4. Construir un módulo de ventas y tesorería para la gestión de presupuestos, facturas y control de cajas.
5. Aplicar un sistema de control de acceso basado en roles (RBAC) que garantice la seguridad y confidencialidad de la información.
6. Integrar servicios externos para el envío de recordatorios automáticos de citas vía WhatsApp.
7. Contenerizar la aplicación mediante Docker para facilitar su despliegue en diferentes entornos.

---

## 4. Justificación Académica

Este proyecto integra conocimientos de múltiples áreas de la ingeniería de software:

| Área de Conocimiento | Aplicación en el Proyecto |
|---|---|
| Programación Orientada a Objetos | Clases DAO, Services y Controllers |
| Bases de Datos Relacionales | Modelo entidad-relación en PostgreSQL |
| Desarrollo Web | Backend con Flask, Frontend con Jinja2 + Bootstrap |
| Arquitectura de Software | Patrón MVC + capas DAO/Service |
| Seguridad Informática | Autenticación JWT, CSRF, RBAC |
| Integración de Servicios | API REST, WhatsApp, generación de PDFs |
| DevOps / Despliegue | Contenedores Docker y Docker Compose |
| Ingeniería de Requisitos | Levantamiento y documentación de módulos funcionales |

---

## 5. Marco Tecnológico

### 5.1 Lenguaje y Framework Principal

- **Python 3.x**: Lenguaje de programación principal, elegido por su legibilidad, amplio ecosistema y soporte para desarrollo web.
- **Flask**: Microframework web de Python. Se optó por Flask en lugar de frameworks más pesados (como Django) para tener control explícito sobre cada componente de la arquitectura, lo cual resulta didácticamente más valioso en un contexto académico.

### 5.2 Base de Datos

- **PostgreSQL**: Sistema de gestión de bases de datos relacional de código abierto, robusto y ampliamente utilizado en entornos de producción. Se optó por SQL directo (sin ORM) para demostrar dominio del lenguaje de consulta y del diseño relacional.

### 5.3 Frontend

- **Jinja2**: Motor de plantillas integrado con Flask para la generación de HTML dinámico en el servidor (SSR — Server Side Rendering).
- **Bootstrap 5**: Framework CSS para el diseño responsive y componentes visuales.
- **jQuery + DataTables**: Para interactividad del lado del cliente y manejo de tablas de datos con paginación, búsqueda y ordenamiento.

### 5.4 Librerías Complementarias

| Librería | Propósito |
|---|---|
| `APScheduler` | Tareas programadas en background (recordatorios de citas) |
| `PyJWT` | Generación y validación de tokens de autenticación |
| `Flask-WTF` | Protección CSRF en formularios |
| `ReportLab` / `WeasyPrint` | Generación de documentos PDF |
| `psycopg2` | Conector Python-PostgreSQL |
| `Ultramsg` / `Twilio` | Envío de mensajes WhatsApp |

### 5.5 Infraestructura

- **Docker**: Contenerización de la aplicación para entornos reproducibles.
- **Docker Compose**: Orquestación de múltiples servicios (aplicación + base de datos).

---

## 6. Arquitectura del Sistema

El sistema sigue una **Arquitectura en Capas** combinada con el patrón **MVC (Model-View-Controller)** adaptado a Flask:

```
┌─────────────────────────────────────────────────────┐
│                   CAPA DE PRESENTACIÓN               │
│          Plantillas HTML Jinja2 + Bootstrap 5        │
└────────────────────────┬────────────────────────────┘
                         │ HTTP Request / Response
┌────────────────────────▼────────────────────────────┐
│                  CAPA DE CONTROL                     │
│        Blueprints Flask + API REST (/api/v1/)        │
│     Middleware de Autenticación y Autorización       │
└────────────────────────┬────────────────────────────┘
                         │ Llamadas internas
┌────────────────────────▼────────────────────────────┐
│                CAPA DE SERVICIOS                     │
│           Lógica de negocio pura (Services)          │
│           Tareas programadas (APScheduler)           │
└────────────────────────┬────────────────────────────┘
                         │ Consultas de datos
┌────────────────────────▼────────────────────────────┐
│              CAPA DE ACCESO A DATOS (DAO)            │
│         Data Access Objects — SQL directo            │
│           Pool de conexiones a PostgreSQL            │
└────────────────────────┬────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────┐
│                  BASE DE DATOS                       │
│              PostgreSQL — Modelo Relacional           │
└─────────────────────────────────────────────────────┘
```

### 6.1 Patrones de Diseño Aplicados

**Patrón DAO (Data Access Object):**  
Cada entidad del dominio posee su propia clase DAO que encapsula todas las operaciones de base de datos. Esto desacopla la lógica de negocio de la persistencia, facilitando el mantenimiento y la testabilidad. Ejemplo: `PacienteDao`, `CitaDao`, `RecetaDao`.

**Patrón Blueprint (Flask):**  
La aplicación se organiza en Blueprints independientes por dominio funcional. Cada módulo tiene su propio Blueprint para rutas HTML y otro para la API REST. Esto permite el desarrollo modular y la separación clara de responsabilidades.

**Patrón RBAC (Role-Based Access Control):**  
El control de acceso se implementa mediante roles asignados a usuarios. Cada ruta está decorada con verificaciones de rol, garantizando que solo el personal autorizado acceda a cada funcionalidad.

**Patrón de Tareas Programadas:**  
Se utiliza APScheduler para ejecutar tareas en background: envío de recordatorios de citas, limpieza de tokens expirados y actualización de estados de presupuestos.

---

## 7. Módulos Funcionales del Sistema

### 7.1 Módulo de Agendamiento

Gestiona la disponibilidad de los médicos especialistas y la programación de citas.

- Configuración de agenda médica por especialista y turno
- Creación, modificación y cancelación de citas
- Validación de disponibilidad en tiempo real
- Envío automático de recordatorios vía WhatsApp (24 horas antes)
- Vista de calendario por especialista

### 7.2 Módulo de Consultorio (Atención Clínica)

Centraliza la información generada durante la consulta médica.

- **Fichas clínicas**: Anamnesis, signos vitales, diagnóstico, evolución
- **Recetas médicas**: Registro de medicamentos, dosis e indicaciones
- **Órdenes de estudio**: Solicitud de análisis y estudios complementarios
- **Derivaciones**: Referencia de pacientes a otros especialistas
- **Certificados médicos**: Generación de documentos oficiales
- **Historial clínico completo** del paciente

### 7.3 Módulo de Gestión de Personas

Administra los actores del sistema.

- **Pacientes**: Registro, historial, datos demográficos, documentación
- **Funcionarios**: Personal médico y administrativo
- **Usuarios del sistema**: Cuentas de acceso con roles asignados

### 7.4 Módulo de Ventas y Tesorería

Gestiona la dimensión comercial y financiera de la clínica.

- Presupuestos con estados (Pendiente, Aprobado, Rechazado, Vencido)
- Pedidos y órdenes de servicio
- Facturación (compatible con SIFEN — facturación electrónica Paraguay)
- Notas de crédito y débito
- Cobranzas
- Apertura y cierre de cajas
- Arqueo de caja
- Libro de ventas

### 7.5 Módulo de Referenciales (Datos Maestros)

Administra las tablas de configuración del sistema.

- Especialidades médicas, días y horarios
- Medicamentos y principios activos
- Diagnósticos, síntomas, signos vitales
- Ciudades, géneros, estado civil
- Tipos de análisis, estudios y procedimientos
- Configuración de impuestos, monedas y condiciones de pago

---

## 8. Modelo de Seguridad

La seguridad del sistema se aborda en múltiples niveles:

### 8.1 Autenticación
- Autenticación por sesión de Flask con cookies seguras
- Tokens JWT para endpoints de la API REST
- Expiración automática de sesiones inactivas
- Limpieza periódica de tokens mediante tareas programadas

### 8.2 Autorización — Control de Acceso Basado en Roles (RBAC)

| Rol | Permisos Principales |
|---|---|
| **Superadministrador** | Acceso total; único rol que puede crear usuarios |
| **Administrador** | Acceso completo a todos los módulos |
| **Recepcionista** | Agendamiento, registro de pacientes, ventas básicas |
| **Especialista / Médico** | Consulta médica, fichas, recetas, sus propios pacientes |
| **Ventas / Tesorería** | Módulo comercial completo |

### 8.3 Protección de Formularios
- Protección CSRF (Cross-Site Request Forgery) mediante Flask-WTF en todos los formularios
- Validación de entradas del lado del servidor

---

## 9. Estructura del Proyecto

```
syscomcli/
├── run.py                          # Punto de entrada de la aplicación
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno (excluido del control de versiones)
├── app/
│   ├── __init__.py                 # Inicialización de Flask y registro de Blueprints
│   ├── config/                     # Configuración de la aplicación
│   ├── conexion/                   # Gestión del pool de conexiones PostgreSQL
│   ├── auth/                       # Módulo de autenticación (JWT, middleware, tareas)
│   ├── dao/                        # Capa de acceso a datos
│   │   ├── gestionar_personas/     # DAOs de Pacientes, Funcionarios, Usuarios
│   │   ├── modulos/                # DAOs de módulos de negocio
│   │   └── referenciales/          # DAOs de tablas maestras
│   ├── rutas/                      # Controladores y endpoints
│   │   ├── seguridad/              # Login, manejo de errores
│   │   ├── dashboard/              # Panel principal
│   │   ├── gestionar_personas/     # CRUD de personas
│   │   ├── modulos/                # Agendamiento, Consultorio, Ventas
│   │   └── referenciales/          # Maestros configurables
│   ├── services/                   # Lógica de negocio y automatizaciones
│   ├── tasks/                      # Tareas programadas (recordatorios)
│   ├── utils/                      # Decoradores, helpers, validadores
│   ├── static/                     # CSS, JavaScript, imágenes, vendors
│   ├── templates/                  # Plantillas HTML Jinja2
│   └── varios/
│       ├── SQL/                    # Scripts de instalación y migración de BD
│       └── MD/                     # Documentación técnica interna
├── dock/                           # Configuración Docker y Docker Compose
├── docs/                           # Documentación del proyecto
└── tests/                          # Pruebas unitarias e integración
```

---

## 10. Metodología de Desarrollo

El proyecto fue desarrollado siguiendo un enfoque **iterativo e incremental**, organizado en fases:

- **Fase 1**: Arquitectura base — estructura de proyecto, autenticación, roles y acceso a base de datos.
- **Fase 2**: Implementación de módulos clínicos y mejoras del sistema de agendamiento. Integración de relación paciente-profesional (muchos a muchos).
- **Fase 3** (en curso): Modernización del frontend con migración a Bootstrap 5, rediseño de interfaces y mejoras de experiencia de usuario.

---

## 11. Conclusión

SYSCOMcli es el resultado de la aplicación práctica de conocimientos teóricos adquiridos durante la carrera universitaria. El proyecto demuestra competencias en:

- Diseño de arquitecturas de software escalables y mantenibles
- Modelado de bases de datos relacionales complejas
- Desarrollo full-stack (backend + frontend) con tecnologías modernas
- Implementación de seguridad en aplicaciones web
- Integración de servicios externos (mensajería, generación de documentos)
- Contenerización y despliegue de aplicaciones
- Resolución de problemas reales mediante tecnología

El sistema fue construido con enfoque en la calidad del código, la separación de responsabilidades y la escalabilidad, características que lo hacen apto no solo como proyecto académico sino como solución real para centros médicos.

---

*Documento elaborado como parte del trabajo de Tesis de Grado Universitaria.*  
*Autor: Manuel Ramirez*  
*Fecha: Junio 2026*
