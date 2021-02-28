from flask import Flask
from mysql.connector import DatabaseError, ProgrammingError
from os import getcwd, path

db_path = path.join(getcwd(), 'database.sql')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ee1ec83497565fa4ca2ccb5e16b74ae7'

from unolocum.sql import cur, conn

try:
    for query in open(db_path):
        cur.execute(query)
except Exception as exception:
    print(exception)

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
