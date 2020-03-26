import re
from bs4 import NavigableString

def make_list_of_words(data):
    list_data = []
    for line in data:
        list_data.append(line.strip())
    return list_data

def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

data_price = open('C:\data_price.txt', 'r', encoding='utf-8')
data_words = make_list_of_words(data_price)

def compare_list_of_words(text,data_words):
    for key_word in data_words:
        regex = re.compile(key_word+'\s*\d+')
        if re.search("\d+\s*%s"%(key_word),text) or re.search("%s\s*\d+"%(key_word),text) or text.strip() in data_words or text.strip() == '$': # or re.search("\$"+"\s*\d+",text) or re.search("\d+\s*"+"\$",text):
            return True
    return False

def search_price(tag):
    if isinstance(tag, NavigableString):
          return ' '
    #print(getText(tag))
    if compare_list_of_words(getText(tag), data_words):
        #print(getText(tag))
        return getText(tag)

    for child in list(tag.children):
        ans = search_price(child)
        if ans != ' ':
            return ans
    return ' '