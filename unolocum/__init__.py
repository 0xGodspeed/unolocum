from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = 'ee1ec83497565fa4ca2ccb5e16b74ae7'
from unolocum import routes
