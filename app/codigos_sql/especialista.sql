-- Crear tabla estados_civiles
CREATE TABLE estado_civiles (
    id_estado_civil SERIAL PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL UNIQUE
);

-- Crear tabla ciudades
CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Crear tabla especialidades
CREATE TABLE especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL UNIQUE
);

-- Insertar datos en estados_civiles
INSERT INTO estados_civiles (descripcion) VALUES ('Soltero');
INSERT INTO estados_civiles (descripcion) VALUES ('Casado');
INSERT INTO estados_civiles (descripcion) VALUES ('Divorciado');

-- Insertar datos en ciudades (Departamento Central)
INSERT INTO ciudades (nombre_ciudad) VALUES ('Asunción');
INSERT INTO ciudades (nombre_ciudad) VALUES ('Luque');
INSERT INTO ciudades (nombre_ciudad) VALUES ('San Lorenzo');
INSERT INTO ciudades (nombre_ciudad) VALUES ('Capiatá');
INSERT INTO ciudades (nombre_ciudad) VALUES ('Fernando de la Mora');

-- Insertar datos en especialidades (Psicología)
INSERT INTO especialidades (nombre_especialidad) VALUES ('Psicología Clínica');
INSERT INTO especialidades (nombre_especialidad) VALUES ('Psicología Educacional');
INSERT INTO especialidades (nombre_especialidad) VALUES ('Psicología Organizacional');

-- Crear tabla especialistas
CREATE TABLE especialistas ( 
    id_especialista SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) NOT NULL UNIQUE,
    sexo VARCHAR(10) CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')), 
    telefono VARCHAR(15) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR(255),
    correo VARCHAR(100) NOT NULL UNIQUE,
    matricula VARCHAR(50) NOT NULL UNIQUE,
    id_estado_civil INT NOT NULL,
    id_ciudad INT NOT NULL,
    id_especialidad INT NOT NULL
);

-- Agregar las claves foráneas después de la definición de columnas
ALTER TABLE especialistas
    ADD CONSTRAINT fk_especialista_estado_civil FOREIGN KEY (id_estado_civil) REFERENCES estados_civiles(id_estado_civil) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT fk_especialista_ciudad FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad) ON DELETE CASCADE ON UPDATE CASCADE,
    ADD CONSTRAINT fk_especialista_especialidad FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) ON DELETE CASCADE ON UPDATE CASCADE;


-- Insertar datos en especialistas
-- Insertar un especialista
INSERT INTO especialistas (
    nombre, 
    apellido, 
    cedula, 
    sexo, 
    telefono, 
    fecha_nacimiento, 
    direccion, 
    correo, 
    matricula, 
    id_estado_civil, 
    id_ciudad, 
    id_especialidad
) 
VALUES (
    'Juan', 
    'Pérez', 
    '1234567890', 
    'Masculino', 
    '0987654321', 
    '1985-06-15', 
    'Av. Falcón 123', 
    'juan.perez@mail.com', 
    'MATR12345', 
    (SELECT id_estado_civil FROM estados_civiles WHERE descripcion = 'Soltero'), 
    (SELECT id_ciudad FROM ciudades WHERE nombre_ciudad = 'Asunción'), 
    (SELECT id_especialidad FROM especialidades WHERE nombre_especialidad = 'Psicología Clínica')
);

-- Insertar otro especialista
INSERT INTO especialistas (
    nombre, 
    apellido, 
    cedula, 
    sexo, 
    telefono, 
    fecha_nacimiento, 
    direccion, 
    correo, 
    matricula, 
    id_estado_civil, 
    id_ciudad, 
    id_especialidad
) 
VALUES (
    'María', 
    'López', 
    '9876543210', 
    'Femenino', 
    '0981122334', 
    '1990-02-20', 
    'Av. España 456', 
    'maria.lopez@mail.com', 
    'MATR67890', 
    (SELECT id_estado_civil FROM estados_civiles WHERE descripcion = 'Casado'), 
    (SELECT id_ciudad FROM ciudades WHERE nombre_ciudad = 'Luque'), 
    (SELECT id_especialidad FROM especialidades WHERE nombre_especialidad = 'Psicología Educacional')
);
