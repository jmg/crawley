"""
    Parser utils
"""

def removeBraces(propertyValues):
    
    return propertyValues.replace("[", "").replace("]", "")

def compoundPropertyEndingBraces(properties):
    
    return compoundPropertyBraces(properties, False)

def compoundPropertyStartingBraces(properties):
    
    return compoundPropertyBraces(properties, True)

def compoundPropertyBraces(properties, starting_position):
    
    if "[" in properties and "]" in properties:
        if starting_position:
            return "["
        return "]"
    return ""

def trimSingleQuotes(htmlElement):

    return htmlElement.replace("'", "")
