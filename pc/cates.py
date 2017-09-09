from collections import namedtuple

__all__ = ('cate_list',)

Cate = namedtuple('Cate', ['name', 'code'])

cate_list = [
    Cate(name='自用', code='zzzz_自用'),
    Cate(name='共享', code='共享'),
    None,
    None,
]

# 约束
assert len(cate_list) == 4
assert cate_list[0] is not None
