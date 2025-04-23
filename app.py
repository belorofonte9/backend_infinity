import psycopg2
from faker import Faker
import time

# Configura el generador de datos falsos
fake = Faker()

# Conexión a la base de datos PostgreSQL
def connect_db():
    try:
        connection = psycopg2.connect(
            host="db",  # Se refiere al nombre del servicio de PostgreSQL en Docker
            database="mydatabase",
            user="postgres",
            password="password"
        )
        return connection
    except Exception as error:
        print(f"Error al conectar a la base de datos: {error}")
        return None

# Crear tabla en PostgreSQL
def create_table(connection):
    cursor = connection.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        address VARCHAR(100),
        email VARCHAR(50)
    );
    '''
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

# Insertar datos falsos en la base de datos
def insert_fake_data(connection):
    cursor = connection.cursor()
    insert_query = '''
    INSERT INTO users (name, address, email) VALUES (%s, %s, %s);
    '''
    name = fake.name()
    address = fake.address()
    email = fake.email()

    cursor.execute(insert_query, (name, address, email))
    connection.commit()
    cursor.close()

# Ejecutar la inserción en bucle
def main():
    connection = connect_db()
    if connection is None:
        return

    create_table(connection)

    try:
        while True:
            insert_fake_data(connection)
            print("Datos insertados correctamente")
            time.sleep(5)  # Espera 5 segundos entre cada inserción
    except KeyboardInterrupt:
        print("Detenido por el usuario")
    finally:
        connection.close()

if __name__ == '__main__':
    main()
