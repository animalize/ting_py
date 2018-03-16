try:
    from cate_define import Cate
except:
    from .cate_define import Cate
    
__all__ = ('cate_list', 'host', 'tz2txt_path')

# 定义分类
# 1、总数（包括None）必须是4个。
# 2、name中不能有下划线。
# 3、code为过滤前缀：
#    如果为空字符串，所有人都可以访问。
#    如果不为空字符串，只有设置了相应“过滤前缀”的人才能访问。
cate_list = [
    Cate(name='自用', code=''),
    Cate(name='共享', code=''),
    None,
    None
]

# 服务器地址
host = 'http://192.168.21.60:17828'

# tz2txt.py路径
tz2txt_path = r'D:\git\tz2txt\tz2txt\tz2txt.py'