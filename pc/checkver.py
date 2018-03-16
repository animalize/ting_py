# coding=utf-8

import re

import requests

__all__ = ('check_ver',)

session = requests.Session()
session.trust_env = False

url = 'https://raw.githubuserc1ontent.com/animalize/ting_py/master/launcher.py'

def check_ver(current, full=True):
    try:
        r = session.get(url)
    except:
        return '无法获取GitHub上的页面'
    
    try:
        r.encoding = 'utf-8'
        html = r.text
    except:
        return '无法用utf-8解码“包含版本信息的网页”'
    
    if full:
        p = r'FULL_VERSION\s*=\s*(\d+)'
    else:
        p = r'TING_VERSION\s*=\s*(\d+)'

    m = re.search(p, html)
    if not m:
        return '无法从“包含版本信息的网页”提取最新的版本号'
    
    ver = int(m.group(1))
    if ver > current:        
        b = '当前版本%d，发现新版本%d\n' % (current, ver)
        
        if full:
            a = 'Ting桌面端集成版 检查更新\n'
            c = '到这里下载新版：https://github.com/animalize/ting_py/releases\n'
        else:
            a = 'Ting桌面端 检查更新\n'
            c = '到这里下载新版：https://github.com/animalize/ting_py\n'
            
        s = a + b + c
    else:
        s = '没有发现新版本\n'
    
    return s
