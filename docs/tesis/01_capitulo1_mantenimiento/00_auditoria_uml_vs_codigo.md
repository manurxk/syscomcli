# Auditoría — Capítulo Mantenimiento y Seguridad
## UML actual vs. TALLER.MD vs. código real

Este documento es la bitácora de trabajo de la Fase A (documento). Registra, en orden cronológico, cada decisión tomada y su evidencia — para que el proceso de nivelación quede trazable y defendible ante el jurado, no solo el resultado final.

---

## 0. Metodología de esta auditoría

Para cada caso de uso del UML se verificó:
1. **¿Existe en TALLER.MD?** (documento de diseño original, Cap. III)
2. **¿Existe en código?** — se comprobó archivo DAO, archivo de rutas (`*_routes.py`/`*_api.py`) y, cuando aplicó, la tabla SQL real (`docs_reestructuracion/sql_nueva_bd/`). No se acepta "existe el DAO" como prueba de ABM completo: se verificó que la ruta HTTP esté realmente registrada en `app/__init__.py` y que el método (`guardar/update/delete`) sea alcanzable — varios DAO tienen métodos de escritura que ninguna ruta invoca (código muerto).
3. **Veredicto**: `MANTENER` (sin cambios) / `QUITAR` (no debe seguir como ABM) / `MODIFICAR` (cambia de forma — fusión, reubicación, reinterpretación) / `AGREGAR` (existe en código pero no en el UML original).

---

## 1. Estructura UML recibida (tal cual, sin editar)

11 diagramas bajo `<<useCaseModel>> Use Case Model` en `SYSCOMCLI.uml`:

```
Main (vacío, placeholder de StarUML)
Modelo_negocio
 ├─ DC_GESTIONAR_MAN_SEG        (Administrador de sistema)
 │   ├─ DCU_REF_AGENDAMIENTO
 │   ├─ DCU_REF_CONSULTORIO
 │   ├─ DCU_REF_FACTURACIÓN
 │   └─ DCU_REF_MAN_SEG
 ├─ DC_GESTIONAR_AGENDAMIENTO   (Encargado de agendamiento)
 ├─ DC_GESTIONAR_CONSULTORIO    (Encargado de consultorio)
 ├─ DC_GESTIONAR_FACTURACION    (Encargado de venta y cobro)
 └─ DC_ELABORAR_INFORMES        (transversal: Administrador, Agendamiento, Consultorio, Venta y cobro)
```

## 2. Verificación contra TALLER.MD (Cap. III, sección 3)

Se revisó el índice y el cuerpo del documento original línea por línea. Orden real encontrado:

| Línea aprox. | Sección TALLER.MD | Contenido |
|---|---|---|
| 61 | 3.1 Registrar Mantenimiento y seguridad | Padre único de TODOS los referenciales |
| 62 | 3.1.1 Módulo Agendamiento | persona, bloque horario, especialidad, consultorio, ubicación, día, turno **+ diagnóstico, síntoma, tipo análisis, tipo estudio, medicamento, tipo procedimiento** (mezclados acá, ver hallazgo abajo) |
| — | *(3.1.2 no existe como encabezado)* | — |
| 244 | 3.1.3 Módulo Ventas | forma cobro, marca tarjeta, entidad adherida, entidad emisora, caja, tipo ítems, depósito |
| 343 | 3.2 Registrar Agendamiento | agenda médica, citas, avisos recordatorio, ficha médica (operación) |
| 400 | 3.3 Registrar Consultorio | consulta, diagnóstico, procedimiento/insumo, orden estudio, orden análisis, recetas, tratamiento, ficha médica, justificativo médico (operación) |
| 527 | 3.4 Registrar Ventas | pedido, cuentas cobrar, apertura/cierre caja, forma cobro, nota remisión, NC/ND, arqueo caja (operación) |

**Hallazgo 1 — confirmado**: TALLER.MD agrupa TODOS los referenciales (agenda, clínico, ventas) bajo un único caso de uso padre "3.1 Registrar Mantenimiento y seguridad", separado de la operación diaria (3.2/3.3/3.4). El UML de 11 diagramas respeta exactamente esta jerarquía (`DC_GESTIONAR_MAN_SEG` como padre de los 4 `DCU_REF_*`, con `DC_GESTIONAR_AGENDAMIENTO/CONSULTORIO/FACTURACION` como hermanos). **Conclusión: no hay que redibujar el UML para que "calque las carpetas del código" — ya es fiel al documento fuente y al criterio correcto de modelado (agrupar por actor, no por carpeta de implementación).**

**Hallazgo 2 — gap de numeración en el original**: TALLER.MD nunca declara un "3.1.2 Módulo Consultorio" — los referenciales clínicos quedan mezclados dentro de "3.1.1 Módulo Agendamiento" y el documento salta directo a "3.1.3 Módulo Ventas". El UML actual **ya corrige esto** al darle a Consultorio su propio diagrama (`DCU_REF_CONSULTORIO`). Se documenta como corrección de un error de numeración del borrador, no como desviación.

**Decisión tomada**: se mantiene la estructura de 11 diagramas tal como está. No se reestructura el UML.

---

## 3. Auditoría entidad por entidad

### 3.1 DCU_REF_AGENDAMIENTO (bajo Mantenimiento)

| Caso de uso (UML) | Código real | Ruta expuesta | Veredicto |
|---|---|---|---|
| Mantener especialidad | `agendamiento/referenciales/especialidad/` | ABM completo, activo | `MANTENER` — pero nota de ubicación: en código vive dentro del paquete `agendamiento`, no `mantenimiento`; en el UML puede seguir bajo Mantenimiento por agrupación de actor (ver Hallazgo 1) |
| Mantener día | `agendamiento/referenciales/dia_semana/` (`DiaSemanaDao`) | Solo `GET` (`getDiasSemana`, `getDiaSemanaById` — el DAO ni siquiera define guardar/update/delete) | `QUITAR` como ABM. Reinterpretar como catálogo de solo lectura (7 valores fijos, Lunes-Domingo). No se elimina la entidad, se elimina el caso de uso "Mantener" |
| Mantener turno | No existe como entidad independiente | — | `QUITAR` — absorbido, ver siguiente fila |
| Mantener bloque horario *(no está en tu lista pegada, pero sí en TALLER.MD)* | No existe como entidad independiente | — | `QUITAR` — fusionado junto con Turno y Día en `agenda_horarios` |
| Mantener consultorio | `mantenimiento/referenciales/consultorio/` (`ConsultorioDao`) | ABM completo (`guardarConsultorio`, `updateConsultorio`, `desactivarConsultorio`), cuelga de Sede | `MANTENER` |
| Mantener ubicación | No existe como entidad "ubicación" plana | — | `MODIFICAR` → reemplazada por `Ciudad`/`Departamento`/`País` (ver 3.4) + concepto nuevo `Sede` |
| Mantener persona | No existe "Persona" como entidad única | — | `MODIFICAR` → se dividió en `Paciente` (`mantenimiento/personas/paciente/PacienteDao.py`) y `Funcionario` (`mantenimiento/personas/funcionario/FuncionarioDao.py`), ambos con ABM completo. Paciente y Funcionario tienen atributos y reglas de negocio muy distintas (paciente no tiene cargo/fecha de ingreso, funcionario no tiene antecedentes clínicos) — separarlos es correcto |
| Mantener horario | No existe como mantenedor separado | — | `MODIFICAR` → absorbido en `agenda_horarios` (junto con día/turno/bloque horario), que además genera slots de citas automáticamente (`AgendaHorariosDao._generarSlots`) |

**Nuevo, no está en el UML**: `lista_espera` no es un referencial (es movimiento, va en el capítulo de Agendamiento operativo, no acá).

### 3.2 DCU_REF_CONSULTORIO (bajo Mantenimiento)

| Caso de uso (UML) | Código real | Ruta expuesta | Veredicto |
|---|---|---|---|
| Mantener tipo diagnóstico | `clinico/referenciales/diagnostico/` | ABM completo | `MANTENER` |
| Mantener síntomas | `clinico/referenciales/sintoma/` | ABM completo | `MANTENER` |
| Mantener tipo de análisis | `clinico/referenciales/tipo_analisis/` | ABM completo | `MANTENER` |
| Mantener tipo de estudio | `clinico/referenciales/tipo_estudio/` | ABM completo | `MANTENER` |
| Mantener medicamentos | `clinico/referenciales/medicamento/` | ABM completo | `MANTENER` |
| Mantener tipo procedimiento médico | `clinico/referenciales/tipo_procedimiento/` | ABM completo | `MANTENER` |

**Nuevo, no está en el UML — hay que decidir si se agregan (pendiente, ver §5):**
- `signo` (`clinico/referenciales/signo/`) — ABM completo
- `instrumento` (`clinico/referenciales/instrumento/`) — catálogo de tests/escalas psicológicas
- `insumo` (`clinico/referenciales/insumo/`) — ABM completo
- `tipo_tratamiento` (`clinico/referenciales/tipo_tratamiento/`) — ABM completo
- `tipo_certificado_medico` (`clinico/referenciales/tipo_certificado_medico/`) — ABM completo

### 3.3 DCU_REF_FACTURACIÓN (bajo Mantenimiento)

| Caso de uso (UML) | Código real | Ruta expuesta | Veredicto |
|---|---|---|---|
| Mantener forma de cobro | `ventas/referenciales/forma_cobro/` | ABM completo | `MANTENER` |
| Mantener marca tarjeta | `ventas/referenciales/marca_tarjeta/` | ABM completo | `MANTENER` |
| Mantener entidad adherida | `ventas/referenciales/entidad_adherida/` | ABM completo | `MANTENER` |
| Mantener entidad emisora | `ventas/referenciales/entidad_emisora/` | ABM completo | `MANTENER` |
| Mantener caja | `ventas/referenciales/caja/` | ABM completo | `MANTENER` |
| Mantener tipo de ítems | `ventas/referenciales/tipo_item/` | ABM completo | `MANTENER` (además existe `item_servicio`, más concreto — ver nuevos) |
| Mantener depósito | `ventas/referenciales/deposito/` | ABM completo | `MANTENER` |
| Mantener tipo impuestos | `ventas/referenciales/tipo_impuesto/` | ABM completo | `MANTENER` |

**Nuevo, no está en el UML — por marco legal SIFEN (Paraguay), pendiente de decisión (ver §5):**
- `timbrado`, `punto_expedicion`, `tipo_comprobante` — numeración fiscal obligatoria
- `condicion_venta`, `estado_factura`, `moneda`, `item_servicio` — operativos/normativos

### 3.4 Referenciales geográficos/demográficos (implícitos en "Mantener ubicación" y "Mantener persona" del UML original, hoy formalizados aparte)

| Entidad | Código real | Ruta expuesta | Veredicto |
|---|---|---|---|
| País | `mantenimiento/referenciales/pais/` | Solo `GET /api/v1/paises` (DAO tiene CRUD pero ninguna ruta lo invoca) | `QUITAR` como ABM — solo lectura de facto |
| Departamento | `mantenimiento/referenciales/departamento/` | Solo `GET /api/v1/departamentos` | `QUITAR` como ABM — solo lectura de facto |
| Ciudad | `mantenimiento/referenciales/ciudad/` | Solo `GET /api/v1/ciudades` | `QUITAR` como ABM — solo lectura de facto |
| Género | `mantenimiento/referenciales/genero/` | Solo `GET /api/v1/generos` | `QUITAR` como ABM — solo lectura de facto |
| Estado civil | `mantenimiento/referenciales/estado_civil/` | Solo `GET /api/v1/estados-civiles` | `QUITAR` como ABM — solo lectura de facto |
| Nivel de instrucción | `mantenimiento/referenciales/nivel_instruccion/` | Solo `GET /api/v1/niveles-instruccion` | `QUITAR` como ABM — solo lectura de facto |
| Profesión | `mantenimiento/referenciales/profesion/` | Solo `GET /api/v1/profesiones` | `QUITAR` como ABM — solo lectura de facto |

**Nuevo, no está en el UML — arquitectura multi-sede no prevista en el relevamiento original:**
- `empresa` (`mantenimiento/referenciales/empresa/`) — ABM completo
- `sede` (`mantenimiento/referenciales/sede/`) — ABM completo
- `cargo` (`mantenimiento/referenciales/cargo/`) — ABM completo (aplica a Funcionario)

### 3.5 DCU_REF_MAN_SEG (Seguridad)

| Caso de uso (UML) | Código real | Evidencia | Veredicto |
|---|---|---|---|
| Mantener login | `app/dao/auth/auth_dao.py`, `app/rutas/auth/` | Implementado: autenticación, historial de contraseñas (`obtener_historial_passwords`), reset por token (`crear_password_reset_token`, `resetear_password_con_token`) | `MODIFICAR` — el nombre "Mantener login" no corresponde a un ABM; es el caso de uso "Autenticar Usuario" (y aparte, "Recuperar contraseña"). Se renombra, no se elimina |
| Mantener menú | No existe tabla `menu` | El menú lateral se genera en Python (`app/utils/sidebar_builder.py`), filtrando ítems hardcodeados por rol de sesión (`session.get("roles")`) | `QUITAR` — no es un mantenedor de base de datos, es lógica de presentación. No corresponde como CU de ABM |
| Mantener roles | Tabla `roles` existe (`docs_reestructuracion/sql_nueva_bd/04_roles_auditoria.sql`) | Catálogo **fijo de 5 filas** con `CHECK (cod_rol IN ('SUPERADMIN','ADMINISTRADOR','RECEPCION','CLINICO','VENTAS'))` — agregar un rol nuevo requiere migración SQL, no hay pantalla de alta | `QUITAR` como ABM — es un catálogo cerrado por diseño, no un parámetro operativo |
| Mantener permisos | No existe tabla de permisos granulares | El control de acceso se hace por nombre de rol directamente en las rutas/decoradores, no hay entidad `Permiso` independiente de `Rol` | `QUITAR` — el modelo de seguridad implementado es RBAC simple (por rol), no un sistema de permisos granulares. No corresponde como CU |
| Mantener accesos | Tabla `accesos_sistema` existe | Bitácora automática de intentos de login (`resultado IN ('EXITOSO','FALLIDO_CLAVE','FALLIDO_BLOQUEADO',...)`), se llena sola en cada intento | `MODIFICAR` → reinterpretar como "Consultar accesos al sistema" (consulta/reporte, no alta manual) |

**Nuevo, no está en el UML:**
- `auditoria_sistema` (`AuditoriaDao`) — bitácora general de cambios (quién modificó qué), transversal a todo el sistema. Propuesta: agregar como CU "Consultar auditoría del sistema", junto con Accesos, ambos de solo consulta.
- Gestión de roles múltiples por usuario (`usuarios_roles`, `asignar_rol_usuario`, `remover_rol_usuario`, `cambiar_rol_principal` en `UsuarioDao`) — un usuario puede tener más de un rol activo a la vez (ej. ADMINISTRADOR + CLINICO). No estaba previsto en el UML original (que asume un actor = un rol).

---

## 4. Tabla resumen de veredictos (Mantenimiento y Seguridad)

| Veredicto | Cantidad | Entidades |
|---|---|---|
| `MANTENER` sin cambios | 15 | especialidad, consultorio, tipo diagnóstico, síntomas, tipo análisis, tipo estudio, medicamentos, tipo procedimiento, forma cobro, marca tarjeta, entidad adherida, entidad emisora, caja, tipo ítems, depósito, tipo impuestos |
| `QUITAR` (deja de ser ABM) | 10 | día, turno, bloque horario, país, departamento, ciudad, género, estado civil, nivel instrucción, profesión, menú, roles, permisos |
| `MODIFICAR` (cambia de forma) | 5 | ubicación→ciudad/país/sede, persona→paciente+funcionario, horario→agenda_horarios, login→autenticar, accesos→consultar accesos |
| `AGREGAR` (existe en código, no en UML) | ~13 | empresa, sede, cargo, signo, instrumento, insumo, tipo_tratamiento, tipo_certificado_medico, timbrado, punto_expedicion, tipo_comprobante, condicion_venta, estado_factura, moneda, item_servicio, auditoría, roles múltiples por usuario |

*(los conteos de "QUITAR" listan 13 nombres pero se cuentan 10 porque turno/bloque horario/horario se agrupan como una sola decisión de fusión, y algunos se repiten entre listas por prolijidad de trazabilidad — se ajusta al redactar el capítulo final)*

---

## 5. Pendientes — requieren tu decisión antes de cerrar el capítulo

1. **Referenciales clínicos nuevos** (signo, instrumento, insumo, tipo_tratamiento, tipo_certificado_medico): ¿se agregan al UML como parte de `DCU_REF_CONSULTORIO`, o se documentan aparte como ampliación?
2. **Referenciales SIFEN nuevos** (timbrado, punto_expedicion, tipo_comprobante, condicion_venta, estado_factura, moneda, item_servicio): mismo dilema — ¿entran al `DCU_REF_FACTURACIÓN` o van en nota de "Restricciones/Dependencias" del capítulo de Ventas?
3. **Auditoría y Accesos**: ¿se agregan como dos CU nuevos de solo consulta dentro de `DCU_REF_MAN_SEG`, o se dejan fuera del alcance del documento por ser bitácoras automáticas sin interacción de usuario?
4. **PEI y Derivaciones** (capítulo Clínico, no Mantenimiento — quedó pendiente de la conversación anterior): ¿entran al documento como anexo/ampliación del capítulo 3, o quedan fuera del alcance?
5. **Limpieza de código** (Fase F): confirmar que se puede eliminar el `guardar/update/delete` muerto de los 7 referenciales de solo lectura (país, departamento, ciudad, género, estado civil, nivel instrucción, profesión) — no se toca nada de código todavía, es solo para dejarlo agendado.

---

## 6. Próximo paso propuesto

Con esta auditoría cerrada, el siguiente paso natural es: vos ajustás el UML en tu herramienta aplicando los veredictos `QUITAR`/`MODIFICAR`/`AGREGAR` de la tabla del §4 (yo no toco el `.uml`), y en paralelo yo redacto las especificaciones de CU (con la plantilla de `_plantillas/plantilla_cu.md`) para los que quedan como `MANTENER`/`MODIFICAR`, empezando por Seguridad (Autenticar, Gestión de usuarios) ya que es lo que tiene más código construido y verificable.
