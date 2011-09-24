import utils

class CrawleyDSL(object):
    
    def __init__(self, crawley_dsl):
        
        self.dsl = crawley_dsl
        
    def parse(self):
        
        for n, line in self._get_lines():
            Line(line, n).parse()

    def _get_lines(self):
        
        return enumerate(utils.replace_escape_char(self.dsl, "\\\n").split("\n"))

class Line(object):
    
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "
    RECURSION_SEPARATOR = " -> "
    TAG_PROPERTY_SEPARATOR = ":"
    INTER_PROPERTY_SEPARATOR = ","
        
    def __init__(self, crawley_line, line_number):
        
        self.dsl = crawley_line
        self.number = line_number

        action_section, get_section = self.dsl.split(self.QUERY_SEPARATOR)
        action, properties = action_section.lower().split(self.ACTION_SEPARATOR)

        self.action = action

        self.properties = self._get_properties(properties)

    def is_simple(self):
        
        return len(self.properties) == 1 and not self.is_recursive()
    
    def is_compound(self):
        
        return not self.is_simple() and not self.is_recursive()
    
    def is_recursive(self):
        
        return self.dsl.count(self.RECURSION_SEPARATOR) > 0
    
    def parse(self):
        
        DSLAnalizer().parse(self)

    def _get_properties(self, properties):

        property_map = {}
        for property_and_values in properties.split():
            key, values = property_and_values.split(self.TAG_PROPERTY_SEPARATOR)
            property_map[key] = utils.remove_braces(values).replace(" ", "").split(self.INTER_PROPERTY_SEPARATOR)
        
        return property_map