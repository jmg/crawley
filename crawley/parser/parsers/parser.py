from properties import Property
from actions import Action
import utils

class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    COMPREHENSION_LIST_HEAD = "[x for x in "
    COMPREHENSION_LIST_TAIL = "]"
    
    def __init__(self, crawley_line):
        
        self.dsl = crawley_line
    
    def parse(self):
        
        result = self.RETURN + self.COMPREHENSION_LIST_HEAD

        count = 0
        for key, value in self.dsl.properties.iteritems():
            for index, property_element in enumerate(value):
                result += ''.join([self._get_compound_positional_element(count),
                          utils.not_first_element_plus(index), self.PYQUERY_HEAD, 
                          Property().get(key),
                          utils.trim_single_quotes(property_element),
                          self.CLOSING_PARENTHESIS,
                          Action().get(self.dsl.action)])
            count += 1
        
        return "%s%s" % (result, self.COMPREHENSION_LIST_TAIL)


    def can_parse(self):
        
        if not self._can_parse():
            raise self._get_exception()
        return ""
    
    def _can_parse(self):
        
        raise Exception("Abstract")
    
    def _get_exception(self):
        
        raise Exception("Abstract")

    def _get_compound_positional_element(self, count):
        
        raise Exception("Abstract")

class ParserException(Exception):
    
    def __init__(self, message):
        
        self.message = message
        self.args = (message,)