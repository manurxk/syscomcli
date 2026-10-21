"""Mensajes estándar de validación de datos.

Un solo texto por tipo de error, para que el sistema diga lo mismo en todas las pantallas y el
anexo del manual (docs/scripts/extraer_mensajes_validacion.py) los agrupe como "mensajes comunes".
Cambiar la redacción acá la cambia en todo el sistema; la regla (qué caracteres se admiten) sigue
en cada DAO y en su check constraint.
"""


# Nombre que ve la persona en el formulario para cada dato que el servidor recibe con su clave interna.
ETIQUETAS = {
    'id_especialista': 'Especialista', 'id_sede': 'Sede', 'id_consultorio': 'Consultorio',
    'id_dia_semana': 'Día', 'hora_inicio': 'Hora de inicio', 'hora_fin': 'Hora de fin',
    'duracion_turno_min': 'Duración del turno', 'fec_desde': 'Fecha desde',
    'id_slot_agenda': 'Turno', 'id_agenda_horario': 'Horario', 'id_paciente': 'Paciente',
    'motivo': 'Motivo', 'motivo_consulta': 'Motivo de la consulta',
    'consulta_fecha': 'Fecha de la consulta', 'consulta_motivo': 'Motivo de la consulta',
    'consulta_estado': 'Estado de la consulta',
    'id_cuenta_cobrar': 'Cuenta a cobrar', 'id_factura': 'Factura', 'id_caja': 'Caja',
    'id_deposito': 'Depósito', 'id_tipo_comprobante': 'Tipo de comprobante',
    'id_condicion_venta': 'Condición de venta', 'id_timbrado': 'Timbrado',
    'id_punto_expedicion': 'Punto de expedición', 'id_estado_factura': 'Estado de la factura',
    'fecha_factura': 'Fecha de la factura', 'fecha_remision': 'Fecha de la remisión',
    'nombre': 'Nombre', 'apellido': 'Apellido', 'cedula': 'Cédula', 'telefono': 'Teléfono',
    'id_cargo': 'Cargo', 'fecha_nacimiento': 'Fecha de nacimiento',
    'username': 'Username', 'password': 'Contraseña', 'id_funcionario': 'Funcionario', 'id_rol': 'Rol',
}


def etiqueta(campo):
    """Nombre visible del dato; si no está en la tabla se deja tal cual."""
    return ETIQUETAS.get(campo, campo)


def msg_obligatorio(campo):
    """El campo está vacío: 'El campo "Descripción" es obligatorio.' (acepta la clave interna)."""
    return f'El campo "{etiqueta(campo)}" es obligatorio.'


def msg_caracteres(campo, permitidos):
    """El campo trae caracteres que no se admiten; `permitidos` dice cuáles sí (p. ej. 'letras, números y espacios')."""
    return f'El campo "{campo}" contiene caracteres no permitidos. Use solo {permitidos}.'


def msg_existe(entidad, valor):
    """El dato ya está cargado; `entidad` lleva su artículo (p. ej. 'una especialidad', 'un tipo de análisis')."""
    return f'Ya existe {entidad} "{valor}".'
