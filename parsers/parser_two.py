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
        catalog = html.find('ul', class_='products columns-3').find_all('li')
    except:
        return;
    for product in catalog:
        try:
            prod_url = product.find('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link').get('href')
        except:
            prod_url = ''
        try:
            prod_price = product.find('span').text
        except:
            prod_price = ''
        try:
            prod_name = product.find('h2').text
        except:
            prod_name = ''
        tuple = (prod_name, prod_price, prod_url)
        prod_list.append(tuple)


def parse_pages(page):
    pages = soup.find('div', class_='storefront-sorting').find('ul', class_='page-numbers').find_all('li')
    for element in pages:
        take_list_of_products_from_page(page)
        try:
            new_link = element.find('a').get('href')
        except:
            continue;
        page = BeautifulSoup(get_result(new_link).text, 'lxml')

    take_list_of_products_from_page(page)

base_url = 'http://f6pxr3iqw7iziuc2.onion/'
soup = BeautifulSoup(get_result('http://f6pxr3iqw7iziuc2.onion/').text,'lxml')
parse_pages(soup)
print(prod_list)
print(len(prod_list))