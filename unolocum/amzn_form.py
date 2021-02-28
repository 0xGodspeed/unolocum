from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from bs4 import BeautifulSoup
from unolocum.sql import cur
import requests

class UrlForm(FlaskForm):
    url = StringField('Enter Amazon Product URL:', validators=[DataRequired()])   
    submit = SubmitField('Submit')
    def validate_url(self, url):        
        product = cur.execute(f"SELECT * FROM URL WHERE url='{url.data}' LIMIT 1")       
        print(product)
        if product != None:
            print('working')
            error_text = 'This product has already been added'
            raise ValidationError('This product has already been added.')
