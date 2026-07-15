# Mejoras fuera del alcance original — SYSCOMcli

Funcionalidades que **existen y funcionan en el código**, pero no forman parte de los requisitos relevados en `TALLER.MD` ni de los diagramas de diseño base. Se implementaron por iniciativa propia durante el desarrollo. No se documentan en los capítulos de nivelación (esos capítulos comparan el UML contra el diseño original) — se registran acá aparte, como anexo, para no perder el trabajo ni la trazabilidad.

**Cuándo se agregan al documento de tesis:** recién cuando termine la adaptación del UML principal (todos los capítulos 1-4 cerrados). No antes — evita mezclar "lo que el diseño pedía" con "lo que agregué yo" mientras todavía se está nivelando lo primero.

---

## 1. Lista de Espera (Agendamiento)

**Fecha de decisión:** 2026-07-14

**Qué es:** cuando no hay slots disponibles para un especialista/horario, el paciente puede anotarse en una lista de espera. Recepción gestiona el ciclo de estados manualmente (`PENDIENTE → NOTIFICADO → ACEPTADO / EXPIRADO / CANCELADO`) cuando se libera un cupo.

**Por qué queda fuera del diseño base:** se revisó `TALLER.MD` línea por línea en los CU "Registrar Citas" y "Gestión de Avisos Recordatorios" (líneas 2236-2402) y la lista de espera no aparece en ningún lado — ni como requisito, ni como caso de uso, ni mencionada en la prosa. El documento original solo contempla reservación, confirmación, anulación y reagendamiento de citas.

**Justificación (si preguntan en la defensa):** el propio `TALLER.MD` cita como referencia de industria a agendapro.com (línea 638-648), que menciona explícitamente la reducción de inasistencias y mejor aprovechamiento de la agenda como objetivo de un sistema de este tipo. La lista de espera es una extensión natural de esa idea — implementada por decisión propia, no por requisito del cliente/documento original.

**Evidencia de código:**
- `app/dao/agendamiento/lista_espera/ListaEsperaDao.py`
- `app/rutas/agendamiento/lista_espera/lista_espera_api.py` (blueprint `listaesperaapi`, prefijo `/agendamiento/lista-espera`)
- Tabla `lista_espera`, validada en Fase B.4 (ver memoria de proyecto)

**Estado en el diagrama DA_AGENDAMIENTO:** no se dibuja. La decisión "¿Hay slot disponible?" → NO termina en un Final simple (sin cita agendada), sin rama de lista de espera. Ver `02_capitulo2_agendamiento/00_diagrama_actividades.md` §3.

**Pendiente:** cuando cierres la adaptación completa del UML, agregar acá (o como anexo del capítulo de Agendamiento) un diagrama de actividad aparte solo para este flujo, documentado explícitamente como mejora fuera de alcance.

---

## 2. (próxima mejora fuera de alcance a registrar acá, si aparece)
