import json

import requests

host = 'http://192.168.21.60:17828'
#host = 'http://127.0.0.1:17828'

def post_article(title, text, cate):
    url = host + '/post_article'

    values = {'title': title,
              'text': text,
              'cate': cate}
    
    d = json.dumps(values, ensure_ascii=False)

    try:
        r = requests.post(url, data=d.encode('gb18030'))
        return r.text == 'ok'
    except:
        return False
    

def get_list():
    url = host + '/get_list'
    
    r = requests.get(url)
    r.encoding = 'gb18030'
    
    o = r.json()
    assert type(o) == list
    
    return o

def get_article(aid):
    url = host + '/get_article'

    d = {'aid': aid}
    r = requests.get(url, params=d)
    r.encoding = 'gb18030'
    
    text = r.text
    
    return text
    
    