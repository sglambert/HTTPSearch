import requests
import re
import textwrap
from db import Database
from html import make_html_table
from mailer import Mailer

#TODO Testing with 'Nike' as the search term, update this so it's driven through config data
URL = 'https://www.depop.com/search/?q=nike'

request_text = requests.get(URL).text

#TODO Can probably move all of these to a config table
username_and_product_titles = re.findall("(?<=/products/).*(?=/\")", request_text)
price_amount = re.findall("(?<=\"priceAmount\":\")([\d]+.[\d]+)", request_text)
currency_symbol = re.findall("(?<=\"currencySymbol\":\")(.)(?=\"\,)", request_text)
currency_name = re.findall("(?<=\"currencyName\":\")(\w{3})(?=\"\},)", request_text)
product_image_url = re.findall("(?<=\"1280\":\")(.+?)(.gif|.jpg|.jpeg|.tiff|.png)", request_text)

search_titles = []
search_users = []
search_images = []
search_url = []

for title in username_and_product_titles:
    search_users.append(' '.join(title.split('-')[0:1]))
    search_titles.append(' '.join(title.split('-')[1:]))
    search_url.append('https://www.depop.com/products/' + title + '/')

for image in product_image_url:
    search_images.append(''.join(image))

y = list(zip(price_amount, currency_name))
price = [' '.join(i) for i in y]

search_results = list(zip(search_titles, search_users, search_images, search_url, price))

database = Database()

with database as db:
    connection = db.connect()
    sql = textwrap.dedent("""INSERT INTO depop_results 
                          (post_title, post_user, post_image, post_url, post_price) 
                          VALUES (%s, %s, %s, %s, %s)""")
    db.executemany(sql, search_results)

#TODO Make a seperate select query to the depop_results table
#The result from this query can go into the email
#We can define our query so we avoid things like repeated posts
#It might be a good idea to put a date_posted column in depop_results as well

body = []
body.append('<h2>Depop Search Results</h2>')
headings = [
            {'label': 'Post Title', 'show': False},
            {'label': 'Image', 'show': False},
            {'label': 'Title', 'show': True},
            {'label': 'Price', 'show': True}
            ]
email = make_html_table(body, search_results, headings)
mail = Mailer()
email_body = ''.join(body)
mail.send_message('Your Depop Search Results', email_body)
