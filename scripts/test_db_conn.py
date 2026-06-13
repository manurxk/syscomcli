import os
import psycopg2

def test_conn():
    print("Testing DB connection...")
    dbname = os.getenv("DB_NAME", "clinicain")
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "postgres")
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "5432")
    
    print(f"Connecting to {host}:{port}/{dbname} as {user}...")
    try:
        conn = psycopg2.connect(
            dbname=dbname, 
            user=user, 
            password=password, 
            host=host, 
            port=port,
            connect_timeout=5
        )
        print("Connection SUCCESS!")
        conn.close()
    except Exception as e:
        print(f"Connection FAILED: {e}")

if __name__ == "__main__":
    test_conn()
