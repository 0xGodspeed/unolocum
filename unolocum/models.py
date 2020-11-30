from flask_sqlalchemy import SQLAlchemy
from unolocum import db

class URL(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), unique=True, nullable=False)
    name = db.Column(db.String(100))
    price = db.Column(db.Float)
    def __repr__(self):
        return f"Url('{self.id}', '{self.url}', '{self.name}', '{self.price}')"
