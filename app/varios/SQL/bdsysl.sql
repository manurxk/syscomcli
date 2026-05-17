ORDEN RECOMENDADO DE ABM
1. PRIMERO: ABM de PERSONAS ❌ (NO directamente)
NO deberías crear un ABM de Personas independiente porque:
Las personas solo existen como Pacientes o como parte de Funcionarios
No hay "personas sueltas" en tu sistema
Sería confuso para el usuario

2. CREAR: ABM de PACIENTES ✅ (Prioridad 1)
Este ABM maneja TODO lo relacionado al paciente:
Al dar de ALTA un paciente:
Creas el registro en personas (datos personales completos)
Automáticamente creas el registro en pacientes (vinculado a la persona)
Si marcas "es menor", habilitas campos adicionales y guardas en pacientes_menores
Formulario incluye:
Todos los campos de persona (nombre, apellido, cédula, teléfono, etc.)
Selects de referenciales (ciudad, género, estado civil, etc.)
Checkbox "¿Es menor de edad?" que muestra/oculta campos de tutores
Número de historia clínica
Observaciones
Al MODIFICAR:
Actualizas datos en personas y pacientes
Si cambia de adulto a menor o viceversa, manejas pacientes_menores
Al dar de BAJA:
Lógica: ¿eliminación física o desactivación?
Considerar si tiene citas asociadas

3. CREAR: ABM de ESPECIALISTAS ✅ (Prioridad 2)
Este ABM es MÁS COMPLEJO porque involucra 3 tablas:
Al dar de ALTA un especialista:
Creas el registro en personas (datos personales)
Creas el registro en funcionarios (vinculando persona + cargo)
Creas el registro en especialistas (vinculando funcionario + matrícula + especialidad)
OPCIONALMENTE: Crear usuario si necesita acceder al sistema
Formulario incluye:
Datos personales (nombre, apellido, cédula, etc.)
Selects de referenciales
Cargo (select de tabla cargos)
Matrícula profesional (único)
Especialidad (select)
Color de agenda
Duración de sesión por defecto
Checkbox "¿Crear usuario para acceso al sistema?"
Si marca, pedir: username, contraseña, grupo
Al MODIFICAR:
Actualizas en personas, funcionarios y especialistas
Usuario se maneja aparte (en otro ABM)
Al dar de BAJA:
Desactivar en funcionarios (campo fun_estado = FALSE)
Considerar si tiene citas programadas
¿Desactivar también su usuario?

4. CREAR: ABM de USUARIOS ✅ (Prioridad 3)
Este ABM maneja SOLO el acceso al sistema:
Al dar de ALTA un usuario:
Seleccionas un funcionario existente (combo que muestre funcionarios sin usuario)
Asignas username (validar que no exista)
Asignas contraseña (encriptada)
Asignas grupo (Administrador, Recepcionista, Especialista)
Estado activo
Formulario muestra:
Datos del funcionario (solo lectura: nombre, cargo)
Username (editable, único)
Contraseña (editable, con confirmación)
Grupo (select)
Estado (activo/inactivo)
Al MODIFICAR:
Cambiar contraseña
Cambiar grupo
Activar/desactivar
Resetear intentos de login
NO se puede cambiar el funcionario asociado
Al dar de BAJA:
Desactivar (usu_estado = FALSE) en lugar de eliminar
Mantener historial de auditoría

-- ============================================
-- TABLAS REFERENCIALES - FORMATO UNIFICADO
-- ============================================

CREATE TABLE generos (
    id_genero SERIAL PRIMARY KEY,
    des_genero VARCHAR(50) NOT NULL UNIQUE,
    est_genero BOOLEAN DEFAULT TRUE
);

INSERT INTO generos (des_genero) VALUES
('Masculino'),
('Femenino'),
('No binario'),
('Prefiero no decir');


CREATE TABLE estados_civiles (
    id_estado_civil SERIAL PRIMARY KEY,
    des_estado_civil VARCHAR(50) NOT NULL UNIQUE,
    est_estado_civil BOOLEAN DEFAULT TRUE
);

INSERT INTO estados_civiles (des_estado_civil) VALUES
('Soltero'),
('Casado'),
('Divorciada'),
('Viuda'),
('Unión libre'),
('Separada');


CREATE TABLE ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    des_ciudad VARCHAR(100) NOT NULL,
    est_ciudad BOOLEAN DEFAULT TRUE
);

INSERT INTO ciudades (des_ciudad) VALUES
('Asunción'),
('Ciudad del Este'),
('Encarnación'),
('Luque'),
('San Lorenzo'),
('Lambaré'),
('Fernando de la Mora');


CREATE TABLE niveles_instruccion (
    id_nivel_instruccion SERIAL PRIMARY KEY,
    des_nivel_instruccion VARCHAR(100) NOT NULL UNIQUE,
    est_nivel_instruccion BOOLEAN DEFAULT TRUE
);

INSERT INTO niveles_instruccion (des_nivel_instruccion) VALUES
('Sin estudios'),
('Primaria incompleta'),
('Primaria completa'),
('Secundaria incompleta'),
('Secundaria completa'),
('Terciario incompleto'),
('Terciario completo'),
('Universitario incompleto'),
('Universitario completo'),
('Postgrado'),
('Maestría'),
('Doctorado');


CREATE TABLE profesiones (
    id_profesion SERIAL PRIMARY KEY,
    des_profesion VARCHAR(150) NOT NULL UNIQUE,
    est_profesion BOOLEAN DEFAULT TRUE
);

INSERT INTO profesiones (des_profesion) VALUES
('Estudiante'),
('Docente'),
('Comerciante'),
('Empleado público'),
('Empleado privado'),
('Profesional independiente'),
('Ama de casa'),
('Jubilado'),
('DesempleadO');


CREATE TABLE especialidades (
    id_especialidad SERIAL PRIMARY KEY,
    des_especialidad VARCHAR(150) NOT NULL UNIQUE,
    est_especialidad BOOLEAN DEFAULT TRUE
);

INSERT INTO especialidades (des_especialidad) VALUES
('Psicología Clínica'),
('Psicología Infantil'),
('Psicología de Adolescentes'),
('Psicología de Adultos'),
('Neuropsicología'),
('Psicología Organizacional'),
('Terapia Cognitivo-Conductual'),
('Terapia Familiar'),
('Psicología Educacional');

-- ============================================
-- TABLAS DE AUTENTICACIÓN - FORMATO UNIFICADO
-- ============================================

CREATE TABLE grupos (
    id_grupo SERIAL PRIMARY KEY,
    des_grupo VARCHAR(60) UNIQUE NOT NULL,
    est_grupo BOOLEAN DEFAULT TRUE
);

INSERT INTO grupos (des_grupo) VALUES 
('Administrador'),
('Recepcionista'),
('Especialista'),
('Ventas');

select * from grupos;


CREATE TABLE modulos (
    id_modulo SERIAL PRIMARY KEY,
    des_modulo VARCHAR(60) UNIQUE NOT NULL,
    est_modulo BOOLEAN DEFAULT TRUE
);

INSERT INTO modulos (des_modulo) VALUES
('Gestión de Usuario'),
('Agendamiento'),
('Consultorios'),
('Reportes'),
('Ventas'),
('Configuración');


CREATE TABLE cargos (
    id_cargo SERIAL PRIMARY KEY,
    des_cargo VARCHAR(60) UNIQUE NOT NULL,
    est_cargo BOOLEAN DEFAULT TRUE
);

INSERT INTO cargos (des_cargo) VALUES
('Administrador'),
('Recepcionista'),
('Especialista'),
('Ventas');


-- ============================================
-- TABLA BASE: PERSONAS
-- ============================================

-- ============================================
-- PERSONAS
-- ============================================

CREATE TABLE personas (
    id_persona SERIAL PRIMARY KEY,
    per_nombre VARCHAR(100) NOT NULL,
    per_apellido VARCHAR(100) NOT NULL,
    per_cedula VARCHAR(20) UNIQUE NOT NULL,
    per_telefono VARCHAR(20)NOT NULL,
    per_correo VARCHAR(100),
    per_domicilio TEXT,
    per_fecha_nacimiento DATE,
    
    -- Referencias
    id_genero INT,
    id_estado_civil INT,
    id_ciudad INT,
    id_ciudad_nacimiento INT,
    id_nivel_instruccion INT,
    id_profesion INT,
    
    -- Auditoría
    per_fecha_inscripcion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_genero) REFERENCES generos(id_genero),
    FOREIGN KEY (id_estado_civil) REFERENCES estados_civiles(id_estado_civil),
    FOREIGN KEY (id_ciudad) REFERENCES ciudades(id_ciudad),
    FOREIGN KEY (id_ciudad_nacimiento) REFERENCES ciudades(id_ciudad),
    FOREIGN KEY (id_nivel_instruccion) REFERENCES niveles_instruccion(id_nivel_instruccion),
    FOREIGN KEY (id_profesion) REFERENCES profesiones(id_profesion)
);

CREATE INDEX idx_cedula ON personas (per_cedula);
CREATE INDEX idx_nombre ON personas (per_nombre, per_apellido);


-- ============================================
-- FUNCIONARIOS
-- ============================================

CREATE TABLE funcionarios(
    id_funcionario SERIAL PRIMARY KEY,
    id_persona INT UNIQUE NOT NULL,  
    id_cargo INT NOT NULL,
    fun_estado BOOLEAN NOT NULL DEFAULT TRUE,
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT,
    
    FOREIGN KEY(id_persona) REFERENCES personas(id_persona) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(id_cargo) REFERENCES cargos(id_cargo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- ============================================
-- USUARIOS
-- ============================================

CREATE TABLE usuarios(
    id_usuario SERIAL PRIMARY KEY,
    usu_nick VARCHAR(10) UNIQUE NOT NULL,
    usu_clave VARCHAR(300) NOT NULL,
    usu_nro_intentos INT NOT NULL DEFAULT 0,
    id_funcionario INT NOT NULL,
    id_grupo INT NOT NULL,
    usu_estado BOOLEAN NOT NULL DEFAULT TRUE,
    
    FOREIGN KEY(id_funcionario) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(id_grupo) REFERENCES grupos(id_grupo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- ============================================
-- PAGINAS
-- ============================================

CREATE TABLE paginas(
    id_pagina SERIAL PRIMARY KEY,
    des_pagina VARCHAR(60) UNIQUE NOT NULL,
    pag_direcc TEXT NOT NULL,
    est_pagina BOOLEAN NOT NULL,
    id_modulo INT NOT NULL,
    
    FOREIGN KEY(id_modulo) REFERENCES modulos(id_modulo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- ============================================
-- PERMISOS
-- ============================================

CREATE TABLE permisos(
    id_pagina INT,
    id_grupo INT,
    leer BOOLEAN NOT NULL,
    insertar BOOLEAN NOT NULL,
    editar BOOLEAN NOT NULL,
    borrar BOOLEAN NOT NULL,
    
    PRIMARY KEY(id_pagina, id_grupo),
    FOREIGN KEY(id_pagina) REFERENCES paginas(id_pagina) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY(id_grupo) REFERENCES grupos(id_grupo) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);


-- ============================================
-- PACIENTES
-- ============================================

CREATE TABLE pacientes (
    id_paciente SERIAL PRIMARY KEY,
    id_persona INT UNIQUE NOT NULL,
    pac_es_menor BOOLEAN DEFAULT FALSE,
    pac_historia_clinica VARCHAR(50) UNIQUE,  
    pac_observaciones TEXT,
    
    FOREIGN KEY (id_persona) REFERENCES personas(id_persona) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE INDEX idx_historia ON pacientes(pac_historia_clinica);


CREATE TABLE pacientes_menores (
    id_paciente_menor SERIAL PRIMARY KEY,
    id_paciente INT UNIQUE NOT NULL,
    pam_nom_madre VARCHAR(100),
    pam_tel_madre VARCHAR(20),
    pam_nom_padre VARCHAR(100),
    pam_tel_padre VARCHAR(20),
    pam_educacion VARCHAR(100),
    pam_colegio VARCHAR(150),
    pam_tel_colegio VARCHAR(20),
    
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente) 
        ON DELETE CASCADE
);


-- ============================================
-- ESPECIALISTAS
-- ============================================

CREATE TABLE especialistas (
    id_especialista SERIAL PRIMARY KEY,
    id_funcionario INT UNIQUE NOT NULL,  
    esp_matricula VARCHAR(50) UNIQUE NOT NULL,
    id_especialidad INT,
    esp_color_agenda VARCHAR(7) DEFAULT '#3498db',
    esp_duracion_sesion_default INT DEFAULT 60,  
    
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);



-- ============================================
-- INSERTAR PERSONAS (4 pacientes + 3 funcionarios)
-- ============================================

-- FUNCIONARIOS (Administrador, Recepcionista, Especialista)
INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono) VALUES
('Carlos', 'Ramírez', '1234567', '0981111111'),  -- Admin
('Lucía', 'Gómez', '2345678', '0981222222'),    -- Recepcionista
('Jorge', 'Benítez', '3456789', '0981333333');  -- Psicólogo especialista

-- PACIENTES (3 adultos + 2 niños)
INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono) VALUES
('Ana', 'Martínez', '4567890', '0981444444'),   -- Paciente adulto
('Pedro', 'Lopez', '5678901', '0981555555'),    -- Paciente adulto
('María', 'Fernández', '6789012', '0981666666'),-- Paciente adulto
('Sofía', 'García', '7890123', '0981777777'),   -- Paciente niña
('Diego', 'Torres', '8901234', '0981888888');   -- Paciente niño


-- ============================================
-- FUNCIONARIOS (se vinculan a personas y cargos)
-- ============================================

-- Suponiendo cargos:
-- 1 = Administrador, 2 = Recepcionista, 3 = Especialista
INSERT INTO funcionarios (id_persona, id_cargo) VALUES
(1, 1), -- Carlos -> Admin
(2, 2), -- Lucía -> Recepcionista
(3, 3); -- Jorge -> Especialista


-- ============================================
-- USUARIOS (Administrador, Recepcionista, Especialista)
-- ============================================

-- Suponiendo grupos:
-- 1 = Administrador, 2 = Recepcionista, 3 = Especialista
INSERT INTO usuarios (usu_nick, usu_clave, id_funcionario, id_grupo) VALUES
('admin', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 1, 1),
('recep1', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 2, 2),
('psico1', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 3, 3);


-- ============================================
-- PACIENTES (adultos y niños)
-- ============================================

-- Adultos
INSERT INTO pacientes (id_persona, pac_es_menor, pac_historia_clinica, pac_observaciones) VALUES
(4, FALSE, 'HC001', 'Chequeo general'),
(5, FALSE, 'HC002', 'Consulta por estrés'),
(6, FALSE, 'HC003', 'Evaluación psicológica');

-- Niños
INSERT INTO pacientes (id_persona, pac_es_menor, pac_historia_clinica, pac_observaciones) VALUES
(7, TRUE, 'HC004', 'Problemas de conducta'),
(8, TRUE, 'HC005', 'Dificultades escolares');


-- ============================================
-- PACIENTES MENORES (datos de padres)
-- ============================================

INSERT INTO pacientes_menores (id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre, pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio) VALUES
(4, 'Laura García', '0981999999', 'Luis García', '0981888777', 'Primaria', 'Colegio Central', '021222333'),
(5, 'Marta Torres', '0981777666', 'Carlos Torres', '0981666555', 'Primaria', 'Colegio San Juan', '021444555');


-- ============================================
-- ESPECIALISTAS (dos vinculados a funcionarios)
-- ============================================

-- Suponiendo especialidades: 1 = Psicología Clínica
INSERT INTO especialistas (id_funcionario, esp_matricula, id_especialidad) VALUES
(3, 'PSI-001', 1);











select * from pacientes;
select * from personas;



ALTER TABLE especialidades
DROP COLUMN descripcion;






ALTER TABLE especialistas 
DROP COLUMN esp_duracion_sesion_default;


-- Eliminar la columna id_especialidad de especialistas
ALTER TABLE especialistas 
DROP COLUMN id_especialidad;

-- Crear tabla intermedia para múltiples especialidades
CREATE TABLE especialista_especialidades (
    id SERIAL PRIMARY KEY,
    id_especialista INT NOT NULL,
    id_especialidad INT NOT NULL,
    fecha_asignacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
        ON DELETE RESTRICT,
    
    UNIQUE(id_especialista, id_especialidad)
);

CREATE INDEX idx_especialista_esp ON especialista_especialidades(id_especialista);

-- Ahora tu tabla especialistas queda así:
CREATE TABLE especialistas (
    id_especialista SERIAL PRIMARY KEY,
    id_funcionario INT UNIQUE NOT NULL,  
    esp_matricula VARCHAR(50) UNIQUE NOT NULL,
    esp_color_agenda VARCHAR(7) DEFAULT '#3498db',
    
    FOREIGN KEY (id_funcionario) REFERENCES funcionarios(id_funcionario) 
        ON DELETE RESTRICT ON UPDATE CASCADE
);



-- Paso 1: Insertar persona
INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono, per_correo, 
                      per_domicilio, per_fecha_nacimiento, id_genero, id_estado_civil, 
                      id_ciudad, id_ciudad_nacimiento, id_nivel_instruccion, id_profesion)
VALUES ('Gloria', 'González', '4567855590', '0981234567', 'maria.gonzalez@clinica.com',
        'Av. España 1234', '1985-06-15', 1, 2, 1, 1, 5, 2)
RETURNING id_persona;
-- Supongamos que retorna id_persona = 1

-- Paso 2: Insertar funcionario
INSERT INTO funcionarios (id_persona, id_cargo, fun_estado)
VALUES (21, 3, TRUE)
RETURNING id_funcionario;
-- Supongamos que retorna id_funcionario = 1

-- Paso 3: Insertar especialista
INSERT INTO especialistas (id_funcionario, esp_matricula, esp_color_agenda)
VALUES (4, 'MAT-PSI-2024-001', '#2ecc71')
RETURNING id_especialista;
-- Supongamos que retorna id_especialista = 1

-- Paso 4: Asignar especialidades (múltiples)
INSERT INTO especialista_especialidades (id_especialista, id_especialidad)
VALUES 
    (1, 1),  -- Psicología Clínica
    (1, 3);  -- Neuropsicología



select * from cargos;






-- ============================================
-- MODIFICACIONES A LA TABLA USUARIOS
-- ============================================

-- 1. Agregar constraint UNIQUE a id_funcionario
-- (Un funcionario solo puede tener un usuario)
ALTER TABLE usuarios 
ADD CONSTRAINT usuarios_id_funcionario_unique UNIQUE (id_funcionario);

-- 2. Expandir el campo username de 10 a 30 caracteres
ALTER TABLE usuarios 
ALTER COLUMN usu_nick TYPE VARCHAR(30);

-- 3. Agregar campos de auditoría
ALTER TABLE usuarios 
ADD COLUMN creacion_fecha DATE DEFAULT CURRENT_DATE,
ADD COLUMN creacion_hora TIME DEFAULT CURRENT_TIME,
ADD COLUMN creacion_usuario INT,
ADD COLUMN modificacion_fecha DATE,
ADD COLUMN modificacion_hora TIME,
ADD COLUMN modificacion_usuario INT;

-- 4. Agregar foreign key para auditoría (opcional)
-- Solo si quieres rastrear qué usuario hizo el cambio
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_creacion_usuario 
    FOREIGN KEY (creacion_usuario) REFERENCES usuarios(id_usuario) 
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_modificacion_usuario 
    FOREIGN KEY (modificacion_usuario) REFERENCES usuarios(id_usuario) 
    ON DELETE SET NULL ON UPDATE CASCADE;

-- Verificar cambios
\d usuarios



CREATE TABLE consultorios (
    id_consultorio SERIAL PRIMARY KEY,
    des_consultorio VARCHAR(100) NOT NULL UNIQUE,
    est_consultorio BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT
);

CREATE INDEX idx_consultorio_estado ON consultorios(est_consultorio);

-- Inserciones
INSERT INTO consultorios (des_consultorio, est_consultorio) 
VALUES 
('Consultorio 1', TRUE),
('Consultorio 2', TRUE);



CREATE TABLE dias_semana (
    id_dia_semana SERIAL PRIMARY KEY,
    des_dia_semana VARCHAR(15) NOT NULL UNIQUE,
    dia_orden INT NOT NULL UNIQUE, -- Para ordenar correctamente
    est_dia_semana BOOLEAN DEFAULT TRUE
);

-- Datos
INSERT INTO dias_semana (dCREATE TABLE agenda_cabecera (
    id_agenda SERIAL PRIMARY KEY,
    id_consultorio INT NOT NULL,
    id_especialista INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_dia_semana INT NOT NULL, -- CAMBIO: ahora FK
    age_hora_inicio TIME NOT NULL,
    age_hora_fin TIME NOT NULL,
    age_duracion_turno INT NOT NULL,
    age_cupos_totales INT NOT NULL,
    age_fecha_vigencia_desde DATE NOT NULL,
    age_fecha_vigencia_hasta DATE,
    age_observaciones TEXT,
    est_agenda BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT,
    
    FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_dia_semana) REFERENCES dias_semana(id_dia_semana)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    UNIQUE(id_consultorio, id_especialista, id_dia_semana, age_hora_inicio)
);

CREATE INDEX idx_agenda_especialista ON agenda_cabecera(id_especialista);
CREATE INDEX idx_agenda_consultorio ON agenda_cabecera(id_consultorio);
CREATE INDEX idx_agenda_dia ON agenda_cabecera(id_dia_semana, est_agenda);
CREATE INDEX idx_agenda_vigencia ON agenda_cabecera(age_fecha_vigencia_desde, age_fecha_vigencia_hasta);

-- Inserciones ajustadas
INSERT INTO agenda_cabecera (
    id_consultorio, id_especialista, id_especialidad, 
    id_dia_semana, age_hora_inicio, age_hora_fin, 
    age_duracion_turno, age_cupos_totales, 
    age_fecha_vigencia_desde, age_observaciones, est_agenda
) 
VALUES 
(1, 1, 1, 1, '08:00', '12:00', 30, 8, '2025-01-01', 'Agenda de fonoaudiología - mañana', TRUE), -- 1=lunes
(1, 1, 1, 3, '14:00', '18:00', 45, 5, '2025-01-01', 'Agenda de fonoaudiología - tarde', TRUE); -- 3=miercoleses_dia_semana, dia_orden, est_dia_semana) VALUES
('lunes', 1, TRUE),
('martes', 2, TRUE),
('miercoles', 3, TRUE),
('jueves', 4, TRUE),
('viernes', 5, TRUE),
('sabado', 6, TRUE),
('domingo', 7, TRUE);






📂 Estructura de Carpetas Completa
CLAUSYS/
├── app/
│   ├── __init__.py                          # App factory + config
│   │
│   ├── config.py                            # Configuraciones por ambiente
│   │
│   ├── rutas/                               # BLUEPRINTS
│   │   ├── __init__.py
│   │   │
│   │   ├── seguridad/                       # Autenticación
│   │   │   ├── __init__.py
│   │   │   └── login.py                     # Blueprint: login, logout, inicio
│   │   │
│   │   ├── gestionar_personas/
│   │   │   ├── __init__.py
│   │   │   ├── paciente/
│   │   │   │   ├── __init__.py
│   │   │   │   └── paciente_rutas.py        # CRUD pacientes
│   │   │   ├── funcionario/
│   │   │   │   ├── __init__.py
│   │   │   │   └── funcionario_rutas.py
│   │   │   └── medico/
│   │   │       ├── __init__.py
│   │   │       └── medico_rutas.py
│   │   │
│   │   ├── agendamiento/
│   │   │   ├── __init__.py
│   │   │   ├── agendamiento_vista.py        # Vista principal módulo
│   │   │   ├── agenda_medica_rutas.py       # Submodulo
│   │   │   └── cita_rutas.py                # Submodulo
│   │   │
│   │   ├── consultorio/
│   │   │   ├── __init__.py
│   │   │   ├── consultorio_vista.py         # Vista principal
│   │   │   ├── consulta_rutas.py
│   │   │   └── diagnostico_rutas.py
│   │   │
│   │   ├── ventas/
│   │   │   ├── __init__.py
│   │   │   ├── ventas_vista.py              # Vista principal
│   │   │   ├── venta_rutas.py
│   │   │   └── caja_rutas.py
│   │   │
│   │   └── referenciales/
│   │       ├── __init__.py
│   │       ├── especialidad/
│   │       ├── ciudad/
│   │       └── ...
│   │
│   ├── dao/                                  # Acceso a datos
│   │   ├── __init__.py
│   │   ├── seguridad/
│   │   │   ├── __init__.py
│   │   │   └── usuario_dao.py
│   │   ├── gestionar_personas/
│   │   │   ├── paciente_dao.py
│   │   │   ├── funcionario_dao.py
│   │   │   └── medico_dao.py
│   │   └── ...
│   │
│   ├── forms/                                # Formularios WTForms
│   │   ├── __init__.py
│   │   ├── auth_forms.py                     # Login, registro
│   │   ├── paciente_forms.py
│   │   └── ...
│   │
│   ├── utils/                                # Utilidades
│   │   ├── __init__.py
│   │   ├── decorators.py                     # @role_required, etc
│   │   ├── validators.py                     # Validaciones custom
│   │   └── helpers.py                        # Funciones auxiliares
│   │
│   ├── models/                               # Modelos (opcional si usas ORM)
│   │   ├── __init__.py
│   │   └── usuario.py
│   │
│   ├── templates/
│   │   ├── base.html                         # Template base
│   │   ├── errores/
│   │   │   ├── 404.html
│   │   │   ├── 403.html
│   │   │   └── csrf_error.html
│   │   │
│   │   ├── seguridad/
│   │   │   ├── login.html
│   │   │   └── inicio.html                   # Dashboard según rol
│   │   │
│   │   ├── agendamiento/
│   │   │   ├── index.html                    # Vista principal módulo
│   │   │   ├── agenda_medica/
│   │   │   │   ├── index.html
│   │   │   │   ├── crear.html
│   │   │   │   └── editar.html
│   │   │   └── cita/
│   │   │       └── ...
│   │   │
│   │   ├── consultorio/
│   │   │   ├── index.html
│   │   │   └── ...
│   │   │
│   │   ├── ventas/
│   │   │   ├── index.html
│   │   │   └── ...
│   │   │
│   │   ├── gestionar_personas/
│   │   │   ├── paciente/
│   │   │   ├── funcionario/
│   │   │   └── medico/
│   │   │
│   │   └── referenciales/
│   │       └── ...
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   └── vendor/
│   │
│   └── conexion/
│       └── conexion.py
│
├── .env                                      # Variables de entorno
├── .env.example                              # Template para .env
├── .gitignore
├── requirements.txt
└── run.py                                    # Entry point


CREATE TABLE consultorios (
    id_consultorio SERIAL PRIMARY KEY,
    des_consultorio VARCHAR(100) NOT NULL UNIQUE,
    est_consultorio BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT
);

CREATE INDEX idx_consultorio_estado ON consultorios(est_consultorio);

-- Inserciones
INSERT INTO consultorios (des_consultorio, est_consultorio) 
VALUES 
('Consultorio 1', TRUE),
('Consultorio 2', TRUE);



CREATE TABLE dias_semana (
    id_dia_semana SERIAL PRIMARY KEY,
    des_dia_semana VARCHAR(15) NOT NULL UNIQUE,
    dia_orden INT NOT NULL UNIQUE, -- Para ordenar correctamente
    est_dia_semana BOOLEAN DEFAULT TRUE
);

-- Datos
INSERT INTO dias_semana (des_dia_semana, dia_orden, est_dia_semana) VALUES
('lunes', 1, TRUE),
('martes', 2, TRUE),
('miercoles', 3, TRUE),
('jueves', 4, TRUE),
('viernes', 5, TRUE),
('sabado', 6, TRUE),
('domingo', 7, TRUE);







-- ============================================
-- MODIFICACIONES A LA TABLA USUARIOS
-- ============================================

-- 1. Agregar constraint UNIQUE a id_funcionario
-- (Un funcionario solo puede tener un usuario)
ALTER TABLE usuarios 
ADD CONSTRAINT usuarios_id_funcionario_unique UNIQUE (id_funcionario);

-- 2. Expandir el campo username de 10 a 30 caracteres
ALTER TABLE usuarios 
ALTER COLUMN usu_nick TYPE VARCHAR(30);

-- 3. Agregar campos de auditoría
ALTER TABLE usuarios 
ADD COLUMN creacion_fecha DATE DEFAULT CURRENT_DATE,
ADD COLUMN creacion_hora TIME DEFAULT CURRENT_TIME,
ADD COLUMN creacion_usuario INT,
ADD COLUMN modificacion_fecha DATE,
ADD COLUMN modificacion_hora TIME,
ADD COLUMN modificacion_usuario INT;

-- 4. Agregar foreign key para auditoría (opcional)
-- Solo si quieres rastrear qué usuario hizo el cambio
ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_creacion_usuario 
    FOREIGN KEY (creacion_usuario) REFERENCES usuarios(id_usuario) 
    ON DELETE SET NULL ON UPDATE CASCADE;

ALTER TABLE usuarios
ADD CONSTRAINT fk_usuarios_modificacion_usuario 
    FOREIGN KEY (modificacion_usuario) REFERENCES usuarios(id_usuario) 
    ON DELETE SET NULL ON UPDATE CASCADE;

-- Verificar cambios
\d usuarios




SFRS
- =====================================================
-- TABLA: AGENDA_HORARIOS
-- Descripción: Configuración de horarios de atención 
--              por especialista, día y consultorio
-- =====================================================

CREATE TABLE agenda_horarios (
    id_agenda_horario SERIAL PRIMARY KEY,
    
    -- Referencias principales
    id_especialista INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_consultorio INT NOT NULL,
    id_dia_semana INT NOT NULL,
    
    -- Configuración de horarios
    agen_hora_inicio TIME NOT NULL,
    agen_hora_fin TIME NOT NULL,
    agen_duracion_turno INT NOT NULL CHECK (agen_duracion_turno IN (30, 60, 120)), -- minutos
    agen_turno VARCHAR(10) NOT NULL CHECK (agen_turno IN ('MAÑANA', 'TARDE', 'NOCHE')),
    agen_cupos_totales INT NOT NULL,
    
    -- Vigencia
    agen_fecha_desde DATE NOT NULL DEFAULT CURRENT_DATE,
    agen_fecha_hasta DATE, -- NULL = indefinido
    
    -- Estado
    est_agenda_horario BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT,
    
    -- Foreign Keys
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_dia_semana) REFERENCES dias_semana(id_dia_semana)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Validaciones
    CONSTRAINT chk_hora_fin_mayor CHECK (agen_hora_fin > agen_hora_inicio),
    CONSTRAINT chk_cupos_positivos CHECK (agen_cupos_totales > 0),
    CONSTRAINT chk_fecha_vigencia CHECK (agen_fecha_hasta IS NULL OR agen_fecha_hasta >= agen_fecha_desde),
    
    -- Evitar solapamientos: mismo especialista, mismo día, mismo consultorio, horarios que se cruzan
    CONSTRAINT uk_especialista_dia_horario UNIQUE (id_especialista, id_dia_semana, id_consultorio, agen_hora_inicio)
);

-- Índices para optimizar consultas
CREATE INDEX idx_agenda_especialista ON agenda_horarios(id_especialista);
CREATE INDEX idx_agenda_consultorio ON agenda_horarios(id_consultorio);
CREATE INDEX idx_agenda_dia ON agenda_horarios(id_dia_semana);
CREATE INDEX idx_agenda_activa ON agenda_horarios(est_agenda_horario) WHERE est_agenda_horario = TRUE;
CREATE INDEX idx_agenda_vigencia ON agenda_horarios(agen_fecha_desde, agen_fecha_hasta);

-- =====================================================
-- FUNCIÓN: Calcular turno según hora de inicio
-- =====================================================

CREATE OR REPLACE FUNCTION calcular_turno(hora_inicio TIME)
RETURNS VARCHAR(10) AS $$
BEGIN
    IF hora_inicio >= '06:00:00' AND hora_inicio < '13:00:00' THEN
        RETURN 'MAÑANA';
    ELSIF hora_inicio >= '13:00:00' AND hora_inicio < '19:00:00' THEN
        RETURN 'TARDE';
    ELSIF hora_inicio >= '19:00:00' OR hora_inicio < '06:00:00' THEN
        RETURN 'NOCHE';
    END IF;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- =====================================================
-- FUNCIÓN: Calcular cantidad de cupos
-- =====================================================

CREATE OR REPLACE FUNCTION calcular_cupos(hora_inicio TIME, hora_fin TIME, duracion_turno INT)
RETURNS INT AS $$
DECLARE
    minutos_totales INT;
BEGIN
    -- Calcular diferencia en minutos
    minutos_totales := EXTRACT(EPOCH FROM (hora_fin - hora_inicio)) / 60;
    
    -- Retornar cantidad de cupos (división entera)
    RETURN minutos_totales / duracion_turno;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- =====================================================
-- TRIGGER: Auto-calcular turno y cupos antes de insertar/actualizar
-- =====================================================

CREATE OR REPLACE FUNCTION trigger_calcular_agenda()
RETURNS TRIGGER AS $$
BEGIN
    -- Calcular turno automáticamente
    NEW.agen_turno := calcular_turno(NEW.agen_hora_inicio);
    
    -- Calcular cupos automáticamente
    NEW.agen_cupos_totales := calcular_cupos(NEW.agen_hora_inicio, NEW.agen_hora_fin, NEW.agen_duracion_turno);
    
    -- Validar que el especialista tenga la especialidad asignada
    IF NOT EXISTS (
        SELECT 1 FROM especialista_especialidades 
        WHERE id_especialista = NEW.id_especialista 
        AND id_especialidad = NEW.id_especialidad
    ) THEN
        RAISE EXCEPTION 'El especialista no tiene asignada la especialidad seleccionada';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_calcular_agenda_before_insert_update
    BEFORE INSERT OR UPDATE ON agenda_horarios
    FOR EACH ROW
    EXECUTE FUNCTION trigger_calcular_agenda();

-- =====================================================
-- COMENTARIOS EN TABLAS Y COLUMNAS
-- =====================================================

COMMENT ON TABLE agenda_horarios IS 'Configuración de horarios de atención por especialista';
COMMENT ON COLUMN agenda_horarios.agen_duracion_turno IS 'Duración en minutos: 30, 60 o 120';
COMMENT ON COLUMN agenda_horarios.agen_turno IS 'Calculado automáticamente: MAÑANA, TARDE o NOCHE';
COMMENT ON COLUMN agenda_horarios.agen_cupos_totales IS 'Calculado automáticamente según horario y duración';
COMMENT ON COLUMN agenda_horarios.agen_fecha_hasta IS 'NULL indica vigencia indefinida';


-- =====================================================
-- SISTEMA DE CITAS - SCRIPT COMPLETO
-- =====================================================

-- =====================================================
-- 1. TABLA DE ESTADOS DE CITAS
-- =====================================================

CREATE TABLE estados_citas (
    id_estado_cita SERIAL PRIMARY KEY,
    est_cita_nombre VARCHAR(50) UNIQUE NOT NULL,
    est_cita_descripcion TEXT,
    est_cita_color VARCHAR(7),
    est_cita_activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_estado_cita_activo ON estados_citas(est_cita_activo) WHERE est_cita_activo = TRUE;

-- Insertar estados básicos
INSERT INTO estados_citas (est_cita_nombre, est_cita_descripcion, est_cita_color) VALUES
    ('AGENDADA', 'Cita agendada, pendiente de confirmación', '#ffc107'),
    ('CONFIRMADA', 'Cita confirmada por el paciente', '#28a745'),
    ('COMPLETADA', 'Cita realizada exitosamente', '#17a2b8'),
    ('CANCELADA', 'Cita cancelada con anticipación', '#6c757d'),
    ('INASISTENCIA', 'Paciente no asistió sin avisar', '#dc3545'),
    ('REPROGRAMADA', 'Cita movida a otra fecha', '#fd7e14');

COMMENT ON TABLE estados_citas IS 'Catálogo de estados posibles para las citas';
COMMENT ON COLUMN estados_citas.est_cita_color IS 'Color hexadecimal para representación visual en la UI';

-- =====================================================
-- 2. TABLA PRINCIPAL: CITAS
-- =====================================================

CREATE TABLE citas (
    id_cita SERIAL PRIMARY KEY,
    
    -- Referencias principales
    id_paciente INT NOT NULL,
    id_agenda_horario INT NOT NULL,
    id_especialista INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_estado_cita INT NOT NULL DEFAULT 1, -- AGENDADA por defecto
    
    -- Fecha y hora específicas
    cita_fecha DATE NOT NULL,
    cita_hora_inicio TIME NOT NULL,
    cita_hora_fin TIME NOT NULL,
    
    -- Tipo de cita (simple: boolean)
    cita_es_primera_vez BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Información de agendamiento
    cita_motivo TEXT, -- Motivo por el cual agenda
    cita_observaciones TEXT, -- Observaciones generales
    
    -- Control de confirmación
    cita_fecha_confirmacion TIMESTAMP,
    cita_usuario_confirmacion INT,
    
    -- Para tratamientos futuros (opcional, puede quedar NULL)
    id_contrato INT,
    cita_numero_sesion INT,
    
    -- Control
    cita_activo BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    cita_creacion_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cita_creacion_usuario INT NOT NULL,
    cita_modificacion_fecha TIMESTAMP,
    cita_modificacion_usuario INT,
    
    -- Foreign Keys
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_agenda_horario) REFERENCES agenda_horarios(id_agenda_horario)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_estado_cita) REFERENCES estados_citas(id_estado_cita)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    -- Validaciones
    CONSTRAINT chk_hora_fin_mayor CHECK (cita_hora_fin > cita_hora_inicio),
    CONSTRAINT chk_numero_sesion_positivo CHECK (cita_numero_sesion IS NULL OR cita_numero_sesion > 0),
    
    -- Evitar duplicados: mismo especialista, misma fecha/hora
    CONSTRAINT uk_especialista_fecha_hora UNIQUE (id_especialista, cita_fecha, cita_hora_inicio)
);

-- Índices para optimización
CREATE INDEX idx_cita_paciente ON citas(id_paciente);
CREATE INDEX idx_cita_agenda ON citas(id_agenda_horario);
CREATE INDEX idx_cita_especialista ON citas(id_especialista);
CREATE INDEX idx_cita_especialidad ON citas(id_especialidad);
CREATE INDEX idx_cita_fecha ON citas(cita_fecha);
CREATE INDEX idx_cita_estado ON citas(id_estado_cita);
CREATE INDEX idx_cita_fecha_hora ON citas(cita_fecha, cita_hora_inicio);
CREATE INDEX idx_cita_activa ON citas(cita_activo) WHERE cita_activo = TRUE;
CREATE INDEX idx_cita_primera_vez ON citas(cita_es_primera_vez) WHERE cita_es_primera_vez = TRUE;

-- Comentarios
COMMENT ON TABLE citas IS 'Registro de citas médicas agendadas';
COMMENT ON COLUMN citas.cita_es_primera_vez IS 'TRUE = Primera vez, FALSE = Seguimiento/Control';
COMMENT ON COLUMN citas.cita_motivo IS 'Motivo de consulta expresado al agendar';
COMMENT ON COLUMN citas.cita_observaciones IS 'Observaciones o notas adicionales';
COMMENT ON COLUMN citas.cita_numero_sesion IS 'Número de sesión para controles de tratamiento';

-- =====================================================
-- 3. FUNCIÓN: VALIDAR CUPOS DISPONIBLES
-- =====================================================

CREATE OR REPLACE FUNCTION validar_cupo_disponible()
RETURNS TRIGGER AS $$
DECLARE
    v_cupos_totales INT;
    v_cupos_ocupados INT;
    v_estado_cancelada INT;
BEGIN
    -- Obtener ID del estado CANCELADA
    SELECT id_estado_cita INTO v_estado_cancelada
    FROM estados_citas 
    WHERE est_cita_nombre = 'CANCELADA';
    
    -- Obtener cupos totales de la agenda
    SELECT agen_cupos_totales INTO v_cupos_totales
    FROM agenda_horarios
    WHERE id_agenda_horario = NEW.id_agenda_horario;
    
    IF v_cupos_totales IS NULL THEN
        RAISE EXCEPTION 'No existe configuración de agenda para este horario';
    END IF;
    
    -- Contar citas ya agendadas (excluyendo canceladas)
    SELECT COUNT(*) INTO v_cupos_ocupados
    FROM citas
    WHERE id_especialista = NEW.id_especialista
        AND cita_fecha = NEW.cita_fecha
        AND cita_hora_inicio = NEW.cita_hora_inicio
        AND id_estado_cita != v_estado_cancelada
        AND id_cita != COALESCE(NEW.id_cita, 0) -- Excluir la misma cita en UPDATE
        AND cita_activo = TRUE;
    
    -- Validar disponibilidad
    IF v_cupos_ocupados >= v_cupos_totales THEN
        RAISE EXCEPTION 'No hay cupos disponibles para este horario (Cupos: %, Ocupados: %)', 
            v_cupos_totales, v_cupos_ocupados;
    END IF;
    
    -- Auto-calcular hora_fin si no viene (60 min después)
    IF NEW.cita_hora_fin IS NULL OR NEW.cita_hora_fin <= NEW.cita_hora_inicio THEN
        NEW.cita_hora_fin := NEW.cita_hora_inicio + INTERVAL '60 minutes';
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_validar_cupo_before_insert_update
    BEFORE INSERT OR UPDATE ON citas
    FOR EACH ROW
    EXECUTE FUNCTION validar_cupo_disponible();

COMMENT ON FUNCTION validar_cupo_disponible() IS 'Valida que haya cupos disponibles antes de crear o modificar una cita';

-- =====================================================
-- 4. FUNCIÓN: REGISTRAR CONFIRMACIÓN AUTOMÁTICA
-- =====================================================

CREATE OR REPLACE FUNCTION registrar_confirmacion_cita()
RETURNS TRIGGER AS $$
DECLARE
    v_estado_confirmada INT;
BEGIN
    -- Obtener ID del estado CONFIRMADA
    SELECT id_estado_cita INTO v_estado_confirmada
    FROM estados_citas 
    WHERE est_cita_nombre = 'CONFIRMADA';
    
    -- Si pasa a CONFIRMADA y no tenía fecha de confirmación
    IF NEW.id_estado_cita = v_estado_confirmada 
       AND OLD.id_estado_cita != v_estado_confirmada
       AND NEW.cita_fecha_confirmacion IS NULL THEN
        
        NEW.cita_fecha_confirmacion := CURRENT_TIMESTAMP;
        NEW.cita_usuario_confirmacion := NEW.cita_modificacion_usuario;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_registrar_confirmacion
    BEFORE UPDATE ON citas
    FOR EACH ROW
    WHEN (NEW.id_estado_cita IS DISTINCT FROM OLD.id_estado_cita)
    EXECUTE FUNCTION registrar_confirmacion_cita();

COMMENT ON FUNCTION registrar_confirmacion_cita() IS 'Registra automáticamente la fecha y usuario que confirmó la cita';

-- =====================================================
-- 5. FUNCIÓN: OBTENER CUPOS DISPONIBLES POR ESPECIALIDAD
-- =====================================================

CREATE OR REPLACE FUNCTION obtener_cupos_por_especialidad(
    p_id_especialidad INT,
    p_fecha_inicio DATE,
    p_fecha_fin DATE
)
RETURNS TABLE (
    id_especialista INT,
    especialista_nombre TEXT,
    especialista_color VARCHAR,
    dia_semana VARCHAR,
    fecha_especifica DATE,
    hora_inicio TIME,
    hora_fin TIME,
    turno VARCHAR,
    cupos_totales INT,
    cupos_ocupados BIGINT,
    cupos_disponibles BIGINT,
    id_agenda_horario INT
) AS $$
DECLARE
    v_estado_cancelada INT;
BEGIN
    -- Obtener ID del estado CANCELADA
    SELECT id_estado_cita INTO v_estado_cancelada
    FROM estados_citas WHERE est_cita_nombre = 'CANCELADA';
    
    RETURN QUERY
    SELECT 
        e.id_especialista,
        CONCAT(p.per_nombre, ' ', p.per_apellido) as especialista_nombre,
        e.esp_color_agenda,
        ds.dia_nombre,
        d.fecha_especifica,
        ah.agen_hora_inicio,
        ah.agen_hora_fin,
        ah.agen_turno,
        ah.agen_cupos_totales,
        COUNT(c.id_cita) as cupos_ocupados,
        (ah.agen_cupos_totales - COUNT(c.id_cita)) as cupos_disponibles,
        ah.id_agenda_horario
    FROM agenda_horarios ah
    JOIN especialistas e ON ah.id_especialista = e.id_especialista
    JOIN especialista_especialidades ee ON e.id_especialista = ee.id_especialista
    JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
    JOIN personas p ON f.id_persona = p.id_persona
    JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
    -- Generar fechas específicas del rango
    CROSS JOIN LATERAL (
        SELECT fecha::DATE as fecha_especifica
        FROM generate_series(p_fecha_inicio, p_fecha_fin, '1 day'::interval) fecha
        WHERE EXTRACT(DOW FROM fecha) = (ah.id_dia_semana - 1)
    ) d
    LEFT JOIN citas c ON c.id_especialista = e.id_especialista
        AND c.cita_fecha = d.fecha_especifica
        AND c.cita_hora_inicio = ah.agen_hora_inicio
        AND c.id_estado_cita != v_estado_cancelada
        AND c.cita_activo = TRUE
    WHERE ee.id_especialidad = p_id_especialidad
        AND ah.est_agenda_horario = TRUE
        AND ah.agen_fecha_desde <= d.fecha_especifica
        AND (ah.agen_fecha_hasta IS NULL OR ah.agen_fecha_hasta >= d.fecha_especifica)
    GROUP BY e.id_especialista, p.per_nombre, p.per_apellido, e.esp_color_agenda,
             ds.dia_nombre, d.fecha_especifica, ah.agen_hora_inicio, ah.agen_hora_fin, 
             ah.agen_turno, ah.agen_cupos_totales, ah.id_agenda_horario
    HAVING (ah.agen_cupos_totales - COUNT(c.id_cita)) > 0
    ORDER BY d.fecha_especifica, ah.agen_hora_inicio;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obtener_cupos_por_especialidad IS 'Retorna todos los cupos disponibles para una especialidad en un rango de fechas';

-- =====================================================
-- 6. FUNCIÓN: OBTENER CUPOS DISPONIBLES POR ESPECIALISTA
-- =====================================================

CREATE OR REPLACE FUNCTION obtener_cupos_por_especialista(
    p_id_especialista INT,
    p_fecha_inicio DATE,
    p_fecha_fin DATE
)
RETURNS TABLE (
    dia_semana VARCHAR,
    fecha_especifica DATE,
    hora_inicio TIME,
    hora_fin TIME,
    turno VARCHAR,
    cupos_totales INT,
    cupos_ocupados BIGINT,
    cupos_disponibles BIGINT,
    id_agenda_horario INT
) AS $$
DECLARE
    v_estado_cancelada INT;
BEGIN
    -- Obtener ID del estado CANCELADA
    SELECT id_estado_cita INTO v_estado_cancelada
    FROM estados_citas WHERE est_cita_nombre = 'CANCELADA';
    
    RETURN QUERY
    SELECT 
        ds.dia_nombre,
        d.fecha_especifica,
        ah.agen_hora_inicio,
        ah.agen_hora_fin,
        ah.agen_turno,
        ah.agen_cupos_totales,
        COUNT(c.id_cita) as cupos_ocupados,
        (ah.agen_cupos_totales - COUNT(c.id_cita)) as cupos_disponibles,
        ah.id_agenda_horario
    FROM agenda_horarios ah
    JOIN dias_semana ds ON ah.id_dia_semana = ds.id_dia_semana
    -- Generar fechas específicas del rango
    CROSS JOIN LATERAL (
        SELECT fecha::DATE as fecha_especifica
        FROM generate_series(p_fecha_inicio, p_fecha_fin, '1 day'::interval) fecha
        WHERE EXTRACT(DOW FROM fecha) = (ah.id_dia_semana - 1)
    ) d
    LEFT JOIN citas c ON c.id_especialista = ah.id_especialista
        AND c.cita_fecha = d.fecha_especifica
        AND c.cita_hora_inicio = ah.agen_hora_inicio
        AND c.id_estado_cita != v_estado_cancelada
        AND c.cita_activo = TRUE
    WHERE ah.id_especialista = p_id_especialista
        AND ah.est_agenda_horario = TRUE
        AND ah.agen_fecha_desde <= d.fecha_especifica
        AND (ah.agen_fecha_hasta IS NULL OR ah.agen_fecha_hasta >= d.fecha_especifica)
    GROUP BY ds.dia_nombre, d.fecha_especifica, ah.agen_hora_inicio, ah.agen_hora_fin, 
             ah.agen_turno, ah.agen_cupos_totales, ah.id_agenda_horario
    HAVING (ah.agen_cupos_totales - COUNT(c.id_cita)) > 0
    ORDER BY d.fecha_especifica, ah.agen_hora_inicio;
END;
$$ LANGUAGE plpgsql;

COMMENT ON FUNCTION obtener_cupos_por_especialista IS 'Retorna todos los cupos disponibles para un especialista específico en un rango de fechas';

-- =====================================================
-- 7. EJEMPLOS DE INSERCIÓN DE CITAS
-- =====================================================

-- =====================================================
-- EJEMPLO 1: CITA DE PRIMERA VEZ
-- =====================================================
-- Escenario: Nuevo paciente llama para agendar primera consulta

-- Paso 1: Crear la persona
INSERT INTO personas (
    per_nombre, 
    per_apellido, 
    per_cedula, 
    per_telefono, 
    per_fecha_nacimiento,
    id_genero
)
VALUES (
    'Carlos',
    'Ramírez',
    '3456789',
    '0981111222',
    '1990-05-15',
    1  -- Masculino
)
RETURNING id_persona;
-- Supongamos que retorna id_persona = 22

-- Paso 2: Crear el paciente
INSERT INTO pacientes (
    id_persona,
    pac_es_menor,
    pac_observaciones
)
VALUES (
    22,
    FALSE,
    'Paciente nuevo - Derivado por médico clínico'
)
RETURNING id_paciente;
-- Supongamos que retorna id_paciente = 10

-- Paso 3: Crear la cita de primera vez
-- (Asumiendo que ya consultamos los cupos disponibles y seleccionamos uno)
INSERT INTO citas (
    id_paciente,
    id_agenda_horario,
    id_especialista,
    id_especialidad,
    id_estado_cita,
    cita_fecha,
    cita_hora_inicio,
    cita_hora_fin,
    cita_es_primera_vez,
    cita_motivo,
    cita_observaciones,
    cita_creacion_usuario
)
VALUES (
    10,                     -- id_paciente creado arriba
    1,                      -- id_agenda_horario (obtenido de la consulta de cupos)
    1,                      -- id_especialista
    1,                      -- id_especialidad (Psicología Clínica)
    1,                      -- id_estado_cita (AGENDADA)
    '2025-10-20',          -- Lunes 20 de octubre
    '09:00:00',
    '10:00:00',
    TRUE,                   -- Es primera vez
    'Ansiedad y problemas de sueño',
    'Paciente solicita urgencia en la atención',
    1                       -- Usuario que crea la cita (recepcionista)
);

-- =====================================================
-- EJEMPLO 2: CITA DE SEGUIMIENTO
-- =====================================================
-- Escenario: Paciente existente que ya tuvo consultas anteriores

-- Paso 1: Buscar el paciente (no hace falta crear, ya existe)
-- SELECT id_paciente FROM pacientes WHERE id_persona = (
--     SELECT id_persona FROM personas WHERE per_cedula = '4567855590'
-- );
-- Supongamos que existe id_paciente = 5

-- Paso 2: Crear la cita de seguimiento
INSERT INTO citas (
    id_paciente,
    id_agenda_horario,
    id_especialista,
    id_especialidad,
    id_estado_cita,
    cita_fecha,
    cita_hora_inicio,
    cita_hora_fin,
    cita_es_primera_vez,
    cita_motivo,
    cita_observaciones,
    cita_numero_sesion,
    cita_creacion_usuario
)
VALUES (
    5,                      -- id_paciente existente
    1,                      -- id_agenda_horario
    1,                      -- id_especialista (mismo especialista)
    1,                      -- id_especialidad
    2,                      -- id_estado_cita (CONFIRMADA - paciente ya confirmó)
    '2025-10-27',          -- Lunes siguiente
    '09:00:00',
    '10:00:00',
    FALSE,                  -- NO es primera vez (seguimiento)
    'Control de evolución del tratamiento',
    'Paciente reporta mejoras en síntomas de ansiedad',
    3,                      -- Sesión número 3 del seguimiento
    1                       -- Usuario que crea la cita
);

-- =====================================================
-- 8. CONSULTAS ÚTILES PARA VERIFICAR
-- =====================================================

-- Ver todas las citas agendadas con información completa
SELECT 
    c.id_cita,
    CONCAT(p.per_nombre, ' ', p.per_apellido) as paciente,
    p.per_cedula,
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) as especialista,
    esp.esp_nombre as especialidad,
    c.cita_fecha,
    c.cita_hora_inicio,
    c.cita_hora_fin,
    CASE WHEN c.cita_es_primera_vez THEN 'Primera Vez' ELSE 'Seguimiento' END as tipo_cita,
    ec.est_cita_nombre as estado,
    c.cita_motivo
FROM citas c
JOIN pacientes pac ON c.id_paciente = pac.id_paciente
JOIN personas p ON pac.id_persona = p.id_persona
JOIN especialistas e ON c.id_especialista = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona
JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
WHERE c.cita_activo = TRUE
ORDER BY c.cita_fecha, c.cita_hora_inicio;

-- Ver cupos disponibles para Psicología Clínica en la próxima semana
SELECT * FROM obtener_cupos_por_especialidad(
    1,                  -- id_especialidad (Psicología Clínica)
    CURRENT_DATE,       -- desde hoy
    CURRENT_DATE + 7    -- hasta dentro de 7 días
);

-- Ver cupos disponibles para un especialista específico
SELECT * FROM obtener_cupos_por_especialista(
    1,                  -- id_especialista
    CURRENT_DATE,       -- desde hoy
    CURRENT_DATE + 7    -- hasta dentro de 7 días
);

-- Ver agenda del día para un especialista
SELECT 
    c.cita_hora_inicio,
    c.cita_hora_fin,
    CONCAT(p.per_nombre, ' ', p.per_apellido) as paciente,
    p.per_telefono,
    CASE WHEN c.cita_es_primera_vez THEN 'Primera Vez' ELSE 'Seguimiento' END as tipo,
    ec.est_cita_nombre as estado,
    c.cita_motivo
FROM citas c
JOIN pacientes pac ON c.id_paciente = pac.id_paciente
JOIN personas p ON pac.id_persona = p.id_persona
JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
WHERE c.id_especialista = 1
    AND c.cita_fecha = CURRENT_DATE
    AND c.cita_activo = TRUE
ORDER BY c.cita_hora_inicio;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================

-- Agregar nuevo campo cita_tipo
ALTER TABLE citas 
ADD COLUMN cita_tipo VARCHAR(20) 
    CHECK (cita_tipo IN ('EVALUACION', 'PRIMERA_VEZ', 'SEGUIMIENTO', 'TRATAMIENTO'))
    DEFAULT 'PRIMERA_VEZ';

-- Actualizar datos existentes basados en cita_es_primera_vez
UPDATE citas 
SET cita_tipo = CASE 
    WHEN cita_es_primera_vez = TRUE THEN 'PRIMERA_VEZ'
    ELSE 'SEGUIMIENTO'
END;

-- (Opcional) Puedes mantener cita_es_primera_vez para compatibilidad
-- o eliminarlo si ya no lo necesitas:
-- ALTER TABLE citas DROP COLUMN cita_es_primera_vez;





-- ============================================
-- TABLAS REFERENCIALES - CATÁLOGOS BÁSICOS
-- Sistema Médico/Psicológico Genérico
-- ============================================
-- Tabla: SÍNTOMAS
CREATE TABLE sintomas (
    id_sintoma SERIAL PRIMARY KEY,
    des_sintoma VARCHAR(200) NOT NULL,
    est_sintoma CHAR(1) DEFAULT 'A' CHECK (est_sintoma IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: SIGNOS
CREATE TABLE signos (
    id_signo SERIAL PRIMARY KEY,
    des_signo VARCHAR(200) NOT NULL,
    est_signo CHAR(1) DEFAULT 'A' CHECK (est_signo IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: DIAGNÓSTICOS
CREATE TABLE diagnosticos (
    id_diagnostico SERIAL PRIMARY KEY,
    des_diagnostico VARCHAR(500) NOT NULL,
    est_diagnostico CHAR(1) DEFAULT 'A' CHECK (est_diagnostico IN ('A', 'I')),
    diagnostico_codigo_cie10 VARCHAR(10),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: TIPOS DE ANÁLISIS
CREATE TABLE tipos_analisis (
    id_tipo_analisis SERIAL PRIMARY KEY,
    des_tipo_analisis VARCHAR(200) NOT NULL,
    est_tipo_analisis CHAR(1) DEFAULT 'A' CHECK (est_tipo_analisis IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: TIPOS DE ESTUDIOS
CREATE TABLE tipos_estudios (
    id_tipo_estudio SERIAL PRIMARY KEY,
    des_tipo_estudio VARCHAR(200) NOT NULL,
    est_tipo_estudio CHAR(1) DEFAULT 'A' CHECK (est_tipo_estudio IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: MEDICAMENTOS
CREATE TABLE medicamentos (
    id_medicamento SERIAL PRIMARY KEY,
    des_medicamento VARCHAR(200) NOT NULL,
    est_medicamento CHAR(1) DEFAULT 'A' CHECK (est_medicamento IN ('A', 'I')),
    medicamento_concentracion VARCHAR(50),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);

-- Tabla: TIPOS DE PROCEDIMIENTOS MÉDICOS
CREATE TABLE tipos_procedimientos (
    id_tipo_procedimiento SERIAL PRIMARY KEY,
    des_tipo_procedimiento VARCHAR(200) NOT NULL,
    est_tipo_procedimiento CHAR(1) DEFAULT 'A' CHECK (est_tipo_procedimiento IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);



-- Tabla: TIPOS DE TRATAMIENTOS MÉDICOS
CREATE TABLE tipos_tratamientos (
    id_tipo_tratamiento SERIAL PRIMARY KEY,
    des_tipo_tratamiento VARCHAR(200) NOT NULL,
    est_tipo_tratamiento CHAR(1) DEFAULT 'A' CHECK (est_tipo_tratamiento IN ('A', 'I')),
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL
);



select * from diagnosticos;



























-- Insert para la tabla SÍNTOMAS
INSERT INTO sintomas (des_sintoma, est_sintoma, usuario_creacion)
VALUES
    ('ANSIEDAD', 'A', 'ADMIN'),
    ('DEPRESIÓN', 'A', 'ADMIN'),
    ('ESTRÉS', 'A', 'ADMIN'),
    ('FATIGA', 'A', 'ADMIN'),
    ('DIFICULTAD PARA CONCENTRARSE', 'A', 'ADMIN');

-- Insert para la tabla SIGNOS
INSERT INTO signos (des_signo, est_signo, usuario_creacion)
VALUES
    ('AGITACIÓN PSICOMOTRIZ', 'A', 'ADMIN'),
    ('HIPERHIDROSIS', 'A', 'ADMIN'),
    ('TENSIÓN MUSCULAR', 'A', 'ADMIN'),
    ('FALTA DE ENERGÍA', 'A', 'ADMIN'),
    ('CAMBIOS EN EL APETITO', 'A', 'ADMIN');

-- Insert para la tabla DIAGNÓSTICOS
INSERT INTO diagnosticos (des_diagnostico, est_diagnostico, diagnostico_codigo_cie10, usuario_creacion)
VALUES
    ('TRASTORNO DE ANSIEDAD GENERALIZADA', 'A', 'F41.1', 'ADMIN'),
    ('DEPRESIÓN MAYOR', 'A', 'F32', 'ADMIN'),
    ('TRASTORNO OBSESIVO-COMPULSIVO', 'A', 'F42', 'ADMIN'),
    ('EQUILIBRIO EMOCIONAL ALTERADO', 'A', 'F43.2', 'ADMIN'),
    ('INSOMNIO', 'A', 'G47.0', 'ADMIN');

-- Insert para la tabla TIPOS DE ANÁLISIS
INSERT INTO tipos_analisis (des_tipo_analisis, est_tipo_analisis, usuario_creacion)
VALUES
    ('ANÁLISIS PSICOLÓGICO', 'A', 'ADMIN'),
    ('EVALUACIÓN DE TRASTORNOS EMOCIONALES', 'A', 'ADMIN'),
    ('PRUEBA DE PERSONALIDAD', 'A', 'ADMIN'),
    ('TEST DE IQ', 'A', 'ADMIN'),
    ('EVALUACIÓN DE ESTRÉS', 'A', 'ADMIN');

-- Insert para la tabla TIPOS DE ESTUDIOS
INSERT INTO tipos_estudios (des_tipo_estudio, est_tipo_estudio, usuario_creacion)
VALUES
    ('ESTUDIO COGNITIVO', 'A', 'ADMIN'),
    ('ESTUDIO EMOCIONAL', 'A', 'ADMIN'),
    ('ESTUDIO DE PERSONALIDAD', 'A', 'ADMIN'),
    ('ESTUDIO DE ANSIEDAD', 'A', 'ADMIN'),
    ('ESTUDIO DE DEPRESIÓN', 'A', 'ADMIN');

-- Insert para la tabla MEDICAMENTOS
INSERT INTO medicamentos (des_medicamento, est_medicamento, medicamento_concentracion, usuario_creacion)
VALUES
    ('ALPRAZOLAM', 'A', '0.25MG', 'ADMIN'),
    ('FLUOXETINA', 'A', '20MG', 'ADMIN'),
    ('SERTRALINA', 'A', '50MG', 'ADMIN'),
    ('BUPROPIONA', 'A', '150MG', 'ADMIN'),
    ('CITALOPRAM', 'A', '10MG', 'ADMIN');

-- Insert para la tabla TIPOS DE PROCEDIMIENTOS MÉDICOS
INSERT INTO tipos_procedimientos (des_tipo_procedimiento, est_tipo_procedimiento, usuario_creacion)
VALUES
    ('TERAPIA COGNITIVO-CONDUCTUAL', 'A', 'ADMIN'),
    ('PSICOTERAPIA', 'A', 'ADMIN'),
    ('TERAPIA DE RELACIONES', 'A', 'ADMIN'),
    ('TÉCNICAS DE RELAJACIÓN', 'A', 'ADMIN'),
    ('ENTRENAMIENTO EN HABILIDADES SOCIALES', 'A', 'ADMIN');




PLAN DE DESARROLLO EN 3 FASES

📌 FASE 1: CONSULTA MÉDICA BÁSICA
Atención inicial del paciente
Referenciales necesarios:
✅ Diagnósticos (ABM)
✅ Tipos de Procedimientos (ABM)
Formularios de Registro:
✅ Registrar Consulta (vinculada a cita)
✅ Registrar Diagnóstico (desde consulta)
✅ Registrar Procedimiento Médico (desde consulta)
✅ Registrar Tratamiento (desde consulta/diagnóstico)
Flujo: Cita → Consulta → Diagnóstico → Procedimiento/Tratamiento

📌 FASE 2: SÍNTOMAS, SIGNOS Y FICHA MÉDICA
Evaluación detallada del paciente
Referenciales necesarios:
✅ Síntomas (ABM)
✅ Signos (ABM)
Formularios de Registro:
✅ Registrar Ficha Médica (historial del paciente)
✅ Registrar Síntomas (desde consulta)
✅ Registrar Signos (desde consulta)
Flujo: Consulta → Síntomas/Signos → Ficha Médica

📌 FASE 3: RECETAS, ÓRDENES Y JUSTIFICATIVOS
Prescripciones y documentación
Referenciales necesarios:
✅ Medicamentos (ABM)
✅ Tipos de Análisis (ABM)
✅ Tipos de Estudios (ABM)
Formularios de Registro (Maestro-Detalle):
✅ Registrar Receta + detalle medicamentos (grilla)
✅ Registrar Orden de Análisis + detalle análisis (grilla)
✅ Registrar Orden de Estudio + detalle estudios (grilla)
✅ Registrar Justificativo Médico
Flujo: Consulta → Receta/Órdenes/Justificativo

📋 VENTANA 1: REGISTRAR CONSULTA (registrarconsulta-index.html)
Objetivo: Atención inicial del paciente desde una cita
Debe incluir:
Selector de Paciente (puede venir pre-cargado desde la cita)
Selector de Profesional (puede venir pre-cargado)
Campo Fecha y Hora de la consulta
Motivo de Consulta (textarea)
Descripción de la Consulta (textarea detallada)
Estado: PENDIENTE / EN_ATENCION / FINALIZADA
Observaciones (opcional)
Relación con Cita (si viene desde una cita)
Botón Guardar Consulta
Tabla con lista de consultas registradas

🩺 VENTANA 2: REGISTRAR DIAGNÓSTICO (registrardiagnostico-index.html)
Objetivo: Registrar diagnósticos asociados a una consulta
Debe incluir:
Selector de Consulta (buscar por paciente/fecha)
Selector de Diagnóstico (CIE-10) - desde tu tabla diagnosticos
Tipo de Diagnóstico: Principal / Secundario / Diferencial
Descripción Adicional (textarea)
Estado del Diagnóstico: Confirmado / Presuntivo / Descartado
Observaciones
Botón Guardar Diagnóstico
Tabla con diagnósticos registrados por consulta

💊 VENTANA 3: REGISTRAR TRATAMIENTO (registrartratamiento-index.html)
Objetivo: Prescribir tratamientos para diagnósticos
Debe incluir:
Selector de Paciente
Selector de Diagnóstico (del paciente seleccionado)
Tipo de Tratamiento: Farmacológico / Fisioterapia / Quirúrgico / Otro
Nombre del Tratamiento (medicamento, terapia, etc.)
Descripción del Tratamiento (indicaciones detalladas)
Dosis/Frecuencia
Fecha Inicio y Fecha Fin (estimada)
Duración estimada (días)
Estado: ACTIVO / SUSPENDIDO / FINALIZADO
Observaciones
Botones: Guardar, Suspender Tratamiento, Finalizar Tratamiento
Tabla con tratamientos activos del paciente

🏥 VENTANA 4: REGISTRAR PROCEDIMIENTO (registrarprocedimiento-index.html)
Objetivo: Registrar procedimientos médicos realizados
Debe incluir:
Selector de Consulta (buscar por paciente/fecha)
Selector de Tipo de Procedimiento - desde tu tabla tipo_procedimientos
Fecha y Hora del Procedimiento
Descripción del Procedimiento (qué se hizo exactamente)
Profesional que lo realizó
Resultado del Procedimiento
Observaciones/Complicaciones
Estado: PROGRAMADO / EN_PROCESO / COMPLETADO / CANCELADO
Botón Guardar Procedimiento
Tabla con procedimientos registrados




-- ============================================
-- FASE 1: CONSULTA MÉDICA BÁSICA
-- Sistema Médico/Psicológico PostgreSQL
-- ============================================
-- Nota: Las tablas referenciales (diagnosticos, tipos_procedimientos) 
-- ya están creadas en tu base de datos
-- ============================================

-- =============================================
-- TABLAS DE REGISTRO - FASE 1
-- =============================================

-- Tabla: CONSULTAS (vinculada a citas)
CREATE TABLE consultas (
    id_consulta SERIAL PRIMARY KEY,
    id_cita INT, -- Vinculación opcional con citas
    id_paciente INT NOT NULL,
    id_profesional INT NOT NULL, -- id_especialista de la tabla especialistas
    des_consulta TEXT,
    est_consulta CHAR(1) DEFAULT 'A' CHECK (est_consulta IN ('A', 'I')),
    consulta_fecha TIMESTAMP NOT NULL,
    consulta_motivo VARCHAR(500),
    consulta_estado VARCHAR(20) DEFAULT 'PENDIENTE', -- PENDIENTE, EN_ATENCION, FINALIZADA
    consulta_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_profesional) REFERENCES especialistas(id_especialista)
);

-- Tabla: REGISTRO DE DIAGNÓSTICOS
CREATE TABLE registro_diagnosticos (
    id_registro_diagnostico SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_diagnostico INT NOT NULL,
    des_registro_diagnostico TEXT,
    est_registro_diagnostico CHAR(1) DEFAULT 'A' CHECK (est_registro_diagnostico IN ('A', 'I')),
    registro_tipo VARCHAR(20) DEFAULT 'PRESUNTIVO', -- PRESUNTIVO, DEFINITIVO, DIFERENCIAL
    registro_gravedad VARCHAR(20), -- LEVE, MODERADO, GRAVE
    registro_fecha DATE NOT NULL,
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    FOREIGN KEY (id_diagnostico) REFERENCES diagnosticos(id_diagnostico)
);

-- Tabla: REGISTRO DE PROCEDIMIENTOS
CREATE TABLE registro_procedimientos (
    id_registro_procedimiento SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_paciente INT NOT NULL,
    id_tipo_procedimiento INT NOT NULL,
    des_registro_procedimiento TEXT NOT NULL,
    est_registro_procedimiento CHAR(1) DEFAULT 'A' CHECK (est_registro_procedimiento IN ('A', 'I')),
    registro_fecha TIMESTAMP NOT NULL,
    registro_duracion INT, -- Duración en minutos
    registro_resultado TEXT,
    registro_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_tipo_procedimiento) REFERENCES tipos_procedimientos(id_tipo_procedimiento)
);

-- Tabla: TRATAMIENTOS
CREATE TABLE tratamientos (
    id_tratamiento SERIAL PRIMARY KEY,
    id_paciente INT NOT NULL,
    id_diagnostico INT,
    des_tratamiento TEXT NOT NULL,
    est_tratamiento CHAR(1) DEFAULT 'A' CHECK (est_tratamiento IN ('A', 'I')),
    tratamiento_tipo VARCHAR(100), -- FARMACOLÓGICO, PSICOTERAPÉUTICO, MIXTO
    tratamiento_fecha_inicio DATE NOT NULL,
    tratamiento_fecha_fin DATE,
    tratamiento_estado VARCHAR(20) DEFAULT 'ACTIVO', -- ACTIVO, FINALIZADO, SUSPENDIDO
    tratamiento_objetivos TEXT,
    tratamiento_observaciones TEXT,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_diagnostico) REFERENCES diagnosticos(id_diagnostico)
);

-- =============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =============================================

CREATE INDEX idx_consultas_cita ON consultas(id_cita);
CREATE INDEX idx_consultas_paciente ON consultas(id_paciente);
CREATE INDEX idx_consultas_profesional ON consultas(id_profesional);
CREATE INDEX idx_consultas_fecha ON consultas(consulta_fecha);
CREATE INDEX idx_consultas_estado ON consultas(consulta_estado);

CREATE INDEX idx_registro_diagnosticos_consulta ON registro_diagnosticos(id_consulta);
CREATE INDEX idx_registro_diagnosticos_diagnostico ON registro_diagnosticos(id_diagnostico);
CREATE INDEX idx_registro_diagnosticos_fecha ON registro_diagnosticos(registro_fecha);

CREATE INDEX idx_registro_procedimientos_consulta ON registro_procedimientos(id_consulta);
CREATE INDEX idx_registro_procedimientos_paciente ON registro_procedimientos(id_paciente);
CREATE INDEX idx_registro_procedimientos_tipo ON registro_procedimientos(id_tipo_procedimiento);
CREATE INDEX idx_registro_procedimientos_fecha ON registro_procedimientos(registro_fecha);

CREATE INDEX idx_tratamientos_paciente ON tratamientos(id_paciente);
CREATE INDEX idx_tratamientos_diagnostico ON tratamientos(id_diagnostico);
CREATE INDEX idx_tratamientos_estado ON tratamientos(tratamiento_estado);
CREATE INDEX idx_tratamientos_fecha_inicio ON tratamientos(tratamiento_fecha_inicio);

-- =============================================
-- COMENTARIOS EN TABLAS
-- =============================================

COMMENT ON TABLE consultas IS 'Registro de consultas médicas/psicológicas vinculadas a citas';
COMMENT ON TABLE registro_diagnosticos IS 'Diagnósticos registrados en cada consulta';
COMMENT ON TABLE registro_procedimientos IS 'Procedimientos médicos realizados en consulta';
COMMENT ON TABLE tratamientos IS 'Tratamientos asignados a pacientes';

COMMENT ON COLUMN consultas.id_cita IS 'FK opcional - vincula con cita agendada';
COMMENT ON COLUMN consultas.id_profesional IS 'FK a especialistas.id_especialista';
COMMENT ON COLUMN consultas.consulta_estado IS 'PENDIENTE, EN_ATENCION, FINALIZADA';
COMMENT ON COLUMN registro_diagnosticos.registro_tipo IS 'PRESUNTIVO, DEFINITIVO, DIFERENCIAL';
COMMENT ON COLUMN registro_diagnosticos.registro_gravedad IS 'LEVE, MODERADO, GRAVE';
COMMENT ON COLUMN tratamientos.tratamiento_estado IS 'ACTIVO, FINALIZADO, SUSPENDIDO';

-- =============================================
-- DATOS DE EJEMPLO - REFERENCIALES
-- =============================================

-- Diagnósticos comunes en psicología (usando CIE-10)
INSERT INTO diagnosticos (des_diagnostico, est_diagnostico, diagnostico_codigo_cie10, usuario_creacion) VALUES
('Trastorno de ansiedad generalizada', 'A', 'F41.1', 'ADMIN'),
('Episodio depresivo moderado', 'A', 'F32.1', 'ADMIN'),
('Trastorno de pánico', 'A', 'F41.0', 'ADMIN'),
('Trastorno obsesivo-compulsivo', 'A', 'F42', 'ADMIN'),
('Trastorno de adaptación con ansiedad y depresión mixtas', 'A', 'F43.2', 'ADMIN'),
('Trastorno de estrés postraumático', 'A', 'F43.1', 'ADMIN'),
('Episodio depresivo grave sin síntomas psicóticos', 'A', 'F32.2', 'ADMIN'),
('Trastorno de ansiedad social (fobia social)', 'A', 'F40.1', 'ADMIN'),
('Trastorno de déficit de atención con hiperactividad', 'A', 'F90.0', 'ADMIN'),
('Trastorno de conducta desafiante y oposicionista', 'A', 'F91.3', 'ADMIN');

-- Procedimientos psicológicos comunes
INSERT INTO tipos_procedimientos (des_tipo_procedimiento, est_tipo_procedimiento, usuario_creacion) VALUES
('Terapia Cognitivo-Conductual (TCC)', 'A', 'ADMIN'),
('Psicoterapia Individual', 'A', 'ADMIN'),
('Terapia de Exposición', 'A', 'ADMIN'),
('Terapia de Aceptación y Compromiso (ACT)', 'A', 'ADMIN'),
('Terapia Sistémica Familiar', 'A', 'ADMIN'),
('EMDR (Desensibilización y Reprocesamiento por Movimientos Oculares)', 'A', 'ADMIN'),
('Terapia Gestalt', 'A', 'ADMIN'),
('Terapia de Pareja', 'A', 'ADMIN'),
('Psicoeducación', 'A', 'ADMIN'),
('Técnicas de Relajación y Mindfulness', 'A', 'ADMIN');

-- =============================================
-- DATOS DE EJEMPLO - REGISTROS
-- (Asumiendo que ya existen pacientes y especialistas)
-- =============================================

-- Ejemplo de consultas (reemplaza los IDs según tu BD)
-- INSERT INTO consultas (id_cita, id_paciente, id_profesional, des_consulta, consulta_fecha, consulta_motivo, consulta_estado, usuario_creacion) VALUES
-- (1, 1, 1, 'Primera consulta por ansiedad', '2025-01-15 09:00:00', 'Ansiedad generalizada, insomnio', 'FINALIZADA', 'psicologo1'),
-- (2, 2, 1, 'Consulta de seguimiento', '2025-01-16 10:00:00', 'Episodio depresivo', 'FINALIZADA', 'psicologo1');

-- =============================================
-- FIN DEL SCRIPT FASE 1
-- =============================================






-- /database/recordatorios.sql

CREATE TABLE recordatorios (
    id_recordatorio SERIAL PRIMARY KEY,
    id_cita INTEGER NOT NULL REFERENCES citas(id_cita) ON DELETE CASCADE,
    
    -- Tipo de recordatorio
    recordatorio_tipo VARCHAR(10) NOT NULL CHECK (recordatorio_tipo IN ('12h', '24h')),
    
    -- Programación y envío
    recordatorio_fecha_programada TIMESTAMP NOT NULL,
    recordatorio_fecha_enviado TIMESTAMP,
    
    -- Estado y control
    recordatorio_estado VARCHAR(20) NOT NULL DEFAULT 'pendiente'
        CHECK (recordatorio_estado IN ('pendiente', 'enviado', 'fallido', 'cancelado')),
    recordatorio_intentos INTEGER DEFAULT 0,
    
    -- Mensaje y log
    recordatorio_mensaje_enviado TEXT,
    recordatorio_error TEXT,
    recordatorio_twilio_sid VARCHAR(100), -- ID de mensaje de Twilio
    
    -- Datos del destinatario (cache para no hacer JOIN cada vez)
    recordatorio_telefono VARCHAR(20),
    recordatorio_paciente_nombre VARCHAR(200),
    
    -- Auditoría
    recordatorio_creacion_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    recordatorio_creacion_usuario INTEGER,
    recordatorio_activo BOOLEAN DEFAULT TRUE,
    
    -- Solo puede haber 1 recordatorio de cada tipo por cita
    CONSTRAINT unique_cita_tipo UNIQUE (id_cita, recordatorio_tipo)
);

-- Índice CRÍTICO para el scheduler (busca pendientes rápido)
CREATE INDEX idx_recordatorios_pendientes 
ON recordatorios(recordatorio_estado, recordatorio_fecha_programada) 
WHERE recordatorio_estado = 'pendiente' AND recordatorio_activo = TRUE;

CREATE INDEX idx_recordatorios_cita ON recordatorios(id_cita);

-- Vista para consultas con todos los datos
CREATE OR REPLACE VIEW v_recordatorios_completos AS
SELECT 
    r.id_recordatorio,
    r.id_cita,
    r.recordatorio_tipo,
    r.recordatorio_fecha_programada,
    r.recordatorio_fecha_enviado,
    r.recordatorio_estado,
    r.recordatorio_intentos,
    r.recordatorio_telefono,
    r.recordatorio_mensaje_enviado,
    
    -- Datos de la cita
    c.cita_fecha,
    c.cita_hora_inicio,
    c.cita_hora_fin,
    c.cita_motivo,
    
    -- Datos del paciente
    p.id_paciente,
    CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre,
    pp.per_telefono AS paciente_telefono,
    
    -- Datos del especialista
    CONCAT(pe.per_nombre, ' ', pe.per_apellido) AS especialista_nombre,
    esp.des_especialidad,
    
    -- Estado de la cita
    ec.est_cita_nombre AS cita_estado
    
FROM recordatorios r
JOIN citas c ON r.id_cita = c.id_cita
JOIN pacientes p ON c.id_paciente = p.id_paciente
JOIN personas pp ON p.id_persona = pp.id_persona
JOIN especialistas e ON c.id_especialista = e.id_especialista
JOIN funcionarios f ON e.id_funcionario = f.id_funcionario
JOIN personas pe ON f.id_persona = pe.id_persona
JOIN especialidades esp ON c.id_especialidad = esp.id_especialidad
JOIN estados_citas ec ON c.id_estado_cita = ec.id_estado_cita
WHERE r.recordatorio_activo = TRUE;





-- ============================================
-- FASE 2: REGISTRO DE SÍNTOMAS Y SIGNOS
-- Sistema Médico/Psicológico PostgreSQL
-- ============================================

-- =============================================
-- TABLA: REGISTRO DE SÍNTOMAS
-- =============================================

CREATE TABLE registro_sintomas (
    id_registro_sintoma SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_sintoma INT NOT NULL,
    des_registro_sintoma TEXT,
    est_registro_sintoma CHAR(1) DEFAULT 'A' CHECK (est_registro_sintoma IN ('A', 'I')),
    
    -- Detalles del síntoma
    sintoma_intensidad VARCHAR(20), -- LEVE, MODERADA, SEVERA
    sintoma_frecuencia VARCHAR(50), -- OCASIONAL, FRECUENTE, CONSTANTE
    sintoma_duracion VARCHAR(100), -- "2 días", "1 semana", "3 meses"
    sintoma_fecha_inicio DATE,
    sintoma_factores_desencadenantes TEXT,
    sintoma_factores_atenuantes TEXT,
    sintoma_observaciones TEXT,
    
    registro_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    CONSTRAINT registro_sintomas_id_consulta_fkey 
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    CONSTRAINT registro_sintomas_id_sintoma_fkey 
        FOREIGN KEY (id_sintoma) REFERENCES sintomas(id_sintoma)
);

-- =============================================
-- TABLA: REGISTRO DE SIGNOS
-- =============================================

CREATE TABLE registro_signos (
    id_registro_signo SERIAL PRIMARY KEY,
    id_consulta INT NOT NULL,
    id_signo INT NOT NULL,
    des_registro_signo TEXT,
    est_registro_signo CHAR(1) DEFAULT 'A' CHECK (est_registro_signo IN ('A', 'I')),
    
    -- Mediciones del signo
    signo_valor_medido VARCHAR(100), -- Ej: "120/80", "36.5°C", "75 lpm"
    signo_unidad_medida VARCHAR(20), -- mmHg, °C, lpm, etc.
    signo_rango_normal VARCHAR(100), -- Ej: "110/70 - 130/85"
    signo_estado_resultado VARCHAR(20), -- NORMAL, ALTERADO, CRÍTICO
    signo_metodo_medicion VARCHAR(100), -- Ej: "Tensiómetro digital", "Observación directa"
    signo_observaciones TEXT,
    
    registro_fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_creacion VARCHAR(50),
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    usuario_modificacion VARCHAR(50),
    fecha_modificacion TIMESTAMP NULL,
    
    CONSTRAINT registro_signos_id_consulta_fkey 
        FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta) ON DELETE CASCADE,
    CONSTRAINT registro_signos_id_signo_fkey 
        FOREIGN KEY (id_signo) REFERENCES signos(id_signo)
);

-- =============================================
-- ÍNDICES PARA OPTIMIZACIÓN
-- =============================================

-- Índices para REGISTRO_SINTOMAS
CREATE INDEX idx_registro_sintomas_consulta ON registro_sintomas(id_consulta);
CREATE INDEX idx_registro_sintomas_sintoma ON registro_sintomas(id_sintoma);
CREATE INDEX idx_registro_sintomas_intensidad ON registro_sintomas(sintoma_intensidad);
CREATE INDEX idx_registro_sintomas_fecha ON registro_sintomas(registro_fecha);

-- Índices para REGISTRO_SIGNOS
CREATE INDEX idx_registro_signos_consulta ON registro_signos(id_consulta);
CREATE INDEX idx_registro_signos_signo ON registro_signos(id_signo);
CREATE INDEX idx_registro_signos_estado ON registro_signos(signo_estado_resultado);
CREATE INDEX idx_registro_signos_fecha ON registro_signos(registro_fecha);

-- =============================================
-- COMENTARIOS EN TABLAS
-- =============================================

COMMENT ON TABLE registro_sintomas IS 'Síntomas registrados en cada consulta';
COMMENT ON TABLE registro_signos IS 'Signos vitales y observaciones registradas en cada consulta';

COMMENT ON COLUMN registro_sintomas.sintoma_intensidad IS 'LEVE, MODERADA, SEVERA';
COMMENT ON COLUMN registro_sintomas.sintoma_frecuencia IS 'OCASIONAL, FRECUENTE, CONSTANTE';
COMMENT ON COLUMN registro_signos.signo_estado_resultado IS 'NORMAL, ALTERADO, CRÍTICO';

-- =============================================
-- TRIGGERS PARA HISTORIA CLÍNICA
-- =============================================

-- Función: Agregar síntoma a historia clínica
CREATE OR REPLACE FUNCTION agregar_sintoma_a_hc()
RETURNS TRIGGER AS $$
DECLARE
    v_historia_clinica VARCHAR(50);
    v_descripcion TEXT;
    v_desc_sintoma TEXT;
    v_id_paciente INT;
BEGIN
    -- Obtener paciente e historia clínica desde la consulta
    SELECT c.id_paciente, p.pac_historia_clinica 
    INTO v_id_paciente, v_historia_clinica
    FROM consultas c
    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
    WHERE c.id_consulta = NEW.id_consulta;
    
    -- Obtener descripción del síntoma
    SELECT des_sintoma INTO v_desc_sintoma
    FROM sintomas WHERE id_sintoma = NEW.id_sintoma;
    
    -- Crear descripción completa
    v_descripcion := 'SÍNTOMA: ' || v_desc_sintoma;
    
    IF NEW.sintoma_intensidad IS NOT NULL THEN
        v_descripcion := v_descripcion || ' - Intensidad: ' || NEW.sintoma_intensidad;
    END IF;
    
    IF NEW.sintoma_frecuencia IS NOT NULL THEN
        v_descripcion := v_descripcion || ' - Frecuencia: ' || NEW.sintoma_frecuencia;
    END IF;
    
    IF NEW.des_registro_sintoma IS NOT NULL THEN
        v_descripcion := v_descripcion || E'\n' || NEW.des_registro_sintoma;
    END IF;
    
    -- Insertar en detalle_historia_clinica
    INSERT INTO detalle_historia_clinica (
        id_paciente,
        pac_historia_clinica,
        tipo_registro,
        id_consulta,
        fecha_evento,
        descripcion_evento,
        observaciones,
        usuario_creacion
    ) VALUES (
        v_id_paciente,
        v_historia_clinica,
        'SINTOMA',
        NEW.id_consulta,
        NEW.registro_fecha,
        v_descripcion,
        NEW.sintoma_observaciones,
        NEW.usuario_creacion
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Función: Agregar signo a historia clínica
CREATE OR REPLACE FUNCTION agregar_signo_a_hc()
RETURNS TRIGGER AS $$
DECLARE
    v_historia_clinica VARCHAR(50);
    v_descripcion TEXT;
    v_desc_signo TEXT;
    v_id_paciente INT;
BEGIN
    -- Obtener paciente e historia clínica desde la consulta
    SELECT c.id_paciente, p.pac_historia_clinica 
    INTO v_id_paciente, v_historia_clinica
    FROM consultas c
    INNER JOIN pacientes p ON c.id_paciente = p.id_paciente
    WHERE c.id_consulta = NEW.id_consulta;
    
    -- Obtener descripción del signo
    SELECT des_signo INTO v_desc_signo
    FROM signos WHERE id_signo = NEW.id_signo;
    
    -- Crear descripción completa
    v_descripcion := 'SIGNO: ' || v_desc_signo;
    
    IF NEW.signo_valor_medido IS NOT NULL THEN
        v_descripcion := v_descripcion || ' - Valor: ' || NEW.signo_valor_medido;
        IF NEW.signo_unidad_medida IS NOT NULL THEN
            v_descripcion := v_descripcion || ' ' || NEW.signo_unidad_medida;
        END IF;
    END IF;
    
    IF NEW.signo_estado_resultado IS NOT NULL THEN
        v_descripcion := v_descripcion || ' - Estado: ' || NEW.signo_estado_resultado;
    END IF;
    
    IF NEW.des_registro_signo IS NOT NULL THEN
        v_descripcion := v_descripcion || E'\n' || NEW.des_registro_signo;
    END IF;
    
    -- Insertar en detalle_historia_clinica
    INSERT INTO detalle_historia_clinica (
        id_paciente,
        pac_historia_clinica,
        tipo_registro,
        id_consulta,
        fecha_evento,
        descripcion_evento,
        observaciones,
        usuario_creacion
    ) VALUES (
        v_id_paciente,
        v_historia_clinica,
        'SIGNO',
        NEW.id_consulta,
        NEW.registro_fecha,
        v_descripcion,
        NEW.signo_observaciones,
        NEW.usuario_creacion
    );
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Crear triggers
CREATE TRIGGER trigger_sintoma_a_hc
    AFTER INSERT ON registro_sintomas
    FOR EACH ROW
    EXECUTE FUNCTION agregar_sintoma_a_hc();

CREATE TRIGGER trigger_signo_a_hc
    AFTER INSERT ON registro_signos
    FOR EACH ROW
    EXECUTE FUNCTION agregar_signo_a_hc();

-- =============================================
-- DATOS DE EJEMPLO - SÍNTOMAS
-- =============================================

INSERT INTO sintomas (des_sintoma, est_sintoma, usuario_creacion) VALUES
-- Síntomas Emocionales
('Tristeza persistente', 'A', 'ADMIN'),
('Ansiedad generalizada', 'A', 'ADMIN'),
('Irritabilidad', 'A', 'ADMIN'),
('Sensación de vacío', 'A', 'ADMIN'),
('Miedo intenso', 'A', 'ADMIN'),
('Sentimientos de culpa', 'A', 'ADMIN'),
('Desesperanza', 'A', 'ADMIN'),

-- Síntomas Cognitivos
('Dificultad para concentrarse', 'A', 'ADMIN'),
('Pensamientos intrusivos', 'A', 'ADMIN'),
('Pérdida de memoria', 'A', 'ADMIN'),
('Indecisión', 'A', 'ADMIN'),
('Pensamientos negativos recurrentes', 'A', 'ADMIN'),
('Despersonalización', 'A', 'ADMIN'),
('Desrealización', 'A', 'ADMIN'),
('Confusión mental', 'A', 'ADMIN'),

-- Síntomas Físicos
('Insomnio', 'A', 'ADMIN'),
('Hipersomnia', 'A', 'ADMIN'),
('Fatiga crónica', 'A', 'ADMIN'),
('Dolor de cabeza frecuente', 'A', 'ADMIN'),
('Palpitaciones', 'A', 'ADMIN'),
('Tensión muscular', 'A', 'ADMIN'),
('Problemas gastrointestinales', 'A', 'ADMIN'),
('Pérdida de apetito', 'A', 'ADMIN'),
('Aumento de apetito', 'A', 'ADMIN'),
('Sudoración excesiva', 'A', 'ADMIN'),
('Temblores', 'A', 'ADMIN'),
('Mareos', 'A', 'ADMIN'),

-- Síntomas Conductuales
('Aislamiento social', 'A', 'ADMIN'),
('Procrastinación excesiva', 'A', 'ADMIN'),
('Evitación de situaciones', 'A', 'ADMIN'),
('Conductas compulsivas', 'A', 'ADMIN'),
('Agitación psicomotora', 'A', 'ADMIN'),
('Lentitud psicomotora', 'A', 'ADMIN'),
('Descuido personal', 'A', 'ADMIN'),
('Llanto frecuente', 'A', 'ADMIN');

-- =============================================
-- DATOS DE EJEMPLO - SIGNOS
-- =============================================

INSERT INTO signos (des_signo, est_signo, usuario_creacion) VALUES
-- Signos Vitales
('Presión arterial', 'A', 'ADMIN'),
('Frecuencia cardíaca', 'A', 'ADMIN'),
('Temperatura corporal', 'A', 'ADMIN'),
('Frecuencia respiratoria', 'A', 'ADMIN'),
('Saturación de oxígeno', 'A', 'ADMIN'),

-- Signos de Observación Psicológica
('Estado de ánimo observado', 'A', 'ADMIN'),
('Nivel de ansiedad observado', 'A', 'ADMIN'),
('Contacto visual', 'A', 'ADMIN'),
('Higiene y presentación personal', 'A', 'ADMIN'),
('Postura corporal', 'A', 'ADMIN'),
('Expresión facial', 'A', 'ADMIN'),
('Tono de voz', 'A', 'ADMIN'),
('Fluidez del lenguaje', 'A', 'ADMIN'),
('Coherencia del discurso', 'A', 'ADMIN'),

-- Signos Cognitivos Observables
('Orientación en tiempo', 'A', 'ADMIN'),
('Orientación en espacio', 'A', 'ADMIN'),
('Orientación en persona', 'A', 'ADMIN'),
('Atención y concentración', 'A', 'ADMIN'),
('Memoria inmediata', 'A', 'ADMIN'),
('Memoria reciente', 'A', 'ADMIN'),
('Memoria remota', 'A', 'ADMIN'),
('Juicio crítico', 'A', 'ADMIN'),
('Insight (conciencia de enfermedad)', 'A', 'ADMIN'),

-- Signos Conductuales Observables
('Agitación psicomotriz', 'A', 'ADMIN'),
('Retardo psicomotor', 'A', 'ADMIN'),
('Tics o movimientos involuntarios', 'A', 'ADMIN'),
('Conductas repetitivas', 'A', 'ADMIN'),
('Nivel de colaboración', 'A', 'ADMIN');

-- =============================================
-- FIN DEL SCRIPT FASE 2 - REGISTROS
-- =============================================















-- ============================================
-- CONSULTA COMPLETA CON UNION ALL
-- ============================================

SELECT 'grupos' AS tabla, id_grupo::VARCHAR AS col1, des_grupo AS col2, est_grupo::VARCHAR AS col3, NULL AS col4, NULL AS col5
FROM grupos

UNION ALL

SELECT 'modulos' AS tabla, id_modulo::VARCHAR, des_modulo, est_modulo::VARCHAR, NULL, NULL
FROM modulos

UNION ALL

SELECT 'cargos' AS tabla, id_cargo::VARCHAR, des_cargo, est_cargo::VARCHAR, NULL, NULL
FROM cargos

UNION ALL

SELECT 'funcionarios' AS tabla, id_funcionario::VARCHAR, id_persona::VARCHAR, id_cargo::VARCHAR, fun_estado::VARCHAR, creacion_fecha::VARCHAR
FROM funcionarios

UNION ALL

SELECT 'usuarios' AS tabla, id_usuario::VARCHAR, usu_nick, id_funcionario::VARCHAR, id_grupo::VARCHAR, usu_estado::VARCHAR
FROM usuarios

UNION ALL

SELECT 'paginas' AS tabla, id_pagina::VARCHAR, des_pagina, id_modulo::VARCHAR, est_pagina::VARCHAR, NULL
FROM paginas

UNION ALL

SELECT 'permisos' AS tabla, id_pagina::VARCHAR, id_grupo::VARCHAR, leer::VARCHAR, insertar::VARCHAR, editar::VARCHAR
FROM permisos

ORDER BY tabla;




-- =====================================================
-- SCRIPT SQL COMPLETO: PÁGINAS + PERMISOS
-- Sistema de Gestión Médica
-- Grupos: ADMINISTRADOR | RECEPCIONISTA | ESPECIALISTA
-- =====================================================

-- =====================================================
-- PASO 1: LIMPIAR DATOS ANTERIORES
-- =====================================================
TRUNCATE TABLE permisos CASCADE;
DELETE FROM paginas;

-- =====================================================
-- PASO 2: INSERTAR PÁGINAS CON RUTAS REALES
-- =====================================================

-- MÓDULO 1: Gestión de Usuario
INSERT INTO paginas (des_pagina, pag_direcc, est_pagina, id_modulo) VALUES
('Lista de Usuarios', '/modulos/usuario/usuario-index', TRUE, 1),
('Crear Usuario', '/api/v1/usuarios', TRUE, 1),
('Editar Usuario', '/api/v1/usuarios', TRUE, 1),
('Eliminar Usuario', '/api/v1/usuarios', TRUE, 1),

('Lista de Funcionarios', '/modulos/funcionario/funcionario-index', TRUE, 1),
('Crear Funcionario', '/api/v1/funcionarios', TRUE, 1),
('Editar Funcionario', '/api/v1/funcionarios', TRUE, 1),
('Eliminar Funcionario', '/api/v1/funcionarios', TRUE, 1);

-- MÓDULO 2: Agendamiento
INSERT INTO paginas (des_pagina, pag_direcc, est_pagina, id_modulo) VALUES
('Ver Agenda Médica', '/agenda/agenda-index', TRUE, 2),
('Gestionar Agenda', '/api/v1/agendas', TRUE, 2),

('Ver Citas', '/cita/cita-index', TRUE, 2),
('Crear Cita', '/api/v1/citas', TRUE, 2),
('Editar Cita', '/api/v1/citas', TRUE, 2),
('Cancelar Cita', '/api/v1/citas', TRUE, 2),

('Ver Recordatorios', '/recordatorio/recordatorio-index', TRUE, 2),
('Gestionar Recordatorios', '/api/v1/recordatorios', TRUE, 2);

-- MÓDULO 3: Consultorios
INSERT INTO paginas (des_pagina, pag_direcc, est_pagina, id_modulo) VALUES
('Lista de Pacientes', '/modulos/paciente/paciente-index', TRUE, 3),
('Registrar Paciente', '/api/v1/pacientes', TRUE, 3),
('Editar Paciente', '/api/v1/pacientes', TRUE, 3),

('Ver Ficha Médica', '/ficha-medica/ficha-index', TRUE, 3),

('Lista de Consultas', '/consulta/consulta-index', TRUE, 3),
('Registrar Consulta', '/api/v1/consultas', TRUE, 3),

('Lista de Diagnósticos', '/diagnostico/diagnostico-index', TRUE, 3),
('Registrar Diagnóstico', '/api/v1/diagnosticos', TRUE, 3),

('Lista de Tratamientos', '/tratamiento/tratamiento-index', TRUE, 3),
('Registrar Tratamiento', '/api/v1/tratamientos', TRUE, 3),

('Lista de Procedimientos', '/procedimiento/procedimiento-index', TRUE, 3),
('Registrar Procedimiento', '/api/v1/procedimientos', TRUE, 3),

('Lista de Anamnesis', '/anamnesis/anamnesis-index', TRUE, 3),
('Registrar Anamnesis', '/api/v1/anamnesis', TRUE, 3);

-- MÓDULO 4: Reportes
INSERT INTO paginas (des_pagina, pag_direcc, est_pagina, id_modulo) VALUES
('Ver Reportes', '/reportes/reportes-index', TRUE, 4),
('Reporte de Citas', '/reportes/citas', TRUE, 4),
('Reporte de Pacientes', '/reportes/pacientes', TRUE, 4),
('Reporte de Consultas', '/reportes/consultas', TRUE, 4);

-- MÓDULO 6: Configuración (Referenciales)
INSERT INTO paginas (des_pagina, pag_direcc, est_pagina, id_modulo) VALUES
('Gestionar Ciudades', '/referenciales/ciudad/ciudad-index', TRUE, 6),
('Gestionar Especialidades', '/referenciales/especialidad/especialidad-index', TRUE, 6),
('Gestionar Géneros', '/referenciales/genero/genero-index', TRUE, 6),
('Gestionar Estados Civiles', '/referenciales/estado-civil/estado-civil-index', TRUE, 6),
('Gestionar Niveles Instrucción', '/referenciales/nivel-instruccion/nivel-instruccion-index', TRUE, 6),
('Gestionar Profesiones', '/referenciales/profesion/profesion-index', TRUE, 6),
('Gestionar Días', '/referenciales/dia/dia-index', TRUE, 6),
('Gestionar Consultorios', '/referenciales/consultorio/consultorio-index', TRUE, 6),
('Gestionar Cargos', '/referenciales/cargo/cargo-index', TRUE, 6),
('Gestionar Grupos', '/referenciales/grupo/grupo-index', TRUE, 6),
('Gestionar Módulos', '/referenciales/modulo/modulo-index', TRUE, 6),
('Gestionar Diagnósticos', '/referenciales/diagnostico/diagnostico-index', TRUE, 6),
('Gestionar Medicamentos', '/medicamento/medicamento-index', TRUE, 6),
('Gestionar Signos', '/signo/signo-index', TRUE, 6),
('Gestionar Síntomas', '/sintoma/sintoma-index', TRUE, 6),
('Gestionar Tipos Análisis', '/tipo-analisis/tipo-analisis-index', TRUE, 6),
('Gestionar Tipos Estudios', '/tipo-estudio/tipo-estudio-index', TRUE, 6),
('Gestionar Tipos Procedimientos', '/tipo-procedimiento/tipo-procedimiento-index', TRUE, 6),
('Gestionar Tipos Tratamientos', '/tipo-tratamiento/tipo-tratamiento-index', TRUE, 6);

-- =====================================================
-- PASO 3: ASIGNAR PERMISOS POR GRUPO
-- =====================================================

-- =====================================================
-- GRUPO 1: ADMINISTRADOR - Acceso TOTAL
-- =====================================================
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    1,      -- ID Grupo Administrador
    TRUE,   -- Leer: SÍ
    TRUE,   -- Insertar: SÍ
    TRUE,   -- Editar: SÍ
    TRUE    -- Borrar: SÍ
FROM paginas 
WHERE est_pagina = TRUE;

-- =====================================================
-- GRUPO 2: RECEPCIONISTA
-- Agendamiento + Funcionarios + Pacientes + Reportes
-- =====================================================

-- 2.1 MÓDULO USUARIO - Gestión de Funcionarios (sin eliminar)
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    2,  -- ID Grupo Recepcionista
    TRUE,  -- Leer: SÍ
    CASE WHEN des_pagina = 'Crear Funcionario' THEN TRUE ELSE FALSE END,
    CASE WHEN des_pagina = 'Editar Funcionario' THEN TRUE ELSE FALSE END,
    FALSE  -- Borrar: NO
FROM paginas 
WHERE id_modulo = 1
  AND des_pagina IN ('Lista de Funcionarios', 'Crear Funcionario', 'Editar Funcionario')
  AND est_pagina = TRUE;

-- 2.2 MÓDULO AGENDAMIENTO - Acceso Completo
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    2,  -- ID Grupo Recepcionista
    TRUE, TRUE, TRUE, TRUE
FROM paginas 
WHERE id_modulo = 2
  AND est_pagina = TRUE;

-- 2.3 MÓDULO CONSULTORIOS - Solo Pacientes (sin eliminar)
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    2,  -- ID Grupo Recepcionista
    TRUE,
    CASE WHEN des_pagina = 'Registrar Paciente' THEN TRUE ELSE FALSE END,
    CASE WHEN des_pagina = 'Editar Paciente' THEN TRUE ELSE FALSE END,
    FALSE
FROM paginas 
WHERE id_modulo = 3
  AND des_pagina IN ('Lista de Pacientes', 'Registrar Paciente', 'Editar Paciente')
  AND est_pagina = TRUE;

-- 2.4 MÓDULO REPORTES - Solo Lectura
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    2,  -- ID Grupo Recepcionista
    TRUE, FALSE, FALSE, FALSE
FROM paginas 
WHERE id_modulo = 4
  AND des_pagina IN ('Ver Reportes', 'Reporte de Citas', 'Reporte de Pacientes')
  AND est_pagina = TRUE;

-- =====================================================
-- GRUPO 3: ESPECIALISTA (Médico/Psicólogo)
-- Atención Médica + Consultas + Fichas
-- =====================================================

-- 3.1 MÓDULO AGENDAMIENTO - Solo Ver (Lectura)
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    3,  -- ID Grupo Especialista
    TRUE, FALSE, FALSE, FALSE
FROM paginas 
WHERE id_modulo = 2
  AND des_pagina IN ('Ver Agenda Médica', 'Ver Citas')
  AND est_pagina = TRUE;

-- 3.2 MÓDULO CONSULTORIOS - Acceso Completo (sin eliminar)
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    3,  -- ID Grupo Especialista
    TRUE, TRUE, TRUE, FALSE
FROM paginas 
WHERE id_modulo = 3
  AND est_pagina = TRUE;

-- 3.3 MÓDULO REPORTES - Lectura de reportes médicos
INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
SELECT 
    id_pagina, 
    3,  -- ID Grupo Especialista
    TRUE, FALSE, FALSE, FALSE
FROM paginas 
WHERE id_modulo = 4
  AND des_pagina IN ('Ver Reportes', 'Reporte de Consultas', 'Reporte de Pacientes')
  AND est_pagina = TRUE;

-- =====================================================
-- PASO 4: CONSULTAS DE VERIFICACIÓN
-- =====================================================

-- Ver TODAS las páginas insertadas
SELECT 
    m.des_modulo AS "Módulo",
    pg.id_pagina AS "ID",
    pg.des_pagina AS "Página",
    pg.pag_direcc AS "Ruta"
FROM paginas pg
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE pg.est_pagina = TRUE
ORDER BY m.id_modulo, pg.des_pagina;

-- Ver RESUMEN de permisos por grupo
SELECT 
    g.id_grupo,
    g.des_grupo AS "Grupo",
    m.des_modulo AS "Módulo",
    COUNT(*) AS "Total Páginas",
    SUM(CASE WHEN p.leer THEN 1 ELSE 0 END) AS "Ver",
    SUM(CASE WHEN p.insertar THEN 1 ELSE 0 END) AS "Crear",
    SUM(CASE WHEN p.editar THEN 1 ELSE 0 END) AS "Editar",
    SUM(CASE WHEN p.borrar THEN 1 ELSE 0 END) AS "Eliminar"
FROM permisos p
INNER JOIN grupos g ON p.id_grupo = g.id_grupo
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
GROUP BY g.id_grupo, g.des_grupo, m.des_modulo
ORDER BY g.id_grupo, m.des_modulo;

-- Ver detalle ADMINISTRADOR
SELECT 
    m.des_modulo AS "Módulo",
    pg.des_pagina AS "Página",
    pg.pag_direcc AS "Ruta",
    '✓' AS "Ver", '✓' AS "Crear", '✓' AS "Editar", '✓' AS "Eliminar"
FROM permisos p
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE p.id_grupo = 1
ORDER BY m.des_modulo, pg.des_pagina;

-- Ver detalle RECEPCIONISTA
SELECT 
    m.des_modulo AS "Módulo",
    pg.des_pagina AS "Página",
    pg.pag_direcc AS "Ruta",
    CASE WHEN p.leer THEN '✓' ELSE '✗' END AS "Ver",
    CASE WHEN p.insertar THEN '✓' ELSE '✗' END AS "Crear",
    CASE WHEN p.editar THEN '✓' ELSE '✗' END AS "Editar",
    CASE WHEN p.borrar THEN '✓' ELSE '✗' END AS "Eliminar"
FROM permisos p
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE p.id_grupo = 2
ORDER BY m.des_modulo, pg.des_pagina;

-- Ver detalle ESPECIALISTA
SELECT 
    m.des_modulo AS "Módulo",
    pg.des_pagina AS "Página",
    pg.pag_direcc AS "Ruta",
    CASE WHEN p.leer THEN '✓' ELSE '✗' END AS "Ver",
    CASE WHEN p.insertar THEN '✓' ELSE '✗' END AS "Crear",
    CASE WHEN p.editar THEN '✓' ELSE '✗' END AS "Editar",
    CASE WHEN p.borrar THEN '✓' ELSE '✗' END AS "Eliminar"
FROM permisos p
INNER JOIN paginas pg ON p.id_pagina = pg.id_pagina
INNER JOIN modulos m ON pg.id_modulo = m.id_modulo
WHERE p.id_grupo = 3
ORDER BY m.des_modulo, pg.des_pagina;

-- =====================================================
-- EJEMPLOS PARA MODIFICAR PERMISOS DESPUÉS
-- =====================================================

-- Ejemplo 1: Dar permiso de eliminar pacientes a recepcionista
-- UPDATE permisos 
-- SET borrar = TRUE
-- WHERE id_grupo = 2 
--   AND id_pagina IN (SELECT id_pagina FROM paginas WHERE des_pagina = 'Editar Paciente');

-- Ejemplo 2: Quitar permiso de crear agenda a recepcionista
-- UPDATE permisos 
-- SET insertar = FALSE
-- WHERE id_grupo = 2 
--   AND id_pagina IN (SELECT id_pagina FROM paginas WHERE des_pagina = 'Gestionar Agenda');

-- Ejemplo 3: Dar acceso completo a Configuración para especialista
-- INSERT INTO permisos (id_pagina, id_grupo, leer, insertar, editar, borrar)
-- SELECT id_pagina, 3, TRUE, TRUE, TRUE, TRUE
-- FROM paginas WHERE id_modulo = 6;

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================


-- =====================================================
-- SCRIPT PARA REINICIAR BASE DE DATOS - POSTGRESQL
-- Elimina TODOS los datos pero mantiene las tablas
-- Basado en las secuencias reales de tu BD
-- =====================================================

-- ⚠️ ADVERTENCIA: Este script elimina TODOS los datos
-- Ejecutar solo en desarrollo o cuando estés seguro

-- =====================================================
-- PASO 1: TRUNCATE CASCADE - Elimina datos respetando dependencias
-- =====================================================

-- Módulo de Seguridad y Usuarios
TRUNCATE TABLE usuarios CASCADE;
TRUNCATE TABLE funcionarios CASCADE;
TRUNCATE TABLE grupos CASCADE;
TRUNCATE TABLE modulos CASCADE;
TRUNCATE TABLE paginas CASCADE;
TRUNCATE TABLE permisos CASCADE;

-- Personas y Pacientes
TRUNCATE TABLE personas CASCADE;
TRUNCATE TABLE pacientes CASCADE;
TRUNCATE TABLE pacientes_menores CASCADE;

-- Especialistas
TRUNCATE TABLE especialistas CASCADE;
TRUNCATE TABLE especialista_especialidades CASCADE;

-- Módulo de Agendamiento
TRUNCATE TABLE recordatorios CASCADE;
TRUNCATE TABLE citas CASCADE;
TRUNCATE TABLE estados_citas CASCADE;
TRUNCATE TABLE agenda_horarios CASCADE;

-- Módulo de Consultorios
TRUNCATE TABLE anamnesis CASCADE;
TRUNCATE TABLE anamnesis_historial CASCADE;
TRUNCATE TABLE detalle_historia_clinica CASCADE;
TRUNCATE TABLE consultas CASCADE;
TRUNCATE TABLE diagnosticos CASCADE;
TRUNCATE TABLE registro_diagnosticos CASCADE;
TRUNCATE TABLE tratamientos CASCADE;
TRUNCATE TABLE registro_procedimientos CASCADE;

-- Referenciales / Configuración
TRUNCATE TABLE medicamentos CASCADE;
TRUNCATE TABLE signos CASCADE;
TRUNCATE TABLE sintomas CASCADE;
TRUNCATE TABLE tipos_analisis CASCADE;
TRUNCATE TABLE tipos_estudios CASCADE;
TRUNCATE TABLE tipos_procedimientos CASCADE;
TRUNCATE TABLE tipos_tratamientos CASCADE;
TRUNCATE TABLE consultorios CASCADE;
TRUNCATE TABLE dias_semana CASCADE;
TRUNCATE TABLE cargos CASCADE;
TRUNCATE TABLE profesiones CASCADE;
TRUNCATE TABLE niveles_instruccion CASCADE;
TRUNCATE TABLE estados_civiles CASCADE;
TRUNCATE TABLE generos CASCADE;
TRUNCATE TABLE especialidades CASCADE;
TRUNCATE TABLE ciudades CASCADE;

-- =====================================================
-- PASO 2: REINICIAR SECUENCIAS (Basado en tus secuencias reales)
-- =====================================================

-- Módulo de Usuarios
ALTER SEQUENCE usuarios_id_usuario_seq RESTART WITH 1;
ALTER SEQUENCE funcionarios_id_funcionario_seq RESTART WITH 1;
ALTER SEQUENCE grupos_id_grupo_seq RESTART WITH 1;
ALTER SEQUENCE modulos_id_modulo_seq RESTART WITH 1;
ALTER SEQUENCE paginas_id_pagina_seq RESTART WITH 1;

-- Personas y Pacientes
ALTER SEQUENCE personas_id_persona_seq RESTART WITH 1;
ALTER SEQUENCE pacientes_id_paciente_seq RESTART WITH 1;
ALTER SEQUENCE pacientes_menores_id_paciente_menor_seq RESTART WITH 1;

-- Especialistas
ALTER SEQUENCE especialistas_id_especialista_seq RESTART WITH 1;
ALTER SEQUENCE especialista_especialidades_id_seq RESTART WITH 1;

-- Módulo de Agendamiento
ALTER SEQUENCE agenda_horarios_id_agenda_horario_seq RESTART WITH 1;
ALTER SEQUENCE citas_id_cita_seq RESTART WITH 1;
ALTER SEQUENCE estados_citas_id_estado_cita_seq RESTART WITH 1;
ALTER SEQUENCE recordatorios_id_recordatorio_seq RESTART WITH 1;

-- Módulo de Consultorios
ALTER SEQUENCE anamnesis_id_anamnesis_seq RESTART WITH 1;
ALTER SEQUENCE anamnesis_historial_id_historial_seq RESTART WITH 1;
ALTER SEQUENCE detalle_historia_clinica_id_detalle_hc_seq RESTART WITH 1;
ALTER SEQUENCE consultas_id_consulta_seq RESTART WITH 1;
ALTER SEQUENCE diagnosticos_id_diagnostico_seq RESTART WITH 1;
ALTER SEQUENCE registro_diagnosticos_id_registro_diagnostico_seq RESTART WITH 1;
ALTER SEQUENCE tratamientos_id_tratamiento_seq RESTART WITH 1;
ALTER SEQUENCE registro_procedimientos_id_registro_procedimiento_seq RESTART WITH 1;

-- Referenciales
ALTER SEQUENCE ciudades_id_ciudad_seq RESTART WITH 1;
ALTER SEQUENCE especialidades_id_especialidad_seq RESTART WITH 1;
ALTER SEQUENCE generos_id_genero_seq RESTART WITH 1;
ALTER SEQUENCE estados_civiles_id_estado_civil_seq RESTART WITH 1;
ALTER SEQUENCE niveles_instruccion_id_nivel_instruccion_seq RESTART WITH 1;
ALTER SEQUENCE profesiones_id_profesion_seq RESTART WITH 1;
ALTER SEQUENCE cargos_id_cargo_seq RESTART WITH 1;
ALTER SEQUENCE dias_semana_id_dia_semana_seq RESTART WITH 1;
ALTER SEQUENCE consultorios_id_consultorio_seq RESTART WITH 1;
ALTER SEQUENCE medicamentos_id_medicamento_seq RESTART WITH 1;
ALTER SEQUENCE signos_id_signo_seq RESTART WITH 1;
ALTER SEQUENCE sintomas_id_sintoma_seq RESTART WITH 1;
ALTER SEQUENCE tipos_analisis_id_tipo_analisis_seq RESTART WITH 1;
ALTER SEQUENCE tipos_estudios_id_tipo_estudio_seq RESTART WITH 1;
ALTER SEQUENCE tipos_procedimientos_id_tipo_procedimiento_seq RESTART WITH 1;
ALTER SEQUENCE tipos_tratamientos_id_tipo_tratamiento_seq RESTART WITH 1;

-- =====================================================
-- PASO 3: VERIFICAR QUE TODO ESTÁ VACÍO
-- =====================================================

SELECT 'usuarios' AS tabla, COUNT(*) AS registros FROM usuarios
UNION ALL
SELECT 'funcionarios', COUNT(*) FROM funcionarios
UNION ALL
SELECT 'personas', COUNT(*) FROM personas
UNION ALL
SELECT 'pacientes', COUNT(*) FROM pacientes
UNION ALL
SELECT 'especialistas', COUNT(*) FROM especialistas
UNION ALL
SELECT 'citas', COUNT(*) FROM citas
UNION ALL
SELECT 'consultas', COUNT(*) FROM consultas
UNION ALL
SELECT 'agenda_horarios', COUNT(*) FROM agenda_horarios
UNION ALL
SELECT 'diagnosticos', COUNT(*) FROM diagnosticos
UNION ALL
SELECT 'tratamientos', COUNT(*) FROM tratamientos
UNION ALL
SELECT 'paginas', COUNT(*) FROM paginas
UNION ALL
SELECT 'permisos', COUNT(*) FROM permisos
UNION ALL
SELECT 'grupos', COUNT(*) FROM grupos
UNION ALL
SELECT 'modulos', COUNT(*) FROM modulos
UNION ALL
SELECT 'especialidades', COUNT(*) FROM especialidades
UNION ALL
SELECT 'ciudades', COUNT(*) FROM ciudades;

-- =====================================================
-- MENSAJE FINAL
-- =====================================================
SELECT '✓ Base de datos reiniciada correctamente' AS resultado;
SELECT '✓ Todas las tablas vacías' AS info;
SELECT '✓ Secuencias reiniciadas desde 1' AS secuencias;

-- =====================================================
-- NOTAS IMPORTANTES
-- =====================================================
-- 1. Este script usa CASCADE para eliminar datos relacionados automáticamente
-- 2. Las secuencias se reinician desde 1
-- 3. La estructura de las tablas se mantiene intacta
-- 4. Ejecuta la consulta de verificación para confirmar

-- =====================================================
-- FIN DEL SCRIPT
-- =====================================================


-- FUNCIONARIOS (Administrador, Recepcionista, Especialista)
INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono) VALUES
('Carlos', 'Ramírez', '1234567', '0981111111'),  -- Admin
('Lucía', 'Gómez', '2345678', '0981222222'),    -- Recepcionista
('Jorge', 'Benítez', '3456789', '0981333333');  -- Psicólogo especialista

INSERT INTO grupos (des_grupo) VALUES 
('Administrador'),
('Recepcionista'),
('Especialista'),
('Ventas');

INSERT INTO modulos (des_modulo) VALUES
('Gestión de Usuario'),
('Agendamiento'),
('Consultorios'),
('Reportes'),
('Ventas'),
('Configuración');



INSERT INTO cargos (des_cargo) VALUES
('Administrador'),
('Recepcionista'),
('Especialista'),
('Ventas');



-- Suponiendo cargos:
-- 1 = Administrador, 2 = Recepcionista, 3 = Especialista
INSERT INTO funcionarios (id_persona, id_cargo) VALUES
(1, 1), -- Carlos -> Admin
(2, 2), -- Lucía -> Recepcionista
(3, 3); -- Jorge -> Especialista



-- Suponiendo grupos:
-- 1 = Administrador, 2 = Recepcionista, 3 = Especialista
INSERT INTO usuarios (usu_nick, usu_clave, id_funcionario, id_grupo) VALUES
('admin', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 1, 1),
('recep1', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 2, 2),
('psico1', 'scrypt:32768:8:1$h7dNpMvyyZuWpd9D$93ad0e42372a7ec5d9ba17f556e2dc824e8694da8ce5c79737ddd310f387a26af4233e848fe5206a572aa7fb67e633cfb3baaa4f5a82853a05ae545a1c7e8e6b', 3, 3);



INSERT INTO profesiones (des_profesion) VALUES
('Estudiante'),
('Docente'),
('Empleado público'),
('Empleado privado'),
('Comerciante'),
('Profesional independiente'),
('Médico'),
('Abogado'),
('Contador'),
('Ingeniero'),
('Arquitecto'),
('Enfermero'),
('Agricultor'),
('Ganadero'),
('Empresario'),
('Técnico'),
('Ama de casa'),
('Jubilado'),
('Desempleado'),
('Otro');







-- Datos
INSERT INTO dias_semana (des_dia_semana, dia_orden, est_dia_semana) VALUES
('LUNES', 1, TRUE),
('MARTES', 2, TRUE),
('MIERCOLES', 3, TRUE),
('JUEVES', 4, TRUE),
('VIERNES', 5, TRUE),
('SABADO', 6, TRUE),
('DOMINGO', 7, TRUE);















INSERT INTO personas (per_nombre, per_apellido, per_cedula, per_telefono) VALUES
('Ana', 'Martínez', '4567890', '0981444444'),   -- Paciente adulto
('Pedro', 'Lopez', '5678901', '0981555555'),    -- Paciente adulto
('María', 'Fernández', '6789012', '0981666666'),-- Paciente adulto
('Sofía', 'García', '7890123', '0981777777'),   -- Paciente niña
('Diego', 'Torres', '8901234', '0981888888');   -- Paciente niño


-- ============================================
-- PACIENTES (adultos y niños)
-- ============================================

-- Adultos
INSERT INTO pacientes (id_persona, pac_es_menor, pac_historia_clinica, pac_observaciones) VALUES
(5, FALSE, 'HC001', 'Chequeo general'),
(6, FALSE, 'HC002', 'Consulta por estrés'),
(7, FALSE, 'HC003', 'Evaluación psicológica');

-- Niños
INSERT INTO pacientes (id_persona, pac_es_menor, pac_historia_clinica, pac_observaciones) VALUES
(8, TRUE, 'HC004', 'Problemas de conducta'),
(9, TRUE, 'HC005', 'Dificultades escolares');


-- ============================================
-- PACIENTES MENORES (datos de padres)
-- ============================================

INSERT INTO pacientes_menores (id_paciente, pam_nom_madre, pam_tel_madre, pam_nom_padre, pam_tel_padre, pam_educacion, pam_colegio, pam_tel_colegio) VALUES
(11, 'Laura García', '0981999999', 'Luis García', '0981888777', 'Primaria', 'Colegio Central', '021222333'),
(12, 'Marta Torres', '0981777666', 'Carlos Torres', '0981666555', 'Primaria', 'Colegio San Juan', '021444555');




SELECT * FROM PACIENTES;












CREATE TABLE estados_citas (
    id_estado_cita SERIAL PRIMARY KEY,
    est_cita_nombre VARCHAR(50) UNIQUE NOT NULL,
    est_cita_descripcion TEXT,
    est_cita_color VARCHAR(7),
    est_cita_activo BOOLEAN DEFAULT TRUE
);

CREATE INDEX idx_estado_cita_activo ON estados_citas(est_cita_activo) WHERE est_cita_activo = TRUE;

-- Insertar estados básicos
INSERT INTO estados_citas (est_cita_nombre, est_cita_descripcion, est_cita_color) VALUES
    ('AGENDADA', 'Cita agendada, pendiente de confirmación', '#ffc107'),
    ('CONFIRMADA', 'Cita confirmada por el paciente', '#28a745'),
    ('COMPLETADA', 'Cita realizada exitosamente', '#17a2b8'),
    ('CANCELADA', 'Cita cancelada con anticipación', '#6c757d'),
    ('INASISTENCIA', 'Paciente no asistió sin avisar', '#dc3545'),
    ('REPROGRAMADA', 'Cita movida a otra fecha', '#fd7e14');

COMMENT ON TABLE estados_citas IS 'Catálogo de estados posibles para las citas';
COMMENT ON COLUMN estados_citas.est_cita_color IS 'Color hexadecimal para representación visual en la UI';




















CREATE TABLE consultorios (
    id_consultorio SERIAL PRIMARY KEY,
    des_consultorio VARCHAR(100) NOT NULL UNIQUE,
    est_consultorio BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT
);

CREATE INDEX idx_consultorio_estado ON consultorios(est_consultorio);

-- Inserciones
INSERT INTO consultorios (des_consultorio, est_consultorio) 
VALUES 
('Consultorio 1', TRUE),
('Consultorio 2', TRUE);



CREATE TABLE dias_semana (
    id_dia_semana SERIAL PRIMARY KEY,
    des_dia_semana VARCHAR(15) NOT NULL UNIQUE,
    dia_orden INT NOT NULL UNIQUE, -- Para ordenar correctamente
    est_dia_semana BOOLEAN DEFAULT TRUE
);

-- Datos
INSERT INTO dias_semana (dCREATE TABLE agenda_cabecera (
    id_agenda SERIAL PRIMARY KEY,
    id_consultorio INT NOT NULL,
    id_especialista INT NOT NULL,
    id_especialidad INT NOT NULL,
    id_dia_semana INT NOT NULL, -- CAMBIO: ahora FK
    age_hora_inicio TIME NOT NULL,
    age_hora_fin TIME NOT NULL,
    age_duracion_turno INT NOT NULL,
    age_cupos_totales INT NOT NULL,
    age_fecha_vigencia_desde DATE NOT NULL,
    age_fecha_vigencia_hasta DATE,
    age_observaciones TEXT,
    est_agenda BOOLEAN DEFAULT TRUE,
    
    -- Auditoría
    creacion_fecha DATE NOT NULL DEFAULT CURRENT_DATE,
    creacion_hora TIME NOT NULL DEFAULT CURRENT_TIME,
    creacion_usuario INT NOT NULL DEFAULT 1,
    modificacion_fecha DATE,
    modificacion_hora TIME,
    modificacion_usuario INT,
    
    FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialista) REFERENCES especialistas(id_especialista) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad) 
        ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (id_dia_semana) REFERENCES dias_semana(id_dia_semana)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    
    UNIQUE(id_consultorio, id_especialista, id_dia_semana, age_hora_inicio)
);

CREATE INDEX idx_agenda_especialista ON agenda_cabecera(id_especialista);
CREATE INDEX idx_agenda_consultorio ON agenda_cabecera(id_consultorio);
CREATE INDEX idx_agenda_dia ON agenda_cabecera(id_dia_semana, est_agenda);
CREATE INDEX idx_agenda_vigencia ON agenda_cabecera(age_fecha_vigencia_desde, age_fecha_vigencia_hasta);

-- Inserciones ajustadas
INSERT INTO agenda_cabecera (
    id_consultorio, id_especialista, id_especialidad, 
    id_dia_semana, age_hora_inicio, age_hora_fin, 
    age_duracion_turno, age_cupos_totales, 
    age_fecha_vigencia_desde, age_observaciones, est_agenda
) 
VALUES 
(1, 1, 1, 1, '08:00', '12:00', 30, 8, '2025-01-01', 'Agenda de fonoaudiología - mañana', TRUE), -- 1=lunes
(1, 1, 1, 3, '14:00', '18:00', 45, 5, '2025-01-01', 'Agenda de fonoaudiología - tarde', TRUE); -- 3=miercoleses_dia_semana, dia_orden, est_dia_semana) VALUES
('lunes', 1, TRUE),
('martes', 2, TRUE),
('miercoles', 3, TRUE),
('jueves', 4, TRUE),
('viernes', 5, TRUE),
('sabado', 6, TRUE),
('domingo', 7, TRUE);




{% extends 'base.html' %}


{% block titulo %}
Dashboard - Inicio
{% endblock %}


{% block contenido %}


<style>
 .stat-counter {
   animation: countUp 0.8s ease-out;
 }
  @keyframes countUp {
   from { opacity: 0; transform: translateY(20px); }
   to { opacity: 1; transform: translateY(0); }
 }


 .module-card {
   transition: all 0.3s ease;
   border: none;
 }


 .module-card:hover {
   transform: translateY(-5px);
   box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
 }


 .hero-gradient {
   background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
 }


 .cita-card {
   transition: all 0.2s ease;
 }


 .cita-card:hover {
   box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
 }
</style>


<!-- ========================================== -->
<!-- HERO SECTION - Personalizado por Rol -->
<!-- ========================================== -->
<div class="hero-gradient text-white rounded-lg shadow-lg mb-4 p-4 p-md-5">
 <div class="row align-items-center">
   <div class="col-lg-8">
     {% if es_admin() %}
       <h1 class="h2 mb-3 font-weight-bold">
         <i class="fas fa-user-shield mr-2"></i>
         Panel de Administración
       </h1>
       <p class="lead mb-4">Control total del sistema - Gestión de usuarios, configuración y reportes</p>
     {% elif es_recepcion() %}
       <h1 class="h2 mb-3 font-weight-bold">
         <i class="fas fa-calendar-check mr-2"></i>
         Panel de Recepción
       </h1>
       <p class="lead mb-4">Gestión de citas, agendamiento y atención a pacientes</p>
     {% elif es_especialista() %}
      <h1 class="h2 mb-3 font-weight-bold">
       <span class="mr-2" style="font-size: 1.3em;">Ψ</span>
       Panel Especialista
     </h1>


       <p class="lead mb-4">Consultas, diagnósticos y seguimiento de pacientes</p>
     {% else %}
       <h1 class="h2 mb-3 font-weight-bold">
         <i class="fas fa-brain mr-2"></i>
         Bienvenido al Sistema CIN
       </h1>
       <p class="lead mb-4">Panel de control integral para la gestión de tu clínica</p>
     {% endif %}


     <div class="d-flex flex-wrap gap-3 mb-3">
       {% if es_recepcion() or es_admin() %}
       <a href="{{ url_for('cita.citaIndex') }}" class="btn btn-light btn-lg shadow-sm">
         <i class="fas fa-calendar-plus mr-2"></i>Nueva Cita
       </a>
       {% endif %}
      
       {% if es_especialista() %}
       <a href="{{ url_for('registrarconsulta.consultaIndex') }}" class="btn btn-light btn-lg shadow-sm">
         <i class="fas fa-notes-medical mr-2"></i>Registrar Consulta
       </a>
       {% endif %}
      
       <button onclick="mostrarContacto()" class="btn btn-outline-light btn-lg">
         <i class="fas fa-phone-alt mr-2"></i>Contacto
       </button>
     </div>


     <div class="mt-4 d-flex flex-wrap gap-4 small">
       <div>
         <i class="fas fa-clock mr-2"></i>
         <span>Lun-Vie: 8:00 - 18:00</span>
       </div>
       <div>
         <i class="fas fa-phone mr-2"></i>
         <span>+595 982 388921</span>
       </div>
       <div>
         <i class="fas fa-envelope mr-2"></i>
         <span>clinicainterneuropsicologica@gmail.com</span>
       </div>
     </div>
   </div>
   <div class="col-lg-4 d-none d-lg-flex justify-content-center align-items-center">
     <img src="{{ url_for('static', filename='img/cin.avif') }}"
    alt="Clínica Integral Neuropsicológica"
    class="img-fluid rounded shadow-lg w-100"
    style="max-height: 400px; object-fit: contain;">


   </div>
 </div>
</div>


<!-- ========================================== -->
<!-- ESTADÍSTICAS - Personalizadas por Rol -->
<!-- ========================================== -->
<div class="row mb-4">
  {% if es_admin() %}
   <!-- ESTADÍSTICAS PARA ADMINISTRADOR -->
   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-primary shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Total Usuarios</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="totalUsuarios">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-users fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-success shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Ingresos del Mes</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="ingresosMes">₲ 0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-dollar-sign fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-info shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Citas Hoy</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="citasHoy">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-calendar-day fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-warning shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Pacientes Activos</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="pacientesActivos">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-user-injured fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


 {% elif es_recepcion() %}
   <!-- ESTADÍSTICAS PARA RECEPCIONISTA -->
   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-primary shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Citas Hoy</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="citasHoy">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-calendar-day fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-warning shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Citas Pendientes</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="citasPendientes">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-clock fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-success shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Citas Confirmadas</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="citasConfirmadas">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-check-circle fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-info shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Próxima Cita</div>
             <div class="h6 mb-0 font-weight-bold text-gray-800" id="proximaCita">Cargando...</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-calendar-check fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


 {% elif es_especialista() %}
   <!-- ESTADÍSTICAS PARA ESPECIALISTA -->
   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-primary shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">Pacientes Asignados</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="pacientesAsignados">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-user-injured fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-info shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-info text-uppercase mb-1">Consultas Hoy</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="consultasHoy">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-notes-medical fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-warning shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">Pendientes Informe</div>
             <div class="h5 mb-0 font-weight-bold text-gray-800 stat-counter" id="informesPendientes">0</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-file-medical-alt fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-md-6 mb-4">
     <div class="card border-left-success shadow h-100 py-2">
       <div class="card-body">
         <div class="row no-gutters align-items-center">
           <div class="col mr-2">
             <div class="text-xs font-weight-bold text-success text-uppercase mb-1">Próxima Sesión</div>
             <div class="h6 mb-0 font-weight-bold text-gray-800" id="proximaSesion">Cargando...</div>
           </div>
           <div class="col-auto">
             <i class="fas fa-calendar-alt fa-2x text-gray-300"></i>
           </div>
         </div>
       </div>
     </div>
   </div>
 {% endif %}


</div>


<!-- ========================================== -->
<!-- MÓDULOS - Filtrados por Rol -->
<!-- ========================================== -->
<div class="d-sm-flex align-items-center justify-content-between mb-4">
 <h1 class="h3 mb-0 text-gray-800">
   <i class="fas fa-th-large mr-2"></i>
   {% if es_admin() %}Módulos del Sistema{% elif es_recepcion() %}Mis Módulos{% else %}Accesos Rápidos{% endif %}
 </h1>
</div>


<div class="row">
  {% if es_admin() %}
   <!-- MÓDULOS PARA ADMINISTRADOR (TODOS) -->
   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%);">
         <div class="text-white text-center">
           <i class="fas fa-users-cog fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Gestión Usuarios</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Funcionarios, roles y permisos del sistema.</p>
         <div class="mt-auto">
           <a href="{{ url_for('funcionario.funcionarioIndex') }}" class="btn btn-secondary btn-block" style="background-color: #805ad5; border-color: #805ad5;">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);">
         <div class="text-white text-center">
           <i class="fas fa-calendar-alt fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Agendamiento</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Gestiona citas, horarios y turnos.</p>
         <div class="mt-auto">
           <a href="{{ url_for('agenda.agendaIndex') }}" class="btn btn-primary btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
         <div class="text-white text-center">
           <i class="fas fa-stethoscope fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Consultorios</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Fichas médicas, diagnósticos y tratamientos.</p>
         <div class="mt-auto">
           <a href="{{ url_for('registrarconsulta.consultaIndex') }}" class="btn btn-success btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);">
         <div class="text-white text-center">
           <i class="fas fa-database fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Referenciales</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Configuración y datos maestros.</p>
         <div class="mt-auto">
           <a href="{{ url_for('ciudad.ciudadIndex') }}" class="btn btn-warning btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


 {% elif es_recepcion() %}
   <!-- MÓDULOS PARA RECEPCIONISTA -->
   <div class="col-xl-4 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);">
         <div class="text-white text-center">
           <i class="fas fa-calendar-alt fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Agendamiento</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Gestiona citas y agenda médica completa.</p>
         <div class="mt-auto">
           <a href="{{ url_for('agenda.agendaIndex') }}" class="btn btn-primary btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-4 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);">
         <div class="text-white text-center">
           <i class="fas fa-user-injured fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Pacientes</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Registro y gestión de pacientes.</p>
         <div class="mt-auto">
           <a href="{{ url_for('paciente.pacienteIndex') }}" class="btn btn-warning btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-4 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
         <div class="text-white text-center">
           <i class="fas fa-file-medical fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Fichas Médicas</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Consulta historiales clínicos.</p>
         <div class="mt-auto">
           <a href="{{ url_for('fichamedica.fichaMedicaIndex') }}" class="btn btn-success btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


 {% elif es_especialista() %}
   <!-- MÓDULOS PARA ESPECIALISTA -->
   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #48bb78 0%, #38a169 100%);">
         <div class="text-white text-center">
           <i class="fas fa-notes-medical fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Registrar Consulta</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Nueva consulta médica o psicológica.</p>
         <div class="mt-auto">
           <a href="{{ url_for('registrarconsulta.consultaIndex') }}" class="btn btn-success btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #4299e1 0%, #3182ce 100%);">
         <div class="text-white text-center">
           <i class="fas fa-diagnoses fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Diagnósticos</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Registro de diagnósticos clínicos.</p>
         <div class="mt-auto">
           <a href="{{ url_for('registrardiagnostico.diagnosticoIndex') }}" class="btn btn-primary btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%);">
         <div class="text-white text-center">
           <i class="fas fa-pills fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Tratamientos</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Prescripción de tratamientos.</p>
         <div class="mt-auto">
           <a href="{{ url_for('registrartratamiento.tratamientoIndex') }}" class="btn btn-warning btn-block">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>


   <div class="col-xl-3 col-lg-6 mb-4">
     <div class="card module-card shadow-sm h-100">
       <div class="card-header py-3" style="background: linear-gradient(135deg, #9f7aea 0%, #805ad5 100%);">
         <div class="text-white text-center">
           <i class="fas fa-file-medical fa-3x mb-2"></i>
           <h6 class="m-0 font-weight-bold">Anamnesis</h6>
         </div>
       </div>
       <div class="card-body d-flex flex-column">
         <p class="text-muted small mb-3">Historiales y evaluaciones completas.</p>
         <div class="mt-auto">
           <a href="{{ url_for('anamnesis.anamnesisIndex') }}" class="btn btn-secondary btn-block" style="background-color: #805ad5; border-color: #805ad5;">
             <i class="fas fa-arrow-right mr-2"></i>Acceder
           </a>
         </div>
       </div>
     </div>
   </div>
 {% endif %}


</div>


<!-- ========================================== -->
<!-- CITAS DEL DÍA Y MAÑANA -->
<!-- ========================================== -->
{% if es_recepcion() or es_admin() or es_especialista() %}
<div class="row">
  <!-- Citas de Hoy -->
 <div class="col-lg-6 mb-4">
   <div class="card shadow h-100">
     <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
       <h6 class="m-0 font-weight-bold text-primary">
         <i class="fas fa-calendar-day mr-2"></i>
         {% if es_especialista() %}Mis Pacientes Hoy{% else %}Citas de Hoy{% endif %}
       </h6>
       <span class="text-muted small" id="fechaHoy"></span>
     </div>
     <div class="card-body">
       <div id="listaCitas" style="max-height: 500px; overflow-y: auto;">
         <div class="text-center py-4">
           <div class="spinner-border text-primary" role="status">
             <span class="sr-only">Cargando...</span>
           </div>
           <p class="text-muted mt-2">Cargando citas...</p>
         </div>
       </div>
       <div class="text-center mt-3">
         <a href="{{ url_for('cita.citaIndex') }}" class="btn btn-sm btn-outline-primary">
           Ver todas las citas <i class="fas fa-arrow-right ml-2"></i>
         </a>
       </div>
     </div>
   </div>
 </div>


 <!-- Citas de Mañana -->
 <div class="col-lg-6 mb-4">
   <div class="card shadow h-100">
     <div class="card-header py-3 d-flex flex-row align-items-center justify-content-between">
       <h6 class="m-0 font-weight-bold text-success">
         <i class="fas fa-calendar-plus mr-2"></i>
         {% if es_especialista() %}Mis Pacientes Mañana{% else %}Citas de Mañana{% endif %}
       </h6>
       <span class="text-muted small" id="fechaManana"></span>
     </div>
     <div class="card-body">
       <div id="listaCitasManana" style="max-height: 500px; overflow-y: auto;">
         <div class="text-center py-4">
           <div class="spinner-border text-success" role="status">
             <span class="sr-only">Cargando...</span>
           </div>
           <p class="text-muted mt-2">Cargando citas...</p>
         </div>
       </div>
       <div class="text-center mt-3">
         <a href="{{ url_for('cita.citaIndex') }}" class="btn btn-sm btn-outline-success">
           Ver todas las citas <i class="fas fa-arrow-right ml-2"></i>
         </a>
       </div>
     </div>
   </div>
 </div>


</div>
{% endif %}


<!-- Modal de Contacto -->
<div class="modal fade" id="modalContacto" tabindex="-1" role="dialog" aria-hidden="true">
 <div class="modal-dialog modal-dialog-centered" role="document">
   <div class="modal-content">
     <div class="modal-header" style="background-color: #4f46e5; color: white;">
       <h5 class="modal-title">
         <i class="fas fa-phone-alt mr-2"></i>Información de Contacto
       </h5>
       <button type="button" class="close text-white" data-dismiss="modal" aria-label="Close">
         <span aria-hidden="true">&times;</span>
       </button>
     </div>
     <div class="modal-body">
       <div class="mb-3 p-3 bg-light rounded">
         <div class="d-flex align-items-center">
           <i class="fas fa-phone fa-2x text-primary mr-3"></i>
           <div>
             <small class="text-muted d-block">Teléfono / WhatsApp</small>
             <strong>+595 982 388921</strong>
           </div>
         </div>
       </div>
       <div class="mb-3 p-3 bg-light rounded">
         <div class="d-flex align-items-center">
           <i class="fas fa-envelope fa-2x text-primary mr-3"></i>
           <div>
             <small class="text-muted d-block">Email</small>
             <strong>clinicainterneuropsicologica@gmail.com</strong>
           </div>
         </div>
       </div>
       <div class="p-3 bg-light rounded mb-3">
         <div class="d-flex align-items-center">
           <i class="fas fa-map-marker-alt fa-2x text-primary mr-3"></i>
           <div>
             <small class="text-muted d-block">Dirección</small>
             <strong>José Martí 5160, Asunción, Paraguay</strong>
           </div>
         </div>
       </div>
      
       <div class="mt-4">
         <a href="https://wa.me/595982388921" target="_blank" class="btn btn-success btn-block mb-2">
           <i class="fab fa-whatsapp mr-2"></i>Contactar por WhatsApp
         </a>
         <a href="mailto:clinicainterneuropsicologica@gmail.com" class="btn btn-primary btn-block mb-2">
           <i class="fas fa-envelope mr-2"></i>Enviar Email
         </a>
         <a href="https://www.google.com/maps/search/?api=1&query=José+Martí+5160,+Asunción,+Paraguay" target="_blank" class="btn btn-outline-secondary btn-block">
           <i class="fas fa-map-marked-alt mr-2"></i>Ver en Google Maps
         </a>
       </div>
     </div>
     <div class="modal-footer">
       <button type="button" class="btn btn-secondary" data-dismiss="modal">Cerrar</button>
     </div>
   </div>
 </div>
</div>


{% endblock %}








{% block js %}
<script>
// ============================================
// CONFIGURACIÓN DEL ROL DE USUARIO
// ============================================
const usuarioRol = {
 esAdmin: data_usuario.esAdmin ? true : false,
 esRecepcion: data_usuario.esRecepcion ? true : false,
 esEspecialista: data_usuario.esEspecialista ? true : false,
 grupoId: data_usuario.grupoId || '',
 nombre: data_usuario.nombre || ''
};


// ============================================
// INICIALIZACIÓN PRINCIPAL
// ============================================
$(document).ready(function() {
 console.log('Dashboard cargado - Rol:',
   usuarioRol.esAdmin ? 'Admin' :
   usuarioRol.esRecepcion ? 'Recepción' :
   usuarioRol.esEspecialista ? 'Especialista' : 'Desconocido'
 );
 console.log('Datos del usuario:', usuarioRol);
});


   // Configurar fechas
   configurarFechas();
  
   // Cargar datos iniciales
   cargarEstadisticas();
   cargarCitasHoy();
   cargarCitasManana();
  
   // Actualizar automáticamente cada 30 segundos
   setInterval(function() {
     cargarEstadisticas();
     cargarCitasHoy();
     cargarCitasManana();
   }, 30000);




 // ========================================
 // CONFIGURAR FECHAS EN EL DASHBOARD
 // ========================================
 function configurarFechas() {
   const hoy = new Date();
   const manana = new Date(hoy);
   manana.setDate(manana.getDate() + 1);
  
   const opciones = {
     weekday: 'long',
     year: 'numeric',
     month: 'long',
     day: 'numeric'
   };
  
   $('#fechaHoy').text(hoy.toLocaleDateString('es-ES', opciones));
   $('#fechaManana').text(manana.toLocaleDateString('es-ES', opciones));
 }


 // ========================================
 // CARGAR ESTADÍSTICAS DESDE LA API
 // ========================================
 function cargarEstadisticas() {
   $.ajax({
     url: '/api/v1/estadisticas',
     method: 'GET',
     dataType: 'json',
     success: function(response) {
       console.log('Estadísticas recibidas:', response);
       if (response.success) {
         mostrarEstadisticasSegunRol(response);
       } else {
         console.error('Error en respuesta:', response.error);
         cargarEstadisticasPorDefecto();
       }
     },
     error: function(xhr, status, error) {
       console.error('Error cargando estadísticas:', error);
       console.error('Status:', status);
       console.error('Respuesta:', xhr.responseText);
       cargarEstadisticasPorDefecto();
     }
   });
 }


 // ========================================
 // MOSTRAR ESTADÍSTICAS SEGÚN ROL
 // ========================================
 function mostrarEstadisticasSegunRol(response) {
   if (usuarioRol.esAdmin) {
     // Estadísticas para Administrador
     animarContador('#totalUsuarios', response.total_usuarios || 0);
     $('#ingresosMes').text('₲ ' + formatearNumero(response.ingresos_mes || 0));
     animarContador('#citasHoy', response.citas_hoy || 0);
     animarContador('#pacientesActivos', response.pacientes_activos || 0);
    
   } else if (usuarioRol.esRecepcion) {
     // Estadísticas para Recepcionista
     animarContador('#citasHoy', response.citas_hoy || 0);
     animarContador('#citasPendientes', response.citas_pendientes || 0);
     animarContador('#citasConfirmadas', response.citas_confirmadas || 0);
     $('#proximaCita').text(response.proxima_cita || 'Sin citas pendientes');
    
   } else if (usuarioRol.esEspecialista) {
     // Estadísticas para Especialista
     animarContador('#pacientesAsignados', response.pacientes_asignados || 0);
     animarContador('#consultasHoy', response.consultas_hoy || 0);
     animarContador('#informesPendientes', response.informes_pendientes || 0);
     $('#proximaSesion').text(response.proxima_sesion || 'Sin sesiones hoy');
   }
 }


 // ========================================
 // CARGAR VALORES POR DEFECTO EN CASO DE ERROR
 // ========================================
 function cargarEstadisticasPorDefecto() {
   if (usuarioRol.esAdmin) {
     animarContador('#totalUsuarios', 0);
     $('#ingresosMes').text('₲ 0');
     animarContador('#citasHoy', 0);
     animarContador('#pacientesActivos', 0);
    
   } else if (usuarioRol.esRecepcion) {
     animarContador('#citasHoy', 0);
     animarContador('#citasPendientes', 0);
     animarContador('#citasConfirmadas', 0);
     $('#proximaCita').text('Sin citas');
    
   } else if (usuarioRol.esEspecialista) {
     animarContador('#pacientesAsignados', 0);
     animarContador('#consultasHoy', 0);
     animarContador('#informesPendientes', 0);
     $('#proximaSesion').text('Sin sesiones');
   }
 }


 // ========================================
 // CARGAR CITAS DEL DÍA DESDE LA API
 // ========================================
 function cargarCitasHoy() {
   $.ajax({
     url: '/api/v1/citas-hoy',
     method: 'GET',
     dataType: 'json',
     success: function(response) {
       console.log('Citas de hoy recibidas:', response);
       if (response.success && response.citas && response.citas.length > 0) {
         let html = '';
        
         response.citas.forEach(function(cita) {
           html += generarHTMLCita(cita);
         });
        
         $('#listaCitas').html(html);
       } else {
         $('#listaCitas').html(`
           <div class="text-center py-4">
             <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
             <p class="text-muted">No hay citas programadas para hoy</p>
           </div>
         `);
       }
     },
     error: function(xhr, status, error) {
       console.error('Error cargando citas:', error);
       console.error('Status:', status);
       console.error('Detalles:', xhr.responseText);
       $('#listaCitas').html(`
         <div class="alert alert-warning">
           <i class="fas fa-exclamation-triangle mr-2"></i>
           Error al cargar las citas del día
         </div>
       `);
     }
   });
 }


 // ========================================
 // CARGAR CITAS DE MAÑANA DESDE LA API
 // ========================================
 function cargarCitasManana() {
   $.ajax({
     url: '/api/v1/citas-manana',
     method: 'GET',
     dataType: 'json',
     success: function(response) {
       console.log('Citas de mañana recibidas:', response);
       if (response.success && response.citas && response.citas.length > 0) {
         let html = '';
        
         response.citas.forEach(function(cita) {
           html += generarHTMLCita(cita);
         });
        
         $('#listaCitasManana').html(html);
       } else {
         $('#listaCitasManana').html(`
           <div class="text-center py-4">
             <i class="fas fa-calendar-times fa-3x text-muted mb-3"></i>
             <p class="text-muted">No hay citas programadas para mañana</p>
           </div>
         `);
       }
     },
     error: function(xhr, status, error) {
       console.error('Error cargando citas de mañana:', error);
       console.error('Status:', status);
       console.error('Detalles:', xhr.responseText);
       $('#listaCitasManana').html(`
         <div class="alert alert-warning">
           <i class="fas fa-exclamation-triangle mr-2"></i>
           Error al cargar las citas de mañana
         </div>
       `);
     }
   });
 }


 // ========================================
 // GENERAR HTML DE UNA CITA
 // ========================================
 function generarHTMLCita(cita) {
   // Mapeo de estados con sus estilos
   const estadosMap = {
     'agendada': {
       class: 'warning',
       icon: 'clock',
       texto: 'Agendada'
     },
     'pendiente': {
       class: 'warning',
       icon: 'clock',
       texto: 'Pendiente'
     },
     'confirmada': {
       class: 'success',
       icon: 'check',
       texto: 'Confirmada'
     },
     'completada': {
       class: 'info',
       icon: 'check-circle',
       texto: 'Completada'
     },
     'cancelada': {
       class: 'danger',
       icon: 'times',
       texto: 'Cancelada'
     }
   };
  
   const estadoNormalizado = (cita.estado || 'pendiente').toLowerCase();
   const estadoConfig = estadosMap[estadoNormalizado] || estadosMap['pendiente'];
  
   const especialidad = cita.especialidad ? `<small class="text-muted">${cita.especialidad}</small>` : '';
   const observacion = cita.observacion ? `
     <div class="small text-muted">
       <i class="fas fa-comment mr-1"></i>${cita.observacion}
     </div>
   ` : '';
  
   return `
     <div class="cita-card mb-3 p-3 border-left border-left-${estadoConfig.class} rounded shadow-sm">
       <div class="row align-items-center">
         <div class="col-auto">
           <div class="text-center">
             <div class="h5 mb-0 font-weight-bold text-primary">${cita.hora}</div>
             ${especialidad}
           </div>
         </div>
        
         <div class="col">
           <div class="font-weight-bold text-gray-800 mb-1">
             <i class="fas fa-user text-primary mr-2"></i>${cita.paciente}
           </div>
           <div class="small text-muted mb-1">
             <i class="fas fa-user-md mr-1"></i>${cita.profesional}
           </div>
           ${observacion}
         </div>
        
         <div class="col-auto">
           <span class="badge badge-${estadoConfig.class} badge-pill px-3 py-2">
             <i class="fas fa-${estadoConfig.icon} mr-1"></i>${estadoConfig.texto}
           </span>
         </div>
       </div>
     </div>
   `;
 }


 // ========================================
 // ANIMACIÓN DE CONTADORES NUMÉRICOS
 // ========================================
 function animarContador(selector, valorFinal) {
   const $elemento = $(selector);
   const valorInicial = 0;
   const duracion = 1500;
   const pasos = 60;
   const incremento = Math.ceil(valorFinal / pasos);
   const intervaloTiempo = duracion / pasos;
  
   let valorActual = valorInicial;
  
   const intervalo = setInterval(function() {
     valorActual += incremento;
    
     if (valorActual >= valorFinal) {
       $elemento.text(formatearNumero(valorFinal));
       clearInterval(intervalo);
     } else {
       $elemento.text(formatearNumero(valorActual));
     }
   }, intervaloTiempo);
 }


 // ========================================
 // FORMATEAR NÚMEROS CON SEPARADOR DE MILES
 // ========================================
 function formatearNumero(numero) {
   if (numero === null || numero === undefined) {
     return '0';
   }
   return numero.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
 }


 // ========================================
 // FUNCIONES DE MODAL
 // ========================================
 function mostrarContacto() {
   $('#modalContacto').modal('show');
 }


 // ========================================
 // ACTUALIZACIÓN MANUAL
 // ========================================
 function actualizarDashboard() {
   const $btnActualizar = $('#btnActualizar');
   const iconoOriginal = $btnActualizar.html();
  
   $btnActualizar.html('<i class="fas fa-spinner fa-spin"></i>').prop('disabled', true);
  
   cargarEstadisticas();
   cargarCitasHoy();
   cargarCitasManana();
  
   setTimeout(function() {
     $btnActualizar.html(iconoOriginal).prop('disabled', false);
    
     if (typeof Swal !== 'undefined') {
       Swal.fire({
         icon: 'success',
         title: 'Actualizado',
         text: 'Dashboard actualizado correctamente',
         timer: 1500,
         showConfirmButton: false
       });
     }
   }, 2000);
 }


 // ========================================
 // MANEJO DE ERRORES GLOBAL
 // ========================================
 window.onerror = function(msg, url, lineNo, columnNo, error) {
   console.error('Error global capturado:', {
     mensaje: msg,
     url: url,
     linea: lineNo,
     columna: columnNo,
     error: error
   });
   return false;
 };
</script>
{% endblock %}

