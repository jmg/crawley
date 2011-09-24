from parser import Parser, ParserException

class SimpleParser(Parser):
    
    def _get_compound_positional_element(self, count):
        
        return ""

    def _can_parse(self):
        
        return self.dsl.is_simple()
    
    def _get_exception(self):
        
        return ParserException("Can't Parse, only Simple admitted, Line %d" % self.dsl.number)