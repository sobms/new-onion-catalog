def search_url(tag,base_url):
    try:
        url = tag.find('a').get('href')
    except:
        return ''
    try:
        if url[:4] == 'http':
            return url
        else:
            return base_url+url
    except: return ''