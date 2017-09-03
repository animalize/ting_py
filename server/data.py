import re
import json
import os
import binascii
import time

ENCODING = 'gb18030'
JSON_FILE = 'data.json'

# 数据目录，创建
dir_path = os.path.dirname(os.path.abspath(__file__))
dir_path = os.path.join(dir_path, 'data')

if not os.path.isdir(dir_path):
    try:
        os.mkdir(dir_path)
    except:
        pass

# json对象
try:
    path = os.path.join(dir_path, JSON_FILE)
    with open(path, encoding=ENCODING) as f:
        l = json.load(f)
except:
    # (cate, aid, chars, title)
    l = []


def count_chinese(string):
    '统计汉字字数，不含汉字标点符号'
    count = 0
    for c in string:
        c = ord(c)
        # CJK统一汉字                  20,950
        # CJK统一汉字扩展A区      6,582
        # CJK兼容汉字                  472
        # CJK统一汉字扩展B~E区   52844
        if 0x4E00 <= c <= 0x9FFF or \
           0x3400 <= c <= 0x4DBF or \
           0xF900 <= c <= 0xFAFF or \
           0x20000 <= c <= 0x2EBEF:
            count += 1
    return count


def add_article(title, text, cate):
    '保存一篇文章'
    assert type(title) == type(text) == type(cate) == str

    # 编码
    b = text.encode(ENCODING)

    # aid
    unixtime = int(time.time())
    crc = binascii.crc32(b)
    aid = '{}_{:08x}'.format(unixtime, crc)

    # 保存文章
    path = os.path.join(dir_path, aid)
    with open(path, 'wb') as f:
        f.write(b)

    # 生成标题
    title = title.strip()
    if not title:
        title = text[:47] + '...'
    title = re.sub(r'\s+', ' ', title)

    # 字数
    chn_count = count_chinese(text)

    # json
    one = {'cate': cate,
           'aid': aid,
           'title': title,

           'time': unixtime,
           'cjk_chars': chn_count,
           'file_size': len(b),
           'crc32': crc,
           }
    l.append(one)

    # json文件
    path = os.path.join(dir_path, JSON_FILE)
    with open(path, 'w', encoding=ENCODING) as f:
        json.dump(l, f, ensure_ascii=False)


def get_list():
    '得到列表'
    return l


def get_article(aid):
    '从aid得到文章内容'
    try:
        path = os.path.join(dir_path, aid)
        with open(path, encoding=ENCODING) as f:
            text = f.read()
    except:
        return None
    else:
        return text


def del_article(del_lst):
    # 删除文章
    for aid in del_lst:
        path = os.path.join(dir_path, aid)
        try:
            os.remove(path)
        except:
            pass
    
    # 更新列表
    del_set = set(del_lst)
    global l
    l = [one for one in l if one['aid'] not in del_set]
    
    # json文件
    path = os.path.join(dir_path, JSON_FILE)
    with open(path, 'w', encoding=ENCODING) as f:
        json.dump(l, f, ensure_ascii=False)
