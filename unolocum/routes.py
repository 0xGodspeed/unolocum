from flask import render_template, url_for, redirect, request, flash
from unolocum.models import URL
from unolocum.amzn_form import UrlForm
from unolocum import app, db
from bs4 import BeautifulSoup
import requests

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.htm')

@app.route('/about')
def about():
    return render_template('about.htm', title = 'About')

@app.route('/services')
def services():
    return render_template('services.htm', title = 'Services')

@app.route('/test')
def test():
    return render_template('test.htm', title = 'test')

@app.route("/callback")
def callback():
    global authorization_url
    authorization_url = (request.url)
    returnf()
    return render_template('home.htm')

def returnf():
    tempvar = authorization_url

@app.route('/amzn', methods=['GET', 'POST'])
def amzn():
    form = UrlForm()
    if form.validate_on_submit():
        url = form.url.data
        headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
        page = requests.get(url, headers = headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        pname = soup.find(id="productTitle").get_text()
        pname = pname.strip()         #product name
        p_price = soup.find(id="priceblock_ourprice").get_text()     # price in string form
        c_p_price = float(p_price.replace(',', '')[2: ])             # price in float form
        amzn_url = URL(url=url, name=pname, price=c_p_price)
        db.session.add(amzn_url)
        db.session.commit()
        flash(f'Added.', 'success')
        return redirect('/amzn')
    return render_template('amzn.htm', title  = 'Amazon Tracking', form = form)