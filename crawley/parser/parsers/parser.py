import utils

class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    COMPREHENSION_LIST_TAIL = "]"
    
    def __init__(self, crawley_line):
        
        self.dsl = crawley_line
    
    def _can_parse(self):
        
        raise Exception("Abstract")
    
    def _get_exception(self):
        
        raise Exception("Abstract")

    def _get_compound_positional_element(self, count):
        
        raise Exception("Abstract")

    def _do_parse(self):
        
        raise Exception("Abstract")

    def parse(self):
        
        result = self.RETURN + self._get_comprehension_list_head()

        result += self._do_parse()
        
        return "%s%s" % (result, self.COMPREHENSION_LIST_TAIL)

    def can_parse(self):
        
        if not self._can_parse():
            raise self._get_exception()
        return ""

    def _get_comprehension_list_head(self, head_val='x'):
        return '[%s for %s in ' % (head_val, head_val)
    
class ParserException(Exception):
    
    def __init__(self, message):
        
        self.message = message
        self.args = (message,)
