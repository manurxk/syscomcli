# Análisis de Estructura de Fases SQL

## Resumen de Inserts por Fase

### ✅ Fases CON inserts (datos incluidos):
- **FASE 1**: Géneros, Estados Civiles, Ciudades (263 ciudades), Niveles Instrucción, Profesiones, Especialidades
- **FASE 2**: Grupos (incluye Superadministrador), Módulos, Cargos
- **FASE 4**: Días de la Semana, Estados de Citas
- **FASE 10**: Monedas, Formas de Cobro, Marcas de Tarjeta, Tipos de Items, Tipos de Impuestos, Condiciones de Venta, Tipos de Comprobantes, Estados de Factura

### ⚠️ Fases SIN inserts (solo estructura):
- **FASE 3**: Solo estructura (Pacientes, Pacientes Menores)
- **FASE 5**: Solo estructura (Consultorio: Síntomas, Signos, Diagnósticos, Tipos de Análisis, Tipos de Estudios, Medicamentos, Tipos de Procedimientos, Tipos de Tratamientos, Consultas, etc.)
- **FASE 6**: Solo estructura (Referenciales Ventas: Formas de Cobro, Marcas de Tarjeta, Entidades, Depósitos, Cajas, etc.)
- **FASE 7**: Solo estructura (Principales Ventas: Facturas, Pedidos, Cobranzas, etc.)
- **FASE 8**: Solo estructura (Presupuestos, Recetas, Órdenes de Estudios, Certificados, Insumos, Informes)
- **FASE 9**: Solo triggers y funciones
- **FASE 11**: Solo migraciones
- **FASE 14**: Solo estructura (Empresa, Sede, Timbrados, Establecimientos, Puntos de Expedición)

## Problemas Detectados

### 1. **FASE 5 - Consultorio: Falta datos iniciales**
La FASE 5 crea las tablas referenciales pero NO inserta datos:
- `sintomas` - vacía
- `signos` - vacía
- `diagnosticos` - vacía
- `tipos_analisis` - vacía
- `tipos_estudios` - vacía (pero hay inserts en `inserts_tablas_nuevas.sql`)
- `medicamentos` - vacía (pero hay inserts en `inserts_tablas_nuevas.sql`)
- `tipos_procedimientos` - vacía (pero hay inserts en `inserts_tablas_nuevas.sql`)
- `tipos_tratamientos` - vacía

### 2. **FASE 6 - Referenciales Ventas: Falta datos iniciales**
La FASE 6 crea las tablas pero NO inserta datos (los datos están en FASE 10):
- `formas_cobro` - datos en FASE 10
- `marcas_tarjeta` - datos en FASE 10
- `entidades_adheridas` - vacía
- `entidades_emisoras` - vacía
- `depositos` - vacía
- `cajas` - vacía
- `tipos_items` - datos en FASE 10
- `tipos_impuestos` - datos en FASE 10
- `condiciones_venta` - datos en FASE 10
- `tipos_comprobantes` - datos en FASE 10
- `estados_factura` - datos en FASE 10
- `monedas` - datos en FASE 10

### 3. **FASE 8 - Tablas Nuevas: Falta datos iniciales**
La FASE 8 crea las tablas pero NO inserta datos (los datos están en `inserts_tablas_nuevas.sql`):
- `tipos_certificados_medicos` - vacía (pero hay inserts en `inserts_tablas_nuevas.sql`)
- `presupuestos` - vacía
- `ordenes_estudios` - vacía
- `recetas` - vacía
- `certificados_medicos` - vacía
- `insumos` - vacía (pero hay inserts en `inserts_datos_iniciales.sql` y `inserts_tablas_nuevas.sql`)

### 4. **Duplicación de Inserts**
- Los inserts están dispersos entre las fases individuales y archivos separados (`inserts_tablas_nuevas.sql`, `inserts_datos_iniciales.sql`)
- La FASE 15 duplica todos estos inserts

## Recomendaciones

### Opción A: Mantener estructura actual (recomendada)
- Las fases individuales tienen sus datos mínimos necesarios
- La FASE 15 es un resumen consolidado OPCIONAL
- Usar `ON CONFLICT DO NOTHING` para evitar duplicados
- **Ventaja**: Cada fase es autocontenida y puede ejecutarse independientemente

### Opción B: Consolidar todos los inserts en FASE 15
- Remover inserts de las fases individuales (solo dejar estructura)
- Poner TODOS los inserts en FASE 15
- **Ventaja**: Separación clara entre estructura y datos
- **Desventaja**: Las fases individuales no son autocontenidas

### Opción C: Completar cada fase con sus datos
- Agregar inserts faltantes a FASE 5, 6, 8
- Mantener FASE 15 como resumen consolidado
- **Ventaja**: Cada fase es completamente autocontenida
- **Desventaja**: Más duplicación

## Verificación de Dependencias

### ✅ Dependencias correctas:
- FASE 1 → FASE 2 (personas necesita generos, ciudades, etc.)
- FASE 2 → FASE 3 (pacientes necesita personas)
- FASE 2 → FASE 4 (especialistas necesita funcionarios)
- FASE 4 → FASE 5 (consultas necesita especialistas)
- FASE 5 → FASE 6 (no hay dependencia directa)
- FASE 6 → FASE 7 (ventas necesita referenciales)
- FASE 7 → FASE 8 (no hay dependencia directa)
- FASE 1-8 → FASE 9 (triggers necesitan todas las tablas)
- FASE 1-10 → FASE 11 (migraciones necesitan tablas existentes)
- FASE 7 → FASE 14 (facturas necesita empresa, timbrado, etc.)

### ⚠️ Posibles problemas:
1. **FASE 5** crea tablas referenciales vacías que pueden causar errores si se intentan usar
2. **FASE 6** crea tablas que dependen de datos de FASE 10 (separación lógica pero puede confundir)
3. **FASE 8** crea tablas sin datos iniciales (depende de `inserts_tablas_nuevas.sql`)

## Conclusión

**La estructura está bien organizada PERO:**
1. Algunas fases (5, 6, 8) crean tablas sin datos iniciales
2. Los datos están dispersos entre fases y archivos separados
3. La FASE 15 duplica inserts pero es útil como resumen consolidado

**Recomendación final:**
- Mantener la estructura actual (fases con sus datos mínimos)
- Completar FASE 15 con TODOS los inserts (incluyendo los que faltan en fases 5, 6, 8)
- Documentar claramente que FASE 15 es OPCIONAL si ya ejecutaste las fases individuales
- Usar `ON CONFLICT DO NOTHING` en todos los inserts para evitar duplicados

