import json

import requests

try:
    import vars
except:
    from . import vars

session = requests.Session()
session.trust_env = False

def post_article(title, text, cate):
    url = vars.host + '/post_article'

    values = {'title': title,
              'text': text,
              'cate': cate}
    
    d = json.dumps(values, ensure_ascii=False)

    try:
        r = session.post(url, data=d.encode('gb18030'))
        return r.text == 'ok'
    except Exception as e:
        print(e)
        return False
    

def get_list():
    url = vars.host + '/get_list'
    
    try:
        r = session.get(url)
        r.encoding = 'gb18030'
        
        o = r.json()
        assert type(o) == list
        
        return o[::-1]
    except:
        return []


def get_article(aid):
    url = vars.host + '/get_article'

    d = {'aid': aid}
    
    try:
        r = session.get(url, params=d)
        r.encoding = 'gb18030'
        
        text = r.text
        return text
    except:
        return ''
    