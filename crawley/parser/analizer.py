from parsers import parsers
from parsers.parser import ParserException

class DSLAnalizer(object):

    def _detect_parser(self, crawley_line):
        
        error = ParserException("")
        
        for parser in parsers:
            parser_instance = parser(crawley_line)
            try:
                parser_instance.can_parse()
                return parser_instance
            except ParserException, e:
                error = e  
        raise AnalizerException("Line not parsable", error) 
    
    def parse(self, crawley_line):
        
        return self._detect_parser(crawley_line).parse()
    
class AnalizerException(Exception):
    
    def __init__(self, message):
        
        Exception(self, message)
        
    def __init__(self, message, inner_exception):
        
        Exception(self, message, inner_exception)