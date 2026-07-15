# Plan Maestro de Nivelación — Documento de Tesis SYSCOMcli

Este archivo es el índice de trabajo. Cada capítulo se completa en su propia carpeta (`01_capitulo1_mantenimiento/`, etc.) usando las plantillas de `_plantillas/`. No se avanza al siguiente capítulo sin cerrar el anterior (auditoría + CU + diagrama de secuencia validados contra el código real).

**Importante — separar dos líneas de trabajo que no deben confundirse:**
- **Fases de código** (ya ejecutadas, ver `docs_reestructuracion/avance_*.md`): A=Mantenimiento, B=Agendamiento, C=Clínico, D=Ventas. **Ya están construidas y funcionando.** No se repiten acá.
- **Fases de documento** (lo que define este plan, A-F): son capítulos de la tesis. Se apoyan en el código ya construido, no lo vuelven a implementar — excepto donde se detecta una brecha real de código (ver Fase E).

---

## Fase A (documento) — Capítulo Mantenimiento

Cubre: Seguridad (login, usuarios, roles) + Gestión de personas (paciente, funcionario, especialista) + Referenciales de apoyo.

### A.1 Auditoría de lo ya construido

| Función | Dónde vive en el código | Estado |
|---|---|---|
| Login / autenticación | `app/dao/auth/auth_dao.py`, `app/rutas/auth/` | Implementado (incluye historial de contraseñas y reset por token) |
| Gestión de usuarios (alta, roles, activar/desactivar) | `app/dao/auth/user_dao.py` (`UsuarioDao`), `app/rutas/mantenimiento/usuario/` | Implementado, ABM completo + gestión de roles múltiples |
| Paciente | `app/dao/mantenimiento/personas/paciente/PacienteDao.py` | Implementado |
| Funcionario / especialista | `app/dao/mantenimiento/personas/funcionario/FuncionarioDao.py` | Implementado |
| Cargo | `app/dao/mantenimiento/referenciales/cargo/` | ABM completo |
| Empresa | `app/dao/mantenimiento/referenciales/empresa/` | ABM completo |
| Sede | `app/dao/mantenimiento/referenciales/sede/` | ABM completo |
| Consultorio | `app/dao/mantenimiento/referenciales/consultorio/` | ABM completo (cuelga de Sede) |
| Ciudad / Departamento / País | `app/dao/mantenimiento/referenciales/{ciudad,departamento,pais}/` | Ver A.2 — de facto solo lectura |
| Género / Estado civil / Nivel de instrucción / Profesión | `app/dao/mantenimiento/referenciales/{genero,estado_civil,nivel_instruccion,profesion}/` | Ver A.2 — de facto solo lectura |

### A.2 Referenciales sin ABM — evidencia, no opinión

Se verificó código de rutas, no solo el DAO. Resultado: **6 referenciales + día de la semana ya son de solo lectura en la práctica**, aunque sus DAO todavía cargan métodos `guardarX/updateX/deleteX` que **no están conectados a ninguna ruta HTTP** (código muerto, nunca alcanzable desde la UI):

| Referencial | Rutas expuestas hoy | Veredicto |
|---|---|---|
| `dia_semana` | Solo `GET` (`DiaSemanaDao` ni siquiera define guardar/update/delete) | Solo lectura — catálogo cerrado (7 valores fijos) |
| `pais` | Solo `GET /api/v1/paises` (`referenciales_api.py`) | Solo lectura de facto — DAO tiene CRUD muerto |
| `departamento` | Solo `GET /api/v1/departamentos` | Solo lectura de facto — DAO tiene CRUD muerto |
| `ciudad` | Solo `GET /api/v1/ciudades` | Solo lectura de facto — DAO tiene CRUD muerto |
| `genero` | Solo `GET /api/v1/generos` | Solo lectura de facto — DAO tiene CRUD muerto |
| `estado_civil` | Solo `GET /api/v1/estados-civiles` | Solo lectura de facto — DAO tiene CRUD muerto |
| `nivel_instruccion` | Solo `GET /api/v1/niveles-instruccion` | Solo lectura de facto — DAO tiene CRUD muerto |
| `profesion` | Solo `GET /api/v1/profesiones` | Solo lectura de facto — DAO tiene CRUD muerto |

**Por qué ya son así (justificación de negocio, para la tesis):** son catálogos normativos/geográficos que no cambian por la operación diaria de la clínica (no se "inventa" un género o un país nuevo desde la aplicación). Se cargan una sola vez por seed/migración SQL y se consumen como combos en los formularios de Paciente/Funcionario.

**Consecuencia para el código (Fase F, no ahora):** limpiar los métodos `guardar/update/delete` no usados en esos 8 DAO para que el código fuente no sugiera una capacidad que no existe — esto es justo el tipo de "básico pero bien estructurado" que pediste, porque hoy hay una inconsistencia entre lo que el DAO *permite* y lo que el sistema *expone*. Se ejecuta recién en Fase F para no tocar código mientras se redacta el documento.

**Mantienen ABM completo (activo y con ruta), sin cambios:** `cargo`, `empresa`, `sede`, `consultorio`, `especialidad` (agendamiento) y todos los referenciales de Clínico y Ventas — todos varían por decisión operativa real de la clínica (agregar una especialidad nueva, un consultorio nuevo, una condición de venta nueva, etc.).

### A.3 Entregable de Fase A
- `01_capitulo1_mantenimiento/01_cu_login.md`
- `01_capitulo1_mantenimiento/02_cu_usuario.md`
- `01_capitulo1_mantenimiento/03_cu_paciente.md`
- `01_capitulo1_mantenimiento/04_cu_funcionario.md`
- `01_capitulo1_mantenimiento/05_referenciales_solo_lectura.md` (tabla de A.2 documentada como catálogos, no como CU de ABM)
- `01_capitulo1_mantenimiento/06_referenciales_abm.md` (cargo, empresa, sede, consultorio)
- Un diagrama de secuencia por cada CU con ABM real (login, usuario, paciente, funcionario, cargo, empresa, sede, consultorio)

---

## Fase B (documento) — Capítulo Agendamiento

Mapea 1:1 contra los 4 requerimientos que diste:
1. Registrar agenda médica → `agenda_horarios` (fusiona día+turno+bloque horario del diseño original, ver nota abajo)
2. Gestionar citas (reserva, confirmación, anulación) → `cita`
3. Gestionar avisos recordatorios → `recordatorio` (UltraMsg/WhatsApp)
4. Registrar documentos varios de la ficha médica (opcional) → cubierto por `ficha` (Cap. Clínico) referenciado desde la cita

**Nota que va en el documento, no una disculpa:** el diseño original (TALLER.MD) proponía 3 ABM independientes (Día, Turno, Bloque horario). Se reemplazan por una sola entidad `agenda_horarios` porque los tres datos siempre se configuran juntos en la operación real ("el especialista atiende los lunes de 8 a 12 en el consultorio 2"). `dia_semana` queda como catálogo de solo lectura (ver A.2).

**Entidad adicional no prevista:** `lista_espera` — se agrega como CU nuevo con su propia especificación, aclarando que surgió de la operación real, no del relevamiento original.

### Entregable de Fase B
- CU: Agenda médica (`agenda_horarios`), Gestionar citas, Gestionar avisos recordatorios, Lista de espera
- Diagramas de secuencia de cada uno (alta / anulación como mínimo)

---

## Fase C (documento) — Capítulo Clínico (llamado "Consultorio" en el documento original)

Mapea contra los 9 requerimientos que diste. Aclaración de nombre: el módulo se llama `clinico` en el código porque el sistema ya no es exclusivo de psicología; en el documento de tesis puede mantenerse el título "Módulo de Consultorio" si la cátedra lo exige literalmente, aclarando en una nota que el paquete de código usa `clinico` por alcance ampliado.

| # | Requerimiento | Entidad real |
|---|---|---|
| 1 | Registrar consulta | `consulta` + `anamnesis` |
| 2 | Registrar diagnóstico | `registro_clinico` (ver nota) |
| 3 | Registrar procedimientos e insumos | `registro_clinico` (mismo, ver nota) |
| 4 | Registrar orden de estudios | `orden` (ver nota) |
| 5 | Registrar orden de análisis | `orden` (mismo, ver nota) |
| 6 | Registrar recetas e indicaciones | `receta` |
| 7 | Registrar tratamientos | `tratamiento` |
| 8 | Registrar ficha médica | `ficha` |
| 9 | Registrar justificativo médico | `certificado_medico` (tipo "justificativo" vía catálogo `tipo_certificado_medico`) |

**Nota que va en el documento:** los requerimientos 2+3 comparten una sola entidad (`registro_clinico`) porque diagnóstico, signos, síntomas, procedimientos e insumos se registran en el mismo acto clínico, sobre la misma consulta — no tienen ciclo de vida propio. Lo mismo para 4+5 (`orden` unificada con un campo de tipo). Esto se documenta como decisión de diseño, con su propio diagrama de clase que muestre ambos requerimientos apuntando a la misma tabla.

**Fuera de los 9 puntos que diste, existen en el código:** PEI y Derivaciones. No están en tu lista de requerimientos — quedan pendientes de tu decisión: ¿los incluyo en el capítulo como anexo/ampliación, o los dejamos fuera del documento de tesis por no estar en el alcance que definiste? (a decidir en Fase C, no ahora).

### Entregable de Fase C
- 7 CU (uno por fila de la tabla, con 4+5 y 2+3 fusionados con nota aclaratoria)
- Diagramas de secuencia correspondientes

---

## Fase D (documento) — Capítulo Ventas / Facturación / Caja

Mapea 1:1 contra tus 10 requerimientos (ya en el orden que diste):

| # | Requerimiento | Entidad real |
|---|---|---|
| 1 | Registrar Pedido de Clientes | `pedido` |
| 2 | Registrar ventas y generar ctas a cobrar | `factura` + `cuenta_cobrar` |
| 3 | Registrar apertura y cierre de caja | `apertura_cierre_caja` |
| 4 | Registrar cobranzas por forma de cobro + comprobantes | `cobranza` |
| 5 | Registrar Nota de Remisión | `remision` + `remision_detalle` |
| 6 | Registrar Notas de Créditos y Débitos | `nota_credito`, `nota_debito` |
| 7 | Registrar el arqueo de caja | `arqueo_caja` |
| 8 | Registrar recaudaciones a depositar | `recaudacion` |
| 9 | Registrar Libro Ventas | `libro_ventas` |
| 10 | Elaborar Informes Web | **No implementado** → pasa a Fase E |

**Adicional no previsto, por marco legal (SIFEN Paraguay), va como nota de "Restricciones/Dependencias" del capítulo, no como CU nuevo:** `timbrado`, `punto_expedicion`, `tipo_comprobante`, `condicion_venta` — necesarios para que la factura sea válida fiscalmente.

### Entregable de Fase D
- 9 CU (el punto 10 se documenta como "diferido a Fase E")
- Diagramas de secuencia

---

## Fase E (documento + código) — Capítulo Reportes

**Esta es la única fase con trabajo de código pendiente real**, porque el documento original pide informes web en los 3 módulos (agendamiento, consultorio, ventas) y hoy no existe `app/dao/reportes` ni `app/rutas/reportes` con contenido.

Antes de escribir el capítulo hay que decidir alcance mínimo (básico, como pediste): probablemente listados simples con filtro de fecha por módulo, no un dashboard con gráficos. Esto se define en el arranque de esta fase, no ahora.

### Entregable de Fase E
- Definición de alcance mínimo de Reportes (a acordar)
- Implementación básica
- CU + diagrama de secuencia

---

## Fase F (documento + código) — Verificación UML, limpieza de código y cierre

1. **Verificación de instancias UML**: recorrer cada diagrama de clase y de secuencia del documento final contra el modelo real de base de datos (`docs_reestructuracion/sql_nueva_bd/`), entidad por entidad, marcando coincide / difiere / no existe.
2. **Limpieza de código**: eliminar los métodos `guardar/update/delete` muertos en los 8 referenciales de solo lectura (A.2), dejando el DAO tan simple como lo que realmente se usa — esto es lo "básico pero bien estructurado" que pediste, y es evidencia concreta de código auditado para el jurado.
3. **Formato APA**: aplicar portada, numeración, citas y referencias al documento consolidado (plantilla en `_plantillas/portada_apa.md`, a crear cuando se llegue a esta fase).
4. **Verificación de validaciones**: repasar reglas de negocio críticas por módulo (unicidad, estados, transiciones) contra lo documentado en cada CU.

---

## Cómo usar este plan
1. Se trabaja **una fase a la vez**, en su carpeta, con las plantillas de `_plantillas/`.
2. Cada CU se valida contra el código real (nombre de tabla, campos, endpoint) antes de darse por cerrado — no se redacta "a memoria".
3. No se pasa de fase sin que el capítulo anterior tenga sus CU + diagramas completos.
4. Vos seguís siendo quien edita/ajusta los diagramas UML en tu herramienta; este motor solo estandariza el texto que los acompaña.
