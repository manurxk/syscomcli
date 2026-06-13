-- ============================================================================
-- TRIGGERS Y FUNCIONES PARA AUDITORÍA AUTOMÁTICA
-- ============================================================================
-- Este script crea triggers y funciones para manejar automáticamente
-- la auditoría de usuarios en las tablas del sistema
-- Ejecutar después de todas las fases anteriores
-- ============================================================================
-- IMPORTANTE: 
-- 1. Los triggers capturan automáticamente usuario_creacion y usuario_modificacion
-- 2. El usuario se obtiene de la sesión de Flask (session['id_usuario'])
-- 3. Para tablas con patrón antiguo (creacion_usuario), se mantiene compatibilidad
-- ============================================================================

-- ============================================================================
-- FUNCIÓN: Obtener usuario actual desde sesión
-- ============================================================================
-- NOTA: Esta función debe ser llamada desde la aplicación Flask
-- El usuario se pasa como parámetro en los INSERT/UPDATE
-- ============================================================================

-- ============================================================================
-- FUNCIÓN: Actualizar fecha_modificacion automáticamente
-- ============================================================================
CREATE OR REPLACE FUNCTION actualizar_fecha_modificacion()
RETURNS TRIGGER AS $$
BEGIN
    NEW.fecha_modificacion = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS PARA TABLAS CON PATRÓN NUEVO (fecha_creacion, usuario_creacion)
-- ============================================================================

-- Tablas referenciales básicas
CREATE TRIGGER trg_actualizar_fecha_modificacion_generos
    BEFORE UPDATE ON generos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_estados_civiles
    BEFORE UPDATE ON estados_civiles
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_ciudades
    BEFORE UPDATE ON ciudades
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_niveles_instruccion
    BEFORE UPDATE ON niveles_instruccion
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_profesiones
    BEFORE UPDATE ON profesiones
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_especialidades
    BEFORE UPDATE ON especialidades
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Tablas de seguridad
CREATE TRIGGER trg_actualizar_fecha_modificacion_grupos
    BEFORE UPDATE ON grupos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_modulos
    BEFORE UPDATE ON modulos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_cargos
    BEFORE UPDATE ON cargos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_personas
    BEFORE UPDATE ON personas
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_pacientes
    BEFORE UPDATE ON pacientes
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Tablas de consultorio
CREATE TRIGGER trg_actualizar_fecha_modificacion_consultas
    BEFORE UPDATE ON consultas
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_registro_diagnosticos
    BEFORE UPDATE ON registro_diagnosticos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_tratamientos
    BEFORE UPDATE ON tratamientos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_anamnesis
    BEFORE UPDATE ON anamnesis
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- Tablas de ventas
CREATE TRIGGER trg_actualizar_fecha_modificacion_formas_cobro
    BEFORE UPDATE ON formas_cobro
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_cajas
    BEFORE UPDATE ON cajas
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

CREATE TRIGGER trg_actualizar_fecha_modificacion_facturas
    BEFORE UPDATE ON facturas
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_fecha_modificacion();

-- ============================================================================
-- FUNCIÓN: Validar cupos disponibles en citas
-- ============================================================================
CREATE OR REPLACE FUNCTION validar_cupo_disponible()
RETURNS TRIGGER AS $$
DECLARE
    v_cupos_totales INT;
    v_cupos_ocupados INT;
    v_estado_cancelada INT;
BEGIN
    -- Obtener ID del estado CANCELADA
    SELECT id_estado_cita INTO v_estado_cancelada
    FROM estados_citas 
    WHERE est_cita_nombre = 'CANCELADA';
    
    -- Obtener cupos totales de la agenda
    SELECT agen_cupos_totales INTO v_cupos_totales
    FROM agenda_horarios
    WHERE id_agenda_horario = NEW.id_agenda_horario;
    
    IF v_cupos_totales IS NULL THEN
        RAISE EXCEPTION 'No existe configuración de agenda para este horario';
    END IF;
    
    -- Contar citas ya agendadas (excluyendo canceladas)
    SELECT COUNT(*) INTO v_cupos_ocupados
    FROM citas
    WHERE id_especialista = NEW.id_especialista
        AND cita_fecha = NEW.cita_fecha
        AND cita_hora_inicio = NEW.cita_hora_inicio
        AND id_estado_cita != v_estado_cancelada
        AND id_cita != COALESCE(NEW.id_cita, 0)
        AND cita_activo = TRUE;
    
    -- Validar disponibilidad
    IF v_cupos_ocupados >= v_cupos_totales THEN
        RAISE EXCEPTION 'No hay cupos disponibles para este horario (Cupos: %, Ocupados: %)', 
            v_cupos_totales, v_cupos_ocupados;
    END IF;
    
    -- Auto-calcular hora_fin si no viene
    IF NEW.cita_hora_fin IS NULL OR NEW.cita_hora_fin <= NEW.cita_hora_inicio THEN
        NEW.cita_hora_fin := NEW.cita_hora_inicio + INTERVAL '60 minutes';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_cupo_before_insert_update
    BEFORE INSERT OR UPDATE ON citas
    FOR EACH ROW
    EXECUTE FUNCTION validar_cupo_disponible();

-- ============================================================================
-- FUNCIÓN: Registrar confirmación automática de citas
-- ============================================================================
CREATE OR REPLACE FUNCTION registrar_confirmacion_cita()
RETURNS TRIGGER AS $$
DECLARE
    v_estado_confirmada INT;
BEGIN
    -- Obtener ID del estado CONFIRMADA
    SELECT id_estado_cita INTO v_estado_confirmada
    FROM estados_citas 
    WHERE est_cita_nombre = 'CONFIRMADA';
    
    -- Si pasa a CONFIRMADA y no tenía fecha de confirmación
    IF NEW.id_estado_cita = v_estado_confirmada 
       AND OLD.id_estado_cita != v_estado_confirmada
       AND NEW.cita_fecha_confirmacion IS NULL THEN
        
        NEW.cita_fecha_confirmacion := CURRENT_TIMESTAMP;
        NEW.cita_usuario_confirmacion := NEW.cita_modificacion_usuario;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_registrar_confirmacion
    BEFORE UPDATE ON citas
    FOR EACH ROW
    WHEN (NEW.id_estado_cita IS DISTINCT FROM OLD.id_estado_cita)
    EXECUTE FUNCTION registrar_confirmacion_cita();

-- ============================================================================
-- COMENTARIOS
-- ============================================================================

COMMENT ON FUNCTION actualizar_fecha_modificacion() IS 'Actualiza automáticamente fecha_modificacion en UPDATE';
COMMENT ON FUNCTION validar_cupo_disponible() IS 'Valida que haya cupos disponibles antes de crear o modificar una cita';
COMMENT ON FUNCTION registrar_confirmacion_cita() IS 'Registra automáticamente la fecha y usuario que confirmó la cita';

-- ============================================================================
-- NOTAS IMPORTANTES
-- ============================================================================
-- 
-- 1. Los triggers de fecha_modificacion se ejecutan automáticamente en UPDATE
-- 2. El usuario_creacion y usuario_modificacion deben ser pasados desde la aplicación
-- 3. Para obtener el usuario desde Flask: session.get('id_usuario') o session.get('usu_nick')
-- 4. En las consultas SQL, usar: usuario_creacion = %s o usuario_modificacion = %s
-- 5. Los triggers de validación de cupos y confirmación funcionan automáticamente
-- 
-- ============================================================================

-- ============================================================================
-- FIN TRIGGERS Y FUNCIONES
-- ============================================================================








