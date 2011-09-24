import utils
from parser import Parser
from properties import Property
from actions import Action

class OtroParser(Parser):
    
    COMPREHENSION_LIST_HEAD = "[x for x in "
    COMPREHENSION_LIST_TAIL = "]"
    
    def parse(self):
        
        action_section, get_section = utils.trim(self.dsl).split(self.QUERY_SEPARATOR)
        action, properties = action_section.lower().split(self.ACTION_SEPARATOR)

        property_map = {}

        for property_and_values in properties.split():
            key, values =  property_and_values.split(":")
            property_map[key] = utils.remove_braces(values).split(",")

        result = self.RETURN + self.COMPREHENSION_LIST_HEAD \
                 + utils.compound_property_starting_braces(properties)
        
        for key, value in property_map.iteritems():
            for index, property_element in enumerate(value):
                result += ''.join([utils.not_first_element_comma(index), self.PYQUERY_HEAD, 
                                  Property().get(key),
                                  utils.trim_single_quotes(property_element),
                                  self.CLOSING_PARENTHESIS,
                                  Action().get(action)])
                
        return "%s%s" % (result, utils.compound_property_ending_braces(properties))

    def can_parse(self):
        
        return ""