from flask import Flask
from mysql.connector import DatabaseError, ProgrammingError
from os import getcwd

cwd = getcwd()
print(cwd)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ee1ec83497565fa4ca2ccb5e16b74ae7'

from unolocum.sql import cur, conn

try:
    for query in open(f"{cwd}\\database.sql"):
        cur.execute(query)
except Exception:
    print("unolocum_space_objects exists")

try:
    cur.execute("CREATE DATABASE unolocum")
    print("Database created")
except DatabaseError:
    print("Database already exists")

try:
    cur.execute("USE unolocum")
    cur.execute("CREATE TABLE URL (id int AUTO_INCREMENT PRIMARY KEY, url VARCHAR(500) UNIQUE, name VARCHAR(100), price FLOAT)")
    print("Table Created.")
except ProgrammingError:
    print("Table already exists")



from unolocum import routes
