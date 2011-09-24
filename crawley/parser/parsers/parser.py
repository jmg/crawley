from utils import trim

class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "

    def __init__(self, crawley_line):
        
        self.dsl = crawley_line
    
    def parse(self):
        
        raise Exception("Abstract")

    def can_parse(self):
        
        return "Abstract Error"