import os
import mysql.connector

def get_historial_mysql_connection():
    host = os.getenv('MYSQL_HISTORIAL_HOST', 'mysql_historial')
    user = os.getenv('MYSQL_HISTORIAL_USER', 'root')
    password = os.getenv('MYSQL_HISTORIAL_PASSWORD', 'root')
    database = os.getenv('MYSQL_HISTORIAL_DB', 'historialmedico')
    port = int(os.getenv('MYSQL_HISTORIAL_PORT', 3306))

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
