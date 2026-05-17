## Análisis de cambio en Agenda Médica: múltiples especialidades por día/consultorio

### 1. Situación actual (a partir de `Agenda_MedicaDao.py`)

- **Modelo de agenda**  
  - La tabla `agenda_horarios` define la agenda a nivel de **bloque de horario**:  
    - Un especialista (`id_especialista`)  
    - Una especialidad (`id_especialidad`)  
    - Un consultorio (`id_consultorio`)  
    - Un día de semana (`id_dia_semana`)  
    - Un rango horario (`agen_hora_inicio` – `agen_hora_fin`)  
    - Una duración fija de turno (`agen_duracion_turno`)  
    - Un turno lógico (`agen_turno`: mañana/tarde)  
    - Cupos totales, fechas desde/hasta, estado, etc.
  - Los métodos como `getAgendasByEspecialista`, `getAgendaSemanalConsultorio` y `guardarAgenda` asumen que **ese bloque completo** corresponde a **una única especialidad**.

- **Consumo esperado en frontend / módulo de citas**  
  - Se construye una “grilla” por día/turno donde cada celda tiene: una especialidad, un consultorio, un especialista y un rango de horas continuo.  
  - La generación de turnos de 45 minutos normalmente se hace derivando slots homogéneos desde `hora_inicio` hasta `hora_fin` con la misma especialidad.

### 2. Nuevo requerimiento

- **Escenario planteado**  
  - Un especialista atiende, por ejemplo, lunes y martes, en un mismo consultorio.  
  - La duración del turno sigue siendo fija (p.ej. 45 minutos).  
  - **Dentro del mismo día y consultorio, la especialidad puede cambiar turno a turno**.  
    - Ejemplo lunes:  
      - Turno 1: Especialidad 1 – Consultorio 1  
      - Turno 2: Especialidad 2 – Consultorio 1  
      - Turno 3 y 4: Especialidad 1 – Consultorio 1  
  - Esto genera muchas combinaciones posibles (patrones distintos de especialidades por día).

- **Implicancia clave**  
  - Ya no alcanza con un solo registro de `agenda_horarios` por día/turno.  
  - Necesitamos **definir la especialidad a nivel de cada slot (cada 45 minutos)**, no solo a nivel de bloque horario.

### 3. Opciones de diseño

- **Opción A: Seguir usando solo `agenda_horarios` dividiendo los bloques**
  - Crear varios registros en `agenda_horarios` para el mismo día/consultorio/especialista, cada uno cubriendo solo el rango horario de una especialidad.  
    - Ejemplo:  
      - 08:00–08:45 → Especialidad 1  
      - 08:45–09:30 → Especialidad 2  
      - 09:30–10:15 y 10:15–11:00 → Especialidad 1 (dos filas más).
  - **Ventajas**  
    - No cambia el modelo de datos ni el DAO de forma profunda.  
    - El motor de generación de turnos puede seguir usando el mismo criterio (bloques homogéneos).
  - **Desventajas**  
    - La configuración de agenda se vuelve muy granular y tediosa de mantener.  
    - El frontend de administración de agenda puede hacerse difícil de usar cuando hay muchos patrones.

- **Opción B: Introducir una tabla de detalle por turno**
  - Mantener `agenda_horarios` como bloque “macro” (día, consultorio, rango total) y agregar una tabla, por ejemplo `agenda_turnos_detalle`, con campos:  
    - `id_agenda_horario`  
    - `hora_inicio_turno`, `hora_fin_turno`  
    - `id_especialidad` (puede variar por turno)  
    - Estado del turno, cupos, etc.
  - El flujo:  
    - `agenda_horarios` define el “marco” (lunes de 08:00 a 12:00, consultorio 1, especialista X).  
    - El detalle define **cada slot de 45 minutos** con su especialidad concreta.  
  - **Ventajas**  
    - Mucho más flexible: soporta cualquier patrón de especialidades por día.  
    - Permite reutilizar la misma estructura futura si cambian duraciones o reglas.  
  - **Desventajas**  
    - Requiere cambios más profundos:  
      - Nuevos métodos en DAO para leer/escribir el detalle.  
      - Adaptar el módulo de generación de turnos y la UI de agenda.  

- **Opción C: Lógica dinámica sin cambios en modelo (no recomendado)**
  - Guardar solo el bloque macro y “hardcodear” en código reglas que determinen qué especialidad corresponde a cada turno (por posición 1, 2, 3...).  
  - **Problemas**  
    - Poco mantenible y muy rígido (las reglas quedarían “quemadas” en código).  
    - Difícil de explicar/configurar a usuarios administrativos.

### 4. Impacto estimado en el código (escala 1–10)

- **Si se elige Opción A (múltiples bloques en `agenda_horarios`)**  
  - Cambios principales:  
    - Lógica de UI para crear/editar agendas: permitir configurar varios bloques por día y consultorio.  
    - Validaciones de solapamiento de consultorio (`validarDisponibilidadConsultorio`) ya soportan múltiples bloques, pero habrá que revisar bien colisiones.  
    - Revisión de `getAgendasByEspecialista` y `getAgendaSemanalConsultorio` para que muestren correctamente varios bloques.  
  - **Impacto global aproximado**: **4/10**  
    - Estructura de datos se mantiene igual.  
    - El esfuerzo está sobre todo en UX de configuración y en pequeños ajustes en consultas/agrupaciones.

- **Si se elige Opción B (nueva tabla de detalle por turno)**  
  - Cambios en backend:  
    - Crear nueva tabla y modelo lógico de detalle.  
    - Nuevos métodos DAO:  
      - Alta/edición/borrado de slots (`agenda_turnos_detalle`).  
      - Consultas de agenda que incluyan la lista de turnos con su especialidad.  
    - Ajustar `getAgendasByEspecialista` para devolver estructura más rica (lista de slots en vez de solo un bloque).  
    - Ajustar todo lo que asume “una especialidad por bloque” (incluyendo generación de citas).  
  - Cambios en frontend:  
    - Pantalla de configuración de agenda con editor de slots (timeline de 45 min) con selección de especialidad por bloque.  
    - Ajustes en la pantalla de reserva de citas si hoy se asume una sola especialidad por franja.  
  - **Impacto global aproximado**: **7/10**  
    - Es un cambio estructural en cómo se modela la agenda.  
    - Sin embargo, es alineado con buenas prácticas y future-proof.

### 5. Recomendación práctica según tu caso

- **Si el caso “especialidad por turno” será algo puntual / poco frecuente**  
  - Empezar por la **Opción A**: dividir el día en bloques más chicos en `agenda_horarios`.  
  - Con esto ya podés cubrir casos como: 1 turno Especialidad 1, 1 turno Especialidad 2, 2 turnos Especialidad 1, siempre que estés dispuesto a crear los registros necesarios por franja.

- **Si sabés que habrá muchos patrones distintos y cambiarán en el tiempo**  
  - Ir directamente por la **Opción B** (nueva tabla de detalle) aunque el impacto sea mayor (7/10).  
  - Te evita un “techo” de complejidad más adelante y hace más claras las reglas de negocio: cada turno tiene su especialidad y punto.

### 6. Resumen corto

- **El problema de fondo**: hoy el modelo de agenda asume una especialidad por bloque de horario; tu requerimiento necesita especialidad por turno.  
- **Impacto estimado**:  
  - Solución rápida basada en el modelo actual (dividir bloques): **~4/10** de cambio.  
  - Solución robusta con tabla de detalle de turnos: **~7/10** de cambio.  
- **Siguiente paso sugerido**: decidir si este patrón de mezcla de especialidades es la excepción o la regla; con eso se elige si vale la pena ir por una solución rápida (A) o un rediseño más sólido (B).


