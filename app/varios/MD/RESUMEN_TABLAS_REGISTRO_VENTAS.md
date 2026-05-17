# 📋 Resumen de Tablas de Registro - Módulo de Ventas

## ✅ Todas las tablas son para REGISTRAR operaciones

### 1. **Registrar Apertura y Cierre de Caja**
- **Tabla:** `aperturas_cierre_caja`
- **Propósito:** Registrar cuando se abre y cierra una caja
- **Campos principales:** tipo_operacion (APERTURA/CIERRE), saldos, montos por forma de pago

### 2. **Registrar Arqueo de Caja**
- **Tabla:** `arqueos_caja`
- **Propósito:** Registrar el conteo físico de dinero en caja
- **Campos principales:** monto_esperado, monto_real, diferencia

### 3. **Registrar Recaudaciones a Depositar**
- **Tabla:** `recaudaciones`
- **Propósito:** Registrar recaudaciones que se van a depositar en banco
- **Campos principales:** monto_total, fecha_deposito, montos por forma de pago

### 4. **Registrar Pedido del Cliente**
- **Tablas:** `pedidos` + `pedido_detalle`
- **Propósito:** Registrar pedidos de pacientes/clientes
- **Campos principales:** paciente, fecha, items, totales

### 5. **Registrar Facturación**
- **Tablas:** `facturas` + `factura_detalle`
- **Propósito:** Registrar facturas emitidas (facturación electrónica)
- **Campos principales:** número factura, paciente, items, totales, código SIFEN

### 6. **Registrar Cuentas a Cobrar**
- **Tabla:** `cuentas_cobrar`
- **Propósito:** Registrar cuentas por cobrar generadas de facturas
- **Campos principales:** factura, paciente, monto, fechas de vencimiento

### 7. **Registrar Cobranzas**
- **Tablas:** `cobranzas` + `cobranza_detalle`
- **Propósito:** Registrar cobranzas realizadas
- **Campos principales:** cuenta a cobrar, forma de pago, monto cobrado

### 8. **Registrar Notas de Crédito**
- **Tablas:** `notas_credito` + `nota_credito_detalle`
- **Propósito:** Registrar notas de crédito emitidas
- **Campos principales:** factura origen, motivo, monto, código SIFEN

### 9. **Registrar Notas de Débito**
- **Tablas:** `notas_debito` + `nota_debito_detalle`
- **Propósito:** Registrar notas de débito emitidas
- **Campos principales:** factura origen, motivo, monto, código SIFEN

### 10. **Registrar Libro de Ventas**
- **Tabla:** `libro_ventas`
- **Propósito:** Registro contable automático de todas las ventas
- **Campos principales:** fecha, tipo comprobante, montos gravados/exentos/IVA

---

## 📊 Estructura de Cada Tabla de Registro

Todas las tablas siguen este patrón:

```sql
CREATE TABLE nombre_tabla (
    id_ SERIAL PRIMARY KEY,              -- ID único
    numero VARCHAR(50) UNIQUE,          -- Número único del registro
    id_referencial INTEGER,              -- FK a referenciales
    fecha_registro TIMESTAMP,            -- Fecha de registro
    montos INTEGER,                      -- Valores monetarios
    observaciones TEXT,                  -- Notas adicionales
    est_ CHAR(1) DEFAULT 'A',           -- Estado simple
    fecha_creacion TIMESTAMP,            -- Auditoría
    usuario_creacion VARCHAR(50),        -- Auditoría
    ...
);
```

---

## ✅ Características de las Tablas de Registro

1. **Simples y directas:** Solo campos necesarios para registrar la operación
2. **Sin gestión compleja:** No tienen campos de workflow avanzado
3. **Enfocadas en registro:** Cada tabla registra UNA operación específica
4. **Auditoría básica:** Solo fecha_creacion y usuario_creacion
5. **Estados simples:** Solo estados básicos (A=Activo, I=Inactivo, etc.)

---

## 🎯 Próximos Pasos

1. ✅ SQL de tablas creado (`crear_tablas_principales_ventas.sql`)
2. ⏳ Implementar DAO + API + Routes + Template para cada módulo
3. ⏳ Cada módulo será una página de "Registrar [Operación]"









