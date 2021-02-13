import mysql.connector

conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="mysql"
        )
cur = conn.cursor(buffered=True)