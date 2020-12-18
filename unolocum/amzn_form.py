from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from bs4 import BeautifulSoup
# from unolocum.mysql import cur
import requests

class UrlForm(FlaskForm):
    url = StringField('Enter Amazon Product URL:', validators=[DataRequired()])    # product name
    submit = SubmitField('Submit')

    def validate_url(self, url):
        product = URL.query.filter_by(url=url.data).first()
        print(product)
        if product != None:
            print('working')
            error_text = 'This product has already been added'
            raise ValidationError('This product has already been added.')


    # app_pass = 'qalmwjknwlnuywks'
    # sender_address = 'unolocum@gmail.com'               #   email that will be used to send the user email
 
    # print(p_price)
    c_p_price = 0

    # def send_mail():
    #     server = smtplib.SMTP('smtp.gmail.com', 587)
    #     server.ehlo()
    #     server.starttls()
    #     server.ehlo()

    #     server.login(sender_address, 'qalmwjknwlnuywks')
    #     subject = 'Price fell down!'    
    #     body = f'''Check the amazon link:
    #     {url}'''

    #     msg = f"Subject: {subject} \n\n {body}"
    #     server.sendmail(
    #         sender_address,
    #         user_email,
    #         msg
    #     )
    #     print('Sent.')
    #     server.quit()


    # if c_p_price <= wanted_price:
    #     send_mail()

# https://www.amazon.in/gp/product/B078BN2H3R/ref=s9_acss_bw_cg_oneplus_1a1_w?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-2&pf_rd_r=41Z7AAPG2P2NCBPV5NZ8&pf_rd_t=101&pf_rd_p=b793da0e-6a2e-4954-8c63-a8e6f5e6c4ee&pf_rd_i=21439725031
