import psycopg2

class Conexion:

    """Metodo constructor
    """
    def __init__(self):
        # Leer desde variables de entorno con fallbacks para desarrollo local
        import os
        dbname = os.getenv("DB_NAME", "clinicain")
        user = os.getenv("DB_USER", "postgres")
        password = os.getenv("DB_PASSWORD", "postgres")
        host = os.getenv("DB_HOST", "127.0.0.1")
        port = os.getenv("DB_PORT", "5432")
        
        try:
            self.con = psycopg2.connect(
                dbname=dbname, 
                user=user, 
                password=password, 
                host=host, 
                port=port
            )
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
            raise e

    """getConexion

        retorna la instancia de la base de datos
    """
    def getConexion(self):
        return self.con
    


    