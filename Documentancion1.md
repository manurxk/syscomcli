# Documentación Exhaustiva de Negocio y Operativa - Sistema Angasys

El siguiente documento provee el marco analítico y normativo formal de la capa de negocio del ERP Clínico Angasys. Ha sido elaborado para cubrir con exhaustividad los procesos de Agendamiento, Consultorio, Facturación Electrónica SIFEN, Cobranzas y Notificaciones, bajo los perfiles de acceso de la clínica.

---

## 1. Glosario de Dominio

A continuación, se define la terminología clave del sistema, diferenciando el uso coloquial del rigor técnico aplicado en la arquitectura de Angasys:

| Término | Definición Técnica en Angasys |
| :--- | :--- |
| **Agenda Médica** | Módulo planificador compuesto por `agenda_horarios`. No es un simple calendario, sino una matriz de Días de la Semana (DOW) y Franjas Horarias que dictamina la capacidad máxima de un especialista. |
| **Cita Médica** | Transacción central que reserva un bloque indivisible de tiempo entre un paciente y un especialista. Posee ciclo de vida estricto (Agendada -> Confirmada -> Atendida / Cancelada). |
| **Colisión de Horario** | Falla de integridad lógica prevenida activamente. Ocurre cuando se intenta insertar una cita donde el binomio Fecha y Hora ya existe para el mismo paciente o especialista. |
| **Consultorio** | Instancia de atención clínica originada a partir de una cita "Confirmada". Aquí se asienta la Historia Clínica (anamnesis, signos, diagnósticos y recetas). |
| **Cupo Diario** | Límite matemático de pacientes que un especialista puede atender por día. El sistema lo descuenta temporalmente por cada agendamiento. |
| **Paciente** | Entidad de negocio que se distingue de forma única por su número de Cédula de Identidad, dato vital para enrutar comunicaciones y emitir comprobantes de la SET. |
| **Factura Electrónica** | Documento mercantil emitido desde un Punto de Expedición, estructurado internamente en formato XML bajo las directrices de la SET. |
| **Descomposición de IVA** | Proceso algorítmico ejecutado por la BD. El sistema recibe "Precios Finales", aplicando la fórmula de división de porcentajes para separar netos e impuestos automáticamente. |
| **SIFEN** | Sistema Integrado de Facturación Electrónica Nacional, el ente gubernamental regulador operado por la SET. |
| **Norma v150** | Especificación técnica (XSD) actual exigida de forma estricta por SIFEN para validar y autorizar los archivos XML de ventas. |
| **CDC (Código de Control)** | Hash numérico de exactamente 44 posiciones, generado algorítmicamente por la aplicación, que sirve como Primary Key de la factura a nivel nacional. |
| **KUDE** | Representación gráfica (usualmente un ticket PDF con código QR) de la Factura Electrónica que contiene el CDC para su verificación. |
| **Timbrado** | Estructura fiscal de control que otorga un rango numérico secuencial habilitado por la SET, sujeto a una fecha de caducidad estricta. |
| **Punto de Expedición** | Terminal de emisión o sub-sucursal lógica específica desde la que una caja genera comprobantes de venta de forma independiente. |
| **Cuenta a Cobrar** | Obligación financiera autogenerada cuando una factura se emite a Crédito, o cuando surge un copago pendiente. Balance dinámico mediante monto pendiente. |
| **Cobranza** | Asiento de flujo de caja que reduce parcial o totalmente el monto pendiente de una cuenta. Obliga a cruzar con una forma de cobro. |
| **UltraMsg** | Pasarela RESTful de terceros (API) consumida por Angasys para enrutar mensajes de texto automatizados vía WhatsApp sin intervención manual. |
| **Roles de Seguridad** | Decorador `@role_required` de Python en la capa de Rutas que intercepta la sesión HTTP y compara el grupo del usuario contra una matriz de permisos. |
| **Anulación Lógica** | Concepto donde los registros jamás se borran (DELETE). Simplemente mutan su campo de estado para dejar rastro histórico auditable. |
| **Presupuesto** | Módulo de cotización de planes de tratamiento que no tiene impacto fiscal automático ante la SET hasta su explícita aprobación por el paciente. |

---

## 2. Documento de Reglas de Negocio

### Módulo: Agenda Médica y Agendamiento

**Prevención de Colisiones de Agenda**
La regla de prevención de colisiones se dispara cada vez que el decorador de la API recibe una petición HTTP POST para crear una cita nueva. La validación recae en la comprobación bidireccional sobre la tabla de citas activas, verificando sistemáticamente que el especialista seleccionado no posea ya una agenda comprometida en la misma fecha y bloque horario. Asimismo, el sistema cruza esta validación para asegurar que el paciente no intente solapar su propio turno en dos consultorios simultáneamente. Ante el incumplimiento de este pre-requisito temporal, el objeto DAO declina la inserción con un retorno nulo, ocasionando que la interfaz detenga el flujo exhibiendo al operador un error de tipo "Bad Request", evitando cualquier sobre-agendamiento nocivo.

**Verificación de Cupos y Disponibilidad Base**
El sistema restringe la sobrecarga médica disparando esta regla al inicio del intento de agendamiento en la interfaz gráfica. Se valida lógicamente que el día de la semana escogido coincida con la matriz de horas laborales declaradas previamente, y examina que el flujo de citas no supere la cantidad tope del cupo diario acordado. A tal fin, si se transgrede este límite matemático, la capa del servidor rechaza formalmente la transacción y no despacha el turno, solicitando en cambio la reasignación hacia un día dotado de espacio operativo disponible.

### Módulo: Consultorio

**Acceso Restringido y Transición de Estados**
Dentro del consultorio médico integral, el formulario de anamnesis o atenciones es disparado cuando el especialista intenta abrir un legajo en el día de la fecha. La validación exige que este legajo de atención provenga única y exclusivamente de una Cita Médica que posea el estado estricto de "Confirmada". Consecuentemente, el sistema proscribe atender citas canceladas, caducas o pertenecientes a un futuro no transcurrido. Ante el incumplimiento material de esta regla, el sistema suprime los botones de tratamiento clínico de la interfaz y dictamina una denegación de operación, blindando el tracto legal de la historia médica del paciente. El mecanismo preciso donde cambia el estado de atendido se rige por [PENDIENTE DE CONFIRMAR], asumiendo por el relevamiento que ocurre al generar un diagnóstico.

### Módulo: Facturación Electrónica SIFEN (Ventas)

**Descomposición Matemática Impositiva**
El registro final de la facturación comercial acciona el proceso aritmético sobre los detalles médicos digitados. La capa lógica de base de datos valida irrevocablemente que los aranceles ingresados por el cajero representan el valor total al contado (Precios Finales), obligando al motor a ejecutar la sustracción del Impuesto al Valor Agregado gravado. Este cálculo se basa en derivar el importe exento, al 5% o al 10%, diviendo el monto entero por el factor tributario correspondiente. En la circunstancia de un incumplimiento por fallo aritmético, falla flotante o divisor nulo, la base de datos se retractará lanzando una excepción sistémica bloqueante que cancela en su totalidad la generación teórica del documento XML para la SET.

**Cumplimiento Integral de la Norma v150**
La normativa tributaria local requiere su cumplimiento justo en el umbral que el usuario presiona el envío y emisión formal del certificado SIFEN. Todo el payload JSON es validado contra los requerimientos precisos de un identificador de Código de Control de cuarenta y cuatro cifras generadas. Las exigencias estructurales requieren que el formato agrupe a RUC, fecha, sucursal, terminal y firma digital incrustada en el hash sin asimetrías. El incumplimiento sobre la arquitectura XSD o fallas por llaves revocadas resultará en la denegación total vía API tributaria, almacenándose el comprobante bajo una etiqueta roja de error criptográfico y quedando inutilizado el KUDE para circulación mercantil.

### Módulo: Cobranzas y Manejo de Saldos

**Amortización Lógica de las Cuentas a Cobrar**
En finanzas, la aplicación de todo ticket de ingreso de fondos desencadena la presente lógica operativa restrictiva de saneamiento. La inserción contable del nuevo pago efectúa una validación crítica contra el sumario del saldo acreedor del paciente (monto_pendiente), debiendo confirmar que el ingreso de caja jamás exceda a la deuda fiscal bruta. Una vez aprobado en la memoria relacional, transfiere este fondo deduciéndolo en la matriz del saldo. Cuando la deuda restante marca un equilibrio pleno de cero guaraníes, el estatus transiciona hacia un escenario de cancelación formal. En caso contrario y existiendo un incumplimiento —sea por montos inflados o deudas irreales— la inyección se repudia devolviendo una alerta preventiva de error transaccional excesivo al administrativo.

### Módulo: Notificaciones Automáticas UltraMsg

**Aislamiento de la Pasarela de Notificaciones**
La comunicación a terceros está programada para dispararse en segundo plano justo al momento en que la estructura central ha afirmado la inserción permanente en las bases de datos maestras. La aserción que efectúa demanda la estructura pura de un identificador telefónico regional junto al formato numérico correcto del paciente receptor. Si sobreviene el incumplimiento, por timeout de los servidores de WhatsApp, desuso de número por el paciente o inconsistencias HTTP propias, el sistema lo califica como un fallo silenciado y registra los hechos internamente en la tabla de excepciones de red, permitiendo a todos los flujos seguir operando ilesos a nivel nosocomial.

---

## 3. Manual de Usuario (Guías Operativas)

Por diseño de seguridad, este sistema Angasys controla los perfiles o accesos operacionales mediante filtros basados en decoradores (`@role_required`).

### Rol Operativo: **RECEPCIONISTA**

**Permisos y Restricciones**
Es el operador central de agendamientos y primer punto de contacto. Accede libremente al módulo de la Agenda Médica y a las Listas de Pacientes, pero está rotundamente inhibido, experimentando bloqueos con *mensajes error 403 (Acceso Denegado)*, si intenta visualizar el menú de ventas, anular turnos ajenos o consultar resúmenes financieros SIFEN.

**Flujo Operativo de Agendamiento Principal**
1. **Cómo acceder**: Inicie sesión en la pantalla inicial e ingrese al submenú **Agenda Médica** ubicado en la barra lateral izquierda.
2. Hacer clic en el botón visible delineado presuntamente como **Nueva Cita**.
3. Seleccionar la especialidad deseada y al médico interviniente.
4. Cargar o buscar al paciente con su número de cédula de identidad guaraní original y aguardar.
5. De la paleta verde visual de tiempos desocupados, elegir un recuadro de bloque horario.
6. Guardar la reservación en base.  
**Posibles Mensajes de Error Esperados**:
* *Error de Conflicto*: Mensaje rojo de choque que dicta textualmente "El profesional o el paciente ya poseen un turno en el horario". Resulta cuando debe forzosamente volver a escoger otro intervalo desocupado.

### Rol Operativo: **VENTAS / CAJA**

**Permisos y Restricciones**
Es un rol circunscripto a la tributación diaria de la clínica. Ingresa a todo el conjunto de aranceles, emitirá las facturas de contado y gestionará los saldos adeudados de tratamientos extensivos. Tiene el impedimento técnico absoluto y formal de asomarse a leer los registros, síntomas y medicamentos dictados en el marco confidencial de los consultorios (impidiendo accesos no éticos).

**Flujo Operativo de Cobranza (Recibo de Dinero)**
1. **Cómo acceder**: Ingrese al panel inicial y expanda la sección **Ventas**, eligiendo a la vista el listado de **Cuentas a Cobrar / Saldos**.
2. Con la ayuda del buscador de la cabecera, digite el número de RUC, cédula, o nombre del deudor.
3. Una vez se filtre en la pantalla, pulse en la alternativa operativa de **Registrar Pago**.
4. Ingrese con máxima prolijidad manual la cantidad monetaria cedida por el sujeto, la procedencia del dinero (ej: Tarjeta, Depósito) y la terminal de caja donde obra.
5. Aprobar la remisión final de fondos a la empresa. La deuda pasará al estatus "Pagado" y desaparecerá de su alerta.  
**Posibles Mensajes de Error Esperados**:
* *Fallo de Exceso de Pago*: El aplicativo frenará el accionar si los importes rebasan los decimales lógicos acordados, alertándole acerca de una irregularidad financiera de la deuda superada. Todo el vuelto efectivo es exterior a la herramienta.

### Rol Operativo: **ADMINISTRADOR**

**Permisos y Restricciones**
El máximo eslabón directivo dentro del organigrama sistémico. Transita el ERP local completo y puede forzar todas las mecánicas que involucran correcciones técnicas y autorizaciones. Podrá anular transacciones o enmendar roles sin restricción frontal de seguridad alguna.

**Flujo Operativo de Configuración de SIFEN**
1. **Cómo acceder**: Ingresar al apartado especializado delineado como **Administración / Empresa** situado en el último peldaño de la barra lateral.
2. Acceder y revisar los timbrados impositivos actualmente cargados y marcados en alertas rojas si hubieren sobrepasado formalmente su fecha tope legal.
3. Escoger el comando interno **Nuevo Timbrado** e ingresar los extensos patrones cedidos por escrito por la Subsecretaría de Tributación (SET).
4. Settear inminentemente las validaciones de vencimiento estricto solicitadas.
5. Someterlo al servidor interno, cerciorándose obligatoriamente que este bloque sea ligado a un "Punto de Expedición" (la caja registradora específica para los facturadores de ventanilla).  
**Posibles Mensajes de Error Esperados**:
* Fallos sobrevenidos en base de datos si la asignación no cumple un marco de fechas válidas para la red paraguaya, o advertencias locales dictaminadas si intentó borrar de raíz un usuario activo del sanatorio (el cual sólo debe inactivarse).

---
*Fin Documentación Operativa y del Negocio - Revisión Angasys Marzo 2026*
