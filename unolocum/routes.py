from flask import render_template, url_for, redirect, request, flash
from unolocum.amzn_form import UrlForm
from unolocum import app
from bs4 import BeautifulSoup
import requests
from unolocum.sql import cur, conn
from mysql.connector import DatabaseError, ProgrammingError
from mysql.connector.errors import DataError

amzn_redirects = 0
change_in_price = 'none'

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


def productinfo(url):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
    page = requests.get(url, headers = headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    pname = soup.find(id="productTitle").get_text()
    pname = pname.strip()         #product name
    print(url)
    try:
        p_price = soup.find(id="priceblock_ourprice").get_text()     # price in string form
    except AttributeError:
        p_price = soup.find(id="priceblock_dealprice").get_text()     # price in string form
    c_p_price = float(p_price.replace(',', '')[2: ])             # price in float form
    return [url, pname, c_p_price]
    
def update_prices():
    global change_in_price
    cur.execute("SELECT url from URL")
    urls = cur.fetchall()
    for url in urls:        
        url = url[0]
        product_info = productinfo(url)
        c_p_price = product_info[2]              # current price
        cur.execute("SELECT price FROM URL")
        old_price = cur.fetchone()[0]
        if c_p_price != old_price:
            if c_p_price >= old_price:
                change_in_price = 'inc'
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")
            elif  c_p_price <= old_price:
                change_in_price = 'dec'
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")

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
    global amzn_redirects
    amzn_redirects += 1
    if amzn_redirects <= 1:
        update_prices()
    form = UrlForm()
    url = form.url.data
    if form.validate_on_submit():
        product_info = productinfo(url)
        url = product_info[0]
        pname = product_info[1]
        c_p_price = product_info[2]

        try:
            cur.execute(f"INSERT INTO URL (url, name, price) VALUES('{url}', '{pname}', {c_p_price})")
        except DataError:
            pname = pname[ :97] + '...'
            print(pname)
            cur.execute(f"INSERT INTO URL (url, name, price) VALUES('{url}', '{pname}', {c_p_price})")
        conn.commit()
        
        flash(f'Added.', 'success')
        return redirect('/amzn')
    
    
    cur.execute("SELECT id, name, price FROM URL")   
    table_data = cur.fetchall()
    table_headings = ('#', 'Product', 'Current Price') 
    return render_template('amzn.htm', title='Amazon Tracking', form=form, table_headings=table_headings, table_data=table_data, change_in_price=change_in_price)
