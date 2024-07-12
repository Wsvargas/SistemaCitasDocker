import os
import mysql.connector

def get_mysql_connection():
    host = os.getenv('MYSQL_CITAS_HOST', 'mysql_citas')
    user = os.getenv('MYSQL_CITAS_USER', 'root')
    password = os.getenv('MYSQL_CITAS_PASSWORD', 'root')
    database = os.getenv('MYSQL_CITAS_DB', 'citas_medicas')
    port = int(os.getenv('MYSQL_CITAS_PORT', 3306))

    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        port=port
    )
