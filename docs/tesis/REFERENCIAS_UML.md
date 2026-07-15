# Referencias y dudas conceptuales de UML — para profundizar

Documento vivo, separado de las bitácoras de auditoría por capítulo (`0X_capituloX_*/`). Acá se registran preguntas conceptuales de modelado UML que surgen durante la nivelación, con la respuesta dada en el momento y una referencia para investigar más a fondo después (con tiempo, no en medio de una sesión de auditoría). No es una fuente citable tal cual para la tesis — hay que verificar cada referencia contra el material original antes de citarla formalmente.

---

## 1. Piscinas (swimlanes) en diagramas de actividad: ¿qué puede ser una piscina?

**Fecha:** 2026-07-09 (sesión de auditoría DA_AGENDAMIENTO)

**Pregunta:** ¿Por qué una piscina no puede ser un lugar físico (ej. "Consultorio/Clínica") y sí un rol/actor (ej. "Recepcionista")?

**Respuesta dada en el momento:** una piscina (`ActivityPartition`) se asocia a un *classifier* responsable de ejecutar las acciones que contiene — puede ser un actor, un rol, una unidad organizacional o un sistema, pero necesita agencia (poder ejecutar la acción). Un lugar físico sin agencia no encaja; una unidad organizacional como "Recepción" (el puesto/rol) sí.

**Fuentes citadas de memoria (sin verificar página exacta — pendiente de chequear antes de citar en la tesis):**
- OMG UML Superstructure Specification — sección de *Activities*, concepto `ActivityPartition`
- Martin Fowler, *UML Distilled*
- Booch/Rumbaugh/Jacobson, *The Unified Modeling Language User Guide*

**Pendiente de investigar:** confirmar la definición exacta de `ActivityPartition` en la spec de OMG (versión vigente, UML 2.5.1) y buscar el capítulo/página específica en Fowler y en Booch et al. para poder citarlos correctamente en el marco teórico de la tesis.

**Decisión práctica tomada (independiente de la discusión teórica):** para DA_AGENDAMIENTO, las piscinas quedan **PACIENTE / RECEPCION / SISTEMA** (ver actualización 2026-07-11 más abajo — se descartó `ESPECIALISTA` como tercera piscina porque en ese diagrama no tiene acciones propias, y se reemplazó por `SISTEMA` para reflejar la automatización real de recordatorios y generación de slots), en base a evidencia de código (rol `RECEPCION` en `role_required(...)` de `cita_api.py`, `agenda_horarios_api.py`, `lista_espera_api.py`; automatización en `CitaDao.cambiarEstadoCita()`, `app/tasks/recordatorio_tasks.py`), no solo por el argumento teórico de la convención UML.

---

## 2. Nomenclatura de actor: "Médico" vs. "Especialista" — convención global para todo el UML

**Fecha:** 2026-07-11

**Pregunta:** el sistema real no usa el rol "Médico", usa "Especialista" (`id_especialista`, `especialista_especialidades`, `FuncionarioDao.getEspecialistasActivos()`). ¿Hay que corregir esto en todos los diagramas del UML, no solo en el que se está auditando?

**Respuesta:** sí, pero con un límite claro para no sobre-corregir:

- **SÍ se renombra** cuando "Médico" aparece como **actor/piscina** — es decir, como sujeto que ejecuta una acción o es dueño de un caso de uso. Ahí el término correcto y consistente con el código es `ESPECIALISTA`.
- **NO se toca** cuando "médico" aparece como **adjetivo de una entidad o documento del dominio** — `ficha médica`, `certificado médico`, `orden médica`, `tipo_certificado_medico`. Esos nombres son correctos y coinciden con nombres reales de tabla/entidad en el código. Renombrarlos sería un error (cambiaría el significado del dato, no del actor).

**Evidencia de que el documento original ya apuntaba a "Especialista"**: TALLER.MD usa "Especialista" como actor en la enorme mayoría de las especificaciones de CU (líneas 759, 774, 805, 821, 836, 855, 870, 890, 1201, 1205, 1209, 1213, 1217, 1221, 1225, entre otras — patrón "Él especialista registra/genera..."). Solo desliza "médico" sueltamente en un par de frases de prosa (ej. línea 2280, dentro de una lista de datos de cita). Esto confirma que el UML se desvió del documento fuente en los diagramas donde puso "Médico" como piscina, no al revés.

**Diagramas ya identificados con este problema (a corregir uno por uno, en el orden de la metodología, no todos de una):**

| Diagrama | Estado |
|---|---|
| DA_AGENDAMIENTO | Corregido — pasa a `SISTEMA`, no queda actor "Médico" (ver `02_capitulo2_agendamiento/00_diagrama_actividades.md`) |
| DA_CONSULTORIO | Pendiente — lanes actuales `PACIENTE, MEDICO, CONSULTORIO`; se corrige en Fase 2.2 |
| DC_GESTIONAR_CONSULTORIO / DCU_REF_CONSULTORIO (casos de uso) | No verificado aún — pendiente cuando se audite Análisis 3 |
| Diagrama de secuencia / clase "Registrar Cita" (TALLER.MD línea 371, 2326-2331) | No verificado — revisar cuando se audite ese CU puntual |

**No es un search-and-replace global de una sola vez** — cada diagrama se corrige cuando le toca su turno en la metodología (uno por uno, con aprobación tuya), para no romper la trazabilidad de la bitácora.

---

## 3. (siguiente pregunta a registrar acá cuando surja)
