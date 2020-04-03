def search_url(tag,base_url):
    try:                                 #first case
        url = tag.find('a').get('href')
    except:
        url = ''

    try:                                 #second case
        if url == '':
            url = tag.find('form').get('action')
    except:
        url = ''

    try:                                 # third case
        if url == '':
            url = tag.parent.find('form').get('action')
    except:
        url = ''
    try:
        if url[:4] == 'http':
            return url
        else:
            return base_url+url
    except: return ''