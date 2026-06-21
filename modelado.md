


SISTEMA DE GESTIÓN DE AGENDAMIENTO, CONSULTORIO Y FACTURACIÓN PARA LA CLÍNICA INTEGRAL NEUROPSICOLÓGICA 





ALUMNO:

Armando Manuel Ramírez Ramírez

DOCENTE:

Dr. Cristian David Macen Rojas



Trabajo final presentada a la Sede de Ñemby-Facultad de Tecnología Informática, de la Universidad Tecnológica Intercontinental para la culminación de la materia:


MODELADO DE LA INFORMACIÓN



Ñemby – Paraguay
junio, 2025



Tabla de contenido
1. INTRODUCCIÓN	6
1.1 Datos de la empresa	6
1.2 Descripción de la organización	6
1.3 Organigrama de la organización	7
1.4 Planteamiento del Problema	8
2. ANTECEDENTES DEL SOFTWARE	10
2.1 Módulo de agendamiento	10
2.2 Módulo de consultorio	14
2.3 Módulo de ventas	17
3. LISTA DE REQUERIMIENTOS	20
3.1 Módulo de agendamiento	20
3.2 Módulo de consultorio	21
3.3 Módulo de ventas	22
4. DICCIONARIO DE DATOS	23
4.1 Módulo de agendamiento	23
4.1.1 Prototipos de Referenciales de agenda médica	23
4.1.1.1 Ventana de Persona	23
4.1.1.1.1 Descripción de los campos	24
4.1.1.2 Ventana de Bloque Horario	29
4.1.1.2.1 Diagrama entidad relación	29
4.1.1.2.2 Descripción de los campos	30
4.1.1.3 Ventana de Especialidad	33
4.1.1.3.1 Diagrama entidad relación	33
4.1.1.3.2 Descripción de los campos	33
4.1.1.4 Ventana de Consultorio	36
4.1.1.4.1 Diagrama entidad relación	36
4.1.1.4.2 Descripción de los campos	37
4.1.1.5 Ventana de Ubicación	40
4.1.1.5.1 Diagrama entidad relación	40
4.1.1.5.2 Descripción de los campos	41
4.1.1.6 Ventana de Dia	43
4.1.1.6.1 Diagrama entidad relación	43
4.1.1.6.2 Descripción de los campos	43
4.1.1.7 Ventana de Turno	46
4.1.1.7.1 Diagrama entidad relación	46
4.1.1.7.2 Descripción de los campos	46
4.1.2 Prototipos de Movimientos de Agendamiento	49
4.1.2.1 Ventana de Registrar Agenda Médica	49
4.1.2.1.1 Diagrama entidad relación	49
4.1.2.1.2 Descripción de los campos	50
4.1.2.2 Ventana de Gestionar Citas	57
4.1.2.2.1 Diagrama entidad relación	57
4.1.2.2.2 Descripción de los campos	58
4.1.2.3 Ventana de Gestionar Avisos Recordatorio	62
4.1.2.3.1 Diagrama entidad relación	62
4.1.2.3.2 Descripción de los campos	63
4.1.2.4 Ventana de Registrar Ficha Médica	68
4.1.2.4.1 Diagrama entidad relación	68
4.1.2.4.2 Descripción de los campos	69
4.2 Módulo de consultorio	77
4.2.1 Prototipos de Referenciales de consultorio	77
4.2.1.1 Ventana de Tipo Diagnóstico	77
4.2.1.1.1 Diagrama entidad relación	77
4.2.1.1.2 Descripción de los campos	77
4.2.1.2 Ventana de Síntomas	80
4.2.1.2.1 Diagrama entidad relación	80
4.2.1.2.2 Descripción de los campos	80
4.2.1.3 Ventana de Tipo Análisis	83
4.2.1.3.1 Diagrama entidad relación	83
4.2.1.3.2 Descripción de los campos	83
4.2.1.4 Ventana de Tipo  Estudio	86
4.2.1.4.1 Diagrama entidad relación	86
4.2.1.4.2 Descripción de los campos	86
4.2.1.5 Ventana de Medicamento	89
4.2.1.5.1 Diagrama entidad relación	89
4.2.1.5.2 Descripción de los campos	89
4.2.1.6 Ventana de Tipo Procedimiento Médico	92
4.2.1.6.1 Diagrama entidad relación	92
4.2.1.6.2 Descripción de los campos	92
4.2.2 Prototipos de Movimientos de Consultorio	95
4.2.2.1 Ventana de Registrar Consulta	95
4.2.2.1.1 Diagrama entidad relación	95
4.2.2.1.2 Descripción de los campos	96
4.2.2.2 Ventana de Gestionar Diagnóstico	105
4.2.2.2.1 Diagrama entidad relación	105
4.2.2.2.2 Descripción de los campos	106
4.2.2.3 Ventana de Gestionar Procedimiento Médico	112
4.2.2.3.1 Diagrama entidad relación	112
4.2.2.3.2 Descripción de los campos	113
4.2.2.4 Ventana de Generar Orden Estudios	119
4.2.2.4.1 Diagrama entidad relación	119
4.2.2.4.2 Descripción de los campos	120
4.2.2.5 Ventana de Generar Orden Análisis	126
4.2.2.5.1 Diagrama entidad relación	126
4.2.2.5.2 Descripción de los campos	127
4.2.2.6 Ventana de Registrar Recetas e Indicaciones	133
4.2.2.6.1 Diagrama entidad relación	133
4.2.2.6.2 Descripción de los campos	134
4.2.2.7 Ventana de Registrar Tratamiento	141
4.2.2.7.1 Diagrama entidad relación	141
4.2.2.7.2 Descripción de los campos	142
4.2.2.8 Ventana de Generar Ficha Médica	150
4.2.2.8.1 Diagrama entidad relación	151
4.2.2.8.2 Descripción de los campos	152
4.2.2.9 Ventana de Generar Justificativo Médico	162
4.2.2.9.1 Diagrama entidad relación	162
4.2.2.9.2 Descripción de los campos	163
4.3 Módulo de Ventas	171
4.3.1 Prototipos de Referenciales de ventas	171
4.3.1.1 Ventana de Forma de cobro	171
4.3.1.1.1 Diagrama entidad relación	171
4.3.1.1.2 Descripción de los campos	171
4.3.1.2 Ventana de Marca Tarjeta	174
4.3.1.2.1 Diagrama entidad relación	174
4.3.1.2.2 Descripción de los campos	174
4.3.1.3 Ventana de Entidad Emisora	177
4.3.1.3.1 Diagrama entidad relación	177
4.3.1.3.2 Descripción de los campos	178
4.3.1.4 Ventana de Entidad Adherida	180
4.3.1.4.1 Diagrama entidad relación	180
4.3.1.4.2 Descripción de los campos	181
4.3.1.5 Ventana de Caja	184
4.3.1.5.1 Diagrama entidad relación	184
4.3.1.5.2 Descripción de los campos	185
4.3.1.6 Ventana de Tipo items	187
4.3.1.6.1 Diagrama entidad relación	187
4.3.1.6.2 Descripción de los campos	188
4.3.1.7 Ventana de Depósito	190
4.3.1.7.1 Diagrama entidad relación	190
4.3.1.7.2 Descripción de los campos	191
4.3.1.8 Ventana de Tipo Impuesto	193
4.3.1.8.1 Diagrama entidad relación	193
4.3.1.8.2 Descripción de los campos	193
4.3.2 Prototipos de Movimientos de Ventas	196
4.3.2.1 Ventana de Registrar Pedido Cliente	196
4.3.2.1.1 Diagrama entidad relación	196
4.3.2.1.2 Descripción de los campos	197
4.3.2.2 Ventana de Gestionar Ventas y Generar Cuentas a Cobrar	204
4.3.2.2.1 Diagrama entidad relación	204
4.3.2.2.2 Descripción de los campos	205
4.3.2.3 Ventana de Registrar Apertura y cierre de caja	211
4.3.2.3.1 Diagrama entidad relación	211
4.3.2.3.2 Descripción de los campos	212
4.3.2.4 Ventana de Gestionar Forma de cobro	221
4.3.2.4.1 Diagrama entidad relación	221
4.3.2.4.2 Descripción de los campos	222
4.3.2.5 Ventana de Registrar Nota de Remisión	232
4.3.2.5.1 Diagrama entidad relación	232
4.3.2.5.2 Descripción de los campos	233
4.3.2.6 Ventana de Gestionar Notas de Créditos y Débitos	239
4.3.2.6.1 Diagrama entidad relación	239
4.3.2.6.2 Descripción de los campos	240
4.3.2.7 Ventana de Arqueo de Caja	245
4.3.2.7.1 Diagrama entidad relación	246
4.3.2.7.2 Descripción de los campos	247
4.4 Generar Informes	256
4.4.1 Ventana informes de referenciales de agendamiento	256
4.4.2 Ventana informes de referenciales de consultorio	256
4.4.3 Ventana informes de referenciales de ventas	257
4.4.4 Ventana informes de movimientos de agendamiento	258
4.4.5 Ventana informes de movimientos de consultorio	258
4.4.6 Ventana informes de movimientos de ventas	259
5. CONCLUSIÓN	260
6. REFERENCIAS	261
7. APÉNDICE	262
7.1 Documentos	262
7.1.1 Módulo de agendamiento	262
7.1.2 Módulo de consultorio	264
7.1.3 Módulo de ventas	269
7.2 Relevamiento	273
7.2.1 Módulo de agendamiento	273
7.2.2 Módulo de consultorio	275
7.2.3 Módulo de ventas	280
INTRODUCCIÓN
Datos de la empresa
Razón Social: Clínica Integral Neuropsicológica CIN
Dirección:  José Martí 5160 entre Charle de Gaulle y Cruz del Chaco.
Ciudad: Asunción 
Celular: 0982 388921
Propietaria: Dra. Joanna Muñoz.
Descripción de la organización
La Clínica Integral Neuropsicológica brinda a sus pacientes instalaciones de vanguardia y atención por parte de profesionales de primer nivel que cuentan con la capacitación y el entrenamiento. En el año 2015, CIN abrió sus puertas a la población de Asunción, desde entonces, su misión es ofrecer cuidados de calidad en un entorno seguro adquiriendo la reputación del Centro de salud neuropsicológico líder en el área. Cuenta con servicios personalizados que le permite atender cualquier problema de salud mental, el desarrollo intelectual y la rehabilitación cognitiva del aprendizaje, lenguaje, afectivo y social, garantizando a partir de diferentes estrategias el bienestar psíquico a partir del conocimiento de las neurociencias.

Organigrama de la organización





Planteamiento del Problema
Módulo Agendamiento:
La agenda médica se organiza de manera manual en planillas esto dificultando la consulta en cuanto a disponibilidad y provocando errores, también afectando los horarios. La gestión de citas (reservas, confirmaciones, anulaciones) se realiza por teléfono enviando mensajes por sms y whatsApp de forma manual, sin formato específico, lo que provoca pérdidas de información. No hay un historial digital que registre las acciones sobre las citas. Los recordatorios se envían manualmente, igual que las confirmaciones de cita lo que  demanda tiempo y no garantiza que los pacientes asistan.
Módulo Consultorio:
El especialista no tiene acceso ágil a datos clínicos del paciente ya que estos se archivan por carpetas de forma manual lo que toma tiempo para seguir un diagnósticos o tratamientos. Los procedimientos, recetas e indicaciones se registran de forma manual, tampoco poseen una respaldo digital. Las órdenes de estudios y certificados médicos se emiten manualmente, con riesgo de errores y falta de validez formal. No existen informes automatizados sobre la atención del consultorio.
Módulo Ventas:
En los procesos de apertura y cierre de caja se hacen manualmente cada día lo que facilita errores. Los pedidos se registran consultando el stock de forma manual provocando demoras. La facturación y cuentas a cobrar se gestionan de forma ambigua según la necesidad. El libro de ventas se lleva en una planilla básica. Los cobros, pedidos de cliente y el contrato de tratamiento no se relacionan de manera eficiente, dificultando conciliaciones y reportes.


ANTECEDENTES DEL SOFTWARE 
Módulo de agendamiento
AgendaPro
Enfocado en: Clínicas, consultorios y centros médicos en Latinoamérica.
Características principales:
Agenda médica online (24/7):
Los pacientes pueden reservar citas en línea a cualquier hora del día.
Integración con el sitio web o redes sociales del consultorio.
Evita llamadas telefónicas innecesarias y reduce tiempos de gestión manual.
Recordatorios automáticos:
Envío de alertas por SMS, WhatsApp o correo electrónico.
Reduce significativamente las inasistencias a las citas.
Fichas clínicas digitales:
Historial médico completo de cada paciente.
Permite agregar notas, diagnósticos, archivos adjuntos, tratamientos, y recetas.
Personalización por especialidad médica.
Control de inventario:
Gestión de stock de insumos médicos o productos de venta.
Alertas automáticas cuando hay escasez o vencimiento.

Gestión de pagos e informes financieros:
Registro de pagos por cita o producto.
Facturación electrónica (en países que lo permiten).
Panel financiero con estadísticas de ingresos, citas realizadas, cancelaciones, etc.
Módulo de marketing:
Seguimiento de pacientes inactivos.
Campañas automatizadas para fidelizar clientes (felicitaciones, promociones, etc.).
Acceso multiusuario y por perfiles:
Permite configurar roles: médicos, secretarias, administradores.
Control de permisos y acceso a funciones.
Ventajas:
Interfaz intuitiva.
Soporte en español con atención personalizada.
Ideal para clínicas que buscan digitalizar su proceso completo.
Precios aproximados:
Tiene un plan gratuito de prueba.
Los planes pagos parten desde USD 29 por mes por profesional (varía según país y módulo contratado).
Incluyen funcionalidades escalables: desde solo agenda hasta CRM, marketing y finanzas.

Carepatron
Enfocado en: Profesionales de la salud independientes, clínicas pequeñas y equipos interdisciplinarios en todo el mundo.
Características principales:
Agendamiento de citas:
Calendario sincronizable con Google Calendar.
Visualización por día, semana, profesional, o tipo de servicio.
Citas ilimitadas incluso en el plan gratuito.
Portal del paciente:
Acceso seguro donde el paciente puede:
Agendar o reprogramar citas.
Consultar sus notas clínicas y documentos.
Completar formularios previos a la cita.
Telesalud integrada:
Videollamadas médicas seguras y encriptadas.
Enlace único para cada consulta, sin necesidad de apps externas.
Historial de videollamadas y notas integradas.
Notas clínicas y documentación:
Plantillas personalizables para diferentes especialidades.
Firma electrónica y almacenamiento seguro (cumple HIPAA y GDPR).
Integración con evaluaciones clínicas y diagnósticos.
Facturación y cobros:
Generación de facturas y recibos automáticos.
Registro de pagos, reembolsos, y cobros pendientes.
Integración con Stripe para recibir pagos online.
Automatización de recordatorios:
Recordatorios automáticos por email o SMS.
Plantillas editables.
Colaboración en equipo:
Permite añadir otros profesionales y personal administrativo.
Chat interno y gestión compartida de pacientes.
Ventajas:
Muy buen plan 100% gratuito sin límite de pacientes o citas.
Excelente para profesionales que trabajan remoto o en varias ubicaciones.
Multilingüe, con interfaz disponible en español,
Precios aproximados:
Gratis: para 1 usuario, con funcionalidades completas (agenda, portal, videollamadas).
Planes pagos (desde USD 12/mes): agregan funcionalidades como más usuarios, branding personalizado, análisis avanzados, etc.

Módulo de consultorio
SaludVitale – Software para Consultorios Médicos
Es una plataforma diseñada para facilitar la gestión integral de consultorios médicos, ofreciendo herramientas que optimizan la atención al paciente y la administración del consultorio
Características principales:
Gestión de citas: Permite programar y administrar citas médicas a través de la web o una aplicación móvil, accesible desde cualquier dispositivo y en cualquier momento.
Recordatorios automáticos: Envía notificaciones por WhatsApp y correo electrónico para reducir ausencias, permitiendo a los pacientes confirmar o cancelar sus citas fácilmente.
Historia clínica electrónica: Digitaliza las historias clínicas, reduciendo el uso de papel y optimizando el espacio físico del consultorio.
Informes médicos automatizados: Genera informes y documentos personalizados con logo, firma y sello digital, facilitando la documentación médica.
Recetas electrónicas: Permite crear y enviar recetas médicas digitales a los pacientes por WhatsApp o correo electrónico.
Facturación electrónica: Integra con el software contable Alegra para emitir facturas electrónicas conforme a las normativas fiscales del país.
Funciones destacadas:
Seguridad de la información: Cuenta con certificados de seguridad (SiteLock) para proteger los datos sensibles de los pacientes.

MedFlow – Sistema Integral para Clínicas y Consultorios Médicos
Es un software paraguayo desarrollado específicamente para facilitar la administración médica en centros de salud de distintos tamaños, desde pequeños consultorios individuales hasta clínicas con múltiples especialidades. Su diseño intuitivo y sus funciones avanzadas permiten a los profesionales de la salud optimizar sus tareas administrativas, mejorar la atención al paciente y cumplir con las normativas locales.
FUNCIONALIDADES DESTACADAS
Historia clínica electrónica completa
Registros médicos centralizados por paciente: antecedentes, diagnósticos, evoluciones, recetas, órdenes de estudios, etc.
Adjuntos: permite subir estudios, imágenes, certificados o documentos relacionados a cada ficha médica.
Plantillas configurables por especialidad: medicina general, ginecología, psicología, psicología, etc.
Facturación electrónica
Compatible con la normativa fiscal paraguaya.
Generación de facturas electrónicas por consulta, procedimientos u otros servicios.
Integración con métodos de pago: efectivo, POS, transferencia o plataformas online.
Emisión de comprobantes electrónicos con código QR.

Portal del paciente
Acceso personalizado para cada paciente con clave segura.
Consultas de citas pasadas y futuras, recetas médicas, resultados de estudios.
Posibilidad de solicitar turnos y ver disponibilidad de profesionales.
Notificaciones automáticas
Recordatorios de citas por WhatsApp, SMS o correo electrónico.
Alertas de vencimientos, seguimiento de tratamientos o estudios pendientes.
Comunicación directa entre el consultorio y el paciente.
Módulo administrativo
Control de ingresos y egresos diarios.
Gestión de caja y arqueos automáticos.
Reportes financieros, productivos y de asistencia médica.
Reportes por sucursal (en caso de clínicas con varias sedes).
Soporte multi clínica y multiusuario
Permite operar con varias clínicas o sucursales desde una misma cuenta.
Control de accesos según rol: administrador, médico, recepcionista, contabilidad, etc.
Configuración independiente de agendas, facturación y reportes por cada sede.


SEGURIDAD Y TECNOLOGÍA
Software en la nube: accesible desde cualquier lugar con conexión a internet.
Respaldos automáticos diarios de todos los datos.
Módulo de ventas
Software de facturación: Holded
Es una plataforma de gestión empresarial en la nube que ofrece soluciones para facturación, contabilidad, CRM, proyectos y más. Es especialmente útil para pequeñas y medianas empresas (PYMEs) que buscan automatizar y simplificar sus procesos administrativos.
Características principales:
Facturación electrónica: Crea y envía facturas personalizadas de manera sencilla.
Gestión de clientes y productos: Administra tu base de datos de clientes y catálogos de productos o servicios.
Control de inventario: Supervisa el stock en tiempo real y recibe alertas de niveles bajos.
Contabilidad integrada: Automatiza asientos contables y genera informes financieros.
CRM y gestión de proyectos: Organiza tus relaciones con clientes y gestiona proyectos desde la misma plataforma.
Funciones destacadas:
Emisión de presupuestos y facturas: Genera documentos profesionales con tu logotipo y colores corporativos.
Seguimiento de pagos: Controla facturas pendientes y recibe notificaciones de vencimientos.
Integraciones: Conecta con otras herramientas como bancos, plataformas de e-commerce y aplicaciones de productividad.

eVENDÉ
Es una plataforma paraguaya de facturación electrónica diseñada para pequeñas y medianas empresas. Ofrece una solución integral que cumple con las normativas de la Subsecretaría de Estado de Tributación (SET) y facilita la gestión administrativa y financiera.
Características principales:
Sistema web accesible desde cualquier dispositivo: Puedes facturar desde una computadora, tablet o celular, sin necesidad de instalaciones adicionales.
Facturación electrónica conforme a la SET: Cumple con las regulaciones fiscales paraguayas, incluyendo la generación del KUDE (comprobante impreso).
Gestión de inventario y control de stock: Permite llevar un seguimiento detallado de tus productos y niveles de existencias.
Libros IVA y RG90: Genera automáticamente los libros requeridos por la SET.
Informes gerenciales en tiempo real: Accede a reportes detallados para tomar decisiones informadas.
Interfaz intuitiva y fácil de usar: Diseñada para usuarios sin experiencia técnica.
Soporte técnico incluido: Asistencia disponible para resolver dudas o inconvenientes.
Funciones destacadas:
Emisión de facturas electrónicas: Crea y envía facturas personalizadas a tus clientes.
Control de clientes y productos: Administra tu base de datos de clientes y catálogos de productos o servicios.
Automatización de procesos: Genera presupuestos, órdenes de pedido y facturas de forma rápida y eficiente.
Acceso multiusuario: Permite que diferentes miembros del equipo trabajen simultáneamente con permisos personalizados.



LISTA DE REQUERIMIENTOS
Módulo de agendamiento
EVENTO
REQUERIMIENTO
ESTÍMULO
RESPUESTA
La recepcionista registra la agenda médica
Registrar agenda médica.
Solicitud de la agenda médica
Agenda Médica registrada.
Recepcionista gestiona las citas, reserva, confirma, anula y reagenda.
Gestionar citas, reservación, confirmación, anulación y reagendamiento.
Solicitud de cita.
Citas registradas
Recepcionista genera los avisos recordatorios.
Generar avisos recordatorios
Solicitud de avisos recordatorios
Avisos recordatorios registrados
Especialista solicita informes web de agendamiento.
Elaborar informes web de agendamiento.
Solicitud de informes web de agendamiento.
Informes web de agendamiento generado.


Módulo de consultorio
EVENTO
REQUERIMIENTO
ESTÍMULO
RESPUESTA
Especialista genera presupuesto.
Generar Presupuesto.
Solicitud de presupuesto.
Presupuesto generado.
El especialista gestiona la consulta.
Gestionar consulta
Solicitud de la consulta.
Consulta registrada.
Especialista registra diagnóstico.
Registrar diagnóstico
Necesidad de diagnóstico.
Diagnóstico registrado.
El especialista registra los procedimientos e insumos utilizados.
Registrar procedimientos e insumos utilizados
Obtener insumos utilizados en procedimientos.
Procedimientos e insumos utilizados registrados.
Especialista genera orden de estudios.
Generar orden de estudios
Solicitud de generar orden de estudios.
Orden de estudio generado.
Especialista registra recetas e indicaciones.
Registrar recetas e indicaciones.
Solicitud de recetas e indicaciones.
Recetas e indicaciones registrados
Especialista registra tratamientos.
Registrar tratamientos.
Solicitud de tratamientos.
Tratamientos registrados.
Especialista genera historial clínico.
Generar historial clínico.
Solicitud de historial clínico.
Historial Clínico
generado.
Gerente General solicita informes web de consultorio.
Elaborar informes web de consultorio.
Solicitud de informes web de consultorio.
Informes web de consultorio elaborado.

Módulo de ventas
EVENTO
REQUERIMIENTO
ESTÍMULO
RESPUESTA
Él cajero registra apertura y cierre de caja.
Registrar apertura y cierre de caja.
Solicitud de apertura y cierre de caja.
Apertura y cierre registrado.
Él  cajero genera el arqueo de caja.
Generar el arqueo de caja.
Solicitud de arqueo de caja.
Arqueo de caja generado.
Él cajero genera recaudaciones a depositar.
Generar recaudaciones a depositar
Solicitud de generar recaudaciones a depositar.
Recaudaciones a depositar generadas.
Él cajero gestiona facturación y genera cuentas a cobrar.
Gestionar facturación y generar cuentas a cobrar.
Solicitud de ventas.
Facturación y cuentas a cobrar registradas.
Él cajero gestiona las cobranzas por formas de cobro e imprime comprobantes.
Gestionar las cobranzas por forma de cobro (efectivo, cheque, tarjeta de crédito y débito) e imprimir comprobantes.
Solicitud de cobro.
Cobro registrado e impreso.
Él cajero genera notas de créditos y débitos.
Generar notas de créditos y débitos.
Solicitud de notas de créditos y débitos.
Notas de créditos y débitos registrados.
Él cajero  solicita informes web de ventas.
Elaborar informes web de ventas.
Solicitud de informes de ventas.
Informes web de ventas elaborados.

DICCIONARIO DE DATOS 
Módulo de agendamiento
Prototipos de Referenciales de agenda médica
Ventana de Persona
Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Personas
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
persona_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_nombre
carácter
SI
Este campo almacenara el nombre de la persona.
persona_apellido
carácter
SI
Este campo almacenara el apellido de la persona.
persona_cedula
carácter
SI
Este campo almacenara la cédula de la persona.
persona_sexo
carácter
SI
Este campo almacenara el sexo.
persona_correo
carácter
SI
Este campo almacenara el correo de la persona.
persona_direc
carácter
SI
Este campo almacenara la dirección de la persona.
persona_telfono
carácter
SI
Este campo almacenara el número de teléfono.
persona_fecha_nac
carácter
SI
Este campo almacenara la fecha de nacimiento.
persona_rol
carácter
SI
Este campo almacenara lel rol de la persona.
ubicacion_cod
Clave foránea
SI
Almacena la clave foránea de ubicación.


NOMBRE DE LA TABLA: Especialistas
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
especialidad_cod
Clave foránea
SI
Almacena la clave foránea de especialidad.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


funcionario_cod
Clave foránea
SI
Almacena la clave foránea de funcionario.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenará la fecha de fecha de registro del paciente.
contacto_emergencia
carácter
SI
Este campo almacenara el nombre del contacto de emergencia del paciente.
telefono_emergencia
carácter
SI
Este campo almacenara el número de teléfono del contacto de emergencia.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
cargos_cod
Clave foránea
SI
Este campo almacenara clave foránea de cargos.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
tipo_contrato
carácter
SI
Almacenara el tipo de contrato del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.




Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las personas
v_ persona: visualización de las personas presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar el formato de datos específicos.
Validar que no se ingresen caracteres no permitidos.
Validar al actualizar que no se generen conflictos



Ventana de Bloque Horario

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Bloques Horarios
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
bloque_hora_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
dia_cod
Clave foránea
SI
Almacena la clave foránea del dia.
hora_estado
booleano
SI
Este campo almacenara el estado de las horas de inicio disponible del especialista.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
disponibilidad_hora
time
SI
Este campo almacenara las horas disponibles del especialista.
hora_inicio
time
SI
En este campo se podrá guardar la hora inicial disponible del especialista.
hora_fin
time
SI
En este campo se podrá guardar la hora final disponible del especialista.
duracion
date
SI
En este campo se podrá guardar la duración de cada turno del especialista.
cantidad_turno
integer
SI
En este campo se podrá guardar la cantidad de turnos disponible del especialista.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las horas disponibles.
v_bloque_horario: visualización de las disponibilidades horarias presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el horario final sea mayor que el horario inicio.
Validar que el especialista no tenga dos disponibilidades el mismo día.
Validar que el especialista no tenga cierto número de horas por día(máx:8hs).
Validar que el campo cupo se ingrese números enteros y positivos.
Validar que los cupos no superen la cantidad según el tiempo estimado por paciente.
Validar si el número de cupos excede al tiempo disponible de atención que genere un mensaje de error.

Ventana de Especialidad

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Especialidad
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
especialidad_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.


especialidad_des
carácter
SI
Este campo almacena la descripción de la especialidad del especialista.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular especialidades.
v_especialidad: visualización de las especialidades presionando el botón consultar
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.





Ventana de Consultorio

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: Consultorio
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nom
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_dir
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_tel
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consul_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios teléfonos. 
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los consultorios
v_consultorio: visualización de los consultorios presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.



Ventana de Ubicación

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: ubicación
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
ubicacion_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ciudad_cod
Clave foránea
SI
Almacena la clave foránea de la ciudad.
pais_cod
Clave foránea
SI
Almacena la clave foránea de país.
barrio_cod
Clave foránea
SI
Almacena la clave foránea de barrio.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las ciudades
v_ubicacion: visualización de las ciudades presionando el botón consultar
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.

Ventana de Dia

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Dia
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
dia_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
dia_des
carácter
SI
Este campo almacenara la descripción de los días de la semana.


Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los días
v_día: visualización de los días presionando el botón consultar
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.






Ventana de Turno

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Turno
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
turno_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.


turno_des
carácter
SI
Este campo almacenara la descripción de los turnos.


Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_turno: visualización de los turnos presionando el botón consultar
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.



Prototipos de Movimientos de Agendamiento
Ventana de Registrar Agenda Médica

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: Agenda Médica
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
agenda_med_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
agend_med_fecha
fecha
SI
Almacenará la fecha de fecha disponible del especialista.
especialidad_cod
Clave foránea
SI
Almacena la clave foránea de especialidad.
dia_cod
Clave foránea
SI
Almacena la clave foránea de día.
turno_cod
Clave foránea
SI
Almacena la clave foránea de turno.
NOMBRE DE LA TABLA: Especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
bloque_hora_cod
Clave foránea
SI
Almacena la clave foránea del bloque horario.


persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: Dia
dia_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
dia_des
carácter
SI
Este campo almacenara la descripción de los días de la semana.
NOMBRE DE LA TABLA: Especialidad
especialidad_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialidad_des
carácter
SI
Este campo almacenara la descripción de la especialidad del especialista.
NOMBRE DE LA TABLA: funcionario
funcionariol_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Turno
turno_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
turno_des
carácter
SI
Este campo almacenara la descripción de los turnos.
NOMBRE DE LA TABLA: Consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: bloque_horario_det
bloque_hora_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
disponibilidad_hora
time
SI
Este campo almacenara la disponibilidad del especialista.
hora_inicio
time
SI
En este campo se podrá guardar la hora inicial disponible del especialista.
hora_fin
time
SI
En este campo se podrá guardar la hora final disponible del especialista.
duracion
date
SI
En este campo se podrá guardar la duracion de cada turno.
cantidad_turnos
carácter
SI
Este campo permitirá almacenar la fecha disponible del especialista.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registro de la agenda
v_agenda_medica: visualización de los datos de la agenda presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no permita registrar fechas pasadas.
Validar que el valor de los cupos no sea mayor a la tabla disponibilidad horaria correspondiente.
Validar que no haya dos agendas para un mismo especialista, fecha, horario y especialidad.
Validar que no se registre la agenda si el especialista no tiene disponibilidad ese día.
Validar que el número de pacientes registrados no debe superar los cupos definidos.
Validar que no se ingresen caracteres especiales no permitidos.



Ventana de Gestionar Citas

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: cita_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
cita_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialidad_cod
Clave foránea
SI
Almacena la clave foránea de especialidad.
turno_cod
Clave foránea
SI
Almacena la clave foránea de turno.
dia_cod
Clave foránea
SI
Almacena la clave foránea de día.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


cita_fecha
fecha
SI
Almacenara la fecha de fecha de la cita.
cita_hora
hora
SI
Almacenara la hora de la cita agendada.
cita_estado
boolean
SI
Este campo almacenara si la cita está confirmada, cancelada, etc.
NOMBRE DE LA TABLA: cita_detalle
cita_motivo_consulta
carácter
SI
Este campo almacenara los motivos de consulta en la cita.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registro de la cita
v_cita: visualización de los datos de la cita presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que la fecha de la cita coincide con la agenda médica disponible del especialista.
Validar que el paciente no tenga dos citas activas el mismo día, especialista y hora.
Validar que el especialista tenga disponibilidad y agenda médica en esa fecha y horario.
Validar que no se solapase con otras citas ya agendadas par ese medio en ese horario.
Validar que el campo motivo consulta sea con caracteres necesario para registrar lo mas resaltantes.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Gestionar Avisos Recordatorio

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: aviso_recordatorio_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
aviso_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consultorio_cod
Clave foránea
SI
Clave primaria de consultorio que se representa en aviso recordatorio cabecera como clave foránea.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


recordatorio_fecha
time
SI
Almacenara la fecha para el aviso recordatorio.
aviso_fecha
date
SI
Almacenara la fecha para la cita en el aviso recordatorio.


aviso_hora
time
SI
Este campo almacenara si la cita está confirmada, cancelada, etc.
aviso_medio_envio
carácter
SI
En este campo se guardará los medios de envío del aviso.
NOMBRE DE LA TABLA: Consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
En este campo se almacenan los nombres los consultorios.
consul_direc
carácter
SI
En este campo se guardan las direcciones de los consultorios registrados.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono de los conusltorios, debería de analizar de almacenar línea baja y celular o varios teléfonos.
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


funcionario_cargo
carácter
SI
Este campo se almacenan los cargos de los funcionarios.
funcionario_fecha_ingreso
fecha
SI
Este campo registrara las fechas de ingresos de los funcionarios.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los avisos recordatorios.
v_aviso_recordatorio: visualización de los datos de los avisos presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Generar_aviso: Método que permita generar el mensaje de recordatorio para la cita.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar la fecha que coincida con la cita registrada.
Validar que el consultorio este asignado al especialista y a la cita del paciente.
Validar que la hora de avisos se genere antes de la hora de la cita registrada.
Validar que el funcionario no tenga múltiples avisos asignados al mismo tiempo.
Validar que el formato de envío sea solo(Gmail, SMS, WhatsApp) y que cada campo contenga con información necesaria del paciente.
Validar que el mensaje del aviso tenga mínimo de caracteres y evitar campos vacíos.



Ventana de Registrar Ficha Médica

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA:ficha_medica_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
ficha_med_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
diagnostico_cod
Clave foránea
SI
Clave primaria de diagnóstico que se representa en ficha médica cabecera como clave foránea.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


consulta_cod
Clave foránea
SI
Almacena la clave foránea de consulta.


historial_clinico
Clave foránea
SI
Almacena la clave foránea de historial clínico.


tratamiento_cod
Clave foránea
SI
Almacena la clave foránea de tratamiento.


recetas_medicas_cod
Clave foránea
SI
Almacena la clave foránea de recetas médicas.


síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.


ficha_medica_observación
carácter
SI
En este campo se almacenan las observaciones del especialista al paciente.
ficha_med_fech_registro
fecha
SI
En este campo se almacenan las fechas de registro de la ficha del paciente.
ficha_med_estado
carácter
SI
En este campo se almacenan el estado de la ficha médica.
ficha_med_ci_paciente
carácter
SI
Este campo almacena la cédula del paciente.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
bloque_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.


NOMBRE DE LA TABLA: Diagnóstico
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de la ficha médica.


síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.


tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.


diagnostico_des
Caracter
SI
Este campo almacenara la descripción del diagnóstico.


historial_clinico_cod
Clave foránea
SI
Almacena la clave foránea de historial clínico
tratamiento_cod
Clave foránea
SI
Almacena la clave foránea de tratamiento.
consulta_cod
Clave foránea
SI
Almacena la clave foránea de consulta.
receta_medica_cod
Clave foránea
SI
Almacena la clave foránea de receta médica.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: Sintomas
sintomas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
síntomas_des
carácter
SI
Este campo almacenara los síntomas del paciente.
NOMBRE DE LA TABLA: Tratamientos
tratamientos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


tratamiento_des
carácter
SI
Este campo almacena la descripción de los tratamientos. 


historial_clinico_cod
Clave foránea
SI
Almacena la clave foránea de historial clínico.
tip_proced_med_cod
Clave foránea
SI
Almacena la clave foránea de tipo procedimiento médico.
insumo_utilizado_cod
Clave foránea
SI
Almacena la clave foránea de insumos utilizados.
NOMBRE DE LA TABLA: recetas médicas
recetas_medicas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


recetas_med_dosis
carácter
SI
Este campo almacena las dosis del medicamento.
recetas_med_duracion
carácter
SI
Este campo almacena la duración de la receta.
recetas_med_fecha
Carácter 
SI
Este campo almacena la fecha realizada de la receta.
medicamentos_cod
numérico
SI
Clave primaria






Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las fichas médicas.
v_cita: visualización de los datos de las fichas presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se duplique la misma ficha sin justificación
Validar que exista al menos un síntomas en la misma ficha.
Validar que los medicamentos y tratamientos coincida en la fecha y la receta.
Validar que los medicamentos existan en la tabla medicamentos.
Validar que el medicamento este relacionado con la receta.
Validar que el campo motivo de consulta se permita cargar contenido coherente y mínimo de características.
Validar que no se ingresen caracteres especiales no permitidos.


Módulo de consultorio
Prototipos de Referenciales de consultorio
Ventana de Tipo Diagnóstico

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Tipo_diagnostico
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tipo_diagn_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_diagn_des
carácter
SI
Este campo almacenara la descripción de los tipo diagnósticos.
diagn_des
carácter
SI
Este campo almacenara la descripción de los diagnósticos.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_diagnóstico: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.



Ventana de Síntomas

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: sintomas_det
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
sintomas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
sintomas_des
carácter
SI
Este campo almacenara la descripción de los turnos.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_sintomas: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Tipo Análisis

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Analisis_det
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
analisis_tipo_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
analisis_tipo_des
carácter
SI
Este campo almacenara la descripción de los turnos.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_tipo_analisis: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Tipo  Estudio

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: tipo_estudio
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tipo_estudio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.


tipo_estudio_des
carácter
SI
Este campo almacenara la descripción de los turnos.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_tipo_estudio: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Medicamento

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Medicamentos
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
medicamentos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
medicamento_nombre
carácter
SI
Este campo almacenara el nombre de los medicamentos.
medicamento_formula
carácter
SI
Este campo almacenara la formula de los medicamentos.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_medicamentos: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Tipo Procedimiento Médico

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: tipo_insumo_utilizado
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tipo_insu_uti_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
proced_med_cod
Clave foránea
SI
Este campo es la clave foránea de esta entidad por la misma será generada de manera automática.
insu_utili_des
carácter
SI
SI
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_tipo_insumo_utilizado: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.
Validar que no se ingresen caracteres especiales no permitidos.


Prototipos de Movimientos de Consultorio
Ventana de Registrar Consulta

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA:consulta_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
consulta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
diagnostico_cod
Clave foránea
SI
Clave primaria de diagnóstico que se representa en ficha medica cabecera como clave foránea.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
historial_clinico
Clave foránea
SI
Almacena la clave foránea de historial clínico.
tratamiento_cod
Clave foránea
SI
Almacena la clave foránea de tratamiento.
recetas_medicas_cod
Clave foránea
SI
Almacena la clave foránea de recetas médicas.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
especialista_cod
Clave foránea
SI
Almacena la clave foránea de especialista.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.
consulta_fecha
fecha
SI
En este campo se almacenan las fechas de registro de la consulta.
consulta_estado
boolean
SI
Este campo almacenara si la agenda está finalizada, en seguimiento, pagado, etc.
consulta_hora
hora
SI
Este campo almacenara la hora de la consulta.
NOMBRE DE LA TABLA:consulta_detalle
consulta_cod
Clave foránea
SI
Almacena la clave foránea de consulta.
tratamiento_cod
Clave foránea
SI
Almacena la clave foránea de tratamiento.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: especialsita
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
NOMBRE DE LA TABLA: Diagnóstico
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de la ficha médica.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.
diagnostico_des
Carácter
SI
Este campo almacenara la descripción del diagnóstico.
historial_clinico_cod
numérico
SI
Clave primaria
tratamiento_cod
numérico
SI
Clave primaria
consulta_cod
numérico
SI
Clave primaria
receta_medica_cod
numérico
SI
Clave primaria
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Sintomas
sintomas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
síntomas_des
carácter
SI
Este campo almacenara los síntomas del paciente.
NOMBRE DE LA TABLA: Tratamientos
tratamientos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


tratamiento_des
carácter
SI
Este campo almacena la descripción de los tratamientos. 


historial_clinico_cod
numérico
SI
Clave primaria
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: procedimiento_medico
tipo_proced_med
Clave foránea
SI
Almacena la clave foránea de tipo de procedimiento especialista.
insumo_utilizado_cod
Clave foránea
SI
Almacena la clave foránea de insumos utilizados.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
disp_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
proced_med_des
carácter


SI
Este campo almacena la descripción del procedimiento.
proced_med_nombre
carácter


SI
Este campo almacena el nombre del procedimiento.
proced_med_duracion
carácter


SI
Este campo almacena la duración de los procedimientos.
proced_med_fecha
fecha


SI
Este campo almacena las fechas que se realizara o se realizó el procedimiento.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registros de las consultas.
v_registrar_consulta: visualización de los datos de las consultas presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se duplique la misma ficha sin justificación.
Validar que exista al menos un síntoma en la misma consulta.
Validar que los medicamentos y tratamientos coincida en la fecha.
Validar que los medicamentos existan en la tabla medicamentos
Validar no registrar consultar futuras (una consulta no se puede registrar antes de ocurrir).
Validar que deben coincidir con la agenda médica previa.
Registrar automáticamente el usuario que completa la ficha de consulta.
Validar y verificar que el especialista haya atendido esa cita.
Validar que el especialista esté habilitado para realizar el procedimiento decidido.



Ventana de Gestionar Diagnóstico

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: Diagnóstico
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.
diagnostico_des
Caracter
SI
Este campo almacenara la descripción del diagnóstico.
historial_clinico_cod
numérico
SI
Clave primaria
tratamiento_cod
numérico
SI
Clave primaria
consulta_cod
numérico
SI
Clave primaria
receta_medica_cod
numérico
SI
Clave primaria
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.
NOMBRE DE LA TABLA: tipo_diagnostico
tipo_diag_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_diag_des
numérico
SI
Este campo almacenara el tipo de diagnóstico.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: Médico
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Sintomas
sintomas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
síntomas_des
carácter
SI
Este campo almacenara los síntomas del paciente.
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registros de los diagnósticos.
v_reg_diagnóstico: visualización de los datos de los diagnósticos presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que exista al menos un síntoma en la misma consulta.
Validar que el especialista debe estar activo y habilitado para registrar diagnósticos.
Validar que el consultorio debe corresponder al espacio donde se realizó la atención clínica.
Validar y verificar que el paciente haya tenido una cita médica en esa fecha.
Validar que estén definidos en la tabla de diagnóstico y vinculados a un tipo de diagnóstico.
Validar que no se ingresen caracteres especiales no permitidos.



Ventana de Gestionar Procedimiento Médico

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Insumos_utilizados
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
insumo_utilizado_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_proced_med_cod
Clave foránea
SI
Almacena la clave foránea de tipos de procedimientos.
Insu_utili_des
carácter


SI
Este campo almacena la descripción de los insumos utilizados.
NOMBRE DE LA TABLA: procedimiento_medico
tipo_proced_med
Clave foránea
SI
Almacena la clave foránea de tipo de procedimiento médico.
insumo_utilizado_cod
Clave foránea
SI
Almacena la clave foránea de insumos utilizados.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
disp_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
proced_med_des
carácter


SI
Este campo almacena la descripción del procedimiento.
proced_med_nombre
carácter


SI
Este campo almacena el nombre del procedimiento.
proced_med_duracion
carácter


SI
Este campo almacena la duración de los procedimientos.
proced_med_fecha
fecha


SI
Este campo almacena las fechas que se realizará o se realizó el procedimiento.
NOMBRE DE LA TABLA: tipo_proced_medico
tipo_estudio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_proced_med_des
carácter
SI
Este campo almacenara la descripción de los tipos de procedimientos.
tipo_proced_med_nombre
carácter
SI
Este campo almacenara el nombre del procedimiento.
tipo_proced_med_duracion
carácter
SI
Este campo almacenara la duración del procedimiento.
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.


consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente


consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.


consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 



Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registros de los insumos utilizados.
v_gestionar_insumos_utilizado: visualización de los datos de los insumos utilizados presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar el registro a usuarios con rol de especialista o funcionario autorizado.
Validar que exista y esté activo en la tabla de procedimientos médicos
Validar que cada insumo esté cargado en la tabla de insumos y tenga stock disponible.
Validar que no se haya registrado el mismo insumo en la misma fecha y procedimiento por error.
Validar consumo de stock al cargar los insumos utilizados.
Validar no exceder duración habitual para el procedimiento.
Validar que no se ingresen caracteres especiales no permitidos.


Ventana de Generar Orden Estudios

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: Orden_estudio_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
orden_estudio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
Orden_estudio_fecha_orden
fecha
SI
Este campo almacenara las fechas de emisión de las órdenes.
tipo_estudio_cod
Clave foránea
SI
Almacena la clave foránea de tipo estudio.
tipo_analisis_estado
boolean
SI
Este campo almacenara si la orden esta en estado de espera de resultados, cancelada, etc.
NOMBRE DE LA TABLA: orden_estudio_detalle
orden_estudio_cod
Clave foránea
SI
Almacena la clave foránea de orden estudio.
orden_estudio_indicaciones
carácter
SI
En este campo se almacenan las indicaciones de las ordenes de estudios.
orden_estudio_motivo
carácter
SI
Este campo almacena los motivos para las ordenes de estudios.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente.
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: tipo_estudio
tipo_estudio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_estudio_des
carácter
SI
Este campo almacena los tipos de estudios.



Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las órdenes de estudios.
v_generar_orden_estudio: visualización de los datos de las órdenes de estudios presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Generar orden():Método que genera e imprime una orden clínica o administrativa para el paciente.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que exista en la tabla tipo de estudios y esté habilitado.
Validar que el campo indicaciones no esté vacío ni tenga solo caracteres especiales.
Validar que el campo motivo de orden tenga texto coherente y sin repeticiones automáticas
Validar que se eviten duplicados en un mismo día para el mismo paciente y tipo de estudio.
Validar que el consultorio esté habilitado para emitir órdenes.

Ventana de Generar Orden Análisis

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Orden_analisis_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
orden_analisis_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
Orden_analisis_fecha
fecha
SI
Este campo almacenara las fechas de emisión de las ordenes de análisis.
tipo_analisis_cod
Clave foránea
SI
Almacena la clave foránea de tipo de análisis.
orden_analisis_estado
boolean
SI
Este campo almacenara si la orden esta en estado de espera de resultados, cancelada, etc.
NOMBRE DE LA TABLA: orden_analisis_detalle
orden_analisis_cod
Clave foránea
SI
Almacena la clave foránea de orden estudio.
orden_analisis_des
carácter
SI
En este campo se almacenan las indicaciones de las ordenes de análisis.
orden_analisis_indic_medica
carácter
SI
Este campo almacena las indicaciones de la orden.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
bloque_hora_cod
Clave foránea
SI
Almacena la clave foránea de bloque horario.


NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: tipo_analisis
tipo_analisis_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_analisis_des
carácter
SI
Este campo almacena los tipos de análisis.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las ordenes de análisis.
v_generar_orden_analisis: visualización de los datos de las ordenes de análisis presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Generar orden():Método que genera e imprime una orden clínica o administrativa para el paciente.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que exista en la tabla tipo de análisis y esté habilitado.
Validar que el campo indicaciones no esté vacío ni tenga solo caracteres especiales.
Validar que el campo de indicaciones tenga texto coherente y sin repeticiones automática
Validar que se eviten duplicados en un mismo día para el mismo paciente y tipo de análisis.
Validar que el consultorio este habilitado para emitir órdenes de análisis.

Ventana de Registrar Recetas e Indicaciones

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Recetas_medicas
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
recetas_medicas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de personas.
recetas_med_dosis
carácter
SI
Este campo almacenara las dosis de medicamentos en la receta.
receta_med_fecha
fecha
SI
Este campo almacenara las fechas de las recetas emitidas.
medicamentos_cod
numérico
SI
Clave primaria
NOMBRE DE LA TABLA: Medicamentos
medicamentos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
medicamentos_nombre
carácter
SI
Este campo almacenara el nombre de los medicamentos.
medicamentos_formula
carácter
SI
Este campo almacena las fórmulas de cada medicamento.
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
bloque_horario
Clave foránea
SI
Almacena la clave foránea del bloque horario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
NOMBRE DE LA TABLA: Consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registros de las recetas e indicaciones.
v_gestionar_recetas_indicaciones: visualización de los datos de las recetas presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el consultorio esté habilitado para emisión de recetas.
Validar evitar duplicidad de recetas idénticas en un mismo día.
Validar que el campo de recetas incluya nombres claros y adecuados (sin solo símbolos, campos vacíos o incoherencias).
Validar que se detalle claramente dosis por medicamento.
Validar que la fecha de emisión no puede ser anterior a la última consulta médica o visita registrada.



Ventana de Registrar Tratamiento

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Tratamientos
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tratamientos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
tratamiento_des
carácter
SI
Este campo almacena la descripción de los tratamientos. 
historial_clinico_cod
numérico
SI
Clave primaria
tip_proced_med_cod
numérico
SI
Clave primaria
insumo_utilizado_cod
numérico
SI
Clave primaria
NOMBRE DE LA TABLA: Diagnósticos
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.
diagnostico_des
Caracter
SI
Este campo almacenara la descripción del diagnóstico.
historial_clinico_cod
numérico
SI
Clave primaria
tratamiento_cod
numérico
SI
Clave primaria
consulta_cod
numérico
SI
Clave primaria
receta_medica_cod
numérico
SI
Clave primaria
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Insumo_utilizado
insumo_utilizado_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_proced_med
Clave foránea
SI
Almacena la clave foránea de tipo procedimiento médico.
insu_util_des
carácter
SI
Este campo almacenara la descripción de los insumos utilizados.
NOMBRE DE LA TABLA: tipo_diagnostico
tipo_diag_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_diag_des
carácter
SI
Este campo almacenara los tipos de diagnósticos.
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.



NOMBRE DE LA TABLA: Consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 




Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los registros de los tratamientos.
v_gestionar_tratamientos: visualización de los datos de los tratamientos presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el funcionario tenga permisos de ingreso/registro de datos.
Validar que exista en la tabla tipo diagnóstico.
Validar que los insumos existan en el inventario y tengan stock disponible.
Validar que no se repita insumo innecesariamente.
Validar que la fecha de registro no puede ser futura ni anterior a la fecha de diagnóstico relacionado
Verificar que el paciente no tenga otro tratamiento igual activo.
Validar que el tratamiento sea coherente con el diagnóstico.






Ventana de Generar Ficha Médica

Diagrama entidad relación




Descripción de los campos
NOMBRE DE LA TABLA: ficha_medica_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
ficha_med_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
diagnostico_cod
Clave foránea
SI
Clave primaria de diagnóstico que se representa en ficha medica cabecera como clave foránea.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consulta_cod
Clave foránea
SI
Almacena la clave foránea de consulta.
historial_clinico
Clave foránea
SI
Almacena la clave foránea de historial clínico.
tratamiento_cod
Clave foránea
SI
Almacena la clave foránea de tratamiento.
recetas_medicas_cod
Clave foránea
SI
Almacena la clave foránea de recetas médicas.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
ficha_medica_observación
carácter
SI
En este campo se almacenan las observaciones del especialista al paciente.
ficha_med_alergias
carácter
SI
En este campo se almacenan las alergias del paciente.
ficha_med_fech_registro
fecha
SI
En este campo se almacenan las fechas de registro de la ficha del paciente.
ficha_med_estado
carácter
SI
En este campo se almacenan el estado de la ficha médica.
ficha_med_ci_paciente
carácter
SI
Este campo almacenara la cédula del paciente.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
NOMBRE DE LA TABLA: Historial_clinico
historial_clinico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_proced_med_cod
Clave foránea
SI
Almacena la clave foránea de tipo procedimiento.
insumo_utilizado_cod
Clave foránea
SI
Almacena la clave foránea de insumos utilizados.
tratamientos_cod
Clave foránea
SI
Almacena la clave foránea de tratamientos.
historial_clinico_des
Carácter
SI
Este campo almacenara la descripción del historial.
historial_clinico_fecha
fecha
SI
Este campo almacenara la fecha del historial.
historial_clinico_estado
Boolean
SI
Este campo almacenara si el historial está finalizado, en seguimiento, etc.
NOMBRE DE LA TABLA: Diagnóstico
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.
diagnostico_des
Carácter
SI
Este campo almacenara la descripción del diagnóstico.
historial_clinico_cod
numérico
SI
Clave primaria
tratamiento_cod
numérico
SI
Clave primaria
consulta_cod
numérico
SI
Clave primaria
receta_medica_cod
numérico
SI
Clave primaria
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Tipo_diagnostico
tipo_diag_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_diag_des
numérico
SI
Este campo almacenara el tipo de diagnóstico.
NOMBRE DE LA TABLA: Insumos_utilizados
insumo_utilizado_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_proced_med
Clave foránea
SI
Almacena la clave foránea de tipo procedimiento médico.
insu_util_des
carácter
SI
Este campo almacenara la descripción de los insumos utilizados.
NOMBRE DE LA TABLA: Sintomas
sintomas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
síntomas_des
carácter
SI
Este campo almacenara los síntomas del paciente.
NOMBRE DE LA TABLA: Tratamientos
tratamientos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
tratamiento_des
carácter
SI
Este campo almacena la descripción de los tratamientos. 
historial_clinico_cod
numérico
SI
Clave primaria
tip_proced_med_cod
numérico
SI
Clave primaria
insumo_utilizado_cod
numérico
SI
Clave primaria
NOMBRE DE LA TABLA: recetas_medicas
recetas_medicas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
recetas_med_dosis
carácter
SI
Este campo almacena las dosis del medicamento.
recetas_med_duracion
carácter
SI
Este campo almacena la duración de la receta.
recetas_med_fecha
Carácter 
SI
Este campo almacena la fecha realizada de la receta.
medicamentos_cod
numérico
SI
Clave primaria




Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las fichas médicas.
v_generar_ficha_medica: visualización de los datos de las fichas presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Generar Ficha(): Método que genera e imprime la ficha para el paciente.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no se duplique la misma ficha sin justificación
Validar que exista al menos un síntoma en la misma ficha.
Validar que los medicamentos y tratamientos coincida en la fecha y la receta.
Validar que los medicamentos existan en la tabla medicamentos.
Validar que el medicamento esté relacionado con la receta.
Validar que el campo motivo de consulta se permita cargar contenido coherente y mínimo de características.




Ventana de Generar Justificativo Médico

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: justificativo_medico_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
justif_med_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consulta_cod
Clave foránea
SI
Almacena la clave foránea de consulta.
historial_clinico_cod
Clave foránea
SI
Almacena la clave foránea de historial clínico.
diagnostico_cod
Clave foránea
SI
Almacena la clave foránea de diagnóstico.
tratamientos_cod
Clave foránea
SI
Almacena la clave foránea de tratamientos.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
recetas_medicas_cod
Clave foránea
SI
Almacena la clave foránea de recetas médicas.
síntomas_cod
Clave foránea
SI
Almacena la clave foránea de persona.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
justif_med_fecha_emision
Carácter 
SI
Este campo almacenara las fechas de emisión del justificativo.
justif_med_estado
caracter
SI


NOMBRE DE LA TABLA: justificativo_medico_detall
justif_med_cod
Clave foránea
SI
Almacena la clave foránea de justificativo medico cabecera.
tratamientos_cod
Clave foránea
SI
Almacena la clave foránea de tratamientos.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
justif_med_motivo
carácter
SI
Este campo se almacena los motivos de la justificación.
justif_med_recomendaciones
carácter
SI
Este campo almacenara las recomendaciones del justificativo.
justif_med_dias_reposo
carácter
SI
Este campo almacenará los días de reposo que tendrá el paciente.
NOMBRE DE LA TABLA: Paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: especialista
especialista_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
especialista_num_registro
carácter
SI
Este campo almacenara el número de registro del especialista.
dip_hora_cod
Clave foránea
SI
Almacena la clave foránea de disponibilidad horaria.
NOMBRE DE LA TABLA: Diagnóstico
diagnostico_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ficha_med_cod
Clave foránea
SI
Almacena la clave foránea de ficha médica.


síntomas_cod
Clave foránea
SI
Almacena la clave foránea de síntomas.
tipo_diag_cod
Clave foránea
SI
Almacena la clave foránea de tipo diagnósticos.
diagnostico_des
Carácter
SI
Este campo almacenara la descripción del diagnóstico.
historial_clinico_cod
numérico
SI
Clave primaria
tratamiento_cod
numérico
SI
Clave primaria
consulta_cod
numérico
SI
Clave primaria
receta_medica_cod
numérico
SI
Clave primaria
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los justificativos médicos.
v_generar_justif_medico: visualización de los datos de los justificativos presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Generar Justificativo(): Método que genera e imprime el justificativo para el paciente.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que la fecha debe estar relacionada con una fecha próxima a la atención médica (misma semana o día).
Validar que el diagnostico sea coherente con la necesidad de reposo o justificación
Validar que el campo motivo sea resumida y acuerdo para el justificativo.
Validar que el paciente haya tenido una consulta médica registrada con ese especialista antes de emitir el justificativo.
Validar que solo especialistas puedan emitir este documento.
Validar el Máximo sugerido de días: 30 (se puede limitar según el protocolo clínico).






Módulo de Ventas
Prototipos de Referenciales de ventas
Ventana de Forma de cobro

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Forma_cobro
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
forma_cobro_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
forma_cobro_desc
carácter
SI
Este campo almacenara la descripción de la forma de cobro.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_forma_cobro: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Ventana de Marca Tarjeta

Diagrama entidad relación
 
Descripción de los campos

NOMBRE DE LA TABLA: Marca_Tarjeta
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
marca_tarjeta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
marca_tarjeta_des
carácter
SI
Este campo almacenara la descripción de las marca tarjeta.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_marca_tarjeta: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Ventana de Entidad Emisora

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: Entidad_emisora
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
entidad_emisora_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_nombre
carácter
SI
Este campo almacenara los nombres de las entidades emisoras.
entidad_nombre_direccion
carácter
SI
Este campo almacenara las direcciones de las entidades.
entidad_emisora_telef
carácter
SI
Este campo almacenara los teléfonos de las entidades.
entidad_emisora_email
carácter
SI
Este campo almacenara los correos de las entidades.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las entidades emisoras.
v_entidad_emisora: visualización de las entidades emisoras presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el nombre de la entidad tenga caracteres inválidos o solo símbolos.
Validar duplicidad con otras entidades ya registradas con mismo nombre y dirección.
Validar no permitir correos inválidos o vacíos si se completa el campo.





Ventana de Entidad Adherida

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Entidad_adherida
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
entidad_adherida_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_cod
Clave foránea
SI
Almacena la clave foránea de entidad emisora.
marc_tarj_cod
Clave foránea
SI
Almacena la clave foránea de marca tarjeta.
entidad_adherida_nombre
carácter
SI
Este campo almacenara los nombres de las entidades.
entidad_adherida_direccion
carácter
SI
Este campo almacenara las direcciones de las entidades.
entidad_adherida_telf
carácter
SI
Este campo almacenara los teléfonos de las entidades.
entidad_adherida_correo
carácter
SI
Este campo almacenara los correos de las entidades.


NOMBRE DE LA TABLA: Entidad_emisora
entidad_emisora_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_nombre
carácter
SI
Este campo almacenara los nombres de las entidades emisoras.
entidad_nombre_direccion
carácter
SI
Este campo almacenara las direcciones de las entidades.
entidad_emisora_telef
carácter
SI
Este campo almacenara los teléfonos de las entidades.
entidad_emisora_email
carácter
SI
Este campo almacenara los correos de las entidades.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las entidades adheridas.
v_entidad_adherida: visualización de las entidades adheridas presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar el nombre de la entidad tenga caracteres inválidos o solo símbolos.
Validar duplicidad con otras entidades ya registradas con mismo nombre y dirección.
Validar no permitir correos inválidos o vacíos si se completa el campo.
Validar que el valor pertenezca a una lista de opciones válidas:
Ej: Visa, MasterCard, American Express, Cabal, Otros.



Ventana de Caja

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA:  caja
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
caja_des
carácter
SI
Este campo almacenara la descripción de las caja.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_caja: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Ventana de Tipo items

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA:  Tipo items
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tipo_item_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_items_des
carácter
SI
Este campo almacenara la descripción de los tipos de items.


Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_tipo_items: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Ventana de Depósito


Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA:  depósito
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
deposito_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
deposito_des
carácter
SI
Este campo almacenara la descripción de los depósitos.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_deposito: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Ventana de Tipo Impuesto

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: tipo impuesto
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
tipo_impuesto_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
venta_cod
numerico
SI
Almacena la clave foránea de venta.
iva_5
decimal
SI
Este campo almacenara el iva del 5% en tipo impuesto.
iva_10
decimal
SI
Este campo almacenara el iva del 10% en tipo impuesto.
exentas
numerico
Si
Este campo almacenara las exentas en tipo impuesto.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los turnos
v_tipo_impuesto: visualización de los turnos presionando el botón consultar
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permite limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se este escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se graben los datos de acuerdo al tipo de dato definido.


Prototipos de Movimientos de Ventas
Ventana de Registrar Pedido Cliente

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: Pedido_venta_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
pedido_venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
items_cod
Clave foránea
SI
Almacena la clave foránea de ítems.
stok_cod
Clave foránea
SI
Almacena la clave foránea de stock.
Depos_cod
Clave foránea
SI
Almacena la clave foránea de depósito.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
pedido_venta_fecha
fecha
SI
Este campo almacenara la fecha del pedido.
pedido_venta_estado
Boolean
SI
Este campo almacenara el estado del pedido.
tipo_impuesto_cod
numérico
SI
Clave primaria.



NOMBRE DE LA TABLA: pedido_venta_det
pedido_venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
items_cod
Clave foránea
SI
Almacena la clave foránea de persona.
ped_vent_tipo_pedido
carácter
SI
Este campo almacena el tipo de pedido.
ped_vent_pedido_des
carácter
SI
Este campo almacenara la descripción del tipo de pedido
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 


consul_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: tipo_items 
tipo_item_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_items_des
carácter
SI
Este campo almacenara la descripción de los ítems.
NOMBRE DE LA TABLA: tipo_impuestos
tipo_impuesto_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_impuetos
carácter
SI
Este campo almacenara la descripción del tipo impuestos.
NOMBRE DE LA TABLA: deposito
Depos_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de persona.
Depos_des
carácter
SI
Este campo almacenara la descripción del depósito.
persona_cod
numérico
SI
Almacena la clave primaria de persona.


NOMBRE DE LA TABLA: items
items_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
items_ins_cuestinario
carácter
SI
Este campo almacenara la descripción de los insumos varios.
items_servicios_psico
carácter
SI
Este campo almacenara la descripción de los servicios psicologicos.
tipo_item_cod
numérico
SI
Almacena la clave primaria de tipo ítems.
NOMBRE DE LA TABLA: stock
stok_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
Depos_cod
Clave foránea
SI
Almacena la clave foránea de depósito.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
items_cod
Clave foránea
SI
Almacena la clave foránea de ítems.
stock_cantidad
numérico
SI
Almacena las cantidades de productos en stock.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los pedidos de clientes.
v_registrar_pedido_cliente: visualización de los pedidos de clientes presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el funcionario esté habilitado para registrar pedidos.
Validar coherencia con el tipo de ítems.
Validar que no sea una fecha futura o anterior.
Validar restar stock solo al momento de marcar el pedido como entregado.
Validar que cada ítem exista, esté activo y tenga tipo asignado.
Validar que exista stock suficiente antes de confirmar el pedido.
Validar el depósito debe estar activo y vinculado al consultorio.



Ventana de Gestionar Ventas y Generar Cuentas a Cobrar

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: venta_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ven_cab_num_factura
numérico
SI
Este campo almacenara el numero de la factura.
vent_cab_costo
numérico
SI
Este campo almacenara el precio para cobrar.
vent_cab_tipo_factura
carácter
SI
Este campo almacenara el tipo de factura.
vent_cab_interv_fech_venc
fecha
SI
Este campo almacenara la fecha de vencimiento de cuentas a cobrar.
consultorio_cod
numérico
SI
Clave primaria.
persona_cod
numérico
SI
Clave primaria.
NOMBRE DE LA TABLA: venta_det
venta_cod
Clave foránea
SI
Almacena la clave foránea de venta.
stok_cod
Clave foránea
SI
Almacena la clave foránea de stock.
vent_det_servicio_des
carácter
SI
Este campo almacena el servicio a cobrar.
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consult_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: Libro_ventas
libro_ventas_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
venta_cod
Clave foránea
SI
Almacena la clave foránea de venta.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
iva_5
numérico
SI
Almacenará el iva 5%
excentas
numérico
SI
Almacenará  las exentas
iva_10
numérico
SI
Almacenará el iva 10% 
NOMBRE DE LA TABLA: Cuentas_cobrar
cuenta_cobrar_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
venta_cod
Clave foránea
SI
Almacena la clave foránea de venta.
cuent_cob_num_cuenta
numérico
SI
Este campo almacena el número de cuenta.
cuent_cob_monto
numérico
SI
Este campo almacena el monto de cuenta a cobrar.
cuent_cob_saldo
numérico
SI
Este campo almacena el saldo.
cuent_cob_estado
Boolean
SI
Este campo almacena el estado de la cuenta a cobrar.
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las cuentas a cobrar.
v_generar_cuentasta_cobrar: visualización de las cuentas a cobrar presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que el funcionario esté habilitado para generar las cuentas.
Validar que no sea una fecha futura o anterior.
Validar la fecha de vencimiento si el tipo de factura o forma de pago es a crédito.
Validar el monto a pagada solo si existe comprobante o registro de cobro vinculado.
Validar cambio a vencida automático si la fecha de vencimiento pasa y sigue pendiente.
Validar relacionar con la tabla forma de cobro (validar que exista).
Validar coherencia con el servicio prestado (puede venir de procedimientos, tratamientos, etc.).



Ventana de Registrar Apertura y cierre de caja

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: apertura_cierre_caja
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
apert_cier_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
caja_cod
Clave foránea
SI
Almacena la clave foránea de caja.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apertura_fecha
fecha
SI
Este campo almacena la fecha de apertura.
apertura_monto
numérico
SI
Este campo almacena el monto de apertura.
apertura_cierre
numérico
SI
Este campo almacena el monto cierre.
fecha_cierre
fecha
SI
Este campo almacena la feche de cierre.
apert_cier_caj_estado
boolean
SI
Este campo almacena el estado de la apertura y cierre de caja.



NOMBRE DE LA TABLA: cobro_cab
cobro_cod
Clave foránea
SI
Almacena la clave foránea de caja.
cuenta_cobrar_cod
Clave foránea
SI
Almacena la clave foránea de persona.
venta_cod
Clave foránea
SI
Almacena la clave foránea de persona.
forma_cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apert_cier_caja_cod
numérico
SI
Clave primaria.
caja_cod
numérico
SI
Clave primaria.
consultorio_cod
numérico
SI
Clave primaria.
cobro_cab_cobro_fecha
fecha
SI
Este campo almacena la fecha de cobro.
cobro_estado
boolean
SI
Este campo almacena el estado de cobro.
NOMBRE DE LA TABLA: cobro_det
cobro_cod
Clave foránea
SI
Almacena la clave foránea de cobro.
cobro_monto
numérico
SI
Almacena el monto del cobro.



NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consul_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios correos. 
NOMBRE DE LA TABLA: Recaudaciones_depositar
recaud_depositar_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
apert_cier_caja_cod
Clave foránea
SI
Almacena la clave foránea de apertura cierre de caja.
caja_cod
Clave foránea
SI
Almacena la clave foránea de caja.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
Recau_monto_efectivo
numérico
SI
Este campo almacena el monto con pago en efectivo.
Recau_monto_cheque
numérico
SI
Este campo almacena el monto con pago en cheque.
NOMBRE DE LA TABLA: arqueo_caja
arqueo_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
apert_cier_caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de persona.
arq_monto_efectivo
numérico
SI
Almacena el monto en pagos con efectivo.
arq_monto_cheque
numérico
SI
Almacena el monto en pagos con cheque.
arq_monto_tarj
numérico
SI
Almacena el monto con pagos en tarjeta.
NOMBRE DE LA TABLA: Formo_cobro
forma_cobro_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
forma_cobro_des
carácter
SI
Este campo almacena la descripción de forma de cobro.
NOMBRE DE LA TABLA: caja
caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de persona.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
caja_fecha
Fecha
SI
Almacena la fecha de registro de fecha de la caja.
caja_n°
numérico
SI
Almacena el número de caja que será registrado.
NOMBRE DE LA TABLA: cobro_cheque
cobro_cheque_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_cod
Clave foránea
SI
Almacena la clave foránea de persona.
cobro_cod
numérico
SI
Clave primaria.
cobro_cheque_monto
numérico
SI
Este campo almacena el monto pagado con cheques.
cobro_cheque_fecha_venc
fecha
SI
Este campo almacena la fecha vencida del cheque.
cobro_cheque_numero
numérico
SI
Este campo almacena el número de cheque.
NOMBRE DE LA TABLA: cobro_tarjeta
cobro_tarj_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
entidad_adherida_cod
numérico
SI
Clave primaria.
entidad_emisora_cod
numérico
SI
Clave primaria.
cobro_tarj_monto
numérico
SI
Este campo almacena el monto pagado con tarjeta.
cobro_tarj_numero
numérico
SI
Este campo almacena el número de la tarjeta
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las aperturas y cierres de cajas.
v_apertura_cierre_caja: visualización de las aperturas y cierres de cajas presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no sea una fecha futura o anterior.
Validar existir una apertura por día por consultorio/funcionario activo.
Validar que se pueda actualizar automáticamente a partir de ingresos registrados (pagos, cobros, etc.).
Validar que el estado del formulario cierre automático puede estar disponible al final del día.
Validar mostrar advertencia si la diferencia supera un margen aceptable.
Validar si el estado es "cerrada", impedir edición posterior (solo lectura).






Ventana de Gestionar Forma de cobro
	
Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: apertura_cierre_caja
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
apert_cier_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
caja_cod
Clave foránea
SI
Almacena la clave foránea de caja.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apertura_fecha
fecha
SI
Este campo almacena la fecha de apertura.
apertura_monto
numérico
SI
Este campo almacena el monto de apertura.
apertura_cierre
numérico
SI
Este campo almacena el monto cierre.
fecha_cierre
fecha
SI
Este campo almacena la feche de cierre.
apert_cier_caj_estado
boolean
SI
Este campo almacena el estado de la apertura y cierre de caja.



NOMBRE DE LA TABLA: cobro_cab
cobro_cod
Clave foránea
SI
Almacena la clave foránea de caja.
cuenta_cobrar_cod
Clave foránea
SI
Almacena la clave foránea de persona.
venta_cod
Clave foránea
SI
Almacena la clave foránea de persona.
forma_cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apert_cier_caja_cod
numérico
SI
Clave primaria.
caja_cod
numérico
SI
Clave primaria.
consultorio_cod
numérico
SI
Clave primaria.
cobro_cab_cobro_fecha
fecha
SI
Este campo almacena la fecha de cobro.
cobro_estado
boolean
SI
Este campo almacena el estado de cobro.
NOMBRE DE LA TABLA: cobro_det
cobro_cod
Clave foránea
SI
Almacena la clave foránea de cobro.


cobro_monto
numérico
SI
Almacena el monto del cobro.


NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consultorio_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consul_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios correos. 
NOMBRE DE LA TABLA: Entidad_emisora
entidad_emisora_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_nombre
carácter
SI
Este campo almacenara los nombres de las entidades emisoras.
entidad_nombre_direccion
carácter
SI
Este campo almacenara las direcciones de las entidades.
entidad_emisora_telef
carácter
SI
Este campo almacenara los teléfonos de las entidades.
entidad_emisora_email
carácter
SI
Este campo almacenara los correos de las entidades.
NOMBRE DE LA TABLA: Entidad_adherida
entidad_adherida_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_cod
Clave foránea
SI
Almacena la clave foránea de entidad emisora.
marc_tarj_cod
Clave foránea
SI
Almacena la clave foránea de marca tarjeta.
entidad_adherida_nombre
carácter
SI
Este campo almacenara los nombres de las entidades.
entidad_adherida_direccion
carácter
SI
Este campo almacenara las direcciones de las entidades.
entidad_adherida_telf
carácter
SI
Este campo almacenara los teléfonos de las entidades.
entidad_adherida_email
carácter
SI
Este campo almacenara los correos de las entidades.
NOMBRE DE LA TABLA: arqueo_caja
arqueo_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
apert_cier_caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de persona.
arq_monto_efectivo
numérico
SI
Almacena el monto en pagos con efectivo.


arq_monto_cheque
numérico
SI
Almacena el monto en pagos con cheque.


arq_monto_tarj
numérico
SI
Almacena el monto con pagos en tarjeta.


NOMBRE DE LA TABLA: Forma_cobro
forma_cobro_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
forma_cobro_des
carácter
SI
Este campo almacena la descripción de forma de cobro.
NOMBRE DE LA TABLA: cuentas_cobrar
cuenta_cobrar_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
venta_cod
Clave foránea
SI
Almacena la clave foránea de venta.
cuent_cob_num_cuenta
numérico
SI
Este campo almacena el numero de cuenta a cobrar.
cuent_cob_monto
numérico
SI
Almacena el monto a cobrar.
cuent_cob_saldo
numérico
SI
Almacena el saldo de la cuenta.
cuent_cob_estado
Boolean
SI
Almacena el estado de la cuenta (pendiente, pagado, etc.)


NOMBRE DE LA TABLA: cobro_cheque
cobro_cheque_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_cod
Clave foránea
SI
Almacena la clave foránea de persona.
cobro_cod
numérico
SI
Clave primaria.
cobro_cheque_monto
numérico
SI
Este campo almacena el monto pagado con cheques.
cobro_cheque_fecha_venc
fecha
SI
Este campo almacena la fecha vencida del cheque.
cobro_cheque_numero
numérico
SI
Este campo almacena el número de cheque.
NOMBRE DE LA TABLA: cobro_tarjeta
cobro_tarj_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
entidad_adherida_cod
numérico
SI
Clave primaria.
entidad_emisora_cod
numérico
SI
Clave primaria.
cobro_tarj_monto
numérico
SI
Este campo almacena el monto pagado con tarjeta.
cobro_tarj_numero
numérico
SI
Este campo almacena el número de la tarjeta
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las cobranzas por forma de cobro.
v_gestionar_cobro_forma_cobro: visualización de las cobranzas por forma de cobro presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no sea una fecha futura o anterior.
Validar que el funcionario que tenga permisos para registrar cobros.
Validar existencia y estado en la tabla de entidades emisoras.
Validar número de cheque longitud (mínimo 6 dígitos), solo números.
Validar que la suma de los pagos coincida con la cuenta a cobrar.
Validar que no tenga cuentas vencidas o servicios sin registrar.
Validar que solo usuarios autorizados pueden anular una cobranza.







Ventana de Registrar Nota de Remisión

Diagrama entidad relación


Descripción de los campos
NOMBRE DE LA TABLA: nota_remisión_venta_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
nota_remis_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
venta_cod
Clave foránea
SI
Almacena la clave foránea de venta.
consultorio_cod
numérico
SI
Clave primaria.
not_rem_vent_fecha
fecha
SI
Este campo almacena la fecha de la nota de remisión
persona_cod
numérico
SI
Clave primaria.
not_rem_vent_estado
Boolean
SI
Este campo almacena el estado de la nota de remisión.
NOMBRE DE LA TABLA: nota_remisión_venta_det
nota_remis_cod
Clave foránea
SI
Almacena la clave foránea de nota de remisión.
items_cod
Clave foránea
SI
Almacena la clave foránea de ítems.
not_rem_vent_monto
numérico
SI
Este campo almacena el monto para el pedido en la nota de remisión.
not_rem_vent_des
carácter 
SI
Este campo almacena la descripción de la nota
NOMBRE DE LA TABLA: venta_cab
venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ven_cab_num_factura
numérico
SI
Almacena el número de la factura.
vent_cab_costo
numérico 
SI
Almacena el costo de la venta.
vent_cab_tipo_factura
carácter
SI
Almacena el tipo de factura en el campo.
vent_cab_interv_fech_venc
fecha
SI
Almacena la fecha de vencimiento de la venta.
consultorio_cod
numérico
SI
Clave primaria.
persona_cod
numérico
SI
Clave primaria.
NOMBRE DE LA TABLA: Items
items_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
items_insumo_cuestionarios
carácter
SI
Este campo almacenara la descripción de los insumos varios.
items_servicios_psico
carácter
SI
Este campo almacenara la descripción de los servicios psicológicos.
tipo_item_cod
numérico
SI
Clave primaria.
NOMBRE DE LA TABLA: tipo_items
tipo_item_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_items_des
carácter
SI
Almacena la descripción de los tipos de ítems.
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consult_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios correos. 
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las notas de remisión.
v_registrar_nota_remision: visualización de las notas de remisión presionando el botón consultar.
Habilitar Campos():
método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no sea una fecha futura o anterior.
Validar que el usuario tenga permisos para generar notas de remisión.
Validar coherencia con el tipo se servicio al solicitar.
Validar que no se registre el mismo trabajo para el mismo paciente en la misma fecha.
Validar que el campo de observaciones se permita palabras coherentes y explicativo para la solicitud en la nota.






Ventana de Gestionar Notas de Créditos y Débitos

Diagrama entidad relación


Descripción de los campos

NOMBRE DE LA TABLA: Nota_Venta_cab
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
nota_venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
venta_cod
numérico
SI
Clave primaria.
not_vent_fecha
fecha
SI
Este campo almacena la fecha de la nota.
not_vent_tipo_nota
carácter
SI
Este campo almacena el tipo de la nota.
nota_vent_estado
boolean
SI
Este campo almacena el estado de la nota.
NOMBRE DE LA TABLA: Nota_Venta_det
nota_venta_num
Clave foránea
SI
Almacena la clave foránea de persona.
items_cod
Clave foránea
SI
Almacena la clave foránea de persona.
not_vent_monto
numérico
SI
Almacena el monto de la venta.
not_vent_des
carácter
SI
Almacena la descripción de la nota venta.
NOMBRE DE LA TABLA: venta_cab
venta_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
ven_cab_num_factura
numérico
SI
Almacena el número de la factura.
vent_cab_costo
numérico 
SI
Almacena el costo de la venta.
vent_cab_tipo_factura
carácter
SI
Almacena el tipo de factura en el campo.
vent_cab_interv_fech_venc
fecha
SI
Almacena la fecha de vencimiento de la venta.
consultorio_cod
numérico
SI
Clave primaria.
persona_cod
numérico
SI
Clave primaria.
NOMBRE DE LA TABLA: Items
items_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
items_insumo_cuestionarios
carácter
SI
Este campo almacenara la descripción de los insumos varios.
items_servicios_psico
carácter
SI
Este campo almacenara la descripción de los servicios psicológicos.
tipo_item_cod
numérico
SI
Clave primaria.


NOMBRE DE LA TABLA: tipo_items
tipo_item_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
tipo_items_des
carácter
SI
Almacena la descripción de los tipos de ítems.
NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.


NOMBRE DE LA TABLA: consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consul_correo
numérico
SI
SI
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular las notas de crédito y débito.
v_registrar_nota_credito_debito: visualización de las notas de crédito y débito presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que tenga permisos para emitir notas de crédito o débito.
Validar que la factura no esté anulada o cerrada definitivamente.
Validar la existencia de forma de pago (transferencias, tarjetas, etc.)
Validar formato (números, sin caracteres especiales).
Validar que se cargue el tipo de servicio con claridad.
Validar si ya tiene una nota de crédito/débito aplicado, evitar duplicaciones.
  




Ventana de Arqueo de Caja

Diagrama entidad relación

Descripción de los campos

NOMBRE DE LA TABLA: apertura_cierre_caja
CAMPOS
TIPO
OBLIGATORIO
DESCRIPCIÓN
apert_cier_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
caja_cod
Clave foránea
SI
Almacena la clave foránea de caja.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apertura_fecha
fecha
SI
Este campo almacena la fecha de apertura.
apertura_monto
numérico
SI
Este campo almacena el monto de apertura.
apertura_cierre
numérico
SI
Este campo almacena el monto cierre.
fecha_cierre
fecha
SI
Este campo almacena la feche de cierre.
apert_cier_caj_estado
boolean
SI
Este campo almacena el estado de la apertura y cierre de caja.


NOMBRE DE LA TABLA: cobro_cab
cobro_cod
Clave foránea
SI
Almacena la clave foránea de caja.
cuenta_cobrar_cod
Clave foránea
SI
Almacena la clave foránea de persona.
venta_cod
Clave foránea
SI
Almacena la clave foránea de persona.
forma_cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
apert_cier_caja_cod
numérico
SI
Clave primaria.
caja_cod
numérico
SI
Clave primaria.
consultorio_cod
numérico
SI
Clave primaria.
cobro_cab_cobro_fecha
fecha
SI
Este campo almacena la fecha de cobro.
cobro_estado
boolean
SI
Este campo almacena el estado de cobro.
NOMBRE DE LA TABLA: cobro_det
cobro_cod
Clave foránea
SI
Almacena la clave foránea de cobro.


cobro_monto
numérico
SI
Almacena el monto del cobro.


NOMBRE DE LA TABLA: funcionario
funcionario_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
funcionario_cargo
carácter
SI
Este campo almacenara el cargo del funcionario.
funcionario_fech_ingreso
fecha
SI
Almacenara la fecha de ingreso del funcionario.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: consultorio
consul_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
consul_nombre
carácter
SI
Este campo almacenara las los nombres de los consultorios con las sedes correspondiente
consul_direc
carácter
SI
En este campo se podrá guardar la dirección exacta de los consultorios, y también se puede agregar la opción de mostrar en un mapa.
consul_telf
carácter
SI
Este campo permitirá almacenar el teléfono del consultorio, debería de analizar de almacenar varios teléfonos. 
consult_correo
carácter
SI
Este campo permitirá almacenar el correo del consultorio, debería de analizar de almacenar varios correos. 
NOMBRE DE LA TABLA: paciente
paciente_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
paciente_fech_registro
fecha
SI
Almacenara la fecha de fecha de registro del paciente.
persona_cod
Clave foránea
SI
Almacena la clave foránea de persona.
NOMBRE DE LA TABLA: arqueo_caja
arqueo_caja_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
apert_cier_caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
caja_cod
Clave foránea
SI
Almacena la clave foránea de persona.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de persona.
arq_monto_efectivo
numérico
SI
Almacena el monto en pagos con efectivo.
arq_monto_cheque
numérico
SI
Almacena el monto en pagos con cheque.
arq_monto_tarj
numérico
SI
Almacena el monto con pagos en tarjeta.
NOMBRE DE LA TABLA: Forma_cobro
forma_cobro_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
forma_cobro_des
carácter
SI
Este campo almacena la descripción de forma de cobro.
NOMBRE DE LA TABLA: Recaudaciones_depositar
recaud_depositar_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
apert_cier_caja_cod
Clave foránea
SI
Almacena la clave foránea de apertura y cierre de caja.
caja_cod
Clave foránea
SI
Almacena la clave foránea de caja.
consultorio_cod
Clave foránea
SI
Almacena la clave foránea de consultorio.
Recau_monto_efectivo
numérico
SI
Este campo almacena el monto con pago en efectivo.
Recau_monto_cheque
numérico
SI
Este campo almacena el monto con pago en cheque.
NOMBRE DE LA TABLA: cobro_cheque
cobro_cheque_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
entidad_emisora_cod
Clave foránea
SI
Almacena la clave foránea de persona.
cobro_cod
numérico
SI
Clave primaria.
cobro_cheque_monto
numérico
SI
Este campo almacena el monto pagado con cheques.
cobro_cheque_fecha_venc
fecha
SI
Este campo almacena la fecha vencida del cheque.
cobro_cheque_numero
numérico
SI
Este campo almacena el número de cheque.
NOMBRE DE LA TABLA: cobro_tarjeta
cobro_tarj_cod
numérico
SI
Este campo es la clave primaria de esta entidad por la misma será generada de manera automática.
cobro_cod
Clave foránea
SI
Almacena la clave foránea de persona.
entidad_adherida_cod
numérico
SI
Clave primaria.
entidad_emisora_cod
numérico
SI
Clave primaria.
cobro_tarj_monto
numérico
SI
Este campo almacena el monto pagado con tarjeta.
cobro_tarj_numero
numérico
SI
Este campo almacena el número de la tarjeta
Lista SP(procedimientos almacenados) o trigger
Lista de vistas
Lista de métodos
Lista de validaciones
sp_abm: procedimiento almacenado para agregar, grabar y anular los datos de arqueo de caja.
v_generar_arqueo_caja: visualización de los datos de arqueo de caja presionando el botón consultar.
Habilitar Campos():
Método que permita habilitar campos para los diferentes escenarios (agregar, grabar y anular).
Limpiar Campos(): método que permita limpiar los objetos de la ventana una vez utilizada por el usuario.
Deshabilitar Botones(): método que permite desactivar el conjunto de botones en caso que sea necesario.
Habilitar Botones(): método que permite habilitar el conjunto de botones en caso que sea necesario.
Deshabilitar Campos(): método que permita deshabilitar campos para los diferentes escenarios cuando no se esté escribiendo en ellos.
Validar que no se dupliquen los datos.
Validar los campos que son obligatorio que se cargue, debe emitir un mensaje de aviso al usuario.
Validar que se grabe los datos de acuerdo al tipo de dato definido.
Validar que no sea una fecha futura o anterior.
Validar que al seleccionar forma de pago sea una opción válida (Cheque, Transferencia, Efectivo).
Validar que el total coincida con el saldo real en caja.
Validar que el funcionario esté registrado y autorizado para la realización del arqueo de caja.
Se debe validar que el paciente esté en la base de datos.
Validar seleccionar forma de pago ya existente.
Validar descripción clara del motivo de egreso de la caja. 






Generar Informes
Ventana informes de referenciales de agendamiento

Ventana informes de referenciales de consultorio


Ventana informes de referenciales de ventas 


Ventana informes de movimientos de agendamiento

Ventana informes de movimientos de consultorio


Ventana informes de movimientos de ventas












	





 
CONCLUSIÓN 
Luego de haber abordado los distintos componentes del sistema, se puede afirmar que su desarrollo estuvo orientado a mejorar la organización y el funcionamiento general de una clínica de psicología esta  herramienta permite centralizar tareas fundamentales como la gestión de turnos, el registro clínico de los pacientes, el control de insumos y la administración financiera, lo que se traduce en una operativa más ordenada y eficaz.
Cada componente fue pensado cuidadosamente para asegurar que la información se registre de manera correcta y se mantenga protegida. Se incorporaron mecanismos de validación que ayudan a prevenir errores, mantener la integridad de los datos y brindar a los profesionales un respaldo confiable para la toma de decisiones.
En general, está  tecnológica va a ayudar positivamente la dinámica de trabajo en el consultorio, sino que también genera un impacto directo en la experiencia del paciente, al facilitar un mejor seguimiento de su proceso  y promover una comunicación más rapida de una herramienta moderna, versátil y con potencial para adaptarse a nuevas demandas que puedan surgir más adelante.

	

























REFERENCIAS
AgendaPro. (s.f.). Agenda médica: Software para agendamiento de citas médicas. Recuperado el 11 de mayo de 2025, de https://agendapro.com/es/agenda-medica


Carepatron. (s.f.). 9 best free appointment scheduling software for healthcare [Features + Pricing]. Recuperado el 11 de mayo de 2025, de https://www.carepatron.com/es/blog/9-best-free-appointment-scheduling-software-for-healthcare-features-pricing


eVENDÉ. (s.f.). Sistema de facturación electrónica para Paraguay. Recuperado el 11 de mayo de 2025, de https://www.evende.com.py/


Holded. (s.f.). Programa de facturación en la nube para pymes, asesorías y emprendedores. Recuperado el 11 de mayo de 2025, de https://www.holded.com/es/programa-facturacion


SaludVitale. (s.f.). Aplicación de gestión de consultorio médico. Recuperado el 11 de mayo de 2025, de https://www.saludvitale.com/doctor/aplicacion-de-gestion-de-consultorio-medico/


MedFlow. (s.f.). Sistema integral para clínicas y consultorios médicos. Recuperado el 11 de mayo de 2025, de https://medflow.com.py/



APÉNDICE 
Documentos
Módulo de agendamiento
Registrar agenda médica.

Gestionar citas (debe incluir reservación, confirmación y anulación).

Gestionar avisos recordatorios.

Registrar documentos varios relacionados a la ficha médica del paciente.


Módulo de consultorio
Gestionar consulta.





Gestionar diagnóstico.



Gestionar procedimientos e insumos utilizados.


Generar orden de estudios.


Generar orden de análisis.


Registrar recetas e indicaciones.


Registrar tratamientos.

Generar ficha médica.


Generar justificativo médico.


Módulo de ventas
Registrar Pedido de Clientes.

Gestionar ventas y generar cuentas a cobrar.


Registrar apertura y cierre de caja.

Gestionar las cobranzas por forma de cobro.

Registrar Nota de Remisión.


Gestionar Notas de Créditos y Débitos.

 
Generar el arqueo de caja.


Relevamiento
Módulo de agendamiento
1.  Registrar agenda médica
¿Posee un proceso de agenda médica? 
Si
¿Quien registra el proceso de agenda médica ?
La recepcionista registra la agenda médica
¿Qué documentos se utilizan para registrar la agenda médica?
Historial de pacientes, ficha médica y planilla de horarios de médicos.
¿Qué datos posee la agenda médica?
Nombre del paciente, fecha y hora de la cita, médico asignado, especialidad, motivo de consulta y estado de la cita (reservada, confirmada, anulada).
¿Le gustaría automatizar el proceso de agenda médica ?
si
¿Qué reportes le gustaría que emita el sistema?
Listado de citas por día, citas pendientes, citas canceladas
2. Gestionar citas (debe incluir reservación, confirmación y anulación)
¿Posee un proceso de? 
si
¿Quien registra la gestión de citas?
La recepcionista gestiona las citas, reserva, confirma, anula y agenda
¿Qué documentos se utilizan para ?
Historial de pacientes, ficha médica y registros de agenda médica.
¿Qué datos posee?
Nombre del paciente, fecha y hora de la cita, especialista asignado, especialidad, motivo de consulta, estado de la cita (reservada, confirmada, anulada) y observaciones.
¿Le gustaría automatizar el proceso de?
si
¿Qué reportes le gustaría que emita el sistema?
Listado de citas programadas por día, semana y mes. Citas confirmadas, pendientes y anuladas.  Disponibilidad de médicos y tiempos de espera.

3. Gestionar avisos recordatorios
¿Posee un proceso de gestionar avisos recordatorios? 
si
¿Quién registra los avisos recordatorios?
La recepcionista genera avisos recordatorios
¿Qué documentos se utilizan para avisar o recordar una cita ?
Registro de citas, historial de pacientes y notificaciones automatizadas (correo electrónico, mensajes de texto o WhatsApp).
¿Qué datos posee el detalle de la cita?
Nombre del paciente, fecha y hora de la cita, médico asignado, especialidad, estado de la cita (reservada, confirmada, anulada), medio de contacto del paciente y observaciones.
¿Le gustaría automatizar el proceso de gestionar los avisos recordatorios?
Sí, mediante notificaciones automáticas vía correo, SMS o WhatsApp.
¿Qué reportes le gustaría que emita el sistema?
Listado de pacientes que recibieron recordatorios. Registro de citas con recordatorio enviado y respuesta del paciente. Citas con alto riesgo de inasistencia.
4. Registrar documentos varios relacionados a la ficha médica del paciente (Opcional)
¿Posee un proceso relacionado? 
si
¿Quién registra la ficha médica?
La recepcionista registra la ficha médica
¿Qué documentos se utilizan para tener una ficha médica del paciente ?
Ficha clínica, antecedentes médicos, estudios previos, recetas médicas, informes de laboratorio y documentos de consentimiento informado.
¿Qué datos posee la ficha médica?
Datos personales del paciente (nombre, cédula, edad, contacto). Antecedentes médicos. Historial de consultas y tratamientos. Resultados de estudios y laboratorios.
¿Le gustaría automatizar el proceso relacionado a la ficha médica?
Sí, permitiendo la digitalización de documentos y acceso centralizado.
¿Qué reportes le gustaría que emita el sistema referente a la ficha médica?
Historial clínico completo del paciente. Reporte de diagnósticos y tratamientos aplicados. Listado de estudios. Registro de medicamentos y tratamientos en curso.

Módulo de consultorio
1. Gestionar consulta
¿Posee un proceso de consulta? 
Sí, pero actualmente se maneja de forma manual
¿Quién registra la consulta?
Él especialista registra la consulta
¿Qué documentos se utilizan para registrar la consulta?
Agenda física, ficha del paciente y notas manuscritas del profesional.
¿Qué datos posee el registro de la consulta ?
Datos del paciente (nombre, edad, contacto). Fecha y hora de la consulta. Motivo de consulta. Observaciones del profesional.
¿Le gustaría automatizar el proceso de consulta?
Sí, para agilizar la gestión de pacientes y mejorar el control de citas.
¿Qué reportes le gustaría que emita el sistema referente a las consultas?
Historial de consultas por paciente. Reporte de consultas realizadas en un período de tiempo.
2. Gestionar diagnóstico
¿Posee un proceso de gestión de diagnóstico? 
Sí.
¿Quién registra el diagnóstico?
Él especialista registra el diagnóstico 
¿Qué documentos se utilizan para realizar el diagnóstico ?
ficha clínica del paciente, notas manuscritas y pruebas psicológicas en papel.
¿Qué datos posee un diagnóstico?
Nombre del paciente. Fecha del diagnóstico. Evaluaciones aplicadas. Diagnóstico preliminar o definitivo.
¿Le gustaría automatizar el proceso de diagnósticos?
Sí, para organizar mejor los historiales y mejorar el acceso a la información.
¿Qué reportes le gustaría que emita el sistema de diagnósticos?
Diagnósticos realizados por fecha o paciente. Registro de evaluaciones aplicadas. Seguimiento de diagnósticos y evolución del paciente.

3. Gestionar procedimientos e insumos utilizados
¿Posee un proceso de gestión de procedimientos e insumos utilizados? 
No, pero se registran manualmente algunos insumos usados en sesiones.
¿Quien registra  los procedimientos utilizados?
Él  especialista registra los procedimientos e insumos utilizados
¿Qué documentos se utilizan para registrar los procedimientos e insumos ?
Notas manuales, fichas de seguimiento y registros de sesiones.
¿Qué datos posee?
Paciente atendido. Fecha del procedimiento. Técnicas o métodos aplicados (terapias cognitivas, conductuales, etc.).Insumos utilizados (test psicológicos, material audiovisual, etc.).
¿Le gustaría automatizar el proceso de gestionar los procedimientos e insumos utilizados?
Sí, para un mejor control de insumos y técnicas aplicadas.
¿Qué reportes le gustaría que emita el sistema?
Registro de procedimientos aplicados por paciente. Inventario de insumos utilizados. Análisis de efectividad de procedimientos por diagnóstico.
4. Generar orden de estudios
¿Posee un proceso de generar orden de estudios? 
Sí, pero se realiza manualmente.
¿Quién registra la orden de estudios?
Él especialista genera la orden de estudios 
¿Qué documentos se utilizan para generar el orden de estudios ?
Notas escritas y formularios físicos de derivación.
¿Qué datos posee una orden de estudios?
Nombre del paciente. Fecha de emisión. Estudios recomendados (evaluaciones psicológicas, test específicos, estudios médicos complementarios). Justificación del estudio.
¿Le gustaría automatizar el proceso de orden de estudios?
Sí, para emitir órdenes electrónicas y facilitar la gestión de estudios complementarios.
¿Qué reportes le gustaría que emita el sistema?
Registro de órdenes de estudios por paciente. Análisis de estudios solicitados con mayor frecuencia Resultados de estudios adjuntados al historial del paciente.

5. Generar orden de análisis
¿Posee un proceso de orden de análisis? 
Sí, pero actualmente se hace de forma manual.
¿Quién registra la orden de análisis?
Él especialista genera orden de análisis 
¿Qué documentos se utilizan para generar un orden de análisis ?
Notas manuscritas o formularios físicos de derivación.
¿Qué datos posee la orden de análisis?
Nombre del paciente. Fecha de emisión. Tipo de análisis solicitado (pruebas psicológicas, exámenes médicos complementarios). Justificación del análisis.
¿Le gustaría automatizar el proceso para generar orden de análisis?
Sí, para generar documentos digitales y facilitar su control.
¿Qué reportes le gustaría que emita el sistema?
Registro de órdenes de análisis por paciente.
Análisis de pruebas solicitadas con mayor frecuencia.
Resultados de análisis adjuntados al historial clínico.
6. Registrar recetas e indicaciones
¿Posee un proceso de recetas e indicaciones? 
si
¿Quien registra recetas e indicaciones?
Él especialista registra recetas e indicaciones
¿Qué documentos se utilizan para  registrar las recetas e indicaciones ?
Papeles manuscritos o formularios físicos.
¿Qué datos posee una receta?
Nombre del paciente. Fecha de emisión. Medicación recomendada (si aplica). Indicaciones terapéuticas (ejercicios, cambios en rutina, técnicas psicológicas recomendadas).
¿Le gustaría automatizar el proceso para registrar recetas e indicaciones?
Sí, para mayor claridad en la documentación y control de prescripciones.
¿Qué reportes le gustaría que emita el sistema?
Registro de recetas e indicaciones por paciente. Listado de medicamentos o tratamientos recomendados.
Seguimiento de indicaciones terapéuticas


7. Registrar tratamientos
¿Posee un proceso de registrar tratamientos ? 
si
¿Quien registra  el tratamiento?
Él especialista registra el tratamiento
¿Qué documentos se utilizan para registrar el tratamiento?
Notas en la ficha clínica del paciente.
¿Qué datos posee un tratamiento?
Nombre del paciente. Fecha de inicio del tratamiento. Tipo de tratamiento psicológico aplicado (terapia cognitivo-conductual, terapia de aceptación y compromiso, etc.).
¿Le gustaría automatizar el proceso de tratamientos?
si
¿Qué reportes le gustaría que emita el sistema?
Registro de tratamientos activos.
Evolución del paciente por tratamiento.
Análisis de efectividad de los tratamientos aplicados.
8. Generar ficha médica
¿Posee un proceso de fecha médica? 
si
¿Quién registra la ficha médica?
Él especialista genera la ficha médica 
¿Qué documentos se utilizan para generar la ficha médica?
Formatos físicos de historia clínica y notas manuscritas.	
¿Qué datos posee la ficha médica?
Datos personales del paciente.
Motivo de consulta. Antecedentes médicos y psicológicos.
Evaluaciones realizadas. Diagnóstico y plan de tratamiento.
¿Le gustaría automatizar el proceso de ficha médica?
Sí, para digitalizar y organizar los registros clínicos.
¿Qué reportes le gustaría que emita el sistema?
Historial clínico detallado por paciente.
Registro de diagnósticos y tratamientos asociados.
Reportes de evolución y seguimiento.

9. Generar justificativo médico
¿Posee un proceso de justificativo médico? 
si
¿Quien registra el  justificativo médico?
Él especialista genera el justificativo médico
¿Qué documentos se utilizan para registrar el justificativo médico?
Formularios impresos con firma del profesional.
¿Qué datos posee un  justificativo médico?
Nombre del paciente.
Fecha de emisión.
Motivo de la justificación (cita psicológica, reposo, tratamiento recomendado).
Firma y sello del psicólogo.
¿Le gustaría automatizar el proceso de justificativo médico?
Sí, para agilizar su emisión y reducir errores.
¿Qué reportes le gustaría que emita el sistema?
Registro de justificativos emitidos por el paciente.
Análisis de los motivos más comunes de justificación.
Historial de reposos recomendados.


Módulo de ventas
1. Registrar apertura y cierre de caja
¿Posee un proceso de Registro, apertura y cierre de caja ? 
Sí, pero se gestiona de forma manual en registros físicos o planillas de Excel.
¿Quién registra la apertura y cierre de caja ?
Él cajero registra la apertura y cierre de caja
¿Qué documentos se utilizan para  registrar la apertura y cierre de caja?
Planillas de caja o reportes internos.
¿Qué datos posee la apertura y cierre de caja?
Fecha y hora.
Usuario que realiza la apertura/cierre.
Saldo inicial y final. Detalle de ingresos y egresos.
¿Le gustaría automatizar el proceso de Registrar apertura y cierre de caja?
Sí, para mayor control y trazabilidad.
¿Qué reportes le gustaría que emita el sistema?
Registro de movimientos diarios.
Informe de diferencias de caja.
Auditoría de aperturas y cierres.
2. Generar el arqueo de caja
¿Posee un proceso de arqueo de caja? 
si
¿Quien registra el arqueo de caja ?
Él cajero genera el arqueo de caja
¿Qué documentos se utilizan para el arqueo de caja?
Planillas manuales de arqueo.
¿Qué datos posee el arqueo de caja?
Total de ingresos en efectivo, tarjetas y cheques.
Saldos de apertura y cierre.
Diferencias en caja.
¿Le gustaría automatizar el proceso de arqueo de caja?
si
¿Qué reportes le gustaría que emita el sistema de arqueo de caja?
Reporte detallado del arqueo de caja.
3. Generar recaudaciones a depositar
¿Posee un proceso de generar recaudaciones a depositar? 
si
¿Quién registra las recaudaciones a depositar ?
Él cajero genera las recaudaciones a depositar
¿Qué documentos se utilizan para generar recaudaciones a depositar?
Boletas de depósito y registros manuales.
¿Qué datos posee las recaudaciones a depositar?
Monto total recaudado.
Fecha y hora del depósito.
Banco y número de cuenta.
¿Le gustaría automatizar el proceso de  generar recaudaciones a depositar?
si
¿Qué reportes le gustaría que emita el sistema?
Resumen de depósitos realizados.
Control de depósitos pendientes.
4. Registrar Pedido de Clientes (Opcional)
¿Posee un proceso de registro de pedidos actualmente?
Sí
¿Quién registra el pedido?
El cajero
¿Qué documentos se utilizan para registrar el pedido?
Se utilizan hojas de pedido impresas, cuadernos o plantillas de Excel. 
En algunos casos también se hace mediante mensajes por WhatsApp o llamadas telefónicas.
¿Qué datos posee el pedido?
Nombre del cliente, Fecha del pedido Detalle de productos solicitados 
(nombre, tipo, precio) Forma de pago Fecha estimada del procedimiento Observaciones adicionales
¿Le gustaría automatizar el proceso de registro de pedidos?
Sí, sería útil para agilizar la gestión, evitar errores, mantener un historial organizado y mejorar la atención al cliente
¿Qué reportes le gustaría que emita el sistema?
Pedidos por fecha. Pedidos por cliente




5. Gestionar ventas y generar cuentas a cobrar.
¿Posee un proceso de Gestionar ventas y generar cuentas a cobrar.? 
Si
¿Quien registra las ventas y generar cuentas a cobrar. ?
Él cajero genera  las ventas y  cuentas a cobrar.
¿Qué documentos se utilizan para gestionar ventas y generar cuentas a cobrar. ?
Facturas, recibos y planillas de cuentas.
¿Qué datos posee la gestión ventas y generar cuentas a cobrar.?
Cliente y productos vendidos.
Monto y forma de pago.
Estado de la cuenta (pagado o pendiente).
¿Le gustaría automatizar el proceso de gestionar ventas y generar cuentas a cobrar.?
si
¿Qué reportes le gustaría que emita el sistema?
Ventas diarias y mensuales.
Cuentas por cobrar detalladas
6. Registrar Libro Ventas
¿Posee un proceso de registrar Libro Ventas? 
Sii
¿Quien registra el Libro Ventas ?
Él cajero registra Libro Ventas
¿Qué documentos se utilizan para registrar Libro Ventas ?
Facturas y registros contables.
¿Qué datos posee el registro de Libro Ventas 
Número de factura.
Cliente y monto.
Impuestos aplicados.
¿Le gustaría automatizar el proceso de rregistrar Libro Ventas?
Sí, para facilitar auditorías.
¿Qué reportes le gustaría que emita el sistema?
Libro IVA mensual.
Ventas detalladas con impuestos.


7. Gestionar las cobranzas por forma de cobro (efectivo, cheque, tarjeta de crédito y
débito) e imprimir comprobantes
¿Posee un proceso de  gestionar las cobranzas por forma de cobro (efectivo, cheque, tarjeta de crédito y débito) e imprimir comprobantes? 
si
¿Quien registra  las cobranzas por forma de cobro?
Él cajero genera las cobranzas por forma de cobro
¿Qué documentos se utilizan para las cobranzas por forma de cobro ?
Recibos y planillas de cobro.
¿Qué datos posee  las cobranzas por forma de cobro?
Cliente y monto pagado.
Forma de pago (efectivo, cheque, tarjeta)
¿Le gustaría automatizar el proceso de  las cobranzas por forma de cobro?
si
¿Qué reportes le gustaría que emita el sistema?
Resumen de cobranzas por tipo de pago.
Comprobantes de pago.
8. Registrar Nota de Remisión
¿Posee un proceso de registrar Nota de Remisión? 
si
¿Quién registra las notas de remisión ?
Él cajero genera Nota de Remisión
¿Qué documentos se utilizan para registrar la Nota de Remisión ?
Formularios impresos.
¿Qué datos posee una Nota de Remisión?
Cliente y productos enviados.
Fecha.
¿Le gustaría automatizar el proceso de las notas de remisión?
si
¿Qué reportes le gustaría que emita el sistema?

Historial de remisiones.
Control de entregas pendientes.



9. Gestionar Notas de Créditos y Débitos
¿Posee un proceso de gestionar Notas de Créditos y Débitos? 
si
¿Quien registra las Notas de Créditos y Débitos ?
Él cajero genera Notas de Créditos y Débitos
¿Qué documentos se utilizan para gestionar Notas de Créditos y Débitos ?
Facturas anuladas y notas de crédito/débito.
¿Qué datos posee las Notas de Créditos y Débitos?
Cliente y motivo.
Monto y número de factura afectada.
¿Le gustaría automatizar el proceso de gestionar Notas de Créditos y Débitos?
Sí, para control de devoluciones.
¿Qué reportes le gustaría que emita el sistema?
Resumen de notas de crédito y débito.
Impacto en la facturación.
10. Elaborar Informes Web
¿Posee un proceso de elaborar Informes Web? 
No
¿Quién registra informes web ?
Él cajero genera Informes Web
¿Qué documentos se utilizan para  elaborar Informes Web?
Reportes en Excel o Word
¿Qué datos posee un informe web?
Ventas, cobranzas y cuentas por cobrar.
Movimientos de caja y arqueos.
¿Le gustaría automatizar el proceso de elaborar Informes Web?
Si
¿Qué reportes le gustaría que emita el sistema?
Dashboard financiero.
Reportes de gestión de ventas y cobranzas.
