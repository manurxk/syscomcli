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

-- Tabla de pacientes (actualizada)
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    nro_ficha VARCHAR(50) NOT NULL UNIQUE,  -- Nuevo campo para el número de ficha del paciente
    id_persona INT NOT NULL UNIQUE,  -- Vinculado con la tabla personas
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
    descripcion VARCHAR(50) NOT NULL,  -- Ejemplo: "Mañana", "Tarde", "Noche"
    hora_inicio TIME NOT NULL,  -- Hora de inicio del turno
    hora_fin TIME NOT NULL,  -- Hora de fin del turno
    disponible BOOLEAN DEFAULT TRUE  -- Si el turno está disponible o no
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

-- Tabla de disponibilidad_medico (Vincula médicos, días y turnos)
CREATE TABLE disponibilidad_medico (
    id SERIAL PRIMARY KEY,
    id_medico INT NOT NULL,
    id_dia INT NOT NULL,  -- Día de la semana (relación con la tabla dias)
    id_turno INT NOT NULL,  -- Relación con la tabla turnos
    estado BOOLEAN DEFAULT TRUE,  -- Indica si el médico está disponible o no en ese día y turno
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_dia) REFERENCES dias(id) ON DELETE CASCADE,
    FOREIGN KEY (id_turno) REFERENCES turnos(id) ON DELETE CASCADE
);

-- Tabla de agendamiento_medico (Vincula pacientes, médicos, días, turnos y estados de citas)
CREATE TABLE agendamiento_medico (
    id SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_turno INT NOT NULL,
    id_dia INT NOT NULL,
    fecha_agenda DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    estado VARCHAR(50) NOT NULL CHECK (estado IN ('pendiente', 'confirmada', 'anulada')),  -- Estado de la cita
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_turno) REFERENCES turnos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_dia) REFERENCES dias(id) ON DELETE CASCADE
);

-- Tabla de consultorios
CREATE TABLE consultorios (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,  -- Ejemplo: "Consultorio 1", "Consultorio 2"
    ubicacion VARCHAR(100) NOT NULL  -- Ubicación dentro del centro de salud
);

-- Actualización de la tabla agendamiento_medico para vincular consultorios
ALTER TABLE agendamiento_medico
ADD COLUMN id_consultorio INT,
ADD FOREIGN KEY (id_consultorio) REFERENCES consultorios(id) ON DELETE CASCADE;

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

-- Tabla de documentos relacionados a ficha médica del paciente
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

-- Tabla de estado_medico
CREATE TABLE estado_medico (
    id SERIAL PRIMARY KEY,  -- Identificador único
    id_medico INT NOT NULL, -- Vinculado con la tabla de médicos
    estado VARCHAR(50) NOT NULL CHECK (estado IN ('activo', 'inactivo')), -- Estado del médico
    fecha_actualizacion DATE NOT NULL, -- Fecha de la última actualización del estado
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE -- Relación con la tabla de médicos
);


-- 1. Vincular duracion_consulta con citas
ALTER TABLE citas
ADD COLUMN id_duracion INT,
ADD CONSTRAINT fk_duracion_consulta
FOREIGN KEY (id_duracion) REFERENCES duracion_consulta(id) ON DELETE CASCADE;

-- 2. Vincular diagnosticos, tratamientos e instrumentos con documentos_fichas
ALTER TABLE documentos_fichas
ADD COLUMN id_diagnostico INT,
ADD CONSTRAINT fk_diagnostico
FOREIGN KEY (id_diagnostico) REFERENCES diagnosticos(id) ON DELETE CASCADE,
ADD COLUMN id_tratamiento INT,
ADD CONSTRAINT fk_tratamiento
FOREIGN KEY (id_tratamiento) REFERENCES tratamientos(id) ON DELETE CASCADE,
ADD COLUMN id_instrumento INT,
ADD CONSTRAINT fk_instrumento
FOREIGN KEY (id_instrumento) REFERENCES instrumentos(id) ON DELETE CASCADE;

-- 3. Vincular especialidad con medicos
ALTER TABLE medicos
ADD COLUMN id_especialidad INT,
ADD CONSTRAINT fk_especialidad
FOREIGN KEY (id_especialidad) REFERENCES especialidades(id) ON DELETE CASCADE;

ALTER TABLE personas
ADD COLUMN sexo VARCHAR(50) NOT NULL CHECK (sexo IN ('femenino', 'masculino', 'otro')),
ADD COLUMN correo_electronico VARCHAR(100) UNIQUE;
 
 -- Agregar fecha_registro y hora_registro a la tabla personas
ALTER TABLE personas
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla pacientes
ALTER TABLE pacientes
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla medicos
ALTER TABLE medicos
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla empleados
ALTER TABLE empleados
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla duracion_consulta
ALTER TABLE duracion_consulta
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla disponibilidad_medico
ALTER TABLE disponibilidad_medico
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla agendamiento_medico
ALTER TABLE agendamiento_medico
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla consultorios
ALTER TABLE consultorios
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla citas
ALTER TABLE citas
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla documentos_fichas
ALTER TABLE documentos_fichas
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla avisos_recordatorios
ALTER TABLE avisos_recordatorios
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla estados_cita
ALTER TABLE estados_cita
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

-- Agregar fecha_registro y hora_registro a la tabla estado_medico
ALTER TABLE estado_medico
ADD COLUMN fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
ADD COLUMN hora_registro TIME NOT NULL DEFAULT CURRENT_TIME;

ALTER TABLE medicos
ADD COLUMN nro_registro_profesional VARCHAR(50) NOT NULL;
