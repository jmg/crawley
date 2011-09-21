from actions import *
from properties import *

class Parser(object):

    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "
    actionElements = {}
    propertyElements = {}

    def __init__(self):
        
        self.populateMaps()

    def populateMaps(self):
        
        self.populateActions()
        self.populateProperties()

    def populateProperties(self):
        
        self.propertyElements["id"] = IDProperty()
        self.propertyElements["tag"] = TagProperty()
        self.propertyElements["class"] = ClassProperty()

    def populateActions(self):
        
        self.actionElements["first"] = FirstAction()
        self.actionElements["last"] = LastAction()
        self.actionElements["all"] = AllAction()

    def parse(self, crawleyDSL):
        
        parsingString = crawleyDSL.split(self.QUERY_SEPARATOR)
        action, properties = parsingString[0].lower().split(self.ACTION_SEPARATOR)
        getSection = parsingString[1]

        return self.getFinalQuery(action, properties)
        
    def getFinalQuery(self, action, properties):
        
        propertyMap = {}

        for name in properties.split(): 
            propertyMap[name.split(":")[0]] = self.removeBraces(name.split(":")[1]).split(",")

        result = self.RETURN + self.compoundPropertyStartingBraces(properties)
        
        for property in propertyMap.keys():
            for j, x in enumerate(propertyMap.get(property)):
                result = "%s%s%s%s%s%s%s" % (result, "" if j == 0 else ", ", self.PYQUERY_HEAD, 
                         self.propertyElements.get(property),
                         self.trimSingleQuotes(propertyMap.get(property)[j]),
                         self.CLOSING_PARENTHESIS,
                         self.actionElements.get(action))
                
        res = "%s%s" % (result, self.compoundPropertyEndingBraces(properties))
        print res
        return res

    def removeBraces(self, propertyValues):
        
        return propertyValues.replace("[", "").replace("]", "")

    def compoundPropertyEndingBraces(self, properties):
        
        return self.compoundPropertyBraces(properties, False)

    def compoundPropertyStartingBraces(self, properties):
        
        return self.compoundPropertyBraces(properties, True)

    def compoundPropertyBraces(self, properties, starting_position):
        
        if "[" in properties and "]" in properties:
            if starting_position:
                return "["
            return "]"
        return ""

    def trimSingleQuotes(self, htmlElement):

        return htmlElement.replace("'", "")
