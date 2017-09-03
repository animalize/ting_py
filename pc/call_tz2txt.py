import os
import re
import tempfile

from vars import tz2txt_path

__all__ = ('getArticle')

def remove(fpath):
    try:
        os.remove(fpath)
    except Exception as e:
        print(e)
        
        
# 验证url
def is_url(url):
    p = re.compile(
        r'^https?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE|re.A)
    if p.match(url):
        return True
    else:
        return False


def getArticle(url):
    if not is_url(url):
        return '', ''
    
    # 得到临时文件名
    with tempfile.NamedTemporaryFile('wb') as f:
        fpath = f.name
        print('临时文件：', fpath)

    # tz2txt
    cmd = 'python %s a -u %s -t %d -o %s -s none' % (
        tz2txt_path, url, -1, fpath)
    os.system(cmd)

    # 提取
    try:
        with open(fpath, encoding='GB18030') as f:
            content = f.read()
    except:
        remove(fpath)
        return '', ''

    p = r'(?s)^标题：([^\n]*).*?\n起始网址：[^\n]*\n(.*)$'
    m = re.search(p, content)
    if m:
        title = m.group(1).strip()
        text = m.group(2).strip()
    else:
        title = text = ''

    remove(fpath)

    return title, text
