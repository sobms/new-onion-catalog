products_base = open('', 'r', encoding='utf-8')
data = []
for row in products_base:
    good=row.strip()
    data.append(good)
