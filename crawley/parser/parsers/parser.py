class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "

    def __init__(self, crawley_dsl):
        self.dsl = crawley_dsl
    
    def parse(self):
        raise Exception("Abstract")
