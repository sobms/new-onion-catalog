import psycopg2
import requests
import re
import os
import time
from bs4 import NavigableString, BeautifulSoup
import Find_Catalog_lib as cat_lib
import Search_name as srch_nm
import Search_price as srch_pr
import  Search_url as srch_url
import socks
import csv


def make_list_of_words(data):
    list_data = []
    for line in data:
        list_data.append(line.strip())
    return list_data

set_links = open('C:\set_links.txt', 'r',encoding='utf-8')
data_price = open('C:\data_price.txt', 'r', encoding='utf-8')
data_words = make_list_of_words(data_price)
names = open('C:\\names.txt', 'r', encoding='utf-8')
names_list = make_list_of_words(names)
set_of_tuples = set()
list_links = make_list_of_words(set_links)
list_of_catalogs = []

def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def compare_list_of_words(text,data_words):
    for key_word in data_words:
        regex = re.compile(key_word+'\s*\d+')
        if re.search("\d+\s*%s"%(key_word),text) or re.search("%s\s*\d+"%(key_word),text) or text.strip() in data_words or text.strip() == '$': # or re.search("\$"+"\s*\d+",text) or re.search("\d+\s*"+"\$",text):
            return True
    return False

def get_result(url):
    rs = requests.session()
    rs.proxies['http'] = os.getenv("proxy", "socks5h://localhost:9150")  # что передается?
    rs.proxies['https'] = os.getenv("proxy", "socks5h://localhost:9150")
    rs.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
    rs.headers['Accept-Language'] = 'Accept-Language: en-US,en;q=0.5'
    result = rs.get(url, timeout=1000)
    rs.close()
    return result
#base_url = 'http://amazingd64el2zty.onion/?post_type=product'
#soup = BeautifulSoup(get_result(base_url).text,'lxml')

used = set()
return_flag = False
def dfs(link):
    global used, base_url
    global start_time, return_flag
    if return_flag == True:
        return
    soup = BeautifulSoup(get_result(link).text, 'lxml')
    find_price(soup)#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!S
    print(link)                                          #print page link
    # insert_in_table_url(get_cursor(), link)
    used.add(link)

    try:
        html_page = get_result(link)
    except:
         return
    parse_page = BeautifulSoup(html_page.text, 'lxml')
    #f.write(str(text_from_html(html_page.text))+'\n')
    for html_element in parse_page.findAll('a'):
        # for tmp_element in parse_page.findAll('a'):
        #     print('!  ',tmp_element.get('href'))
        if str(html_element.get('href'))[:4] == 'http':
            if str(html_element.get('href'))[:len(base_url)] == base_url:
                new_link = str(html_element.get('href'))
            else:
                continue
        else: new_link = base_url + str(html_element.get('href'))

        if new_link not in used:
            now_time = time.time()
            if now_time - start_time >= 720:        # twelve minutes limit to check site
                return_flag = True
                return
            dfs(new_link)


def move_up_in_tree(tag):
    cursor = connect_with_base();
    while (tag.parent.name != 'html'):
        tag = tag.parent
        #print(tag.name,'\n')
        lst = list(tag.children)
        cat_lib.del_None(lst)

        if (cat_lib.is_catalog(lst)):
            if (lst in list_of_catalogs):
                continue
            list_of_catalogs.append(lst)
            lst2=[i.name for i in lst]
             #print(lst2)
            ######output
            for l in lst:
                #print(l.name)
                #print(getText(l))
                product_name = srch_nm.search_name(l)
                product_price = srch_pr.search_price(l);
                product_url = srch_url.search_url(l,base_url);
                if (product_price == '') or (product_name == ''):
                    continue
                tuple = (product_name,product_price,product_url)
                print(tuple)
                set_of_tuples.add(tuple)
                #print(len(set_of_tuples))
                #print(tuple)
                #insert_data(cursor, product_name,product_price,product_url)
             #exit(0)

        #print('\n\n\n')

def find_price(page):
    num_child = 0
    for child in page.recursiveChildGenerator():
        # print([i.name for i in page.recursiveChildGenerator()])
        if child.name:
            if isinstance(child, NavigableString):
                continue
            try:
                text = getText(child)
            except:
                continue;
            if compare_list_of_words(text,data_words):
                 #print(child.name)
                 #print(child.text)
                 num_child+=1;

                 move_up_in_tree(child)

    if (num_child == 1) and (child.name =='span'):
        while child.parent.name == 'span':
            child = child.parent
        levels=2 #Уровни подъёма при одной ссылке
        for l in levels:
            child = child.parent
            product_name = srch_nm.search_name(l)
            product_price = srch_pr.search_price(l);
            product_url = srch_url.search_url(l, base_url);
            if (product_price == '') or (product_name == ''):
                continue
            tuple = (product_name, product_price, product_url)
            set_of_tuples.add(tuple)

def connect_with_base():
    conn = psycopg2.connect(dbname='wordbase', user='postgres',
                            password='aventador1357', host='localhost')
    return conn

def get_cursor(conn):
    return conn.cursor()

def insert_data(cursor, product_name, product_price, product_url):
    insert_query = "INSERT INTO products_base (Наименование, Цена, Ссылка) VALUES (%s, %s, %s);"
    cursor.execute(insert_query, (product_name, product_price, product_url))

def get_table(cursor):
    cursor.execute("SELECT (Наименование, Цена, Ссылка) FROM products_base")
    print(cursor.fetchall())

def save_data_in_base(set_of_tuples):
    conn = connect_with_base()
    cursor = get_cursor(conn)
    for elem in set_of_tuples:
        print(str(elem))
        insert_data(cursor, elem[0], elem[1], elem[2])
    conn.commit()
    print(len(set_of_tuples))

for link in list_links:
    return_flag = False
    list_of_catalogs.clear()
    used.clear()
    base_url = link #save base link
    start_time = time.time() #start time
    dfs(link) #dfs
    save_data_in_base(set_of_tuples)
    set_of_tuples.clear()









