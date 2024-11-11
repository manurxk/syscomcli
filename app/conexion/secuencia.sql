-- Tabla de países
CREATE TABLE paises (
    id SERIAL PRIMARY KEY,
    nombre_pais VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de nacionalidades
CREATE TABLE nacionalidades (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de estado_civil
CREATE TABLE estados_civiles (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de sexos
CREATE TABLE sexos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE CHECK (descripcion IN ('femenino', 'masculino', 'otro'))
);

-- Tabla de ocupaciones
CREATE TABLE ocupaciones (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de ciudades
CREATE TABLE ciudades (
    id SERIAL PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL UNIQUE,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES paises(id) ON DELETE CASCADE
);

-- Tabla de barrios
CREATE TABLE barrios (
    id SERIAL PRIMARY KEY,
    nombre_barrio VARCHAR(100) NOT NULL UNIQUE,
    id_ciudad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id) ON DELETE CASCADE
);

-- Tabla de personas
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    direccion VARCHAR(255),
    id_ciudad INT,
    id_pais INT,
    id_nacionalidad INT,
    id_estado_civil INT,
    id_sexo INT,
    id_ocupacion INT,  -- Nueva columna para ocupación
    id_barrio INT,  -- Nueva columna para barrio
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id) ON DELETE SET NULL,
    FOREIGN KEY (id_pais) REFERENCES paises(id) ON DELETE SET NULL,
    FOREIGN KEY (id_nacionalidad) REFERENCES nacionalidades(id) ON DELETE SET NULL,
    FOREIGN KEY (id_estado_civil) REFERENCES estados_civiles(id) ON DELETE SET NULL,
    FOREIGN KEY (id_sexo) REFERENCES sexos(id) ON DELETE SET NULL,
    FOREIGN KEY (id_ocupacion) REFERENCES ocupaciones(id) ON DELETE CASCADE,  -- Eliminar personas al eliminar ocupación
    FOREIGN KEY (id_barrio) REFERENCES barrios(id) ON DELETE SET NULL  -- Eliminar personas al eliminar barrio
);

-- Tabla de pacientes
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    id_persona INT NOT NULL UNIQUE,
    FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
);

-- Tabla de médicos
CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    id_persona INT NOT NULL UNIQUE,
    especialidad VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    email VARCHAR(100) UNIQUE,
    FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
);

-- Tabla de empleados
CREATE TABLE empleados (
    id SERIAL PRIMARY KEY,
    id_persona INT NOT NULL UNIQUE,
    cargo VARCHAR(100) NOT NULL,
    fecha_contratacion DATE NOT NULL,
    salario DECIMAL(10, 2),
    FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE
);

-- Tabla de diagnósticos
CREATE TABLE diagnosticos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de instrumentos
CREATE TABLE instrumentos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de especialidades
CREATE TABLE especialidades (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de tratamientos
CREATE TABLE tratamientos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(255) NOT NULL UNIQUE
);

-- Tabla de turnos
CREATE TABLE turnos (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Tabla de días
CREATE TABLE dias (
    id SERIAL PRIMARY KEY,
    nombre_dia VARCHAR(10) NOT NULL UNIQUE CHECK (nombre_dia IN ('Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo'))
);

-- Tabla de duración_consulta
CREATE TABLE duracion_consulta (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE,
    minutos INT NOT NULL
);

-- Tabla de citas
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo_consulta VARCHAR(255) NOT NULL,
    estado VARCHAR(50),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE
);

-- Tabla de documentos relacionados a ficha médica del paciente (actualizada)
CREATE TABLE documentos_fichas (
    id SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    tipo_documento VARCHAR(100),
    descripcion TEXT,
    ruta_archivo VARCHAR(255),  -- Almacenar la ruta del archivo
    fecha_subida DATE NOT NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Tabla de avisos_recordatorios
CREATE TABLE avisos_recordatorios (
    id SERIAL PRIMARY KEY,
    id_cita INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATE NOT NULL,
    enviado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_cita) REFERENCES citas(id) ON DELETE CASCADE
);

-- Tabla para la gestión de estado_cita (reservación, confirmación, anulación)
CREATE TABLE estados_cita (
    id SERIAL PRIMARY KEY,
    id_cita INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_actualizacion DATE NOT NULL,
    FOREIGN KEY (id_cita) REFERENCES citas(id) ON DELETE CASCADE
);
