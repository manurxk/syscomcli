-- 111_catalogos_clinicos_psicologia.sql
-- Catálogos clínicos orientados a la especialidad de la clínica (psicología y psiquiatría
-- infantil), aprobado por el usuario 2026-10-13. Antes tenían datos de medicina general
-- (Radiografía de Tórax, Ibuprofeno) o estaban vacíos (tratamientos, instrumentos).
--
-- - Los ítems de medicina general se DESACTIVAN (no se borran): ya los usan órdenes y
--   recetas de prueba y la historia clínica no se modifica.
-- - Hemograma se conserva (control de algunos psicofármacos) y se pasa a mayúsculas.
-- - Nombres en mayúsculas y solo con letras, números, acentos, espacios y puntos: la misma
--   regla que validarDescripcion de cada ABM, para que se puedan editar desde las pantallas.
-- - ON CONFLICT DO NOTHING: se puede volver a ejecutar sin duplicar.
--
--   Get-Content migrations\111_catalogos_clinicos_psicologia.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

-- 1. Medicina general: dar de baja (se conservan por la historia que ya los referencia)
UPDATE tipos_estudios SET est_tipo_estudio = FALSE WHERE des_tipo_estudio = 'Radiografía de Tórax';
UPDATE medicamentos   SET est_medicamento  = FALSE WHERE des_medicamento  = 'Ibuprofeno 400mg';
UPDATE tipos_analisis SET des_tipo_analisis = 'HEMOGRAMA COMPLETO' WHERE des_tipo_analisis = 'Hemograma Completo';

-- 2. Estudios y evaluaciones
INSERT INTO tipos_estudios (des_tipo_estudio) VALUES
    ('EVALUACIÓN PSICODIAGNÓSTICA'),
    ('EVALUACIÓN NEUROPSICOLÓGICA'),
    ('EVALUACIÓN PSICOPEDAGÓGICA'),
    ('EVALUACIÓN FONOAUDIOLÓGICA'),
    ('ELECTROENCEFALOGRAMA'),
    ('RESONANCIA MAGNÉTICA DE CEREBRO'),
    ('AUDIOMETRÍA')
ON CONFLICT (des_tipo_estudio) DO NOTHING;

-- 3. Análisis de laboratorio
INSERT INTO tipos_analisis (des_tipo_analisis) VALUES
    ('HEMOGRAMA COMPLETO'),
    ('PERFIL TIROIDEO TSH Y T4 LIBRE'),
    ('LITEMIA'),
    ('DOSAJE DE ÁCIDO VALPROICO'),
    ('PERFIL HEPÁTICO'),
    ('GLUCEMIA'),
    ('PERFIL LIPÍDICO'),
    ('VITAMINA B12 Y ÁCIDO FÓLICO')
ON CONFLICT (des_tipo_analisis) DO NOTHING;

-- 4. Medicamentos (los prescribe Psiquiatría infantil)
INSERT INTO medicamentos (des_medicamento) VALUES
    ('METILFENIDATO 10 MG'),
    ('ATOMOXETINA 18 MG'),
    ('SERTRALINA 50 MG'),
    ('FLUOXETINA 20 MG'),
    ('ESCITALOPRAM 10 MG'),
    ('RISPERIDONA 1 MG'),
    ('ARIPIPRAZOL 5 MG'),
    ('MELATONINA 3 MG')
ON CONFLICT (des_medicamento) DO NOTHING;

-- 5. Tipos de tratamiento
INSERT INTO tipos_tratamientos (des_tipo_tratamiento) VALUES
    ('PSICOTERAPIA INDIVIDUAL'),
    ('TERAPIA COGNITIVO CONDUCTUAL'),
    ('TERAPIA FAMILIAR'),
    ('TERAPIA DE JUEGO'),
    ('PSICOPEDAGOGÍA'),
    ('ENTRENAMIENTO A PADRES')
ON CONFLICT (des_tipo_tratamiento) DO NOTHING;

-- 6. Instrumentos de evaluación
INSERT INTO instrumentos (des_instrumento) VALUES
    ('WISC V'),
    ('WAIS IV'),
    ('TEST GESTÁLTICO VISOMOTOR DE BENDER'),
    ('HTP CASA ÁRBOL PERSONA'),
    ('CBCL ACHENBACH'),
    ('CONNERS 3'),
    ('BDI II INVENTARIO DE DEPRESIÓN DE BECK'),
    ('ESCALA DE ANSIEDAD DE HAMILTON')
ON CONFLICT (des_instrumento) DO NOTHING;

COMMIT;

-- Vuelta atrás (solo si hiciera falta): desactivar los ítems nuevos con UPDATE ... SET est_... = FALSE
-- (no borrarlos si ya los usa alguna orden, receta o tratamiento) y reactivar los dos de medicina general.
