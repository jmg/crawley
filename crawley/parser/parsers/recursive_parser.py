from parser import Parser, ParserException

class RecursiveParser(Parser):
    
    def _can_parse(self):
        
        return self.dsl.is_recursive()
    
    def _get_exception(self):
        
        return ParserException("Can't Parse, only Recursive admitted, Line %d" % self.dsl.number)