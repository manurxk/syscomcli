# Checklist de edición — DA_AGENDAMIENTO

**CERRADO ✅ — 2026-07-14.** Todos los puntos verificados contra la captura final. Justificación y evidencia de código de cada punto están en `00_diagrama_actividades.md`.

## Piscinas y estructura base

- [x] Piscinas `PACIENTE / RECEPCION / SISTEMA` (confirmado, `SYSCOMCLI` corregido a `SISTEMA`)
- [x] Bloque de disponibilidad con Recepción como arranque
- [x] Bloque de ficha médica eliminado
- [x] Bloque manual de "próxima cita" eliminado, reemplazado por recordatorios automáticos
- [x] Uso correcto de Flow Final (⊗) vs Activity Final (● relleno)

## Lista de Espera (decisión 2026-07-14 — fuera del diagrama)

La Lista de Espera se documenta aparte como mejora fuera de alcance (`docs/tesis/MEJORAS_FUERA_DE_ALCANCE.md`), no en este diagrama. Código intacto, solo se sacó del dibujo.

- [x] Borrado: "Paciente acepta anotarse en lista de espera"
- [x] Borrado: "Recepción anota al paciente en lista de espera"
- [x] Borrado: "Recepción gestiona el estado de la lista de espera"
- [x] Borrado: rombo "¿Paciente acepta el cupo notificado?"
- [x] Borrado: "Se anula la cita" (paso propio de esa rama)
- [x] Borrado: el Flow Final que cerraba esa rama
- [x] Borrado: el `ActionState` "Recepción retoma el registro de la cita..." (el que no tenía salida)
- [x] El rombo "¿Hay slot disponible?" queda con:
  - **SI** → "Recepción registra los datos de la cita y del paciente"
  - **NO** → vuelve (loop) a "Recepción busca slots disponibles" — bucle de reintento, sin Final en esta rama

## Corregido

- [x] "Recepción confirma la fecha de la cita" conecta directo al rombo "¿Se confirma la consulta?"

## Verificación final

- [x] 3 piscinas: PACIENTE, RECEPCION, SISTEMA
- [x] Ninguna piscina vacía
- [x] Sin finales duplicados
- [x] Sin `Initial` duplicados
- [x] Sin rama de lista de espera
- [x] Sin `ActionState` sin flecha de salida
- [x] Sin bloque de ficha médica (documentado en DA_CONSULTORIO, Fase 2.2)

Fase 2.1 cerrada. Siguiente: Fase 2.2 (DA_CONSULTORIO).
