import utils
from properties import Property
from actions import Action

class Parser(object):

    CLOSING_PARENTHESIS = "')"
    PYQUERY_HEAD = "PyQuery(html).query('"
    RETURN = "return "
    ACTION_SEPARATOR = " < "
    QUERY_SEPARATOR = " => "

    def parse(self, crawleyDSL):
        
        parsingString = crawleyDSL.split(self.QUERY_SEPARATOR)
        action, properties = parsingString[0].lower().split(self.ACTION_SEPARATOR)
        getSection = parsingString[1]

        return self.getFinalQuery(action, properties)
        
    def getFinalQuery(self, action, properties):
        
        propertyMap = {}

        for name in properties.split(): 
            propertyMap[name.split(":")[0]] = utils.removeBraces(name.split(":")[1]).split(",")

        result = self.RETURN + utils.compoundPropertyStartingBraces(properties)
        
        for property in propertyMap.keys():
            for j, x in enumerate(propertyMap.get(property)):
                result = "%s%s%s%s%s%s%s" % (result, "" if j == 0 else ", ", self.PYQUERY_HEAD, 
                         Property.getProperty(property),
                         utils.trimSingleQuotes(propertyMap.get(property)[j]),
                         self.CLOSING_PARENTHESIS,
                         Action.getAction(action))
                
        res = "%s%s" % (result, utils.compoundPropertyEndingBraces(properties))
        print res
        return res
