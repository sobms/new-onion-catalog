from collections import Counter
from bs4 import NavigableString

def del_None(lst):
    for l in lst:
        if isinstance(l, NavigableString):
            l.extract();

    for l in lst:
        if l.name == None:
            lst.remove(l)

def is_necessary_type(tag):
    lst2 = ['tr','li','div', 'td']
    for l in lst2:
        if tag == l:
            return True
def is_catalog(lst_tags):
    answer = False
    del_None(lst_tags)
    lst_tags = [i.name for i in lst_tags]

    c = Counter(lst_tags)                       #check if we have equal elements
    for i in lst_tags:
        # print(c[i])
        if ((len(lst_tags) >=3) and ((c[i] / len(lst_tags)) >= 0.8)):
            type = i;                           #tag of elements
            answer = True

    if len(lst_tags) < 3:                       #check if length is very small
        ###
        for i in lst_tags:                      #check if we have products in table
            if ((lst_tags[0] == i) and (lst_tags[0] == 'tr')):
                answer = True;
                return answer;
        ###
        answer = False

    if ((answer == True) and (not is_necessary_type(type))):              #check if it have necessary type
        answer = False;

    return answer