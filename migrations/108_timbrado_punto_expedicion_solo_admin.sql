-- 108_timbrado_punto_expedicion_solo_admin.sql
-- Timbrados y Puntos de Expedición son configuración fiscal: sus rutas solo admiten
-- ADMINISTRADOR y SUPERADMIN, pero el menú (roles_paginas) también se los mostraba a VENTAS,
-- que al entrar recibía un 403. Se ocultan del menú de VENTAS (visible = false, no se borra
-- la fila: se puede volver a habilitar desde Seguridad → Menú).
--
-- Detectado al generar las capturas de la Guía de uso (2026-10-13).
-- Antes de aplicarla se hizo un backup: sysclin_bd_20261013_182021.dump.gpg
--   Get-Content migrations\108_timbrado_punto_expedicion_solo_admin.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

UPDATE roles_paginas rp
   SET visible = false
  FROM roles r, paginas p
 WHERE r.id_rol = rp.id_rol
   AND p.id_pagina = rp.id_pagina
   AND r.cod_rol = 'VENTAS'
   AND p.pag_direccion IN ('timbrado.timbradoIndex', 'punto_expedicion.puntoExpedicionIndex');
