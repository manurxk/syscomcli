from flask import session


def build_sidebar():
    """Builds the sidebar structure based on current user's permissions.

    FASE 1 (2026-06-21): se reconstruye sub-fase por sub-fase a medida que
    cada modulo se registra en app/__init__.py
    (ver docs_reestructuracion/06_MAPEO_ENTIDADES_NUEVA_ESTRUCTURA.md).
    """
    roles = {(r or "").strip().upper() for r in session.get("roles", [])}
    items = []

    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        items.append({
            "title": "Funcionarios",
            "endpoint": "funcionario.funcionarioIndex",
            "html_icon": '<i data-feather="briefcase"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN", "RECEPCION"}:
        items.append({
            "title": "Pacientes",
            "endpoint": "paciente.pacienteIndex",
            "html_icon": '<i data-feather="users"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        items.append({
            "title": "Usuarios",
            "endpoint": "usuario.usuarioIndex",
            "html_icon": '<i data-feather="user-check"></i>'
        })

    agendamiento_items = []
    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        agendamiento_items.append({
            "title": "Agenda Médica",
            "endpoint": "agenda_horarios.agendaHorariosIndex",
            "html_icon": '<i data-feather="calendar"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN", "RECEPCION"}:
        agendamiento_items.append({
            "title": "Citas",
            "endpoint": "cita.citaIndex",
            "html_icon": '<i data-feather="clipboard"></i>'
        })

    if roles & {"ADMINISTRADOR", "SUPERADMIN", "RECEPCION"}:
        agendamiento_items.append({
            "title": "Lista de Espera",
            "endpoint": "lista_espera.listaEsperaIndex",
            "html_icon": '<i data-feather="clock"></i>'
        })

    clinico_items = []
    if roles & {"ADMINISTRADOR", "SUPERADMIN", "CLINICO"}:
        clinico_items.append({
            "title": "Mi Agenda",
            "endpoint": "mi_agenda.miAgendaIndex",
            "html_icon": '<i data-feather="calendar"></i>'
        })
        clinico_items.append({
            "title": "Consultas",
            "endpoint": "consulta.consultaIndex",
            "html_icon": '<i data-feather="file-text"></i>'
        })
        clinico_items.append({
            "title": "PEI",
            "endpoint": "pei.peiIndex",
            "html_icon": '<i data-feather="book-open"></i>'
        })
        clinico_items.append({
            "title": "Fichas Médicas",
            "endpoint": "ficha.fichaIndex",
            "html_icon": '<i data-feather="clipboard"></i>'
        })

    ventas_items = []
    if roles & {"ADMINISTRADOR", "SUPERADMIN", "VENTAS"}:
        ventas_items.append({
            "title": "Pedidos",
            "endpoint": "pedido.pedidoIndex",
            "html_icon": '<i data-feather="shopping-cart"></i>'
        })
        ventas_items.append({
            "title": "Presupuestos",
            "endpoint": "presupuesto.presupuestoIndex",
            "html_icon": '<i data-feather="file-text"></i>'
        })
        ventas_items.append({
            "title": "Estado de Caja",
            "endpoint": "apertura_cierre_caja.cajaEstado",
            "html_icon": '<i data-feather="unlock"></i>'
        })
        ventas_items.append({
            "title": "Historial de Caja",
            "endpoint": "apertura_cierre_caja.cajaHistorial",
            "html_icon": '<i data-feather="clock"></i>'
        })
        ventas_items.append({
            "title": "Arqueos de Caja",
            "endpoint": "arqueo_caja.arqueoIndex",
            "html_icon": '<i data-feather="check-square"></i>'
        })
        ventas_items.append({
            "title": "Facturas",
            "endpoint": "factura.facturaIndex",
            "html_icon": '<i data-feather="file-text"></i>'
        })
        ventas_items.append({
            "title": "Remisiones",
            "endpoint": "remision.remisionIndex",
            "html_icon": '<i data-feather="truck"></i>'
        })
        ventas_items.append({
            "title": "Notas de Crédito",
            "endpoint": "nota_credito.notaCreditoIndex",
            "html_icon": '<i data-feather="minus-circle"></i>'
        })
        ventas_items.append({
            "title": "Notas de Débito",
            "endpoint": "nota_debito.notaDebitoIndex",
            "html_icon": '<i data-feather="plus-circle"></i>'
        })
        ventas_items.append({
            "title": "Cuentas a Cobrar",
            "endpoint": "cuenta_cobrar.cuentaCobrarIndex",
            "html_icon": '<i data-feather="credit-card"></i>'
        })
        ventas_items.append({
            "title": "Cobranzas",
            "endpoint": "cobranza.cobranzaIndex",
            "html_icon": '<i data-feather="dollar-sign"></i>'
        })
        ventas_items.append({
            "title": "Recaudaciones",
            "endpoint": "recaudacion.recaudacionIndex",
            "html_icon": '<i data-feather="archive"></i>'
        })
        ventas_items.append({
            "title": "Libro de Ventas",
            "endpoint": "libro_ventas.libroVentasIndex",
            "html_icon": '<i data-feather="book"></i>'
        })

    config_items = []
    if roles & {"ADMINISTRADOR", "SUPERADMIN"}:
        config_items.append({
            "title": "Referenciales",
            "endpoint": "referenciales.referencialesIndex",
            "html_icon": '<i data-feather="sliders"></i>'
        })
        config_items.append({
            "title": "Timbrados",
            "endpoint": "timbrado.timbradoIndex",
            "html_icon": '<i data-feather="award"></i>'
        })
        config_items.append({
            "title": "Puntos de Expedición",
            "endpoint": "punto_expedicion.puntoExpedicionIndex",
            "html_icon": '<i data-feather="map-pin"></i>'
        })
        config_items.append({
            "title": "Roles y Permisos",
            "endpoint": "permisos.permisosIndex",
            "html_icon": '<i data-feather="shield"></i>'
        })

    if not items and not agendamiento_items and not clinico_items and not ventas_items and not config_items:
        return []

    groups = []
    if items:
        groups.append({"heading": "Personas", "items": items})
    if agendamiento_items:
        groups.append({"heading": "Agendamiento", "items": agendamiento_items})
    if clinico_items:
        groups.append({"heading": "Clínico", "items": clinico_items})
    if ventas_items:
        groups.append({"heading": "Ventas", "items": ventas_items})
    if config_items:
        groups.append({"heading": "Configuración", "items": config_items})

    return [{
        "is_flat": True,
        "groups": groups
    }]
