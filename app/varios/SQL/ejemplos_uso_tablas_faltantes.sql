-- ============================================================================
-- EJEMPLOS DE USO Y CONSULTAS PARA LAS TABLAS FALTANTES
-- ============================================================================
-- Este archivo contiene ejemplos prácticos de cómo usar las nuevas tablas
-- 
-- NOTA: Todos los montos están en Guaraníes Paraguayos (PYG) - números enteros sin decimales
-- Ejemplo: 150000 = ciento cincuenta mil guaraníes
-- ============================================================================

-- ============================================================================
-- EJEMPLO 1: CREAR UN PRESUPUESTO
-- ============================================================================

-- Paso 1: Insertar el presupuesto principal
INSERT INTO presupuestos (
    id_consulta,
    id_paciente,
    id_profesional,
    presupuesto_numero,
    presupuesto_fecha,
    presupuesto_validez_dias,
    presupuesto_estado,
    presupuesto_observaciones,
    usuario_creacion
) VALUES (
    1,  -- id_consulta (puede ser NULL si es presupuesto independiente)
    1,  -- id_paciente
    1,  -- id_profesional
    'PRES-2024-001',  -- número único
    CURRENT_DATE,
    30,  -- válido por 30 días
    'PENDIENTE',
    'Presupuesto para tratamiento psicológico',
    'ADMIN'
) RETURNING id_presupuesto;

-- Paso 2: Insertar los detalles del presupuesto
-- (Supongamos que el id_presupuesto retornado fue 1)
INSERT INTO presupuesto_detalle (
    id_presupuesto,
    id_tipo_procedimiento,
    des_item,
    cantidad,
    precio_unitario,
    subtotal,
    observaciones
) VALUES
    (1, 1, 'Consulta psicológica inicial', 1, 150000, 150000, 'Primera consulta'),
    (1, 2, 'Sesión de terapia', 4, 120000, 480000, '4 sesiones programadas'),
    (1, NULL, 'Evaluación psicológica', 1, 200000, 200000, 'Evaluación completa');

-- Paso 3: Actualizar el total del presupuesto
UPDATE presupuestos
SET 
    presupuesto_subtotal = (
        SELECT SUM(subtotal) 
        FROM presupuesto_detalle 
        WHERE id_presupuesto = 1
    ),
    presupuesto_total = (
        SELECT SUM(subtotal) 
        FROM presupuesto_detalle 
        WHERE id_presupuesto = 1
    ) - presupuesto_descuento
WHERE id_presupuesto = 1;

-- ============================================================================
-- EJEMPLO 2: CREAR UNA ORDEN DE ESTUDIOS
-- ============================================================================

-- Paso 1: Crear la orden principal
INSERT INTO ordenes_estudios (
    id_consulta,
    id_paciente,
    id_profesional,
    orden_numero,
    orden_fecha,
    orden_tipo,
    orden_estado,
    orden_indicaciones,
    usuario_creacion
) VALUES (
    1,  -- id_consulta
    1,  -- id_paciente
    1,  -- id_profesional
    'ORD-LAB-2024-001',
    CURRENT_DATE,
    'LABORATORIO',
    'PENDIENTE',
    'Realizar estudios en ayunas de 12 horas',
    'ADMIN'
) RETURNING id_orden_estudio;

-- Paso 2: Agregar estudios específicos a la orden
-- (Supongamos que el id_orden_estudio retornado fue 1)
INSERT INTO orden_estudio_detalle (
    id_orden_estudio,
    id_tipo_estudio,
    id_tipo_analisis,
    des_estudio,
    estudio_estado,
    observaciones
) VALUES
    (1, 1, 1, 'Hemograma completo', 'PENDIENTE', 'Incluir recuento diferencial'),
    (1, 1, 2, 'Glicemia en ayunas', 'PENDIENTE', NULL),
    (1, 1, 3, 'Perfil lipídico', 'PENDIENTE', 'Ayuno de 12 horas');

-- ============================================================================
-- EJEMPLO 3: CREAR UNA RECETA MÉDICA
-- ============================================================================

-- Paso 1: Crear la receta principal
INSERT INTO recetas (
    id_consulta,
    id_paciente,
    id_profesional,
    receta_numero,
    receta_fecha,
    receta_validez_dias,
    receta_indicaciones_generales,
    receta_observaciones,
    usuario_creacion
) VALUES (
    1,  -- id_consulta
    1,  -- id_paciente
    1,  -- id_profesional
    'REC-2024-001',
    CURRENT_DATE,
    30,  -- válida por 30 días
    'Tomar con las comidas. No suspender sin consultar al médico.',
    'Seguir tratamiento completo',
    'ADMIN'
) RETURNING id_receta;

-- Paso 2: Agregar medicamentos a la receta
-- (Supongamos que el id_receta retornado fue 1)
INSERT INTO receta_detalle (
    id_receta,
    id_medicamento,
    medicamento_dosis,
    medicamento_frecuencia,
    medicamento_duracion,
    medicamento_cantidad,
    medicamento_indicaciones,
    medicamento_posologia
) VALUES
    (
        1,  -- id_receta
        1,  -- id_medicamento (ej: Paracetamol)
        '500mg',
        'Cada 8 horas',
        '7 días',
        21,  -- 3 veces al día x 7 días
        'Tomar después de las comidas',
        '1 tableta cada 8 horas con abundante agua'
    ),
    (
        1,
        2,  -- id_medicamento (ej: Ibuprofeno)
        '400mg',
        '2 veces al día',
        '5 días',
        10,
        'Tomar con alimentos',
        '1 tableta en el desayuno y 1 en la cena'
    );

-- ============================================================================
-- EJEMPLO 4: CREAR UN CERTIFICADO MÉDICO
-- ============================================================================

INSERT INTO certificados_medicos (
    id_consulta,
    id_paciente,
    id_profesional,
    certificado_numero,
    certificado_fecha,
    certificado_tipo,
    certificado_dias_reposo,
    certificado_desde_fecha,
    certificado_hasta_fecha,
    certificado_motivo,
    certificado_diagnostico,
    certificado_recomendaciones,
    certificado_estado,
    usuario_creacion
) VALUES (
    1,  -- id_consulta
    1,  -- id_paciente
    1,  -- id_profesional
    'CERT-2024-001',
    CURRENT_DATE,
    'REPOSO',
    5,  -- 5 días de reposo
    CURRENT_DATE,
    CURRENT_DATE + INTERVAL '5 days',
    'Reposo médico por cuadro gripal',
    'Infección respiratoria aguda',
    'Reposo absoluto, hidratación abundante, dieta blanda',
    'VIGENTE',
    'ADMIN'
);

-- ============================================================================
-- EJEMPLO 5: REGISTRAR INSUMOS UTILIZADOS EN UN PROCEDIMIENTO
-- ============================================================================

-- Paso 1: Registrar los insumos utilizados
INSERT INTO registro_insumos (
    id_registro_procedimiento,
    id_insumo,
    insumo_cantidad,
    insumo_costo_unitario,
    insumo_costo_total,
    observaciones
) VALUES
    (
        1,  -- id_registro_procedimiento
        1,  -- id_insumo (Algodón)
        2,  -- cantidad: 2 paquetes
        15000,  -- precio unitario (guaraníes)
        30000,  -- total (guaraníes)
        'Utilizado para limpieza'
    ),
    (
        1,
        2,  -- Gasa esterilizada
        1,
        25000,
        25000,
        'Para vendaje'
    ),
    (
        1,
        5,  -- Guantes quirúrgicos
        1,
        55000,
        55000,
        NULL
    );

-- ============================================================================
-- CONSULTAS ÚTILES (QUERIES)
-- ============================================================================

-- 1. Obtener presupuestos de un paciente
SELECT 
    p.id_presupuesto,
    p.presupuesto_numero,
    p.presupuesto_fecha,
    p.presupuesto_total,
    p.presupuesto_estado,
    CONCAT(per.per_nombre, ' ', per.per_apellido) AS paciente_nombre
FROM presupuestos p
JOIN pacientes pac ON p.id_paciente = pac.id_paciente
JOIN personas per ON pac.id_persona = per.id_persona
WHERE p.id_paciente = 1
ORDER BY p.presupuesto_fecha DESC;

-- 2. Obtener recetas activas de un paciente
SELECT 
    r.id_receta,
    r.receta_numero,
    r.receta_fecha,
    r.receta_validez_dias,
    CONCAT(per.per_nombre, ' ', per.per_apellido) AS profesional_nombre,
    COUNT(rd.id_receta_detalle) AS cantidad_medicamentos
FROM recetas r
JOIN especialistas e ON r.id_profesional = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas per ON f.id_persona = per.id_persona
LEFT JOIN receta_detalle rd ON r.id_receta = rd.id_receta
WHERE r.id_paciente = 1 
    AND r.est_receta = 'A'
    AND r.receta_fecha + INTERVAL '1 day' * r.receta_validez_dias >= CURRENT_DATE
GROUP BY r.id_receta, r.receta_numero, r.receta_fecha, r.receta_validez_dias, per.per_nombre, per.per_apellido
ORDER BY r.receta_fecha DESC;

-- 3. Obtener órdenes de estudios pendientes
SELECT 
    o.id_orden_estudio,
    o.orden_numero,
    o.orden_fecha,
    o.orden_tipo,
    CONCAT(per.per_nombre, ' ', per.per_apellido) AS paciente_nombre,
    COUNT(od.id_orden_detalle) AS cantidad_estudios
FROM ordenes_estudios o
JOIN pacientes p ON o.id_paciente = p.id_paciente
JOIN personas per ON p.id_persona = per.id_persona
LEFT JOIN orden_estudio_detalle od ON o.id_orden_estudio = od.id_orden_estudio
WHERE o.orden_estado = 'PENDIENTE'
    AND o.est_orden = 'A'
GROUP BY o.id_orden_estudio, o.orden_numero, o.orden_fecha, o.orden_tipo, per.per_nombre, per.per_apellido
ORDER BY o.orden_fecha DESC;

-- 4. Obtener certificados vigentes de un paciente
SELECT 
    c.id_certificado,
    c.certificado_numero,
    c.certificado_fecha,
    c.certificado_tipo,
    c.certificado_desde_fecha,
    c.certificado_hasta_fecha,
    c.certificado_motivo,
    CONCAT(per.per_nombre, ' ', per.per_apellido) AS profesional_nombre
FROM certificados_medicos c
JOIN especialistas e ON c.id_profesional = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas per ON f.id_persona = per.id_persona
WHERE c.id_paciente = 1
    AND c.certificado_estado = 'VIGENTE'
    AND c.est_certificado = 'A'
    AND c.certificado_hasta_fecha >= CURRENT_DATE
ORDER BY c.certificado_fecha DESC;

-- 5. Obtener insumos utilizados en un procedimiento
SELECT 
    ri.id_registro_insumo,
    i.des_insumo,
    ri.insumo_cantidad,
    i.insumo_unidad_medida,
    ri.insumo_costo_unitario,
    ri.insumo_costo_total,
    ri.observaciones
FROM registro_insumos ri
JOIN insumos i ON ri.id_insumo = i.id_insumo
WHERE ri.id_registro_procedimiento = 1
ORDER BY ri.fecha_registro DESC;

-- 6. Obtener detalle completo de una receta con medicamentos
SELECT 
    r.id_receta,
    r.receta_numero,
    r.receta_fecha,
    m.des_medicamento,
    m.medicamento_concentracion,
    rd.medicamento_dosis,
    rd.medicamento_frecuencia,
    rd.medicamento_duracion,
    rd.medicamento_cantidad,
    rd.medicamento_posologia,
    rd.medicamento_indicaciones
FROM recetas r
JOIN receta_detalle rd ON r.id_receta = rd.id_receta
JOIN medicamentos m ON rd.id_medicamento = m.id_medicamento
WHERE r.id_receta = 1
    AND rd.est_receta_detalle = 'A'
ORDER BY rd.id_receta_detalle;

-- 7. Obtener presupuesto con detalle completo
SELECT 
    p.id_presupuesto,
    p.presupuesto_numero,
    p.presupuesto_fecha,
    p.presupuesto_subtotal,
    p.presupuesto_descuento,
    p.presupuesto_total,
    pd.des_item,
    pd.cantidad,
    pd.precio_unitario,
    pd.subtotal
FROM presupuestos p
LEFT JOIN presupuesto_detalle pd ON p.id_presupuesto = pd.id_presupuesto
WHERE p.id_presupuesto = 1
ORDER BY pd.id_presupuesto_detalle;

-- ============================================================================
-- FUNCIONES ÚTILES (TRIGGERS Y FUNCIONES)
-- ============================================================================

-- Función para generar número automático de presupuesto
CREATE OR REPLACE FUNCTION generar_numero_presupuesto()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.presupuesto_numero IS NULL OR NEW.presupuesto_numero = '' THEN
        NEW.presupuesto_numero := 'PRES-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-' || 
                                  LPAD(COALESCE((SELECT MAX(CAST(SUBSTRING(presupuesto_numero FROM '[0-9]+$') AS INTEGER)) 
                                                 FROM presupuestos 
                                                 WHERE presupuesto_numero LIKE 'PRES-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-%'), 0) + 1, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_generar_numero_presupuesto
    BEFORE INSERT ON presupuestos
    FOR EACH ROW
    EXECUTE FUNCTION generar_numero_presupuesto();

-- Función similar para recetas
CREATE OR REPLACE FUNCTION generar_numero_receta()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.receta_numero IS NULL OR NEW.receta_numero = '' THEN
        NEW.receta_numero := 'REC-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-' || 
                             LPAD(COALESCE((SELECT MAX(CAST(SUBSTRING(receta_numero FROM '[0-9]+$') AS INTEGER)) 
                                            FROM recetas 
                                            WHERE receta_numero LIKE 'REC-' || TO_CHAR(CURRENT_DATE, 'YYYY') || '-%'), 0) + 1, 4, '0');
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_generar_numero_receta
    BEFORE INSERT ON recetas
    FOR EACH ROW
    EXECUTE FUNCTION generar_numero_receta();

-- Función para actualizar stock de insumos cuando se registra su uso
CREATE OR REPLACE FUNCTION actualizar_stock_insumo()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE insumos
    SET insumo_stock_actual = insumo_stock_actual - NEW.insumo_cantidad
    WHERE id_insumo = NEW.id_insumo;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_actualizar_stock_insumo
    AFTER INSERT ON registro_insumos
    FOR EACH ROW
    EXECUTE FUNCTION actualizar_stock_insumo();

-- ============================================================================
-- NOTAS FINALES
-- ============================================================================
-- 
-- Estos ejemplos muestran cómo:
-- 1. Insertar datos en las nuevas tablas
-- 2. Realizar consultas útiles
-- 3. Crear triggers para automatizar procesos
--
-- Recuerda ajustar los IDs según tus datos reales antes de ejecutar los INSERTs
--
-- ============================================================================

