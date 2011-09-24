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

def trim(a_string):
    
    return _replace_by_regex(a_string, r'\s+')

def replace_escape_char(a_string):
    
    return _replace_by_regex(a_string, r'\[\s|\n]*')

def _replace_by_regex(a_string, a_pattern, replace_char=' '):
    
    return re.sub(re.compile(a_pattern), replace_char, a_string)

def not_first_element_plus(index):
    
    return "" if index == 0 else " + "

class UncasedDict(dict):
    
    def __getitem__(self, key):
        
        return dict.__getitem__(self, self._check_key_case(key))
        
    def __setitem__(self, key, value):
        
        dict.__setitem__(self, self._check_key_case(key), value)

    def __delitem__(self, key):
        
        dict.__delitem__(self, self._check_key_case(key))
    
    def _check_key_case(self, key):
    
        if isinstance(key, basestring):
            key = key.lower()
        return key
