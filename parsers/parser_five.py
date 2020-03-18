import requests
import os
from bs4 import BeautifulSoup
import csv
import socks

prod_list= []
def csv_writer(list):
        with open('data_base.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)
            for line in list:
                writer.writerows([line])

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

    tables = html.find_all('table', class_='table1')
    catalog = []
    for table in tables:
            catalog +=table.find('tbody').find_all('tr')
    for product in catalog:
        try:
            prod_name = product.find_all('td')[0].text
        except:
            prod_name = ''
        try:
            prod_price = product.find_all('td')[1].text
        except:
            prod_price = ''

        tuple = (prod_name, prod_price)
        prod_list.append(tuple)


# def parse_pages(page):
#     pages = soup.find('div', class_='storefront-sorting').find('ul', class_='page-numbers').find_all('li')
#     for element in pages:
#         take_list_of_products_from_page(page)
#         try:
#             new_link = element.find('a').get('href')
#         except:
#             continue;
#         page = BeautifulSoup(get_result(new_link).text, 'lxml')
#
#     take_list_of_products_from_page(page)

base_url = 'http://ll6lardicrvrljvq.onion/'
soup = BeautifulSoup(get_result(base_url).text,'lxml')
take_list_of_products_from_page(soup)
print(prod_list)
print(len(prod_list))
csv_writer(prod_list)