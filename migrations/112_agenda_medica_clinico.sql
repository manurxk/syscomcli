-- 112_agenda_medica_clinico.sql
-- Agenda Médica (agenda_horarios.agendaHorariosIndex) pasa a mostrarse también al rol CLINICO.
-- El especialista solo ve SU agenda y sus cupos, en solo lectura: la API resuelve el
-- id_especialista desde la sesión y no le permite crear, editar ni activar/desactivar horarios
-- (eso sigue siendo de ADMINISTRADOR, SUPERADMIN y RECEPCION).
--
-- Pedido del usuario 2026-10-13.
--   Get-Content migrations\112_agenda_medica_clinico.sql -Raw | docker exec -i syscomcli_bd psql -U postgres -d sysclin_bd -v ON_ERROR_STOP=1

INSERT INTO roles_paginas (id_rol, id_pagina, visible)
SELECT r.id_rol, p.id_pagina, true
  FROM roles r, paginas p
 WHERE r.cod_rol = 'CLINICO'
   AND p.pag_direccion = 'agenda_horarios.agendaHorariosIndex'
ON CONFLICT (id_rol, id_pagina) DO UPDATE SET visible = true;
