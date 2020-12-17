import requests
import re
from html import make_html_table
from mailer import Mailer


url = 'https://www.depop.com/search/?q=nike'

request_text = requests.get(url).text

username_and_product_titles = re.findall("(?<=/products/).*(?=/\")", request_text)

price_amount = re.findall("(?<=\"priceAmount\":\")([\d]+.[\d]+)", request_text)
currency_symbol = re.findall("(?<=\"currencySymbol\":\")(.)(?=\"\,)", request_text)
currency_name = re.findall("(?<=\"currencyName\":\")(\w{3})(?=\"\},)", request_text)
product_image_url = re.findall("(?<=\"1280\":\")(.+?)(.gif|.jpg|.jpeg|.tiff|.png)", request_text)

search_titles = []
search_images = []
search_url = []

for title in username_and_product_titles:
    search_titles.append(' '.join(title.split('-')[1:]))
    search_url.append('https://www.depop.com/products/' + title + '/')

for image in product_image_url:
    search_images.append(''.join(image))

y = list(zip(currency_symbol, price_amount, currency_name))
price = [' '.join(i) for i in y]

results = list(zip(search_titles, search_images, search_url, price))

body = []
body.append('<h2>Depop Search Results</h2>')
headings = [
            {'label': 'Post Title', 'show': False},
            {'label': 'Image', 'show': False},
            {'label': 'Title', 'show': True},
            {'label': 'Price', 'show': True}
            ]
email = make_html_table(body, results, headings)
mail = Mailer()
email_body = ''.join(body)
mail.send_message('Your Depop Search Results', email_body)
