CREATE TABLE citas (
    id SERIAL PRIMARY KEY,
    nombrepaciente VARCHAR(100) NOT NULL,
    motivoconsulta VARCHAR(255) NOT NULL,
    medico VARCHAR(100) NOT NULL,
    fecha DATE NOT NULL,
    hora TIME NOT NULL
);