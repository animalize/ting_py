
__all__ = ('cate_list',)

class Cate:
    def __init__(self, name, code):
        assert '_' not in name, '分类的name里不要有下划线'
        self._name = name
        
        if code:
            self._code = code + '_' + name
        else:
            self._code = code
    
    @property
    def name(self):
        return self._name
    
    @property
    def code(self):
        return self._code

cate_list = [
    Cate(name='自用', code=''),
    Cate(name='共享', code=''),
    None,
    None,
]

# 约束
assert len(cate_list) == 4
assert cate_list[0] is not None
