-- ============================================================================
-- FASE 1: TABLAS REFERENCIALES BÁSICAS
-- ============================================================================
-- Este script crea las tablas referenciales básicas del sistema
-- Ejecutar después de: 00_CREAR_BASE_DATOS.sql
-- ============================================================================

-- ============================================================================
-- 1. GÉNEROS
-- ============================================================================
CREATE TABLE IF NOT EXISTS generos (
    id_genero SERIAL PRIMARY KEY,
    des_genero VARCHAR(50) NOT NULL UNIQUE,
    est_genero BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 2. ESTADOS CIVILES
-- ============================================================================
CREATE TABLE IF NOT EXISTS estados_civiles (
    id_estado_civil SERIAL PRIMARY KEY,
    des_estado_civil VARCHAR(50) NOT NULL UNIQUE,
    est_estado_civil BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 3. CIUDADES
-- ============================================================================
CREATE TABLE IF NOT EXISTS ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    des_ciudad VARCHAR(100) NOT NULL UNIQUE,
    est_ciudad BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 4. NIVELES DE INSTRUCCIÓN
-- ============================================================================
CREATE TABLE IF NOT EXISTS niveles_instruccion (
    id_nivel_instruccion SERIAL PRIMARY KEY,
    des_nivel_instruccion VARCHAR(100) NOT NULL UNIQUE,
    est_nivel_instruccion BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 5. PROFESIONES
-- ============================================================================
CREATE TABLE IF NOT EXISTS profesiones (
    id_profesion SERIAL PRIMARY KEY,
    des_profesion VARCHAR(150) NOT NULL UNIQUE,
    est_profesion BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- 6. ESPECIALIDADES
-- ============================================================================
CREATE TABLE IF NOT EXISTS especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    des_especialidad VARCHAR(150) NOT NULL UNIQUE,
    est_especialidad BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50) DEFAULT 'SISTEMA',
    fecha_modificacion TIMESTAMP,
    usuario_modificacion VARCHAR(50)
);

-- ============================================================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_generos_estado ON generos(est_genero);
CREATE INDEX IF NOT EXISTS idx_estados_civiles_estado ON estados_civiles(est_estado_civil);
CREATE INDEX IF NOT EXISTS idx_ciudades_estado ON ciudades(est_ciudad);
CREATE INDEX IF NOT EXISTS idx_niveles_instruccion_estado ON niveles_instruccion(est_nivel_instruccion);
CREATE INDEX IF NOT EXISTS idx_profesiones_estado ON profesiones(est_profesion);
CREATE INDEX IF NOT EXISTS idx_especialidades_estado ON especialidades(est_especialidad);

-- ============================================================================
-- COMENTARIOS EN TABLAS
-- ============================================================================

COMMENT ON TABLE generos IS 'Catálogo de géneros (Masculino, Femenino, No binario, etc.)';
COMMENT ON TABLE estados_civiles IS 'Catálogo de estados civiles (Soltero, Casado, etc.)';
COMMENT ON TABLE ciudades IS 'Catálogo de ciudades de Paraguay';
COMMENT ON TABLE niveles_instruccion IS 'Catálogo de niveles de instrucción educativa';
COMMENT ON TABLE profesiones IS 'Catálogo de profesiones y ocupaciones';
COMMENT ON TABLE especialidades IS 'Catálogo de especialidades médicas/psicológicas';

-- ============================================================================
-- DATOS INICIALES
-- ============================================================================

-- Géneros
INSERT INTO generos (des_genero, est_genero, usuario_creacion) VALUES
    ('MASCULINO', TRUE, 'SISTEMA'),
    ('FEMENINO', TRUE, 'SISTEMA'),
    ('PREFIERO NO DECIR', TRUE, 'SISTEMA')
ON CONFLICT (des_genero) DO NOTHING;

-- Estados civiles
INSERT INTO estados_civiles (des_estado_civil, est_estado_civil, usuario_creacion) VALUES
    ('SOLTERO', TRUE, 'SISTEMA'),
    ('CASADO', TRUE, 'SISTEMA'),
    ('DIVORCIADO', TRUE, 'SISTEMA'),
    ('VIUDO', TRUE, 'SISTEMA'),
    ('UNION LIBRE', TRUE, 'SISTEMA')
ON CONFLICT (des_estado_civil) DO NOTHING;

-- INSERT DE CIUDADES/DISTRITOS DE PARAGUAY
-- Tabla: ciudades

INSERT INTO ciudades (des_ciudad, est_ciudad, usuario_creacion) VALUES
('ASUNCIÓN', TRUE, 'SISTEMA'),
('CONCEPCIÓN', TRUE, 'SISTEMA'),
('BELÉN', TRUE, 'SISTEMA'),
('HORQUETA', TRUE, 'SISTEMA'),
('LORETO', TRUE, 'SISTEMA'),
('SAN CARLOS DEL APA', TRUE, 'SISTEMA'),
('SAN LÁZARO', TRUE, 'SISTEMA'),
('YBY YAÚ', TRUE, 'SISTEMA'),
('AZOTE''Y', TRUE, 'SISTEMA'),
('SARGENTO JOSÉ FÉLIX LÓPEZ', TRUE, 'SISTEMA'),
('SAN ALFREDO', TRUE, 'SISTEMA'),
('PASO BARRETO', TRUE, 'SISTEMA'),
('ARROYITO', TRUE, 'SISTEMA'),
('PASO HORQUETA', TRUE, 'SISTEMA'),
('ITACUÁ', TRUE, 'SISTEMA'),
('SAN PEDRO DEL YCUAMANDYYÚ', TRUE, 'SISTEMA'),
('ANTEQUERA', TRUE, 'SISTEMA'),
('CHORÉ', TRUE, 'SISTEMA'),
('GENERAL ELIZARDO AQUINO', TRUE, 'SISTEMA'),
('ITACURUBÍ DEL ROSARIO', TRUE, 'SISTEMA'),
('LIMA', TRUE, 'SISTEMA'),
('NUEVA GERMANIA', TRUE, 'SISTEMA'),
('SAN ESTANISLAO', TRUE, 'SISTEMA'),
('SAN PABLO', TRUE, 'SISTEMA'),
('TACUATÍ', TRUE, 'SISTEMA'),
('UNIÓN', TRUE, 'SISTEMA'),
('25 DE DICIEMBRE', TRUE, 'SISTEMA'),
('VILLA DEL ROSARIO', TRUE, 'SISTEMA'),
('GENERAL FRANCISCO ISIDORO RESQUÍN', TRUE, 'SISTEMA'),
('YATAITY DEL NORTE', TRUE, 'SISTEMA'),
('GUAJAYVI', TRUE, 'SISTEMA'),
('CAPIIBARY', TRUE, 'SISTEMA'),
('SANTA ROSA DEL AGUARAY', TRUE, 'SISTEMA'),
('YRYBUCUA', TRUE, 'SISTEMA'),
('LIBERACIÓN', TRUE, 'SISTEMA'),
('SAN VICENTE PANCHOLO', TRUE, 'SISTEMA'),
('SAN JOSÉ DEL ROSARIO', TRUE, 'SISTEMA'),
('CAACUPÉ', TRUE, 'SISTEMA'),
('ALTOS', TRUE, 'SISTEMA'),
('ARROYOS Y ESTEROS', TRUE, 'SISTEMA'),
('ATYRÁ', TRUE, 'SISTEMA'),
('CARAGUATAY', TRUE, 'SISTEMA'),
('EMBOSCADA', TRUE, 'SISTEMA'),
('EUSEBIO AYALA', TRUE, 'SISTEMA'),
('ISLA PUCÚ', TRUE, 'SISTEMA'),
('ITACURUBÍ DE LA CORDILLERA', TRUE, 'SISTEMA'),
('JUAN DE MENA', TRUE, 'SISTEMA'),
('LOMA GRANDE', TRUE, 'SISTEMA'),
('MBOCAYATY DEL YHAGUY', TRUE, 'SISTEMA'),
('NUEVA COLOMBIA', TRUE, 'SISTEMA'),
('PIRIBEBUY', TRUE, 'SISTEMA'),
('PRIMERO DE MARZO', TRUE, 'SISTEMA'),
('SAN BERNARDINO', TRUE, 'SISTEMA'),
('SANTA ELENA', TRUE, 'SISTEMA'),
('TOBATÍ', TRUE, 'SISTEMA'),
('VALENZUELA', TRUE, 'SISTEMA'),
('SAN JOSÉ OBRERO', TRUE, 'SISTEMA'),
('VILLARRICA', TRUE, 'SISTEMA'),
('BORJA', TRUE, 'SISTEMA'),
('CAPITÁN MAURICIO JOSÉ TROCHE', TRUE, 'SISTEMA'),
('CORONEL MARTÍNEZ', TRUE, 'SISTEMA'),
('FÉLIX PÉREZ CARDOZO', TRUE, 'SISTEMA'),
('GRAL. EUGENIO A. GARAY', TRUE, 'SISTEMA'),
('INDEPENDENCIA', TRUE, 'SISTEMA'),
('ITAPÉ', TRUE, 'SISTEMA'),
('ITURBE', TRUE, 'SISTEMA'),
('JOSÉ FASSARDI', TRUE, 'SISTEMA'),
('MBOCAYATY', TRUE, 'SISTEMA'),
('NATALICIO TALAVERA', TRUE, 'SISTEMA'),
('ÑUMÍ', TRUE, 'SISTEMA'),
('SAN SALVADOR', TRUE, 'SISTEMA'),
('YATAITY', TRUE, 'SISTEMA'),
('DOCTOR BOTTRELL', TRUE, 'SISTEMA'),
('PASO YOBAI', TRUE, 'SISTEMA'),
('TEBICUARY', TRUE, 'SISTEMA'),
('CORONEL OVIEDO', TRUE, 'SISTEMA'),
('CAAGUAZÚ', TRUE, 'SISTEMA'),
('CARAYAÓ', TRUE, 'SISTEMA'),
('DR. CECILIO BÁEZ', TRUE, 'SISTEMA'),
('SANTA ROSA DEL MBUTUY', TRUE, 'SISTEMA'),
('DR. JUAN MANUEL FRUTOS', TRUE, 'SISTEMA'),
('REPATRIACIÓN', TRUE, 'SISTEMA'),
('NUEVA LONDRES', TRUE, 'SISTEMA'),
('SAN JOAQUÍN', TRUE, 'SISTEMA'),
('SAN JOSÉ DE LOS ARROYOS', TRUE, 'SISTEMA'),
('YHÚ', TRUE, 'SISTEMA'),
('DR. J. EULOGIO ESTIGARRIBIA', TRUE, 'SISTEMA'),
('R.I. 3 CORRALES', TRUE, 'SISTEMA'),
('RAÚL ARSENIO OVIEDO', TRUE, 'SISTEMA'),
('JOSÉ DOMINGO OCAMPOS', TRUE, 'SISTEMA'),
('MARISCAL FRANCISCO SOLANO LÓPEZ', TRUE, 'SISTEMA'),
('LA PASTORA', TRUE, 'SISTEMA'),
('3 DE FEBRERO', TRUE, 'SISTEMA'),
('SIMÓN BOLIVAR', TRUE, 'SISTEMA'),
('VAQUERÍA', TRUE, 'SISTEMA'),
('TEMBIAPORÁ', TRUE, 'SISTEMA'),
('NUEVA TOLEDO', TRUE, 'SISTEMA'),
('CAAZAPÁ', TRUE, 'SISTEMA'),
('ABAÍ', TRUE, 'SISTEMA'),
('BUENA VISTA', TRUE, 'SISTEMA'),
('DR. MOISÉS S. BERTONI', TRUE, 'SISTEMA'),
('GRAL. HIGINIO MORINIGO', TRUE, 'SISTEMA'),
('MACIEL', TRUE, 'SISTEMA'),
('SAN JUAN NEPOMUCENO', TRUE, 'SISTEMA'),
('TAVAÍ', TRUE, 'SISTEMA'),
('YEGROS', TRUE, 'SISTEMA'),
('YUTY', TRUE, 'SISTEMA'),
('3 DE MAYO', TRUE, 'SISTEMA'),
('ENCARNACIÓN', TRUE, 'SISTEMA'),
('BELLA VISTA (ITAPÚA)', TRUE, 'SISTEMA'),
('CAMBYRETÁ', TRUE, 'SISTEMA'),
('CAPITÁN MEZA', TRUE, 'SISTEMA'),
('CAPITÁN MIRANDA', TRUE, 'SISTEMA'),
('NUEVA ALBORADA', TRUE, 'SISTEMA'),
('CARMEN DEL PARANÁ', TRUE, 'SISTEMA'),
('CORONEL BOGADO', TRUE, 'SISTEMA'),
('CARLOS ANTONIO LÓPEZ', TRUE, 'SISTEMA'),
('NATALIO', TRUE, 'SISTEMA'),
('FRAM', TRUE, 'SISTEMA'),
('GENERAL ARTIGAS', TRUE, 'SISTEMA'),
('GENERAL DELGADO', TRUE, 'SISTEMA'),
('HOHENAU', TRUE, 'SISTEMA'),
('JESÚS', TRUE, 'SISTEMA'),
('JOSÉ LEANDRO OVIEDO', TRUE, 'SISTEMA'),
('OBLIGADO', TRUE, 'SISTEMA'),
('MAYOR JULIO DIONISIO OTAÑO', TRUE, 'SISTEMA'),
('SAN COSME Y DAMIÁN', TRUE, 'SISTEMA'),
('SAN PEDRO DEL PARANÁ', TRUE, 'SISTEMA'),
('SAN RAFAEL DEL PARANÁ', TRUE, 'SISTEMA'),
('TRINIDAD', TRUE, 'SISTEMA'),
('EDELIRA', TRUE, 'SISTEMA'),
('TOMÁS ROMERO PEREIRA', TRUE, 'SISTEMA'),
('ALTO VERÁ', TRUE, 'SISTEMA'),
('LA PAZ', TRUE, 'SISTEMA'),
('YATYTAY', TRUE, 'SISTEMA'),
('SAN JUAN DEL PARANÁ', TRUE, 'SISTEMA'),
('PIRAPÓ', TRUE, 'SISTEMA'),
('ITAPÚA POTY', TRUE, 'SISTEMA'),
('SAN JUAN BAUTISTA DE LAS MISIONES', TRUE, 'SISTEMA'),
('AYOLAS', TRUE, 'SISTEMA'),
('SAN IGNACIO', TRUE, 'SISTEMA'),
('SAN MIGUEL', TRUE, 'SISTEMA'),
('SAN PATRICIO', TRUE, 'SISTEMA'),
('SANTA MARÍA', TRUE, 'SISTEMA'),
('SANTA ROSA', TRUE, 'SISTEMA'),
('SANTIAGO', TRUE, 'SISTEMA'),
('VILLA FLORIDA', TRUE, 'SISTEMA'),
('YABEBYRY', TRUE, 'SISTEMA'),
('PARAGUARÍ', TRUE, 'SISTEMA'),
('ACAHAY', TRUE, 'SISTEMA'),
('CAAPUCÚ', TRUE, 'SISTEMA'),
('CABALLERO', TRUE, 'SISTEMA'),
('CARAPEGUÁ', TRUE, 'SISTEMA'),
('ESCOBAR', TRUE, 'SISTEMA'),
('LA COLMENA', TRUE, 'SISTEMA'),
('MBUYAPEY', TRUE, 'SISTEMA'),
('PIRAYÚ', TRUE, 'SISTEMA'),
('QUIINDY', TRUE, 'SISTEMA'),
('QUYQUYHÓ', TRUE, 'SISTEMA'),
('ROQUE GONZALEZ DE SANTA CRUZ', TRUE, 'SISTEMA'),
('SAPUCÁI', TRUE, 'SISTEMA'),
('TEBICUARY-MÍ', TRUE, 'SISTEMA'),
('YAGUARÓN', TRUE, 'SISTEMA'),
('YBYCUÍ', TRUE, 'SISTEMA'),
('YBYTYMÍ', TRUE, 'SISTEMA'),
('MARÍA ANTONIA', TRUE, 'SISTEMA'),
('CIUDAD DEL ESTE', TRUE, 'SISTEMA'),
('PRESIDENTE FRANCO', TRUE, 'SISTEMA'),
('DOMINGO MARTÍNEZ DE IRALA', TRUE, 'SISTEMA'),
('DR. JUAN LEÓN MALLORQUÍN', TRUE, 'SISTEMA'),
('HERNANDARIAS', TRUE, 'SISTEMA'),
('ITAKYRY', TRUE, 'SISTEMA'),
('JUAN E. O''LEARY', TRUE, 'SISTEMA'),
('ÑACUNDAY', TRUE, 'SISTEMA'),
('YGUAZÚ', TRUE, 'SISTEMA'),
('LOS CEDRALES', TRUE, 'SISTEMA'),
('MINGA GUAZÚ', TRUE, 'SISTEMA'),
('SAN CRISTÓBAL', TRUE, 'SISTEMA'),
('SANTA RITA', TRUE, 'SISTEMA'),
('NARANJAL', TRUE, 'SISTEMA'),
('SANTA ROSA DEL MONDAY', TRUE, 'SISTEMA'),
('MINGA PORÁ', TRUE, 'SISTEMA'),
('MBARACAYÚ', TRUE, 'SISTEMA'),
('SAN ALBERTO', TRUE, 'SISTEMA'),
('IRUÑA', TRUE, 'SISTEMA'),
('SANTA FE DEL PARANÁ', TRUE, 'SISTEMA'),
('TAVAPY', TRUE, 'SISTEMA'),
('DR. RAÚL PEÑA', TRUE, 'SISTEMA'),
('AREGUÁ', TRUE, 'SISTEMA'),
('CAPIATÁ', TRUE, 'SISTEMA'),
('FERNANDO DE LA MORA', TRUE, 'SISTEMA'),
('GUARAMBARÉ', TRUE, 'SISTEMA'),
('ITÁ', TRUE, 'SISTEMA'),
('ITAUGUÁ', TRUE, 'SISTEMA'),
('LAMBARÉ', TRUE, 'SISTEMA'),
('LIMPIO', TRUE, 'SISTEMA'),
('LUQUE', TRUE, 'SISTEMA'),
('MARIANO ROQUE ALONSO', TRUE, 'SISTEMA'),
('NUEVA ITALIA', TRUE, 'SISTEMA'),
('ÑEMBY', TRUE, 'SISTEMA'),
('SAN ANTONIO', TRUE, 'SISTEMA'),
('SAN LORENZO', TRUE, 'SISTEMA'),
('VILLA ELISA', TRUE, 'SISTEMA'),
('VILLETA', TRUE, 'SISTEMA'),
('YPACARAÍ', TRUE, 'SISTEMA'),
('YPANÉ', TRUE, 'SISTEMA'),
('J. AUGUSTO SALDÍVAR', TRUE, 'SISTEMA'),
('PILAR', TRUE, 'SISTEMA'),
('ALBERDI', TRUE, 'SISTEMA'),
('CERRITO', TRUE, 'SISTEMA'),
('DESMOCHADOS', TRUE, 'SISTEMA'),
('GRAL. JOSÉ EDUVIGIS DÍAZ', TRUE, 'SISTEMA'),
('GUAZÚ-CUÁ', TRUE, 'SISTEMA'),
('HUMAITÁ', TRUE, 'SISTEMA'),
('ISLA UMBÚ', TRUE, 'SISTEMA'),
('LAURELES', TRUE, 'SISTEMA'),
('MAYOR JOSÉ DEJESÚS MARTÍNEZ', TRUE, 'SISTEMA'),
('PASO DE PATRIA', TRUE, 'SISTEMA'),
('SAN JUAN BAUTISTA DE ÑEEMBUCÚ', TRUE, 'SISTEMA'),
('TACUARAS', TRUE, 'SISTEMA'),
('VILLA FRANCA', TRUE, 'SISTEMA'),
('VILLA OLIVA', TRUE, 'SISTEMA'),
('VILLALBÍN', TRUE, 'SISTEMA'),
('PEDRO JUAN CABALLERO', TRUE, 'SISTEMA'),
('CAPITÁN BADO', TRUE, 'SISTEMA'),
('ZANJA PYTÁ', TRUE, 'SISTEMA'),
('KARAPAÍ', TRUE, 'SISTEMA'),
('CERRO CORÁ', TRUE, 'SISTEMA'),
('SALTO DEL GUAIRÁ', TRUE, 'SISTEMA'),
('CORPUS CHRISTI', TRUE, 'SISTEMA'),
('VILLA CURUGUATY', TRUE, 'SISTEMA'),
('VILLA YGATIMÍ', TRUE, 'SISTEMA'),
('ITANARÁ', TRUE, 'SISTEMA'),
('YPEJHÚ', TRUE, 'SISTEMA'),
('FRANCISCO CABALLERO ALVAREZ', TRUE, 'SISTEMA'),
('KATUETÉ', TRUE, 'SISTEMA'),
('LA PALOMA DEL ESPÍRITU SANTO', TRUE, 'SISTEMA'),
('NUEVA ESPERANZA', TRUE, 'SISTEMA'),
('YASY CAÑY', TRUE, 'SISTEMA'),
('YBYRAROBANÁ', TRUE, 'SISTEMA'),
('YBY PYTÁ', TRUE, 'SISTEMA'),
('MARACANÁ', TRUE, 'SISTEMA'),
('PUERTO ADELA', TRUE, 'SISTEMA'),
('LAUREL', TRUE, 'SISTEMA'),
('BENJAMÍN ACEVAL', TRUE, 'SISTEMA'),
('PUERTO PINASCO', TRUE, 'SISTEMA'),
('VILLA HAYES', TRUE, 'SISTEMA'),
('NANAWA', TRUE, 'SISTEMA'),
('JOSÉ FALCÓN', TRUE, 'SISTEMA'),
('TTE. 1° MANUEL IRALA FERNÁNDEZ', TRUE, 'SISTEMA'),
('TENIENTE ESTEBAN MARTÍNEZ', TRUE, 'SISTEMA'),
('GENERAL JOSÉ MARÍA BRUGUEZ', TRUE, 'SISTEMA'),
('CAMPO ACEVAL', TRUE, 'SISTEMA'),
('NUEVA ASUNCIÓN', TRUE, 'SISTEMA'),
('MARISCAL JOSÉ FÉLIX ESTIGARRIBIA', TRUE, 'SISTEMA'),
('FILADELFIA', TRUE, 'SISTEMA'),
('LOMA PLATA', TRUE, 'SISTEMA'),
('BOQUERÓN', TRUE, 'SISTEMA'),
('FUERTE OLIMPO', TRUE, 'SISTEMA'),
('PUERTO CASADO', TRUE, 'SISTEMA'),
('BAHÍA NEGRA', TRUE, 'SISTEMA'),
('CARMELO PERALTA', TRUE, 'SISTEMA')

ON CONFLICT (des_ciudad) DO NOTHING;

-- Niveles de instrucción
INSERT INTO niveles_instruccion (des_nivel_instruccion, est_nivel_instruccion, usuario_creacion) VALUES
    ('SIN ESTUDIOS', TRUE, 'SISTEMA'),
    ('PRIMARIA COMPLETA', TRUE, 'SISTEMA'),
    ('SECUNDARIA COMPLETA', TRUE, 'SISTEMA'),
    ('TERCIARIO COMPLETO', TRUE, 'SISTEMA'),
    ('UNIVERSITARIO COMPLETO', TRUE, 'SISTEMA'),
    ('POSTGRADO', TRUE, 'SISTEMA'),
    ('MAESTRÍA', TRUE, 'SISTEMA'),
    ('DOCTORADO', TRUE, 'SISTEMA')
ON CONFLICT (des_nivel_instruccion) DO NOTHING;

-- Profesiones comunes
INSERT INTO profesiones (des_profesion, est_profesion, usuario_creacion) VALUES
    ('ESTUDIANTE', TRUE, 'SISTEMA'),
    ('DOCENTE', TRUE, 'SISTEMA'),
    ('COMERCIANTE', TRUE, 'SISTEMA'),
    ('EMPLEADO PÚBLICO', TRUE, 'SISTEMA'),
    ('EMPLEADO PRIVADO', TRUE, 'SISTEMA'),
    ('PROFESIONAL INDEPENDIENTE', TRUE, 'SISTEMA'),
    ('AMA DE CASA', TRUE, 'SISTEMA'),
    ('JUBILADO', TRUE, 'SISTEMA'),
    ('DESEMPLEADO', TRUE, 'SISTEMA')
ON CONFLICT (des_profesion) DO NOTHING;

-- Especialidades psicológicas/médicas
INSERT INTO especialidades (des_especialidad, est_especialidad, usuario_creacion) VALUES
    ('Psicología Clínica', TRUE, 'SISTEMA')
ON CONFLICT (des_especialidad) DO NOTHING;

-- ============================================================================
-- FIN FASE 1
-- ============================================================================


