import mysql.connector
import os


db_params = {
    "host": os.environ.get('DB_HOST', '127.0.0.1'),
    "user": os.environ.get('DB_USER'),
    "password": os.environ.get('DB_PASSWORD'),
    "port":os.environ.get('DB_PORT', '3306')
}

def check_create_database(conn_params, db_name):

    conn = mysql.connector.connect(**conn_params)
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES")
    databases = [row[0] for row in cursor.fetchall()]

    if db_name not in databases:
        cursor.execute(f"CREATE DATABASE {db_name}")
        print(f"Database '{db_name}' created.")
    else:
        print(f"Database '{db_name}' already exists.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    db_to_check = os.environ.get('DB_NAME', 'ecomm')
    try:
        check_create_database(db_params, db_to_check)
    except mysql.connector.Error as e:
        print(f"An error was1 occurred in connecting databse: {e}")
