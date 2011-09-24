import utils
from parser import Parser
from properties import Property
from actions import Action

class OtroParser(Parser):
    
    COMPREHENSION_LIST_HEAD = "[x for x in "
    COMPREHENSION_LIST_TAIL = "]"
    
    def parse(self):
        
        result = self.RETURN + self.COMPREHENSION_LIST_HEAD

        for key, value in self.dsl.properties.iteritems():
            for index, property_element in enumerate(value):
                result += ''.join([utils.not_first_element_plus(index), self.PYQUERY_HEAD, 
                              Property().get(key),
                              utils.trim_single_quotes(property_element),
                              self.CLOSING_PARENTHESIS,
                              Action().get(self.dsl.action)])

        return "%s%s" % (result, self.COMPREHENSION_LIST_TAIL)

    def can_parse(self):
        
        return "" if self.dsl.is_simple() else "Can't Parse, only Simple admitted, Line %d" % self.dsl.number