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

-- Tabla de ocupaciones
CREATE TABLE ocupaciones (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Tabla de especialidades
CREATE TABLE especialidades (
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

-- Tabla de ubicacion (geografía), vincula país, nacionalidad, ciudad y barrio
CREATE TABLE ubicacion (
    id SERIAL PRIMARY KEY,
    id_pais INT,
    id_nacionalidad INT,
    id_ciudad INT,
    id_barrio INT,
    FOREIGN KEY (id_pais) REFERENCES paises(id) ON DELETE CASCADE,
    FOREIGN KEY (id_nacionalidad) REFERENCES nacionalidades(id) ON DELETE CASCADE,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (id_barrio) REFERENCES barrios(id) ON DELETE CASCADE
);

-- Tabla de personas con agregado de estado_civil y vínculo con ubicacion
CREATE TABLE personas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    telefono VARCHAR(20) UNIQUE,
    direccion VARCHAR(255),
    sexo VARCHAR(50) NOT NULL CHECK (sexo IN ('femenino', 'masculino', 'otro')),
    correo_electronico VARCHAR(100) UNIQUE,
    estado_civil VARCHAR(50) NOT NULL CHECK (estado_civil IN ('soltero', 'casado', 'viudo')),  -- Estado civil
    id_ubicacion INT,  -- Relación con la tabla de ubicación
    id_ocupacion INT,  -- Relación con la tabla de ocupaciones
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_ubicacion) REFERENCES ubicacion(id) ON DELETE SET NULL,
    FOREIGN KEY (id_ocupacion) REFERENCES ocupaciones(id) ON DELETE CASCADE
);

-- Tabla de médicos con vínculo a especialidades
CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    id_persona INT NOT NULL UNIQUE,
    id_especialidad INT,  -- Nueva columna para la especialidad
    nro_registro_profesional VARCHAR(50) NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_persona) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id) ON DELETE CASCADE
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
    minutos INT NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME
);

-- Tabla de disponibilidad_medico (Vincula médicos, días y turnos)
CREATE TABLE disponibilidad_medico (
    id SERIAL PRIMARY KEY,
    id_medico INT NOT NULL,
    id_dia INT NOT NULL,  -- Día de la semana (relación con la tabla dias)
    id_turno INT NOT NULL,  -- Relación con la tabla turnos
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
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
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_turno) REFERENCES turnos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_dia) REFERENCES dias(id) ON DELETE CASCADE
);

-- Tabla de consultorios
CREATE TABLE consultorios (
    id SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,  -- Ejemplo: "Consultorio 1", "Consultorio 2"
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME
);

-- Actualización de la tabla agendamiento_medico para vincular consultorios
ALTER TABLE agendamiento_medico
ADD COLUMN id_consultorio INT,
ADD FOREIGN KEY (id_consultorio) REFERENCES consultorios(id) ON DELETE CASCADE;

-- Tabla de citas con vínculo a duracion_consulta
CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_medico INT NOT NULL,
    id_duracion INT,  -- Nueva columna para duración de consulta
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    motivo_consulta VARCHAR(255) NOT NULL,
    estado VARCHAR(50),
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id) ON DELETE CASCADE,
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE,
    FOREIGN KEY (id_duracion) REFERENCES duracion_consulta(id) ON DELETE CASCADE
);

-- Tabla de avisos_recordatorios
CREATE TABLE avisos_recordatorios (
    id SERIAL PRIMARY KEY,
    id_cita INT NOT NULL,
    mensaje TEXT NOT NULL,
    fecha_envio DATE NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    enviado BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (id_cita) REFERENCES citas(id) ON DELETE CASCADE
);

-- Tabla para la gestión de estado_cita (reservación, confirmación, anulación)
CREATE TABLE estados_cita (
    id SERIAL PRIMARY KEY,
    id_cita INT NOT NULL,
    estado VARCHAR(50) NOT NULL,
    fecha_actualizacion DATE NOT NULL,
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_cita) REFERENCES citas(id) ON DELETE CASCADE
);

-- Tabla de estado_medico
CREATE TABLE estado_medico (
    id SERIAL PRIMARY KEY,  -- Identificador único
    id_medico INT NOT NULL, -- Vinculado con la tabla de médicos
    estado VARCHAR(50) NOT NULL CHECK (estado IN ('activo', 'inactivo')), -- Estado del médico
    fecha_actualizacion DATE NOT NULL, -- Fecha de la última actualización del estado
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    hora_registro TIME NOT NULL DEFAULT CURRENT_TIME,
    FOREIGN KEY (id_medico) REFERENCES medicos(id) ON DELETE CASCADE -- Relación con la tabla de médicos
);
