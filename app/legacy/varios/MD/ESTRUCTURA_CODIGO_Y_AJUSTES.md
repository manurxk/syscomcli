# 📋 Estructura de Código del Sistema CIN - Guía de Referencia

## 🏗️ Estructura de Archivos por Módulo

Cada módulo sigue esta estructura estándar:

```
app/
├── dao/                          # Capa de acceso a datos
│   ├── referenciales/            # Tablas referenciales simples
│   │   └── ciudad/
│   │       └── CiudadDao.py      # DAO con métodos CRUD
│   └── modulos/                  # Módulos de negocio
│       └── consulta/
│           └── ReConsultaDao.py  # DAO con lógica de negocio
│
└── rutas/                        # Capa de presentación
    ├── referenciales/            # Rutas de referenciales
    │   └── ciudad/
    │       ├── __init__.py
    │       ├── ciudad_api.py     # Endpoints API (JSON)
    │       ├── ciudad_routes.py  # Rutas de vistas (HTML)
    │       └── templates/
    │           └── ciudad-index.html
    └── modulos/                  # Rutas de módulos
        └── consulta/
            └── registrarconsulta/
                ├── __init__.py
                ├── registrarconsulta_api.py
                ├── registrarconsulta_routes.py
                └── templates/
                    └── registrarconsulta-index.html
```

---

## 📝 Ejemplo Completo: Módulo Ciudad (Referencial)

### 1. **DAO** (`app/dao/referenciales/ciudad/CiudadDao.py`)

```python
# Data access object - DAO
import re
from flask import current_app as app
from app.conexion.Conexion import Conexion

class CiudadDao:
    
    def getCiudades(self):
        sql = """
        SELECT id_ciudad, des_ciudad, est_ciudad
        FROM ciudades
        """
        conexion = Conexion()
        con = conexion.getConexion()
        cur = con.cursor()
        try:
            cur.execute(sql)
            ciudades = cur.fetchall()
            return [{'id': c[0], 'descripcion': c[1], 'estado': c[2]} for c in ciudades]
        except Exception as e:
            app.logger.error(f"Error al obtener todas las ciudades: {str(e)}")
            return []
        finally:
            cur.close()
            con.close()
    
    def getCiudadById(self, id_ciudad):
        # ... código ...
    
    def guardarCiudad(self, descripcion, estado=True):
        # Validaciones
        # INSERT con RETURNING id_ciudad
    
    def updateCiudad(self, id_ciudad, descripcion, estado=True):
        # UPDATE
    
    def deleteCiudad(self, id_ciudad):
        # DELETE
```

**Características:**
- ✅ Usa `Conexion()` para obtener conexión
- ✅ Manejo de errores con try/except/finally
- ✅ Cierra cursor y conexión en finally
- ✅ Retorna diccionarios/listas para fácil serialización JSON
- ✅ Logging de errores con `app.logger`

---

### 2. **API** (`app/rutas/referenciales/ciudad/ciudad_api.py`)

```python
from flask import Blueprint, request, jsonify, current_app as app
from app.dao.referenciales.ciudad.CiudadDao import CiudadDao

ciuapi = Blueprint('ciuapi', __name__)

@ciuapi.route('/ciudades', methods=['GET'])
def getCiudades():
    ciudao = CiudadDao()
    try:
        ciudades = ciudao.getCiudades()
        return jsonify({
            'success': True,
            'data': ciudades,
            'error': None
        }), 200
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Ocurrió un error interno.'
        }), 500

@ciuapi.route('/ciudades', methods=['POST'])
def addCiudad():
    data = request.get_json()
    ciudao = CiudadDao()
    
    # Validar campos requeridos
    campos_requeridos = ['descripcion', 'estado']
    for campo in campos_requeridos:
        if campo not in data:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        ciudad_id = ciudao.guardarCiudad(data['descripcion'], data['estado'])
        if ciudad_id:
            return jsonify({
                'success': True,
                'data': {'id': ciudad_id, ...},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar.'
            }), 400
    except Exception as e:
        # Manejo de errores
```

**Características:**
- ✅ Blueprint con nombre descriptivo (`ciuapi`)
- ✅ Endpoints RESTful (GET, POST, PUT, DELETE)
- ✅ Validación de campos requeridos
- ✅ Respuestas JSON consistentes: `{success, data, error}`
- ✅ Códigos HTTP apropiados (200, 201, 400, 404, 500)

---

### 3. **Routes** (`app/rutas/referenciales/ciudad/ciudad_routes.py`)

```python
from flask import Blueprint, render_template

ciumod = Blueprint('ciudad', __name__, template_folder='templates')

@ciumod.route('/ciudad-index')
def ciudadIndex():
    return render_template('ciudad-index.html')
```

**Características:**
- ✅ Blueprint separado para vistas HTML
- ✅ Nombre del módulo como prefijo de función (`ciudadIndex`)
- ✅ `template_folder='templates'` para organizar HTML

---

### 4. **Registro en `app/__init__.py`**

```python
# Referenciales
from app.rutas.referenciales.ciudad.ciudad_routes import ciumod
from app.rutas.referenciales.ciudad.ciudad_api import ciuapi
app.register_blueprint(ciumod, url_prefix='/ciudad')
app.register_blueprint(ciuapi, url_prefix=API_V1)  # API_V1 = '/api/v1'
```

---

## 📝 Ejemplo Completo: Módulo Consulta (Negocio)

### 1. **DAO** (`app/dao/modulos/consulta/ReConsultaDao.py`)

```python
from flask import current_app as app
from app.conexion.Conexion import Conexion
from datetime import datetime, date

class ConsultaDao:
    
    def getConsultas(self):
        """Obtiene todas las consultas con sus datos completos"""
        consultaSQL = """
            SELECT
                c.id_consulta,
                c.id_cita,
                c.id_paciente,
                -- ... más campos ...
                CONCAT(pp.per_nombre, ' ', pp.per_apellido) AS paciente_nombre
            FROM consultas c
            JOIN pacientes p ON c.id_paciente = p.id_paciente
            JOIN personas pp ON p.id_persona = pp.id_persona
            WHERE c.est_consulta = 'A'
            ORDER BY c.consulta_fecha DESC
        """
        # ... ejecución y retorno ...
    
    def guardarConsulta(self, id_paciente, id_profesional, consulta_fecha, ...):
        insertConsultaSQL = """
            INSERT INTO consultas(...)
            VALUES(%s, %s, %s, ...)
            RETURNING id_consulta
        """
        # ... ejecución ...
```

**Características:**
- ✅ JOINs para obtener datos relacionados
- ✅ Formateo de fechas en Python (`strftime`)
- ✅ Validaciones antes de INSERT/UPDATE
- ✅ RETURNING para obtener ID generado

---

### 2. **API** (`app/rutas/modulos/consulta/registrarconsulta/registrarconsulta_api.py`)

```python
from flask import Blueprint, request, jsonify, current_app as app
from app.dao.modulos.consulta.ReConsultaDao import ConsultaDao

consultaapi = Blueprint('consultaapi', __name__)

@consultaapi.route('/consultas', methods=['POST'])
def addConsulta():
    data = request.get_json()
    dao = ConsultaDao()
    
    campos_requeridos = ['id_paciente', 'id_profesional', 'consulta_fecha', 'consulta_motivo']
    for campo in campos_requeridos:
        if campo not in data or not data[campo]:
            return jsonify({
                'success': False,
                'error': f'El campo {campo} es obligatorio.'
            }), 400
    
    try:
        consulta_id = dao.guardarConsulta(
            id_paciente=data['id_paciente'],
            id_profesional=data['id_profesional'],
            consulta_fecha=data['consulta_fecha'],
            consulta_motivo=data['consulta_motivo'],
            consulta_estado=data.get('consulta_estado', 'PENDIENTE'),
            usuario_creacion=data.get('usuario_creacion', 'ADMIN')
        )
        
        if consulta_id:
            return jsonify({
                'success': True,
                'data': {'id_consulta': consulta_id, 'mensaje': 'Consulta creada exitosamente'},
                'error': None
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'No se pudo guardar la consulta.'
            }), 500
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({'success': False, 'error': f'Ocurrió un error interno: {str(e)}'}), 500
```

---

## 🔧 Ajustes para Guaraníes Paraguayos (PYG)

### Cambios en Tipos de Datos SQL

**ANTES (con decimales):**
```sql
presupuesto_subtotal DECIMAL(10,2) DEFAULT 0.00,
precio_unitario DECIMAL(10,2) NOT NULL
```

**DESPUÉS (guaraníes sin decimales):**
```sql
presupuesto_subtotal INTEGER DEFAULT 0,
precio_unitario INTEGER NOT NULL
```

**Razón:** El guaraní paraguayo (PYG) no tiene decimales. Todos los montos son números enteros.

---

## 📋 Checklist para Crear un Nuevo Módulo

### Para Referenciales (ej: ciudades, medicamentos):
- [ ] Crear `app/dao/referenciales/[nombre]/[Nombre]Dao.py`
- [ ] Crear `app/rutas/referenciales/[nombre]/[nombre]_api.py`
- [ ] Crear `app/rutas/referenciales/[nombre]/[nombre]_routes.py`
- [ ] Crear `app/rutas/referenciales/[nombre]/templates/[nombre]-index.html`
- [ ] Registrar blueprints en `app/__init__.py`

### Para Módulos de Negocio (ej: presupuestos, recetas):
- [ ] Crear `app/dao/modulos/[modulo]/[Modulo]Dao.py`
- [ ] Crear `app/rutas/modulos/[modulo]/[submodulo]/[submodulo]_api.py`
- [ ] Crear `app/rutas/modulos/[modulo]/[submodulo]/[submodulo]_routes.py`
- [ ] Crear `app/rutas/modulos/[modulo]/[submodulo]/templates/[submodulo]-index.html`
- [ ] Registrar blueprints en `app/__init__.py`

---

## 🎯 Convenciones de Nombres

### Archivos Python:
- **DAO**: `[Nombre]Dao.py` (ej: `PresupuestoDao.py`, `RecetaDao.py`)
- **API**: `[nombre]_api.py` (ej: `presupuesto_api.py`, `receta_api.py`)
- **Routes**: `[nombre]_routes.py` (ej: `presupuesto_routes.py`)

### Clases:
- **DAO**: `[Nombre]Dao` (ej: `PresupuestoDao`, `RecetaDao`)
- **Blueprint API**: `[nombre]api` (ej: `presupuestoapi`, `recetaapi`)
- **Blueprint Routes**: `[nombre]mod` (ej: `presupuestomod`, `recetamod`)

### Funciones:
- **DAO**: `get[Nombre]s()`, `get[Nombre]ById()`, `guardar[Nombre]()`, `update[Nombre]()`, `delete[Nombre]()`
- **API**: `get[Nombre]s()`, `get[Nombre]()`, `add[Nombre]()`, `update[Nombre]()`, `delete[Nombre]()`
- **Routes**: `[nombre]Index()` (ej: `presupuestoIndex()`)

---

## 📚 Próximos Pasos

1. ✅ Ajustar scripts SQL para usar INTEGER en lugar de DECIMAL
2. ⏳ Crear estructura de archivos para nuevos módulos siguiendo este patrón
3. ⏳ Implementar DAOs, APIs y Routes para cada módulo faltante









