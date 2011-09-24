from utils import trim

class Parser(object):
    
    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "

    def __init__(self, crawley_dsl):
        
        self.dsl = trim(crawley_dsl)
    
    def parse(self):
        
        raise Exception("Abstract")

    def can_parse(self):
        
        return "Abstract Error"
    
class CrawleyDSL(object):
    
    def __init__(self, crawley_dsl):
        
        self.dsl = crawley_dsl
        
    def parse(self):
        for n, line in enumerate(dsl.split("\n")):
            Line(line, n).parse()

class Line(object):
    
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "
        
    def __init__(self, crawley_line, line_number):
        self.dsl = crawley_line
        self.number = line_number

        action_section, get_section = self.dsl.split(self.QUERY_SEPARATOR)
        action, properties = action_section.lower().split(self.ACTION_SEPARATOR)

        self.action = action

        self.property_map = {}

        for property_and_values in properties.split():
            key, values =  property_and_values.split(":")
            property_map[key] = utils.remove_braces(values).split(",")

    def is_simple(self):
        
        return len(self.property_map) == 1 and not self.is_recursive()
    
    def is_compound(self):
        
        return not self.is_simple() and not self.is_recursive()
    
    def is_recursive(self):
        
        return self.dsl.count("->") > 0
    
    def parse(self):
        
        DSLAnalizer().parse(self)