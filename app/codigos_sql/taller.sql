CREATE TABLE pais (
    id_pais SERIAL PRIMARY KEY,
    nombre_pais VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    nombre_ciudad VARCHAR(100) NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES pais(id_pais) ON DELETE CASCADE
);

CREATE TABLE barrios (
    id_barrio SERIAL PRIMARY KEY,
    nombre_barrio VARCHAR(100) NOT NULL,
    id_ciudad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad) ON DELETE CASCADE
);

CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    registro_profesional VARCHAR(50),
    fecha_nacimiento DATE,
    especialidad VARCHAR(100),
    numero_telefono VARCHAR(20),
    correo_electronico VARCHAR(150),
    ocupacion VARCHAR(100),
    nombre_pais VARCHAR(100),
    nombre_ciudad VARCHAR(100),
    nombre_barrio VARCHAR(100),
    direccion VARCHAR(255),
    sexo VARCHAR(10) CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
    estado_civil VARCHAR(20) CHECK (estado_civil IN ('Soltero', 'Casado', 'Viudo', 'Divorciado')),
    contacto_emergencia VARCHAR(100),
    telefono_emergencia VARCHAR(20),
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE
);

INSERT INTO pais (nombre_pais) VALUES 
('Paraguay');

INSERT INTO ciudades (nombre_ciudad, id_pais) VALUES 
('Asunción', 1);

INSERT INTO barrios (nombre_barrio, id_ciudad) VALUES 
('Centro', 1);

INSERT INTO medicos (
    nombre, apellido, cedula, registro_profesional, fecha_nacimiento, 
    especialidad, numero_telefono, correo_electronico, ocupacion, 
    nombre_pais, nombre_ciudad, nombre_barrio, direccion, sexo, 
    estado_civil, contacto_emergencia, telefono_emergencia
) VALUES 
('María', 'Gomez', '12345678', 'REG001', '1985-06-15', 'Psicología', 
'0981123456', 'maria.gomez@clinica.com', 'Psicóloga', 
'Paraguay', 'Asunción', 'Centro', 'Av. Principal 123', 'Femenino', 
'Soltero', 'Carlos Gomez', '0981987654');

INSERT INTO medicos (
    nombre, apellido, cedula, registro_profesional, fecha_nacimiento, 
    especialidad, numero_telefono, correo_electronico, ocupacion, 
    nombre_pais, nombre_ciudad, nombre_barrio, direccion, sexo, 
    estado_civil, contacto_emergencia, telefono_emergencia
) VALUES 
('Juan', 'Perez', '87654321', 'REG002', '1980-01-20', 'Psicología', 
'0981765432', 'juan.perez@clinica.com', 'Psicólogo', 
'Paraguay', 'Asunción', 'Centro', 'Calle 14 de Mayo', 'Masculino', 
'Casado', 'Ana Perez', '0981543782');

INSERT INTO medicos (
    nombre, apellido, cedula, registro_profesional, fecha_nacimiento, 
    especialidad, numero_telefono, correo_electronico, ocupacion, 
    nombre_pais, nombre_ciudad, nombre_barrio, direccion, sexo, 
    estado_civil, contacto_emergencia, telefono_emergencia
) VALUES 
('Laura', 'Lopez', '56781234', 'REG003', '1992-03-10', 'Psicología', 
'0978123456', 'laura.lopez@clinica.com', 'Psicóloga', 
'Paraguay', 'Asunción', 'Centro', 'Av. Colon 456', 'Femenino', 
'Divorciado', 'Martin Lopez', '0981789654');
