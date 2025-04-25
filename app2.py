import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random, os, time

# Configuración
NUM_PERSONAS = 10
DIAS_HISTORICOS = 365
JORNADA_MINUTOS = 360  # 6 horas

# variablaes para conexion 
DB_HOST = os.getenv('POSTGRES_HOST')
DB_NAME = os.getenv('POSTGRES_DB', 'db')
DB_USER = os.getenv('POSTGRES_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')


def wait_for_postgres(timeout=30):
    start = time.time()
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            conn.close()
            print("✅ PostgreSQL está listo.")
            break
        except OperationalError:
            if time.time() - start > timeout:
                raise Exception("❌ PostgreSQL no respondió a tiempo.")
            print("⏳ Esperando PostgreSQL...")
            time.sleep(1)

# Llamar al helper
wait_for_postgres()

fake = Faker()

# Conexión a PostgreSQL
def connect_db():
    try:
        conn = psycopg2.connect(
            host= DB_HOST,
            database= DB_NAME,
            user= DB_USER,
            password= DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# Crear tablas necesarias
def crear_tablas(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS personas (
            id SERIAL PRIMARY KEY,
            nombre VARCHAR(100),
            email VARCHAR(100) UNIQUE
        );
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registros_diarios (
            id SERIAL PRIMARY KEY,
            persona_id INTEGER REFERENCES personas(id),
            fecha DATE,
            total_llamadas INTEGER,
            tiempo_sanitario INTEGER,
            tiempo_descanso INTEGER,
            minutos_totales INTEGER
        );
    """)
    conn.commit()
    cursor.close()

# Insertar personas si no existen
def insertar_personas(conn):
    cursor = conn.cursor()
    personas = []
    for _ in range(NUM_PERSONAS):
        nombre = fake.name()
        email = fake.unique.email()
        cursor.execute(
            "INSERT INTO personas (nombre, email) VALUES (%s, %s) RETURNING id;",
            (nombre, email)
        )
        persona_id = cursor.fetchone()[0]
        personas.append((persona_id, nombre, email))
    conn.commit()
    cursor.close()
    return personas

# Generar registros diarios
def generar_datos_diarios(conn, personas):
    cursor = conn.cursor()
    hoy = datetime.today()

    for persona in personas:
        persona_id = persona[0]
        for i in range(DIAS_HISTORICOS):
            fecha = hoy - timedelta(days=i)
            total_llamadas = random.randint(10, 100)
            tiempo_sanitario = random.randint(2, 10)
            tiempo_descanso = random.randint(5, 20)
            minutos_totales = JORNADA_MINUTOS - (tiempo_sanitario + tiempo_descanso)

            cursor.execute("""
                INSERT INTO registros_diarios (
                    persona_id, fecha, total_llamadas,
                    tiempo_sanitario, tiempo_descanso, minutos_totales
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                persona_id, fecha.date(), total_llamadas,
                tiempo_sanitario, tiempo_descanso, minutos_totales
            ))

    conn.commit()
    cursor.close()

def main():
    conn = connect_db()
    if conn is None:
        return

    crear_tablas(conn)
    personas = insertar_personas(conn)
    generar_datos_diarios(conn, personas)
    print("Datos generados correctamente.")
    conn.close()

if __name__ == '__main__':
    main()
