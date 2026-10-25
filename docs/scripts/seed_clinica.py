"""
Carga de la clínica de neuropsicología sobre una base limpia (migrations/00 a 18 + configuración).

Dos etapas, porque el primer administrador no puede crearse por la API (todavía no existe):

  base   Cargos, especialidades, funcionarios, especialistas, usuarios y roles. Usa los mismos DAO
         que la aplicación y se ejecuta DENTRO del contenedor de la app:
           docker exec -e PYTHONPATH=/app -e DB_NAME=sysclin_nueva -e DB_NAME_NUEVA=sysclin_nueva syscomcli_app \
             python docs/scripts/seed_clinica.py base
  datos  Pacientes, horarios, cupos y citas por la API HTTP (como seed_prueba.py), con el usuario
         del director. Se ejecuta desde el equipo con la app ya apuntando a la base nueva:
           SEED_ADMIN_PASS='...' python docs/scripts/seed_clinica.py datos

Notas:
- TELÉFONOS: todos son de prueba (0991000xxx) y NO existen. Nunca poner números de formato real (098x, 097x,
  096x...): al crear una cita el sistema programa recordatorios y la tarea los envía por WhatsApp (UltraMsg)
  al teléfono del paciente. El 2026-10-22 se mandaron 3 mensajes a números inventados que eran de personas reales.
- Las cuentas nuevas no llevan correo: así el sistema no envía ningún mail (MFA, recuperación ni
  recordatorios). El correo se configura después, desde el sistema.
- Todas las cuentas usan PASS_USUARIOS; la clave no vence ni obliga a cambiarse (demo).
"""
import os
import re
import sys
from datetime import date

PASS_USUARIOS = 'Prueba2026!'
ID_ROL_ADMIN, ID_ROL_RECEPCION, ID_ROL_CLINICO, ID_ROL_VENTAS = 2, 3, 4, 5
ID_USUARIO_SISTEMA = 1   # manu

CARGOS_NUEVOS = ['DIRECTOR CLINICO', 'NEUROPSICOLOGO', 'FONOAUDIOLOGO', 'PSICOPEDAGOGO']
ESPECIALIDADES_NUEVAS = ['PSICOLOGIA CLINICA', 'NEUROPSICOLOGIA', 'FONOAUDIOLOGIA', 'PSICOPEDAGOGIA']

# (nick, nombre, apellido, cedula, telefono, nacimiento, id_genero, id_estado_civil, id_nivel,
#  ciudad, domicilio, cargo, especialidad, matricula, color, roles [principal primero])
PERSONAL = [
    ('mvillalba', 'Mónica Beatriz', 'Villalba Rojas', '2845117', '0991000001', '1978-04-12', 2, 2, 6,
     'ASUNCION', 'Av. España 1450', 'DIRECTOR CLINICO', 'PSICOLOGIA CLINICA', 'MAT-0001', '#2E86AB',
     [ID_ROL_ADMIN, ID_ROL_CLINICO]),
    ('gferreira', 'Gustavo Daniel', 'Ferreira Cabrera', '3921846', '0991000002', '1985-09-23', 1, 2, 6,
     'LAMBARE', 'Calle Cerro Corá 320', 'NEUROPSICOLOGO', 'NEUROPSICOLOGIA', 'MAT-0002', '#7B4EA3',
     [ID_ROL_CLINICO]),
    ('ncuevas', 'Natalia Andrea', 'Cuevas Benítez', '4318752', '0991000003', '1988-02-07', 2, 1, 5,
     'SAN LORENZO', 'Av. Mcal. Estigarribia 2210', 'FONOAUDIOLOGO', 'FONOAUDIOLOGIA', 'MAT-0003', '#2A9D8F',
     [ID_ROL_CLINICO]),
    ('rsamaniego', 'Rocío Elizabeth', 'Samaniego Giménez', '4876234', '0991000004', '1990-11-30', 2, 1, 5,
     'LUQUE', 'Calle Pettirossi 815', 'PSICOPEDAGOGO', 'PSICOPEDAGOGIA', 'MAT-0004', '#E76F51',
     [ID_ROL_CLINICO]),
    ('sduarte', 'Sofía Raquel', 'Duarte Aquino', '5412968', '0991000005', '1995-06-18', 2, 1, 4,
     'FERNANDO DE LA MORA', 'Calle Tte. Fariña 640', 'RECEPCION', None, None, None,
     [ID_ROL_RECEPCION, ID_ROL_VENTAS]),
]


def etapa_base():
    from app.core.base_dao import BaseDAO
    from app.dao.mantenimiento.personas.funcionario.FuncionarioDao import FuncionarioDao
    from app.dao.auth.user_dao import UsuarioDao

    bd = BaseDAO()
    print('Base:', bd.execute_query('SELECT current_database() AS b')[0]['b'])
    if bd.execute_query("SELECT 1 FROM usuarios WHERE usu_nick = 'mvillalba'"):
        sys.exit('mvillalba ya existe: la etapa base ya se ejecutó.')

    for cargo in CARGOS_NUEVOS:
        bd.execute_query('INSERT INTO cargos (des_cargo, es_clinico, usuario_creacion) VALUES (%s, TRUE, %s)',
                         (cargo, ID_USUARIO_SISTEMA), commit=True)
    for esp in ESPECIALIDADES_NUEVAS:
        bd.execute_query('INSERT INTO especialidades (des_especialidad, usuario_creacion) VALUES (%s, %s)',
                         (esp, ID_USUARIO_SISTEMA), commit=True)

    cargos = {f['des_cargo']: f['id_cargo'] for f in bd.execute_query('SELECT id_cargo, des_cargo FROM cargos')}
    espec = {f['des_especialidad']: f['id_especialidad']
             for f in bd.execute_query('SELECT id_especialidad, des_especialidad FROM especialidades')}
    ciudades = {f['des_ciudad']: f['id_ciudad'] for f in bd.execute_query('SELECT id_ciudad, des_ciudad FROM ciudades')}

    funcionarios, usuarios = FuncionarioDao(), UsuarioDao()
    for (nick, nombre, apellido, cedula, tel, nac, gen, civil, nivel, ciudad, domicilio,
         cargo, especialidad, matricula, color, roles) in PERSONAL:
        id_func = funcionarios.guardarFuncionario(
            nombre=nombre, apellido=apellido, cedula=cedula, fecha_nacimiento=nac, genero_id=gen,
            estado_civil_id=civil, telefono=tel, correo=None, domicilio=domicilio,
            ciudad_id=ciudades[ciudad], ciudad_nacimiento_id=ciudades['ASUNCION'],
            nivel_instruccion_id=nivel, profesion_id=None, id_cargo=cargos[cargo],
            usuario_creacion=ID_USUARIO_SISTEMA, esp_matricula=matricula,
            especialidades=[espec[especialidad]] if especialidad else None,
            esp_color_agenda=color or '#3498db')
        id_usuario = usuarios.guardarUsuario(nick, PASS_USUARIOS, id_func, roles[0],
                                             usuario_creacion=ID_USUARIO_SISTEMA, requiere_cambio_clave=False)
        for id_rol in roles[1:]:
            usuarios.asignar_rol_usuario(id_usuario, id_rol, es_principal=False,
                                         usuario_creacion=ID_USUARIO_SISTEMA)
        print(f'[OK ] {nick}: funcionario {id_func}, usuario {id_usuario}, roles {roles}')


# ─── Etapa datos: horarios, pacientes y citas por la API ────────────────────
BASE = os.getenv('SEED_BASE_URL', 'http://localhost:5005')
API = BASE + '/api/v1'
HOY = date.today().isoformat()
ID_SEDE = 1
informe = []   # (paso, ok, detalle)

# especialista (nick) -> (consultorio, [(id_dia_semana, hora_inicio, hora_fin, modalidad)]).
# Turnos de 60 min, dentro del horario de la clínica.
HORARIOS = {
    'mvillalba':  (1, [(1, '11:00', '17:00', 'PRESENCIAL'), (2, '09:00', '14:00', 'PRESENCIAL'),
                       (4, '14:00', '20:00', 'PRESENCIAL'), (6, '08:00', '12:00', 'PRESENCIAL')]),
    'gferreira':  (2, [(2, '09:00', '17:00', 'PRESENCIAL'), (3, '11:00', '19:00', 'PRESENCIAL'),
                       (5, '11:00', '15:00', 'PRESENCIAL'), (5, '15:00', '19:00', 'TELEMEDICINA')]),
    'ncuevas':    (3, [(1, '11:00', '19:00', 'PRESENCIAL'), (4, '09:00', '17:00', 'PRESENCIAL'),
                       (6, '09:00', '14:00', 'PRESENCIAL')]),
    'rsamaniego': (4, [(2, '10:00', '18:00', 'PRESENCIAL'), (3, '11:00', '19:00', 'PRESENCIAL'),
                       (6, '08:00', '17:00', 'PRESENCIAL')]),
}

# (nombre, apellido, cedula, nacimiento, id_genero, ciudad, domicilio, telefono, motivo, especialista, extra)
PACIENTES = [
    ('Carlos Alberto', 'Benítez Duarte', '6102845', '1982-03-14', 1, 'ASUNCION', 'Calle Palma 720', '0991000006',
     'Ansiedad y estrés laboral', 'mvillalba', {}),
    ('Liz Verónica', 'Ortigoza Salinas', '6254317', '1991-08-02', 2, 'SAN LORENZO', 'Barrio Industrial 118',
     '0991000007', 'Síntomas depresivos persistentes', 'mvillalba', {}),
    ('Hugo Ramón', 'Escobar Vera', '6387529', '1958-11-21', 1, 'LAMBARE', 'Av. Cacique Lambaré 905', '0991000008',
     'Evaluación neuropsicológica por olvidos frecuentes', 'gferreira', {}),
    ('Patricia Noemí', 'Ayala Franco', '6490163', '1974-05-09', 2, 'LUQUE', 'Calle Cap. Figari 233', '0991000009',
     'Rehabilitación cognitiva posterior a un ACV', 'gferreira', {}),
    ('Fabián Andrés', 'Román Cardozo', '6571480', '1989-01-27', 1, 'FERNANDO DE LA MORA',
     'Calle Defensores del Chaco 410', '0991000010', 'Disfluencia del habla (tartamudez)', 'ncuevas', {}),
    ('Gladys Mabel', 'Rolón Martínez', '6623905', '1969-09-16', 2, 'ASUNCION', 'Calle Eligio Ayala 1560',
     '0991000011', 'Alteración de la voz (disfonía)', 'ncuevas', {}),
    ('Jessica Paola', 'Cáceres Lezcano', '6738214', '1999-12-04', 2, 'SAN LORENZO', 'Calle 14 de Mayo 87',
     '0991000012', 'Dificultades de aprendizaje en estudios universitarios', 'rsamaniego', {}),
    ('Mateo Joaquín', 'Insfrán Barrios', '6845702', '2016-04-12', 1, 'LAMBARE', 'Calle Jejuí 342', '0991000013',
     'Evaluación por sospecha de trastorno del espectro autista', 'gferreira',
     {'nom_madre': 'Rosa Barrios', 'tel_madre': '0991010008', 'educacion': 'ESCOLAR BASICA',
      'colegio': 'Colegio San José'}),
    ('Valentina Sofía', 'Giménez Amarilla', '6956038', '2018-07-30', 2, 'LUQUE', 'Calle Mcal. López 129',
     '0991000014', 'Retraso en el desarrollo del lenguaje', 'ncuevas',
     {'nom_madre': 'Andrea Amarilla', 'tel_madre': '0991010009', 'educacion': 'PREESCOLAR',
      'colegio': 'Jardín Los Pitufos'}),
    ('Thiago Emanuel', 'Ortiz Paredes', '7064917', '2015-10-05', 1, 'FERNANDO DE LA MORA', 'Calle Mburicaó 56',
     '0991000015', 'Dificultades de aprendizaje y atención en la escuela', 'rsamaniego',
     {'nom_padre': 'Rubén Ortiz', 'tel_padre': '0991020010', 'educacion': 'ESCOLAR BASICA',
      'colegio': 'Colegio Nacional EMD'}),
]

# Estado objetivo de cada cita, por paciente (la 1ª es primera vez): AG=Agendada, CONF=Confirmada, CANC=Cancelada
PLAN_CITAS = [['CONF', 'AG'], ['AG'], ['CONF', 'AG'], ['CONF'], ['AG', 'AG'],
              ['CONF'], ['AG'], ['CONF', 'AG'], ['CONF'], ['AG', 'CANC']]


def registrar(paso, ok, detalle=''):
    informe.append((paso, ok, detalle))
    print(f"[{'OK ' if ok else 'ERR'}] {paso}" + (f" -> {detalle}" if detalle else ''))


class Cliente:
    """Sesión HTTP autenticada con CSRF, como la usa el navegador."""

    def __init__(self, usuario, clave):
        import requests
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
        r = self.s.request(metodo, API + ruta, json=json, params=params, headers={'X-CSRFToken': self.csrf})
        try:
            cuerpo = r.json()
        except ValueError:
            cuerpo = {'success': False, 'error': f'HTTP {r.status_code} sin JSON'}
        ok = r.ok and cuerpo.get('success', True)
        if paso:
            registrar(f'{paso} [{self.usuario}]', ok, '' if ok else cuerpo.get('error') or f'HTTP {r.status_code}')
        return cuerpo.get('data') if ok else None


def etapa_datos():
    clave = os.getenv('SEED_ADMIN_PASS', PASS_USUARIOS)
    admin, recep = Cliente('mvillalba', clave), Cliente('sduarte', clave)

    esp_de = {}   # nick -> id_especialista (por la cédula del funcionario)
    for e in admin.llamar('GET', '/funcionarios/especialistas', None) or []:
        for u in PERSONAL:
            if str(e.get('cedula') or e.get('per_cedula')) == u[3]:
                esp_de[u[0]] = e['id_especialista']
    if not all(n in esp_de for n in HORARIOS):
        sys.exit(f'No se encontraron todos los especialistas: {esp_de}')
    espec = {e['des_especialidad']: e['id_especialidad'] for e in recep.llamar('GET', '/especialidades', None) or []}
    id_espec = {u[0]: espec.get(u[12]) for u in PERSONAL if u[12]}
    ciudades = {c['descripcion']: c['id'] for c in recep.llamar('GET', '/ciudades', None) or []}

    for nick, (consultorio, tramos) in HORARIOS.items():
        for dia, ini, fin, modalidad in tramos:
            admin.llamar('POST', '/agenda-horarios', f'Horario {nick} día {dia} {ini}-{fin} {modalidad}', json={
                'id_especialista': esp_de[nick], 'id_sede': ID_SEDE, 'id_consultorio': consultorio,
                'id_dia_semana': dia, 'hora_inicio': ini, 'hora_fin': fin, 'duracion_turno_min': 60,
                'modalidad_default': modalidad, 'fec_desde': HOY,
            })

    ids = []
    for (nombre, apellido, cedula, nac, gen, ciudad, dom, tel, motivo, esp, extra) in PACIENTES:
        datos = dict(extra, nombre=nombre, apellido=apellido, cedula=cedula, fecha_nacimiento=nac,
                     id_genero=gen, telefono=tel, domicilio=dom, id_ciudad=ciudades.get(ciudad),
                     observaciones=f'Paciente de prueba. Motivo: {motivo}')
        data = recep.llamar('POST', '/pacientes', f'Paciente {nombre} {apellido}', json=datos)
        ids.append(data['id_paciente'] if data else None)

    slots = {nick: recep.llamar('GET', '/citas/slots-disponibles', None,
                                params={'id_especialista': esp_de[nick], 'id_especialidad': id_espec[nick]}) or []
             for nick in HORARIOS}
    for idx, (pac, plan) in enumerate(zip(PACIENTES, PLAN_CITAS)):
        nick, id_pac = pac[9], ids[idx]
        if not id_pac:
            continue
        for sesion, estado in enumerate(plan, start=1):
            if len(slots[nick]) < 3:
                registrar(f'Cita {pac[0]} sesión {sesion}', False, 'sin turnos disponibles')
                continue
            slot = slots[nick].pop(idx % 3)   # salta turnos para no ocupar siempre el primero
            data = recep.llamar('POST', '/citas', f'Cita {pac[0]} sesión {sesion} ({slot["slot_inicio"]})', json={
                'id_paciente': id_pac, 'id_slot_agenda': slot['id_slot_agenda'],
                'id_especialidad': id_espec[nick], 'modalidad': 'PRESENCIAL',
                'cita_es_primera_vez': sesion == 1, 'cita_numero_sesion': sesion,
                'motivo': pac[8] if sesion == 1 else f'Sesión de seguimiento {sesion}',
            })
            if data and estado == 'CONF':
                recep.llamar('PATCH', f'/citas/{data["id_cita"]}/estado', f'  CONFIRMADA cita {data["id_cita"]}',
                             json={'cod_estado_nuevo': 'CONFIRMADA'})
            elif data and estado == 'CANC':
                recep.llamar('PATCH', f'/citas/{data["id_cita"]}/estado', f'  CANCELADA cita {data["id_cita"]}',
                             json={'cod_estado_nuevo': 'CANCELADA', 'motivo': 'Paciente avisó que no puede asistir'})

    fallos = [i for i in informe if not i[1]]
    print(f'\n{len(informe) - len(fallos)} pasos OK, {len(fallos)} con error')


# ─── Etapa circuito: consultas, caja, facturas y cobros (sobre las citas ya creadas) ───
# No crea citas nuevas (cada cita nueva programa recordatorios por WhatsApp). Usa las citas CONFIRMADAS de la etapa datos.
ID_CAJA, ID_MONEDA_PYG = 1, 1
ID_TIPO_COMPROBANTE, CONTADO, CREDITO = 2, 1, 2
ID_TIMBRADO, ID_PUNTO_EXPEDICION, ID_ESTADO_EMITIDA = 1, 1, 1
IVA10, ID_TIPO_ITEM_SERVICIO = 4, 1
EFECTIVO, TARJETA_DEBITO, TRANSFERENCIA = 1, 4, 5
# (id_item_servicio, descripción, precio con IVA) — ids de los ítems cargados con la configuración de la clínica
ITEM_CONSULTA = (1, 'CONSULTA PSICOLOGICA', 150000)
ITEM_SESION_NEURO = (3, 'SESION DE NEUROPSICOLOGIA', 180000)
ITEM_SESION_FONO = (4, 'SESION DE FONOAUDIOLOGIA', 120000)
ITEM_EVAL_NEURO = (6, 'EVALUACION NEUROPSICOLOGICA', 450000)
ITEM_EVAL_LENGUAJE = (7, 'EVALUACION DEL LENGUAJE', 300000)
ID_DIAGNOSTICOS = {3: 'ansiedad', 4: 'depresión', 5: 'atención', 6: 'lectura', 7: 'adaptación'}
ID_MEDICAMENTO_SERTRALINA = 7
ID_TIPO_ESTUDIO_EVAL_NEURO, ID_TIPO_ANALISIS_HEMOGRAMA = 6, 4

# (id_cita, especialista, diagnóstico, estado final de la consulta, agregados). Una consulta solo se abre el día de
# su cita, así que se atiende a quien tiene cita HOY (Carlos Benítez, citas 1 y 2); las demás citas son de días
# futuros y se atienden en vivo ese día.
CONSULTAS = [
    (1, 'mvillalba', 3, 'FINALIZADA', 'receta+orden'),
    (2, 'mvillalba', 3, 'EN_ATENCION', 'orden'),  # queda abierta, sin facturar
]


def cobro(*formas):
    return {'id_caja': ID_CAJA, 'detalles': [dict(id_forma_cobro=f, monto_cobrado=m, **extra) for f, m, extra in formas]}


def linea(item, id_consulta):
    id_item, descripcion, precio = item
    fila = {'id_item_servicio': id_item, 'id_tipo_item': ID_TIPO_ITEM_SERVICIO,
            'item_descripcion': descripcion, 'item_cantidad': 1, 'item_precio_con_iva': precio,
            'id_tipo_impuesto': IVA10}
    if id_consulta:
        fila['id_consulta'] = id_consulta
    return fila


def atender_consultas(clinicos, recep, lista):
    """Abre y completa las consultas de `lista` (ver CONSULTAS). Devuelve {id_cita: (id_consulta, id_paciente)}
    de las finalizadas. Una cita ya atendida no se vuelve a abrir."""
    consultas = {}   # id_cita -> (id_consulta, id_paciente)

    for id_cita, nick, id_diag, estado, extra in lista:
        clin = clinicos[nick]
        cita = recep.llamar('GET', f'/citas/{id_cita}', None) or {}   # el clínico no puede leer la cita; recepción sí
        if cita.get('cod_estado_cita') in ('EN_CONSULTA', 'COMPLETADA'):
            registrar(f'Cita {id_cita} ya atendida: se omite', True)
            continue
        if cita.get('cod_estado_cita') == 'AGENDADA':
            recep.llamar('PATCH', f'/citas/{id_cita}/estado', f'Confirmar cita {id_cita}', json={'cod_estado_nuevo': 'CONFIRMADA'})
        id_pac = cita.get('id_paciente')
        data = clin.llamar('POST', f'/citas/{id_cita}/iniciar-consulta', f'Iniciar consulta cita {id_cita}')
        if not data or not id_pac:
            continue
        id_consulta = data['id_consulta']
        if not clin.llamar('GET', f'/anamnesis/paciente/{id_pac}', None):
            clin.llamar('POST', f'/anamnesis/paciente/{id_pac}', f'Anamnesis paciente {id_pac}', json={
                'informante': 'PACIENTE', 'relacion_informante': 'El propio paciente',
                'motivo_consulta': cita.get('cita_motivo') or 'Consulta inicial',
                'historia_problema_actual': 'Cuadro de varios meses de evolución, con impacto en la vida diaria.',
                'impresion_diagnostica': 'A confirmar con la evaluación', 'plan_trabajo': 'Sesiones semanales',
                'eval_psicologica': True, 'terapia_individual': True})
        clin.llamar('POST', f'/consultas/{id_consulta}/diagnosticos', f'Consulta {id_consulta}: diagnóstico', json={
            'id_diagnostico': id_diag, 'registro_tipo': 'PRESUNTIVO', 'registro_gravedad': 'MODERADO'})
        if extra and 'receta' in extra:
            clin.llamar('POST', f'/consultas/{id_consulta}/recetas', f'Consulta {id_consulta}: receta', json={
                'receta_fecha': HOY, 'receta_validez_dias': 30,
                'receta_indicaciones_generales': 'Tomar con alimentos',
                'detalles': [{'id_medicamento': ID_MEDICAMENTO_SERTRALINA, 'medicamento_dosis': '1 comprimido',
                              'medicamento_frecuencia': 'Cada 24 horas', 'medicamento_duracion': '30 días',
                              'medicamento_cantidad': 30}]})
        if extra and 'orden' in extra:
            clin.llamar('POST', f'/consultas/{id_consulta}/ordenes', f'Consulta {id_consulta}: orden', json={
                'orden_fecha': HOY, 'orden_indicaciones': 'Traer los resultados a la próxima sesión',
                'detalles': [{'tipo_orden': 'ESTUDIO', 'id_tipo_estudio': ID_TIPO_ESTUDIO_EVAL_NEURO},
                             {'tipo_orden': 'ANALISIS', 'id_tipo_analisis': ID_TIPO_ANALISIS_HEMOGRAMA}]})
        clin.llamar('PUT', f'/consultas/{id_consulta}', f'Consulta {id_consulta} → {estado}', json={
            'consulta_fecha': HOY, 'consulta_motivo': cita.get('cita_motivo') or 'Consulta inicial',
            'consulta_estado': estado, 'des_consulta': 'Sesión de evaluación inicial'})
        if estado == 'FINALIZADA':
            consultas[id_cita] = (id_consulta, id_pac)
    return consultas


def etapa_circuito():
    clave = os.getenv('SEED_ADMIN_PASS', PASS_USUARIOS)
    clinicos = {n: Cliente(n, clave) for n in ('mvillalba', 'gferreira', 'ncuevas')}
    recep = Cliente('sduarte', clave)
    consultas = atender_consultas(clinicos, recep, CONSULTAS)

    # Caja abierta por recepción/ventas
    if not recep.llamar('GET', f'/cajas/{ID_CAJA}/apertura-activa', None):
        recep.llamar('POST', '/apertura-caja', 'Apertura de CAJA01', json={
            'id_caja': ID_CAJA, 'id_moneda': ID_MONEDA_PYG, 'saldo_inicial': 200000,
            'observaciones': 'Apertura de la jornada'})

    # (id_cita, descripción, condición, ítem, cobro al contado o None, cobros posteriores de una cuenta a crédito)
    FACTURAS = [
        (1, 'Contado efectivo', CONTADO, ITEM_CONSULTA, cobro((EFECTIVO, 150000, {})), []),
        (4, 'Contado tarjeta de débito', CONTADO, ITEM_EVAL_NEURO,
         cobro((TARJETA_DEBITO, 450000, {'numero_tarjeta': '4111'})), []),
        (6, 'Crédito con cobro parcial', CREDITO, ITEM_SESION_NEURO, None, [(80000, EFECTIVO)]),
        (9, 'Contado mixto efectivo + transferencia', CONTADO, ITEM_SESION_FONO,
         cobro((EFECTIVO, 70000, {}), (TRANSFERENCIA, 50000, {})), []),
        (13, 'Crédito 30 días pendiente', CREDITO, ITEM_EVAL_LENGUAJE, None, []),
    ]
    for id_cita, nombre, condicion, item, cobro_contado, pagos in FACTURAS:
        id_consulta, id_pac = consultas.get(id_cita, (None, None))
        if id_cita == 1 and not id_pac:
            continue   # la factura de Carlos ya se hizo en una corrida anterior (no duplicar)
        if not id_pac:   # paciente sin consulta todavía (la cita es de un día futuro)
            id_pac = (recep.llamar('GET', f'/citas/{id_cita}', None) or {}).get('id_paciente')
        if not id_pac:
            continue
        datos = {'id_paciente': id_pac, 'id_tipo_comprobante': ID_TIPO_COMPROBANTE, 'id_condicion_venta': condicion,
                 'id_timbrado': ID_TIMBRADO, 'id_punto_expedicion': ID_PUNTO_EXPEDICION,
                 'id_estado_factura': ID_ESTADO_EMITIDA, 'id_moneda': ID_MONEDA_PYG, 'fecha_factura': HOY,
                 'factura_descuento': 0, 'observaciones': f'Prueba: {nombre}',
                 'detalles': [linea(item, id_consulta)]}
        if cobro_contado:
            datos['cobro'] = cobro_contado
        data = recep.llamar('POST', '/facturas', f'Factura "{nombre}" (cita {id_cita})', json=datos)
        if not data or not pagos:
            continue
        cuentas = recep.llamar('GET', '/cuentas-cobrar', None) or []
        cta = next((c for c in cuentas if c['id_factura'] == data['id_factura']), None)
        for monto, forma in pagos if cta else []:
            recep.llamar('POST', '/cobranzas', f'Cobro {monto} factura {data["id_factura"]}', json={
                'id_cuenta_cobrar': cta['id_cuenta_cobrar'], 'id_factura': data['id_factura'], 'id_caja': ID_CAJA,
                'detalles': [{'id_forma_cobro': forma, 'monto_cobrado': monto}]})

    fallos = [i for i in informe if not i[1]]
    print(f'\n{len(informe) - len(fallos)} pasos OK, {len(fallos)} con error')
    for paso, _, detalle in fallos:
        print(f'  - {paso}: {detalle}')


if __name__ == '__main__':
    etapa = sys.argv[1] if len(sys.argv) > 1 else ''
    if etapa == 'base':
        etapa_base()
    elif etapa == 'datos':
        etapa_datos()
    elif etapa == 'circuito':
        etapa_circuito()
    else:
        sys.exit(__doc__)
