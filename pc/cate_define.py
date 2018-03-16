
class Cate:
    def __init__(self, name, code):
        assert '_' not in name, '分类的name里不要有下划线'
        self._name = name
        
        if code:
            self._code = code + '_' + name
        else:
            self._code = name
    
    @property
    def name(self):
        return self._name
    
    @property
    def code(self):
        return self._code

