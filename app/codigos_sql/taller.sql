CREATE TABLE pais (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) UNIQUE NOT NULL
);
CREATE TABLE ciudad (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES pais(id) ON DELETE CASCADE
);
CREATE TABLE barrio (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    id_ciudad INT NOT NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id) ON DELETE CASCADE
);

CREATE TABLE medicos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    documento_identidad VARCHAR(20) UNIQUE NOT NULL,
    registro_profesional VARCHAR(50),
    fecha_nacimiento DATE,
    especialidad VARCHAR(100),
    numero_telefono VARCHAR(20),
    correo_electronico VARCHAR(150),
    ocupacion VARCHAR(100),
    id_pais INT,
    id_ciudad INT,
    id_barrio INT,
    direccion VARCHAR(255),
    sexo VARCHAR(10) CHECK (sexo IN ('Masculino', 'Femenino', 'Otro')),
    estado_civil VARCHAR(20) CHECK (estado_civil IN ('Soltero', 'Casado', 'Viudo', 'Divorciado')),
    contacto_emergencia VARCHAR(100),
    telefono_emergencia VARCHAR(20),
    fecha_registro DATE NOT NULL DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_pais) REFERENCES pais(id) ON DELETE SET NULL,
    FOREIGN KEY (id_ciudad) REFERENCES ciudad(id) ON DELETE SET NULL,
    FOREIGN KEY (id_barrio) REFERENCES barrio(id) ON DELETE SET NULL
);













INSERT INTO pais (id, nombre) VALUES 
(1, 'Paraguay'),
(2, 'Argentina'),
(3, 'Brasil');


INSERT INTO ciudad (id, nombre, id_pais) VALUES 
(1, 'Asunción', 1),
(2, 'Buenos Aires', 2),
(3, 'São Paulo', 3);




INSERT INTO barrio (id, nombre, id_ciudad) VALUES 
(1, 'Villa Morra', 1),
(2, 'Recoleta', 2),
(3, 'Bela Vista', 3);



INSERT INTO medicos (
    nombre, apellido, documento_identidad, registro_profesional, fecha_nacimiento, 
    especialidad, numero_telefono, correo_electronico, ocupacion, id_pais, id_ciudad, 
    id_barrio, direccion, sexo, estado_civil, contacto_emergencia, 
    telefono_emergencia, fecha_registro
) VALUES 
(
    'Juan', 'González', '12345678', 'PROF-001', '1990-05-15',
    'Cardiología', '0981123456', 'juan.gonzalez@gmail.com', 'Médico', 
    1, 1, 1, 'Calle Falsa 123', 'Masculino', 'Soltero', 'María González', 
    '0981987654', CURRENT_DATE
),
(
    'Laura', 'Martínez', '87654321', 'PROF-002', '1988-11-20',
    'Odontología', '0977123456', 'laura.martinez@gmail.com', 'Odontóloga', 
    2, 2, 2, 'Avenida Siempreviva 456', 'Femenino', 'Casado', 'Carlos Martínez', 
    '0987654321', CURRENT_DATE
),
(
    'Pedro', 'Silva', '56473829', 'PROF-003', '1985-08-10',
    'Neurología', '0961122334', 'pedro.silva@gmail.com', 'Médico', 
    3, 3, 3, 'Rua Principal 789', 'Masculino', 'Divorciado', 'Ana Silva', 
    '0911122334', CURRENT_DATE
);
