from parser import Parser, ParserException

class CompoundParser(Parser):

    def _get_compound_positional_element(self, count):
        
        if count == 0:
            return ""
        elif count == 1:
            return " if x in "
        else:
            return " and x in "
    
    def _can_parse(self):
        
        return self.dsl.is_compound()
    
    def _get_exception(self):
        
        return ParserException("Can't Parse, only Compound admitted, Line %d" % self.dsl.number)