from bs4 import NavigableString

def make_list_of_words(data):
    list_data = []
    for line in data:
        list_data.append(line.strip())
    return list_data

names = open('C:\\names.txt', 'r', encoding='utf-8')
names_list = make_list_of_words(names)

def getText(parent):
    return ''.join(parent.find_all(text=True, recursive=False)).strip()

def is_text_name(text,names):
    txt_as_list = text.strip().lower().split()

    for wrd in txt_as_list:
        #print(wrd)
        for name in names_list:
            if name == wrd:
                return True
    return False

def search_name(tag):
    if isinstance(tag, NavigableString):
          return ' '
    if is_text_name(getText(tag), names):
         return(getText(tag))

    for child in list(tag.children):
        ans = search_name(child)
        if ans != ' ':
            return ans
    return ' '