import numpy as np
com_wrd_lst = []
common_sites_words = open('C:\common_sites_words.txt', 'r', encoding='utf-8')

for wrd in common_sites_words:
    com_wrd_lst.append(wrd)
com_wrd_lst = np.array(com_wrd_lst)
print(com_wrd_lst)
com_wrd_lst = np.unique(com_wrd_lst)
print(len(com_wrd_lst))
common_sites_words = open('C:\common_sites_words.txt', 'w', encoding='utf-8')
for wrd in list(com_wrd_lst):
    common_sites_words.write(str(wrd))