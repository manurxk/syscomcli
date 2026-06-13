Problemas comunes a los tres archivos
1. Bootstrap 4 mezclado con Bootstrap 5
Se usa mr-2, ml-2 (Bootstrap 4) junto con fw-bold (Bootstrap 5). Hay que unificar. Si es BS5, reemplazar mr-* → me-*, ml-* → ms-*, mb-* se mantiene igual.
2. data-bs-toggle vs data-toggle
En soporte.html el acordeón usa data-bs-toggle (BS5), pero si el resto del proyecto usa BS4, el acordeón no va a funcionar.
3. Clases CSS personalizadas sin definir en los templates
text-gray-700, text-gray-800, card-header-actions, icon-circle se usan pero no están definidas localmente. Dependen del base.html. Si ese base cambia, todo se rompe.

privacidad.html — Mejoras específicas

El contenido es muy largo y denso. Convendría agregar un índice navegable al inicio con anclas (<a href="#seccion-1">), para que el usuario salte directo a la sección que le interesa.
Las listas de secciones son repetitivas visualmente. Podrían agruparse en cards de dos columnas para romper la monotonía.
La alert-info al final podría ser un elemento más destacado (banner o franja), no solo una alerta genérica.


contacto.html — Mejoras específicas

El formulario hace mailto: al enviarse, lo cual depende del cliente de correo del usuario y puede fallar silenciosamente. Lo ideal sería enviarlo por AJAX a un endpoint Flask (/contacto/enviar) que use Flask-Mail o similar.
No hay validación visual de campos (feedback de Bootstrap con was-validated, mensajes de error por campo).
El alert() nativo de JS es bloqueante y muy anticuado — reemplazar por un toast de Bootstrap o un div de alerta que aparezca en el DOM.
Falta un campo de teléfono opcional, útil para soporte técnico.


soporte.html — Mejoras específicas

El acordeón de FAQ usa data-bs-parent que colapsa los demás items, lo cual es correcto, pero el ícono fa-chevron-right nunca rota al expandirse. Falta CSS o JS para cambiar a fa-chevron-down al abrir.
La sección "Funcionalidades del Sistema" tiene 6 cards con listas iguales visualmente. Agregar un ícono con color de fondo distinto por categoría ayudaría a distinguirlas.
Sería útil agregar un campo de búsqueda en el FAQ para filtrar preguntas con JS simple, especialmente si la lista crece.
La versión está hardcodeada como 1.0. Convendría pasarla como variable de contexto desde Flask igual que current_year.


Mejora transversal: SEO y accesibilidad

Ninguno de los tres tiene atributos aria-label en los botones de iconos.
Las imágenes/íconos decorativos deberían tener aria-hidden="true".
Los <h1> dentro del {% block contenido %} compiten con el <h1> que probablemente ya existe en base.html.





Prompt de implementación — Mejora de archivos de información AngaSys
Tengo tres templates HTML de Flask (soporte.html, privacidad.html, contacto.html) que usan {% extends "base.html" %} y {% block contenido %}. Necesito que los reescribas completamente con las siguientes instrucciones:

Reglas generales para los tres archivos

Respetar siempre la estructura {% extends "base.html" %} y {% block contenido %}{% endblock %}
Usar Bootstrap 5 de forma consistente: me-*, ms-*, mb-*, data-bs-*
No usar mr-*, ml-*, data-toggle, ni data-parent (Bootstrap 4)
Usar aria-hidden="true" en todos los íconos decorativos de FontAwesome
Usar aria-label="..." en todos los botones que solo tengan íconos sin texto visible
No duplicar <h1> — el título principal ya viene del base.html, usar <h2> como primer nivel dentro del bloque
Variables de Flask disponibles: {{ current_year }}


soporte.html — Cambios y textos nuevos
Sección "Acerca de AngaSys" — reemplazar texto por:

AngaSys es un sistema integral de gestión diseñado para consultorios psicológicos y neuropsicológicos. Desarrollado para la Clínica Integral Neuropsicológica (CIN), centraliza en una sola plataforma todos los procesos clínicos y administrativos: desde el primer turno de un paciente hasta la emisión de su factura, pasando por el registro de consultas, diagnósticos y documentos médicos. El sistema está pensado para todo el personal de la clínica, con accesos y vistas adaptadas al rol de cada usuario.

Sección "Funcionalidades del Sistema" — enriquecer cada módulo:

Gestión de Pacientes: Registro completo con datos personales, de contacto y obra social. Historial médico unificado con todas las consultas anteriores. Gestión de pacientes menores con datos del tutor responsable. Carga y visualización de fichas médicas.
Agendamiento: Agenda visual por especialista con vista diaria, semanal y mensual. Creación, modificación y cancelación de citas. Validación automática de disponibilidad horaria para evitar solapamientos. Registro del estado de cada cita (pendiente, confirmada, atendida, cancelada).
Consultas Médicas: Registro detallado de cada consulta vinculada al paciente y al especialista. Carga de motivo de consulta, anamnesis, diagnósticos con codificación, tratamientos indicados y evolución. Acceso al historial completo desde la misma pantalla de consulta.
Documentos Médicos: Generación de recetas médicas, órdenes de estudios complementarios, certificados de salud y presupuestos. Documentos vinculados al paciente y disponibles en su historial.
Módulo de Ventas: Facturación de consultas y servicios. Gestión de cuentas a cobrar, registro de pagos y cobranzas. Control de caja diaria con apertura y cierre. Seguimiento del estado de deuda por paciente.
Seguridad: Acceso al sistema mediante usuario y contraseña. Roles diferenciados (administrador, especialista, recepción) con permisos específicos por módulo. Registro de auditoría de todas las operaciones realizadas. Gestión de usuarios desde el panel de administración.

FAQ — agregar estas preguntas nuevas además de las existentes:

¿Puedo ver el historial completo de un paciente? → Sí, desde la ficha del paciente podés acceder a todas sus consultas, documentos generados, citas anteriores y estado de cuenta, siempre según tu rol en el sistema.
¿Qué pasa si cancelo una cita por error? → Contactá al administrador del sistema. Las citas canceladas quedan registradas en el historial y pueden ser revisadas, pero no se eliminan automáticamente.
¿El sistema funciona desde el celular? → AngaSys está optimizado para uso en computadora de escritorio o notebook. Puede visualizarse en dispositivos móviles, pero la experiencia está pensada para pantallas más grandes.

Mejoras técnicas:

Agregar CSS para rotar el ícono fa-chevron-right a fa-chevron-down cuando el acordeón se expande, usando la clase collapsed de Bootstrap 5
Agregar campo de búsqueda en tiempo real sobre las preguntas del FAQ con JS puro (filtrar por texto del botón)
Diferenciar los 6 módulos con colores distintos en el icon-circle: primary, success, info, warning, danger, secondary
Reemplazar "1.0" hardcoded por {{ system_version | default('1.0') }}


privacidad.html — Cambios y textos nuevos
Agregar índice navegable al inicio, antes del primer card, con anclas a cada sección:
1. Recopilación de Información (#seccion-1)
2. Uso de la Información (#seccion-2)
3. Confidencialidad Médica (#seccion-3)
4. Seguridad de los Datos (#seccion-4)
5. Acceso y Control de Datos (#seccion-5)
6. Compartir Información (#seccion-6)
7. Retención de Datos (#seccion-7)
8. Derechos de los Usuarios (#seccion-8)
9. Contacto (#seccion-9)
10. Cambios en la Política (#seccion-10)
Agregar id="seccion-N" a cada <h4> correspondiente.
Sección "Información General" — reemplazar texto por:

AngaSys es un sistema de gestión de consultorios psicológicos y neuropsicológicos desarrollado para la Clínica Integral Neuropsicológica (CIN). Dado que el sistema maneja información sensible de salud, nos comprometemos con los más altos estándares de privacidad y confidencialidad. Esta política describe qué datos se recopilan, cómo se usan, quién puede acceder a ellos y cuáles son los derechos de los pacientes y usuarios del sistema.

Sección "Derechos de los Usuarios" — agregar estos puntos:

Solicitar que sus datos sean corregidos si contienen errores.
Conocer quién accedió a su información dentro del sistema.
Solicitar la eliminación de datos cuando corresponda legalmente.

Mejoras técnicas:

El índice debe tener scroll suave con CSS: html { scroll-behavior: smooth; }
Dividir el card único actual en múltiples cards, uno por sección, para mejorar legibilidad
Cada card debe tener su id correspondiente para que los anclas funcionen


contacto.html — Cambios y textos nuevos
Sección informativa — reemplazar texto "Sobre AngaSys" por:

AngaSys gestiona de forma integrada los turnos, consultas, documentos médicos y facturación de la Clínica Integral Neuropsicológica. Si tenés dudas sobre cómo usar el sistema, encontraste un error o necesitás soporte técnico, este es el canal correcto para comunicarte con el equipo de desarrollo.

Formulario — mejoras:

Agregar campo Teléfono (opcional, tipo tel, placeholder +595 ...)
Aplicar validación visual de Bootstrap 5 con la clase needs-validation y novalidate en el form
Activar validación en JS con el patrón estándar de Bootstrap 5 (classList.add('was-validated'))
Reemplazar el alert() nativo por un <div id="mensajeEnvio"> que aparezca en el DOM con clase alert alert-success después de hacer clic en enviar
El mensaje de confirmación debe decir: "Se abrirá tu cliente de correo para completar el envío. Si no se abre automáticamente, escribinos directamente a armanuramirez16@gmail.com"

Mejoras técnicas:

Reemplazar el <form id="contactoForm"> sin atributos por <form id="contactoForm" class="needs-validation" novalidate>
Cada <input> y <select> obligatorio debe tener <div class="invalid-feedback"> con mensaje descriptivo
El botón de envío debe desactivarse visualmente mientras se "procesa" (cambiar texto a "Enviando..." por 1.5 segundos antes de abrir el mailto)