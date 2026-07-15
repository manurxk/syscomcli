# Análisis Técnico de Nivelación — SYSCOMcli
**Comparación entre el documento de diseño (TALLER.MD) y la implementación actual del sistema**
Fecha de corte: 2026-07-09 | Rama: `implementacion`

---

## 1. Objetivo

TALLER.MD es el documento de relevamiento y diseño (Cap. I-III: antecedentes, relevamiento, casos de uso, diagramas de clase/secuencia) elaborado **antes** de programar, para una "Clínica Psicológica Salud Total" con 3 módulos: Agendamiento, Consultorio, Ventas.

El sistema real evolucionó hacia una **clínica multiespecialidad** (no solo psicología) con arquitectura multi-sede y cumplimiento fiscal paraguayo (SIFEN). Este documento identifica, por entidad, si el diseño original:

- **Se implementó tal cual** → mantener referencia al documento sin cambios.
- **Se fusionó/simplificó** → el documento sobreestimó la necesidad de ABM independiente.
- **Fue reemplazado por un concepto superior** → el documento quedó corto frente a la necesidad real.
- **Es nuevo, no contemplado** → debe documentarse como ampliación de alcance (adenda), no como incumplimiento del diseño original.

Esto es clave para la defensa académica: no es que el proyecto "se desvió" del diseño, sino que el diseño original era de un **prototipo desktop-céntrico con ABMs genéricos**, y la implementación aplicó **decisiones de ingeniería de dominio** que consolidan varias entidades en una sola cuando el proceso de negocio real las gobierna en conjunto.

---

## 2. Módulo Agendamiento

### 2.1 Caso central: Día, Turno y Bloque Horario → ¿siguen siendo ABM completos?

**Respuesta corta: No.** El documento (líneas 1693-2138 de TALLER.MD) diseña **tres ABM independientes** con Alta/Baja/Modificación completos:

| Entidad (documento) | Campos previstos | Estado real |
|---|---|---|
| Mantener bloque horario | `bloque_horario_cod`, inicio, fin | **No existe como entidad independiente** |
| Mantener día | `dia_cod`, `dia_des` | Existe como `dia_semana`, pero es **catálogo fijo de solo lectura** (`DiaSemanaDao.getDiasSemana()`, `getDiaSemanaById()` — sin create/update/delete) |
| Mantener Turno | `turno_cod`, `turno_des` | **No existe como entidad independiente** |

En la implementación, estos tres conceptos se **fusionaron en una sola entidad: `agenda_horarios`** (`AgendaHorariosDao.py`), que representa el horario recurrente de un especialista en un consultorio, para un día de la semana, con hora inicio/fin — y que además **genera automáticamente los slots de citas disponibles** (`_generarSlots`, `getSlotsByAgendaHorario`) validando conflictos (`validarConflictoHorario`).

**Justificación técnica para la tesis:**
- El documento modela "Día", "Turno" y "Bloque horario" como catálogos administrables porque asume una interfaz desktop clásica donde cada tabla maestra se gestiona por separado (patrón típico de ingeniería de software de esa época/metodología).
- En la práctica clínica, día+turno+bloque horario **nunca se usan de forma independiente**: siempre se configuran juntos como "el Dr. X atiende los Lunes de 08:00 a 12:00 en el consultorio 2". Mantenerlos como 3 ABM separados obligaría al usuario a crear combinaciones manualmente sin garantía de coherencia (ej. un turno sin día asociado no tiene sentido de negocio).
- `dia_semana` se dejó como catálogo de solo lectura (7 registros fijos: Lunes-Domingo) porque **no es una necesidad real del negocio poder "dar de alta un nuevo día de la semana"** — es un dominio cerrado y universal, no un parámetro configurable por el administrador.

**Recomendación para el capítulo de análisis/diseño de la tesis:**
Documentar esto como una **decisión de diseño evolutivo**: el CU "Mantener bloque horario / Mantener día / Mantener Turno" del anteproyecto se reemplaza por el CU "Mantener Agenda Horaria" (horario recurrente + generación de slots), justificando la fusión por cohesión funcional. No mantengas el ABM completo de "día" en el documento final sin esta nota — de lo contrario un tribunal puede marcarlo como diseño no implementado.

### 2.2 Mantener ubicación → reemplazada

El documento define "Mantener ubicación" con `barrio_des`, `ciudad_des`, `pais_des` como entidad ligada al paciente/consultorio (líneas 1920-1995).

Real: no existe una entidad `ubicacion`. Se normalizó en `mantenimiento/referenciales` como **Ciudad**, **País**, y además se agregó **Departamento** y **Sede** — conceptos que el documento no contemplaba porque asumía una clínica de sede única. La ubicación física del consultorio ahora cuelga de `Sede` → `Consultorio` (`mantenimiento/referenciales/consultorio`), no de un catálogo "ubicación" plano.

**Nuevo respecto al documento:** `Sede` y `Empresa` — arquitectura multi-sede no prevista en el relevamiento original (el documento asume una sola clínica física). Esto es una ampliación de alcance legítima si el sistema apunta a ser multi-sucursal; debe declararse explícitamente como extensión.

### 2.3 Mantener Especialidad y Mantener Consultorio → se implementaron según diseño

Ambos siguen el ABM completo tal como está especificado (`especialidad`, `consultorio` con `des_consultorio`, estado activo/inactivo = borrado lógico). **Sin cambios respecto al documento.**

### 2.4 Ficha médica — duplicada en el documento, unificada en el sistema

El documento especifica "Registrar ficha médica" **dos veces**: una en Agendamiento (punto 4, opcional) y otra en Consultorio (punto 8). En la implementación existe una sola entidad `ficha` dentro de `clinico/movimientos`, generada desde la consulta. Esto es correcto: evita duplicar el mismo concepto en dos módulos, tal como el propio documento sugiere de forma implícita al repetir la misma especificación.

### 2.5 Avisos recordatorios → implementado y ampliado

El CU "Registrar Avisos Recordatorio" se implementó (`recordatorio/RecordatorioDao.py`) con envío real vía UltraMsg (WhatsApp), cumpliendo la automatización que el documento pedía como deseable ("Sí, mediante notificaciones automáticas vía correo, SMS o WhatsApp").

**Entidad nueva no prevista:** `lista_espera` (`agendamiento/lista_espera`). El documento no contempla lista de espera como caso de uso; se agregó como mejora funcional derivada de la operación real (pacientes que esperan un cupo cuando la agenda está saturada). Debe documentarse como requerimiento adicional identificado durante el desarrollo, no como parte del relevamiento original.

### 2.6 Informes web de agendamiento — pendiente

El documento pide "Elaborar informes web de agendamiento" como requerimiento explícito (listado de citas por día/semana/mes, disponibilidad, etc.). **No hay módulo de reportes implementado aún** (no existe `app/dao/reportes` ni `app/rutas/reportes` para agendamiento). Es una brecha real frente al documento — a diferencia de los casos anteriores, aquí sí falta desarrollo, no es una decisión de rediseño.

---

## 3. Módulo Consultorio → renombrado "Clínico" en la implementación

El documento usa "Consultorio" como nombre de módulo; el código usa `clinico`. Es coherente porque el sistema dejó de ser exclusivo de psicología (target original: consultas + diagnóstico + tratamiento en general, con roles CLINICO en vez de "psicólogo/especialista").

| Caso de uso (documento) | Implementación real | Veredicto |
|---|---|---|
| Registrar Presupuesto | Movido a `ventas/movimientos/presupuesto` | Reubicado — el presupuesto es un documento comercial (precede a la venta), no clínico. Coherente con que el propio documento también lo repite en Ventas ("Registrar pedido de clientes" con presupuesto implícito). |
| Registrar Consulta | `clinico/movimientos/consulta` + `anamnesis` embebida | Ampliado — el documento no exige anamnesis como sub-entidad versionada; se agregó por necesidad clínica real. |
| Registrar diagnóstico | Parte de `registro_clinico` (unificado) | Fusionado con signos/síntomas/procedimientos/insumos |
| Registrar procedimientos e insumos | Parte de `registro_clinico` | Fusionado (ver 3.1) |
| Registrar orden de estudios | `clinico/movimientos/orden` (unificada con análisis) | Fusionado (ver 3.2) |
| Registrar orden de análisis | `clinico/movimientos/orden` | Fusionado con orden de estudios |
| Registrar recetas e indicaciones | `clinico/movimientos/receta` | Según diseño |
| Registrar tratamientos | `clinico/movimientos/tratamiento` | Según diseño |
| Registrar historial clínico | Cubierto transversalmente por consulta+registro_clinico | Reinterpretado como vista agregada, no entidad propia |
| Registrar certificado médico | `clinico/movimientos/certificado_medico` | Según diseño |
| Registrar justificativo médico | Cubierto por `certificado_medico` (tipo "reposo/justificativo") | Fusionado vía catálogo `tipo_certificado_medico` |

### 3.1 Diagnóstico + Procedimientos/Insumos → `registro_clinico`

El documento trata "Registrar diagnóstico" y "Registrar procedimientos e insumos utilizados" como dos CU separados (secciones 2 y 3 del relevamiento de Consultorio). La implementación los unificó en una sola entidad `registro_clinico` que agrupa diagnóstico, signos, síntomas, procedimientos e insumos de una misma consulta.

**Justificación:** todos estos datos se registran en el mismo momento (durante la consulta), sobre el mismo paciente y la misma consulta — no tienen ciclo de vida independiente entre sí. Separarlos en pantallas distintas obligaría a repetir la selección de paciente/consulta en cada uno. Es una decisión de cohesión de datos, igual que el caso de "día/turno/bloque horario" en agendamiento.

### 3.2 Orden de estudios + Orden de análisis → `orden` unificada

El documento define dos CU separados con estructura casi idéntica (mismos campos: paciente, fecha, justificación, tipo). Se unificaron en una sola entidad `orden` con un catálogo `tipo_estudio`/`tipo_analisis` que discrimina el subtipo. Reduce duplicación de código y de tablas sin perder trazabilidad (se puede filtrar por tipo).

### 3.3 Entidades nuevas — no contempladas en el documento

- **PEI (Plan Educativo Individual)** — entidad versionada propia. No existe ninguna mención en TALLER.MD. Es una ampliación de alcance hacia atención de necesidades educativas especiales, fuera del relevamiento original (que se limitaba a terapia individual/evaluación/tratamiento farmacológico).
- **Derivaciones entre especialistas** — CU nuevo, no documentado. Surge de la necesidad real de interconsulta (ej. psicólogo deriva a psiquiatra), que el documento no relevó explícitamente aunque la estructura organizacional (Psicólogos + Psiquiatras) lo sugiere.
- **Instrumento clínico** (catálogo de tests/escalas psicológicas estructurado) — el documento solo menciona "pruebas psicológicas" como texto libre dentro de diagnóstico; se formalizó como catálogo propio.

Estas tres deben incorporarse al documento de tesis como **adenda de alcance**, con su propia mini-especificación de CU, para que la tesis quede coherente con el sistema entregado. No es un defecto: es evidencia de que el análisis de requerimientos maduró durante el desarrollo (normal en proyectos iterativos), pero **debe quedar por escrito**, no solo en el código.

### 3.4 Informes de consultorio — pendiente

Igual que en Agendamiento: "Elaborar informes de consultorio" no tiene módulo de reportes implementado. Brecha real, no decisión de diseño.

---

## 4. Módulo Ventas

Este módulo es el más fiel al documento en términos de cobertura de entidades — las 8 subfases (D.1-D.8) cubren prácticamente el 100% de la lista de requerimientos original (apertura/cierre de caja, arqueo, recaudaciones, pedido, facturación+CxC, libro de ventas, cobranzas, notas de crédito/débito). La Nota de Remisión, que el documento pide, se implementó como entidad nueva (`remision` + `remision_detalle`) sin depender de estructuras legacy, tal como estaba especificado.

### 4.1 Elementos nuevos no previstos en el documento (por marco legal, no por rediseño)

El documento fue relevado sin considerar la normativa de facturación electrónica paraguaya (SIFEN), por lo que estas entidades **no tienen equivalente en TALLER.MD**:

- `timbrado`, `punto_expedicion` — requeridos por ley para numerar comprobantes fiscales válidos.
- `tipo_comprobante`, `condicion_venta`, `estado_factura` — catálogos normativos/operativos que estructuran la factura electrónica.
- `item_servicio` — catálogo de ítems facturables, más genérico que el "tipo ítems" que menciona el documento (línea 315), pero equivalente en función.

**Justificación para la tesis:** el documento se centra en el *proceso de negocio* (qué se cobra, cómo se cobra) pero no contempla el *marco regulatorio* de emisión de comprobantes en Paraguay. Esto no es un error del relevamiento — es normal que un documento de análisis funcional no anticipe el detalle de cumplimiento fiscal, que se agrega en la fase de diseño técnico. Debe mencionarse en el capítulo de "Restricciones, Suposiciones y Dependencias" como un requisito no funcional/legal descubierto durante el diseño.

### 4.2 Informes web de ventas — pendiente

Mismo patrón que los otros dos módulos: "Elaborar informes web de venta" no está implementado como módulo de reportes.

---

## 5. Tabla resumen de decisiones técnicas

| # | Entidad/CU del documento | Decisión tomada | Tipo de decisión |
|---|---|---|---|
| 1 | Mantener bloque horario | Eliminado, absorbido en `agenda_horarios` | Fusión por cohesión |
| 2 | Mantener día | Reducido a catálogo fijo de solo lectura | Simplificación (dominio cerrado) |
| 3 | Mantener Turno | Eliminado, absorbido en `agenda_horarios` | Fusión por cohesión |
| 4 | Mantener ubicación | Reemplazada por Ciudad/País/Departamento/Sede | Normalización + ampliación (multi-sede) |
| 5 | Mantener Especialidad | Sin cambios | Implementado según diseño |
| 6 | Mantener Consultorio | Sin cambios (ahora cuelga de Sede) | Implementado según diseño, extendido |
| 7 | Ficha médica (dup. en 2 módulos) | Unificada en `clinico/movimientos/ficha` | Deduplicación |
| 8 | Registrar Presupuesto (Consultorio) | Movido a Ventas | Reubicación por naturaleza comercial |
| 9 | Diagnóstico + Procedimientos/Insumos | Unificados en `registro_clinico` | Fusión por cohesión |
| 10 | Orden de estudios + Orden de análisis | Unificadas en `orden` | Fusión por cohesión |
| 11 | Justificativo médico | Fusionado en `certificado_medico` (vía tipo) | Fusión por catálogo |
| 12 | — (no existía) | PEI, Derivaciones, Instrumento clínico | Ampliación de alcance |
| 13 | — (no existía) | Lista de espera (Agendamiento) | Ampliación de alcance |
| 14 | — (no existía) | Timbrado, Punto Expedición, Tipo Comprobante, Condición Venta (SIFEN) | Requisito legal no relevado |
| 15 | Informes web (los 3 módulos) | No implementado | Brecha pendiente real |

---

## 6. Conclusión ejecutiva

1. **No hay incumplimiento del diseño original en los casos de fusión (día/turno/bloque horario, diagnóstico/procedimientos, órdenes de estudio/análisis).** Son decisiones de ingeniería que consolidan entidades que en el relevamiento aparecían separadas por seguir un patrón de "ABM por tabla", pero que en el modelo de datos real comparten el mismo ciclo de vida. Para la defensa de tesis, esto se presenta como **refinamiento del diseño en la fase de análisis a diseño técnico**, citando el principio de cohesión funcional.

2. **Las entidades nuevas (PEI, derivaciones, instrumento, lista de espera, catálogos SIFEN) deben incorporarse al documento como adenda de alcance**, con su propia mini-especificación de CU (descripción básica, actores, flujo básico/alternativo, pre/post condición) siguiendo el mismo formato que el resto de TALLER.MD, para que el documento final quede 100% trazable contra el sistema entregado.

3. **La única brecha real (no decisión, sino trabajo pendiente) es el módulo de informes/dashboard web**, exigido explícitamente en los tres módulos del documento original y no implementado aún en ninguno. Si el cronograma de tesis lo permite, es el ítem con mayor prioridad para cerrar antes de la defensa, porque es el único punto donde el documento pide algo que el sistema no ofrece — no una discrepancia de diseño sino una funcionalidad faltante.

4. Recomendación de redacción para el documento final: agregar una sección "Anexo — Evolución del diseño desde el relevamiento inicial" que documente los puntos 1 y 2 de esta conclusión, en vez de reescribir TALLER.MD desde cero. Esto demuestra proceso iterativo de análisis, que es valorado académicamente, y evita que un jurado interprete las fusiones como incoherencias entre diseño e implementación.
