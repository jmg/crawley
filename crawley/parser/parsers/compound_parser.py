from parser import Parser, ParserException
from properties import Property
from actions import Action
import utils


class CompoundParser(Parser):

    def _do_parse(self):
        result = ""
        
        for count, (key, value) in enumerate(self.dsl.properties.iteritems()):
            for index, property_element in enumerate(value):
                result += ''.join([self._get_compound_positional_element(count),
                          utils.not_first_element_plus(index), self.PYQUERY_HEAD,
                          Property().get(key),
                          utils.trim_single_quotes(property_element),
                          self.CLOSING_PARENTHESIS,
                          Action().get(self.dsl.action)])
        return result

    def _get_compound_positional_element(self, count):
        
        if count == 0:
            return ""
        elif count == 1:
            return " if x in "
        else:
            return " and x in "
    
    def _can_parse(self):
        
        return self.dsl.is_compound() or self.dsl.is_simple()
    
    def _get_exception(self):
        
        return ParserException("Can't Parse, only Simple and Compound admitted, Line %d" % self.dsl.number)