from parsers import parsers
from parsers.utils import trim

class DSLAnalizer(object):

    def _detect_parser(self, crawley_dsl):
        return parsers[0](crawley_dsl)
    
    def parse(self, crawley_dsl):
        
        return self._detect_parser(self._trim(crawley_dsl)).parse()
    
    def _trim(self, crawley_dsl):
        return trim(crawley_dsl)