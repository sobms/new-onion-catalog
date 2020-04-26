import pandas as pd
import numpy as np
import psycopg2
base = pd.read_csv('C:\_results_of_research.csv')

lst = []
for i in range(len(base)):
    lst.append(tuple([base['Наименование'].iloc[i], base['Цена'].iloc[i], base['Валюта'].iloc[i], base['Количество товара'].iloc[i], base['Ссылка'].iloc[i]]))
print(len(lst))
def connect_with_base():
    conn = psycopg2.connect(dbname='wordbase', user='postgres',
                            password='aventador1357', host='localhost')
    return conn

def get_cursor(conn):
    return conn.cursor()
cursor = get_cursor(connect_with_base())
def insert_data(cursor, product_name, product_price, valute, quantity, product_url):
    insert_query = "INSERT INTO main_base (Наименование, Цена, Валюта, Количество_товара, Ссылка) VALUES (%s, %s, %s, %s, %s);"
    cursor.execute(insert_query, (product_name, product_price, valute, quantity, product_url))

def save_data_in_base(set_of_tuples):
    conn = connect_with_base()
    cursor = get_cursor(conn)
    for elem in set_of_tuples:
        print(str(elem))
        insert_data(cursor, elem[0], elem[1], elem[2], elem[3],elem[4])
    conn.commit()
    print(len(set_of_tuples))
save_data_in_base(lst)