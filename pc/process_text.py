import re

__all__ = ('process_text',)

pattern_list = [
    r'[^\u0000-\uFFFF]',

    (r'(?:(?<=\n)|^)作者：[^\n]+\n'
     r'链接：[^\n]+\n'
     r'来源：知乎\n'
     r'著作权归作者所有。商业转载请联系作者获得授权，'
     r'非商业转载请注明出处。(?:$|(?=\n))')
]

def process_text(text):
    for pattern in pattern_list:
        text = re.sub(pattern, '', text)
    return text