import mysql.connector

conn=mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="unolocum"
        )
cur = conn.cursor()
cur.execute("SELECT price from URL")
urls = cur.fetchone()
print(urls[0])
