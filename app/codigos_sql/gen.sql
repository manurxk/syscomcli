-- Crear tabla de generos
CREATE TABLE generos (
    id_genero INT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Crear tabla de estado civiles
CREATE TABLE estado_civiles (
    id_estado_civil INT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);

-- Crear tabla de ciudades
CREATE TABLE ciudades (
    id_ciudad INT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

-- Crear tabla de personas
CREATE TABLE personas (
    id_persona INT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    id_genero INT,
    id_estado_civil INT,
    id_ciudad INT,
    telefono_emergencia VARCHAR(20),
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero),
    FOREIGN KEY (id_estado_civil) REFERENCES estado_civiles(id_estado_civil),
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad)
);

-- Insertar datos de generos
INSERT INTO generos (id_genero, descripcion) VALUES
(1, 'Masculino'),
(2, 'Femenino'),
(3, 'Otro');

-- Insertar datos de estado civiles
INSERT INTO estado_civiles (id_estado_civil, descripcion) VALUES
(1, 'Soltero'),
(2, 'Casado'),
(3, 'Divorciado'),
(4, 'Viudo');

-- Insertar datos de ciudades
INSERT INTO ciudades (id_ciudad, descripcion) VALUES
(1, 'Ciudad de México'),
(2, 'Buenos Aires'),
(3, 'Madrid'),
(4, 'Lima');

-- Insertar datos de personas
INSERT INTO personas (id_persona, nombre, apellido, cedula, id_genero, id_estado_civil, id_ciudad, telefono_emergencia) VALUES
(1, 'Juan', 'Pérez', '1234567890', 1, 1, 1, '555-1234'),
(2, 'Ana', 'Gómez', '0987654321', 2, 2, 2, '555-5678'),
(3, 'Carlos', 'Martínez', '1122334455', 1, 3, 3, '555-8765'),
(4, 'Laura', 'Lopez', '5566778899', 2, 4, 4, '555-4321');
