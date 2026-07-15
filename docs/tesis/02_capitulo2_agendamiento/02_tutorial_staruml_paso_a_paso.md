# Tutorial StarUML — construir DA_AGENDAMIENTO clic por clic

Este documento asume que estás construyendo el diagrama desde cero (como se ve en tu captura: piscina `PACIENTE` ya puesta, canvas vacío). Usa los nombres exactos del Toolbox que tenés a la izquierda: `Select`, `ActionState`, `SubactivityState`, `InitialState`, `FinalState`, `Synchronization`, `Decision`, `Flow Final`, `Object Flow`, `Transition`, `SelfTransition`, `Swimlane(Vertical)`.

Para el contenido/veredicto de cada paso (por qué existe, evidencia de código) ver `00_diagrama_actividades.md`. Este documento es solo mecánica de StarUML.

---

## 0. Mecánica general (aplica a todo el tutorial)

- **Colocar un elemento nuevo:** click en la herramienta del Toolbox → click dentro de la piscina donde va. Aparece el elemento con el nombre editable — escribís el texto y `Enter`.
- **Conectar dos elementos:** click en `Transition` del Toolbox → click sobre el elemento de **origen** → click sobre el elemento de **destino**. Se dibuja la flecha sola.
- **Poner una etiqueta a una transición** (ej. "SI"/"NO" saliendo de una `Decision`): con `Select` activo, click sobre la flecha ya dibujada → escribir el texto (o botón derecho → Rename, según versión).
- **Volver a la flecha de selección normal:** click en `Select` (la primera del Toolbox) — hacé esto después de cada elemento que coloques, si no StarUML sigue esperando que pongas otro del mismo tipo.
- **Mover algo ya puesto:** `Select` → arrastrar.
- **Agregar una piscina nueva a la derecha:** `Swimlane(Vertical)` → click a la derecha de la última piscina.
- **Renombrar una piscina:** doble click sobre el título de la piscina (`PACIENTE`, etc.).
- **ActionState vs SubactivityState:** usá `ActionState` (óvalo simple) para todos los pasos de este diagrama. `SubactivityState` solo se usa si un paso tuviera un sub-diagrama propio detrás — no es el caso acá, no lo uses.

---

## 1. Piscinas

1. Ya tenés `PACIENTE` puesta.
2. `Swimlane(Vertical)` → click a la derecha de `PACIENTE` → doble click, escribir `RECEPCION`.
3. `Swimlane(Vertical)` → click a la derecha de `RECEPCION` → doble click, escribir `SISTEMA`.

Quedan 3 piscinas en este orden: `PACIENTE | RECEPCION | SISTEMA`.

---

## 2. Bloque disponibilidad (arranque del especialista)

| #   | Herramienta    | Piscina   | Texto                                                                             | Conectar            |
| --- | -------------- | --------- | --------------------------------------------------------------------------------- | ------------------- |
| 1   | `InitialState` | RECEPCION | (sin texto)                                                                       | —                   |
| 2   | `ActionState`  | RECEPCION | Recepción registra la disponibilidad del especialista (día, horario, consultorio) | `Transition`: 1 → 2 |
| 3   | `ActionState`  | SISTEMA   | Sistema valida conflicto y genera slots disponibles                               | `Transition`: 2 → 3 |
| 4   | `FinalState`   | SISTEMA   | (sin texto)                                                                       | `Transition`: 3 → 4 |

---

## 3. Bloque solicitud de cita

| #   | Herramienta    | Piscina   | Texto                                                      | Conectar             |
| --- | -------------- | --------- | ---------------------------------------------------------- | -------------------- |
| 5   | `InitialState` | PACIENTE  | (sin texto)                                                | —                    |
| 6   | `ActionState`  | PACIENTE  | Paciente solicita una cita                                 | `Transition`: 5 → 6  |
| 7   | `ActionState`  | RECEPCION | Recepción recibe la solicitud                              | `Transition`: 6 → 7  |
| 8   | `ActionState`  | RECEPCION | Recepción pregunta si es primera consulta o de seguimiento | `Transition`: 7 → 8  |
| 9   | `ActionState`  | RECEPCION | Recepción busca slots disponibles (especialista + horario) | `Transition`: 8 → 9  |
| 10  | `Decision`     | RECEPCION | ¿Hay slot disponible?                                      | `Transition`: 9 → 10 |

---

## 4. Rama SI — se registra la cita

| #   | Herramienta   | Piscina   | Texto                                                  | Conectar                               |
| --- | ------------- | --------- | ------------------------------------------------------ | -------------------------------------- |
| 11  | `ActionState` | RECEPCION | Recepción registra los datos de la cita y del paciente | `Transition`: 10 → 11, etiqueta **SI** |
| 12  | `ActionState` | PACIENTE  | Paciente confirma sus datos personales                 | `Transition`: 11 → 12                  |
| 13  | `ActionState` | RECEPCION | Recepción confirma la fecha de la cita                 | `Transition`: 12 → 13                  |
| 14  | `Decision`    | RECEPCION | ¿Se confirma la consulta?                              | `Transition`: 13 → 14                  |

---

## 5. Rama confirmación SI/NO

| #   | Herramienta   | Piscina   | Texto                                   | Conectar                               |
| --- | ------------- | --------- | --------------------------------------- | -------------------------------------- |
| 15  | `ActionState` | RECEPCION | Recepción marca la cita como CONFIRMADA | `Transition`: 14 → 15, etiqueta **SI** |
| 16  | `ActionState` | RECEPCION | Recepción reagenda o anula la cita      | `Transition`: 14 → 16, etiqueta **NO** |
| 17  | `FinalState`  | RECEPCION | (sin texto)                             | `Transition`: 16 → 17                  |

El nodo 15 (`CONFIRMADA`) no termina en un Final propio — sigue directo al bloque de recordatorios (sección 6).

---

## 6. Bloque recordatorios automáticos (piscina SISTEMA)

| #   | Herramienta   | Piscina  | Texto                                                       | Conectar              |
| --- | ------------- | -------- | ----------------------------------------------------------- | --------------------- |
| 18  | `ActionState` | SISTEMA  | Sistema genera recordatorios (1440 min y 120 min antes)     | `Transition`: 15 → 18 |
| 19  | `ActionState` | SISTEMA  | Job programado detecta ventana vencida y envía por WhatsApp | `Transition`: 18 → 19 |
| 20  | `ActionState` | PACIENTE | Paciente recibe la notificación de su próxima cita          | `Transition`: 19 → 20 |
| 21  | `FinalState`  | PACIENTE | (sin texto)                                                 | `Transition`: 20 → 21 |

---

## 7. Rama NO del paso 10 — Lista de Espera

| #   | Herramienta   | Piscina   | Texto                                              | Conectar                                                                                                                      |
| --- | ------------- | --------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| 22  | `ActionState` | PACIENTE  | Paciente acepta anotarse en lista de espera        | `Transition`: 10 → 22, etiqueta **NO**                                                                                        |
| 23  | `ActionState` | RECEPCION | Recepción anota al paciente en lista de espera     | `Transition`: 22 → 23                                                                                                         |
| 24  | `ActionState` | RECEPCION | Recepción gestiona el estado de la lista de espera | `Transition`: 23 → 24                                                                                                         |
| 25  | `Decision`    | RECEPCION | ¿Paciente acepta el cupo notificado?               | `Transition`: 24 → 25                                                                                                         |
| —   | `Transition`  | —         | (sin nodo nuevo)                                   | 25 → **11** (el mismo `ActionState` "Recepción registra los datos de la cita...", ya puesto en la sección 4), etiqueta **SI** |
| 26  | `FinalState`  | RECEPCION | (sin texto)                                        | `Transition`: 25 → 26, etiqueta **NO / expira**                                                                               |

**Nota práctica de StarUML:** para conectar el paso 25 con el nodo 11 que ya existe (en vez de crear uno nuevo), simplemente usá `Transition` → click sobre `Decision 25` → click sobre el `ActionState 11` ya dibujado. StarUML permite que una flecha llegue a un elemento existente en otra parte del canvas, aunque quede un poco largo el trazo — es normal en diagramas con reciclado de flujo, no hace falta duplicar el nodo.

---

## 8. Verificación final antes de exportar

- 3 piscinas: `PACIENTE`, `RECEPCION`, `SISTEMA` — mismo orden de izquierda a derecha
- 4 `InitialState` en total (nodos 1, 5) — dos arranques válidos: disponibilidad y solicitud de cita
- 4 `FinalState` en total (nodos 4, 17, 21, 26)
- 3 `Decision` en total (nodos 10, 14, 25)
- Ningún elemento de ficha médica / anamnesis (ese bloque no va en este diagrama)
- Ninguna piscina vacía

Cuando termines, capturá el diagrama completo y lo reviso contra este tutorial y contra `00_diagrama_actividades.md`.
