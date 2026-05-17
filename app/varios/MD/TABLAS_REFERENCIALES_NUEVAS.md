# TABLAS REFERENCIALES PARA LOS NUEVOS MÓDULOS

## Resumen de Tablas Referenciales Necesarias

### ✅ Tablas Referenciales que YA EXISTEN (con módulos completos):
1. **tipos_procedimientos** - Para Presupuestos
   - DAO: `app/dao/referenciales/tipo_procedimiento/ProcedimientoDao.py`
   - API: `app/rutas/referenciales/tipo_procedimiento/procedimiento_api.py`
   - Routes: `app/rutas/referenciales/tipo_procedimiento/procedimiento_routes.py`
   - Template: `app/rutas/referenciales/tipo_procedimiento/templates/procedimiento-index.html`

2. **tipos_estudios** - Para Órdenes de Estudios
   - DAO: `app/dao/referenciales/tipo_estudio/EstudioDao.py`
   - API: `app/rutas/referenciales/tipo_estudio/estudio_api.py`
   - Routes: `app/rutas/referenciales/tipo_estudio/estudio_routes.py`
   - Template: `app/rutas/referenciales/tipo_estudio/templates/estudio-index.html`

3. **tipos_analisis** - Para Órdenes de Estudios (opcional)
   - DAO: `app/dao/referenciales/tipo_analisis/AnalisisDao.py`
   - API: `app/rutas/referenciales/tipo_analisis/analisis_api.py`
   - Routes: `app/rutas/referenciales/tipo_analisis/analisis_routes.py`
   - Template: `app/rutas/referenciales/tipo_analisis/templates/analisis-index.html`

4. **medicamentos** - Para Recetas
   - DAO: `app/dao/referenciales/medicamento/MedicamentoDao.py`
   - API: `app/rutas/referenciales/medicamento/medicamento_api.py`
   - Routes: `app/rutas/referenciales/medicamento/medicamento_routes.py`
   - Template: `app/rutas/referenciales/medicamento/templates/medicamento-index.html`

### ⚠️ Tablas Referenciales que FALTAN CREAR:

1. **tipos_certificados_medicos** - Para Certificados Médicos
   - ❌ NO EXISTE módulo referencial completo
   - ✅ Tabla SQL creada en `estructura_bd_y_tablas_faltantes.sql`
   - ⚠️ El módulo de Certificados Médicos usa valores hardcodeados (REPOSO, APTITUD, etc.)
   - **ACCIÓN REQUERIDA**: Crear módulo referencial completo (DAO, API, Routes, Template)

### 📋 Tablas que NO son Referenciales (son módulos de gestión):

- **insumos** - Es un módulo de gestión completo, no una referencial
  - Tiene su propio módulo: `app/rutas/modulos/insumo/registrarinsumo/`
  - Se gestiona directamente desde el módulo de Insumos

## IMPORTANTE - Uso de Referenciales

### ✅ CORRECTO (Dinámico):
```javascript
// Cargar tipos desde la API
fetch('/api/v1/tipos_certificados_medicos')
  .then(resp => resp.json())
  .then(data => {
    // Llenar select dinámicamente
    data.data.forEach(tipo => {
      $('#txtTipo').append(`<option value="${tipo.id}">${tipo.descripcion}</option>`);
    });
  });
```

### ❌ INCORRECTO (Hardcodeado):
```html
<select id="txtTipo">
  <option value="REPOSO">Reposo</option>
  <option value="APTITUD">Aptitud</option>
  <!-- Valores fijos -->
</select>
```

## Acciones Pendientes

1. ✅ Crear tabla `tipos_certificados_medicos` en SQL (YA HECHO)
2. ⚠️ Crear módulo referencial completo para `tipos_certificados_medicos`
3. ⚠️ Actualizar módulo de Certificados Médicos para usar la referencial dinámicamente
4. ⚠️ Actualizar archivo SQL de INSERTs para que solo tenga ejemplos (no obligatorios)
5. ✅ Verificar que Presupuestos, Recetas y Órdenes usen referenciales dinámicamente

## Nota sobre el archivo SQL de INSERTs

El archivo `inserts_tablas_nuevas.sql` contiene **SOLO EJEMPLOS** de datos iniciales.
- Los INSERTs de tablas referenciales son opcionales (ejemplos)
- Los INSERTs de módulos principales están comentados (requieren IDs específicos)
- **NO son datos obligatorios** - el administrador puede agregar/eliminar desde las interfaces referenciales









