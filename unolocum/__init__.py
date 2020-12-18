from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ee1ec83497565fa4ca2ccb5e16b74ae7'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost/unolocum'
# db = SQLAlchemy(app)
from unolocum import routes
