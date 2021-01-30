import requests
import re
import textwrap
from db import Database
from html import make_html_table
from mailer import Mailer
from time import gmtime, strftime
import configuration as config

database = Database()

with database as db:
    for search_terms in config.search_list:
        URL = 'https://www.depop.com/search/?q=%s' % search_terms
        request_text = requests.get(URL).text

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

        now = (strftime("%Y-%m-%d %H:%M:%S", gmtime()))

        search_results = [list(a) for a in zip(search_titles, search_users, search_images, search_url, price)]
        [result.append(now) for result in search_results]

        connection = db.connect()

        sql = textwrap.dedent("""
            INSERT INTO depop_results 
            (post_title, post_user, post_image, post_url, post_price, script_run) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (post_title, post_user, post_image, post_url) DO NOTHING
        """)
        db.executemany(sql, search_results)

    sql = textwrap.dedent("""
        SELECT *
        FROM depop_results
        WHERE script_run = %s
    """)
    results = db.select_all(sql, [now])

    if len(results) > 0:

        body = []
        body.append('<h2>Depop Search Results</h2>')
        headings = [
                    {'label': 'Post Title', 'show': False},
                    {'label': 'Image', 'show': False},
                    {'label': 'Title', 'show': False},
                    {'label': 'Title', 'show': True},
                    {'label': 'Price', 'show': True}
                    ]
        email = make_html_table(body, results, headings)
        mail = Mailer()
        email_body = ''.join(body)
        mail.send_message('Your Depop Search Results', email_body)
