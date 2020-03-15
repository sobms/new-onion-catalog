import requests
import os
from bs4 import BeautifulSoup
import socks

prod_list= []

def get_result(url):
    rs = requests.session()
    rs.proxies['http'] = os.getenv("proxy", "socks5h://localhost:9150")  # что передается?
    rs.proxies['https'] = os.getenv("proxy", "socks5h://localhost:9150")
    rs.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0'
    rs.headers['Accept-Language'] = 'Accept-Language: en-US,en;q=0.5'
    result = rs.get(url, timeout=1000)
    rs.close()
    return result

def take_list_of_products_from_page(html):
    try:
        products = html.find('div',class_='col-sm-9 padding-right').find_all('div', class_='col-sm-4')
    except:
        return;
    for product in products:
        try:
            prod_url = base_url + product.find('div', class_='productinfo text-center').find('a').get('href')
            #prods_url.append(prod_url)
        except:
            prod_url = ''
        try:
            prod_price = product.find('div', class_='productinfo text-center').find('h2').text
            #prods_price.append(prod_name)
        except:
            continue;
        try:
            prod_name = product.find('div', class_='productinfo text-center').find('p').text
            #prods_price.append(prod_name)
        except:
            continue;
        tuple = (prod_name, prod_price, prod_url)
        prod_list.append(tuple)

def parse_pages(page):
    catalog = soup.find('div', class_='panel-group category-products')
    for element in catalog.find_all('div', class_='panel panel-default'):
        take_list_of_products_from_page(page)
        new_link = base_url + element.find('a').get('href')
        page = BeautifulSoup(get_result(new_link).text,'lxml')
    take_list_of_products_from_page(page)

base_url = 'http://wzvsz3g6dodj2fyh.onion/'
soup = BeautifulSoup(get_result('http://wzvsz3g6dodj2fyh.onion/').text,'lxml')
parse_pages(base_url)
print(prod_list)
print(len(prod_list))