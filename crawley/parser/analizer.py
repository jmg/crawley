from parsers import parsers

class DSLAnalizer(object):

    def _detect_parser(self, crawley_dsl):
        
        for parser in parsers:
            parser_instance = parser(crawley_dsl)
            error = parser_instance.can_parse()
            if not error:
                return parser_instance
        raise Exception("Couldn't find any compatible parser: %s") % error
    
    def parse(self, crawley_dsl):
        
        return self._detect_parser(crawley_dsl).parse()
    