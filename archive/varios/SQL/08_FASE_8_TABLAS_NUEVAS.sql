-- ============================================================================
-- FASE 8: TABLAS NUEVAS DEL SISTEMA
-- ============================================================================
-- Este script crea las tablas nuevas del sistema (Presupuestos, Recetas, 
-- Órdenes de Estudios, Certificados Médicos, Insumos, Informes)
-- Ejecutar después de: 07_FASE_7_PRINCIPALES_VENTAS.sql
-- ============================================================================
-- IMPORTANTE: 
-- 1. Las tablas referenciales se gestionan desde las interfaces administrativas
-- 2. NO contiene INSERTs - los datos se gestionan desde las interfaces del sistema
-- 3. Todas las tablas siguen las convenciones del sistema
-- ============================================================================

-- ============================================================================
-- TABLA REFERENCIAL: TIPOS DE CERTIFICADOS MÉDICOS
-- ============================================================================
CREATE TABLE IF NOT EXISTS tipos_certificados_medicos (
    id_tipo_certificado SERIAL PRIMARY KEY,
    des_tipo_certificado VARCHAR(100) NOT NULL UNIQUE,
    est_tipo_certificado CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 1. PRESUPUESTOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS presupuestos (
    id_presupuesto SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    presupuesto_numero VARCHAR(50) UNIQUE NOT NULL,
    presupuesto_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    presupuesto_validez_dias INTEGER DEFAULT 30,
    presupuesto_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    presupuesto_subtotal INTEGER DEFAULT 0,
    presupuesto_descuento INTEGER DEFAULT 0,
    presupuesto_total INTEGER DEFAULT 0,
    presupuesto_observaciones TEXT,
    est_presupuesto CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de presupuesto
CREATE TABLE IF NOT EXISTS presupuesto_detalle (
    id_presupuesto_detalle SERIAL PRIMARY KEY,
    id_presupuesto INTEGER NOT NULL,
    id_tipo_procedimiento INTEGER,
    des_item VARCHAR(255) NOT NULL,
    cantidad INTEGER DEFAULT 1,
    precio_unitario INTEGER NOT NULL,
    subtotal INTEGER NOT NULL,
    observaciones TEXT,
    
    FOREIGN KEY (id_presupuesto) REFERENCES presupuestos(id_presupuesto) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_procedimiento) REFERENCES tipos_procedimientos(id_tipo_procedimiento) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================================
-- 2. ÓRDENES DE ESTUDIOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS ordenes_estudios (
    id_orden_estudio SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    orden_numero VARCHAR(50) UNIQUE NOT NULL,
    orden_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    orden_tipo VARCHAR(50) NOT NULL,
    orden_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    orden_observaciones TEXT,
    orden_indicaciones TEXT,
    est_orden CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de estudios
CREATE TABLE IF NOT EXISTS orden_estudio_detalle (
    id_orden_detalle SERIAL PRIMARY KEY,
    id_orden_estudio INTEGER NOT NULL,
    id_tipo_estudio INTEGER,
    id_tipo_analisis INTEGER,
    des_estudio VARCHAR(255) NOT NULL,
    estudio_estado VARCHAR(20) DEFAULT 'PENDIENTE',
    estudio_resultado TEXT,
    estudio_fecha_realizacion DATE,
    observaciones TEXT,
    
    FOREIGN KEY (id_orden_estudio) REFERENCES ordenes_estudios(id_orden_estudio) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_estudio) REFERENCES tipos_estudios(id_tipo_estudio) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_analisis) REFERENCES tipos_analisis(id_tipo_analisis) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================================
-- 3. RECETAS E INDICACIONES (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS recetas (
    id_receta SERIAL PRIMARY KEY,
    id_consulta INTEGER NOT NULL,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    receta_numero VARCHAR(50) UNIQUE NOT NULL,
    receta_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    receta_validez_dias INTEGER DEFAULT 30,
    receta_observaciones TEXT,
    receta_indicaciones_generales TEXT,
    est_receta CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Detalle de medicamentos
CREATE TABLE IF NOT EXISTS receta_detalle (
    id_receta_detalle SERIAL PRIMARY KEY,
    id_receta INTEGER NOT NULL,
    id_medicamento INTEGER NOT NULL,
    medicamento_dosis VARCHAR(100),
    medicamento_frecuencia VARCHAR(100) NOT NULL,
    medicamento_duracion VARCHAR(100) NOT NULL,
    medicamento_cantidad INTEGER,
    medicamento_indicaciones TEXT,
    medicamento_posologia TEXT,
    est_receta_detalle CHAR(1) DEFAULT 'A',
    
    FOREIGN KEY (id_receta) REFERENCES recetas(id_receta) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_medicamento) REFERENCES medicamentos(id_medicamento) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 4. CERTIFICADOS MÉDICOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS certificados_medicos (
    id_certificado SERIAL PRIMARY KEY,
    id_consulta INTEGER,
    id_paciente INTEGER NOT NULL,
    id_profesional INTEGER NOT NULL,
    certificado_numero VARCHAR(50) UNIQUE NOT NULL,
    certificado_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    id_tipo_certificado INTEGER NOT NULL,
    certificado_dias_reposo INTEGER,
    certificado_desde_fecha DATE,
    certificado_hasta_fecha DATE,
    certificado_motivo TEXT NOT NULL,
    certificado_diagnostico TEXT,
    certificado_recomendaciones TEXT,
    certificado_estado VARCHAR(20) DEFAULT 'VIGENTE',
    est_certificado CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_tipo_certificado) REFERENCES tipos_certificados_medicos(id_tipo_certificado)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 5. INSUMOS DE PROCEDIMIENTOS (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS insumos (
    id_insumo SERIAL PRIMARY KEY,
    des_insumo VARCHAR(255) NOT NULL UNIQUE,
    insumo_unidad_medida VARCHAR(20) DEFAULT 'UNIDAD',
    stock_actual INTEGER DEFAULT 0,
    stock_minimo INTEGER DEFAULT 0,
    insumo_precio_unitario INTEGER,
    est_insumo CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA'
);

-- Registro de insumos utilizados
CREATE TABLE IF NOT EXISTS registro_insumos (
    id_registro_insumo SERIAL PRIMARY KEY,
    id_registro_procedimiento INTEGER NOT NULL,
    id_insumo INTEGER NOT NULL,
    insumo_cantidad INTEGER NOT NULL DEFAULT 1,
    insumo_costo_unitario INTEGER,
    insumo_costo_total INTEGER,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_registro_procedimiento) REFERENCES registro_procedimientos(id_registro_procedimiento) 
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (id_insumo) REFERENCES insumos(id_insumo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- ============================================================================
-- 6. INFORMES DE AGENDAMIENTO (Módulo Agenda Médica)
-- ============================================================================
CREATE TABLE IF NOT EXISTS informes_agendamiento (
    id_informe_agendamiento SERIAL PRIMARY KEY,
    informe_tipo VARCHAR(50) NOT NULL,
    informe_fecha_desde DATE NOT NULL,
    informe_fecha_hasta DATE NOT NULL,
    id_especialista INTEGER,
    id_especialidad INTEGER,
    informe_parametros JSONB,
    informe_generado BOOLEAN DEFAULT FALSE,
    informe_fecha_generacion TIMESTAMP,
    usuario_generacion VARCHAR(50),
    est_informe CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================================
-- 7. INFORMES DE CONSULTORIO (Módulo Consultorio)
-- ============================================================================
CREATE TABLE IF NOT EXISTS informes_consultorio (
    id_informe_consultorio SERIAL PRIMARY KEY,
    informe_tipo VARCHAR(50) NOT NULL,
    informe_fecha_desde DATE NOT NULL,
    informe_fecha_hasta DATE NOT NULL,
    id_profesional INTEGER,
    id_especialidad INTEGER,
    informe_parametros JSONB,
    informe_generado BOOLEAN DEFAULT FALSE,
    informe_fecha_generacion TIMESTAMP,
    usuario_generacion VARCHAR(50),
    est_informe CHAR(1) DEFAULT 'A',
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista) 
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_presupuesto_paciente ON presupuestos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_presupuesto_consulta ON presupuestos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_presupuesto_fecha ON presupuestos(presupuesto_fecha);
CREATE INDEX IF NOT EXISTS idx_presupuesto_numero ON presupuestos(presupuesto_numero);
CREATE INDEX IF NOT EXISTS idx_orden_paciente ON ordenes_estudios(id_paciente);
CREATE INDEX IF NOT EXISTS idx_orden_consulta ON ordenes_estudios(id_consulta);
CREATE INDEX IF NOT EXISTS idx_orden_fecha ON ordenes_estudios(orden_fecha);
CREATE INDEX IF NOT EXISTS idx_orden_numero ON ordenes_estudios(orden_numero);
CREATE INDEX IF NOT EXISTS idx_receta_paciente ON recetas(id_paciente);
CREATE INDEX IF NOT EXISTS idx_receta_consulta ON recetas(id_consulta);
CREATE INDEX IF NOT EXISTS idx_receta_fecha ON recetas(receta_fecha);
CREATE INDEX IF NOT EXISTS idx_receta_numero ON recetas(receta_numero);
CREATE INDEX IF NOT EXISTS idx_certificado_paciente ON certificados_medicos(id_paciente);
CREATE INDEX IF NOT EXISTS idx_certificado_consulta ON certificados_medicos(id_consulta);
CREATE INDEX IF NOT EXISTS idx_certificado_fecha ON certificados_medicos(certificado_fecha);
CREATE INDEX IF NOT EXISTS idx_certificado_numero ON certificados_medicos(certificado_numero);
CREATE INDEX IF NOT EXISTS idx_certificado_tipo ON certificados_medicos(id_tipo_certificado);
CREATE INDEX IF NOT EXISTS idx_registro_insumo_procedimiento ON registro_insumos(id_registro_procedimiento);
CREATE INDEX IF NOT EXISTS idx_registro_insumo_insumo ON registro_insumos(id_insumo);
CREATE INDEX IF NOT EXISTS idx_informe_agendamiento_fechas ON informes_agendamiento(informe_fecha_desde, informe_fecha_hasta);
CREATE INDEX IF NOT EXISTS idx_informe_agendamiento_especialista ON informes_agendamiento(id_especialista);
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_fechas ON informes_consultorio(informe_fecha_desde, informe_fecha_hasta);
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_profesional ON informes_consultorio(id_profesional);
CREATE INDEX IF NOT EXISTS idx_informe_consultorio_tipo ON informes_consultorio(informe_tipo);

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE presupuestos IS 'Presupuestos/cotizaciones para pacientes';
COMMENT ON TABLE ordenes_estudios IS 'Órdenes de laboratorio/imagenología/estudios complementarios';
COMMENT ON TABLE recetas IS 'Recetas médicas con indicaciones';
COMMENT ON TABLE certificados_medicos IS 'Certificados médicos emitidos';
COMMENT ON TABLE insumos IS 'Insumos utilizados en procedimientos';
COMMENT ON TABLE informes_agendamiento IS 'Informes de agendamiento (estadísticas, reportes)';
COMMENT ON TABLE informes_consultorio IS 'Informes de consultorio (consultas, diagnósticos, tratamientos)';

-- ============================================================================
-- TABLA ADICIONAL: ITEMS SERVICIOS (de 13_OTROS.sql)
-- ============================================================================

CREATE TABLE IF NOT EXISTS items_servicios (
    id_item             SERIAL PRIMARY KEY,
    cod_item            VARCHAR(30),
    des_item            VARCHAR(150) NOT NULL,
    id_tipo_item        INTEGER NULL REFERENCES tipos_items(id_tipo_item),
    unidad_medida       VARCHAR(20) NOT NULL DEFAULT 'SERVICIO',
    precio_referencial  INTEGER NOT NULL DEFAULT 0,
    id_tipo_impuesto    INTEGER NULL REFERENCES tipos_impuestos(id_tipo_impuesto),
    porcentaje_impuesto NUMERIC(5,2) DEFAULT 0,
    est_item            CHAR(1) NOT NULL DEFAULT 'A',
    usuario_creacion    INTEGER DEFAULT 1,
    fecha_creacion      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion INTEGER,
    fecha_modificacion   TIMESTAMP,
    FOREIGN KEY (usuario_creacion) REFERENCES usuarios(id_usuario) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario) ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_items_servicios_des_item ON items_servicios (LOWER(des_item));

COMMENT ON TABLE items_servicios IS 'Items de servicios disponibles para facturación';

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================

-- Tipos de certificados médicos
INSERT INTO tipos_certificados_medicos (des_tipo_certificado, est_tipo_certificado, usuario_creacion) VALUES
    ('Certificado de Aptitud', 'A', 1),
    ('Certificado de Reposo', 'A', 1),
    ('Certificado de Tratamiento', 'A', 1),
    ('Certificado de Asistencia', 'A', 1),
    ('Certificado de Evaluación', 'A', 1)
ON CONFLICT (des_tipo_certificado) DO NOTHING;

-- Insumos
INSERT INTO insumos (des_insumo, insumo_unidad_medida, stock_actual, stock_minimo, insumo_precio_unitario, est_insumo, usuario_creacion) VALUES
    ('ALGODÓN', 'PAQUETE', 50, 10, 15000, 'A', 1),
    ('GASA ESTERILIZADA', 'PAQUETE', 30, 5, 25000, 'A', 1),
    ('AGUJAS DESECHABLES', 'CAJA', 20, 5, 45000, 'A', 1),
    ('JERINGAS DESECHABLES', 'CAJA', 25, 5, 35000, 'A', 1),
    ('GUANTES QUIRÚRGICOS', 'CAJA', 40, 10, 55000, 'A', 1),
    ('ALCOHOL', 'LITRO', 15, 3, 12000, 'A', 1),
    ('VENDAS', 'UNIDAD', 100, 20, 8000, 'A', 1),
    ('CURITAS', 'CAJA', 50, 10, 18000, 'A', 1),
    ('AGUA OXIGENADA', 'BOTELLA', 25, 5, 15000, 'A', 1),
    ('YODO', 'BOTELLA', 20, 5, 20000, 'A', 1),
    ('Papel A4', 'Resma', 50, 10, 45000, 'A', 1),
    ('Sobres de Correspondencia', 'Unidad', 200, 50, 500, 'A', 1),
    ('Carpetas de Expediente', 'Unidad', 100, 20, 8000, 'A', 1),
    ('Hojas de Evaluación', 'Unidad', 500, 100, 2000, 'A', 1),
    ('Formularios de Consentimiento', 'Unidad', 300, 50, 1500, 'A', 1),
    ('Material de Escritura', 'Set', 30, 10, 15000, 'A', 1),
    ('Alcohol en Gel', 'Litro', 20, 5, 25000, 'A', 1),
    ('Guantes Desechables', 'Caja', 25, 5, 35000, 'A', 1),
    ('Mascarillas', 'Caja', 40, 10, 40000, 'A', 1),
    ('Toallas Desinfectantes', 'Paquete', 15, 5, 12000, 'A', 1)
ON CONFLICT (des_insumo) DO NOTHING;

-- ============================================================================
-- FIN FASE 8
-- ============================================================================








