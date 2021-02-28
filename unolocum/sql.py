import mysql.connector

conn=mysql.connector.connect(
        host="localhost",
        user="godspeed",
        password="password",
        database="mysql"
        )
cur = conn.cursor(buffered=True)