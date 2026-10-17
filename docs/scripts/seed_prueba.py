"""
Carga de datos de prueba de punta a punta por la API HTTP de Sysclin.

Recorre el mismo circuito que un usuario real (con sus validaciones):
catálogos clínicos → usuarios → agenda → pacientes → citas en distintos estados
→ consultas con distinto nivel de detalle → facturas con distintas variantes.

Uso (la contraseña del administrador NUNCA se escribe en este archivo):
    SEED_ADMIN_USER=psicoadmin SEED_ADMIN_PASS='...' python docs/scripts/seed_prueba.py

Notas:
- Los pacientes de prueba usan cédulas 9000001..9000010 y no tienen correo,
  así no se envía ningún mail (recordatorios ni factura).
- Si ya existe la cédula 9000001 el script se detiene (no duplica la carga).
"""
import os
import re
import sys
from datetime import date

import requests

BASE = os.getenv('SEED_BASE_URL', 'http://localhost:5005')
API = BASE + '/api/v1'
ADMIN_USER = os.getenv('SEED_ADMIN_USER', 'psicoadmin')
ADMIN_PASS = os.getenv('SEED_ADMIN_PASS')
PASS_USUARIOS_PRUEBA = 'Prueba2026!'
HOY = date.today().isoformat()

# Referenciales existentes en sysclin_bd (verificados antes de escribir el script)
ID_SEDE = 1
ID_CONSULTORIO = 1
ID_ESPECIALIDAD = 3            # PSICO (la única que tienen ambos especialistas)
ID_ESPECIALISTA_LAURA = 3      # Laura Gonzalez: agenda lunes y martes
ID_ESPECIALISTA_ADMIN = 4      # psicoadmin: se le crea agenda mié/jue/vie
ID_CARGO_RECEPCION = 11
ID_ROL_RECEPCION = 3
ID_ROL_VENTAS = 5
ID_TIPO_COMPROBANTE = 2        # FACTURA
CONTADO, CREDITO = 1, 2
ID_TIMBRADO = 1
ID_PUNTO_EXPEDICION = 1
ID_ESTADO_EMITIDA = 1
ID_MONEDA_PYG = 1
ID_CAJA = 1                    # CAJA PRINCIPAL (ya abierta en PYG)
IVA10, EXENTO = 4, 6
EFECTIVO, CHEQUE, TARJETA_CREDITO, TARJETA_DEBITO, TRANSFERENCIA = 1, 2, 3, 4, 5
ID_TIPO_ITEM_SERVICIO = 1
ITEM_CONSULTA = (2, 'CONSULTA PSICOLOGICA', 150000)
ITEM_EVALUACION = (3, 'EVALUACION PSICOPEDAGOGICA', 200000)
ID_MEDICAMENTO = 4
ID_TIPO_ESTUDIO = 4
ID_TIPO_ANALISIS = 4

informe = []   # (paso, ok, detalle)


def registrar(paso, ok, detalle=''):
    informe.append((paso, ok, detalle))
    print(f"[{'OK ' if ok else 'ERR'}] {paso}" + (f" -> {detalle}" if detalle else ''))


class Cliente:
    """Sesión HTTP autenticada con CSRF, como la usa el navegador."""

    def __init__(self, usuario, clave):
        self.usuario = usuario
        self.s = requests.Session()
        r = self.s.get(BASE + '/login')
        tok = re.search(r'name="csrf_token" value="([^"]+)"', r.text).group(1)
        r = self.s.post(BASE + '/login', data={
            'usuario_nombre': usuario, 'usuario_clave': clave, 'csrf_token': tok,
        }, allow_redirects=False)
        if r.status_code != 302 or 'login' in (r.headers.get('Location') or ''):
            raise RuntimeError(f'No se pudo iniciar sesión como {usuario}')
        r = self.s.get(BASE + '/')
        self.csrf = re.search(r'name="csrf-token" content="([^"]+)"', r.text).group(1)

    def llamar(self, metodo, ruta, paso, json=None, params=None):
        r = self.s.request(metodo, API + ruta, json=json, params=params,
                           headers={'X-CSRFToken': self.csrf})
        try:
            cuerpo = r.json()
        except ValueError:
            cuerpo = {'success': False, 'error': f'HTTP {r.status_code} sin JSON'}
        ok = r.ok and cuerpo.get('success', True)
        if paso:
            registrar(f'{paso} [{self.usuario}]', ok, '' if ok else cuerpo.get('error') or f'HTTP {r.status_code}')
        return cuerpo.get('data') if ok else None


# ─── 1. Catálogos clínicos (estaban vacíos) ─────────────────────────────────
CATALOGOS = {
    'diagnosticos': ('des_diagnostico', 'id_diagnostico', [
        {'des_diagnostico': 'TRASTORNO DE ANSIEDAD GENERALIZADA', 'cod_cie10': 'F41.1'},
        {'des_diagnostico': 'EPISODIO DEPRESIVO MODERADO', 'cod_cie10': 'F32.1'},
        {'des_diagnostico': 'TRASTORNO DE ACTIVIDAD Y ATENCION', 'cod_cie10': 'F90.0'},
        {'des_diagnostico': 'TRASTORNO ESPECIFICO DE LA LECTURA', 'cod_cie10': 'F81.0'},
        {'des_diagnostico': 'TRASTORNO DE ADAPTACION', 'cod_cie10': 'F43.2'},
        {'des_diagnostico': 'INSOMNIO NO ORGANICO', 'cod_cie10': 'F51.0'},
    ]),
    'signos': ('des_signo', 'id_signo', [
        {'des_signo': 'INQUIETUD PSICOMOTORA'}, {'des_signo': 'LLANTO FACIL'},
        {'des_signo': 'CONTACTO VISUAL ESCASO'}, {'des_signo': 'DISCURSO ACELERADO'},
    ]),
    'sintomas': ('des_sintoma', 'id_sintoma', [
        {'des_sintoma': 'PREOCUPACION EXCESIVA'}, {'des_sintoma': 'DIFICULTAD PARA DORMIR'},
        {'des_sintoma': 'TRISTEZA PERSISTENTE'}, {'des_sintoma': 'DIFICULTAD DE CONCENTRACION'},
        {'des_sintoma': 'IRRITABILIDAD'},
    ]),
    'tipos-procedimientos': ('des_tipo_procedimiento', 'id_tipo_procedimiento', [
        {'des_tipo_procedimiento': 'ENTREVISTA CLINICA'},
        {'des_tipo_procedimiento': 'APLICACION DE TEST PSICOMETRICO'},
        {'des_tipo_procedimiento': 'PSICOEDUCACION'},
    ]),
}


def cargar_catalogos(admin):
    ids = {}
    for ruta, (campo_des, campo_id, filas) in CATALOGOS.items():
        existentes = {f[campo_des]: f[campo_id] for f in (admin.llamar('GET', f'/{ruta}', None) or [])}
        ids[ruta] = []
        for fila in filas:
            if fila[campo_des] not in existentes:
                data = admin.llamar('POST', f'/{ruta}', f'Catálogo {ruta}: {fila[campo_des]}', json=fila)
                if data:
                    existentes[fila[campo_des]] = data.get(campo_id) or data.get('id')
            ids[ruta].append(existentes.get(fila[campo_des]))
        if None in ids[ruta]:
            # Si el POST no devolvió el id, se relee la lista
            existentes = {f[campo_des]: f[campo_id] for f in (admin.llamar('GET', f'/{ruta}', None) or [])}
            ids[ruta] = [existentes.get(f[campo_des]) for f in filas]
    return ids


# ─── 2. Usuarios de prueba ──────────────────────────────────────────────────
def crear_usuarios(admin):
    cargos = admin.llamar('GET', '/cargos', None) or []
    id_cargo_cajero = next((c['id_cargo'] for c in cargos if c['des_cargo'] == 'CAJERO'), None)
    if not id_cargo_cajero:
        data = admin.llamar('POST', '/cargos', 'Cargo CAJERO', json={'des_cargo': 'CAJERO', 'es_clinico': False})
        cargos = admin.llamar('GET', '/cargos', None) or []
        id_cargo_cajero = next((c['id_cargo'] for c in cargos if c['des_cargo'] == 'CAJERO'), None)

    usuarios = [
        ('recep2', 'Carmen', 'Benitez', '9100001', ID_CARGO_RECEPCION, ID_ROL_RECEPCION),
        ('cajero1', 'Diego', 'Acosta', '9100002', id_cargo_cajero, ID_ROL_VENTAS),
    ]
    for nick, nombre, apellido, cedula, id_cargo, id_rol in usuarios:
        func = admin.llamar('POST', '/funcionarios', f'Funcionario {nombre} {apellido}', json={
            'nombre': nombre, 'apellido': apellido, 'cedula': cedula,
            'telefono': '0981000000', 'fecha_nacimiento': '1992-05-10', 'id_cargo': id_cargo,
        })
        if not func:
            continue
        admin.llamar('POST', '/usuarios', f'Usuario {nick}', json={
            'username': nick, 'password': PASS_USUARIOS_PRUEBA,
            'password_confirmacion': PASS_USUARIOS_PRUEBA,
            'id_funcionario': func['id_funcionario'], 'id_rol': id_rol,
        })


# ─── 3. Agenda para el segundo especialista ─────────────────────────────────
def crear_agenda(admin):
    for id_dia in (3, 4, 5):   # miércoles, jueves, viernes
        admin.llamar('POST', '/agenda-horarios', f'Agenda especialista {ID_ESPECIALISTA_ADMIN} día {id_dia}', json={
            'id_especialista': ID_ESPECIALISTA_ADMIN, 'id_sede': ID_SEDE, 'id_consultorio': ID_CONSULTORIO,
            'id_dia_semana': id_dia, 'hora_inicio': '08:00', 'hora_fin': '12:00',
            'duracion_turno_min': 60, 'modalidad_default': 'PRESENCIAL', 'fec_desde': HOY,
        })


# ─── 4. Pacientes ───────────────────────────────────────────────────────────
PACIENTES = [
    {'nombre': 'Lucia', 'apellido': 'Fernandez', 'fecha_nacimiento': '1990-03-14', 'id_genero': 2},
    {'nombre': 'Marcos', 'apellido': 'Villalba', 'fecha_nacimiento': '1985-11-02', 'id_genero': 1},
    {'nombre': 'Sofia', 'apellido': 'Ortiz', 'fecha_nacimiento': '1998-07-21', 'id_genero': 2},
    {'nombre': 'Jorge', 'apellido': 'Caballero', 'fecha_nacimiento': '1976-01-30', 'id_genero': 1},
    {'nombre': 'Ana', 'apellido': 'Gimenez', 'fecha_nacimiento': '2001-09-09', 'id_genero': 2},
    {'nombre': 'Mateo', 'apellido': 'Duarte', 'fecha_nacimiento': '2016-04-12', 'id_genero': 1,
     'nom_madre': 'Rosa Duarte', 'tel_madre': '0981000106', 'educacion': 'ESCOLAR BASICA',
     'colegio': 'Colegio San Jose'},
    {'nombre': 'Valentina', 'apellido': 'Rios', 'fecha_nacimiento': '2013-12-01', 'id_genero': 2,
     'nom_padre': 'Hugo Rios', 'tel_padre': '0981000107', 'educacion': 'ESCOLAR BASICA',
     'colegio': 'Colegio Nacional EMD'},
    {'nombre': 'Ricardo', 'apellido': 'Benitez', 'fecha_nacimiento': '1969-06-18', 'id_genero': 1,
     'tipo_documento': 'RUC', 'ruc': '9000008-1'},
    {'nombre': 'Camila', 'apellido': 'Sosa', 'fecha_nacimiento': '1995-02-25', 'id_genero': 2},
    {'nombre': 'Daniel', 'apellido': 'Martinez', 'fecha_nacimiento': '1988-10-05', 'id_genero': 3},
]


def crear_pacientes(recep):
    ids = []
    for i, p in enumerate(PACIENTES, start=1):
        datos = dict(p, cedula=str(9000000 + i), telefono=f'09810001{i:02d}',
                     observaciones='Paciente de prueba (seed_prueba.py)')
        data = recep.llamar('POST', '/pacientes', f'Paciente {p["nombre"]} {p["apellido"]}', json=datos)
        ids.append(data['id_paciente'] if data else None)
    return ids


# ─── 5. Citas y su estado final ─────────────────────────────────────────────
# C=COMPLETADA, EN=EN_CONSULTA, CONF=CONFIRMADA, AG=AGENDADA, CANC=CANCELADA, AUS=AUSENTE
PLAN_CITAS = [
    ['C', 'C', 'C'], ['C', 'C', 'CONF'], ['C', 'C', 'AG'], ['C', 'EN', 'CONF'], ['C', 'CANC', 'CONF'],
    ['C', 'C', 'AUS'], ['C', 'EN', 'AG'], ['C', 'EN', 'CONF'], ['C', 'AUS', 'AG'], ['C', 'CANC', 'CONF'],
]


def crear_citas(recep, ids_pacientes):
    """Reserva 3 turnos por paciente, alternando especialista y en orden cronológico."""
    slots = {
        esp: recep.llamar('GET', '/citas/slots-disponibles', None,
                          params={'id_especialista': esp, 'id_especialidad': ID_ESPECIALIDAD}) or []
        for esp in (ID_ESPECIALISTA_LAURA, ID_ESPECIALISTA_ADMIN)
    }
    citas = []   # (idx_paciente, nro_sesion, id_cita, estado_objetivo, fecha)
    for idx, id_pac in enumerate(ids_pacientes):
        if not id_pac:
            continue
        esp = ID_ESPECIALISTA_LAURA if idx % 2 == 0 else ID_ESPECIALISTA_ADMIN
        for sesion, estado in enumerate(PLAN_CITAS[idx], start=1):
            if not slots[esp]:
                registrar(f'Cita paciente {idx + 1} sesión {sesion}', False, 'sin turnos disponibles')
                continue
            slot = slots[esp].pop(0)
            data = recep.llamar('POST', '/citas', f'Cita paciente {idx + 1} sesión {sesion} ({slot["slot_inicio"]})', json={
                'id_paciente': id_pac, 'id_slot_agenda': slot['id_slot_agenda'],
                'id_especialidad': ID_ESPECIALIDAD, 'modalidad': 'PRESENCIAL',
                'cita_es_primera_vez': sesion == 1, 'cita_numero_sesion': sesion,
                'motivo': 'Primera consulta' if sesion == 1 else f'Sesión de seguimiento {sesion}',
            })
            if data:
                citas.append((idx, sesion, data['id_cita'], estado, slot['slot_inicio'][:10]))
    return citas


def aplicar_estados_previos(recep, citas):
    """Lleva cada cita al estado previo a la consulta (las de consulta las abre el clínico)."""
    for idx, sesion, id_cita, estado, _ in citas:
        etiqueta = f'Cita {id_cita} (paciente {idx + 1}) →'
        if estado == 'CANC':
            recep.llamar('PATCH', f'/citas/{id_cita}/estado', f'{etiqueta} CANCELADA',
                         json={'cod_estado_nuevo': 'CANCELADA', 'motivo': 'Paciente avisó que no puede asistir'})
            continue
        if estado == 'AG':
            continue
        recep.llamar('PATCH', f'/citas/{id_cita}/estado', f'{etiqueta} CONFIRMADA',
                     json={'cod_estado_nuevo': 'CONFIRMADA'})
        if estado == 'AUS':
            recep.llamar('PATCH', f'/citas/{id_cita}/estado', f'{etiqueta} AUSENTE',
                         json={'cod_estado_nuevo': 'AUSENTE'})


# ─── 6. Consultas (ficha clínica) ───────────────────────────────────────────
def anamnesis(paciente, version):
    # informante admite PACIENTE/MADRE/PADRE/TUTOR/OTRO (chk_anamnesis_informante)
    informante = 'MADRE' if paciente.get('nom_madre') else 'PADRE' if paciente.get('nom_padre') else 'PACIENTE'
    base = {
        'informante': informante,
        'relacion_informante': paciente.get('nom_madre') or paciente.get('nom_padre') or 'El propio paciente',
        'motivo_consulta': 'Ansiedad y dificultad para dormir' if not paciente.get('colegio')
        else 'Dificultades de atención en la escuela',
        'antecedentes_patologicos_familiares': 'Madre con antecedentes de depresión',
        'historia_problema_actual': 'Cuadro de 6 meses de evolución, empeora con el estrés laboral/escolar.',
        'patron_sueno': 'Insomnio de conciliación',
        'impresion_diagnostica': 'Compatible con trastorno de ansiedad',
        'plan_trabajo': 'Terapia cognitivo-conductual semanal',
        'eval_psicologica': True, 'terapia_individual': True,
    }
    if version == 2:
        base.update({
            'historia_problema_actual': base['historia_problema_actual'] + ' En seguimiento: mejora parcial del sueño.',
            'plan_trabajo': 'Continuar TCC; sumar terapia familiar quincenal',
            'terapia_familiar': True,
        })
    return base


def ficha_completa(clin, id_consulta, ids_cat, idx, variante):
    """Registro clínico con distinta profundidad según la variante."""
    diag = ids_cat['diagnosticos']
    clin.llamar('POST', f'/consultas/{id_consulta}/diagnosticos', f'Consulta {id_consulta}: diagnóstico', json={
        'id_diagnostico': diag[idx % len(diag)],
        'registro_tipo': 'DEFINITIVO' if variante >= 2 else 'PRESUNTIVO',
        'registro_gravedad': ['LEVE', 'MODERADO', 'GRAVE'][idx % 3],
    })
    if variante >= 1:
        for k in range(2):
            clin.llamar('POST', f'/consultas/{id_consulta}/signos', f'Consulta {id_consulta}: signo', json={
                'id_signo': ids_cat['signos'][(idx + k) % len(ids_cat['signos'])], 'registro_intensidad': 'MODERADO'})
            clin.llamar('POST', f'/consultas/{id_consulta}/sintomas', f'Consulta {id_consulta}: síntoma', json={
                'id_sintoma': ids_cat['sintomas'][(idx + k) % len(ids_cat['sintomas'])], 'registro_intensidad': 'LEVE'})
        clin.llamar('POST', f'/consultas/{id_consulta}/procedimientos', f'Consulta {id_consulta}: procedimiento', json={
            'id_tipo_procedimiento': ids_cat['tipos-procedimientos'][idx % len(ids_cat['tipos-procedimientos'])],
            'registro_duracion': 50, 'registro_resultado': 'Sin incidencias'})


def atender(clin, citas, ids_cat, ids_pacientes):
    """Abre las consultas y las finaliza (o las deja en atención) con distinta profundidad."""
    consultas = []   # (idx, sesion, id_consulta, fecha) solo finalizadas
    primera_anamnesis = set()
    for n, (idx, sesion, id_cita, estado, fecha) in enumerate(citas):
        if estado not in ('C', 'EN'):
            continue
        data = clin.llamar('POST', f'/citas/{id_cita}/iniciar-consulta', f'Iniciar consulta cita {id_cita}')
        if not data:
            continue
        id_consulta = data['id_consulta']
        paciente = PACIENTES[idx]

        # Anamnesis: una vez por paciente; el paciente 1 tiene una segunda versión
        if idx not in primera_anamnesis:
            clin.llamar('POST', f'/anamnesis/paciente/{ids_pacientes[idx]}', f'Anamnesis v1 paciente {idx + 1}',
                        json=anamnesis(paciente, 1))
            primera_anamnesis.add(idx)
        elif idx == 0 and sesion == 3:
            clin.llamar('POST', f'/anamnesis/paciente/{ids_pacientes[idx]}', 'Anamnesis v2 paciente 1',
                        json=anamnesis(paciente, 2))

        variante = n % 4   # 0: mínima, 1: completa, 2: +receta, 3: +orden
        if variante > 0 or estado == 'EN':
            ficha_completa(clin, id_consulta, ids_cat, idx, variante)
        if variante == 2:
            clin.llamar('POST', f'/consultas/{id_consulta}/recetas', f'Consulta {id_consulta}: receta', json={
                'receta_fecha': fecha, 'receta_validez_dias': 30,
                'receta_indicaciones_generales': 'Tomar con alimentos',
                'detalles': [{'id_medicamento': ID_MEDICAMENTO, 'medicamento_dosis': '1 comprimido',
                              'medicamento_frecuencia': 'Cada 12 horas', 'medicamento_duracion': '5 días',
                              'medicamento_cantidad': 10}],
            })
        if variante == 3:
            clin.llamar('POST', f'/consultas/{id_consulta}/ordenes', f'Consulta {id_consulta}: orden', json={
                'orden_fecha': fecha, 'orden_indicaciones': 'Traer resultados a la próxima sesión',
                'detalles': [{'tipo_orden': 'ESTUDIO', 'id_tipo_estudio': ID_TIPO_ESTUDIO},
                             {'tipo_orden': 'ANALISIS', 'id_tipo_analisis': ID_TIPO_ANALISIS}],
            })

        estado_consulta = 'FINALIZADA' if estado == 'C' else 'EN_ATENCION'
        clin.llamar('PUT', f'/consultas/{id_consulta}', f'Consulta {id_consulta} → {estado_consulta}', json={
            'consulta_fecha': fecha, 'consulta_motivo': 'Primera consulta' if sesion == 1 else f'Seguimiento {sesion}',
            'consulta_estado': estado_consulta,
            'des_consulta': 'Sesión de evaluación' if variante == 0 else 'Sesión terapéutica',
            'consulta_observaciones': 'Paciente colaborador' if variante % 2 else None,
        })
        if estado == 'C':
            consultas.append((idx, sesion, id_consulta, fecha))
    return consultas


# ─── 7. Facturación ─────────────────────────────────────────────────────────
def linea(item, id_consulta, impuesto=IVA10, cantidad=1):
    id_item, descripcion, precio = item
    return {'id_item_servicio': id_item, 'id_tipo_item': ID_TIPO_ITEM_SERVICIO, 'id_consulta': id_consulta,
            'item_descripcion': descripcion, 'item_cantidad': cantidad, 'item_precio_con_iva': precio,
            'id_tipo_impuesto': impuesto}


def cobro(*formas):
    return {'id_caja': ID_CAJA, 'detalles': [dict(id_forma_cobro=f, monto_cobrado=m, **extra) for f, m, extra in formas]}


# Una variante por consulta finalizada (la última queda sin facturar a propósito)
VARIANTES_FACTURA = [
    ('Contado efectivo', CONTADO, [ITEM_CONSULTA], {}, cobro((EFECTIVO, 150000, {}))),
    ('Contado tarjeta de débito', CONTADO, [ITEM_CONSULTA], {}, cobro((TARJETA_DEBITO, 150000, {'numero_tarjeta': '4111'}))),
    ('Contado tarjeta de crédito en 3 cuotas', CONTADO, [ITEM_CONSULTA], {},
     cobro((TARJETA_CREDITO, 150000, {'numero_tarjeta': '5500', 'numero_cuotas': 3}))),
    ('Contado mixto efectivo + transferencia', CONTADO, [ITEM_CONSULTA], {},
     cobro((EFECTIVO, 100000, {}), (TRANSFERENCIA, 50000, {}))),
    ('Contado con 2 ítems (consulta + evaluación)', CONTADO, [ITEM_CONSULTA, ITEM_EVALUACION], {},
     cobro((EFECTIVO, 350000, {}))),
    ('Contado con descuento de 20.000', CONTADO, [ITEM_CONSULTA], {'factura_descuento': 20000},
     cobro((EFECTIVO, 130000, {}))),
    ('Crédito 30 días pendiente', CREDITO, [ITEM_CONSULTA], {}, None),
    ('Crédito con cobro parcial', CREDITO, [ITEM_EVALUACION], {}, None),
    ('Crédito cobrado en 2 pagos', CREDITO, [ITEM_CONSULTA], {}, None),
    ('Contado exento de IVA', CONTADO, [ITEM_CONSULTA], {'exento': True}, cobro((EFECTIVO, 150000, {}))),
    ('Contado luego ANULADA', CONTADO, [ITEM_CONSULTA], {}, cobro((EFECTIVO, 150000, {}))),
    ('Contado con nota de crédito parcial', CONTADO, [ITEM_EVALUACION], {}, cobro((EFECTIVO, 200000, {}))),
    ('Contado con cheque', CONTADO, [ITEM_CONSULTA], {}, cobro((CHEQUE, 150000, {'numero_cheque': '00012345'}))),
    ('Crédito 30 días pendiente (paciente menor)', CREDITO, [ITEM_CONSULTA], {}, None),
]


def cuenta_de_factura(cliente, id_factura):
    cuentas = cliente.llamar('GET', '/cuentas-cobrar', None) or []
    return next((c for c in cuentas if c['id_factura'] == id_factura), None)


def facturar(cajero, admin, consultas, ids_pacientes):
    # El paciente con RUC y los menores van primero en la variante que les corresponde
    orden = sorted(consultas, key=lambda c: (c[0] != 7, c[0] not in (5, 6), c[0], c[1]))
    for (idx, sesion, id_consulta, _), (nombre, condicion, items, extra, cobro_contado) in zip(orden, VARIANTES_FACTURA):
        impuesto = EXENTO if extra.get('exento') else IVA10
        datos = {
            'id_paciente': ids_pacientes[idx], 'id_tipo_comprobante': ID_TIPO_COMPROBANTE,
            'id_condicion_venta': condicion, 'id_timbrado': ID_TIMBRADO,
            'id_punto_expedicion': ID_PUNTO_EXPEDICION, 'id_estado_factura': ID_ESTADO_EMITIDA,
            'id_moneda': ID_MONEDA_PYG, 'fecha_factura': HOY,
            'factura_descuento': extra.get('factura_descuento', 0),
            'observaciones': f'Prueba: {nombre}',
            'detalles': [linea(item, id_consulta, impuesto) for item in items],
        }
        if cobro_contado:
            datos['cobro'] = cobro_contado
        data = cajero.llamar('POST', '/facturas', f'Factura "{nombre}" (paciente {idx + 1})', json=datos)
        if not data:
            continue
        id_factura = data['id_factura']

        if nombre.startswith('Crédito con cobro parcial'):
            cta = cuenta_de_factura(cajero, id_factura)
            if cta:
                cajero.llamar('POST', '/cobranzas', f'Cobro parcial factura {id_factura}', json={
                    'id_cuenta_cobrar': cta['id_cuenta_cobrar'], 'id_factura': id_factura, 'id_caja': ID_CAJA,
                    'detalles': [{'id_forma_cobro': EFECTIVO, 'monto_cobrado': 80000}]})
        elif nombre.startswith('Crédito cobrado en 2 pagos'):
            cta = cuenta_de_factura(cajero, id_factura)
            if cta:
                for monto, forma in ((70000, EFECTIVO), (80000, TRANSFERENCIA)):
                    cajero.llamar('POST', '/cobranzas', f'Pago {monto} factura {id_factura}', json={
                        'id_cuenta_cobrar': cta['id_cuenta_cobrar'], 'id_factura': id_factura, 'id_caja': ID_CAJA,
                        'detalles': [{'id_forma_cobro': forma, 'monto_cobrado': monto}]})
        elif nombre.endswith('ANULADA'):
            admin.llamar('PUT', f'/facturas/{id_factura}/anular', f'Anular factura {id_factura}')
        elif nombre.endswith('nota de crédito parcial'):
            cajero.llamar('POST', '/notas-credito', f'Nota de crédito factura {id_factura}', json={
                'id_factura': id_factura, 'motivo': 'Bonificación parcial de la evaluación',
                'detalles': [{'item_descripcion': 'Bonificación evaluación', 'item_cantidad': 1,
                              'item_precio_unitario': 50000}]})


def main():
    if not ADMIN_PASS:
        sys.exit('Defina SEED_ADMIN_PASS con la contraseña del administrador.')

    admin = Cliente(ADMIN_USER, ADMIN_PASS)
    if admin.llamar('GET', '/pacientes/buscar', None, params={'q': '9000001'}):
        sys.exit('Los datos de prueba ya fueron cargados (existe la cédula 9000001).')

    ids_cat = cargar_catalogos(admin)
    crear_usuarios(admin)
    crear_agenda(admin)

    recep = Cliente('recep2', PASS_USUARIOS_PRUEBA)
    ids_pacientes = crear_pacientes(recep)
    citas = crear_citas(recep, ids_pacientes)
    aplicar_estados_previos(recep, citas)

    consultas = atender(admin, citas, ids_cat, ids_pacientes)   # psicoadmin es ADMINISTRADOR + CLINICO

    cajero = Cliente('cajero1', PASS_USUARIOS_PRUEBA)
    facturar(cajero, admin, consultas, ids_pacientes)

    errores = [i for i in informe if not i[1]]
    print(f'\nPasos: {len(informe)}  OK: {len(informe) - len(errores)}  Errores: {len(errores)}')
    for paso, _, detalle in errores:
        print(f'  - {paso}: {detalle}')


if __name__ == '__main__':
    main()
