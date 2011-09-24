from utils import trim

class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    COMPREHENSION_LIST_HEAD = "[x for x in "
    COMPREHENSION_LIST_TAIL = "]"
    
    def __init__(self, crawley_line):
        
        self.dsl = crawley_line
    
    def parse(self):
        
        raise Exception("Abstract")

    def can_parse(self):
        
        if not self._can_parse():
            raise self._get_exception() 
    
    def _can_parse(self):
        
        raise Exception("Abstract")
    
    def _get_exception(self):
        
        raise Exception("Abstract")

class ParserException(Exception):
    
    def __init__(self, message):
        
        self.message = message