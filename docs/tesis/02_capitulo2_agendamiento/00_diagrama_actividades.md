# DA_AGENDAMIENTO — Rediseño aprobado (Fase 2.1)

Bitácora de decisión final para editar en la herramienta UML. Base: diagrama original pegado el 2026-07-09, cruzado contra `TALLER.MD` y código real (`app/dao/agendamiento/`, `app/rutas/agendamiento/`, `app/dao/clinico/`). Metodología y veredictos completos de la discusión en el hilo de chat del 2026-07-09 — este documento es el resultado ya aprobado, no el análisis completo.

---

## 1. Piscinas (swimlanes)

**Antes:** `PACIENTE`, `CONSULTORIO/RECEPCION`, `MEDICO`

**Después (DECISIÓN FINAL):** `PACIENTE`, `RECEPCION`, `SISTEMA`

**Motivo:** una piscina representa un actor con agencia (rol que ejecuta la acción), no un lugar físico. `Consultorio` en el código es una entidad referencial (`mantenimiento/referenciales/consultorio/ConsultorioDao.py`), un dato que se asigna a un horario (`id_consultorio` en `agenda_horarios`), no un actor. El actor real que gestiona citas y horarios está confirmado por control de acceso en código: `role_required("ADMINISTRADOR", "SUPERADMIN", "RECEPCION")` en `cita_api.py`, `agenda_horarios_api.py`, `lista_espera_api.py`.

`ESPECIALISTA` se descartó como tercera piscina porque en este diagrama específico queda sin ninguna acción propia (su disponibilidad la carga Recepción; su participación clínica real empieza en DA_CONSULTORIO). El tutor pidió mantener 3 piscinas, así que se reemplaza por `SISTEMA` — que sí tiene acciones propias con evidencia de código: generación automática de slots, validación de conflictos, generación automática de recordatorios y el job programado que los envía por WhatsApp. `SISTEMA` cumple la misma regla de agencia (ejecuta autónomamente, sin trigger humano por paso) que ya se usó para descartar "lugar físico" como piscina — ver `docs/tesis/REFERENCIAS_UML.md` §1.

---

## 2. Flujo completo rediseñado

### Lane RECEPCION → SISTEMA — arranque (disponibilidad)

1. **(Initial, lane RECEPCION)** Recepción registra la disponibilidad del especialista (día, horario, consultorio)
   - Evidencia: `POST /agendamiento/agenda-horarios` (`AgendaHorariosDao`)
   - Reemplaza: "Médico remite su disponibilidad" + "Recibe datos del médico" + "Registrar la hora, turno, día..." — ya no es el especialista quien inicia, y "turno/día/bloque horario" quedan fusionados en un solo concepto (`agenda_horarios`)
2. **(lane SISTEMA)** Sistema valida que no haya conflicto de horario y genera automáticamente los slots disponibles del horizonte configurado
   - Evidencia: `validarConflictoHorario`, `AgendaHorariosDao._generarSlots` (tabla `slots_agenda`)
3. **(Final)** Horario y slots quedan confirmados/disponibles

### Lane PACIENTE → RECEPCION — solicitud de cita

4. **(Initial)** Paciente solicita una cita
5. Recepción recibe la solicitud
6. Recepción pregunta si es primera consulta o de seguimiento
7. Recepción busca slots disponibles (especialista + horario + consultorio ya vienen juntos en el slot — no existe un paso separado de "asignar especialista")
   - Evidencia: `GET /citas/slots-disponibles`
8. **(Decision)** ¿Hay slot disponible?
   - **SI** → continúa en paso 9
   - **NO** → vuelve al paso 7 (Recepción prueba con otra fecha/horario) — coincide con el comportamiento real: en `cita-agregar.html`, cambiar la fecha vuelve a consultar `GET /citas/slots-disponibles`, no corta el proceso. No hay Final en esta rama.

9. Recepción registra los datos de la cita y del paciente
   - Evidencia: `POST /citas`
10. Paciente confirma sus datos personales
11. Recepción confirma la fecha de la cita
12. **(Decision)** ¿Se confirma la consulta?
    - **SI** → Recepción marca la cita como `CONFIRMADA` → dispara automáticamente la rama de recordatorios (sección 3) → **(Final)**
    - **NO** → Recepción reagenda (nuevo slot, mismo paciente/especialista) o anula la cita (`CANCELADA`, libera el slot) → **(Final)**
    - Evidencia: `PATCH /citas/<id>/estado`, `PUT /citas/<id>` (reprogramación)

**Eliminado de este bloque:** los dos finales redundantes que tenía el original (`Se Confirma la consulta` con doble salida) se fusionan en uno solo por rama.

### Lane SISTEMA — recordatorios (automático)

**Rediseño completo de este bloque** — en el original era una negociación manual ESPECIALISTA↔RECEPCION↔PACIENTE; en el código es automático, sin intervención humana:

13. Sistema genera 2 recordatorios: 1440 min y 120 min antes de la cita, disparado por el paso 12-SI (cita pasa a `CONFIRMADA`)
    - Evidencia: dentro de `CitaDao.cambiarEstadoCita()` al pasar a `CONFIRMADA`
14. Sistema (job programado cada 10 min) detecta recordatorios en ventana vencida y los envía por WhatsApp
    - Evidencia: `app/tasks/recordatorio_tasks.py` (`procesar_recordatorios_pendientes`), `UltraMsgService`, registrado en `run.py` vía `BackgroundScheduler`
15. Paciente recibe la notificación de su próxima cita → **(Final)**

**Eliminado completo de este bloque:** "Médico solicita y confirma próxima cita", "Recibe confirmación del médico", "Se registran los detalles, fecha, día, turno..." — no existen como pasos manuales en el sistema real.

### Eliminado por completo de este diagrama

- Todo el bloque de **ficha médica / anamnesis** ("Médico realiza ficha médica...", "Paciente describe todos sus datos, alergias...", "Médico registra...", "Ficha médica registrado") — pertenece al dominio clínico (`AnamnesisDao`, `FichaDao`, disparado desde `POST /citas/<id>/iniciar-consulta`). Pasa a DA_CONSULTORIO (Fase 2.2).
- Los dos `Initial` redundantes (`Initial3`/`Initial4`) que apuntaban ambos a la ficha médica.
- Los finales duplicados (`FinalState2`/`FinalState6` de ficha médica, ya no aplica al eliminarse el bloque).

---

## 3. Lista de Espera — QUEDA FUERA de este diagrama (decisión 2026-07-14)

**Decisión:** la Lista de Espera **no se dibuja en DA_AGENDAMIENTO**. El código queda tal cual está (`ListaEsperaDao`, `lista_espera_api.py`, CRUD completo, ya validado en Fase B.4) — no se toca ni se borra nada del sistema. Lo que cambia es solo la documentación de tesis: esta funcionalidad no está contemplada en `TALLER.MD` (se revisó línea por línea el CU "Registrar Citas" y "Avisos Recordatorios" y no aparece en ningún lado del documento de diseño original), así que incluirla en el diagrama que se supone nivela contra ese documento generaría una pregunta incómoda en la defensa ("¿por qué esto no está en el diseño que dijiste que seguiste?").

**Tratamiento:** se documenta aparte como mejora del alumno por fuera del alcance original — ver `docs/tesis/MEJORAS_FUERA_DE_ALCANCE.md`. Se agrega a ese documento (como diagrama/anexo opcional) recién **cuando termines de adaptar el UML principal**, no ahora.

**Para tu tesis, si te preguntan:** la Lista de Espera es una funcionalidad implementada por iniciativa propia, inspirada en la referencia de industria citada en el propio `TALLER.MD` (agendapro.com, sección sobre reducción de inasistencias), pero no fue parte de los requisitos originales relevados — por eso no figura en los diagramas de diseño base.

---

## 4. Resumen de piscinas y conteo final (para cuando redibujes)

| Piscina | Acciones que le quedan |
|---|---|
| PACIENTE | Solicita cita, confirma datos, confirma/no confirma consulta, recibe notificación |
| RECEPCION | Registra disponibilidad, recibe solicitud, pregunta tipo de consulta, busca slot, registra cita, confirma fecha, reagenda/anula |
| SISTEMA | Valida conflicto y genera slots, genera recordatorios automáticos al confirmar cita, ejecuta el job programado, envía WhatsApp |

`ESPECIALISTA` no aparece en DA_AGENDAMIENTO — reaparece en DA_CONSULTORIO (Fase 2.2), donde sí tiene acciones propias (atender, diagnosticar, recetar, etc.).

---

## 5. Guía paso a paso para editar en tu herramienta UML

Orden sugerido para no perder nada:

1. **Renombrar piscinas**: `CONSULTORIO/RECEPCION` → `RECEPCION`, `MEDICO` → `SISTEMA`. La piscina `PACIENTE` no cambia de nombre.
2. **Borrar el bloque de ficha médica completo**: las 4 acciones de "Médico realiza ficha médica / Paciente describe datos / Médico registra / Ficha médica registrado", sus 2 `Initial` (`Initial3`, `Initial4`) y sus 2 finales (`FinalState2`, `FinalState6`). Ese bloque se documenta en DA_CONSULTORIO, no acá.
3. **Borrar el bloque manual de "próxima cita"**: "Médico solicita y confirma próxima cita", "Recibe confirmación del médico", "Se registran los detalles, fecha, día, turno...".
4. **Mover a la piscina SISTEMA** las acciones nuevas: "Sistema valida conflicto y genera slots" (junto al bloque de disponibilidad) y "Sistema genera recordatorios" + "Job programado envía WhatsApp" (reemplazando el bloque borrado en el punto 3).
5. **Conectar** el paso "Se confirma la consulta" (RECEPCION) → "Sistema genera recordatorios" (SISTEMA) → "Job programado envía WhatsApp" (SISTEMA) → "Paciente recibe la notificación" (PACIENTE) → Final.
6. **Quitar el paso independiente "Se procede a la asignación de un especialista"**: fusionarlo con "Gestionar citas / buscar slot disponible" (RECEPCION) — el especialista queda implícito en el slot elegido, no es un paso separado.
7. **Unificar finales duplicados**: "Se Confirma la consulta" tenía 2 finales (`FinalState1`, `FinalState4`) — dejar solo uno.
8. ~~Agregar la rama nueva de Lista de Espera~~ — **revertido 2026-07-14**: la Lista de Espera queda fuera de este diagrama (ver sección 3 y `MEJORAS_FUERA_DE_ALCANCE.md`). El punto 8-NO va directo a un loop de reintento hacia "Recepción busca slots disponibles", no a una rama nueva.
9. **Revisar conteo final**: 3 piscinas (PACIENTE, RECEPCION, SISTEMA), sin piscina vacía, sin finales ni inicios duplicados.

---

## 6. Estado

**CERRADO ✅ — 2026-07-14.** Diagrama final validado por captura: 2 arranques (RECEPCION para disponibilidad, PACIENTE para solicitud de cita), bucle de reintento en "¿Hay slot disponible?", sin lista de espera, sin bloque de ficha médica, uso correcto de Flow Final vs. Activity Final, piscina `SISTEMA` (no `SYSCOMCLI`, corregido). Sin nodos sin salida. Pasa a Fase 2.2 (DA_CONSULTORIO).
