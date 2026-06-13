from app.conexion.Conexion import Conexion
from typing import Dict

class UISettingsService:
    @staticmethod
    def obtener_preferencias() -> Dict[str, str]:
        """
        Obtiene todas las preferencias de UI de la base de datos.
        Retorna un diccionario con los valores por defecto si hay error.
        """
        defaults = {
            # Botones de acción
            'boton_agregar':  'primary',
            'boton_editar':   'success',
            'boton_eliminar': 'danger',
            'boton_guardar':  'primary',
            'boton_limpiar':  'secondary',
            # Encabezados de sección (card-header text color)
            'color_card_primario':    'primary',
            'color_card_secundario':  'success',
            'color_card_terciario':   'info',
            'color_card_cuaternario': 'warning',
            # Badges de estado
            'color_badge_activo':   'success',
            'color_badge_inactivo': 'secondary',
        }
        
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            
            cur.execute("SELECT componente, color_clase FROM preferencias_ui")
            rows = cur.fetchall()
            
            preferencias = {row[0]: row[1] for row in rows}
            
            # Combinar con los valores por defecto por si faltan algunos
            return {**defaults, **preferencias}
            
        except Exception as e:
            print(f"Error al obtener preferencias de UI: {e}")
            return defaults
        finally:
            if 'cur' in locals():
                cur.close()
            if 'con' in locals():
                con.close()

    @staticmethod
    def actualizar_preferencia(componente: str, color_clase: str) -> bool:
        """
        Actualiza o inserta una preferencia de UI.
        """
        try:
            conexion = Conexion()
            con = conexion.getConexion()
            cur = con.cursor()
            
            cur.execute("""
                INSERT INTO preferencias_ui (componente, color_clase, actualizado_en)
                VALUES (%s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (componente) DO UPDATE 
                SET color_clase = EXCLUDED.color_clase,
                    actualizado_en = CURRENT_TIMESTAMP
            """, (componente, color_clase))
            
            con.commit()
            return True
        except Exception as e:
            print(f"Error al actualizar preferencia de UI: {e}")
            if 'con' in locals():
                con.rollback()
            return False
        finally:
            if 'cur' in locals():
                cur.close()
            if 'con' in locals():
                con.close()
