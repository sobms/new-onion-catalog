import requests
import re
import os
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

data_price = open('C:\data_price.txt', 'r', encoding='utf-8')
data_words = make_list_of_words(data_price)
names = open('C:\\names.txt', 'r', encoding='utf-8')
names_list = make_list_of_words(names)
set_of_tuples = set()

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
base_url = 'http://brmagic7souidyxq.onion/'
soup = BeautifulSoup(get_result(base_url).text,'lxml')


def move_up_in_tree(tag):
    while (tag.parent.name != 'html'):
        tag = tag.parent
        #print(tag.name,'\n')
        lst = list(tag.children)
        cat_lib.del_None(lst)

        if cat_lib.is_catalog(lst):
            ######output
             lst2=[i.name for i in lst]
             #print(lst2)
            ######output
             for l in lst:
                #print(l.name)
                #print(getText(l))
                product_name = srch_nm.search_name(l)
                product_price = srch_pr.search_price(l);
                product_url = srch_url.search_url(l,base_url);

                tuple = (product_name,product_price,product_url)
                # print(tuple)
                set_of_tuples.add(tuple)
             #exit(0)

        #print('\n\n\n')

def find_price(page):
    print(data_words)
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
                 move_up_in_tree(child)


find_price(soup)
for elem in set_of_tuples:
    print(str(elem))
print(len(set_of_tuples))
