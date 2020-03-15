import requests
import os
from bs4 import BeautifulSoup
from bs4.element import Comment
import psycopg2
import datetime
import time
import socks
url = 'http://rso4hutlefirefqp.onion/'
def get_cursor():
    conn = psycopg2.connect(dbname='wordbase', user='postgres',
                        password='aventador1357', host='localhost')
    cursor = conn.cursor()
    return cursor
def insert_in_table_url(cursor, link):
    sql_insert_value = "INSERT INTO база url VALUES (?, ?)"
    cursor.execute("INSERT INTO база url VALUES (?, ?)")
    cursor.execute(link, datetime.date)
    cursor.commit()

def close_table(cursor):
    cursor.close();

used = set()
def get_result(url):
     rs = requests.session()
     rs.proxies['http'] = os.getenv("proxy", "socks5h://localhost:9150")       #что передается?
     rs.proxies['https'] = os.getenv("proxy", "socks5h://localhost:9150")
     rs.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
     rs.headers['Accept-Language'] = 'Accept-Language: en-US,en;q=0.5'
     result = rs.get(url, timeout=1000)
     rs.close()
     return result

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):            #????
        return False
    return True


def text_from_html(body):
    soup = BeautifulSoup(body, 'lxml')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)
    return u" ".join(t.strip() for t in visible_texts)



def dfs(link):
    global used, url
    print(link)                                          #print page link
    # insert_in_table_url(get_cursor(), link)
    used.add(link)

    try:
        html_page = get_result(link)
    except:
        return
    parse_page = BeautifulSoup(html_page.text, 'lxml')
    print(text_from_html(html_page.text))                       #print page text
    for html_element in parse_page.findAll('a'):
        # for tmp_element in parse_page.findAll('a'):
        #     print('!  ',tmp_element.get('href'))
        if str(html_element.get('href'))[:4] == 'http':
            continue
        new_link = url + str(html_element.get('href'))

        if new_link not in used:
            dfs(new_link)


dfs(url)
print(used)
