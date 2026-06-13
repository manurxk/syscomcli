import os
import sys

# Añadir el directorio raíz del proyecto al path para poder importar módulos de la app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.conexion.Conexion import Conexion

def aplicar_migracion():
    print("Iniciando migración de base de datos para Planes de Tratamiento...")
    
    # Ruta al archivo SQL
    sql_file_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'migrations', '2026_03_10_crear_tablas_tratamiento.sql')
    
    if not os.path.exists(sql_file_path):
        print(f"Error: No se encontró el archivo SQL en {sql_file_path}")
        return False
        
    print(f"Leyendo archivo SQL: {sql_file_path}")
    with open(sql_file_path, 'r', encoding='utf-8') as f:
        sql_content = f.read()
        
    conexion = Conexion()
    con = conexion.getConexion()
    
    if not con:
        print("Error: No se pudo conectar a la base de datos.")
        return False
        
    cur = con.cursor()
    
    try:
        print("Ejecutando sentencias SQL...")
        cur.execute(sql_content)
        con.commit()
        print("Migración aplicada con éxito. Tablas creadas: feriados, frecuencias_agendamiento, citas_log_estados.")
        return True
    except Exception as e:
        con.rollback()
        print(f"Error al ejecutar la migración: {str(e)}")
        return False
    finally:
        cur.close()
        con.close()

if __name__ == "__main__":
    exito = aplicar_migracion()
    sys.exit(0 if exito else 1)
