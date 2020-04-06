from bs4 import BeautifulSoup
import requests
from bs4.element import Comment
import os
import numpy as np
import psycopg2
from lxml.cssselect import CSSSelector

def make_list_of_words(data):
    list_data = []
    y = []
    for line in data:
        list_data.append(line.strip())
    return list_data

def data_sites_processing(data):
    list_data = []
    y = []
    for line in data:
        list_data.append(line.strip().split()[1])
        y.append(line.strip().split()[0])
    return list_data, y
Y = []
data_sites = open('C:\sites.txt', 'r', encoding='utf-8')
sites, Y = data_sites_processing(data_sites)
data_price = open('C:\data_price.txt', 'r', encoding='utf-8')
data_words  = make_list_of_words(data_price)
data_words.append('$')
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(page):
    texts = page.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return " ".join(t.strip() for t in visible_texts)

def get_result(url):
    rs = requests.session()
    rs.proxies['http'] = os.getenv("proxy", "socks5h://localhost:9150")  # что передается?
    rs.proxies['https'] = os.getenv("proxy", "socks5h://localhost:9150")
    rs.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
    rs.headers['Accept-Language'] = 'Accept-Language: en-US,en;q=0.5'
    result = rs.get(url, timeout=1000)
    rs.close()
    return result

def find_all_pictures(page):
    pictures = page.findAll('img')
    return len(pictures)
def find_all_valute_sign(page, data_words):
    str = text_from_html(page)
    numb = 0
    for simb in data_words:
        numb += str.count(simb)
    return numb
def find_symb_numb(page):
    return len(" ".join(text_from_html(page).split()))

def find_buttons(page):
    buttons = page.findAll('form')
    return len(buttons)

def get_data(sites):
    data = []
    print(Y)
    print(sites)
    for site,y in zip(sites,Y):
        page = BeautifulSoup(get_result(site).text, 'lxml')
        x_features = [find_all_pictures(page),find_all_valute_sign(page, data_words),find_buttons(page),find_symb_numb(page)]
        data.append([x_features,y])
    return data

def connect_with_base():
    conn = psycopg2.connect(dbname='wordbase', user='postgres',
                            password='aventador1357', host='localhost')
    return conn

def get_cursor(conn):
    return conn.cursor()

def insert_data(cursor, picture_count, valute_sign_count, buttons_count, symb_numb, site_class):
    print(picture_count, valute_sign_count, buttons_count, symb_numb, site_class)
    insert_query = "INSERT INTO dataset (picture_count, valute_sign_count, buttons_count, symb_numb, class) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(insert_query, (picture_count, valute_sign_count, buttons_count, symb_numb, site_class))

def get_table(cursor):
    cursor.execute("SELECT (picture_count, valute_sign_count, buttons_count, symb_numb, class) FROM dataset")
    print(cursor.fetchall())

def save_data_in_base():
    conn = connect_with_base()
    cursor = get_cursor(conn)
    for elem in get_data(sites):
        print(elem)
        insert_data(cursor, elem[0][0], elem[0][1], elem[0][2],elem[0][3], int(elem[1]))
    conn.commit()

save_data_in_base()