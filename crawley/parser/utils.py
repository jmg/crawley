"""
    Parser utils
"""
import re

def remove_braces(property_values):
    
    return property_values.replace("[", "").replace("]", "")

def compound_property_ending_braces(properties):
    
    return compound_property_braces(properties, False)

def compound_property_starting_braces(properties):
    
    return compound_property_braces(properties, True)

def compound_property_braces(properties, starting_position):
    
    if "[" in properties and "]" in properties:
        if starting_position:
            return "["
        return "]"
    return ""

def trim_single_quotes(html_element):

    return html_element.replace("'", "")

def intersect(first_list, second_list):

    return [x for x in first_list if x in second_list]

def trim(a_string):
    
    pattern = re.compile(r'\s+')
    return re.sub(pattern, ' ', a_string)

def not_first_element_comma(index):
    
    return "" if index == 0 else ", "

class UncasedDict(dict):
    
    def __getitem__(self, key):
        
        return dict.__getitem__(self._check_key_case(key))
        
    def __setitem__(self, key, value):
        
        dict.__setitem__(self._check_key_case(key), value)
    
    def _check_key_case(self, key):
    
        if isinstance(key, basestring):
            key = key.lower()
        return key
