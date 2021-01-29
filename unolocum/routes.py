from flask import render_template, url_for, redirect, request, flash
from unolocum.amzn_form import UrlForm
from unolocum import app
from bs4 import BeautifulSoup
import requests
from unolocum.sql import cur, conn
from mysql.connector import DatabaseError, ProgrammingError
from mysql.connector.errors import DataError

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

# global variables
amzn_redirects = 0
change_in_price = 'none'
cur.execute("SELECT id, name, price FROM URL")   
table_data = []

table_headings = ('#', 'Product', 'Current Price') 
print(table_data)


def TableData():
    global table_data
    cur.execute("SELECT id, name, price FROM URL")   
    table_data = cur.fetchall()
    for i in range(len(table_data)):
        table_data[i] = list(table_data[i])
        table_data[i][2] = str(table_data[i][2]) 

TableData()

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
    TableData()
    cur.execute("SELECT url from URL ORDER BY id")
    urls = cur.fetchall()
    print(urls)
    url_count = 0
    for url in urls: 
        print(url_count)
        url = url[0]
        product_info = productinfo(url)
        c_p_price = product_info[2]              # current price
        cur.execute(f"SELECT price FROM URL where url='{url}'")
        old_price = cur.fetchone()[0]
        print(old_price)
        print(type(old_price), type(c_p_price))
        if c_p_price != old_price:
            print(c_p_price)
            if c_p_price > old_price:
                print("increasing")
                table_data[url_count][2] = str(c_p_price) + ' ▲'                 
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")
            elif c_p_price < old_price:
                print("decreasing")
                table_data[url_count][2] = str(c_p_price) + ' ▼'
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")
        conn.commit()
        url_count += 1

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
    global table_data
    global table_headings
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
        
    return render_template('amzn.htm', title='Amazon Tracking', form=form, table_headings=table_headings, table_data=table_data, change_in_price=change_in_price)


@app.route('/nightsky')
def nightsky():
    
    return render_template('nightsky.htm', title='Night Sky Info')