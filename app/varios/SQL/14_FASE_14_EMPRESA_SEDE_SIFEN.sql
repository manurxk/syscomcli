-- ============================================================================
-- FASE 14: EMPRESA, SEDE, ESTABLECIMIENTO, PUNTO DE EXPEDICIÓN Y TIMBRADO (SIFEN)
-- ============================================================================
-- Este script crea la estructura completa para:
-- - Empresa (con datos SIFEN completos)
-- - Sedes (múltiples sedes por empresa)
-- - Consultorios (modificación para incluir relación con sede)
-- - Timbrados (por empresa)
-- - Establecimientos (por sede)
-- - Puntos de Expedición (por establecimiento)
-- - Modificaciones a tabla Facturas (agregar relaciones)
-- 
-- Ejecutar después de: 07_FASE_7_PRINCIPALES_VENTAS.sql
-- ============================================================================

-- ============================================================================
-- 1. TABLA EMPRESA (Datos corporativos y SIFEN)
-- ============================================================================
CREATE TABLE IF NOT EXISTS empresa (
    id_empresa SERIAL PRIMARY KEY,
    
    -- IDENTIFICACIÓN TRIBUTARIA (OBLIGATORIO para SIFEN)
    ruc_nit VARCHAR(20) NOT NULL UNIQUE,
    digito_verificador CHAR(1) NOT NULL,
    razon_social VARCHAR(255) NOT NULL,
    nombre_comercial VARCHAR(150),
    tipo_contribuyente VARCHAR(50) NOT NULL DEFAULT 'persona_juridica' 
        CHECK (tipo_contribuyente IN ('persona_fisica', 'persona_juridica', 'eas')),
    
    -- DOMICILIO FISCAL (OBLIGATORIO para SIFEN)
    departamento VARCHAR(100) NOT NULL,
    distrito VARCHAR(100) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    direccion TEXT NOT NULL,
    numero_casa VARCHAR(20),
    codigo_postal VARCHAR(10),
    
    -- DATOS DE CONTACTO (OBLIGATORIO para SIFEN)
    telefono VARCHAR(50) NOT NULL,
    celular VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    sitio_web VARCHAR(255),
    
    -- REPRESENTANTE LEGAL (Obligatorio para personas jurídicas)
    representante_legal_nombre VARCHAR(255),
    representante_legal_apellido VARCHAR(255),
    representante_legal_ci VARCHAR(20),
    representante_legal_cargo VARCHAR(100),
    
    -- FACTURACIÓN ELECTRÓNICA SIFEN
    facturador_electronico BOOLEAN DEFAULT FALSE,
    fecha_habilitacion_sifen DATE,
    grupo_obligatoriedad INTEGER, -- Grupo 1-18 según DNIT
    ambiente_sifen VARCHAR(20) DEFAULT 'prueba' CHECK (ambiente_sifen IN ('prueba', 'produccion')),
    
    -- CERTIFICADO DE FIRMA DIGITAL
    certificado_firma_digital_path TEXT, -- Ruta al archivo .pfx
    certificado_firma_digital_password_encrypted TEXT, -- Contraseña cifrada
    certificado_firma_digital_serial VARCHAR(255), -- Serial del certificado
    certificado_firma_digital_fecha_vencimiento DATE,
    
    -- CÓDIGO DE SEGURIDAD DEL CONTRIBUYENTE (CSC)
    codigo_seguridad_contribuyente VARCHAR(100), -- CSC otorgado por DNIT
    
    -- ACTIVIDAD ECONÓMICA
    actividad_economica_principal VARCHAR(255),
    
    -- CONFIGURACIÓN GENERAL
    logo_path VARCHAR(255), -- Ruta al logo
    horario_atencion TEXT,
    es_principal BOOLEAN DEFAULT FALSE, -- Solo una empresa puede ser principal
    
    -- ESTADO Y AUDITORÍA
    est_empresa BOOLEAN DEFAULT TRUE,
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    -- VALIDACIONES
    CONSTRAINT chk_empresa_ruc CHECK (LENGTH(ruc_nit) >= 6 AND LENGTH(ruc_nit) <= 20),
    CONSTRAINT chk_empresa_email CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

-- Constraint: Solo una empresa puede ser principal
CREATE UNIQUE INDEX IF NOT EXISTS idx_empresa_principal 
ON empresa(es_principal) 
WHERE es_principal = TRUE;

-- Índices
CREATE INDEX IF NOT EXISTS idx_empresa_ruc ON empresa(ruc_nit);
CREATE INDEX IF NOT EXISTS idx_empresa_estado ON empresa(est_empresa);
CREATE INDEX IF NOT EXISTS idx_empresa_tipo ON empresa(tipo_contribuyente);

-- Comentarios
COMMENT ON TABLE empresa IS 'Datos corporativos de la empresa/clínica con información completa para SIFEN';
COMMENT ON COLUMN empresa.ruc_nit IS 'RUC sin guión (ej: 800123456)';
COMMENT ON COLUMN empresa.certificado_firma_digital_path IS 'Ruta física del archivo .pfx del certificado digital';
COMMENT ON COLUMN empresa.codigo_seguridad_contribuyente IS 'CSC otorgado por DNIT para generar códigos QR';

-- ============================================================================
-- 2. TABLA SEDES (Múltiples sedes por empresa)
-- ============================================================================
CREATE TABLE IF NOT EXISTS sedes (
    id_sede SERIAL PRIMARY KEY,
    id_empresa INTEGER NOT NULL,
    
    -- IDENTIFICACIÓN
    des_sede VARCHAR(150) NOT NULL,
    codigo_sede VARCHAR(20), -- Código interno único
    
    -- UBICACIÓN FÍSICA
    direccion VARCHAR(255),
    ciudad VARCHAR(100),
    departamento VARCHAR(100),
    codigo_postal VARCHAR(10),
    latitud DECIMAL(10, 8), -- Para mapas/GPS
    longitud DECIMAL(11, 8),
    
    -- CONTACTO
    telefono VARCHAR(50),
    email VARCHAR(100),
    
    -- CONFIGURACIÓN
    horario_atencion TEXT,
    es_principal BOOLEAN DEFAULT FALSE, -- Sede principal de la empresa
    
    -- ESTADO Y AUDITORÍA
    est_sede BOOLEAN DEFAULT TRUE,
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    -- RELACIONES
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- VALIDACIONES
    CONSTRAINT unique_codigo_sede_empresa UNIQUE (id_empresa, codigo_sede)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_sedes_empresa ON sedes(id_empresa);
CREATE INDEX IF NOT EXISTS idx_sedes_estado ON sedes(est_sede);
CREATE INDEX IF NOT EXISTS idx_sedes_principal ON sedes(es_principal);

-- Constraint: Solo una sede principal por empresa
CREATE UNIQUE INDEX IF NOT EXISTS idx_sede_principal_empresa 
ON sedes(id_empresa, es_principal) 
WHERE es_principal = TRUE;

COMMENT ON TABLE sedes IS 'Sedes o sucursales de la empresa';
COMMENT ON COLUMN sedes.codigo_sede IS 'Código interno único por empresa (ej: SEDE-001)';

-- ============================================================================
-- 3. TABLA TIMBRADOS (Por empresa)
-- ============================================================================
CREATE TABLE IF NOT EXISTS timbrados (
    id_timbrado SERIAL PRIMARY KEY,
    id_empresa INTEGER NOT NULL,
    
    -- DATOS DEL TIMBRADO
    numero_timbrado VARCHAR(8) NOT NULL, -- Número de 8 dígitos otorgado por DNIT
    fecha_inicio DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    
    -- TIPO DE DOCUMENTO
    tipo_documento VARCHAR(50) NOT NULL DEFAULT 'factura'
        CHECK (tipo_documento IN ('factura', 'nota_credito', 'nota_debito', 'autofactura', 'nota_remision', 'comprobante_retencion')),
    
    -- TIPO DE GENERACIÓN
    tipo_generacion VARCHAR(50) NOT NULL DEFAULT 'electronico'
        CHECK (tipo_generacion IN ('electronico', 'preimpreso', 'autoimpreso', 'virtual')),
    
    -- ESTADO
    est_timbrado BOOLEAN DEFAULT TRUE,
    estado VARCHAR(50) DEFAULT 'activo' 
        CHECK (estado IN ('activo', 'vencido', 'dado_baja', 'suspendido')),
    
    -- OBSERVACIONES
    observaciones TEXT,
    
    -- AUDITORÍA
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INTEGER,
    
    -- RELACIONES
    FOREIGN KEY (id_empresa) REFERENCES empresa(id_empresa) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- VALIDACIONES
    CONSTRAINT chk_fechas_timbrado CHECK (fecha_vencimiento >= fecha_inicio),
    CONSTRAINT unique_timbrado_empresa UNIQUE (id_empresa, numero_timbrado)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_timbrados_empresa ON timbrados(id_empresa);
CREATE INDEX IF NOT EXISTS idx_timbrados_numero ON timbrados(numero_timbrado);
CREATE INDEX IF NOT EXISTS idx_timbrados_vigencia ON timbrados(fecha_inicio, fecha_vencimiento);
CREATE INDEX IF NOT EXISTS idx_timbrados_estado ON timbrados(estado);

COMMENT ON TABLE timbrados IS 'Timbrados autorizados por DNIT para la empresa';
COMMENT ON COLUMN timbrados.numero_timbrado IS 'Número de 8 dígitos otorgado por DNIT';

-- ============================================================================
-- 4. TABLA ESTABLECIMIENTOS (Por sede - para numeración de documentos)
-- ============================================================================
CREATE TABLE IF NOT EXISTS establecimientos (
    id_establecimiento SERIAL PRIMARY KEY,
    id_sede INTEGER NOT NULL,
    
    -- IDENTIFICACIÓN (Según DNIT)
    codigo_establecimiento VARCHAR(3) NOT NULL, -- Código de 3 dígitos (001, 002, etc.)
    nombre_establecimiento VARCHAR(255) NOT NULL,
    descripcion TEXT,
    
    -- CONFIGURACIÓN
    es_principal BOOLEAN DEFAULT FALSE,
    
    -- ESTADO Y AUDITORÍA
    est_establecimiento BOOLEAN DEFAULT TRUE,
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    
    -- RELACIONES
    FOREIGN KEY (id_sede) REFERENCES sedes(id_sede) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- VALIDACIONES
    CONSTRAINT chk_codigo_establecimiento CHECK (LENGTH(codigo_establecimiento) = 3),
    CONSTRAINT unique_codigo_sede UNIQUE (id_sede, codigo_establecimiento)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_establecimientos_sede ON establecimientos(id_sede);
CREATE INDEX IF NOT EXISTS idx_establecimientos_codigo ON establecimientos(codigo_establecimiento);

COMMENT ON TABLE establecimientos IS 'Establecimientos según numeración DNIT (001=matriz, 002=sucursal1, etc.)';
COMMENT ON COLUMN establecimientos.codigo_establecimiento IS 'Código de 3 dígitos asignado por DNIT o auto-asignado';

-- ============================================================================
-- 5. TABLA PUNTOS DE EXPEDICIÓN (Por establecimiento)
-- ============================================================================
CREATE TABLE IF NOT EXISTS puntos_expedicion (
    id_punto_expedicion SERIAL PRIMARY KEY,
    id_establecimiento INTEGER NOT NULL,
    
    -- IDENTIFICACIÓN
    codigo_punto_expedicion VARCHAR(3) NOT NULL, -- Código de 3 dígitos (001, 002, etc.)
    nombre_punto_expedicion VARCHAR(255) NOT NULL,
    descripcion TEXT, -- Ej: "Caja 1", "Consultorios", "Farmacia"
    
    -- TIPO DE PUNTO
    tipo_punto VARCHAR(50) DEFAULT 'caja'
        CHECK (tipo_punto IN ('caja', 'consultorio', 'farmacia', 'laboratorio', 'ambulancia', 'virtual', 'otro')),
    
    -- CONFIGURACIÓN
    permite_facturacion BOOLEAN DEFAULT TRUE,
    
    -- NUMERACIÓN ACTUAL (para control de secuencia)
    ultimo_numero_usado INTEGER DEFAULT 0, -- Último número secuencial usado
    serie_actual VARCHAR(2) DEFAULT NULL, -- Serie actual: NULL, AA, AB, etc.
    
    -- ESTADO Y AUDITORÍA
    est_punto_expedicion BOOLEAN DEFAULT TRUE,
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_usuario INTEGER NOT NULL DEFAULT 1,
    
    -- RELACIONES
    FOREIGN KEY (id_establecimiento) REFERENCES establecimientos(id_establecimiento) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- VALIDACIONES
    CONSTRAINT chk_codigo_punto CHECK (LENGTH(codigo_punto_expedicion) = 3),
    CONSTRAINT unique_codigo_establecimiento UNIQUE (id_establecimiento, codigo_punto_expedicion),
    CONSTRAINT chk_ultimo_numero CHECK (ultimo_numero_usado >= 0 AND ultimo_numero_usado <= 9999999)
);

-- Índices
CREATE INDEX IF NOT EXISTS idx_puntos_expedicion_establecimiento ON puntos_expedicion(id_establecimiento);
CREATE INDEX IF NOT EXISTS idx_puntos_expedicion_codigo ON puntos_expedicion(codigo_punto_expedicion);

COMMENT ON TABLE puntos_expedicion IS 'Puntos de expedición dentro de un establecimiento (Caja 1, Consultorios, etc.)';
COMMENT ON COLUMN puntos_expedicion.ultimo_numero_usado IS 'Control de numeración secuencial para evitar duplicados';

-- ============================================================================
-- 6. MODIFICAR TABLA CONSULTORIOS (Agregar relación con sede)
-- ============================================================================
ALTER TABLE consultorios 
ADD COLUMN IF NOT EXISTS id_sede INTEGER REFERENCES sedes(id_sede) 
    ON DELETE SET NULL ON UPDATE CASCADE;

-- Índice
CREATE INDEX IF NOT EXISTS idx_consultorios_sede ON consultorios(id_sede);

COMMENT ON COLUMN consultorios.id_sede IS 'Sede a la que pertenece el consultorio';

-- ============================================================================
-- 7. MODIFICAR TABLA FACTURAS (Agregar relaciones)
-- ============================================================================
-- Relación con empresa (para datos del emisor)
ALTER TABLE facturas 
ADD COLUMN IF NOT EXISTS id_empresa INTEGER REFERENCES empresa(id_empresa) 
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- Relación con timbrado (para trazabilidad)
ALTER TABLE facturas 
ADD COLUMN IF NOT EXISTS id_timbrado INTEGER REFERENCES timbrados(id_timbrado) 
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- Relación con punto de expedición (para numeración)
ALTER TABLE facturas 
ADD COLUMN IF NOT EXISTS id_punto_expedicion INTEGER REFERENCES puntos_expedicion(id_punto_expedicion) 
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- Índices
CREATE INDEX IF NOT EXISTS idx_facturas_empresa ON facturas(id_empresa);
CREATE INDEX IF NOT EXISTS idx_facturas_timbrado ON facturas(id_timbrado);
CREATE INDEX IF NOT EXISTS idx_facturas_punto_expedicion ON facturas(id_punto_expedicion);

COMMENT ON COLUMN facturas.id_empresa IS 'Empresa emisora de la factura';
COMMENT ON COLUMN facturas.id_timbrado IS 'Timbrado utilizado para la factura';
COMMENT ON COLUMN facturas.id_punto_expedicion IS 'Punto de expedición desde donde se emitió la factura';

-- ============================================================================
-- DATOS INICIALES DE PRUEBA (OPCIONAL)
-- ============================================================================
-- Estos datos son de ejemplo para probar el sistema
-- IMPORTANTE: Reemplazar con datos reales en producción
-- ============================================================================

DO $$
DECLARE
    v_id_empresa INTEGER;
    v_id_sede INTEGER;
    v_id_establecimiento INTEGER;
BEGIN
    -- Insertar Empresa
    INSERT INTO empresa (
        ruc_nit,
        digito_verificador,
        razon_social,
        nombre_comercial,
        tipo_contribuyente,
        departamento,
        distrito,
        ciudad,
        direccion,
        numero_casa,
        codigo_postal,
        telefono,
        celular,
        email,
        sitio_web,
        representante_legal_nombre,
        representante_legal_apellido,
        representante_legal_ci,
        representante_legal_cargo,
        actividad_economica_principal,
        horario_atencion,
        es_principal,
        est_empresa,
        facturador_electronico,
        fecha_habilitacion_sifen,
        grupo_obligatoriedad,
        ambiente_sifen,
        codigo_seguridad_contribuyente,
        creacion_usuario
    ) VALUES (
        '80012345',                    -- ruc_nit (sin guión)
        '6',                           -- digito_verificador
        'CLÍNICA ANGASYS S.A.',        -- razon_social
        'AngaSys Clínica',             -- nombre_comercial
        'persona_juridica',            -- tipo_contribuyente
        'Central',                     -- departamento
        'Asunción',                    -- distrito
        'Asunción',                    -- ciudad
        'Av. Mariscal López 1234',     -- direccion
        '1234',                        -- numero_casa
        '1000',                        -- codigo_postal
        '+595 21 123456',              -- telefono
        '+595 982 123456',             -- celular
        'info@angasys.com.py',         -- email
        'https://www.angasys.com.py',  -- sitio_web
        'Juan',                        -- representante_legal_nombre
        'Pérez',                       -- representante_legal_apellido
        '1234567',                     -- representante_legal_ci
        'Director General',            -- representante_legal_cargo
        'Servicios de salud mental y atención psicológica', -- actividad_economica_principal
        'Lun-Vie: 8:00 - 18:00, Sáb: 8:00 - 12:00', -- horario_atencion
        TRUE,                          -- es_principal
        TRUE,                          -- est_empresa
        TRUE,                          -- facturador_electronico
        '2024-01-01',                  -- fecha_habilitacion_sifen
        1,                             -- grupo_obligatoriedad
        'prueba',                      -- ambiente_sifen (cambiar a 'produccion' cuando esté listo)
        NULL,                          -- codigo_seguridad_contribuyente (CSC - obtener de DNIT)
        1                              -- creacion_usuario
    )
    ON CONFLICT (ruc_nit) DO UPDATE
    SET razon_social = EXCLUDED.razon_social,
        nombre_comercial = EXCLUDED.nombre_comercial
    RETURNING id_empresa INTO v_id_empresa;
    
    IF v_id_empresa IS NULL THEN
        SELECT id_empresa INTO v_id_empresa FROM empresa WHERE ruc_nit = '80012345';
    END IF;
    
    -- Insertar Sede Principal
    INSERT INTO sedes (
        id_empresa,
        des_sede,
        codigo_sede,
        direccion,
        ciudad,
        departamento,
        codigo_postal,
        telefono,
        email,
        horario_atencion,
        es_principal,
        est_sede,
        creacion_usuario
    ) VALUES (
        v_id_empresa,
        'Sede Central',
        'SEDE-001',
        'Av. Mariscal López 1234',
        'Asunción',
        'Central',
        '1000',
        '+595 21 123456',
        'sede.central@angasys.com.py',
        'Lun-Vie: 8:00 - 18:00',
        TRUE,
        TRUE,
        1
    )
    ON CONFLICT (id_empresa, codigo_sede) DO UPDATE
    SET des_sede = EXCLUDED.des_sede,
        direccion = EXCLUDED.direccion
    RETURNING id_sede INTO v_id_sede;
    
    IF v_id_sede IS NULL THEN
        SELECT id_sede INTO v_id_sede FROM sedes WHERE id_empresa = v_id_empresa AND codigo_sede = 'SEDE-001';
    END IF;
    
    -- Insertar Timbrado Principal
    INSERT INTO timbrados (
        id_empresa,
        numero_timbrado,
        fecha_inicio,
        fecha_vencimiento,
        tipo_documento,
        tipo_generacion,
        estado,
        est_timbrado,
        observaciones,
        creacion_usuario
    ) VALUES (
        v_id_empresa,
        '12345678',                    -- numero_timbrado (8 dígitos - ejemplo)
        '2024-01-01',
        '2025-12-31',
        'factura',
        'electronico',
        'activo',
        TRUE,
        'Timbrado para facturación electrónica',
        1
    )
    ON CONFLICT (id_empresa, numero_timbrado) DO NOTHING;
    
    -- Insertar Establecimiento Principal
    INSERT INTO establecimientos (
        id_sede,
        codigo_establecimiento,
        nombre_establecimiento,
        descripcion,
        es_principal,
        est_establecimiento,
        creacion_usuario
    ) VALUES (
        v_id_sede,
        '001',                         -- codigo_establecimiento (3 dígitos - matriz)
        'Establecimiento Matriz',
        'Establecimiento principal de la sede central',
        TRUE,
        TRUE,
        1
    )
    ON CONFLICT (id_sede, codigo_establecimiento) DO UPDATE
    SET nombre_establecimiento = EXCLUDED.nombre_establecimiento
    RETURNING id_establecimiento INTO v_id_establecimiento;
    
    IF v_id_establecimiento IS NULL THEN
        SELECT id_establecimiento INTO v_id_establecimiento 
        FROM establecimientos 
        WHERE id_sede = v_id_sede AND codigo_establecimiento = '001';
    END IF;
    
    -- Insertar Punto de Expedición Principal
    INSERT INTO puntos_expedicion (
        id_establecimiento,
        codigo_punto_expedicion,
        nombre_punto_expedicion,
        descripcion,
        tipo_punto,
        permite_facturacion,
        ultimo_numero_usado,
        serie_actual,
        est_punto_expedicion,
        creacion_usuario
    ) VALUES (
        v_id_establecimiento,
        '001',                         -- codigo_punto_expedicion (3 dígitos)
        'Caja Principal',
        'Punto de expedición principal para facturación',
        'caja',
        TRUE,
        0,                             -- ultimo_numero_usado (inicia en 0)
        NULL,                          -- serie_actual (NULL para serie inicial)
        TRUE,
        1
    )
    ON CONFLICT (id_establecimiento, codigo_punto_expedicion) DO NOTHING;
    
    RAISE NOTICE '✅ Datos de prueba de empresa insertados correctamente';
    RAISE NOTICE '   Empresa ID: %, Sede ID: %, Establecimiento ID: %', v_id_empresa, v_id_sede, v_id_establecimiento;
END $$;

-- ============================================================================
-- NOTAS IMPORTANTES SOBRE DATOS DE PRUEBA
-- ============================================================================
-- 1. Los datos insertados son de EJEMPLO - reemplazar con datos reales
-- 2. El RUC/NIT y número de timbrado son ejemplos
-- 3. El ambiente_sifen está en 'prueba' - cambiar a 'produccion' cuando esté listo
-- 4. El codigo_seguridad_contribuyente (CSC) debe obtenerse de DNIT
-- 5. Las fechas de timbrado deben ajustarse según timbrados reales
-- 6. El certificado digital (.pfx) debe configurarse por separado
-- ============================================================================

-- ============================================================================
-- FIN DEL SCRIPT
-- ============================================================================



