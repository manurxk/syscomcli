"""
RecurrenceService — Generación masiva de citas para planes de tratamiento.

Fase 2 — Mejoras de robustez:
  - simular_citas():   valida conflictos SIN persistir datos (simulación pura).
  - confirmar_citas(): llama a simular_citas() primero; si hay conflictos lanza
    ConflictoCitas. Toda la inserción ocurre en una única transacción SQL
    con rollback total si cualquier cita individual falla.
  - registrar_plan():  alias de confirmar_citas() para compatibilidad con la API.
"""
from datetime import datetime, date, timedelta
from enum import Enum
import calendar
from typing import List, Dict, Any, Optional

from app.dao.referenciales.agendamiento.feriado.FeriadoDao import FeriadoDao
from app.dao.modulos.agendamiento.agenda_medica.Agenda_MedicaDao import AgendaDao as AgendaMedicaDao
from app.dao.modulos.agendamiento.cita.CitaDao import CitaDao
from app.conexion.Conexion import Conexion
from flask import current_app as app


# ---------------------------------------------------------------------------
# Constantes de estado (sin hardcodear strings dispersos)
# ---------------------------------------------------------------------------

class EstadoPresupuesto(str, Enum):
    """Estados válidos del ciclo de vida de un presupuesto."""
    PENDIENTE         = 'PENDIENTE'
    APROBADO          = 'APROBADO'
    RECHAZADO         = 'RECHAZADO'
    VENCIDO           = 'VENCIDO'
    FACTURADO_PARCIAL = 'FACTURADO_PARCIAL'
    FACTURADO         = 'FACTURADO'


# ---------------------------------------------------------------------------
# Excepciones tipadas
# ---------------------------------------------------------------------------

class ConflictoCitas(Exception):
    """Se lanza cuando confirmar_citas() detecta conflictos de agenda en el plan.

    Atributos:
        conflictos (list): Lista de dicts con 'fecha', 'hora_inicio',
                           'hora_fin' y 'motivo' de cada conflicto detectado.
    """
    def __init__(self, conflictos: List[Dict[str, Any]]):
        self.conflictos = conflictos
        super().__init__(
            f"{len(conflictos)} conflicto(s) detectado(s). "
            "Revisá el atributo 'conflictos' para el detalle."
        )


# ---------------------------------------------------------------------------
# Servicio
# ---------------------------------------------------------------------------

class RecurrenceService:
    def __init__(self):
        self.feriado_dao = FeriadoDao()
        self.agenda_dao  = AgendaMedicaDao()
        self.cita_dao    = CitaDao()
        # Cache de feriados para la sesión actual
        self.feriados_cache: List[str] = [
            f['fecha_feriado']
            for f in self.feriado_dao.getFeriados()
            if f['est_feriado']
        ]

    # -----------------------------------------------------------------------
    # Helpers de validación
    # -----------------------------------------------------------------------

    def es_feriado(self, fecha: date) -> bool:
        """Verifica si una fecha es feriado."""
        fecha_str = fecha.strftime('%Y-%m-%d') if isinstance(fecha, date) else fecha
        return fecha_str in self.feriados_cache

    def es_dia_laborable(self, id_especialista: int, fecha: date,
                         hora_inicio: str, hora_fin: str):
        """
        Verifica si el especialista trabaja en ese día/horario según su
        agenda_medica configurada.

        Returns:
            (True, id_agenda_horario) si el horario es válido.
            (False, mensaje_error)    si no lo es.
        """
        dia_semana = fecha.weekday()
        try:
            agendas = self.agenda_dao.getAgendaByEspecialista(id_especialista)
            if not agendas:
                return False, "Especialista sin agenda configurada."

            dia_bd = str(dia_semana + 1)

            for agenda in agendas:
                if str(agenda.get('dia_semana_id', '')) == dia_bd:
                    ag_ini = (
                        datetime.strptime(str(agenda['horario_inicio']), '%H:%M:%S').time()
                        if len(str(agenda['horario_inicio'])) > 5
                        else datetime.strptime(str(agenda['horario_inicio']), '%H:%M').time()
                    )
                    ag_fin = (
                        datetime.strptime(str(agenda['horario_fin']), '%H:%M:%S').time()
                        if len(str(agenda['horario_fin'])) > 5
                        else datetime.strptime(str(agenda['horario_fin']), '%H:%M').time()
                    )
                    req_ini = (
                        datetime.strptime(hora_inicio, '%H:%M').time()
                        if isinstance(hora_inicio, str) else hora_inicio
                    )
                    req_fin = (
                        datetime.strptime(hora_fin, '%H:%M').time()
                        if isinstance(hora_fin, str) else hora_fin
                    )

                    if req_ini >= ag_ini and req_fin <= ag_fin:
                        duracion = agenda.get('duracion_turno') or 60
                        delta = (
                            req_ini.hour * 60 + req_ini.minute
                        ) - (ag_ini.hour * 60 + ag_ini.minute)
                        if delta % duracion == 0:
                            return True, agenda['id_agenda_horario']
                        else:
                            return False, (
                                f"La hora {hora_inicio} no coincide con los "
                                f"bloques de {duracion} min."
                            )

            return False, "Horario fuera de jornada o el especialista no trabaja este día."

        except Exception as e:
            app.logger.error(f"Error al verificar día laborable: {str(e)}")
            return False, "Error al verificar agenda."

    def hay_solapamiento(self, id_especialista: int, id_paciente: int,
                         fecha: date, hora_inicio: str, hora_fin: str):
        """
        Detecta solapamiento con citas existentes (por especialista y por paciente).

        Returns:
            (True, motivo) si hay solapamiento.
            (False, "Disponible") si está libre.
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()

            overlap_sql = """
                SELECT COUNT(*)
                FROM citas
                WHERE {col} = %s
                  AND cita_fecha = %s
                  AND cita_activo = TRUE
                  AND id_estado_cita != (
                      SELECT id_estado_cita FROM estados_citas
                      WHERE est_cita_nombre = 'CANCELADA'
                  )
                  AND (
                      (cita_hora_inicio < %s AND cita_hora_fin > %s) OR
                      (cita_hora_inicio >= %s AND cita_hora_inicio < %s) OR
                      (cita_hora_fin > %s AND cita_hora_fin <= %s)
                  )
            """
            params = (
                fecha,
                hora_inicio, hora_fin,
                hora_inicio, hora_fin,
                hora_inicio, hora_fin
            )

            cur.execute(overlap_sql.format(col='id_especialista'),
                        (id_especialista,) + params)
            if cur.fetchone()[0] > 0:
                cur.close(); con.close()
                return True, "Solapamiento con otra cita del especialista"

            cur.execute(overlap_sql.format(col='id_paciente'),
                        (id_paciente,) + params)
            if cur.fetchone()[0] > 0:
                cur.close(); con.close()
                return True, "El paciente ya tiene otra cita en este horario"

            cur.close(); con.close()
            return False, "Disponible"

        except Exception as e:
            app.logger.error(f"Error al verificar solapamiento: {str(e)}")
            return True, "Error de validación"

    def avanzar_fecha(self, fecha_actual: date, frecuencia: str,
                      dias_intervalo: int = 1) -> date:
        """Calcula la siguiente fecha según la frecuencia del plan."""
        if frecuencia == 'DIARIO':
            return fecha_actual + timedelta(days=1)
        elif frecuencia == 'SEMANAL':
            return fecha_actual + timedelta(weeks=1)
        elif frecuencia == 'QUINCENAL':
            return fecha_actual + timedelta(weeks=2)
        elif frecuencia == 'MENSUAL':
            month = fecha_actual.month
            year  = fecha_actual.year + (month // 12)
            month = month % 12 + 1
            day   = min(fecha_actual.day, calendar.monthrange(year, month)[1])
            return date(year, month, day)
        elif frecuencia == 'PERSONALIZADO':
            return fecha_actual + timedelta(days=dias_intervalo)
        else:
            return fecha_actual + timedelta(weeks=1)

    # -----------------------------------------------------------------------
    # Simulación pura — FASE 2
    # -----------------------------------------------------------------------

    def simular_plan(self, id_especialista: int, id_paciente: int,
                     fecha_inicio, hora_inicio: str, hora_fin: str,
                     cantidad_sesiones: int, frecuencia: str,
                     dias_intervalo: int = 1) -> Dict[str, Any]:
        """
        Proyecta el plan completo de citas respetando feriados, agenda y
        solapamientos. NO persiste datos.

        Returns::
            {
                "success": bool,
                "error": str | None,
                "sesiones": list,          # Cada sesión incluye campo 'conflicto'
                "con_conflictos": bool
            }
        """
        sesiones: List[Dict] = []
        fecha_actual = (
            datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            if isinstance(fecha_inicio, str) else fecha_inicio
        )
        sesiones_generadas = 0
        iteraciones_maximas = cantidad_sesiones * 15
        iteracion = 0
        dias_semana = ["Lunes", "Martes", "Miércoles", "Jueves",
                       "Viernes", "Sábado", "Domingo"]

        while sesiones_generadas < cantidad_sesiones and iteracion < iteraciones_maximas:
            iteracion += 1

            if self.es_feriado(fecha_actual):
                fecha_actual += timedelta(days=1)
                continue

            trabaja, agenda_info = self.es_dia_laborable(
                id_especialista, fecha_actual, hora_inicio, hora_fin
            )
            if not trabaja:
                fecha_actual += timedelta(days=1)
                continue

            solapado, motivo = self.hay_solapamiento(
                id_especialista, id_paciente, fecha_actual, hora_inicio, hora_fin
            )
            id_agenda_horario = agenda_info if isinstance(agenda_info, int) else None

            sesiones.append({
                'numero_sesion':     sesiones_generadas + 1,
                'fecha':             fecha_actual.strftime('%Y-%m-%d'),
                'dia_nombre':        dias_semana[fecha_actual.weekday()],
                'hora_inicio':       hora_inicio,
                'hora_fin':          hora_fin,
                'id_agenda_horario': id_agenda_horario,
                'conflicto':         solapado,
                'motivo_conflicto':  motivo if solapado else "Sin conflicto"
            })

            sesiones_generadas += 1
            fecha_actual = self.avanzar_fecha(fecha_actual, frecuencia, dias_intervalo)

        if sesiones_generadas < cantidad_sesiones:
            return {
                'success': False,
                'error': "No se pudieron generar todas las sesiones (demasiados conflictos).",
                'sesiones': sesiones,
                'con_conflictos': True
            }

        return {
            'success': True,
            'error': None,
            'sesiones': sesiones,
            'con_conflictos': any(s['conflicto'] for s in sesiones)
        }

    def simular_citas(self, id_especialista: int, id_paciente: int,
                      fecha_inicio, hora_inicio: str, hora_fin: str,
                      cantidad_sesiones: int, frecuencia: str,
                      dias_intervalo: int = 1) -> Dict[str, Any]:
        """
        Validación pura de conflictos de agenda. NO persiste ningún dato.

        Diseñado para ser llamado ANTES de confirmar_citas(), de modo que el
        usuario pueda revisar y corregir fechas conflictivas.

        Returns::
            {
                "tiene_conflictos": bool,
                "conflictos": [
                    {"fecha": "...", "hora_inicio": "...",
                     "hora_fin": "...", "motivo": "..."}
                ]
            }
        """
        resultado = self.simular_plan(
            id_especialista, id_paciente, fecha_inicio,
            hora_inicio, hora_fin, cantidad_sesiones, frecuencia, dias_intervalo
        )
        conflictos = [
            {
                'fecha':       s['fecha'],
                'hora_inicio': s['hora_inicio'],
                'hora_fin':    s['hora_fin'],
                'motivo':      s['motivo_conflicto']
            }
            for s in resultado.get('sesiones', [])
            if s['conflicto']
        ]
        return {
            'tiene_conflictos': bool(conflictos) or not resultado['success'],
            'conflictos': conflictos
        }

    # -----------------------------------------------------------------------
    # Confirmación transaccional — FASE 2
    # -----------------------------------------------------------------------

    def confirmar_citas(self, id_especialista: int, id_paciente: int,
                        id_presupuesto: int, plan_sesiones: List[Dict],
                        id_especialidad: Optional[int] = None,
                        id_usuario: int = 1) -> Dict[str, Any]:
        """
        Registra todas las citas del plan en una única transacción SQL.

        Comportamiento:
          1. Verifica que ninguna sesión tenga 'conflicto': True.
             Si hay conflictos → lanza ``ConflictoCitas`` (no persiste nada).
          2. Abre una conexión y ejecuta todos los INSERT dentro de la misma
             transacción.
          3. Si cualquier INSERT falla → ROLLBACK completo (ninguna cita queda).
          4. Solo hace COMMIT si todos los INSERT son exitosos.

        Args:
            id_especialista: ID del especialista que atenderá.
            id_paciente:     ID del paciente.
            id_presupuesto:  ID del presupuesto origen del plan.
            plan_sesiones:   Lista de sesiones del plan (output de simular_plan).
            id_especialidad: Opcional; se resuelve automáticamente si no se pasa.
            id_usuario:      ID del usuario que confirma.

        Raises:
            ConflictoCitas: si alguna sesión tiene 'conflicto': True.

        Returns:
            {"success": bool, "citas_ids": list, "errores": list}
        """
        # 1. Verificar conflictos en el plan
        conflictos_en_plan = [
            {
                'fecha':       s['fecha'],
                'hora_inicio': s.get('hora_inicio'),
                'hora_fin':    s.get('hora_fin'),
                'motivo':      s.get('motivo_conflicto', 'Conflicto de horario')
            }
            for s in plan_sesiones if s.get('conflicto')
        ]
        if conflictos_en_plan:
            raise ConflictoCitas(conflictos_en_plan)

        # 2. Resolver especialidad
        if not id_especialidad:
            id_especialidad = self._obtener_especialidad(id_especialista)
        if not id_especialidad:
            return {
                'success': False,
                'error': 'El especialista no tiene especialidad asignada.',
                'citas_ids': [], 'errores': []
            }

        # 3. Obtener motivo
        motivo = self._obtener_motivo_presupuesto(id_presupuesto)

        # 4. Transacción única
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        citas_ids: List[int] = []

        try:
            for sesion in plan_sesiones:
                cita_id = self.cita_dao.guardarCita(
                    id_paciente=id_paciente,
                    id_agenda_horario=sesion.get('id_agenda_horario'),
                    id_especialista=id_especialista,
                    id_especialidad=id_especialidad,
                    cita_fecha=sesion['fecha'],
                    cita_hora_inicio=sesion['hora_inicio'],
                    cita_hora_fin=sesion['hora_fin'],
                    cita_tipo='SEGUIMIENTO' if sesion.get('numero_sesion', 1) > 1 else 'PRIMERA_VEZ',
                    cita_motivo=motivo,
                    cita_creacion_usuario=id_usuario,
                    id_estado_cita=1,
                    cita_observaciones=(
                        f"Generado automáticamente. "
                        f"Sesión {sesion.get('numero_sesion')} de plan."
                    ),
                    cita_numero_sesion=sesion.get('numero_sesion')
                )
                if not cita_id:
                    raise RuntimeError(
                        f"El DAO no pudo registrar la sesión {sesion.get('numero_sesion')}."
                    )
                citas_ids.append(cita_id)

            # 5. FASE FINAL: Actualizar estado del presupuesto en la MISMA transacción
            cur.execute("""
                UPDATE presupuestos 
                SET est_presupuesto = 'APROBADO',
                    id_usuario_modificacion = %s,
                    fecha_modificacion = CURRENT_TIMESTAMP
                WHERE id_presupuesto = %s
            """, (id_usuario, id_presupuesto))

            con.commit()
            app.logger.info(
                f"[confirmar_citas] {len(citas_ids)} cita(s) confirmadas "
                f"y presupuesto #{id_presupuesto} aprobado."
            )
            return {
                'success': True,
                'mensaje': f"Se registraron {len(citas_ids)} citas y se aprobó el presupuesto.",
                'citas_ids': citas_ids,
                'errores': []
            }

        except Exception as e:
            con.rollback()
            app.logger.error(
                f"[confirmar_citas] ROLLBACK TOTAL (presupuesto #{id_presupuesto}): {str(e)}"
            )
            return {
                'success': False,
                'error': f"Rollback completo. Ninguna cita fue guardada. Detalle: {str(e)}",
                'citas_ids': [],
                'errores': [str(e)]
            }
        finally:
            cur.close()
            con.close()

    # Alias retrocompatible para la API existente
    def registrar_plan(self, id_especialista: int, id_paciente: int,
                       id_presupuesto: int, plan_sesiones: List[Dict],
                       id_especialidad: Optional[int] = None,
                       id_usuario: int = 1) -> Dict[str, Any]:
        """Alias de confirmar_citas() para compatibilidad con registrarpresupuesto_api.py."""
        return self.confirmar_citas(
            id_especialista=id_especialista,
            id_paciente=id_paciente,
            id_presupuesto=id_presupuesto,
            plan_sesiones=plan_sesiones,
            id_especialidad=id_especialidad,
            id_usuario=id_usuario
        )

    # -----------------------------------------------------------------------
    # Helpers privados
    # -----------------------------------------------------------------------

    def _obtener_especialidad(self, id_especialista: int) -> Optional[int]:
        """Busca la especialidad principal del especialista en la BD."""
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute("""
                SELECT id_especialidad
                FROM especialista_especialidades
                WHERE id_especialista = %s
                LIMIT 1
            """, (id_especialista,))
            row = cur.fetchone()
            return row[0] if row else None
        except Exception as e:
            app.logger.error(f"Error al obtener especialidad: {str(e)}")
            return None
        finally:
            cur.close()
            con.close()

    def _obtener_motivo_presupuesto(self, id_presupuesto: int) -> str:
        """Genera el texto de motivo desde las observaciones del presupuesto."""
        try:
            from app.dao.modulos.ventas.presupuesto.PresupuestoDao import PresupuestoDao
            presupuesto = PresupuestoDao().getPresupuestoById(id_presupuesto)
            if presupuesto and presupuesto.get('presupuesto_observaciones'):
                return f"Plan: {presupuesto['presupuesto_observaciones']}"
        except Exception:
            pass
        return f"Plan de Tratamiento - Presupuesto #{id_presupuesto}"


# ---------------------------------------------------------------------------
# Ejemplo de uso (comentado — no ejecutar en producción)
# ---------------------------------------------------------------------------
# service = RecurrenceService()
#
# # Paso 1: Simular sin persistir
# reporte = service.simular_citas(
#     id_especialista=1, id_paciente=5,
#     fecha_inicio='2026-04-01', hora_inicio='09:00', hora_fin='09:30',
#     cantidad_sesiones=10, frecuencia='SEMANAL'
# )
# if reporte['tiene_conflictos']:
#     print("Conflictos:", reporte['conflictos'])
#     # Mostrar al usuario y detenerse aquí
# else:
#     # Paso 2: Obtener plan
#     plan = service.simular_plan(
#         id_especialista=1, id_paciente=5,
#         fecha_inicio='2026-04-01', hora_inicio='09:00', hora_fin='09:30',
#         cantidad_sesiones=10, frecuencia='SEMANAL'
#     )
#     # Paso 3: Confirmar con rollback total
#     resultado = service.confirmar_citas(
#         id_especialista=1, id_paciente=5, id_presupuesto=42,
#         plan_sesiones=plan['sesiones'], id_usuario=1
#     )
#     print(resultado)
