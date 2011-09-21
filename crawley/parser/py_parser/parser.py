import utils
from properties import Property
from actions import Action

class Parser(object):

    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "

    def parse(self, crawley_DSL):
        
        action_section, get_section = crawley_DSL.split(self.QUERY_SEPARATOR)
        action, properties = action_section.lower().split(self.ACTION_SEPARATOR)

        return self.get_final_query(action, properties)
        
    def get_final_query(self, action, properties):
        
        property_map = {}

        for name in properties.split(): 
            property_map[name.split(":")[0]] = utils.remove_braces(name.split(":")[1]).split(",")

        result = self.RETURN + utils.compound_property_starting_braces(properties)
        
        for property in property_map.keys():
            for index, property_element in enumerate(property_map.get(property)):
                result = ''.join([result, "" if index == 0 else ", ", self.PYQUERY_HEAD, 
                                  Property().get(property),
                                  utils.trim_single_quotes(property_element),
                                  self.CLOSING_PARENTHESIS,
                                  Action().get(action)])
                
        return "%s%s" % (result, utils.compound_property_ending_braces(properties))
