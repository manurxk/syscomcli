# Estado General de la Nivelación — SYSCOMcli

Documento único de seguimiento. Se actualiza al cerrar cada fase. No reemplaza las bitácoras detalladas de cada capítulo (`0X_capituloX_*/`), es el resumen para saber en qué parte estamos sin tener que abrir todo.

---

## Análisis 1 — Modelo de Negocio

**Estado: CERRADO ✅**

- Se comparó la jerarquía de 11 diagramas del UML (`Modelo_negocio` + `DC_GESTIONAR_MAN_SEG` + sus 4 hijos + `DC_GESTIONAR_AGENDAMIENTO/CONSULTORIO/FACTURACION` + `DC_ELABORAR_INFORMES`) contra TALLER.MD Cap. III sección 3.
- Resultado: el UML es fiel al documento original y corrige un hueco de numeración que tenía el borrador (falta de "3.1.2 Módulo Consultorio").
- **No requiere cambios.** Pendiente solo que pegues la captura final en el documento de tesis.

Detalle: `01_capitulo1_mantenimiento/00_auditoria_uml_vs_codigo.md`

---

## Análisis 2 — Diagramas de Actividad

**Estado: EN CURSO 🔶 (1 de 3 fases cerradas)**

| Fase | Diagrama | Estado | Pendiente |
|---|---|---|---|
| 2.1 | DA_AGENDAMIENTO | **CERRADO ✅ (2026-07-14)** | — |
| 2.2 | DA_CONSULTORIO | Auditado, esperando tu aprobación | Fusionar diagnóstico+insumos en "registro clínico", recibir bloque de ficha médica desde 2.1; piscina `MEDICO`→`ESPECIALISTA` (ver `REFERENCIAS_UML.md` §2) |
| 2.3 | DA_VENTAS | Auditado, esperando tu aprobación | Corregir encuadre inicial ("Solicitud de cita"→"Solicitud de pedido"), limpiar transiciones fantasma (Tarjeta→Tarjeta, Cheque→Cheque), agregar 3 ramas completas: Remisión, NC/ND, Libro de Ventas; renombrar tramo de Arqueo de Caja; renombrar diagrama interno `DA_VENTA`→`DA_VENTAS` |

Detalle de Fase 2.1: `02_capitulo2_agendamiento/00_diagrama_actividades.md` (cerrado). Detalle de hallazgos de 2.2/2.3: ver mensaje de chat del 2026-07-09 (a trasladar a archivo cuando se apruebe cada fase).

**Fuera de alcance detectado en 2.1:** Lista de Espera (Agendamiento) — funcionalidad real en código, no contemplada en `TALLER.MD`. Documentada en `MEJORAS_FUERA_DE_ALCANCE.md`, no en el diagrama.

---

## Análisis 3 — Diagrama de Caso de Uso (por entidad)

**Estado: EN CURSO 🔶 (1 de 5 diagramas cerrados)**

| Diagrama | Estado |
|---|---|
| `DC_GESTIONAR_MAN_SEG` (+ 4 hijos: REF_AGENDAMIENTO, REF_CONSULTORIO, REF_FACTURACIÓN, REF_MAN_SEG) | Auditado completo, 5 preguntas pendientes de tu decisión (ver `01_capitulo1_mantenimiento/00_auditoria_uml_vs_codigo.md` §5) |
| `DC_GESTIONAR_AGENDAMIENTO` | No iniciado |
| `DC_GESTIONAR_CONSULTORIO` | No iniciado |
| `DC_GESTIONAR_FACTURACION` | No iniciado |
| `DC_ELABORAR_INFORMES` | No iniciado — acá se define el alcance mínimo de Reportes (única brecha real de código) |

---

## Decisiones abiertas (bloquean cierre de capítulos, no bloquean seguir trabajando)

1. ¿Referenciales clínicos nuevos (signo, instrumento, insumo, tipo_tratamiento, tipo_certificado_medico) entran al UML de `DCU_REF_CONSULTORIO`?
2. ¿Referenciales SIFEN (timbrado, punto_expedicion, tipo_comprobante, condicion_venta, estado_factura, moneda, item_servicio) entran al UML de `DCU_REF_FACTURACIÓN` o quedan como nota de restricciones legales?
3. ¿Auditoría y Accesos entran como CU nuevos de solo consulta en `DCU_REF_MAN_SEG`?
4. ¿PEI y Derivaciones (Clínico) entran al documento como anexo, o quedan fuera del alcance de la tesis?
5. Confirmar limpieza de código (Fase F) de los 7 DAO con métodos ABM muertos (país, departamento, ciudad, género, estado civil, nivel instrucción, profesión).

---

## Próximo paso

Fase 2.2 (DA_CONSULTORIO): pasás el estado actual del diagrama (UML pegado o captura), se audita contra `TALLER.MD` y el código real (`app/dao/clinico/`, `app/rutas/clinico/`), siguiendo la misma metodología que en 2.1 — incluye la convención ya fijada de `MEDICO`→`ESPECIALISTA` y la llegada del bloque de ficha médica/anamnesis desde 2.1.
