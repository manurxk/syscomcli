# 📋 Soporte para Especialistas Externos en Derivaciones

## ✅ Implementación Completada

Se ha agregado soporte para derivar pacientes a especialistas externos (profesionales que no están registrados en el sistema).

---

## 🎯 Características

### Especialistas Externos
- ✅ Campos para nombre, apellido, teléfono y matrícula
- ✅ Opción en formulario para elegir entre interno/externo
- ✅ Validaciones apropiadas según el tipo
- ✅ Visualización diferenciada en listas y detalles

### Especialistas Internos
- ✅ Mantiene funcionalidad existente
- ✅ Lista de especialistas del sistema
- ✅ Notificaciones automáticas

---

## 📊 Cambios en Base de Datos

### Script SQL: `FASE_2_ESPECIALISTAS_EXTERNOS.sql`

1. **Modificaciones a tabla `derivaciones`:**
   - `id_especialista_destino` ahora es NULLABLE
   - Nuevo campo `es_externo` (BOOLEAN)
   - Nuevos campos para datos externos:
     - `especialista_externo_nombre`
     - `especialista_externo_apellido`
     - `especialista_externo_telefono`
     - `especialista_externo_matricula`
   - Constraint: Debe tener especialista interno O datos de externo

2. **Función `crear_derivacion()` actualizada:**
   - Soporta parámetros para especialistas externos
   - Valida que si es externo, tenga nombre mínimo
   - No crea notificaciones para externos (no tienen usuario)

3. **Vista `v_derivaciones_pendientes` actualizada:**
   - Muestra nombre completo de externos
   - Maneja NULLs correctamente

---

## 🔧 Cambios en Backend

### DerivacionDao.py
- `crearDerivacion()` ahora acepta parámetros para externos
- `getDerivaciones()` muestra datos de externos
- `getDerivacionById()` incluye información de externos
- Todas las consultas SQL actualizadas con LEFT JOINs

### derivacion_api.py
- Validación mejorada en `crearDerivacion()`
- Soporta ambos tipos de derivación
- Validaciones específicas según tipo

---

## 🎨 Cambios en Frontend

### Template HTML
- **Radio buttons** para elegir tipo (Interno/Externo)
- **Campos dinámicos** que aparecen según selección
- **Validación** según tipo elegido
- **Visualización** con badges para identificar externos
- **Información adicional** (teléfono, matrícula) en detalles

### Funcionalidades JavaScript
- Toggle entre formularios interno/externo
- Validación condicional
- Envío de datos según tipo
- Visualización diferenciada en tablas

---

## 📝 Cómo Usar

### Derivar a Especialista Interno:
1. Seleccionar "Especialista Interno"
2. Elegir especialista del dropdown
3. Completar motivo y urgencia
4. Enviar derivación
5. **Sistema crea notificación automática**

### Derivar a Especialista Externo:
1. Seleccionar "Especialista Externo"
2. Completar nombre (obligatorio)
3. Completar apellido, teléfono, matrícula (opcionales)
4. Completar motivo y urgencia
5. Enviar derivación
6. **No se crea notificación** (no hay usuario en sistema)

---

## 🔍 Visualización

### En Listas:
- **Interno**: Nombre del especialista
- **Externo**: Nombre + Badge "Externo" + Teléfono (si existe)

### En Detalles:
- **Interno**: Nombre completo del especialista
- **Externo**: 
  - Nombre completo
  - Teléfono (si existe)
  - Matrícula (si existe)
  - Badge "Especialista Externo"

---

## ⚠️ Notas Importantes

1. **Derivaciones externas NO pueden ser aceptadas/rechazadas** desde el sistema
   - Solo se registran para historial
   - El especialista externo no tiene acceso al sistema

2. **Las derivaciones externas siempre quedan en estado "PENDIENTE"**
   - No hay flujo de aceptación/rechazo
   - Se pueden cancelar por el origen

3. **Validaciones:**
   - Interno: Requiere seleccionar especialista
   - Externo: Requiere al menos nombre

---

## 🚀 Próximos Pasos (Opcional)

1. **Historial de Externos:**
   - Lista de especialistas externos más utilizados
   - Estadísticas de derivaciones externas

2. **Integración con Contactos:**
   - Guardar especialistas externos frecuentes
   - Autocompletar desde lista de contactos

3. **Exportación:**
   - Generar reporte de derivaciones externas
   - Enviar por email al especialista externo

---

## ✅ Verificación

Para verificar:

1. **Ejecutar SQL:**
   ```sql
   -- Ejecutar: app/codigos_sql/FASE_2_ESPECIALISTAS_EXTERNOS.sql
   ```

2. **Probar flujo:**
   - Crear derivación interna (debe funcionar como antes)
   - Crear derivación externa (debe guardar datos externos)
   - Verificar visualización en listas
   - Verificar detalles de derivación externa

---

**¡Soporte para Especialistas Externos Implementado!** 🎉


