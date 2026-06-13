import os
import sys
import datetime
import re
from pathlib import Path

# Agregar el directorio raíz al path para importar app
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from dotenv import load_dotenv
import psycopg2
import psycopg2.extras

load_dotenv(os.path.join(BASE_DIR, '.env'))

# Configuración
MULTA_POR_DEFECTO = 50000.0  # Guaraníes o moneda local
MULTA_PORCENTAJE_TRATAMIENTO = 1.0  # 100% como se indicó en el reporte

def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv('DB_NAME', 'clausys'),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASS', 'postgres'),
        host=os.getenv('DB_HOST', 'localhost'),
        port=os.getenv('DB_PORT', '5432')
    )

def procesar_multas():
    """Ejecuta el proceso diario de revisión de citas perdidas"""
    print(f"[{datetime.datetime.now()}] Iniciando procesamiento de ausencias...")
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        
        # 1. Buscar citas de fechas anteriores a hoy que siguen 'AGENDADA' o 'CONFIRMADA' (1, 2)
        # O de hoy, pero cuya hora de fin ya pasó hace 2+ horas. (Simplificado: solo días anteriores)
        cur.execute("""
            SELECT id_cita, id_paciente, cita_fecha, cita_motivo
            FROM citas
            WHERE cita_fecha < CURRENT_DATE
              AND id_estado_cita IN (1, 2) -- AGENDADA o CONFIRMADA
              AND cita_activo = TRUE
        """)
        
        citas_perdidas = cur.fetchall()
        print(f"[{datetime.datetime.now()}] Citas ausentes detectadas: {len(citas_perdidas)}")
        
        if not citas_perdidas:
            return
            
        # 2. Iterar sobre citas, generar multas y cambiar estado
        multas_generadas = 0
        for cita in citas_perdidas:
            id_cita = cita['id_cita']
            id_paciente = cita['id_paciente']
            motivo = cita['cita_motivo'] or ""
            fecha = cita['cita_fecha']
            
            # Buscar si existe la tabla paciente_multas
            
            monto_calculado = MULTA_POR_DEFECTO
            
            # Intentar ver si pertenece a un presupuesto para calcular la multa exacta
            match = re.search(r'Presupuesto #(\d+)', motivo, re.IGNORECASE)
            id_presupuesto = match.group(1) if match else None
            
            if id_presupuesto:
                try:
                    cur.execute("""
                        SELECT presupuesto_total, cantidad_sesiones 
                        FROM presupuestos 
                        WHERE id_presupuesto = %s
                    """, (id_presupuesto,))
                    presupuesto = cur.fetchone()
                    if presupuesto and presupuesto['cantidad_sesiones'] and presupuesto['cantidad_sesiones'] > 0:
                        precio_sesion = presupuesto['presupuesto_total'] / presupuesto['cantidad_sesiones']
                        monto_calculado = precio_sesion * MULTA_PORCENTAJE_TRATAMIENTO
                except Exception as e:
                    print(f"Error calculando precio de sesión: {e}")
            
            try:
                # Comprobar si ya se multó esta cita para no multar dos veces
                cur.execute("SELECT 1 FROM paciente_multas WHERE id_cita = %s", (id_cita,))
                if cur.fetchone():
                    continue
                
                # Insertar multa
                cur.execute("""
                    INSERT INTO paciente_multas 
                    (id_paciente, id_cita, monto_multa, motivo_multa, observaciones)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_paciente, 
                    id_cita, 
                    monto_calculado, 
                    'AUSENCIA A CITA', 
                    f'Multa automática por inasistencia el {fecha}.'
                ))
                
                # Actualizar estado de la cita a AUSENTE (ej. estado 5, o 4 Cancelada si no existe)
                # OJO: dependemos de id_estado_cita = 5 (AUSENTE), insertado en la migracion
                cur.execute("""
                    UPDATE citas 
                    SET id_estado_cita = 5 
                    WHERE id_cita = %s
                """, (id_cita,))
                
                # Log del cambio (si se quiere, podemos saltar si es job en batch)
                cur.execute("""
                    INSERT INTO citas_log_estados 
                    (id_cita, estado_anterior, estado_nuevo, motivo_cambio, usuario_cambio)
                    VALUES (%s, 'AGENDADA/CONFIRMADA', 'AUSENTE', 'Ausencia injustificada procesada por sistema', 'SISTEMA')
                """, (id_cita,))
                
                conn.commit()
                multas_generadas += 1
                
            except Exception as e:
                conn.rollback()
                print(f"[{datetime.datetime.now()}] Error procesando cita {id_cita}: {str(e)}")
                
        print(f"[{datetime.datetime.now()}] Proceso completado. Se generaron {multas_generadas} multas nuevas.")
        
    except Exception as e:
        print(f"[{datetime.datetime.now()}] Error general en el script: {str(e)}")
    finally:
        if cur: cur.close()
        if conn: conn.close()

if __name__ == '__main__':
    procesar_multas()
