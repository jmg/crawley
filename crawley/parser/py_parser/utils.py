"""
    Parser utils
"""

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
