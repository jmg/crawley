from parsers import parsers

class DSLAnalizer(object):

    def _detect_parser(self, crawley_line):
        
        for parser in parsers:
            parser_instance = parser(crawley_line)
            error = parser_instance.can_parse()
            if not error:
                return parser_instance
        raise Exception("Couldn't find any compatible parser: %s") % error
    
    def parse(self, crawley_line):
        
        return self._detect_parser(crawley_line).parse()
    