-- 109_campos_vacios_redundancia.sql
-- PDF 3 (Base de datos), paso 4: campos vacíos (criterio 8), redundancia (criterio 7)
-- y tipo de las columnas de auditoría de remisiones (criterios 1 y 4).
-- Decisiones del usuario 2026-10-13: D4 (eliminar citas.id_agenda_horario), H12 (remisiones).
--
-- 1. citas.id_agenda_horario: 100 % vacía (32 de 32) y redundante. La cita llega a su agenda
--    por id_slot_agenda -> slots_agenda.id_agenda_horario (dependencia transitiva). Ningún
--    código, vista ni función la lee (verificado 2026-10-13). Se elimina con su FK.
-- 2. remisiones.usuario_creacion / usuario_modificacion eran character varying y sin FK
--    (única tabla así). Pasan a integer + FK a usuarios, como las otras 94 tablas.
-- 3. COMMENT ON COLUMN en las columnas vacías que dependen de SIFEN o de un flujo todavía
--    no usado: la explicación queda en la propia base (clasificación completa en
--    docs/taller_programacion/03_plan_base_datos.md §2).
--
--   Get-Content migrations\109_campos_vacios_redundancia.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

BEGIN;

-- 1. Columna redundante
ALTER TABLE citas DROP COLUMN id_agenda_horario;   -- arrastra citas_id_agenda_horario_fkey

-- 2. Tipo de las columnas de auditoría de remisiones
ALTER TABLE remisiones
    ALTER COLUMN usuario_creacion TYPE integer USING NULLIF(usuario_creacion, '')::integer,
    ALTER COLUMN usuario_modificacion TYPE integer USING NULLIF(usuario_modificacion, '')::integer,
    ADD CONSTRAINT remisiones_usuario_creacion_fkey
        FOREIGN KEY (usuario_creacion) REFERENCES usuarios(id_usuario),
    ADD CONSTRAINT remisiones_usuario_modificacion_fkey
        FOREIGN KEY (usuario_modificacion) REFERENCES usuarios(id_usuario);

-- 3. Columnas vacías documentadas
-- 3a. Dependen de SIFEN (facturación electrónica, todavía sin conexión con la SET)
COMMENT ON COLUMN facturas.codigo_sifen IS
    'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';
COMMENT ON COLUMN libro_ventas.codigo_sifen IS
    'CDC del comprobante en SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';
COMMENT ON COLUMN notas_credito.codigo_sifen IS
    'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';
COMMENT ON COLUMN notas_debito.codigo_sifen IS
    'CDC devuelto por SIFEN. Vacío hasta conectar la facturación electrónica con la SET.';
COMMENT ON COLUMN tipos_comprobantes.codigo_sifen IS
    'Código del tipo de documento electrónico en SIFEN. Se completa al conectar la facturación electrónica.';
COMMENT ON COLUMN empresa.certificado_firma_digital_path IS
    'Ruta del certificado de firma digital para SIFEN. Se carga al habilitar la facturación electrónica.';
COMMENT ON COLUMN empresa.certificado_firma_digital_password_encrypted IS
    'Contraseña cifrada del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';
COMMENT ON COLUMN empresa.certificado_firma_digital_serial IS
    'Número de serie del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';
COMMENT ON COLUMN empresa.certificado_firma_digital_fecha_vencimiento IS
    'Vencimiento del certificado de firma digital (SIFEN). Se carga al habilitar la facturación electrónica.';
COMMENT ON COLUMN empresa.codigo_seguridad_contribuyente IS
    'Código de seguridad del contribuyente (CSC) que entrega la SET para SIFEN.';
COMMENT ON COLUMN empresa.fecha_habilitacion_sifen IS
    'Fecha en que la SET habilita a la empresa como emisora electrónica.';
COMMENT ON COLUMN empresa.grupo_obligatoriedad IS
    'Grupo de obligatoriedad de facturación electrónica asignado por la SET.';

-- 3b. Flujos opcionales que la carga actual todavía no usó
COMMENT ON COLUMN facturas.id_pedido IS
    'Pedido de origen, si la factura se emitió desde un pedido (opcional en el formulario).';
COMMENT ON COLUMN remisiones.id_pedido IS
    'Pedido asociado a la remisión (opcional en el formulario).';
COMMENT ON COLUMN remisiones.id_factura IS
    'Factura asociada a la remisión (opcional en el formulario).';
COMMENT ON COLUMN pedidos.id_profesional IS
    'Especialista que solicita el pedido (opcional en el formulario).';
COMMENT ON COLUMN presupuestos.id_profesional IS
    'Especialista que solicita el presupuesto (opcional en el formulario).';
COMMENT ON COLUMN orden_detalle.detalle_resultado IS
    'Resultado del estudio o análisis. Reservado: la carga de resultados todavía no tiene pantalla.';
COMMENT ON COLUMN orden_detalle.detalle_fecha_realizacion IS
    'Fecha en que se realizó el estudio o análisis. Reservado: la carga de resultados todavía no tiene pantalla.';

-- 3c. Sin uso actual
COMMENT ON COLUMN accesos_sistema.csrf_valido IS
    'Resultado de la validación CSRF del intento. Parámetro de registrar_intento_login; hoy la app no lo informa (queda NULL).';

COMMIT;

-- Vuelta atrás (solo si hiciera falta):
--   ALTER TABLE citas ADD COLUMN id_agenda_horario integer,
--       ADD CONSTRAINT citas_id_agenda_horario_fkey FOREIGN KEY (id_agenda_horario)
--           REFERENCES agenda_horarios(id_agenda_horario) ON UPDATE CASCADE ON DELETE RESTRICT;
--   ALTER TABLE remisiones DROP CONSTRAINT remisiones_usuario_creacion_fkey,
--       DROP CONSTRAINT remisiones_usuario_modificacion_fkey,
--       ALTER COLUMN usuario_creacion TYPE character varying USING usuario_creacion::text,
--       ALTER COLUMN usuario_modificacion TYPE character varying USING usuario_modificacion::text;
