from flask import render_template, url_for, redirect, request, flash
from unolocum.amzn_form import UrlForm
from unolocum import app
from bs4 import BeautifulSoup
import requests
from unolocum.sql import cur, conn
from mysql.connector.errors import DataError

# global variables
# amzn
amzn_redirects = 0
change_in_price = 'none'
amzn_table_data = []
amzn_table_headings = ('#', 'Product', 'Current Price') 
cur.execute("SELECT id, name, price FROM URL")   
print(amzn_table_data)

# nsinfo
hemis = "northern"
ns_table_data = []
ns_table_headings = ('#', 'Name', 'Direction', 'Image')


#------------------------------------------amazon functions-----------------------------------------------


def AmazonTableData():                                           # reformats the table data into list so that its 
    global amzn_table_data                                            # more easily accessible 
    cur.execute("SELECT id, name, price FROM URL")   
    amzn_table_data = cur.fetchall()
    for i in range(len(amzn_table_data)):
        amzn_table_data[i] = list(amzn_table_data[i])
        amzn_table_data[i][2] = str(amzn_table_data[i][2]) 

AmazonTableData()

def productinfo(url):                           # gets info of the product from the url
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
    
def update_prices():                            # updates prices
    global change_in_price
    AmazonTableData()
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
                amzn_table_data[url_count][2] = str(c_p_price) + ' ▲'                 
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")
            elif c_p_price < old_price:
                print("decreasing")
                amzn_table_data[url_count][2] = str(c_p_price) + ' ▼'
                cur.execute(f"UPDATE URL SET price={c_p_price} WHERE url='{url}'")
        conn.commit()
        url_count += 1


# ------------------------------------------routes------------------------------------------------------

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
        update_prices()
        return redirect('/amzn')
    print(amzn_table_data)
    return render_template('amzn.htm', title='Amazon Tracking', form=form, amzn_table_headings=amzn_table_headings, amzn_table_data=amzn_table_data, change_in_price=change_in_price)


@app.route('/nightsky', methods = ['GET', 'POST'])
def nightsky():
    global hemis
    if request.method == 'POST':
        hemis = request.form['hemis']
    
    
    return render_template('nightsky.htm', title='Night Sky Info', hemis=hemis, ns_table_data=ns_table_data, ns_table_headings=ns_table_headings)


