import requests
import os
from bs4 import BeautifulSoup
import socks
import csv
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
    try:
        catalog = html.find('td', class_='td-right-side').find_all('table', class_='offer-vertical')
    except:
        return;
    for product in catalog:
        try:
            prod_url = base_url + product.find('td',class_='offer-vertical-title-td').find('a').get('href')
        except:
            prod_url = ''
        try:
            prod_price =  product.find('td',class_='offer-vertical-td-right').find('font',class_='green').text
        except:
            prod_price = ''
        try:
            prod_name = product.find('td',class_='offer-vertical-title-td').find('a').text
        except:
            prod_name = ''
        tuple = (prod_name, prod_price, prod_url)
        #print(tuple)
        prod_list.append(tuple)



def parse_pages(page):
    pages = page.find('div', class_='pagination').find_all('a', class_='')
    current_page = page.find('div', class_='pagination').find('a', class_='active').text
    #print(current_page)
    try_second = False
    for element in pages:
        #print(element.text)
        if element.text == str(int(current_page)+1):
            new_link = base_url + element.get('href')
            print(new_link)
            try:
                page = BeautifulSoup(get_result(new_link).text, 'lxml')
            except:
                try_second = True
            take_list_of_products_from_page(page)
            parse_pages(page)

            #unnecessary
        if try_second == True and element.text == str(int(current_page)+2):
            try_second = False
            new_link = base_url + element.get('href')
            print(new_link)
            try:
                page = BeautifulSoup(get_result(new_link).text, 'lxml')
            except:
                continue;
            take_list_of_products_from_page(page)
            parse_pages(page)
            # unnecessary

    #take_list_of_products_from_page(page)

base_url = 'http://elite6c3wh756biv7v2fyhnoitizvl2gmoisq7xgmp2b2c5ryicottyd.onion/'
drugs_url = 'http://elite6c3wh756biv7v2fyhnoitizvl2gmoisq7xgmp2b2c5ryicottyd.onion/index.php?cid=2'
soup = BeautifulSoup(get_result(drugs_url).text,'lxml')
parse_pages(soup)
set(prod_list)
print(prod_list)
print(len(prod_list))
csv_writer(prod_list)